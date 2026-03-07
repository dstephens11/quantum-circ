"""
Prepare Bell states and measure their counts. Show that the
circuit can be prepared such that each Bell state maps to a unique output measurement.

Prepare oracles from Deutsch's algorithm solutions. Show that
circuit can differentiate between constant and balanced functions with a single query.
"""

import bell_state_preparations as bsp
import oracle_preparations as op

SHOTS = 1024


def main():
    print(f"Each Bell state should produce ~50% counts per outcome!\n")
    for i in range(4):
        qc = bsp.prepare_all_bell_states(i)
        bsp.evaluate_bell_state_results(qc, SHOTS)
    print("\n")

    print(f"Each Bell state should results in a single outcome 100% of the time!\n")
    for i in range(4):
        qc = bsp.prepare_all_bell_states(i)
        qc = bsp.prepare_circuit_for_unique_measurement(qc)
        bsp.evaluate_bell_state_results(qc, SHOTS)

    print(f"Testing oracle 1...")
    op.run_oracle1(SHOTS)

    print(f"Testing oracle 2...")
    op.run_oracle2(SHOTS)

    print(f"Testing oracle 3...")
    op.run_oracle3(SHOTS)

    print(f"Testing oracle 4...")
    op.run_oracle4(SHOTS)


if __name__ == "__main__":
    main()
