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

    def __init__(self, indv=None, transparentFactor=8):
        self.canvas = np.zeros((CanvasSize, CanvasSize, 3), dtype="uint8")
        self.countArray = np.zeros((CanvasSize, CanvasSize, 3), dtype="uint8")
        self.canvasFloat64 = np.zeros((CanvasSize, CanvasSize, 3), dtype="uint64")
        if indv is not None:
            for i, t in enumerate(indv.chromsome):
                self._addTriangle(t)
        self.update()

    def v(self):
        return self._v

    def save(self, path):
        cv2.imwrite(path, self.canvas)
        np.save("%s_countArray.npy" % path, self.countArray)
        np.save("%s_canvasFloat64.npy" % path, self.canvasFloat64)

    def load(self, path):
        self.countArray = np.load("%s_countArray.npy" % path)
        self.canvasFloat64 = np.load("%s_canvasFloat64.npy" % path)
        self.update()

    def _addTriangle(self, t):
        tmpCanvas = np.zeros((CanvasSize, CanvasSize, 3), dtype="uint8")
        v = np.array(t.vertex).reshape((-1,1,2))
        tmpCanvas = cv2.fillPoly(tmpCanvas, [v], t.color)
        self.countArray += (tmpCanvas > 0)
        self.canvasFloat64 += tmpCanvas

    def _removeTriangle(self, t):
        tmpCanvas = np.zeros((CanvasSize, CanvasSize, 3), dtype="uint8")
        v = np.array(t.vertex).reshape((-1,1,2))
        tmpCanvas = cv2.fillPoly(tmpCanvas, [v], t.color)
        self.countArray -= (tmpCanvas > 0)
        self.canvasFloat64 -= tmpCanvas

    def addTriangle(self, t):
        self._addTriangle(t)
        self.update()

    def removeTriangle(self, t):
        self._removeTriangle(t)
        self.update()

    def update(self):
        self.canvas = np.uint8(np.clip((self.canvasFloat64/(self.countArray+(self.countArray==0))), 0, 255))
        self.canvas += np.uint8((self.canvas == 0) * 255)
        self._v = _getV(self.canvas)

if __name__ == '__main__':
    from art_individual import *
    from datetime import datetime
    ChromLen = 10

    cv2.namedWindow("img", 1)
    print datetime.now()
    indv = ArtIndividual()
    ac = ArtCanvas(indv)
    print datetime.now()

    cv2.imshow("img", ac.canvas)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
