def calculate_confidence(domain_type, sector, score):

    if domain_type != "Corporate":
        return "Medium Confidence"

    if sector == "Unknown":
        return "Low Confidence"

    if score >= 0.1:
        return "High Confidence"

    if score >= 0.05:
        return "Medium Confidence"

    return "Low Confidence"