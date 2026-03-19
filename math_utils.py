#!/usr/bin/env python3
"""
NetworkBuster Math Utilities
Mathematical operations and calculations
"""

import math
from fractions import Fraction
from decimal import Decimal, getcontext

# Set high precision for decimal calculations
getcontext().prec = 50

def fibonacci(n):
    """Generate Fibonacci sequence up to n terms."""
    fib = [0, 1]
    for i in range(2, n):
        fib.append(fib[i-1] + fib[i-2])
    return fib[:n]

def prime_sieve(limit):
    """Sieve of Eratosthenes - find all primes up to limit."""
    sieve = [True] * (limit + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(limit**0.5) + 1):
        if sieve[i]:
            for j in range(i*i, limit + 1, i):
                sieve[j] = False
    return [i for i, is_prime in enumerate(sieve) if is_prime]

def factorial(n):
    """Calculate factorial of n."""
    if n <= 1:
        return 1
    return n * factorial(n - 1)

def gcd(a, b):
    """Greatest Common Divisor using Euclidean algorithm."""
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    """Least Common Multiple."""
    return abs(a * b) // gcd(a, b)

def quadratic_solver(a, b, c):
    """Solve quadratic equation ax^2 + bx + c = 0."""
    discriminant = b**2 - 4*a*c
    if discriminant > 0:
        x1 = (-b + math.sqrt(discriminant)) / (2*a)
        x2 = (-b - math.sqrt(discriminant)) / (2*a)
        return (x1, x2)
    elif discriminant == 0:
        x = -b / (2*a)
        return (x,)
    else:
        real = -b / (2*a)
        imag = math.sqrt(abs(discriminant)) / (2*a)
        return (complex(real, imag), complex(real, -imag))

def matrix_multiply(A, B):
    """Multiply two matrices."""
    rows_A, cols_A = len(A), len(A[0])
    rows_B, cols_B = len(B), len(B[0])
    if cols_A != rows_B:
        raise ValueError("Incompatible matrix dimensions")
    result = [[0] * cols_B for _ in range(rows_A)]
    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                result[i][j] += A[i][k] * B[k][j]
    return result

def calculate_pi(precision=100):
    """Calculate Pi using Leibniz formula."""
    pi = Decimal(0)
    for k in range(precision):
        pi += Decimal((-1)**k) / Decimal(2*k + 1)
    return pi * 4

def statistics(data):
    """Calculate basic statistics."""
    n = len(data)
    mean = sum(data) / n
    variance = sum((x - mean)**2 for x in data) / n
    std_dev = math.sqrt(variance)
    sorted_data = sorted(data)
    median = sorted_data[n//2] if n % 2 else (sorted_data[n//2-1] + sorted_data[n//2]) / 2
    return {"mean": mean, "variance": variance, "std_dev": std_dev, "median": median, "min": min(data), "max": max(data)}

# ========== RUN DEMOS ==========
if __name__ == "__main__":
    print("=" * 60)
    print("NetworkBuster Math Utilities - Demo")
    print("=" * 60)
    
    print("\n1. FIBONACCI SEQUENCE (first 15 terms):")
    print(f"   {fibonacci(15)}")
    
    print("\n2. PRIME NUMBERS (up to 100):")
    primes = prime_sieve(100)
    print(f"   {primes}")
    print(f"   Count: {len(primes)} primes")
    
    print("\n3. FACTORIALS:")
    for n in [5, 10, 15, 20]:
        print(f"   {n}! = {factorial(n):,}")
    
    print("\n4. GCD & LCM:")
    print(f"   GCD(48, 18) = {gcd(48, 18)}")
    print(f"   LCM(48, 18) = {lcm(48, 18)}")
    
    print("\n5. QUADRATIC EQUATION SOLVER:")
    print("   Solving x^2 - 5x + 6 = 0:")
    roots = quadratic_solver(1, -5, 6)
    print(f"   Roots: x = {roots}")
    
    print("\n   Solving x^2 + 4 = 0 (complex roots):")
    roots = quadratic_solver(1, 0, 4)
    print(f"   Roots: x = {roots}")
    
    print("\n6. MATRIX MULTIPLICATION:")
    A = [[1, 2], [3, 4]]
    B = [[5, 6], [7, 8]]
    result = matrix_multiply(A, B)
    print(f"   A = {A}")
    print(f"   B = {B}")
    print(f"   A × B = {result}")
    
    print("\n7. PI CALCULATION (Leibniz formula, 1000 iterations):")
    pi = calculate_pi(1000)
    print(f"   π ≈ {pi}")
    print(f"   math.pi = {math.pi}")
    
    print("\n8. STATISTICS:")
    data = [23, 45, 67, 12, 89, 34, 56, 78, 90, 11, 33, 55]
    stats = statistics(data)
    print(f"   Data: {data}")
    print(f"   Mean: {stats['mean']:.2f}")
    print(f"   Median: {stats['median']:.2f}")
    print(f"   Std Dev: {stats['std_dev']:.2f}")
    print(f"   Min: {stats['min']}, Max: {stats['max']}")
    
    print("\n9. TRIGONOMETRY:")
    angles = [0, 30, 45, 60, 90]
    print("   Angle | sin      | cos      | tan")
    print("   " + "-" * 40)
    for deg in angles:
        rad = math.radians(deg)
        sin_val = math.sin(rad)
        cos_val = math.cos(rad)
        tan_val = math.tan(rad) if deg != 90 else float('inf')
        print(f"   {deg:5}° | {sin_val:8.4f} | {cos_val:8.4f} | {tan_val:8.4f}")
    
    print("\n10. EXPONENTIAL & LOGARITHMS:")
    print(f"   e = {math.e}")
    print(f"   e^2 = {math.exp(2):.6f}")
    print(f"   ln(e) = {math.log(math.e)}")
    print(f"   log10(1000) = {math.log10(1000)}")
    print(f"   log2(256) = {math.log2(256)}")
    
    print("\n" + "=" * 60)
    print("Math demo complete!")
    print("=" * 60)
