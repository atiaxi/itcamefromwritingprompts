import json
from collections import defaultdict, Counter
from itertools import izip, tee
from random import randint


# From the itertool examples
# at https://docs.python.org/2/library/itertools.html#recipes
def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return izip(a, b)


class TransitionEntry(object):
    def __init__(self):
        self.destinations = Counter()
        self.total = 0

    @classmethod
    def from_dict(cls, d):
        result = cls()
        for dest, count in d.iteritems():
            result.add(dest, count)
        return result

    def add(self, dest, amount=1):
        self.destinations[dest] += amount
        self.total += amount

    def choose(self):
        assert self.total
        cur_total = 0
        chosen = randint(0, self.total-1)
        for dest, count in self.destinations.iteritems():
            cur_total += count
            if cur_total > chosen:
                return dest
        # Should never happen
        raise AssertionError("A transition should have been chosen! %d of %d" %
                             (cur_total, chosen))

    def to_dict(self):
        return self.destinations

    # Wrong, but I'm lazy
    def __repr__(self):
        return repr(self.destinations)


# TODO: Support order N>1 models
class TransitionTable(object):
    def __init__(self):
        self.transitions = defaultdict(TransitionEntry)
        self.total = 0

    @classmethod
    def from_dict(cls, d):
        result = cls()
        for src, dest_dict in d.iteritems():
            result.transitions[src] = TransitionEntry.from_dict(dest_dict)
        return result

    @classmethod
    def from_filename(cls, filename):
        with open(filename, 'r') as infile:
            result = cls.from_dict(json.load(infile))
        return result

    def add(self, src, dest, amount=1):
        self.transitions[src].add(dest, amount)
        self.total += amount

    def add_from_string(self, item):
        items = item.split()
        items.insert(0, '')
        items.append('')
        for src, dest in pairwise(items):
            self.add(src, dest)

    def persist(self, filename):
        with open(filename, 'w') as outfile:
            json.dump(self.to_dict(), outfile)

    def random_transition_from(self, src):
        entry = self.transitions[src]
        return entry.choose()

    def to_dict(self):
        result = {
            src: dest.to_dict() for src, dest in self.transitions.iteritems()
        }
        return result

    def __iter__(self):
        curr = self.random_transition_from('')
        while curr != '':
            yield curr
            curr = self.random_transition_from(curr)
