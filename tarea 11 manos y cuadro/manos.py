import cv2
import mediapipe as mp
import math
import numpy as np

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)

cap = cv2.VideoCapture(0)

punto_obj = 8

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)
    h, w, _ = frame.shape

    x1 = y1 = x2 = y2 = None
    contador = 0

    if results.multi_hand_landmarks:
        for mano in results.multi_hand_landmarks:
            contador += 1
            mp_draw.draw_landmarks(frame, mano, mp_hands.HAND_CONNECTIONS)

            for i, lm in enumerate(mano.landmark):
                if i == punto_obj:
                    px = int(lm.x * w)
                    py = int(lm.y * h)

                    if contador == 1:
                        x1, y1 = px, py
                    else:
                        x2, y2 = px, py

    if x1 is not None and x2 is not None:
        dist = math.dist([x1, y1], [x2, y2])
        ang = math.atan2(y2 - y1, x2 - x1)

        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2

        ancho = int(dist)
        alto = int(dist * 0.5)

        rect_local = [
            (-ancho // 2, -alto // 2),
            ( ancho // 2, -alto // 2),
            ( ancho // 2,  alto // 2),
            (-ancho // 2,  alto // 2)
        ]

        rect_final = []
        for x0, y0 in rect_local:
            xr = x0 * math.cos(ang) - y0 * math.sin(ang)
            yr = x0 * math.sin(ang) + y0 * math.cos(ang)
            rect_final.append((int(cx + xr), int(cy + yr)))

        pts_cv = np.array(rect_final, np.int32).reshape((-1, 1, 2))
        cv2.polylines(frame, [pts_cv], True, (0, 255, 255), 3)  # AMARILLO

    cv2.imshow("Rectangulo Amarillo", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
