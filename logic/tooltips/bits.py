from typing import List

from ..requirements import Requirement, RequirementType


class BitVector:
    """
    A bunch of bits with useful functions for or- and and-ing.
    """

    def __init__(self, bits: list[int]):
        self.bitset = 0
        self.intset: set[int] = set()
        for i in bits:
            self.set(i)

    def is_empty(self):
        return self.bitset == 0

    def ints(self):
        # NB sorted for determinism in tooltips code
        return sorted(self.intset)

    def set(self, i: int):
        self.bitset |= 1 << i
        self.intset.add(i)

    def clear(self, i: int):
        if i in self.intset:
            self.intset.remove(i)
            self.bitset = self.bitset & ~(1 << i)

    def test(self, i: int):
        return bool(i in self.intset)

    def copy(self):
        return BitVector(self.ints())

    def size(self):
        return len(self.intset)

    def and_(self, other: "BitVector"):
        self.intset.intersection_update(other.intset)
        self.bitset &= other.bitset

    def or_(self, other: "BitVector"):
        self.intset.update(other.intset)
        self.bitset |= other.bitset

    def is_subset_of(self, other: "BitVector"):
        return included_in(self.bitset, other.bitset)

    def equals(self, other: "BitVector"):
        return self.bitset == other.bitset

    def __repr__(self):
        return str(self.bitset)


def included_in(a: int, b: int) -> bool:
    """
    Checks if b has all the bits a has
    """
    return (a | b) == b


class DNF:
    """
    A logical expression in disjunctive normal form.
    Disjuncts are bit-vectors, but we don't use the BitVector class here
    because it doesn't seem necessary since our bitvectors are small
    and we only need bit set access after the propagation code is done
    """

    def __init__(self, terms: List[int]):
        self.terms = terms

    @staticmethod
    def true():
        return DNF([0])

    @staticmethod
    def false():
        return DNF([])

    def copy(self):
        return DNF(self.terms)

    def is_trivially_false(self):
        return len(self.terms) == 0

    def is_trivially_true(self):
        return any(t == 0 for t in self.terms)

    def or_(self, other: "DNF"):
        return DNF([*self.terms, *other.terms])

    def dedup(self):
        """
        Removes all redundant terms from self.
        """
        filtered = []
        for candidate in self.terms:  # next_term
            to_pop = []
            for existing_idx, existing in enumerate(filtered):
                if included_in(existing, candidate):
                    # existing requires fewer or equal things than candidate
                    break  # next_term
                elif included_in(candidate, existing):
                    # candidate requires strictly fewer things than existing
                    to_pop.append(existing_idx)
            else:
                # did not break to next_term
                for c in reversed(to_pop):
                    if c == len(filtered) - 1:
                        filtered.pop()
                    else:
                        # remove c without shifting elements by replacing
                        # it with the last element
                        filtered[c] = filtered.pop()
                filtered.append(candidate)

        return DNF(filtered)

    def or_useful(self, other: "DNF"):
        """
        Returns useful, self.or_(other)
        useful is True if other contained at least one term that
        was not redundant.
        """
        filtered_self = self.terms.copy()
        filtered_other = []
        useful = False

        for candidate in other.terms:
            for existing in filtered_self:
                if included_in(existing, candidate):
                    break
            else:
                filtered_other.append(candidate)
                useful = True
        return useful, DNF([*filtered_self, *filtered_other])

    def and_(self, other: "DNF"):
        d = []
        for t1 in self.terms:
            for t2 in other.terms:
                d.append(t1 | t2)
        return DNF(d)


class BitIndex:
    """
    Helper class that maps requirements to a bit index for equivalence checking.

    Since we have to map our requirements to a bit-based DNF, everything that can
    appear in tooltips has to get a unique number. This class provides the number
    """

    def __init__(self):
        self.item_bits = {}
        self.wallet_cap = {}
        self.crystal_count = {}
        self.notes = {}
        self.reverse_index: list[Requirement] = []
        self.counter = 0

    def bump(self):
        c = self.counter
        self.counter += 1
        return c

    # TODO optimization: This keeps constructing strings every time
    # we do the partial evaluation, maybe we can be smarter about this
    # by preprocessing some requirements
    def req_bit(self, req: Requirement) -> int:
        match req.type:
            case RequirementType.ITEM:
                item_name = req.args[0]
                item_str = f"{item_name}::1"
                if item_str in self.item_bits:
                    return self.item_bits[item_str]
                else:
                    self.item_bits[item_str] = self.counter
                    self.reverse_index.append(req)
                    return self.bump()
            case RequirementType.COUNT:
                item_name = req.args[1]
                item_count = req.args[0]
                item_str = f"{item_name}::{item_count}"
                if item_str in self.item_bits:
                    return self.item_bits[item_str]
                else:
                    self.item_bits[item_str] = self.counter
                    self.reverse_index.append(req)
                    return self.bump()
            case RequirementType.WALLET_CAPACITY:
                req_str = f"{req.args[0]}"
                if req_str in self.wallet_cap:
                    return self.wallet_cap[req_str]
                else:
                    self.wallet_cap[req_str] = self.counter
                    self.reverse_index.append(req)
                    return self.bump()
            case RequirementType.GRATITUDE_CRYSTALS:
                req_str = f"{req.args[0]}"
                if req_str in self.crystal_count:
                    return self.crystal_count[req_str]
                else:
                    self.crystal_count[req_str] = self.counter
                    self.reverse_index.append(req)
                    return self.bump()
            case RequirementType.TRACKER_NOTE:
                req_str = f"{req.args[0]}"
                if req_str in self.notes:
                    return self.notes[req_str]
                else:
                    self.notes[req_str] = self.counter
                    self.reverse_index.append(req)
                    return self.bump()
            case _:
                raise ValueError("not a tooltip requirement")
