from art_individual import *
from art_image import *
from art_config import *
from random import random
import cv2
import numpy as np
from datetime import datetime
from copy import deepcopy

ap = ArtPortrait("./firefox.png")
v2 = ap.v()
v2 = np.array(v2, dtype="float64")
#maxD2 = 256*256*VLen*VLen*3

indv = ArtIndividual()

def fitness(ac):
    v1 = ac.v()
    v1 = np.array(v1, dtype="float64")
    d2 = sum((v1 - v2)**2)
    return 100000000 / (d2+1)

cv2.namedWindow("img", 1)

g = 0
ac = ArtCanvas(indv)
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
        print "generation %s: fitness = %s, newfit=%s, %s" % (g, prev_fit, new_fit, datetime.now())
        cv2.imshow("img", new_ac.canvas)
        cv2.waitKey(1)
        #ac.save("./output/g%s_fit%s.jpg" % (g, prev_fit))
    g += 1


cv2.destroyAllWindows()
