import math
import time

import Adafruit_SSD1306
import os
from PIL import Image, ImageFont, ImageDraw


class Screen:
    # Raspberry Pi pin configuration:
    RST = 24
    EYE_IMAGE_FOLDER_PATH = os.path.dirname(os.path.abspath(__file__))+'/images/'
    TEXT_FILE_PATH = os.path.dirname(os.path.abspath(__file__))+"/arial.ttf"
    EXCITED = {"excited1", "excited2", "excited3"}

    def __init__(self, clear=True):
        try:
            # 128x64 display with hardware I2C:
            self.disp = Adafruit_SSD1306.SSD1306_128_64(rst=self.RST)
            # Initialize library.
            self.disp.begin()
            self.width = self.disp.width
            self.height = self.disp.height
            self.screen_image = None
            # Clear display.
            if clear:
                self.disp.clear()
                self.disp.display()

        except:
            print("OLED screen is not connected")

    def clear_display(self):
        self.disp.clear()
        self.disp.display()

    def draw_text(self, string, x=1, y=1, display=0, image=0, font_size=16, clear=True):
        if display == 0:
            display = self.disp
        if image == 0:
            image = Image.new('1', (self.width, self.height))
        font = ImageFont.truetype(self.TEXT_FILE_PATH, font_size)
        draw = ImageDraw.Draw(image)
        max_x = 0
        max_y = 0
        if clear:
            draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)
        current_x = x
        current_y = y

        for char in string:
            char_width, char_height = draw.textsize(char, font=font)
            # print(char + ": height-" + str(char_height) + ", width-" + str(char_width))
            max_x = char_width if max_x < char_width else max_x
            max_y = char_height if max_y < char_height else max_y
            draw.text((current_x, current_y), char, font=font, fill=255)
            current_x += char_width
            if current_x > self.width - max_x:
                current_x = x
                current_y += max_y + 1
        display.image(image)
        display.display()

        self.screen_image = image

    def draw_text_center(self, string, display=0, image=0, font_size=16, clear=True):

        words = string.split(' ')
        split_lines = []
        text = ""
        current_h = font_size
        font = ImageFont.truetype(self.TEXT_FILE_PATH, font_size)

        if display == 0:
            display = self.disp

        if image == 0:
            image = Image.new('1', (self.width, self.height))

        draw = ImageDraw.Draw(image)

        if clear:
            draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)

        for word in words:
            new_line = False
            new_line_next_word = ""

            if "\n" in word:
                try:
                    word, new_line_next_word = word.split("\n")
                    new_line = True
                except:
                    print("You should use '\\n' only once in one word")
                    return

            text += word + " "
            text_width, text_height = draw.textsize(text, font=font)

            if word == words[0]:
                current_h = text_height

            if text_width >= 124:
                text = text[:-len(word)-2]
                split_lines.append(text)
                text = word + " "
                current_h += text_height

            if new_line:
                split_lines.append(text[:-1])
                current_h += text_height
                text = new_line_next_word + " "

            if current_h >= 60:
                print("Sentence is too long")
                return

        split_lines.append(text[:-1])

        print(split_lines)

        current_y = (self.height - 4 - current_h) / 2

        for text in split_lines:
            text_width, text_height = draw.textsize(text, font=font)
            current_x = (self.width - text_width) / 2
            draw.text((current_x, current_y), text, font=font, fill=255)
            current_y += text_height

        display.image(image)
        display.display()

        self.screen_image = image

    def path_to_image(self, path):
        return Image.open(path).convert('1')

    def draw_image(self, img, display=0):
        if display == 0:
            display = self.disp
        display.image(img)
        display.display()

    def draw_image_by_name(self, name):
        self.draw_image(self.path_to_image(self.EYE_IMAGE_FOLDER_PATH + name + ".ppm"))

    def animate(self, preset=None, custom=False):
        preset = self.EXCITED if preset is None else preset
        if not custom:
            for item in preset:
                self.draw_image(self.path_to_image(self.EYE_IMAGE_FOLDER_PATH + item + ".ppm"))
        else:
            for item in preset:
                self.draw_image(item)

    def calibrating(self):
        self.draw_image(self.path_to_image(self.EYE_IMAGE_FOLDER_PATH + "calibrating.ppm"))

    def calibrated(self):
        self.draw_image(self.path_to_image(self.EYE_IMAGE_FOLDER_PATH + "calibrated.ppm"))

    def close_eyes(self):
        self.draw_image(self.path_to_image(self.EYE_IMAGE_FOLDER_PATH + "close.ppm"))

    def sleepy_eyes(self):
        self.draw_image(self.path_to_image(self.EYE_IMAGE_FOLDER_PATH + "sleep.ppm"))

    def sleepy_left(self):
        self.draw_image(self.path_to_image(self.EYE_IMAGE_FOLDER_PATH + "sleepyleft1.ppm"))

    def sleepy_right(self):
        self.draw_image(self.path_to_image(self.EYE_IMAGE_FOLDER_PATH + "sleepyright1.ppm"))

    def blink(self):
        self.draw_image(self.path_to_image(self.EYE_IMAGE_FOLDER_PATH + "neutral2.ppm"))
        time.sleep(.25)
        self.draw_image(self.path_to_image(self.EYE_IMAGE_FOLDER_PATH + "close.ppm"))
        time.sleep(.25)
        self.draw_image(self.path_to_image(self.EYE_IMAGE_FOLDER_PATH + "neutral1.ppm"))


    def look_around_open01(self):
        self.draw_image_by_name("lookright1")
        time.sleep(.7)
        self.close_eyes()
        self.draw_image_by_name("lookleft1")

    def look_around_open02(self):
        time.sleep(.7)
        self.close_eyes()
        self.draw_image_by_name("lookright1")

    def look_around_open03(self):
        time.sleep(.7)
        self.close_eyes()

    def look_around_open04(self):
        self.hello()
        time.sleep(1)

    def sleeping(self):
        self.draw_image_by_name("close")
        time.sleep(.6)
        self.draw_image_by_name("sleep_z1")
        time.sleep(.6)
        self.draw_image_by_name("sleep_z2")
        time.sleep(.6)
        self.draw_image_by_name("sleep_z3")
        time.sleep(.6)
        self.draw_image_by_name("close")
        time.sleep(.6)

    def look_around(self):
        self.sleepy_eyes()
        time.sleep(2)
        self.close_eyes()
        self.sleepy_left()
        time.sleep(1)
        self.close_eyes()
        self.sleepy_right()
        time.sleep(1)
        self.close_eyes()
        self.sleepy_eyes()
        time.sleep(1)

    def glimmer(self):
        glimmer = ["neutral1", "neutral2", "neutral3"]
        self.animate(glimmer)

    def sad(self):
        sad = ["sad1"]
        #sad = ["sad1", "sad2", "sad3"]
        self.animate(sad)

    def happy(self):
        happy = ["neutral1", "neutral2"]
        wink = ["happy_left2", "happy_right1"]
        self.animate(happy)
        for i in range(3):
            self.animate(wink)
        self.hello()

    def hello(self):
        self.draw_image(self.path_to_image(self.EYE_IMAGE_FOLDER_PATH + "neutral1.ppm"))

    def angry(self):
        self.draw_image(self.path_to_image(self.EYE_IMAGE_FOLDER_PATH + "focus.ppm"))

    def connection_success(self):
        self.draw_image_by_name("connected")

    def connection_fail(self):
        self.draw_image_by_name("onlinefail")

