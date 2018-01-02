import sys

import dlib
import skimage.draw
import skimage.io

load_name = sys.argv[1]
save_name = sys.argv[2]

detector = dlib.simple_object_detector('detector.svm')

img = skimage.io.imread(load_name)
dets = detector(img, 1)
print('Number of faces detected: {}'.format(len(dets)))
for d in dets:
    r0, c0, r1, c1 = d.top(), d.left(), d.bottom(), d.right()
    print('Detection {}'.format([(r0, c0), (r1, c1)]))
    skimage.draw.set_color(img, skimage.draw.line(r0, c0, r0, c1), (255, 0, 0))
    skimage.draw.set_color(img, skimage.draw.line(r0, c1, r1, c1), (255, 0, 0))
    skimage.draw.set_color(img, skimage.draw.line(r1, c1, r1, c0), (255, 0, 0))
    skimage.draw.set_color(img, skimage.draw.line(r1, c0, r0, c0), (255, 0, 0))

skimage.io.imsave(save_name, img)
