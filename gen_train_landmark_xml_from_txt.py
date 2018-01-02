import os
import os.path

import lxml.etree


img_dir = '/tmp/cat'
img_result_dir = '/tmp/cat_result'
xml_save_to = 'train_landmark.xml'


def gen_data():
    for entry in os.scandir(img_result_dir):
        img_path = os.path.join(img_dir, entry.name[:-4])

        with open(entry.path) as f:
            content = f.read()

        points = []
        seps = content.split('|')
        for sep in seps:
            x, y = sep.split(',')
            x = int(float(x))
            y = int(float(y))
            points.append((x, y))

        yield (img_path, points)


dataset = lxml.etree.Element('dataset')
images = lxml.etree.SubElement(dataset, 'images')

for entry in gen_data():
    path = entry[0]
    points = entry[1]

    image = lxml.etree.SubElement(images, 'image', attrib={'file': path})

    top = min([p[1] for p in points])
    left = min([p[0] for p in points])
    width = max([p[0] for p in points]) - left
    height = max([p[1] for p in points]) - top

    box = lxml.etree.SubElement(image, 'box', attrib={
        'top': str(top),
        'left': str(left),
        'width': str(width),
        'height': str(height)
    })

    for i, point in enumerate(points):
        lxml.etree.SubElement(box, 'part', attrib={
            'name': '%02d' % i,
            'x': str(point[0]),
            'y': str(point[1]),
        })

tree = lxml.etree.ElementTree(dataset)
tree.write(xml_save_to, pretty_print=True, xml_declaration=True, encoding='utf-8')
