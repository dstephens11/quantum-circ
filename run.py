"""
Run Bell-state and Deutsch's algorithm examples.
"""

from __future__ import annotations

import bell_state_preparations as bsp
import oracle_preparations as op


SHOTS = 1024


def main() -> None:
    print("Each Bell state should produce about 50% counts per outcome.\n")
    for i in range(4):
        qc = bsp.prepare_all_bell_states(i)
        bsp.evaluate_bell_state_results(qc, SHOTS)
    print()

    print("Each Bell state should map to a single outcome 100% of the time.\n")
    for i in range(4):
        qc = bsp.prepare_all_bell_states(i)
        measured_qc = bsp.prepare_circuit_for_unique_measurement(qc)
        bsp.evaluate_bell_state_results(measured_qc, SHOTS)

    for i in range(1, 5):
        print(f"Testing oracle {i}...")
        op.run_oracle(i, SHOTS)


if __name__ == "__main__":
    main()
