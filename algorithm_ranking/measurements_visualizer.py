import matplotlib.pyplot as plt
from matplotlib import gridspec
from matplotlib.ticker import FormatStrFormatter
import numpy as np

class MeasurementsVisualizer:
    def __init__(self, alg_measurements, alg_seq_h0=None):
        self.measurements = alg_measurements
        self.alg_seq_h0 = alg_seq_h0
        if not alg_seq_h0:
            self.alg_seq_h0 = list(self.measurements.keys())

    def remove_outliers(self,x):
        x = np.array(x)
        q1, q2 = np.percentile(x, [25, 75])
        iqr = q2 - q1
        fence_low = q1 - 1.5 * iqr
        fence_high = q2 + 1.5 * iqr
        return list(x[(x > fence_low) & (x < fence_high)])

    def show_measurement_histograms(self, alg_list=None, bins=10, hspace=0.5):
        if not alg_list:
            alg_list = self.alg_seq_h0
        alg_list.sort()

        n = len(alg_list)
        fig = plt.figure(figsize=(7, 3 * n))
        gs = gridspec.GridSpec(n, 1, height_ratios=[1] * n)

        ax = [None] * n
        for i in range(n):
            if i != 0:
                ax[i] = plt.subplot(gs[i], sharex=ax[0])
            else:
                ax[i] = plt.subplot(gs[i])
            ax[i].set_title(alg_list[i])
            ax[i].hist(self.measurements[alg_list[i]], bins=bins)
            ax[i].xaxis.set_major_formatter(FormatStrFormatter('%.e'))

        plt.subplots_adjust(hspace=hspace)
        plt.show()

    def show_measurements_boxplots(self, alg_list=None, outliers=False, scale=1.5):
        if not alg_list:
            alg_list = self.alg_seq_h0
        # alg_list.sort()

        x = []
        y = []
        for alg in alg_list:
            x.append(self.measurements[alg])
            y.append(alg)

        fig = plt.figure(figsize=(10, scale*len(alg_list)))
        ax = fig.add_subplot(111)

        # # Creating axes instance
        bp = ax.boxplot(x, patch_artist=True,
                        notch=False, vert=0, showfliers=outliers,
                        positions=range(len(y)))

        x_lim = ax.get_xlim()

        try:
            sp = ax.plot(x, y, 'b.', alpha=0.9)
            ax.set_xlim(x_lim)
        except:
            pass

        colors = ['#E1E8E8'] * len(y)

        for patch, color in zip(bp['boxes'], colors):
            patch.set_facecolor(color)

        # changing color and linewidth of
        # whiskers
        for whisker in bp['whiskers']:
            whisker.set(color='#8B008B',
                        linewidth=1.5,
                        linestyle=":")

        # changing color and linewidth of
        # caps
        for cap in bp['caps']:
            cap.set(color='#8B008B',
                    linewidth=2)

        # changing color and linewidth of
        # medians
        for median in bp['medians']:
            median.set(color='red',
                       linewidth=2)

        # y-axis labels
        ax.set_yticklabels(y)

        # Removing top axes and right axes
        # ticks
        ax.get_xaxis().tick_bottom()
        ax.get_yaxis().tick_left()

        plt.show()

    def show_measurements_violinplot(self, alg_list=None, outliers=False, scale=1.5):
        if not alg_list:
            alg_list = self.alg_seq_h0

        fig = plt.figure(figsize=(10, scale * len(alg_list)))
        ax = fig.add_subplot(111)

        x_b = []
        x_v = []
        y = []
        for alg in alg_list:
            data = self.remove_outliers(self.measurements[alg])
            x_v.append(data)
            x_b.append(self.measurements[alg])
            y.append(alg)

        # print(x)

        bp = ax.boxplot(x_b, patch_artist=True,
                        notch=False, vert=0, showfliers=outliers,
                        positions=range(len(y)))

        # # Creating axes instance
        vp = ax.violinplot(x_v, showmedians=False, vert=False, showextrema=False,
                           positions=range(len(y)))

        x_lim = ax.get_xlim()

        for i, data in enumerate(x_b):
            sp = ax.plot(data, np.ones(len(data)) * i, 'b.', alpha=0.9)
            ax.set_xlim(x_lim)

        colors = [(0.0, 0.0, 1.0, 0.05)] * len(y)
        edge_color = '#9FBCF5'

        for patch, color in zip(bp['boxes'], colors):
            plt.setp(patch, color=edge_color)
            patch.set_facecolor(color)

        # changing color and linewidth of
        # whiskers
        for whisker in bp['whiskers']:
            whisker.set(color='#8B008B',
                        linewidth=1.5,
                        linestyle=":")

        # changing color and linewidth of
        # caps
        for cap in bp['caps']:
            cap.set(color='#8B008B',
                    linewidth=2)

        # changing color and linewidth of
        # medians
        for median in bp['medians']:
            median.set(color='red',
                       linewidth=2)

        ax.set_yticks(range(len(y)), labels=y)

        # Removing top axes and right axes
        # ticks
        ax.get_xaxis().tick_bottom()
        ax.get_yaxis().tick_left()
        ax.set_xlabel('time (s)')

        plt.show()
        return fig



