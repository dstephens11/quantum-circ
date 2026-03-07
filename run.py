"""
Prepare Bell states and measure their counts. Show that the
circuit can be prepared such that each Bell state maps to a unique output measurement.
"""

from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler

import bell_state_preparations as bsp

SHOTS = 1024


def evaluate_results(qc: QuantumCircuit(2)):
    qc.measure_all()
    sampler = StatevectorSampler()
    result = sampler.run([qc], shots=SHOTS).result()
    counts = result[0].data.meas.get_counts()
    for key in counts.keys():
        percent = counts[key] / SHOTS * 100
        print(f"Circuit measured state '{key}' at rate {percent:.1f}%")
    print("\n")


def main():
    print(f"Each Bell state should produce ~50% counts per outcome!\n")
    for i in range(4):
        qc = bsp.prepare_all_bell_states(i)
        evaluate_results(qc)
    print("\n")

    print(f"Each Bell state should results in a single outcome 100% of the time!\n")
    for i in range(4):
        qc = bsp.prepare_all_bell_states(i)
        qc = bsp.prepare_circuit_for_unique_measurement(qc)
        evaluate_results(qc)


if __name__ == "__main__":
    main()
