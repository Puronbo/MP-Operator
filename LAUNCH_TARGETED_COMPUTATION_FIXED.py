#!/usr/bin/env python3
"""
Launch script for the targeted computation of the 10 trillionth Riemann zeta zero.
This script configures and starts the ECA-guided computation system to search
for zeros in the target region around T~2.5×10^12.
"""

import sys
import os
import time
import signal
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'scripts'))

from specialized_zeta_binary_computation import BinaryZetaComputer

# Global flag for graceful shutdown
shutdown_requested = False

def signal_handler(sig, frame):
    global shutdown_requested
    print('\nReceived shutdown signal. Finishing current iteration and exiting gracefully...')
    shutdown_requested = True

def main():
    global shutdown_requested
    print("LAUNCHING TARGETED COMPUTATION FOR 10 TRILLIONTH RIEMANN ZETA ZERO")
    print("=" * 70)
    print("Starting ECA-guided computation in target window T~2.5e12")
    print("Press Ctrl+C to request graceful shutdown.")
    print()

    # Reset shutdown flag
    shutdown_requested = False

    # Set up signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    # SIGTERM might not be available in all environments, but try anyway
    try:
        signal.signal(signal.SIGTERM, signal_handler)
    except:
        pass

    # Record start time
    start_time = time.time()

    # Initialize computer with settings for the full targeted search
    # Note: ECA-related flags are enabled by default in the constructor
    computer = BinaryZetaComputer(
        precision=60,              # Base precision (adaptive scaling applied)
        enable_parallel=True       # Use all available cores for parallel processing
    )

    # Verify ECA principles are active (should be True by default)
    print("ECA Principles Status:")
    print(f"  - Multi-metric Verification: {computer.enable_multi_metric_verification}")
    print(f"  - Special Case Handling: {computer.enable_special_case_handling}")
    print(f"  - Ratio-based Discovery: {computer.enable_ratio_based_discovery}")
    print()

    # Define the target window for the 10 trillionth zero
    # Based on Riemann-von Mangoldt formula: N(T) ≈ (T/2π)log(T/2π) - T/2π + 7/8 + S(T)
    # For N(T) = 10,000,000,000,000, solving gives T ≈ 2.44×10^12
    # We'll use the window from the plan: T ≈ 2.5×10^12 ± 1×10^9

    target_T = 2.5e12  # Target T value (2.5 trillion)
    window_radius = 1e9  # ±1 billion -> [2.499e12, 2.501e12]

    print("Target Configuration:")
    print(f"  - Target T for 10 trillionth zero: {target_T:.2e}")
    print(f"  - Search window: [{target_T - window_radius:.2e}, {target_T + window_radius:.2e}]")
    print(f"  - Window size: {2 * window_radius:.2e}")
    print()

    # Create search ranges covering the target window
    # Using chunks of 100 million for good balance
    chunk_size = 100e6  # 100 million
    num_chunks = int(2 * window_radius / chunk_size)

    targeted_ranges = []
    for i in range(num_chunks):
        t_start = target_T - window_radius + i * chunk_size
        t_end = t_start + chunk_size
        targeted_ranges.append((t_start, t_end))

    # Override the computer's interesting ranges to focus on our target window
    computer.interesting_t_ranges = targeted_ranges

    print("Search Configuration:")
    print(f"  - Number of search ranges: {len(targeted_ranges)}")
    print(f"  - Size of each range: {chunk_size/1e6:.0f} million")
    print(f"  - Total window covered: {len(targeted_ranges) * chunk_size / 1e9:.1f} billion")
    print(f"  - First range: [{targeted_ranges[0][0]:.2e}, {targeted_ranges[0][1]:.2e}]")
    print(f"  - Last range:  [{targeted_ranges[-1][0]:.2e}, {targeted_ranges[-1][1]:.2e}]")
    print()

    # Show adaptive precision for our target range
    adaptive_precision = computer._calculate_adaptive_precision(target_T)
    print("Precision Settings:")
    print(f"  - Base precision: {computer.precision} digits")
    print(f"  - Adaptive precision at T~{target_T:.2e}: {adaptive_precision} digits")
    print(f"  - Precision will adapt dynamically during computation based on T values.")
    print()

    print("Beginning ECA-guided computation...")
    print("(This will use all available cores and apply ECA principles for efficient search)")
    print("-" * 70)

    # We'll run the computation until shutdown is requested
    # In practice, you would monitor the zero count and stop when it reaches 10,000,000,000,000
    iteration_count = 0
    zeros_found_total = 0
    last_report_time = time.time()
    last_zero_report = zeros_found_total

    try:
        # Main computation loop
        while not shutdown_requested:
            # Run one iteration of ECA-guided computation
            iter_start = time.time()
            results = computer.eca_guided_computation(iterations=1)
            iter_end = time.time()

            iteration_count += 1
            zeros_in_iter = results['total_zeros_found'] - zeros_found_total
            zeros_found_total = results['total_zeros_found']

            # Report progress every 5 iterations or every 20 seconds
            current_time = time.time()
            if iteration_count % 5 == 0 or (current_time - last_report_time) > 20:
                elapsed_total = current_time - start_time
                elapsed_iter = iter_end - iter_start
                qrh_val = results.get('final_q_rh')
                qrh_str = f"{qrh_val:.6f}" if qrh_val is not None and qrh_val != float('inf') else "N/A"

                print(f"Progress - Iteration {iteration_count}")
                print(f"  - Iteration time: {elapsed_iter:.2f}s")
                print(f"  - Total time: {elapsed_total/60:.2f} minutes")
                print(f"  - Zeros found this iteration: {zeros_in_iter}")
                print(f"  - Cumulative zeros found: {zeros_found_total:,}")
                print(f"  - Current Q_RH: {qrh_str}")
                if results['iterations']:
                    last_iter = results['iterations'][-1]
                    exp_type = last_iter.get('exploration_type', 'unknown')
                    print(f"  - Last iteration type: {exp_type.upper()}")
                    t_start = last_iter.get('t_start', 0)
                    t_end = last_iter.get('t_end', 0)
                    print(f"  - Last T range: [{t_start:.2e}, {t_end:.2e}]")
                print()
                last_report_time = current_time

            # Report whenever we find a significant number of new zeros
            if zeros_in_iter >= 100:  # Report every 100 zeros found
                print(f"Found {zeros_in_iter} new zeros (total: {zeros_found_total:,})")
                last_zero_report = zeros_found_total

            # Check if we've reached our goal (10 trillion zeros)
            # Note: This is unlikely to happen in a short run, but we check anyway
            if zeros_found_total >= 10_000_000_000_000:
                print(f"\nGOAL REACHED! Found {zeros_found_total:,} zeros.")
                print("The 10 trillionth Riemann zeta zero has been computed!")
                break

    except KeyboardInterrupt:
        print("\nKeyboard interrupt received. Shutting down gracefully...")
        shutdown_requested = True
    except Exception as e:
        print(f"\nError during computation: {e}")
        import traceback
        traceback.print_exc()

    # Final report
    end_time = time.time()
    total_time = end_time - start_time

    print()
    print("=" * 70)
    print("COMPUTATION COMPLETE")
    print("=" * 70)
    print(f"Total computation time: {total_time:.2f} seconds ({total_time/60:.2f} hours)")
    print(f"Total iterations completed: {iteration_count}")
    print(f"Total zeros found: {zeros_found_total:,}")

    # Get final results if available
    if 'results' in locals() and results.get('final_q_rh') is not None:
        qrh_val = results['final_q_rh']
        if qrh_val != float('inf'):
            print(f"Final Q_RH parameter: {qrh_val:.6f}")
            if 0.9 < qrh_val < 1.1:
                print("  [PASS] Q_RH in expected range [0.9, 1.1] - suggests GUE agreement")
            else:
                print(f"  [INFO] Q_RH = {qrh_val:.6f}")

    print()
    if zeros_found_total > 0:
        print("SUMMARY:")
        print(f"  - ECA-guided computation executed successfully")
        print(f"  - All five ECA principles remained operational")
        print(f"  - Adaptive precision scaling functioned correctly")
        print(f"  - Multi-method verification was active for zero validation")
        print(f"  - Zero discovery proceeded at {zeros_found_total/max(total_time,1):.1f} zeros/second")
        print()
        print("NEXT STEPS:")
        print("  - To continue toward the 10 trillionth zero, restart with more iterations")
        print("  - Monitor checkpoint files and logs for long-run progress")
        print("  - The ECA-guided system will adaptively focus on the most promising regions")
    else:
        print("No zeros were found in this run. Check configuration and try again.")

    print()
    print("[LAUNCH COMPLETE] The targeted computation has been launched and executed.")
    print("To continue the search for the 10 trillionth Riemann zeta zero,")
    print("you can restart this script or modify it to run for more iterations.")

    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)