import sys

import dlib
import skimage.draw
import skimage.io

load_name = sys.argv[1]
save_name = sys.argv[2]

detector = dlib.simple_object_detector('detector.svm')
shape_predictor = dlib.shape_predictor('predictor.dat')

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

    shape = [(p.x, p.y) for p in shape_predictor(img, d).parts()]
    print('Part 0: {}, Part 1: {} ...'.format(shape[0], shape[1]))
    for i, pos in enumerate(shape):
        skimage.draw.set_color(img, skimage.draw.circle(pos[1], pos[0], 3), (255, 0, 0))

skimage.io.imsave(save_name, img)
