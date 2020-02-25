import sys

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
from scipy import stats

fig, ax = plt.subplots()
fig.set_tight_layout(True)
plt.xlim(0, 4)
plt.ylim(-2, 5)
ax.set_facecolor('black')  # background color of plot


def neuron_spike_fn(x: np.array) -> np.array:
    # TODO: replace gaussian with more accurate neuron spiking function
    return stats.norm.pdf(x, 10, 0.1) - stats.norm.pdf(x, 11, 1) + 0.2 * np.random.random(len(x))


# Query the figure's on-screen size and DPI.
# Note that when saving the figure to a file, we need to provide a DPI for that separately.
print('fig size: {0} DPI, size in inches {1}'.format(
    fig.get_dpi(), fig.get_size_inches()))

# Plot the initial line.
step_size = 0.005
x = np.arange(0, 3, step_size)
print(x.shape)
line_spike, = ax.plot(x, neuron_spike_fn(x), 'y-', linewidth=1)


def update(i):
    """
    :param i:
    :return: a tuple of "artists" that have to be redrawn for this frame.
    """
    label = 'timestep {0}'.format(i)
    print(label)

    # Update the line plot.
    line_spike.set_ydata(neuron_spike_fn(x + 0.5 * i))

    # Update the axes with a new xlabel.
    ax.set_xlabel(label)

    return line_spike, ax


if __name__ == '__main__':
    # You could use imagemagick, but you'll need to install it separately.
    # Matplotlib will otherwise use PillowWriter, which works fine.

    # FuncAnimation will call the 'update' function for each frame.
    n_frames = 30  # animating over this many frames
    interval_time = 20  # interval between frames, in milliseconds
    gif_file_name = 'neuron_spike_spiking.gif'

    anim = FuncAnimation(
        fig,
        update,
        frames=np.arange(0, n_frames),
        interval=interval_time
    )

    # Manual save option if you run this as a Python script.
    # sys.argv.append('save')
    print(sys.argv)

    if len(sys.argv) > 1 and sys.argv[1] == 'save':
        anim.save(
            gif_file_name,
            dpi=80,
            writer='imagemagick'
        )
    else:
        # plt.show() will just loop the animation forever.
        plt.show()
