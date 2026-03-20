"""
Define functions to prepare 2-qubit circuits for Deutsch's algorithm.

Oracle 1 and 4 are constant. Oracle 2 and 3 are balanced.
"""

from __future__ import annotations

from qiskit import ClassicalRegister, QuantumCircuit
from qiskit.primitives import StatevectorSampler


SHOTS_DEFAULT = 1024


def setup_circuit() -> QuantumCircuit:
    qc = QuantumCircuit(2)
    qc.x(1)  # Flip from |0> to |1>.
    qc.h(0)
    qc.h(1)
    return qc


def finish_circuit_setup(qc: QuantumCircuit) -> QuantumCircuit:
    qc.h(0)
    return qc


def prepare_oracle2(qc: QuantumCircuit) -> QuantumCircuit:
    qc.cx(0, 1)
    return qc


def prepare_oracle3(qc: QuantumCircuit) -> QuantumCircuit:
    qc.cx(0, 1)
    qc.x(1)
    return qc


def prepare_oracle4(qc: QuantumCircuit) -> QuantumCircuit:
    qc.x(1)
    return qc


def prepare_oracle(qc: QuantumCircuit, oracle_index: int) -> QuantumCircuit:
    if oracle_index == 1:
        return qc
    if oracle_index == 2:
        return prepare_oracle2(qc)
    if oracle_index == 3:
        return prepare_oracle3(qc)
    if oracle_index == 4:
        return prepare_oracle4(qc)

    raise ValueError(
        f"Oracle index must be between 1 and 4 inclusive, received {oracle_index}."
    )


def build_deutsch_circuit(oracle_index: int) -> QuantumCircuit:
    qc = setup_circuit()
    prepare_oracle(qc, oracle_index)
    finish_circuit_setup(qc)
    return qc


def evaluate_oracle_results(
    qc: QuantumCircuit, shots: int = SHOTS_DEFAULT
) -> tuple[str, dict[str, int]]:
    measured_circuit = qc.copy()
    cr = ClassicalRegister(1, "meas")
    measured_circuit.add_register(cr)
    measured_circuit.measure(0, cr[0])

    sampler = StatevectorSampler()
    result = sampler.run([measured_circuit], shots=shots).result()
    counts = result[0].data.meas.get_counts()

    measured_bit = max(counts, key=counts.get)
    classification = "constant" if int(measured_bit) == 0 else "balanced"

    for key, value in counts.items():
        percent = value / shots * 100
        print(
            f"Circuit measured state '{key}' at rate {percent:.1f}%. "
            f"Function is {classification}!"
        )
    print()

    return classification, counts


def run_oracle(oracle_index: int, shots: int = SHOTS_DEFAULT) -> tuple[str, dict[str, int]]:
    qc = build_deutsch_circuit(oracle_index)
    return evaluate_oracle_results(qc, shots)


def run_oracle1(shots: int = SHOTS_DEFAULT) -> tuple[str, dict[str, int]]:
    return run_oracle(1, shots)


def run_oracle2(shots: int = SHOTS_DEFAULT) -> tuple[str, dict[str, int]]:
    return run_oracle(2, shots)


def run_oracle3(shots: int = SHOTS_DEFAULT) -> tuple[str, dict[str, int]]:
    return run_oracle(3, shots)


def run_oracle4(shots: int = SHOTS_DEFAULT) -> tuple[str, dict[str, int]]:
    return run_oracle(4, shots)
