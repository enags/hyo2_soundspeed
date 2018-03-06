import numpy as np
import matplotlib

matplotlib.use('Qt4Agg')
matplotlib.rcParams['backend.qt4'] = 'PySide'

from matplotlib import rc_context as rc_context
from matplotlib import pyplot as plt
import logging

logger = logging.getLogger(__name__)


class TracedProfilePlot:

    def __init__(self):
        self.old_ssp = None
        self.old_ssp_label = None
        self.old_ssp_color = "#FF8000"

        self.new_ssp = None
        self.new_ssp_label = None
        self.new_ssp_color = "#3399FF"

        self.legend_loc = None
        self.legend_color = '#f5f5f5'

        self.old_z = None
        self.new_z = None
        self.max_tolerance = None

        self.new_outer_raypath = list()
        self.old_outer_raypath = list()

        self._extend = False

    def make_plots(self):

        self._extend = False
        if self.new_ssp.data[0][-1] > self.old_ssp.data[0][-1]:
            self._extend = True

        step = 0
        if self._extend:

            step = len(self.new_ssp.rays[-1][2])

        else:

            step = min(len(self.old_ssp.rays[-1][2]), len(self.new_ssp.rays[-1][2]))

        self.new_outer_raypath = [
            self.new_ssp.rays[-1][1][0:step],
            self.new_ssp.rays[-1][2][0:step]
        ]
        self.old_outer_raypath = [
            self.old_ssp.rays[-1][1][0:step],
            self.old_ssp.rays[-1][2][0:step]
        ]
        if self._extend:

            self.old_outer_raypath = [
                np.append(self.old_outer_raypath[0], self.old_ssp.rays[-1][1][step - 1]),
                np.append(self.old_outer_raypath[1], self.old_ssp.rays[-1][2][step - 1])
            ]

        # take care of labels and legend validity/inputs
        if not isinstance(self.old_ssp_label, str):
            self.old_ssp_label = None
        if not isinstance(self.new_ssp_label, str):
            self.new_ssp_label = None
        if not isinstance(self.legend_loc, str):
            self.legend_loc = None

        if self.old_ssp_label is None:
            self.old_ssp_label = "%s" % self.old_ssp.date_time
        if self.new_ssp_label is None:
            self.new_ssp_label = "%s" % self.new_ssp.date_time
        if self.legend_loc is None:
            self.legend_loc = "upper right"

        # calculate limits
        z_max = max(max(self.new_ssp.rays[len(self.new_ssp.rays) - 1][2]),
                    max(self.old_ssp.rays[len(self.old_ssp.rays) - 1][2]))
        x_max = max(max(self.new_ssp.rays[len(self.new_ssp.rays) - 1][1]),
                    max(self.old_ssp.rays[len(self.old_ssp.rays) - 1][1]))
        ss_min = min(min(self.new_ssp.data[1]), min(self.old_ssp.data[1]))
        ss_max = max(max(self.new_ssp.data[1]), max(self.old_ssp.data[1]))

        logger.debug("Plotting analysis")

        # create figure
        fig = plt.figure(num="Comparison of Ray-Traced Profiles",
                         figsize=(10, 6), dpi=80, facecolor='w', edgecolor='k')

        # profile comparison axis
        svp_ax = fig.add_subplot(1, 2, 1)
        svp_ax.set_title('Sound Speed Profiles')
        svp_ax.set_xlabel('Sound Speed [m/s]')
        svp_ax.set_ylabel('Depth [m]')
        svp_ax.set_ylim((z_max + .05 * z_max, 0))
        svp_ax.set_xlim((ss_min - 3.0, ss_max + 3.0))
        svp_ax.plot(self.old_ssp.data[1],
                    self.old_ssp.data[0],
                    color=self.old_ssp_color, linestyle='--', label=self.old_ssp_label)
        svp_ax.plot(self.new_ssp.data[1],
                    self.new_ssp.data[0],
                    color=self.new_ssp_color, linestyle=':', label=self.new_ssp_label)
        if self.old_ssp.data[0][-1] < self.new_ssp.data[0][-1]:
            svp_ax.plot(np.repeat(self.old_ssp.data[1][-1], 2),
                        [self.old_ssp.data[0][-1],
                         self.new_ssp.data[0][-1]],
                        'r--')

        # error plot axis
        err_ax = fig.add_subplot(1, 2, 2)
        err_ax.set_title('Ray-Tracing Comparison')
        err_ax.set_xlabel('Range [m]')
        err_ax.set_ylabel('Depth [m]')
        err_ax.set_ylim((z_max + .05 * z_max, 0))
        err_ax.set_xlim((0, x_max + 0.05 * x_max))
        err_ax.plot(self.old_outer_raypath[0],
                    self.old_outer_raypath[1], color=self.old_ssp_color,
                    linestyle='--')
        err_ax.plot(self.new_outer_raypath[0],
                    self.new_outer_raypath[1], color=self.new_ssp_color,
                    linestyle=':')
        if self.old_z is not None:
            err_ax.plot(self.old_z[0],
                        self.old_z[1], color=self.old_ssp_color, linestyle='--', label=self.old_ssp_label)
        if self.new_z is not None:
            err_ax.plot(self.new_z[0],
                        self.new_z[1], color=self.new_ssp_color, linestyle=':', label=self.new_ssp_label)
        if (self.new_z is not None) and (self.max_tolerance is not None):
            err_ax.plot(self.new_z[0], self.max_tolerance[0], 'm', label="error tolerance")
            err_ax.plot(self.new_z[0], self.max_tolerance[1], 'm')
        if (self.new_z is not None) or (self.old_z is not None):
            legend = err_ax.legend(loc=self.legend_loc, shadow=True, fontsize='small')
            legend.get_frame().set_facecolor(self.legend_color)

        fig.tight_layout()
        plt.show()
