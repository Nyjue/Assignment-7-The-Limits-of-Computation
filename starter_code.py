"""
Dynamic Programming Assignment - Longest Common Subsequence
Implement three versions: naive recursive, memoization, and tabulation.
"""

import json
import time


# ============================================================================
# PART 1: NAIVE RECURSIVE SOLUTION
# ============================================================================

def lcs_recursive(seq1, seq2, i=None, j=None):
    """Naive recursive solution with optional indices."""
    # If indices not provided, use full string lengths
    if i is None:
        i = len(seq1)
    if j is None:
        j = len(seq2)
    
    # Base case: if either index is 0, return 0
    if i == 0 or j == 0:
        return 0
    
    # If characters match
    if seq1[i-1] == seq2[j-1]:
        return 1 + lcs_recursive(seq1, seq2, i-1, j-1)
    else:
        # If they don't match, try both possibilities
        return max(lcs_recursive(seq1, seq2, i-1, j),
                   lcs_recursive(seq1, seq2, i, j-1))


# ============================================================================
# PART 2: MEMOIZATION (TOP-DOWN WITH CACHING)
# ============================================================================

def lcs_memoization(seq1, seq2, i=None, j=None, memo=None):
    """Memoization solution with caching."""
    # Initialize indices if not provided
    if i is None:
        i = len(seq1)
    if j is None:
        j = len(seq2)
    
    # Initialize memo dictionary if not provided
    if memo is None:
        memo = {}
    
    # Check if already computed
    if (i, j) in memo:
        return memo[(i, j)]
    
    # Base case
    if i == 0 or j == 0:
        return 0
    
    # Compute and store
    if seq1[i-1] == seq2[j-1]:
        memo[(i, j)] = 1 + lcs_memoization(seq1, seq2, i-1, j-1, memo)
    else:
        memo[(i, j)] = max(lcs_memoization(seq1, seq2, i-1, j, memo),
                          lcs_memoization(seq1, seq2, i, j-1, memo))
    
    return memo[(i, j)]


# ============================================================================
# PART 3: TABULATION (BOTTOM-UP WITH TABLE)
# ============================================================================

def lcs_tabulation(seq1, seq2):
    """Tabulation solution using bottom-up DP table."""
    m, n = len(seq1), len(seq2)
    # Create DP table
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # Fill the table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if seq1[i-1] == seq2[j-1]:
                dp[i][j] = 1 + dp[i-1][j-1]
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    
    return dp[m][n]


# ============================================================================
# TESTING & TIMING FUNCTIONS
# ============================================================================

def load_sequence(filename):
    """Load DNA sequence from JSON file."""
    with open(f"sequences/{filename}", "r") as f:
        return json.load(f)


def test_small_cases():
    """Test all implementations on small known cases."""
    print("="*70)
    print("TESTING ON SMALL CASES")
    print("="*70 + "\n")
    
    test_cases = [
        ("AGGTAB", "GXTXAYB", 4),  # LCS: GTAB
        ("ABCDGH", "AEDFHR", 3),   # LCS: ADH
        ("ABC", "AC", 2),           # LCS: AC
        ("", "ABC", 0),             # LCS: empty
    ]
    
    for seq1, seq2, expected in test_cases:
        print(f"Test: '{seq1}' vs '{seq2}'")
        print(f"  Expected LCS length: {expected}")
        
        # Test recursive
        try:
            result = lcs_recursive(seq1, seq2)
            status = "✓ PASS" if result == expected else "✗ FAIL"
            print(f"  Recursive: {result} {status}")
        except Exception as e:
            print(f"  Recursive: ERROR - {str(e)}")
        
        # Test memoization
        try:
            result = lcs_memoization(seq1, seq2)
            status = "✓ PASS" if result == expected else "✗ FAIL"
            print(f"  Memoization: {result} {status}")
        except Exception as e:
            print(f"  Memoization: ERROR - {str(e)}")
        
        # Test tabulation
        try:
            result = lcs_tabulation(seq1, seq2)
            status = "✓ PASS" if result == expected else "✗ FAIL"
            print(f"  Tabulation: {result} {status}")
        except Exception as e:
            print(f"  Tabulation: ERROR - {str(e)}")
        
        print()


def time_recursive():
    """Time the recursive solution on progressively larger inputs."""
    print("\n" + "="*70)
    print("TIMING RECURSIVE SOLUTION")
    print("="*70 + "\n")
    print("WARNING: Recursive solution will become very slow!\n")
    
    sizes = [10, 12, 15, 20, 25, 30]  # Progressive sizes to see slowdown
    
    for size in sizes:
        try:
            data = load_sequence(f"dna_{size}.json")
            seq1 = data["sequence1"]
            seq2 = data["sequence2"]
            
            print(f"Sequence length: {size}")
            
            start = time.perf_counter()
            result = lcs_recursive(seq1, seq2)
            elapsed = time.perf_counter() - start
            
            print(f"  LCS length: {result}")
            print(f"  Time: {elapsed:.4f} seconds")
            
            if elapsed > 1.0:
                print(f"  ⚠️  Getting slow at {size}bp!")
            if elapsed > 5.0:
                print(f"  🛑 Stopping - recursive too slow for larger inputs!")
                break
            print()
            
        except FileNotFoundError:
            print(f"  File dna_{size}.json not found. Run sequence_generator.py first.")
            break
        except Exception as e:
            print(f"  Error: {e}")
            break


def compare_all_approaches():
    """Compare all three approaches on sequences of increasing size."""
    print("\n" + "="*70)
    print("COMPARING ALL APPROACHES")
    print("="*70 + "\n")
    
    sizes = [10, 20, 50, 100, 200, 500, 1000]
    
    print(f"{'Size':<8} {'Recursive':<15} {'Memoization':<15} {'Tabulation':<15} {'Recursive Speedup':<20}")
    print("-" * 80)
    
    for size in sizes:
        try:
            data = load_sequence(f"dna_{size}.json")
            seq1 = data["sequence1"]
            seq2 = data["sequence2"]
            
            # Time recursive (only for smaller sizes)
            if size <= 20:
                start = time.perf_counter()
                lcs_recursive(seq1, seq2)
                rec_time = time.perf_counter() - start
                rec_str = f"{rec_time:.6f}s"
            else:
                rec_time = float('inf')
                rec_str = "N/A (too slow)"
            
            # Time memoization
            start = time.perf_counter()
            lcs_memoization(seq1, seq2)
            mem_time = time.perf_counter() - start
            mem_str = f"{mem_time:.6f}s"
            
            # Time tabulation
            start = time.perf_counter()
            lcs_tabulation(seq1, seq2)
            tab_time = time.perf_counter() - start
            tab_str = f"{tab_time:.6f}s"
            
            # Calculate speedup (if recursive completed)
            if rec_time != float('inf') and rec_time > 0:
                speedup = f"{rec_time/mem_time:.1f}x faster"
            else:
                speedup = "N/A"
            
            print(f"{size:<8} {rec_str:<15} {mem_str:<15} {tab_str:<15} {speedup:<20}")
            
        except FileNotFoundError:
            print(f"{size:<8} {'File not found':<15} {'File not found':<15} {'File not found':<15}")
            print("\n⚠️  Run 'python sequence_generator.py' first to generate the DNA files!")
            break
        except Exception as e:
            print(f"{size:<8} {'Error':<15} {'Error':<15} {'Error':<15}")
            print(f"Error details: {e}")
            break


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    print("="*70)
    print("DYNAMIC PROGRAMMING ASSIGNMENT - LONGEST COMMON SUBSEQUENCE")
    print("="*70)
    print("\nChoose which test to run:")
    print("  1. Test small cases (verifies correctness)")
    print("  2. Time recursive solution (shows exponential growth)")
    print("  3. Compare all approaches (shows performance difference)")
    print("  4. Run all tests sequentially")
    print("-" * 70)
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    if choice == "1":
        test_small_cases()
    elif choice == "2":
        time_recursive()
    elif choice == "3":
        compare_all_approaches()
    elif choice == "4":
        test_small_cases()
        input("\nPress Enter to continue to recursive timing...")
        time_recursive()
        input("\nPress Enter to continue to comparison...")
        compare_all_approaches()
    else:
        print("Invalid choice. Running all tests...")
        test_small_cases()
        time_recursive()
        compare_all_approaches()
    
    print("\n" + "="*70)
    print("ASSIGNMENT COMPLETE!")
    print("="*70)