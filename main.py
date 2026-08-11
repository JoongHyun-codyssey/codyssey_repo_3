def calculate_mac(pattern, filter_):
    score = 0

    n = len(pattern)
    if n != len(filter_):
        raise ValueError("행 수가 맞지 않습니다.")

    for i in range(n):
        if n != len(pattern[i]) or n != len(filter_[i]):
            raise ValueError("열 수가 맞지 않습니다.")
        for j in range(len(pattern[i])):
            score += pattern[i][j] * filter_[i][j]

    return float(score)

def classify_scores(score_cross, score_x, epsilon) -> str:
    if abs(score_cross - score_x) < epsilon:
        return "UNDECIDED"
    elif score_cross > score_x:
        return "Cross"
    else:
        return "X"

def normalize_label(raw_label) -> str:
    if not isinstance(raw_label, str):
        raise ValueError(f"Invalid label: {raw_label}")

    if raw_label == "+":
        return "Cross"
    elif raw_label.lower() == "cross":
        return "Cross"
    elif raw_label.lower() == "x":
        return "X"
    else:
        raise ValueError("Invalid label")

def main():
    cross = [
        [0, 1, 0],
        [1, 1, 1],
        [0, 1, 0]
    ]

    x_pattern = [
        [1, 0, 1],
        [0, 1, 0],
        [1, 0, 1],
    ]

    x_filter = [
        [1, 0, 1],
        [0, 1, 0],
        [1, 0, 1],
    ]

    x_result = calculate_mac(x_pattern, x_filter)
    cross_result = calculate_mac(cross, x_filter)
    print(x_result)
    print(cross_result)


if __name__ == "__main__":
    main()