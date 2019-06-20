import numpy as np
import cv2
import copy


class Arrow:
    def __init__(self, up=0, down=0, left=0, right=0):
        self.up = up
        self.down = down
        self.left = left
        self.right = right


class Crop:
    X = 40
    Y = 37
    idx = 0
    offset = 0
    center_X = [X, X, X - 3, X - 3, X + 3, X + 3, X + 3, X, X - 3, X - 6, X - 6, X - 6, X + 6, X + 6, X + 6]
    center_Y = [Y, Y - 3, Y, Y - 3, Y, Y - 3, Y + 3, Y + 3, Y + 3, Y, Y - 3, Y + 3, Y, Y - 3, Y + 3]

    # up down left right order
    crop_pixel = Arrow()

    max_location = Arrow()
    idx = 0
    up = [0] * 74
    down = [0] * 74
    left = [0] * 74
    right = [0] * 74
    visit = [[0 for col in range(74)] for row in range(74)]

    labeled_image = 0
    threshhold_image = 0

    def zero(self):
        self.up = [0] * 74
        self.down = [0] * 74
        self.left = [0] * 74
        self.right = [0] * 74
        self.visit = [[0 for col in range(74)] for row in range(74)]

    def labeling(self, y, x):
        if y < self.crop_pixel.up:
            self.up[y] += 1
            self.max_location.up = y
            if self.up[y] > 12:
                self.crop_pixel.up = y

        if y > self.crop_pixel.down:
            self.down[y] += 1
            self.max_location.down = y
            if self.down[y] > 12:
                self.crop_pixel.down = y

        if x < self.crop_pixel.left:
            self.left[x] += 1
            self.max_location.left = x
            if self.left[x] > 12:
                self.crop_pixel.left = x

        if x > self.crop_pixel.right:
            self.right[x] += 1
            self.max_location.right = x
            if self.right[x] > 12:
                self.crop_pixel.right = x

        self.visit[y][x] = 1
        self.labeled_image[y, x] = np.array([255])  # RED

        direction = [-2, 0, 2]
        for j in range(3):
            for i in range(3):
                if self.threshhold_image[y + direction[j], x + direction[i]] != 0 and \
                        not self.visit[y + direction[j]][x + direction[i]]:
                    self.labeling(y + direction[j], x + direction[i])

    def crop(self, image, off=offset):
        self.zero()
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        image = cv2.copyMakeBorder(image, 5, 5, 5, 5, cv2.BORDER_CONSTANT, value=[0, 0, 0])
        self.labeled_image = copy.deepcopy(image)
        self.threshhold_image = cv2.threshold(image, 100, 255, cv2.THRESH_BINARY)[1]

        for i in range(len(self.center_X)):
            if self.threshhold_image[self.center_Y[i] - 1:self.center_Y[i] + 1,
               self.center_X[i] - 1:self.center_X[i] + 1].all():
                idx = i
                self.crop_pixel.up = self.center_Y[idx]
                self.crop_pixel.down = self.center_Y[idx]
                self.crop_pixel.left = self.center_X[idx]
                self.crop_pixel.right = self.center_X[idx]
                break

        try:
            if idx == len(self.center_X) - 1:
                print('fail')
                return None
        except:
            return None

        self.labeling(self.center_Y[idx], self.center_X[idx])
        height = self.crop_pixel.down - self.crop_pixel.up
        width = self.crop_pixel.right - self.crop_pixel.left
        size = height * width
        if size > 2100:
            return None
        if size < 300:
            return None
        print("size : " + str(size))
        # 2100 is max img cropped size:
        if height > width + 2:
            print("song")
            img_cropped = image[self.crop_pixel.up:self.crop_pixel.up + width,
                          self.crop_pixel.left:self.crop_pixel.right]
        else:
            img_cropped = image[self.crop_pixel.up-off:self.crop_pixel.down+off, self.crop_pixel.left-off:self.crop_pixel.right+off]

        img_result = cv2.resize(img_cropped, (64, 64), interpolation=cv2.INTER_CUBIC)
        img_result = cv2.cvtColor(img_result,cv2.COLOR_GRAY2BGR)
        # cv2.imshow("frame", img_result)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        return img_result
