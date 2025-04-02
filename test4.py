import cv2
import pytesseract
import pyautogui
import numpy as np

# Tesseract 실행 파일 경로 설정
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# 특정 영역 설정 (x, y, width, height)
region = (0, 0, 1150, 850)

# 화면 캡처 후 특정 영역 가져오기
screenshot = pyautogui.screenshot(region=region)
screenshot = np.array(screenshot)
gray = cv2.cvtColor(screenshot, cv2.COLOR_RGB2GRAY)  # 흑백 변환

# 전처리 - 이진화 & 침식(Erosion) 연산 적용
_, thresh = cv2.threshold(gray, 175, 255, cv2.THRESH_BINARY_INV)

cv2.imshow('bin',thresh)
cv2.waitKey()

kernel = np.ones((7, 7), np.uint8)  # 커널 크기 조정 가능
processed = cv2.erode(thresh, kernel, iterations=1)  # 숫자 간격 넓히기

cv2.imshow('processed',processed)
cv2.waitKey()

# Contour를 이용해 개별 숫자 감지
cnt_num=0
contours, _ = cv2.findContours(processed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# 감지된 숫자별로 OCR 수행
for cnt in contours:
    x, y, w, h = cv2.boundingRect(cnt)
    
    if w > 20 and h > 20:  # 너무 작은 오브젝트는 무시
        roi = gray[y:y+h, x:x+w]  # 개별 숫자 영역 추출
        roi = cv2.resize(roi, (w*15, h*15))  # OCR 인식률 향상을 위해 확대

        cnt_num+=1

        # OCR 실행 (개별 숫자)
        custom_config = r'--oem 3 --psm 8 -c tessedit_char_whitelist=0123456789'
        digit = pytesseract.image_to_string(roi, config=custom_config).strip()
        
        if digit.isdigit():  # 숫자만 필터링
            print(f"숫자: {digit}, 위치: ({x+region[0]}, {y+region[1]}), 크기: {w}x{h}")

            # 시각화 (숫자 영역 표시)
            cv2.rectangle(screenshot, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(screenshot, digit, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

# 결과 표시 (테스트용)
print(f"감지객체 {cnt_num}")
cv2.imshow("OCR 결과", screenshot)
cv2.waitKey(0)
cv2.destroyAllWindows()