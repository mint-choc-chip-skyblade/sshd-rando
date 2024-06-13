import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from logic.requirements import Requirement, RequirementType
from logic.tooltips.bits import DNF, BitIndex
from logic.tooltips.simplify_algebraic import dnf_to_expr
from logic.tooltips.tooltips import print_req


def simplify_dnf(terms: list[list[str]]):
    bit_index = BitIndex()
    terms_bits: list[int] = []
    for term in terms:
        term_bit = 0
        for item in term:
            term_bit |= 1 << bit_index.req_bit(
                Requirement(RequirementType.ITEM, [item])
            )
        terms_bits.append(term_bit)
    dnf = DNF(terms_bits)
    expr = dnf_to_expr(bit_index, dnf)
    return print_req(expr)


def test_simplify():
    terms = [
        ["Mitts", "Bow"],
        ["Mitts", "Clawshots"],
        ["Mitts", "Slingshot"],
        ["Mitts", "Beetle"],
        ["Bomb", "Bow"],
        ["Bomb", "Clawshots"],
        ["Bomb", "Slingshot"],
        ["Bomb", "Beetle"],
    ]

    assert (
        simplify_dnf(terms)
        == "((Mitts or Bomb) and (Bow or Clawshots or Slingshot or Beetle))"
    )


def test_simplify_2():
    terms = [
        ["Progressive Sword", "Progressive Pouch", "Empty Bottle", "Amber Tablet"],
        ["Whip", "Progressive Pouch", "Empty Bottle", "Amber Tablet"],
        ["Bomb Bag", "Amber Tablet"],
        ["Progressive Slingshot", "Progressive Pouch", "Empty Bottle", "Amber Tablet"],
        ["Progressive Beetle", "Amber Tablet", "Progressive Beetle x 2"],
        ["Progressive Beetle", "Progressive Pouch", "Empty Bottle", "Amber Tablet"],
        ["Clawshots", "Progressive Pouch", "Empty Bottle", "Amber Tablet"],
        ["Progressive Bow", "Progressive Pouch", "Empty Bottle", "Amber Tablet"],
    ]

    assert (
        simplify_dnf(terms)
        == "(Amber Tablet and (((Progressive Pouch and Empty Bottle) and (Progressive Sword or Whip or Progressive Slingshot or Progressive Beetle or Clawshots or Progressive Bow)) or (Bomb Bag or (Progressive Beetle and Progressive Beetle x 2))))"
    )
