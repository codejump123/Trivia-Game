def validate_wager(current_points, wager):
    if not isinstance(wager, int):
        return False, "Wager must be an integer"
    if wager <= 0:
        return False, "Wager must be positive"
    if wager > current_points:
        return False, "Wager exceeds available points"
    return True, ""


def apply_answer(current_points, wager, is_correct):
    if is_correct:
        return current_points + wager, wager
    new_points = current_points - wager
    if new_points < 0:
        new_points = 0
    return new_points, -wager


def update_stats(stats, category, is_correct):
    stats["games_played"] += 1
    if is_correct:
        stats["correct_answers"] += 1
    else:
        stats["incorrect_answers"] += 1

    by_category = stats.setdefault("by_category", {})
    category_stats = by_category.setdefault(
        category,
        {"correct_answers": 0, "incorrect_answers": 0, "games_played": 0},
    )
    category_stats["games_played"] += 1
    if is_correct:
        category_stats["correct_answers"] += 1
    else:
        category_stats["incorrect_answers"] += 1
