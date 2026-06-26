#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Быстрое нахождение дроби, стоящей слева от a/b
в последовательности Фарея порядка N.
Для данной задачи:
    a/b = 3/7
    N = 1000000
Ответ: 428570/999997, искомый числитель — 428570.
"""

from __future__ import annotations

import argparse
from math import gcd


def extended_gcd(a: int, b: int) -> tuple[int, int, int]:
    """Возвращает (g, x, y), где a*x + b*y = g = gcd(a, b)."""
    old_r, r = a, b
    old_x, x = 1, 0
    old_y, y = 0, 1

    while r:
        q = old_r // r
        old_r, r = r, old_r - q * r
        old_x, x = x, old_x - q * x
        old_y, y = y, old_y - q * y

    return old_r, old_x, old_y


def modular_inverse(a: int, modulus: int) -> int:
    """Возвращает a^(-1) mod modulus."""
    g, x, _ = extended_gcd(a, modulus)
    if g != 1:
        raise ValueError(
            f"Обратный элемент не существует: gcd({a}, {modulus}) = {g}"
        )
    return x % modulus


def left_farey_neighbor(a: int, b: int, limit: int) -> tuple[int, int]:
    """
    Находит непосредственного левого соседа дроби a/b
    среди всех несократимых дробей с знаменателем <= limit.

    Требования:
      0 < a < b;
      gcd(a, b) = 1;
      limit >= b.

    Возвращает пару (numerator, denominator).
    """
    if not (0 < a < b):
        raise ValueError("Требуется правильная положительная дробь: 0 < a < b.")
    if gcd(a, b) != 1:
        raise ValueError("Дробь a/b должна быть несократимой.")
    if limit < b:
        raise ValueError("Для данного алгоритма требуется limit >= b.")

    # Для левого соседа n/d должно выполняться:
    #     a*d - b*n = 1.
    #
    # Поэтому a*d ? 1 (mod b), то есть d ? a^(-1) (mod b).
    d0 = modular_inverse(a, b)
    if d0 == 0:
        d0 = b

    n0 = (a * d0 - 1) // b

    # Все решения:
    #     d = d0 + k*b,
    #     n = n0 + k*a.
    # Берём максимально возможный знаменатель d <= limit.
    k = (limit - d0) // b
    d = d0 + k * b
    n = n0 + k * a

    # Внутренние проверки корректности.
    assert d <= limit
    assert a * d - b * n == 1
    assert gcd(n, d) == 1
    assert n * b < a * d

    return n, d


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Найти дробь, непосредственно стоящую слева от a/b "
            "в последовательности Фарея порядка N."
        )
    )
    parser.add_argument("--numerator", "-a", type=int, default=3,
                        help="числитель целевой дроби (по умолчанию: 3)")
    parser.add_argument("--denominator", "-b", type=int, default=7,
                        help="знаменатель целевой дроби (по умолчанию: 7)")
    parser.add_argument("--limit", "-N", type=int, default=1_000_000,
                        help="максимальный знаменатель (по умолчанию: 1000000)")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    n, d = left_farey_neighbor(
        args.numerator,
        args.denominator,
        args.limit,
    )

    print(f"Левый сосед: {n}/{d}")
    print(f"Искомый числитель: {n}")


if __name__ == "__main__":
    main()
