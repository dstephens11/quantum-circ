"""
Define functions to prepare 2-qubit Bell states.

Phi Plus: |Phi+> = 1/sqrt(2) (|00> + |11>)
Phi Minus: |Phi-> = 1/sqrt(2) (|00> - |11>)
Psi Plus: |Psi+> = 1/sqrt(2) (|01> + |10>)
Psi Minus: |Psi-> = 1/sqrt(2) (|01> - |10>)
"""

from __future__ import annotations

from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler


SHOTS_DEFAULT = 1024
BELL_STATE_NAMES = ("Phi+", "Phi-", "Psi+", "Psi-")


def evaluate_bell_state_results(
    qc: QuantumCircuit, shots: int = SHOTS_DEFAULT
) -> dict[str, int]:
    measured_circuit = qc.copy()
    measured_circuit.measure_all()

    sampler = StatevectorSampler()
    result = sampler.run([measured_circuit], shots=shots).result()
    counts = result[0].data.meas.get_counts()

    for key, value in counts.items():
        percent = value / shots * 100
        print(f"Circuit measured state '{key}' at rate {percent:.1f}%")
    print()

    return counts


def prepare_phi_plus(qc: QuantumCircuit) -> QuantumCircuit:
    qc.h(0)
    qc.cx(0, 1)
    return qc


def prepare_phi_minus(qc: QuantumCircuit) -> QuantumCircuit:
    qc.x(0)
    qc.h(0)
    qc.cx(0, 1)
    return qc


def prepare_psi_plus(qc: QuantumCircuit) -> QuantumCircuit:
    qc.x(1)
    qc.h(0)
    qc.cx(0, 1)
    return qc


def prepare_psi_minus(qc: QuantumCircuit) -> QuantumCircuit:
    qc.x(1)
    qc.h(0)
    qc.z(0)
    qc.z(1)
    qc.cx(0, 1)
    return qc


def prepare_all_bell_states(index: int) -> QuantumCircuit:
    if index == 0:
        print(f"Preparing Bell state {index + 1} ({BELL_STATE_NAMES[index]})...")
        return prepare_phi_plus(QuantumCircuit(2))
    if index == 1:
        print(f"Preparing Bell state {index + 1} ({BELL_STATE_NAMES[index]})...")
        return prepare_phi_minus(QuantumCircuit(2))
    if index == 2:
        print(f"Preparing Bell state {index + 1} ({BELL_STATE_NAMES[index]})...")
        return prepare_psi_plus(QuantumCircuit(2))
    if index == 3:
        print(f"Preparing Bell state {index + 1} ({BELL_STATE_NAMES[index]})...")
        return prepare_psi_minus(QuantumCircuit(2))

    raise ValueError(
        f"Bell state index must be between 0 and 3 inclusive, received {index}."
    )


def prepare_circuit_for_unique_measurement(qc: QuantumCircuit) -> QuantumCircuit:
    """
    Convert Bell states into unique computational-basis measurements.

    Phi Plus: |Phi+> -> |00>
    Phi Minus: |Phi-> -> |01>
    Psi Plus: |Psi+> -> |10>
    Psi Minus: |Psi-> -> |11>
    """

    transformed_circuit = qc.copy()
    transformed_circuit.cx(0, 1)
    transformed_circuit.h(0)
    transformed_circuit.z(0)
    transformed_circuit.z(1)
    return transformed_circuit
