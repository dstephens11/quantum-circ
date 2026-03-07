"""
Define functions to prepare 2-qubit circuits for Deutcsh's algorithm solutions.

Uses Hadamard gate (h), controlled-NOT gate (cx), and Pauli X gates (x)
"""

from qiskit import QuantumCircuit, ClassicalRegister
from qiskit.primitives import StatevectorSampler


def setup_circuit():
    qc = QuantumCircuit(2)
    qc.x(1)  # Flip from |0> to |1>
    qc.h(0)
    qc.h(1)
    return qc


def finish_circuit_setup(qc: QuantumCircuit(2)):
    qc.h(0)


def prepare_oracle2(qc: QuantumCircuit(2)):
    qc.cx(0, 1)


def prepare_oracle3(qc: QuantumCircuit(2)):
    qc.cx(0, 1)
    qc.x(1)


def prepare_oracle4(qc: QuantumCircuit(2)):
    qc.x(1)


def evaluate_oracle_results(qc: QuantumCircuit(2), SHOTS=1024):
    cr = ClassicalRegister(1, "meas")  # name it 'meas'
    qc.add_register(cr)
    qc.measure(0, cr[0])

    sampler = StatevectorSampler()
    result = sampler.run([qc], shots=SHOTS).result()
    counts = result[0].data.meas.get_counts()
    for key in counts.keys():
        percent = counts[key] / SHOTS * 100
        if int(key) == 0:
            print(f"Circuit measured state '{key}'. Function is constant!")
        elif int(key) == 1:
            print(f"Circuit measured state '{key}'. Function is balanced!")

    print("\n")


def run_oracle1(SHOTS=1024):
    qc = setup_circuit()
    finish_circuit_setup(qc)
    evaluate_oracle_results(qc, SHOTS)


def run_oracle2(SHOTS=1024):
    qc = setup_circuit()
    prepare_oracle2(qc)
    finish_circuit_setup(qc)
    evaluate_oracle_results(qc, SHOTS)


def run_oracle3(SHOTS=1024):
    qc = setup_circuit()
    prepare_oracle3(qc)
    finish_circuit_setup(qc)
    evaluate_oracle_results(qc, SHOTS)


def run_oracle4(SHOTS=1024):
    qc = setup_circuit()
    prepare_oracle4(qc)
    finish_circuit_setup(qc)
    evaluate_oracle_results(qc, SHOTS)
