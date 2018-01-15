import matplotlib.pyplot as plt
import skimage.io


figure = plt.figure()
axes = figure.add_subplot(111)
axes.axis('off')

im = skimage.io.imread('/tmp/cat/1d70f515194052f9771b8f09a8cc3b7e.jpg')

axes.imshow(im)

sca_x = []
sca_y = []
sca = axes.scatter(sca_x, sca_y, s=150, c='#FF0000')

def spot(event):
    sca_x.append(event.xdata)
    sca_y.append(event.ydata)
    sca.set_offsets(list(zip(sca_x, sca_y)))
    figure.canvas.draw()

figure.canvas.mpl_connect('button_press_event', spot)

plt.show()
