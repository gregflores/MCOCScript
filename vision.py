import cv2
from mss import mss
from PIL import Image
import numpy as np
import time


class Vision:
    def __init__(self):
        self.static_templates = {
            'help-button': r'images\help-button.png',
            'empty-slot-bottom': r'images\empty-slot-bottom.png',
            'accept': r'images\accept.png',
            'continue': r'images\continue.png',
            'end-match': r'images\end-match.png',
            'final-fight': r'images\final-fight.png',
            'find-match': r'images\find-match.png',
            'next-fight': r'images\next-fight.png',
            'next-series': r'images\next-series.png',
            'pause': r'images\pause.png',
            'exit': r'images\exit.png',
            'find-match-free': r'images\find-match-free.png',
            'find-match-2000': r'images\find-match-2000.png',
            'info': r'images\info.png',
            'memu-logo': r'images\memu_logo.png'
        }

        self.templates = {k: cv2.imread(v, 0) for (k, v) in self.static_templates.items()}
        self.monitor = {'top': 0, 'left': 0, 'width': 1280, 'height': 880}
        self.screen = mss()

        self.frame = None

    def take_screenshot(self):
        sct_img = self.screen.grab(self.monitor)
        img = Image.frombytes('RGB', sct_img.size, sct_img.rgb)
        img = np.array(img)
        img = self.convert_rgb_to_bgr(img)
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return img_gray

    def get_image(self, path):
        return cv2.imread(path, 0)

    def bgr_to_rgb(self, img):
        b, g, r = cv2.split(img)
        return cv2.merge([r, g, b])

    def convert_rgb_to_bgr(self, img):
        return img[:, :, ::-1]

    def match_template(self, img_grayscale, template, threshold=0.9):
        """
        Matches template image in a target grayscaled image
        """

        res = cv2.matchTemplate(img_grayscale, template, cv2.TM_CCOEFF_NORMED)
        # print(res)
        matches = np.where(res >= threshold)
        # print(matches)
        if not matches[0].size:
            # self.log('no match')
            return False
        else:
            # self.log("match found")
            return True

    def match_template_center(self, img_grayscale, template, threshold=0.9):
        """
        Matches template image in a target grayscaled image
        """
        w, h = template.shape[::-1]
        res = cv2.matchTemplate(img_grayscale, template, cv2.TM_CCOEFF_NORMED)
        # print(res)
        matches = np.where(res >= threshold)
        coord = []
        if not matches[0].size:
            return coord
        else:
            x = matches[1][0] + w / 2
            y = matches[0][0] + h / 2
            coord = [x, y]
            return coord

    def find_template(self, name, image=None, threshold=0.9):
        if image is None:
            if self.frame is None:
                self.refresh_frame()

            image = self.frame

        return self.match_template(
            image,
            self.templates[name],
            threshold
        )

    def find_template_center(self, name, image=None, threshold=0.9):
        if image is None:
            if self.frame is None:
                self.refresh_frame()

            image = self.frame

        return self.match_template_center(
            image,
            self.templates[name],
            threshold
        )

    def refresh_frame(self):
        self.frame = self.take_screenshot()

    def log(self, text):
        print('[%s] %s' % (time.strftime('%H:%M:%S'), text))
