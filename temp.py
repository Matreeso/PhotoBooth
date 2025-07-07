import cv2
import time
import math

# Open the default camera
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Cannot open camera")
    exit()

cv2.namedWindow("Camera", cv2.WINDOW_NORMAL)

# Countdown settings
countdown = 5
start_time = time.time()
last_second = countdown

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    elapsed = time.time() - start_time
    remaining = countdown - int(elapsed)

    # Center of the frame
    height, width = frame.shape[:2]
    center = (width // 2, height // 2)

    if remaining > 0:
        # Pop animation size (pulse effect)
        scale = 1.0 + 0.5 * math.sin((elapsed % 1) * math.pi)

        number = str(remaining)
        font = cv2.FONT_HERSHEY_SIMPLEX

        # Adjust font size and thickness based on scale
        font_scale = 4 * scale
        thickness = int(8 * scale)

        # Get text size
        text_size = cv2.getTextSize(number, font, font_scale, thickness)[0]
        text_x = center[0] - text_size[0] // 2
        text_y = center[1] + text_size[1] // 2

        # Draw circle around text
        radius = max(text_size[0], text_size[1]) // 2 + 30
        cv2.circle(frame, center, radius, (0, 0, 255), 5)

        # Draw countdown number
        cv2.putText(frame, number, (text_x, text_y), font, font_scale, (0, 0, 255), thickness, cv2.LINE_AA)

    else:
        # Save the frame
        time.sleep(0.5)
        cv2.imwrite("captured_photo.jpg", frame)
        print("Photo saved as 'captured_photo.jpg'")
        break

    cv2.imshow("Camera", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
