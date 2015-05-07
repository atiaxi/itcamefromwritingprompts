import os
from datetime import datetime, timedelta
from re import sub

import praw
from pytz import UTC

from icfwp import app, PUNCTUATION, STRIPPABLE_PUNCTUATION
from markov.model import TransitionTable


USERAGENT = "Writingprompts title scraper by /u/reostra"


def now():
    result = datetime.utcnow()
    result.replace(tzinfo=UTC)
    return result


def expand_punctuation(word):
    result = []
    word = word.strip()
    if word[0] in PUNCTUATION:
        result.append(word[0])
        word = word[1:]
    if word and word[-1] in PUNCTUATION:
        result.append(word[:-1])
        result.append(word[-1])
    elif word:
        result.append(word)
    return " ".join(result)


def sanitize(title):
    # Remove all the [WP], [TT], etc tags
    title = sub("\[.*\]", "", title)

    # Get rid of the quotes and stuff, it makes for terrible markovs
    for punct in STRIPPABLE_PUNCTUATION:
        title = title.replace(punct, "")

    # Expand all punctuation
    result = [expand_punctuation(word) for word in title.split()]

    return " ".join(result)


def main(days=1):
    count = 0

    # Load the brain, if it's there
    markov_filename = app.config['MARKOV_STORAGE']
    if os.path.isfile(markov_filename):
        tt = TransitionTable.from_filename(markov_filename)
    else:
        tt = TransitionTable()

    cutoff = now() - timedelta(days=days)
    reddit = praw.Reddit(user_agent=USERAGENT)
    hq = reddit.get_subreddit('writingprompts')
    submissions = hq.get_new(limit=None)
    for submission in submissions:
        created = datetime.utcfromtimestamp(submission.created_utc)
        created.replace(tzinfo=UTC)
        if created < cutoff:
            break

        tt.add_from_string(sanitize(submission.title))

    # Save
    tt.persist(markov_filename)
    print "Populated %d entries over %d days" % (count, days)

if __name__ == '__main__':
    main(days=1)
