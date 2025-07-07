import cv2
import time
import math
from PIL import Image

# --- CONFIGURATION ---
BUTTON_POS = (50, 400, 300, 480)  # x1, y1, x2, y2


def draw_button(frame, label="Take Photos"):
    x1, y1, x2, y2 = BUTTON_POS
    cv2.rectangle(frame, (x1, y1), (x2, y2), (50, 200, 50), -1)
    cv2.putText(
        frame, label, (x1 + 20, y1 + 55),
        cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 3, cv2.LINE_AA
    )
    return frame


def is_inside_button(x, y):
    x1, y1, x2, y2 = BUTTON_POS
    return x1 <= x <= x2 and y1 <= y <= y2


# Mouse click flag
mouse_clicked = False


def mouse_callback(event, x, y, flags, param):
    global mouse_clicked
    if event == cv2.EVENT_LBUTTONDOWN and is_inside_button(x, y):
        mouse_clicked = True


def show_countdown(cap, duration=3):
    start_time = time.time()
    font = cv2.FONT_HERSHEY_SIMPLEX

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)  # 👈 Flip preview (mirror)

        elapsed = time.time() - start_time
        remaining = duration - int(elapsed)

        height, width = frame.shape[:2]
        center = (width // 2, height // 2)

        if remaining > 0:
            # Pop effect
            scale = 1.0 + 0.5 * math.sin((elapsed % 1) * math.pi)
            number = str(remaining)
            font_scale = 4 * scale
            thickness = int(8 * scale)

            text_size = cv2.getTextSize(number, font, font_scale, thickness)[0]
            text_x = center[0] - text_size[0] // 2
            text_y = center[1] + text_size[1] // 2

            radius = max(text_size[0], text_size[1]) // 2 + 30
            cv2.circle(frame, center, radius, (0, 0, 255), 5)
            cv2.putText(frame, number, (text_x, text_y), font, font_scale, (0, 0, 255), thickness, cv2.LINE_AA)
        else:
            return cv2.flip(frame, 1)  # 👈 Flip again before saving (mirror photo)

        cv2.imshow("Camera", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


def take_photo_sequence(cap, total_photos=3):
    for i in range(total_photos):
        print(f"Taking photo {i + 1}...")
        frame = show_countdown(cap, duration=3)
        if frame is not None:
            filename = f"./resources/captured_photo{i}.jpg"
            cv2.imwrite(filename, frame)  # Already flipped
            print(f"Saved {filename}")
        time.sleep(0.5)


def compile_strip():
    bg = Image.open("./resources/background.png").convert("RGBA")
    bgX = 192
    bgY = 578
    target_size = (160, 90)
    x_pos = int((bgX - target_size[0]) / 2)

    imgs = [Image.open(f"./resources/captured_photo{i}.jpg").convert("RGBA") for i in range(3)]
    positions = [(x_pos, 72), (x_pos, 72 + 144), (x_pos, 72 + 144 + 144)]
    resized = [im.resize(target_size, Image.Resampling.LANCZOS) for im in imgs]

    for im, pos in zip(resized, positions):
        bg.paste(im, pos, im)

    bg.save("./resources/composite.png")
    print("Saved composite strip as 'composite.png'")


# --- MAIN LOOP ---
cap = cv2.VideoCapture(0)
cv2.namedWindow("Camera")
cv2.setMouseCallback("Camera", mouse_callback)

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)  # 👈 Flip live preview

        frame = draw_button(frame)
        cv2.imshow("Camera", frame)

        key = cv2.waitKey(1) & 0xFF

        # Trigger session
        if mouse_clicked or key == ord(' '):
            mouse_clicked = False
            take_photo_sequence(cap)
            compile_strip()
            print("Ready for another session!")

        # Handle close (either with 'q' or window close)
        if key == ord('q') or cv2.getWindowProperty("Camera", cv2.WND_PROP_VISIBLE) < 1:
            break

finally:
    cap.release()
    cv2.destroyAllWindows()
