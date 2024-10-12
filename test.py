from ultralytics import YOLO
import cv2
import numpy as np

# Load a model
model = YOLO("best.pt")  # Thay "best.pt" bằng đường dẫn đến mô hình của bạn
class_names = model.names

# Mở camera (0 là chỉ số camera mặc định)
cap = cv2.VideoCapture(0)

# Kiểm tra xem camera có mở được không
if not cap.isOpened():
    print("Không thể mở camera")
    exit()

count = 0

while True:
    ret, img = cap.read()
    if not ret:
        print("Không thể nhận khung hình từ camera, thoát...")
        break

    count += 1
    if count % 3 != 0:  # Xử lý 1 khung hình sau mỗi 3 lần đọc để giảm tải
        continue

    img = cv2.resize(img, (1020, 500))  # Thay đổi kích thước khung hình
    h, w, _ = img.shape

    # Dự đoán đối tượng trên khung hình
    results = model.predict(img)

    for r in results:
        boxes = r.boxes  # Boxes object for bbox outputs
        masks = r.masks  # Masks object for segment masks outputs

        if masks is not None:
            masks = masks.data.cpu()
            for seg, box in zip(masks.data.cpu().numpy(), boxes):
                seg = cv2.resize(seg, (w, h))
                contours, _ = cv2.findContours(seg.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                for contour in contours:
                    d = int(box.cls)  # Lấy chỉ số của lớp
                    c = class_names[d]  # Lấy tên của lớp
                    x, y, x1, y1 = cv2.boundingRect(contour)  # Vẽ bounding box cho mỗi contour
                    cv2.polylines(img, [contour], True, color=(0, 0, 255), thickness=2)
                    cv2.putText(img, c, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    # Hiển thị khung hình đã xử lý
    cv2.imshow('Camera Detection', img)

    # Nhấn 'q' để thoát khỏi vòng lặp
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Giải phóng camera và đóng tất cả cửa sổ
cap.release()
cv2.destroyAllWindows()
