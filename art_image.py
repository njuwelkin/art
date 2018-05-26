import cv2
import numpy as np
from math import pi, sin, cos
from art_config import *

class ArtPortrait(object):
    def __init__(self, path):
        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        assert(img.shape[0] == img.shape[1])
        self._v = cv2.resize(img, (VLen, VLen)).reshape(VLen*VLen)

    def v(self):
        return self._v

class ArtCanvas(object):
    Size = (EdgePerNode - 1) * 128
    R = Size/2
    Center = (R, R)
    Anchors = [(R-int(cos(i*2*pi/Nodes)*R), R+int(sin(i*2*pi/Nodes)*R)) for i in range(0, Nodes)]

    def __init__(self):
        self._canvas = np.ones((ArtCanvas.Size, ArtCanvas.Size), dtype="uint8") *255
        self._updated = False


    def line(self, idx1, idx2):
        Anchors = ArtCanvas.Anchors
        cv2.line(self._canvas, Anchors[idx1], Anchors[idx2], 0, 1)
        self._updated = True

    def v(self):
        if self._updated:
            self._v = cv2.resize(self._canvas, (VLen, VLen)).reshape(VLen*VLen)
        return self._v

    def save(self, path):
        cv2.imwrite(path, self._canvas)


if __name__ == '__main__':
    ac = ArtCanvas()
    for i in range (1, len(ArtCanvas.Anchors)):
        ac.line(0, i)

    cv2.namedWindow("img", 1)
    cv2.imshow("img", ac._canvas)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
