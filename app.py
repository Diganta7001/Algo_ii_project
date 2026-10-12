import time
import pandas as pd
import streamlit as st

from algorithms.knapsack import solve_knapsack_dp
from algorithms.greedy import solve_knapsack_greedy
from algorithms.benchmark import run_benchmarks

st.set_page_config(
    page_title="Delivery Load Optimizer",
    page_icon="🚚",
    layout="wide",
)

st.title("🚚 Delivery Vehicle Load Optimizer")
st.caption("0/1 Knapsack · Dynamic Programming vs Greedy")

with st.sidebar:
    st.header("Vehicle")
    capacity = st.number_input(
        "Maximum capacity (kg)", min_value=0, max_value=100_000,
        value=20, step=1
    )
    st.markdown("---")
    st.subheader("Quick actions")
    use_example = st.button("Load assignment example", use_container_width=True)
    use_counterexample = st.button("Load Greedy counterexample", use_container_width=True)

example_packages = [
    {"id": "P1", "weight": 5, "value": 50},
    {"id": "P2", "weight": 2, "value": 30},
    {"id": "P3", "weight": 7, "value": 45},
    {"id": "P4", "weight": 1, "value": 15},
    {"id": "P5", "weight": 8, "value": 40},
]
counterexample_packages = [
    {"id": "A", "weight": 10, "value": 60},
    {"id": "B", "weight": 20, "value": 100},
    {"id": "C", "weight": 30, "value": 120},
]

if "packages_df" not in st.session_state:
    st.session_state.packages_df = pd.DataFrame(example_packages)
if use_example:
    st.session_state.packages_df = pd.DataFrame(example_packages)
    st.session_state["capacity_widget"] = 20
    capacity = 20
if use_counterexample:
    st.session_state.packages_df = pd.DataFrame(counterexample_packages)
    st.session_state["capacity_widget"] = 50
    capacity = 50

st.subheader("1. Enter available packages")
st.write("Edit the table directly. Weights and values must be non-negative integers; package IDs must be unique.")
edited_df = st.data_editor(
    st.session_state.packages_df,
    num_rows="dynamic",
    use_container_width=True,
    hide_index=True,
    column_config={
        "id": st.column_config.TextColumn("Package ID", required=True),
        "weight": st.column_config.NumberColumn("Weight (kg)", min_value=1, step=1, required=True),
        "value": st.column_config.NumberColumn("Delivery value", min_value=0, step=1, required=True),
    },
    key="package_editor",
)
st.session_state.packages_df = edited_df

def validate_packages(df, cap):
    required = {"id", "weight", "value"}
    if not required.issubset(df.columns):
        return None, "The table must contain id, weight, and value columns."
    clean = df[list(required)].copy()
    clean = df[["id", "weight", "value"]].copy()
    if clean.empty:
        return [], None
    if clean.isnull().any().any():
        return None, "Fill in every package field or remove the incomplete row."
    clean["id"] = clean["id"].astype(str).str.strip()
    if (clean["id"] == "").any():
        return None, "Package IDs cannot be empty."
    if clean["id"].duplicated().any():
        return None, "Package IDs must be unique."
    for col in ("weight", "value"):
        numeric = pd.to_numeric(clean[col], errors="coerce")
        if numeric.isnull().any() or (numeric % 1 != 0).any():
            return None, f"{col.title()} values must be integers."
        clean[col] = numeric.astype(int)
    if (clean["weight"] <= 0).any():
        return None, "Package weights must be greater than zero."
    if (clean["value"] < 0).any():
        return None, "Delivery values cannot be negative."
    return clean.to_dict("records"), None

packages, error = validate_packages(edited_df, capacity)
if error:
    st.error(error)
else:
    st.subheader("2. Optimize loading")
    run = st.button("Run optimization", type="primary", use_container_width=True)
    if run:
        if capacity == 0:
            st.warning("Vehicle capacity is 0 kg, so no positive-weight package can be loaded.")
        dp_start = time.perf_counter()
        dp_result = solve_knapsack_dp(packages, int(capacity))
        dp_seconds = time.perf_counter() - dp_start
        greedy_start = time.perf_counter()
        greedy_result = solve_knapsack_greedy(packages, int(capacity))
        greedy_seconds = time.perf_counter() - greedy_start

        st.session_state["results"] = {
            "dp": dp_result,
            "greedy": greedy_result,
            "dp_seconds": dp_seconds,
            "greedy_seconds": greedy_seconds,
            "capacity": int(capacity),
        }

if "results" in st.session_state:
    results = st.session_state["results"]
    dp = results["dp"]
    greedy = results["greedy"]
    cap = results["capacity"]
    st.subheader("3. Results")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Optimal DP value", dp["total_value"])
    c2.metric("Weight used", f'{dp["total_weight"]} / {cap} kg')
    c3.metric("Unused capacity", f'{cap - dp["total_weight"]} kg')
    c4.metric("Greedy value", greedy["total_value"],
              delta=greedy["total_value"] - dp["total_value"])

    left, right = st.columns(2)
    with left:
        st.markdown("#### Dynamic Programming (optimal)")
        st.write("Selected packages")
        st.dataframe(pd.DataFrame(dp["selected_packages"], columns=["id", "weight", "value"])
                     if dp["selected_packages"] else pd.DataFrame(columns=["id", "weight", "value"]),
                     use_container_width=True, hide_index=True)
        st.caption(f'Execution time: {results["dp_seconds"] * 1000:.4f} ms')
    with right:
        st.markdown("#### Greedy heuristic")
        st.write("Selected packages")
        st.dataframe(pd.DataFrame(greedy["selected_packages"], columns=["id", "weight", "value"])
                     if greedy["selected_packages"] else pd.DataFrame(columns=["id", "weight", "value"]),
                     use_container_width=True, hide_index=True)
        st.caption(f'Execution time: {results["greedy_seconds"] * 1000:.4f} ms')

    if dp["total_value"] > 0:
        gap = (dp["total_value"] - greedy["total_value"]) / dp["total_value"] * 100
    else:
        gap = 0.0
    st.info(f"Greedy optimality gap: {gap:.2f}% of the DP value. DP is optimal for this 0/1 Knapsack instance; Greedy is not guaranteed to be.")
    st.markdown("#### Capacity usage")
    chart_df = pd.DataFrame({
        "Algorithm": ["Dynamic Programming", "Greedy"],
        "Weight used (kg)": [dp["total_weight"], greedy["total_weight"]],
        "Delivery value": [dp["total_value"], greedy["total_value"]],
    }).set_index("Algorithm")
    st.bar_chart(chart_df)

st.markdown("---")
st.subheader("4. Performance analysis")
st.write("Run a small benchmark over generated package sets. Results vary by machine; use these measurements as empirical evidence, not as a proof of complexity.")
max_n = st.slider("Largest package count to test", min_value=10, max_value=200, value=80, step=10)
bench_capacity = st.slider("Benchmark capacity (kg)", min_value=20, max_value=500, value=100, step=20)
if st.button("Run benchmark", use_container_width=True):
    with st.spinner("Running benchmarks..."):
        bench_df = run_benchmarks(max_n=max_n, capacity=bench_capacity)
    st.session_state["benchmark_df"] = bench_df
if "benchmark_df" in st.session_state:
    bench_df = st.session_state["benchmark_df"]
    st.dataframe(bench_df, use_container_width=True, hide_index=True)
    plot_df = bench_df.set_index("Package count")[["DP time (ms)", "Greedy time (ms)"]]
    st.line_chart(plot_df)
    st.download_button(
        "Download benchmark CSV",
        data=bench_df.to_csv(index=False).encode("utf-8"),
        file_name="knapsack_benchmark.csv",
        mime="text/csv",
    )

with st.expander("Algorithm notes"):
    st.markdown("""
    - **0/1 Knapsack DP:** considers including or excluding each package. It returns an optimal result.
    - **Greedy:** sorts packages by value-to-weight ratio and adds each package if it fits. It is a heuristic for 0/1 Knapsack.
    - **DP complexity:** `O(nW)` time and `O(nW)` space in this table-based implementation, where `n` is the number of packages and `W` is the integer capacity.
    - **Greedy complexity:** `O(n log n)` time due to sorting, plus a linear scan.
    - This model assumes package weights and vehicle capacity are positive/non-negative integers and package values are non-negative integers.
    """)
