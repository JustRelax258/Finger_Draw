import cv2
import mediapipe as mp
import turtle
import math


mp_hands = mp.solutions.hands

# For webcam input:
cap = cv2.VideoCapture(0)
if cap.isOpened():
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)  # float `width`
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)  # float `height`

# turtle
playground = turtle.Screen()
playground.setup(width, height)
playground.title("Virtual painter")
turtle.tracer(0, 0)
t = turtle.Turtle()

t.shape('classic')
t.shapesize(1, 2)
t.settiltangle(135)
t.speed('fastest')


with mp_hands.Hands(
        model_complexity=0,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:

    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            # If loading a video, use 'break' instead of 'continue'.
            continue

        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image)

        h, w, c = image.shape
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:

                dots = list(enumerate(hand_landmarks.landmark)) # list of coordinates of dots

                x_big = dots[4][1].x * w # thumb_tip
                y_big = dots[4][1].y * h

                x_forefinger = dots[8][1].x * w # index_finger_tip
                y_forefinger = dots[8][1].y * h

                delta = math.sqrt(pow(x_forefinger - x_big, 2) + pow(y_forefinger - y_big, 2))

                if delta < 45:
                    t.color('black')
                    t.pendown()
                    t.goto(w / 2 - x_forefinger, h / 2 - y_forefinger)
                    turtle.update()
                else:
                    t.penup()
                    t.goto(w / 2 - x_forefinger, h / 2 - y_forefinger)
                    turtle.update()

        # save the paint(then you can open as pdf)
        # ts = t.getscreen()
        # ts.getcanvas().postscript(file="virtual painter.eps")
playground.exitonclick()
cap.release()


if __name__ == '__main__':
    main()
