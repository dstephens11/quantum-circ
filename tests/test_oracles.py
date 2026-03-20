from __future__ import annotations

import contextlib
import io
import unittest

from qiskit.quantum_info import Statevector

import oracle_preparations as op


class OraclePreparationTests(unittest.TestCase):
    def build_oracle_circuit_silently(self, oracle_index: int):
        with contextlib.redirect_stdout(io.StringIO()):
            return op.build_deutsch_circuit(oracle_index)

    def run_oracle_silently(self, oracle_index: int, shots: int = 8):
        with contextlib.redirect_stdout(io.StringIO()):
            return op.run_oracle(oracle_index, shots=shots)

    def test_invalid_oracle_index_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            op.build_deutsch_circuit(5)

    def test_oracles_classify_as_expected(self) -> None:
        expected = {
            1: "constant",
            2: "balanced",
            3: "balanced",
            4: "constant",
        }

        for oracle_index, expected_classification in expected.items():
            with self.subTest(oracle_index=oracle_index):
                classification, _counts = self.run_oracle_silently(oracle_index, shots=8)
                self.assertEqual(classification, expected_classification)

    def test_deutsch_circuits_produce_expected_first_qubit_measurement(self) -> None:
        expected_probabilities = {
            1: {"0": 1.0},
            2: {"1": 1.0},
            3: {"1": 1.0},
            4: {"0": 1.0},
        }

        for oracle_index, expected in expected_probabilities.items():
            with self.subTest(oracle_index=oracle_index):
                qc = self.build_oracle_circuit_silently(oracle_index)
                state = Statevector.from_instruction(qc)
                probabilities = {
                    str(bit): float(probability)
                    for bit, probability in state.probabilities_dict(qargs=[0]).items()
                }

                self.assertEqual(set(probabilities), set(expected))
                for bit, expected_probability in expected.items():
                    self.assertAlmostEqual(
                        probabilities[bit], expected_probability, places=12
                    )

    def test_evaluate_oracle_results_does_not_mutate_input_circuit(self) -> None:
        qc = self.build_oracle_circuit_silently(1)
        original_clbits = len(qc.clbits)
        original_ops = list(qc.count_ops().items())

        with contextlib.redirect_stdout(io.StringIO()):
            op.evaluate_oracle_results(qc, shots=8)

        self.assertEqual(len(qc.clbits), original_clbits)
        self.assertEqual(list(qc.count_ops().items()), original_ops)


if __name__ == "__main__":
    unittest.main()
