# quantum-circ

Small Qiskit examples for:

- preparing the four Bell states
- mapping each Bell state to a unique computational-basis measurement
- classifying Deutsch oracles as constant or balanced with one query

## Setup

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
python3 -m pip install -r requirements.txt
```

## Run

Execute the sample circuits:

```bash
python3 run.py
```

Run the test suite:

```bash
python3 -m unittest discover -s tests
```

## Notes

- The code uses `StatevectorSampler`, so the examples run locally without needing a remote backend.
- The tests validate quantum-state behavior directly, which keeps them deterministic and easier to trust than checking printed output alone.
