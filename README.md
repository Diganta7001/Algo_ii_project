# Delivery Vehicle Loading Optimization

A Python + Streamlit project for the 0/1 Knapsack problem. It compares an optimal dynamic-programming solution with a greedy value-to-weight heuristic and includes a simple benchmark page.

## Features
- Editable package list and vehicle capacity
- 0/1 Knapsack Dynamic Programming solution with package reconstruction
- Greedy value-to-weight ratio heuristic
- Selected packages, total weight/value, and unused capacity
- Benchmark table, line chart, and CSV export
- Unit tests for core behavior

## Requirements
- Python 3.10 or newer recommended

## Run locally
From the project root:

```bash
python -m venv .venv
```

Activate the environment:

Linux/macOS:
```bash
source .venv/bin/activate
```

Windows:
```bash
.venv\Scripts\activate
```

Install dependencies and launch:

```bash
pip install -r requirements.txt
streamlit run app.py
```

Streamlit will print a local URL (normally `http://localhost:8501`) to open in your browser.

## Run tests
From the project root:

```bash
python -m unittest discover -s tests -v
```

## Project structure
```text
delivery_vehicle_knapsack/
├── app.py
├── algorithms/
│   ├── __init__.py
│   ├── knapsack.py
│   ├── greedy.py
│   └── benchmark.py
├── tests/
│   └── test_algorithms.py
├── requirements.txt
└── README.md
```

## Assumptions and limitations
- Package weights and capacity are integers; weights must be positive.
- Package values are non-negative integers.
- Each package can be selected at most once.
- The DP implementation uses a full table and requires `O(nW)` time and space.
- Greedy is a heuristic and is not guaranteed to be optimal for 0/1 Knapsack.
- Benchmark times depend on the computer and should be treated as empirical observations.
