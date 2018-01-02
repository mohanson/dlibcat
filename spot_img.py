import os
import os.path

import matplotlib.pyplot as plt
import matplotlib.widgets
import skimage.io

plt.style.use('seaborn')


class SpotImg:

    nb_spots = 13

    def __init__(self, img_dir, result_dir):
        self.img_dir = img_dir
        self.result_dir = result_dir

        self.imgs = [os.path.join(img_dir, i) for i in os.listdir(img_dir)]
        self.i = 0

        self.fig = plt.figure()
        self.ax_img = self.fig.add_subplot(111)
        self.ax_img.axis('off')

        self.sca_xdata = []
        self.sca_ydata = []
        self.sca = self.ax_img.scatter(self.sca_xdata, self.sca_ydata, s=50, c='#FF0000', alpha=0.5)
        self.fig.canvas.mpl_connect('button_press_event', self.spot)

        self.ax_progress = self.fig.add_axes([0.9, 0.075 * 2, 0.1, 0.075])
        self.ax_progress.axis('off')
        self.progress = self.ax_progress.text(0, 0, '%s/%s' % (self.i, len(self.imgs)))

        self.ax_btn_prev = self.fig.add_axes([0.9, 0.075 * 1, 0.1, 0.075])
        self.btn_prev = matplotlib.widgets.Button(self.ax_btn_prev, 'Prev')
        self.btn_prev.on_clicked(self.prev)

        self.ax_btn_next = self.fig.add_axes([0.9, 0, 0.1, 0.075])
        self.btn_next = matplotlib.widgets.Button(self.ax_btn_next, 'Next')
        self.btn_next.on_clicked(self.next)

        self.load()

    def load(self):
        img = skimage.io.imread(self.imgs[self.i])
        self.ax_img.imshow(img)
        self.progress.set_text('%s/%s' % (self.i + 1, len(self.imgs)))

        self.sca_xdata = []
        self.sca_ydata = []

        name = os.path.basename(self.imgs[self.i])
        try:
            with open(os.path.join(self.result_dir, name + '.txt')) as f:
                result = f.read()
            for xy in result.split('|'):
                x, y = xy.split(',')
                x = float(x)
                y = float(y)
                self.sca_xdata.append(x)
                self.sca_ydata.append(y)
        except FileNotFoundError:
            pass
        self.sca.set_offsets(list(zip(self.sca_xdata, self.sca_ydata)))
        self.fig.canvas.draw()

    def dump(self, event=None):
        print(self.sca_xdata, self.sca_ydata)
        name = os.path.basename(self.imgs[self.i])
        with open(os.path.join(self.result_dir, name + '.data'), 'w') as f:
            content = '|'.join(['%s,%s' % (x, y) for x, y in zip(self.sca_xdata, self.sca_ydata)])
            f.write(content)

    def spot(self, event):
        if event.inaxes != self.ax_img:
            return
        if len(self.sca_xdata) >= self.nb_spots:
            return
        self.sca_xdata.append(event.xdata)
        self.sca_ydata.append(event.ydata)
        self.sca.set_offsets(list(zip(self.sca_xdata, self.sca_ydata)))
        self.fig.canvas.draw()

        if len(self.sca_xdata) == self.nb_spots:
            self.dump()
            self.next()

    def prev(self, event=None):
        if self.i <= 0:
            return
        self.i -= 1
        self.load()

    def next(self, event=None):
        if self.i == len(self.imgs):
            return
        self.i += 1
        self.load()


img_dir = '/tmp/cat'
result_dir = '/tmp/cat_result'
fig = SpotImg(img_dir, result_dir)
plt.show()
