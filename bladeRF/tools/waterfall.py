import numpy
import matplotlib.pyplot
import matplotlib.animation

HEIGHT = 500
WIDTH = 1024

fig = matplotlib.pyplot.figure()
im_data = numpy.zeros((HEIGHT, WIDTH), dtype=numpy.float32)
im = matplotlib.pyplot.imshow(im_data, cmap=matplotlib.pyplot.get_cmap('gray'))
im.set_clim(0.0, 1.0)

data = numpy.zeros(FFTPOINTS, dtype=numpy.float32)

def init_image():
    im.set_array(numpy.zeros((HEIGHT, WIDTH), dtype=numpy.float32))
    return (im,)

def update_image(i):

    data[:] = numpy.fromstring(
        sys.stdin.read(8192),
        dtype=numpy.complex64,
        )

    fft = numpy.fft.rfft(data)
    line = numpy.sqrt(numpy.real(fft)**2+numpy.imag(fft)**2)
    im_data[:,:WIDTH-1] = im_data[:,1:]
    im_data[:,WIDTH-1] = line
    im.set_array(im_data)
    return (im,)


ani = matplotlib.animation.FuncAnimation(
    fig, update_image, init_func=init_image,
    interval=0, blit=True)

matplotlib.pyplot.show()
