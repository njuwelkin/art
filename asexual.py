from art_individual import *
from art_image import *
from art_config import *
from random import random
import cv2
import numpy as np
from datetime import datetime
from copy import deepcopy
import sys

if len(sys.argv) > 2:
    ap = ArtPortrait(sys.argv[1])
    ac = ArtCanvas()
    ac.load(sys.argv[2])
    indv = ArtIndividual()
else:
    if len(sys.argv) > 1:
        ap = ArtPortrait(sys.argv[1])
    else:
        ap = ArtPortrait("./firefox.png")
    indv = ArtIndividual()
    ac = ArtCanvas(indv)

v2 = ap.v()
v2 = np.array(v2, dtype="float64")
#maxD2 = 256*256*VLen*VLen*3


def fitness(ac):
    v1 = ac.v()
    v1 = np.array(v1, dtype="float64")
    d2 = sum((v1 - v2)**2)
    return 100000000 / (d2+1)

cv2.namedWindow("img", 1)

g = 0
prev_fit = fitness(ac)
while True:
    new_indv = indv.clone()
    new_ac = deepcopy(ac)
    idx = int(ChromLen*random())

    oldT = new_indv.chromsome[idx]
    new_ac._removeTriangle(oldT)

    new_indv.chromsome[idx] = Triangle(rand=True)
    new_ac.addTriangle(new_indv.chromsome[idx])
    new_fit = fitness(new_ac)

    if new_fit > prev_fit:
        prev_fit = new_fit
        indv = new_indv
        ac = new_ac

    if g % 10 == 0:
        cv2.imshow("img", new_ac.canvas)
        k = cv2.waitKey(1)
        if k == 13 or g % 10000 == 0:
            ac.save("./output/g%s.jpg" % g)
            np.save("./output/g%s.jpg_indv.npy" % g, indv.chromsome)
        if g % 100 == 0:
            print "generation %s: fitness = %s, newfit=%s, %s" % (g, prev_fit, new_fit, datetime.now())
    g += 1


cv2.destroyAllWindows()
