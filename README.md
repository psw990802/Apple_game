# 사과게임 매크로
만들게 된 동기: 예전에 모바일 게임에서 나보다 낮은 전투력을 가진 상대와 자동으로 전투를 하는 매크로를 만들고 싶었지만 숫자인식 부분에서 어려움을 겪어 실패했었는데 이번에 다시 숫자인식에 도전해보고자 만들게 되었다.

# 사용된 주요 기술 및 라이브러리
1. Opencv
2. PyTesseract
3. PyautoGUI
4. Numpy

# 프로그램 흐름
1. 화면 캡처 및 전처리
  - 특정 영역을 캡처하여 그레이스케일 변환과 이진화, 침식 연산을 적용해 숫자를 더 잘 인식할 수 있도록 하였다.
2. 숫자감지 및 OCR 인식
  - contour 검출을 이용해 숫자가 포함된 영역을 찾고 그 부분만 OCR을 적용해 인식된 숫자 정보를 리스트에 저장하였다.
3. 합이 10이 되는 숫자 조합 찾기
  - 리스트에서 드래그영역(좌표)에 있는 숫자들의 합이 10이 되는 조합을 찾는다.
4. PyautoGUI를 이용해 마우스 드래그
  - 한번 드래그한 영역내의 숫자들은 0으로 처리해 다음 드래그에 영향이 가지않도록 하였다.
5. 합이 10이 되는 조합이 있다면 드래그 반복, 없다면 프로그램 종료

# 과정
# 처음에 Template Matching을 이용해 숫자를 인식하려고 했지만 인식에 어려움을 겪음
1. 템플릿 이미지가 너무 작아 인식에 문제발생
  - 이미지를 리사이즈하여 비교하도록 했지만 여전히 인식에 어려움이 있었다.
2. 템플릿 매칭 과정에서 같은 숫자를 여러번 인식하여 배열에 저장하는 문제발생
  - 중복으로 저장되는 것을 막기 위해 좌표 일정 범위내에 있다면 중복으로 추가하지 않도록 하였지만 이것으로는 정확한 객체를 구별하기 어려웠다.

# Tesseract OCR을 사용해보기로 함
1. 전처리과정에서 임계값을 하나하나 실험해나가면서 최적값을 찾았다.
2. 하지만 OCR 결과가 기대한 것과 다르게 나오는 문제 발생
  - 숫자가 잘 보이는 화면에서도 숫자를 인식하지 못했다.
  - 다시 이진화의 임계값을 조정해보고, 모폴로지 연산을 사용해보고, OCR입력 크기를 확대해보고, OCR의 설정을 바꿔보고, contour을 사용했다.
3. OCR자체 인식률의 한계
  - 결국 화면을 125%로 확대 후 전처리를 강화하고, OCR 입력 이미지를 많이 확대하도록 했다.
4. 비슷한 위치의 숫자가 중복 저장
  - 감지된 숫자들의 좌표가 너무 가깝다면 이미 저장된 숫자의 중심점과 비교하여 새로운 숫자로 추가할지 결정하도록 하였다.

# 드래그
1. 드래그한 후에도 이전 상태의 숫자로 다시 조합을 찾는 문제가 발생
  - 드래그한 숫자는 0으로 변경하여 이후 드래그에 영향이 가지않도록 하였다.
  - 조합을 찾을때 0인 숫자는 무시하도록 하여 드래그 범위의 효율성을 높였다.
  - 이후 10이 되는 조합을 찾지 못할때까지 반복하도록 하였다.
2. 드래그 범위 안의 숫자 합이 10이 아닐 때도 드래그하는 오류 발생
  - 드래그 전에 숫자 합 검증을 통해 정확히 10일때만 드래그 하도록 하였다.
3. 드래그 인식 오류 발생
  - 드래그의 범위가 너무 타이트하여 드래그 범위를 확장하였다.
  - 드래그 속도가 너무 빠르면 게임에서 인식되지 않거나 실패하는 경우가 있어, 드래그할 범위의 대각선 길이를 기준으로 이동시간을 설정하여 작은 거리에서는 빠르게, 큰 거리에서는 느리게 드래그하도록 조정하였다.

# 테스트 및 수정
  - 중앙의 숫자부터 처리하는 것이 고득점에 유리하므로, 화면의 중심에서부터 바깥쪽으로 탐색하도록 변경하여 효율을 높였다.
또한, 이미 드래그된 숫자는 즉시 리스트에서 제외하여 불필요한 반복을 줄이고 코드 실행 속도를 개선하였다.
   


