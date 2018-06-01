import cv2
import numpy as np
from art_config import *

def _getV(img):
    res = cv2.resize(img, (VLen, VLen)).reshape(VLen*VLen*3)
    return res

class ArtPortrait(object):
    def __init__(self, path):
        img = cv2.imread(path)

        self._v = _getV(img)

    def v(self):
        return self._v

class ArtCanvas(object):

    def __init__(self, indv, transparentFactor=4):
        self.canvas = np.zeros((CanvasSize, CanvasSize, 3), dtype="uint8")
        canvasUint64 = np.zeros((CanvasSize, CanvasSize, 3), dtype="uint64")
        for i, t in enumerate(indv.chromsome):
            tmpCanvas = np.zeros((CanvasSize, CanvasSize, 3), dtype="uint8")
            v = np.array(t.vertex).reshape((-1,1,2))
            tmpCanvas = cv2.fillPoly(tmpCanvas, [v], t.color)
            canvasUint64 += tmpCanvas
        self.canvas = 255-np.uint8(np.clip(canvasUint64/transparentFactor, 0, 255))
        self._v = _getV(self.canvas)

    def v(self):
        return self._v

    def save(self, path):
        cv2.imwrite(path, self.canvas)


if __name__ == '__main__':
    from art_individual import *
    from datetime import datetime

    cv2.namedWindow("img", 1)
    print datetime.now()
    indv = ArtIndividual()
    ac = ArtCanvas(indv)
    print datetime.now()

    cv2.imshow("img", ac.canvas)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
