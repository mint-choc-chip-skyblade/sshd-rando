"""
Algebraic simplification techniques treat all requirements as unrelated variables
and allow us to turn our two-level DNF/sum-of-products form into a simpler
multi-level expression.

The general approach is described in:
 * https://faculty.sist.shanghaitech.edu.cn/faculty/zhoupq/Teaching/Spr16/07-Multi-Level-Logic-Synthesis.pdf
 * https://www2.eecs.berkeley.edu/Pubs/TechRpts/1989/ERL-89-49.pdf (pp. 41-70)

This approach does not exploit boolean properties like x & !x = false or x | !x = true
but logic doesn't need this since we only have positive terms. The other thing
these techniques don't handle are "implies" relations like Beetle x 2 => Beetle x 1,
so we may use different techniques for those.
"""

from dataclasses import dataclass
from typing import Callable

from .bits import BitIndex, DNF, BitVector, included_in
from ..requirements import Requirement, RequirementType


@dataclass
class FoundKernel:
    kernel: list[BitVector]
    co_kernel: BitVector


def dnf_to_expr(bit_index: BitIndex, dnf: DNF) -> Requirement:
    if dnf.is_trivially_false():
        return Requirement(RequirementType.IMPOSSIBLE)

    if dnf.is_trivially_true():
        return Requirement(RequirementType.NOTHING)

    # really make sure no dupes exist, not sure if needed
    dnf = dnf.dedup()

    # TODO at this point we must remove weaker requirements. E.g.
    # imagine Beedle existed in this rando and an item required
    # (Wallet x1 and Wallet x2) or (Wallet x1 and ExtraWallet x1 and ExtraWallet x2)
    # then this code would pull out Wallet x1 first, resulting in
    # Wallet x1 and (Wallet x2 or ExtraWallet x1 and ExtraWallet x2) which is not
    # reasonable at all and at that point not even the TWWR-Tracker simplifications can save us

    # map to bitvec
    expr = [
        BitVector([bit for bit in range(bit_index.counter) if ((1 << bit) & t)])
        for t in dnf.terms
    ]

    common_factors_: set[int] = set(expr[0].ints())
    for term in expr:
        common_factors_.intersection_update(term.ints())

    var_set: set[int] = set()
    for term in expr:
        for c in common_factors_:
            term.clear(c)
        for b in term.ints():
            var_set.add(b)

    common_factors = sorted(list(common_factors_))

    variables = sorted(list(var_set))

    if not variables:
        return Requirement(
            RequirementType.AND, [bit_index.reverse_index[i] for i in common_factors]
        )

    kernels = find_kernels(expr, variables, BitVector([]))
    kernels = [k for k in kernels if not k.co_kernel.is_empty()]

    # columns are unique cubes in all kernels
    columns: list[BitVector] = []
    for kernel in kernels:
        for k_cube in kernel.kernel:
            if not any(k_cube.equals(c) for c in columns):
                columns.append(k_cube)

    rows = kernels
    if rows and columns:
        matrix = []
        for _ in rows:
            matrix.append([0 for _ in columns])

        for col, k_cube in enumerate(columns):
            for row, co_kernel in enumerate(rows):
                if any(k_cube.equals(k) for k in co_kernel.kernel):
                    matrix[row][col] = 1

        row_weight = lambda row: rows[row].co_kernel.size() + 1
        col_weight = lambda col: columns[col].size()

        def value(col: int, row: int):
            cpy = rows[row].co_kernel.copy()
            cpy.or_(columns[col])
            return cpy.size()

        def literals_saved(rect: tuple[list[int], list[int]]) -> int:
            rect_rows, rect_cols = rect
            weight = 0
            for row in rect_rows:
                for col in rect_cols:
                    if matrix[row][col]:
                        weight += value(col, row)

            for row in rect_rows:
                weight -= row_weight(row)
            for col in rect_cols:
                weight -= col_weight(col)

            return weight

        all_rects: list[tuple[list[int], list[int]]] = []
        gen_rectangles(
            list(range(len(rows))),
            list(range(len(columns))),
            matrix,
            lambda rows, cols: all_rects.append((rows, cols)),
        )

        if all_rects:
            best = max(all_rects, key=literals_saved)
            best_cols = best[1]

            divisor = [columns[c] for c in best_cols]
            quot, remainder = algebraic_division(expr, divisor)

            quot_e = dnf_to_expr(bit_index, DNF([c.bitset for c in quot]))
            div_e = dnf_to_expr(bit_index, DNF([c.bitset for c in divisor]))

            product = Requirement(
                RequirementType.AND,
                [
                    quot_e,
                    div_e,
                ],
            )

            if remainder:
                sum = Requirement(
                    RequirementType.OR,
                    [
                        product,
                        dnf_to_expr(bit_index, DNF([c.bitset for c in remainder])),
                    ],
                )
            else:
                sum = product

            if common_factors:
                return Requirement(
                    RequirementType.AND,
                    [*[bit_index.reverse_index[bit] for bit in common_factors], sum],
                )
            else:
                return sum

    terms = Requirement(
        RequirementType.OR,
        [
            Requirement(
                RequirementType.AND, [bit_index.reverse_index[i] for i in c.ints()]
            )
            for c in expr
        ],
    )
    if common_factors:
        return Requirement(
            RequirementType.AND,
            [
                *[bit_index.reverse_index[i] for i in common_factors],
                terms,
            ],
        )
    else:
        return terms


def gen_rectangles(
    rows: list[int],
    cols: list[int],
    matrix: list[list[int]],
    callback: Callable[[list[int], list[int]], None],
):
    for row in rows:
        ones = [c for c in cols if matrix[row][c]]
        if len(ones) and not any(
            r != row and all(not c in ones or matrix[r][c] for c in cols) for r in rows
        ):
            callback([row], ones)

    for col in cols:
        ones = [r for r in rows if matrix[r][col]]
        if len(ones) and not any(
            c != col and all(not r in ones or matrix[r][c] for r in rows) for c in cols
        ):
            callback(ones, [col])

    gen_rectangles_recursive(rows, cols, matrix, 0, [], [], callback)


def gen_rectangles_recursive(
    all_rows: list[int],
    all_cols: list[int],
    matrix: list[list[int]],
    index: int,
    _rect_rows: list[int],
    rect_cols: list[int],
    callback: Callable[[list[int], list[int]], None],
):
    for c in all_cols:
        if c >= index and len([row for row in all_rows if matrix[row][c]]) >= 2:
            m1 = [
                row.copy() if matrix[row_idx][c] else [0 for _ in range(len(row))]
                for row_idx, row in enumerate(matrix)
            ]
            rect_1_rows = [row for row in all_rows if matrix[row][c]]
            rect_1_cols = rect_cols.copy()

            prune = False
            for c1 in all_cols:
                if len([row for row in all_rows if m1[row][c1]]) == len(
                    [row for row in all_rows if matrix[row][c]]
                ):
                    if c1 < c:
                        prune = True
                        break
                    else:
                        rect_1_cols.append(c1)
                        for row in all_rows:
                            m1[row][c1] = 0

            if not prune:
                callback(rect_1_rows, rect_1_cols)
                gen_rectangles_recursive(
                    all_rows, all_cols, m1, c, rect_1_rows, rect_1_cols, callback
                )


def find_kernels(
    cubes: list[BitVector],
    variables: list[int],
    co_kernel_path: BitVector,
    seen_co_kernels: list[BitVector] | None = None,
    min_idx=0,
):
    if seen_co_kernels is None:
        seen_co_kernels = []

    kernels: list[FoundKernel] = []
    for idx, bit in enumerate(variables):
        if idx < min_idx:
            continue
        s = [c for c in cubes if c.test(bit)]
        if len(s) >= 2:
            co = s[0].copy()
            for c in s:
                co.and_(c)
            sub_path = co_kernel_path.copy()
            sub_path.or_(co)
            quot, _remainder = algebraic_division(cubes, [co])
            sub_kernels = find_kernels(
                quot, variables, sub_path, seen_co_kernels, idx + 1
            )

            for sub in sub_kernels:
                if not any(
                    seen_co.equals(sub.co_kernel) for seen_co in seen_co_kernels
                ):
                    seen_co_kernels.append(sub.co_kernel)
                    kernels.append(sub)

    if not any(seen_co.equals(co_kernel_path) for seen_co in seen_co_kernels):
        kernels.append(FoundKernel(cubes, co_kernel_path.copy()))

    return kernels


def algebraic_division(expr: list[BitVector], divisor: list[BitVector]):
    quot: list[BitVector] = None
    for div_cube in divisor:
        c = [e.copy() for e in expr if div_cube.is_subset_of(e)]
        if not c:
            return [], expr

        for ci in c:
            for bit in div_cube.ints():
                ci.clear(bit)

        if not quot:
            quot = c
        else:
            quot = [qc for qc in quot if any(cc.equals(qc) for cc in c)]

    product = (
        DNF([i.bitset for i in quot]).and_(DNF([i.bitset for i in divisor])).dedup()
    )
    remainder = [
        e
        for e in expr
        if not any(
            included_in(product_term, e.bitset) for product_term in product.terms
        )
    ]
    return quot, remainder
