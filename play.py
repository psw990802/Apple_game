import cv2
import pytesseract
import pyautogui
import numpy as np
import time

# Tesseract 실행 파일 경로 설정
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# 특정 영역 설정 (x, y, width, height)
region = (0, 0, 1150, 850)
center_x = region[2] // 2  # 화면 중앙 X
center_y = region[3] // 2  # 화면 중앙 Y

# 화면 캡처 후 특정 영역 가져오기
screenshot = pyautogui.screenshot(region=region)
screenshot = np.array(screenshot)
gray = cv2.cvtColor(screenshot, cv2.COLOR_RGB2GRAY)  # 흑백 변환

# 전처리 - 이진화, 침식(Erosion) 연산 적용
_, thresh = cv2.threshold(gray, 175, 255, cv2.THRESH_BINARY_INV)
kernel = np.ones((7, 7), np.uint8)
processed = cv2.erode(thresh, kernel, iterations=1)

# Contour를 이용해 개별 숫자 감지
contours, _ = cv2.findContours(processed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# 감지된 숫자의 정보 저장 (숫자, 위치, 크기)
detected_numbers = []
for cnt in contours:
    x, y, w, h = cv2.boundingRect(cnt)

    if w > 20 and h > 20:  # 너무 작은 오브젝트는 무시
        roi = gray[y:y+h, x:x+w]  # 개별 숫자 영역 추출
        roi = cv2.resize(roi, (w*15, h*15))  # OCR 인식률 향상을 위해 확대

        # OCR 실행 (개별 숫자)
        custom_config = r'--oem 3 --psm 8 -c tessedit_char_whitelist=0123456789'
        digit = pytesseract.image_to_string(roi, config=custom_config).strip()

        if digit.isdigit():  # 숫자만 필터링
            detected_numbers.append({
                "num": int(digit), "x": x, "y": y, "w": w, "h": h,
                "dist": (x - center_x) ** 2 + (y - center_y) ** 2  # 중심에서의 거리
            })

# 중앙에서 가까운 순서대로 정렬
detected_numbers.sort(key=lambda item: item["dist"])

while True:
    found_combination = False  # 조합이 발견되었는지 확인

    for i in range(len(detected_numbers)):
        if detected_numbers[i]["num"] == 0:
            continue  # 이미 사용된 숫자는 무시

        num1 = detected_numbers[i]["num"]
        x1, y1, w1, h1 = detected_numbers[i]["x"], detected_numbers[i]["y"], detected_numbers[i]["w"], detected_numbers[i]["h"]

        for j in range(i + 1, len(detected_numbers)):
            if detected_numbers[j]["num"] == 0:
                continue  # 이미 사용된 숫자는 무시

            num2 = detected_numbers[j]["num"]
            x2, y2, w2, h2 = detected_numbers[j]["x"], detected_numbers[j]["y"], detected_numbers[j]["w"], detected_numbers[j]["h"]

            # 드래그 영역 설정
            left = min(x1, x2) - 5
            top = min(y1, y2) - 5
            right = max(x1 + w1, x2 + w2) + 20
            bottom = max(y1 + h1, y2 + h2) + 18

            # 드래그 범위 내 숫자들의 합 계산
            total = 0
            included_numbers = []

            for item in detected_numbers:
                if item["num"] == 0:
                    continue  # 이미 사용된 숫자는 무시

                ix, iy, iw, ih, inum = item["x"], item["y"], item["w"], item["h"], item["num"]

                # 숫자가 드래그 범위에 포함되는지 확인
                if (ix <= right and ix + iw >= left) and (iy <= bottom and iy + ih >= top):
                    total += inum
                    included_numbers.append(item)

            if total == 10:
                found_combination = True  # 조합을 찾았으므로 다시 탐색

                # 드래그 거리 계산 (대각선 거리)
                drag_distance = np.sqrt((right - left) ** 2 + (bottom - top) ** 2)

                # 드래그 속도 조절 (거리 비례)
                min_time = 0.2  # 최소 0.2초
                max_time = 1.4  # 최대 1.4초
                max_distance = 450  # 기준 거리 (400px)
                drag_time = min_time + (max_time - min_time) * min(1, drag_distance / max_distance)

                # 드래그 시작 (마우스 누르기)
                pyautogui.moveTo(left + region[0], top + region[1], duration=0.1)
                pyautogui.mouseDown()

                # 드래그 이동 (속도 조절 적용)
                pyautogui.moveTo(right + region[0], bottom + region[1], duration=drag_time)

                # 끝지점에서 0.1초 대기 후 마우스 떼기
                time.sleep(0.1)
                pyautogui.mouseUp()

                # 사용된 숫자들을 0으로 처리하여 다시 탐색 가능하게 함
                for item in included_numbers:
                    item["num"] = 0  # 숫자를 0으로 변경하여 다시 계산할 때 무시되도록 처리

                break
        if found_combination:
            break  # 조합을 찾으면 다시 탐색

    # 조합을 찾았으면 반복
    if found_combination:
        continue

    # 조합을 못 찾으면 종료
    break

time.sleep(0.1)
