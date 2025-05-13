import re

def extract_financial_metrics(summary: str) -> dict:
    """
    Extract key financial numbers from an LLM-generated summary.

    Returns a dictionary like:
    {
        'net_sales': 394340000000,
        'net_income': 99900000000,
        ...
    }
    """
    metrics = {}

    # Common patterns
    patterns = {
        'net_sales': r"net sales (?:were|was|is|of)?\s*\$?([\d,.]+)\s*(billion|million)?",
        'net_income': r"net income (?:was|were|of)?\s*\$?([\d,.]+)\s*(billion|million)?",
        'gross_margin': r"gross margin (?:was|of)?\s*\$?([\d,.]+)\s*(billion|million)?",
        'operating_income': r"operating income (?:was|of)?\s*\$?([\d,.]+)\s*(billion|million)?",
        'total_assets': r"total assets (?:were|was|of)?\s*\$?([\d,.]+)\s*(billion|million)?"
    }

    for key, pattern in patterns.items():
        match = re.search(pattern, summary, re.IGNORECASE)
        if match:
            number, unit = match.groups()
            number = float(number.replace(",", ""))
            if unit:
                if unit.lower() == "billion":
                    number *= 1_000_000_000
                elif unit.lower() == "million":
                    number *= 1_000_000
            metrics[key] = number

    return metrics
