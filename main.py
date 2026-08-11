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

# matrix 검증 함수 (NxN, row list, column list, column value)
def validate_square_matrix(matrix, expected_n, matrix_name) -> None:
    if type(matrix) != list:
        raise ValueError(f"{matrix_name}이 list가 아니기 때문에 {expected_n}과 비교할 수 없습니다.")
    elif len(matrix) != expected_n:
        raise ValueError(f"{matrix_name}의 row 수가 {expected_n}과 일치하지 않습니다."
                         f"matrix_row: {len(matrix)}")

    for i in range(len(matrix)):
        if type(matrix[i]) != list:
            raise ValueError(f"{matrix_name} list가 type list가 아닌 row가 존재합니다.")
        elif len(matrix[i]) != expected_n:
            raise ValueError(f"{matrix_name} row가 {expected_n}과 일치하지 않습니다.")
        for j in range(len(matrix[i])):
            if type(matrix[i][j]) not in (int, float):
                raise ValueError(f"{matrix_name}의 Row index: {i}, column index: {j}, value: {matrix[i][j]}의 type이 {type(matrix[i][j])}이기 때문에 검증에 실패했습니다.")

# n값 반환 -> data.json filters dict 정규화 -> matrix 검증 -> MAC -> PASS/FAIL -> 결과 반환
def analyze_case(case_id, case_data, filters) -> dict:
    if type(case_data) != dict:
        raise ValueError(f"{case_id}가 {type(case_data)}의 type이기 때문에 값을 처리할 수 없습니다.")

    n = parse_pattern_size(case_id=case_id)
    size_key = f"size_{n}"

    # filter_group = data.json의 filters key: size_key
    filter_group = filters[size_key]

    # pattern = data.json의 patterns case_id의 value
    pattern = case_data["input"]
    normalized_filters = {}

    # 정규화 작업후 할당
    expected_label = normalize_label(case_data["expected"])

    # raw_label: data.json filters의 비정규화 라벨("cross", "x" 등) matrix: filters 2차원 배열
    # normalized_filters 라벨 정규화 한것을 key, filters 2차원 배열을 value로 정규화한 dict 생성
    for raw_label, matrix in filter_group.items():
        normalized_filters[normalize_label(raw_label)] = matrix

    validate_square_matrix(normalized_filters["Cross"], n, "Cross Filter")
    validate_square_matrix(normalized_filters["X"], n, "X Filter")
    validate_square_matrix(pattern, n, "Pattern")

    score_cross = calculate_mac(pattern=pattern, filter_=normalized_filters["Cross"])
    score_x = calculate_mac(pattern=pattern, filter_=normalized_filters["X"])
    prediction = classify_scores(score_cross=score_cross, score_x=score_x)

    passed = prediction == expected_label

    if passed:
        status = "PASS"
        reason = None
    else:
        status = "FAIL"
        reason = f"prediction과 expected_label이 다르다. prediction: {prediction}, expected_label: {expected_label}"

    return {
        "case_id" : case_id,
        "score_cross" : score_cross,
        "score_x" : score_x,
        "prediction" : prediction,
        "expected" : expected_label,
        "passed" : passed,
        "status" : status,
        "reason" : reason
    }

# json 구조 검증 -> case 순회하며 결과 수집 -> 수집된 결과 반환
def analyze_batch(data) -> list[dict]:
    validate_data_json(data)

    results = []
    filters = data["filters"]
    patterns = data["patterns"]

    for (case_id, case_data) in patterns.items():
        try:
            result = analyze_case(case_id=case_id, case_data=case_data, filters=filters)
        except (KeyError, ValueError) as error:
            result = {
                "case_id": case_id,
                "score_cross": None,
                "score_x": None,
                "prediction": None,
                "expected": None,
                "passed": False,
                "status": "FAIL",
                "reason": str(error)
            }

        results.append(result)

    return results

# 결과 요약 반환 함수
def summarize_results(results) -> dict:
    total_count = len(results)
    pass_count = 0
    fail_count = 0
    failure_cases = []

    for result in results:
        if result["passed"] == True:
            pass_count += 1
        else:
            fail_count += 1
            failure_cases.append({
                "case_id" : result["case_id"],
                "reason" : result["reason"]
            })

    return {
        "total" : total_count,
        "passed" : pass_count,
        "failed" : fail_count,
        "failure_cases" : failure_cases
    }

# 사용자 입력 받아 matrix 구성 함수
def read_matrix(matrix_name, n=3) -> list[list]:

# 평균 시간(ms) 측정 함수
def measure_mac_average_ms(pattern, filter_, repeats=10) -> float:

# 성능 분석 함수
def measure_performance_sizes(sizes=(3, 5, 13, 25), repeats=10) -> list[dict]:

# 평균 시간(ms) 측정 시 matrix 구성 함수
def create_benchmark_matrix(n) -> list[list]:

# 결과 출력 함수
def print_batch_report(results, summary, performance_rows) -> None:
    for result in results:
        print(
            f"case_id: {result['case_id']} | "
            f"score_cross: {result['score_cross']} | "
            f"score_x: {result['score_x']} | "
            f"prediction: {result['prediction']} | "
            f"expected: {result['expected']} | "
            f"status: {result['status']}"
        )
        if result["reason"] != None:
            print(
                f"reason: {result['reason']}"
            )

        print_performance_table(performance_rows=performance_rows)

        print(
            f"total: {summary['total']} | "
            f"passed: {summary['passed']} | "
            f"failed: {summary['failed']}"
        )

        if len(summary["failure_cases"]) != 0:
            for failure in summary["failure_cases"]:
                print(
                    f"failure_cases: {failure['case_id']} | "
                    f"failure_cases_reason: {failure['reason']}"
                )

# 성능 분석 결과 출력 함수
def print_performance_table(performance_rows) -> None

# 모드 1번 선택시 호출되는 함수
def run_manual_mode() -> None:

# 모드 2번 선택시 호출되는 함수
def run_json_mode(path="data.json") -> None:

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