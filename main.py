import json

# MAC
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

# 판정
def classify_scores(score_cross, score_x, epsilon) -> str:
    if abs(score_cross - score_x) < epsilon:
        return "UNDECIDED"
    elif score_cross > score_x:
        return "Cross"
    else:
        return "X"

# 라벨 정규화
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

def load_json(path) -> dict:
    with open(path, mode="r", encoding="utf-8") as file:
        data = json.load(file)

    return data

# json 구조 검사
def validate_data_json(data) -> None:
    if type(data) != dict:
        raise ValueError(f"{data}의 형식이 잘못되었습니다. type: {type(data)}")
    elif not "filters" in data or not "patterns" in data:
        raise ValueError(f"data에 filters key 또는 patterns key가 없습니다.")
    elif type(data["filters"]) != dict or type(data["patterns"]) != dict:
        raise ValueError(f"filters 또는 patterns value type이 잘못되었습니다. filters value: {type(data["filters"])}, pattern value: {type(data['patterns'])}")

# case_id(size_13_1) n값 반환 함수
def parse_pattern_size(case_id) -> int:
    split_case_id = case_id.split("_")
    if len(split_case_id) != 3:
        raise ValueError(f"case_id의 형식이 잘못되었습니다. {case_id}")
    elif split_case_id[0] != "size":
        raise ValueError(f"case_id의 형식이 잘못되었습니다. {case_id}")

    try:
        n = int(split_case_id[1])
        int(split_case_id[2])
    except ValueError:
        raise ValueError(f"case_id 형식 n과 idx가 잘못되었습니다. {case_id}")

    return n


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