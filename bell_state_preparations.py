"""
Define functions to prepare 2-qubit circuits into Bell states

Phi Plus: |Φ+⟩ = 1/√2 (|00⟩ + |11⟩)
Phi Minus: |Φ-⟩ = 1/√2 (|00⟩ - |11⟩)
Psi Plus: |Ψ+⟩ = 1/√2 (|01⟩ + |10⟩)
Psi Minus: |Ψ-⟩ = 1/√2 (|01⟩ - |10⟩)

Uses Hadamard gate (h), controlled-NOT gate (cx), and Pauli X,Z gates (x, z)
"""

from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler


def evaluate_bell_state_results(qc: QuantumCircuit(2), SHOTS=1024):
    qc.measure_all()
    sampler = StatevectorSampler()
    result = sampler.run([qc], shots=SHOTS).result()
    counts = result[0].data.meas.get_counts()
    for key in counts.keys():
        percent = counts[key] / SHOTS * 100
        print(f"Circuit measured state '{key}' at rate {percent:.1f}%")
    print("\n")


def prepare_phi_plus(qc: QuantumCircuit(2)):
    qc.h(0)
    qc.cx(0, 1)
    return qc


def prepare_phi_minus(qc: QuantumCircuit(2)):
    qc.x(0)
    qc.h(0)
    qc.cx(0, 1)
    return qc


def prepare_psi_plus(qc: QuantumCircuit(2)):
    qc.x(1)
    qc.h(0)
    qc.cx(0, 1)
    return qc


def prepare_psi_minus(qc: QuantumCircuit(2)):
    qc.x(1)
    qc.h(0)
    qc.z(0)
    qc.z(1)
    qc.cx(0, 1)
    return qc


def prepare_all_bell_states(index):
    print(f"Preparing Bell state {index+1}...")
    qc = QuantumCircuit(2)
    if index == 0:
        prepare_phi_plus(qc)
    if index == 1:
        prepare_phi_minus(qc)
    if index == 2:
        prepare_psi_plus(qc)
    if index == 3:
        prepare_psi_minus(qc)
    return qc


def prepare_circuit_for_unique_measurement(qc: QuantumCircuit(2)):
    """
    Prepare Bell states such that each of the 4 maps to a unique measurement

    Phi Plus: |Φ+⟩ -> |00⟩
    Phi Minus: |Φ-⟩ -> |01⟩
    Psi Plus: |Ψ+⟩ -> |10⟩
    Psi Minus: |Ψ-⟩ -> |11⟩
    """

    qc.cx(0, 1)
    qc.h(0)
    qc.z(0)
    qc.z(1)
    return qc
