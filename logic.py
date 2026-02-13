# logic.py

def calculate_safety(data, time_of_day):
    """
    Calculates safety score based on amenities.

    Parameters:
    - data: dict with keys shops, restaurants, police, hospitals, open_24_7
    - time_of_day: "Day" or "Night"

    Returns:
    - score_percent: int (0-100)
    - level: str ("Safe", "Moderate", "Risky")
    - reasoning: str explaining the score
    """
    score = 0

    # Base weights
    score += data.get("police", 0) * 5
    score += data.get("hospitals", 0) * 3
    score += data.get("shops", 0) * 1
    score += data.get("restaurants", 0) * 1

    # Extra points for places open at night
    if time_of_day == "Night":
        score += data.get("open_24_7", 0) * 5

    # Normalize score (adjust max_possible as needed)
    max_possible = 50
    score = min(score, max_possible)
    score_percent = int((score / max_possible) * 100)

    # Determine safety level
    if score_percent >= 70:
        level = "Safe"
    elif score_percent >= 40:
        level = "Moderate"
    else:
        level = "Risky"

    # Reasoning text
    reasoning = (
        f"Shops: {data.get('shops',0)}, Restaurants: {data.get('restaurants',0)}, "
        f"Police: {data.get('police',0)}, Hospitals: {data.get('hospitals',0)}. "
    )
    if time_of_day == "Night":
        reasoning += f"Open 24/7: {data.get('open_24_7',0)}."

    return score_percent, level, reasoning
