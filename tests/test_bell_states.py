from __future__ import annotations

import contextlib
import io
import unittest

from qiskit.quantum_info import Statevector

import bell_state_preparations as bsp


class BellStatePreparationTests(unittest.TestCase):
    def prepare_bell_state_silently(self, index: int):
        with contextlib.redirect_stdout(io.StringIO()):
            return bsp.prepare_all_bell_states(index)

    def test_invalid_bell_state_index_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            bsp.prepare_all_bell_states(4)

    def test_each_bell_state_matches_expected_statevector(self) -> None:
        expected_states = {
            0: [1 / (2**0.5), 0, 0, 1 / (2**0.5)],
            1: [1 / (2**0.5), 0, 0, -1 / (2**0.5)],
            2: [0, 1 / (2**0.5), 1 / (2**0.5), 0],
            3: [0, 1 / (2**0.5), -1 / (2**0.5), 0],
        }

        for index, expected in expected_states.items():
            with self.subTest(index=index):
                qc = self.prepare_bell_state_silently(index)
                actual = Statevector.from_instruction(qc)
                self.assertTrue(actual.equiv(Statevector(expected)))

    def test_unique_measurement_transform_maps_bell_states_to_basis_states(self) -> None:
        expected_states = {
            0: [1, 0, 0, 0],
            1: [0, 1, 0, 0],
            2: [0, 0, 1, 0],
            3: [0, 0, 0, 1],
        }

        for index, expected in expected_states.items():
            with self.subTest(index=index):
                bell_state = self.prepare_bell_state_silently(index)
                transformed = bsp.prepare_circuit_for_unique_measurement(bell_state)
                actual = Statevector.from_instruction(transformed)
                self.assertTrue(actual.equiv(Statevector(expected)))

    def test_evaluate_bell_state_results_does_not_mutate_input_circuit(self) -> None:
        qc = self.prepare_bell_state_silently(0)
        original_clbits = len(qc.clbits)
        original_ops = list(qc.count_ops().items())

        with contextlib.redirect_stdout(io.StringIO()):
            bsp.evaluate_bell_state_results(qc, shots=8)

        self.assertEqual(len(qc.clbits), original_clbits)
        self.assertEqual(list(qc.count_ops().items()), original_ops)


if __name__ == "__main__":
    unittest.main()
