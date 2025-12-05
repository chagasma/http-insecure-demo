from math import gcd, isqrt, log
from random import randint
from typing import List, Optional, Tuple


def generate_factor_base(n: int, size: int = None) -> List[int]:
    if size is None:
        # Heuristic: smaller base for smaller numbers
        size = min(100, max(10, int(log(n) ** 0.5)))

    primes = []
    candidate = 2

    while len(primes) < size:
        is_prime = True
        for p in primes:
            if p * p > candidate:
                break
            if candidate % p == 0:
                is_prime = False
                break

        if is_prime:
            primes.append(candidate)

        candidate += 1 if candidate == 2 else 2

    return primes


def is_smooth(num: int, factor_base: List[int]) -> Tuple[bool, List[int]]:
    if num == 0:
        return False, []

    num = abs(num)
    exponents = [0] * len(factor_base)

    for i, prime in enumerate(factor_base):
        while num % prime == 0:
            num //= prime
            exponents[i] += 1

    # If anything remains, not smooth
    if num != 1:
        return False, []

    return True, exponents


def find_smooth_relations(
    n: int, factor_base: List[int], num_relations: int = None
) -> List[Tuple[int, List[int]]]:
    if num_relations is None:
        # Need at least len(base) + 1 relations
        num_relations = len(factor_base) + 5

    relations = []
    sqrt_n = isqrt(n)
    attempts = 0
    max_attempts = num_relations * 1000

    print(f"\nSearching for {num_relations} smooth relations...")
    print(f"Factor base: {len(factor_base)} primes up to {factor_base[-1]}")

    # Try values near sqrt(n)
    x = sqrt_n + 1

    while len(relations) < num_relations and attempts < max_attempts:
        attempts += 1

        # Compute x^2 mod n
        x_squared_mod_n = (x * x) % n

        # Check if smooth
        smooth, exponents = is_smooth(x_squared_mod_n, factor_base)

        if smooth:
            relations.append((x, exponents))
            print(
                f"  Found relation {len(relations)}: x={x}, x^2={x_squared_mod_n} (mod {n})"
            )

        x += 1

        # Also try some random values
        if attempts % 100 == 0:
            x = randint(sqrt_n, sqrt_n + 10000)

    if len(relations) < num_relations:
        print(
            f"\nWarning: Only found {len(relations)} relations in {attempts} attempts"
        )

    return relations


def gauss_mod2(matrix: List[List[int]]) -> Optional[List[int]]:
    if not matrix:
        return None

    rows = len(matrix)
    cols = len(matrix[0])

    # Create copy in mod 2
    M = [[val % 2 for val in row] for row in matrix]

    # Augment with identity to track operations
    for i in range(rows):
        M[i].extend([1 if i == j else 0 for j in range(rows)])

    # Gaussian elimination
    pivot_row = 0

    for col in range(cols):
        # Find pivot
        pivot_found = False
        for i in range(pivot_row, rows):
            if M[i][col] == 1:
                # Swap rows
                M[pivot_row], M[i] = M[i], M[pivot_row]
                pivot_found = True
                break

        if not pivot_found:
            continue

        # Eliminate below pivot
        for i in range(rows):
            if i != pivot_row and M[i][col] == 1:
                for j in range(len(M[i])):
                    M[i][j] ^= M[pivot_row][j]  # XOR

        pivot_row += 1

    # Look for zero row (linear dependency)
    for i in range(rows):
        if all(M[i][j] == 0 for j in range(cols)):
            # Found dependency
            return M[i][cols:]

    return None


def dixon_factorization(n: int, verbose: bool = True) -> Optional[Tuple[int, int]]:
    if verbose:
        print(f"\n{'=' * 70}")
        print(f"DIXON'S METHOD - Factoring {n}")
        print(f"{'=' * 70}")

    # Check trivial cases
    if n % 2 == 0:
        return 2, n // 2

    # Generate factor base
    factor_base = generate_factor_base(n)

    if verbose:
        print(f"\nFactor base ({len(factor_base)} primes):")
        print(f"  {factor_base[:20]}{'...' if len(factor_base) > 20 else ''}")

    # Find smooth relations
    relations = find_smooth_relations(n, factor_base)

    if len(relations) < len(factor_base) + 1:
        if verbose:
            print("\nInsufficient relations found")
        return None

    # Build exponent matrix (mod 2)
    if verbose:
        print("\nBuilding exponent matrix...")

    matrix = [exponents for _, exponents in relations]

    # Solve for linear dependency
    if verbose:
        print(f"  Matrix: {len(matrix)}x{len(matrix[0])}")
        print("  Finding linear dependency mod 2...")

    solution = gauss_mod2(matrix)

    if solution is None:
        if verbose:
            print("\nNo linear dependency found")
        return None

    # Build x and y from solution
    if verbose:
        print("\nDependency found!")
        print(f"  Solution vector: {solution}")

    x = 1
    y_exponents = [0] * len(factor_base)

    for i, use in enumerate(solution):
        if use == 1:
            x = (x * relations[i][0]) % n
            for j in range(len(factor_base)):
                y_exponents[j] += relations[i][1][j]

    # Compute y
    y = 1
    for i, exp in enumerate(y_exponents):
        y = (y * pow(factor_base[i], exp // 2, n)) % n

    if verbose:
        print("\nFound congruence:")
        print(f"  x = {x}")
        print(f"  y = {y}")
        print(f"  x^2 mod n = {(x * x) % n}")
        print(f"  y^2 mod n = {(y * y) % n}")

    # Check x != +-y (mod n)
    if x % n == y % n or x % n == (n - y) % n:
        if verbose:
            print("\nFailed: x = +-y (mod n)")
        return None

    # Compute factors
    factor1 = gcd(x - y, n)
    factor2 = gcd(x + y, n)

    if verbose:
        print("\nComputing GCD:")
        print(f"  gcd(x - y, n) = gcd({x - y}, {n}) = {factor1}")
        print(f"  gcd(x + y, n) = gcd({x + y}, {n}) = {factor2}")

    # Return non-trivial factor
    if 1 < factor1 < n:
        if verbose:
            print("\nFACTOR FOUND!")
        return factor1, n // factor1

    if 1 < factor2 < n:
        if verbose:
            print("\nFACTOR FOUND!")
        return factor2, n // factor2

    if verbose:
        print("\nFailed to find non-trivial factor")

    return None


def main():
    print("Dixon")

    # Test with small numbers
    tests = [
        91,  # 7 x 13
        143,  # 11 x 13
        1147,  # 31 x 37
        2279,  # 43 x 53
        15347,  # 103 x 149
    ]

    for n in tests:
        result = dixon_factorization(n, verbose=True)

        if result:
            p, q = result
            print(f"Result: {n} = {p} x {q}")
            print(f"Verification: {p} x {q} = {p * q}")
        else:
            print(f"Failed to factor {n}")


if __name__ == "__main__":
    main()
