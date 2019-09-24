import numpy as np
import os
import sys
from PIL import Image
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Activation, Flatten, Dense, Dropout, LeakyReLU
from keras import backend as K
import time
from screen import Screen
from personality import Personality, Sound
from zumi.zumi import Zumi
from camera import Camera
from crop import Crop
from parking_with_counter import Drive

# set input resolution
WIDTH = 64
HEIGHT = 64
landmark = ['bigben', 'china', 'nyc', 'eiffel', 'seattle']
LAND_PATH = os.path.dirname(os.path.abspath(__file__)) + "/landmark/"
READ_PATH = os.path.dirname(os.path.abspath(__file__)) + "/reading/"

duration = 1
if len(sys.argv) != 1:
    duration = float(sys.argv[1])

if K.image_data_format() == 'channels_first':
    input_shape = (3, WIDTH, HEIGHT)
else:
    input_shape = (WIDTH, HEIGHT, 3)

weight_file = '/home/pi/ISTE/landmark/weight_drawing.hdf5'


def generate_calssification_model(filen=weight_file):
    model = Sequential()

    model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(64, 64, 3)))
    model.add(Conv2D(64, (3, 3), activation='relu'))
    model.add(Dropout(0.1))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Conv2D(64, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Flatten())
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(0.1))
    model.add(Dense(5, activation='softmax'))

    model.load_weights(filen)
    # compile
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    print(filen)
    return model


def predict(model):
    c = Crop()
    eye = Screen()
    zumi = Zumi()
    camera = Camera(64, 64)
    personality = Personality(zumi, eye)

    cnt = 0
    prev_label = -1
    cnt_none_crop = 0
    try:
        while True:
            img = camera.run()
            crop_img = c.crop(img)
            if crop_img is None:

                if cnt_none_crop == 0:
                    personality.look_around_open01()
                elif cnt_none_crop == 1:
                    personality.look_around_open02()
                elif cnt_none_crop == 2:
                    personality.look_around_open03()
                elif cnt_none_crop == 3:
                    personality.look_around_open04()

                prev_label = -1
                print(cnt, prev_label, cnt_none_crop)
                cnt_none_crop += 1
                cnt_none_crop %= 4

                continue
            else:
                cnt_none_crop = 0

            x = Image.fromarray(crop_img)
            x = np.expand_dims(x, axis=0)
            preds = model.predict_classes(x)
            print(landmark[preds[0]])

            if prev_label == preds[0]:
                cnt += 1
                if cnt > 2:
                    print(eye.EYE_IMAGE_FOLDER_PATH + "sad1.ppm")
                    print("reaction!!!!")
                    eye.draw_image(eye.path_to_image(LAND_PATH + landmark[preds[0]] + ".jpg"))
                    time.sleep(2)
                    drive = Drive(Zumi())
                    if landmark[preds[0]] == 'eiffel':
                        drive.run_demo("a")
                    elif landmark[preds[0]] == 'nyc':
                        drive.run_demo("d")
                    elif landmark[preds[0]] == 'seattle':
                        drive.run_demo("i")
                    elif landmark[preds[0]] == 'china':
                        drive.run_demo("c")
                    else:
                        drive.run_demo("e") # london

                    personality.celebrate()
                    time.sleep(.5)

                    # if landmark[preds[0]] == 'eiffel':
                    #     zumi.turn_left(90)
                    # elif landmark[preds[0]] == 'nyc':
                    #     zumi.turn_left(45)
                    # elif landmark[preds[0]] == 'seattle':
                    #     zumi.turn_right(45)
                    # elif landmark[preds[0]] == 'china':
                    #     zumi.turn_right(90)
                    # else:
                    #     pass # london

                    cnt = 0
                else:
                    personality.reading(eye.path_to_image(READ_PATH + "reading_" + str(cnt) + ".PPM"))
            else:
                cnt = 0
                prev_label = preds[0]

    except KeyboardInterrupt:
        camera.shutdown()
        eye.draw_text("")
        zumi.stop()
        print("\nExiting...")
    except:
        camera.shutdown()
        eye.draw_text("")
        zumi.stop()
        print("\nExiting...")


def run():
    print("init run method")
    start = time.process_time()
    classification_model = generate_calssification_model(os.path.dirname(os.path.abspath(__file__)) + "/weight_drawing.hdf5")
    print("model load : " + str(time.process_time() - start))
    predict(classification_model)
    # print(land + " :  finish")


if __name__ == "__main__":
    run()
