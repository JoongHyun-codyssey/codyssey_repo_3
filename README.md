# Mini NPU Simulator

## 프로젝트 소개

Mini NPU Simulator는 AI의 핵심 연산인 **MAC(Multiply-Accumulate)** 연산을 직접 구현하여 입력된 패턴이 어떤 필터와 가장 유사한지 판별하는 Python 콘솔 프로그램입니다.

사람은 십자가(Cross)와 X 모양을 쉽게 구별할 수 있지만, 컴퓨터는 이미지의 형태를 이해하지 못하기 때문에 숫자로 이루어진 2차원 배열을 이용하여 패턴을 비교합니다.

이 프로젝트에서는 입력 패턴과 필터를 위치별로 곱한 뒤 모든 값을 더하는 MAC 연산을 직접 구현하고, 다양한 크기(3×3, 5×5, 13×13, 25×25)의 데이터를 분석하여 AI에서 사용하는 기본적인 패턴 인식 원리를 학습하는 것을 목표로 합니다.

또한 크기별 연산 시간을 측정하여 데이터 크기에 따른 시간 복잡도(O(N²))도 함께 분석합니다.

---

# 개발환경
| 항목 | 환경 |
| --- | --- |
| OS | macOS |
| Language | Python 3.13.0 |
| IDE | PyCharm |
| Terminal | PyCharm 내장 터미널 |
| Shell | Bash |
| Version Control | Git / GitHub |

# 프로젝트 목표

* MAC(Multiply-Accumulate) 연산 구현
* Cross/X 패턴 판별
* JSON 데이터 분석
* 성능 측정 및 시간 복잡도 분석
* 예외 처리 및 데이터 검증

---

# 주요 기능

## 1. 사용자 입력 모드 (3×3)

* 3×3 Cross 필터 입력
* 3×3 X 필터 입력
* 3×3 패턴 입력
* MAC 연산 수행
* 두 필터의 점수 비교
* Cross / X / UNDECIDED 판정
* 평균 연산 시간(ms) 출력

---

## 2. JSON 분석 모드

data.json 파일을 읽어 다음 기능을 수행합니다.

* 필터 로드
* 패턴 로드
* 패턴 크기 검증
* 필터 크기 검증
* MAC 연산 수행
* 예상 결과(expected)와 비교
* PASS / FAIL 출력

---

## 3. 라벨 정규화

프로그램 내부에서는 다음 두 개의 표준 라벨만 사용합니다.

| 입력 값  | 표준 라벨 |
| ----- | ----- |
| +     | Cross |
| cross | Cross |
| x     | X     |

이를 통해 입력 형식이 달라도 동일한 기준으로 비교할 수 있습니다.

---

## 4. 성능 분석

각 크기에 대해 MAC 연산을 10회 반복 수행하여 평균 실행 시간을 측정합니다.

출력 항목

* 패턴 크기
* 평균 실행 시간(ms)
* 연산 횟수(N²)

---

# 프로젝트 구조

```text
codyssey_mission_3/
│
├── main.py
├── data.json
└── README.md
```

---

# 실행 방법

### 프로그램 실행

```bash
python3 main.py
```

실행 후 원하는 모드를 선택합니다.

```
1. 사용자 입력(3×3)

2. data.json 분석

선택 :
```

---

# MAC 연산 원리

입력 패턴과 필터를 같은 위치끼리 곱한 후 모든 값을 더합니다.

예시

```
입력

0 1 0
1 1 1
0 1 0

필터

0 1 0
1 1 1
0 1 0
```

위치별 곱셈

```
0×0
1×1
0×0
1×1
1×1
1×1
0×0
1×1
0×0
```

합계

```
5
```

점수가 높을수록 해당 필터와 유사한 패턴입니다.

---

# 시간 복잡도

MAC 연산은 모든 원소를 한번씩 방문합니다.

패턴 크기가 N×N일 때

```
연산 횟수

N × N = N²
```

따라서 시간 복잡도는

```
O(N²)
```

입니다.

패턴 크기가 커질수록 연산량도 제곱에 비례하여 증가합니다.

---

# 예외 처리

다음과 같은 상황을 처리합니다.

* 입력 행 개수 오류
* 입력 열 개수 오류
* 숫자가 아닌 값 입력
* 필터와 패턴 크기 불일치
* JSON 형식 오류
* 존재하지 않는 size 필터
* 예상 라벨 오류

Mode1은 row/token 재입력을 받도록 구현했습니다.
Mode2는 schema/label/matrix 오류가 발생시 해당 case를 Fail 처리 후 다음 case 검증 진행
file/json/top-level schema 오류는 안내 후 해당 mode를 traceback없이 안전하게 종료합니다.


---

# 구현 요약
### Mode1
사용자 입력(3x3) -> cross filter, x filter, pattern순으로 구성합니다 -> MAC -> 판정 -> 연산 평균 시간 -> 결과 출력

### Mode2
data.json load -> JSON 구조 검증 -> case_id 및 n 추출 -> label, filters 데이터 정규화 -> NxN matrix 및 값 검증 -> 판정 -> 결과 출력

# 결과 리포트

### Mode 1
1.0/5.0/X를 비교했을때

| 항목 | 결과 |
| --- | --- |
| Cross Score | 1.0 |
| X Score | 5.0 |
| Prediction | X |
| Matrix 크기 | 3 × 3 |
| 평균 시간 (ms) | 0.012554 |
| 연산 횟수 (N²) | 9 |

와 같은 결과가 나온것으로 보아 정상 출력임을 확인할 수 있고, invalid 결과에 대해선 그 입력 값을 확인해 제대로 된 입력값을 받도록 재입력받도록 했다.

### Mode 2
3 PASS/3 FAIL의 결과가 나왔다.

### 테스트 결과

| Case ID | Cross Score | X Score | Prediction | Expected | Status |
| --- | ---: | ---: | --- | --- | --- |
| size_5_1 | 0.9 | 0.8999999999999999 | UNDECIDED | X | FAIL |
| size_5_2 | 8.9 | 0.1 | Cross | Cross | PASS |
| size_13_1 | 0.3 | 14.700000000000008 | X | X | PASS |
| size_13_2 | 7.499999999999997 | 7.5 | UNDECIDED | Cross | FAIL |
| size_25_1 | 4.9 | 4.899999999999999 | UNDECIDED | X | FAIL |
| size_25_2 | 52.9 | 0.1 | Cross | Cross | PASS |

### 실패 케이스

| Case ID | Prediction | Expected | 실패 원인 |
| --- | --- | --- | --- |
| size_5_1 | UNDECIDED | X | prediction과 expected_label이 다름 |
| size_13_2 | UNDECIDED | Cross | prediction과 expected_label이 다름 |
| size_25_1 | UNDECIDED | X | prediction과 expected_label이 다름 |

### 성능 측정 결과

| 크기 (N×N) | 평균 시간 (ms) | 연산 횟수 (N²) |
| --- | ---: | ---: |
| 3×3 | 0.005446 | 9 |
| 5×5 | 0.012329 | 25 |
| 13×13 | 0.045883 | 169 |
| 25×25 | 0.138887 | 625 |

### 결과 요약

| 항목 | 결과 |
| --- | ---: |
| 전체 테스트 | 6 |
| PASS | 3 |
| FAIL | 3 |

fixed overhead/noise/10회 평균 해석
fixed overhead는 모든 측정에 공통으로 더해진다. 또한 10회라는 평균값을 내는 이유는 측정할때마다 매번 동일한 시간 측정을 보장하지 않는다. random noise의 영향으로 인해 매번 값이 달라진다. 이 영향을 완화하기 위해 10회 평균 값을 내어 안정적인 대표값을 만드는 것이다.

## 실패 원인 분석
3 FAIL의 case_id는 size_5_1, size_13_2, size_25_1가 FAIL의 결과를 받았다.
3 FAIL은 epsilon tie로 인해 FAIL을 받았다

| 항목 | Score Cross | Score X |
| --- | ---: | ---: |
| 1 | 0.9 | 0.8999999999999999 |
| 2 | 7.499999999999997 | 7.5 |
| 3 | 4.9 | 4.899999999999999 |

```
epsilon = 1e-9
```

현재 epsilon에서는 거의 같은 score를 UNDECIDED로 처리한다.
지금보다 epsilon 값을 작게 한다 하더라도 FAIL을 받았던 각 case는 expected label과 반대의 경우로 나오기 때문에 epsilon을 변경하더라도 여전히 FAIL이며 epsilon을 정하는 정책으로 인해 너무 작으면 false winner, 너무 크면 false tie의 trade-off가 생긴다.
따라서 PASS 수에 맞춰 임의로 값을 정하면 안된다.

---

## 성능 분석
```bash
크기(N×N) | 평균 시간(ms) | 연산 횟수(N²)
3x3 | 0.005446 | 9
5x5 | 0.012329 | 25
13x13 | 0.045883 | 169
25x25 | 0.138887 | 625
```
MAC algorithm은 matrix 크기가 NxN일때 연산 횟수는 NxN = N²이다.
그렇기때문에 시간 복잡도는 O(N²)이지만, 실제 측정 시간은 N² 증가 비율과 같지 않을 수 있는 이유는 fixed overhead와 random noise와 관련이 있다.
fixed overhead란 모든 함수 호출에 있어 비교적 고정된 시간을, random noise란 실행마다 측정 시간을 흔드는 요인이다. 
이 두 가지의 요소로 인해 측정 값이 N² 비율과 정확히 일치하지 않게된다.

그러하여 표를 보면 연산 횟수가 9 -> 25 -> 169 -> 625 | 3 -> 5 -> 13 -> 25의 제곱을 형태로 증가하기 때문에 평균 시간도 대체로 증가하는 것을 볼 수 있다.
다만 시간 비율이 N²와 같지 않은 이유는 fixed overhead와 random noise의 영향을 받기 때문이다.
