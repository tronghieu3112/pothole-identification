import cv2

# Mở camera (0 là chỉ số camera mặc định)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Không thể mở camera")
    exit()

while True:
    # Đọc từng frame từ camera
    ret, frame = cap.read()

    if not ret:
        print("Không thể nhận frame. Đã thoát...")
        break

    # Chuyển đổi frame sang ảnh grayscale (ảnh xám)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Làm mờ ảnh để giảm nhiễu
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # Phát hiện cạnh bằng Canny Edge Detection
    edges = cv2.Canny(blur, 50, 150)

    # Tìm các contour trong ảnh
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Lọc và vẽ các contour có thể là ổ gà dựa trên kích thước và hình dạng
    for contour in contours:
        area = cv2.contourArea(contour)

        # Lọc những vùng có diện tích nhỏ để loại bỏ nhiễu
        if area > 1000:
            # Tìm bounding box của contour
            x, y, w, h = cv2.boundingRect(contour)

            # Vẽ hình chữ nhật bao quanh các vùng phát hiện
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Hiển thị kết quả
    cv2.imshow('Pothole Detection', frame)

    # Nhấn 'q' để thoát vòng lặp
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Giải phóng tài nguyên và đóng cửa sổ
cap.release()
cv2.destroyAllWindows()
