
def calculate_priority(severity, people_affected, resources_available):
    """
    Calculate a disaster priority score from 0 to 100.
    Higher scores mean the zone needs attention sooner.
    """

    severity_scores = {
        "Low": 20,
        "Medium": 50,
        "High": 80,
        "Critical": 100
    }

    severity_score = severity_scores.get(
        severity.title(), 20
    )

    # More affected people increases priority.
    population_score = min(people_affected / 5, 100)

    # Fewer available resources increases priority.
    shortage_score = max(
        0,
        100 - resources_available
    )

    priority = (
        0.50 * severity_score
        + 0.30 * population_score
        + 0.20 * shortage_score
    )

    return round(min(max(priority, 0), 100))


if __name__ == "__main__":
    score = calculate_priority("High", 200, 50)
    print("Calculated priority score:", score)
