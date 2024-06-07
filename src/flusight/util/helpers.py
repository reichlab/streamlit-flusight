round_ids = [
    "2023-10-07",
    "2023-10-14",
    "2023-10-21",
    "2023-10-28",
    "2023-11-04",
    "2023-11-11",
    "2023-11-18",
    "2023-11-25",
    "2023-12-02",
    "2023-12-09",
    "2023-12-16",
    "2023-12-23",
    "2023-12-30",
    "2024-01-06",
    "2024-01-13",
    "2024-01-20",
    "2024-01-27",
    "2024-02-03",
    "2024-02-10",
    "2024-02-17",
    "2024-02-24",
    "2024-03-02",
    "2024-03-09",
    "2024-03-16",
    "2024-03-23",
    "2024-03-30",
    "2024-04-06",
    "2024-04-13",
    "2024-04-20",
    "2024-04-27",
    "2024-05-04",
]


def get_round(current_round_id, direction="next"):
    """Return the next or previous round_id."""
    current_round_index = round_ids.index(current_round_id)
    if direction == "next":
        new_index = current_round_index + 1
    elif direction == "previous":
        new_index = current_round_index - 1
    else:
        raise ValueError("Invalid direction. Must be 'next' or 'previous'.")

    try:
        new_round_id = round_ids[new_index]
    except IndexError:
        new_round_id = current_round_id

    return new_round_id
