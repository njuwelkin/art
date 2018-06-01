from art_individual import *
from art_image import *
ac=ArtCanvas()
def draw(ac):
    cv2.imshow("img", ac.canvas)
    cv2.waitKey(50)

cv2.namedWindow("img", 1)
draw(ac)
for i in range(0, 100):
    ac.addTriangle(Triangle(rand=True))


for i in range(0, 200):
    t = Triangle(rand=True)
    ac.addTriangle(t)
    draw(ac)
    ac._removeTriangle(t)
    draw(ac)

cv2.destroyAllWindows()
