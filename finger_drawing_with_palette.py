import cv2
import mediapipe as mp
import turtle
import math

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

# For static images:
IMAGE_FILES = []
with mp_hands.Hands(
    static_image_mode=True,
    max_num_hands=2,
    min_detection_confidence=0.5) as hands:
  for idx, file in enumerate(IMAGE_FILES):
    # Read an image, flip it around y-axis for correct handedness output (see
    # above).
    image = cv2.flip(cv2.imread(file), 1)
    # Convert the BGR image to RGB before processing.
    results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

    # Print handedness and draw hand landmarks on the image.
    print('Handedness:', results.multi_handedness)
    if not results.multi_hand_landmarks:
      continue
    image_height, image_width, _ = image.shape
    annotated_image = image.copy()
    for hand_landmarks in results.multi_hand_landmarks:
      print('hand_landmarks:', hand_landmarks)
      print(
          f'Index finger tip coordinates: (',
          f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * image_width}, '
          f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * image_height})'
      )
      mp_drawing.draw_landmarks(
          annotated_image,
          hand_landmarks,
          mp_hands.HAND_CONNECTIONS,
          mp_drawing_styles.get_default_hand_landmarks_style(),
          mp_drawing_styles.get_default_hand_connections_style())
    cv2.imwrite(
        '/tmp/annotated_image' + str(idx) + '.png', cv2.flip(annotated_image, 1))
    # Draw hand world landmarks.
    if not results.multi_hand_world_landmarks:
      continue
    for hand_world_landmarks in results.multi_hand_world_landmarks:
      mp_drawing.plot_landmarks(
        hand_world_landmarks, mp_hands.HAND_CONNECTIONS, azimuth=5)

# For webcam input:
cap = cv2.VideoCapture(0)
if cap.isOpened():
    # width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)  # float `width`
    # height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)  # float `height`
    # # or
    width = cap.get(3) *0.8 # float `width`
    height = cap.get(4) *0.8 # float `height`


#turtle
playground = turtle.Screen()  # use nouns for objects, play is a verb
playground.setup(width,height)
playground.title("Virtual painter")
turtle.tracer(3, 0)
# t_test = turtle.Turtle()
t = turtle.Turtle()
t_stamps = turtle.Turtle()
t_stamps.shape('square')
t_stamps.shapesize(3,2)
# t_green = turtle.Turtle()
t.shape('classic')
# t.fillcolor('black')
t.shapesize(1,2)
t.settiltangle(135)
t.speed('fastest')

def stamps():
    t_stamps.hideturtle()
    t_stamps.penup()
    t_stamps.color('black')
    t_stamps.goto(width-(width/2+48), 130)
    t_stamps.write('color', font=("Comic Sans MS", 14, "normal"))

    t_stamps.color('red')
    t_stamps.goto(width-(width/2+30),100)
    t_stamps.stamp()

    t_stamps.color('white')
    t_stamps.goto(width - (width / 2 + 30), 39)
    t_stamps.stamp()

    t_stamps.color('blue')
    t_stamps.goto(width - (width / 2 + 30), -22)
    t_stamps.stamp()
    t_stamps.stamp()

    t_stamps.color('green')
    t_stamps.goto(width - (width / 2 + 30), -83)
    t_stamps.stamp()
    t_stamps.stamp()

    t_stamps.color('black')
    t_stamps.goto(width - (width / 2 + 30), -144)
    t_stamps.stamp()
    t_stamps.stamp()
    turtle.update()

    #clear
    # t_test.goto(width - (width / 2 + 50), -220)
    t_stamps.goto(width - (width / 2+47), -238)
    t_stamps.write('clear', font=("Comic Sans MS", 15, "normal"))
    t_stamps.goto(width - (width / 2+51), -250)
    t_stamps.pendown()
    t_stamps.forward(40)
    t_stamps.left(90)
    t_stamps.forward(40)
    t_stamps.left(90)
    t_stamps.forward(40)
    t_stamps.left(90)
    t_stamps.forward(40)

    # # size
    # t_stamps.penup()
    # t_test.goto(width - (width / 2 + 50), 270)
    # t_stamps.goto(width - (width / 2 + 50), 270)
    # t_stamps.goto(width - (width / 2 + 48), 270)
    # t_stamps.pendown()
    # t_stamps.write('size', font=("Comic Sans MS", 14, "normal"))



stamps()

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

    # Draw the hand annotations on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    h, w, c = image.shape
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            dots = list(enumerate(hand_landmarks.landmark))
            x_big = dots[4][1].x*w
            y_big = dots[4][1].y*h
            x_forefinger = dots[8][1].x*w
            y_forefinger = dots[8][1].y*h
            delta = math.sqrt( pow(x_forefinger-x_big,2) + pow(y_forefinger-y_big,2) )

            #условие растояния между кончиками
            if delta>45:
                t.pendown()
                t.goto(w/2-x_forefinger, h/2-y_forefinger)
                turtle.update()
            else:
                t.penup()
                t.goto(w / 2 - x_forefinger, h / 2 - y_forefinger)
                if t.xcor() > width - (width / 2 + 30) - 20:
                    if 70 < t.ycor() < 130:
                        t.pencolor('red')
                    elif 10 < t.ycor() < 70:
                        t.pencolor('white')
                    elif -50 < t.ycor() < 10:
                        t.pencolor('blue')
                    elif -110 < t.ycor() < -50:
                        t.pencolor('green')
                    elif -170 < t.ycor() < -110:
                        t.pencolor('black')
                    elif -250 < t.ycor() < -210:
                        t.clear()
    # t_test.goto(width - (width / 2 + 33) - 20,-210)


    turtle.update()

    ts = t.getscreen()
    ts.getcanvas().postscript(file="virtual painter.eps")

playground.exitonclick()
cap.release()
