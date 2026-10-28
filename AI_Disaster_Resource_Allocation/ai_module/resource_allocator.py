
def recommend_allocation(zones, total_resources):
    """
    Recommend how to distribute relief resources
    according to disaster priority scores.
    This is a rule-based recommendation, not an automatic dispatch.
    """
    if total_resources < 0:
        raise ValueError("Total resources cannot be negative.")

    if not zones:
        return []

    # Highest-priority zones receive recommendations first.
    sorted_zones = sorted(
        zones,
        key=lambda zone: zone["priority"],
        reverse=True
    )

    total_priority = sum(
        max(0, zone["priority"]) for zone in sorted_zones
    )

    recommendations = []

    if total_priority == 0:
        for zone in sorted_zones:
            recommendations.append({
                "zone": zone["name"],
                "location": zone["location"],
                "priority": zone["priority"],
                "recommended_resources": 0
            })
        return recommendations

    remaining = total_resources

    for index, zone in enumerate(sorted_zones):
        if index == len(sorted_zones) - 1:
            allocation = remaining
        else:
            allocation = round(
                total_resources
                * max(0, zone["priority"])
                / total_priority
            )
            allocation = min(allocation, remaining)

        remaining -= allocation

        recommendations.append({
            "zone": zone["name"],
            "location": zone["location"],
            "priority": zone["priority"],
            "recommended_resources": allocation
        })

    return recommendations


if __name__ == "__main__":
    sample_zones = [
        {"name": "Flood Zone", "location": "Ludhiana", "priority": 62},
        {"name": "Rainfall Zone", "location": "Chandigarh", "priority": 30},
        {"name": "Storm Zone", "location": "Delhi", "priority": 17}
    ]

    results = recommend_allocation(sample_zones, 100)

    for result in results:
        print(result)
