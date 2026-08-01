REGRESSION_CASES = [
    {
        "question": "What is Chargeability?",
        "expected_route": "rag",
    },
    {
        "question": "Explain utilization.",
        "expected_route": "rag",
    },
    {
        "question": "Which location has the highest average chargeability?",
        "expected_route": "sql",
    },
    {
        "question": "Show the top 5 employees by chargeability.",
        "expected_route": "sql",
    },
    {
        "question": "Why is Hyderabad's chargeability lower than Chennai?",
        "expected_route": "both",
    },
]