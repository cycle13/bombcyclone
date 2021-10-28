"""
Name: mymatlib.py

matplotlib my favorite plot settings.

Usage: This is the module.

Author: Ryosuke Tomita
Date: 2021/08/25
"""
import sys
from os.path import dirname
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
sys.path.append(dirname(__file__))
from fontjp import fontjp


class PltSet:
    def __init__(self):
        self.fig = plt.figure(figsize=(15, 6))
        self.ax = self.fig.add_subplot(111)
        self.plt = plt
        self.linestyle = ["solid", "dashed", "dashdot", "dotted"]
        self.plotcolor = ["b", "g", "r", "m"]
        self.cnt = 0
        self.legend_bar = []
        self.legend_label = []

        self.plt.rcParams['font.family'] = 'Times New Roman'
        self.plt.rcParams['mathtext.fontset'] = 'stix'
        self.plt.rcParams["font.size"] = 15
        self.plt.rcParams['xtick.labelsize'] = 35
        self.plt.rcParams['ytick.labelsize'] = 24
        plt.rcParams['xtick.direction'] = 'in'  # x軸の向きを内側に設定
        self.plt.rcParams['ytick.direction'] = 'in'
        self.plt.rcParams['axes.linewidth'] = 1.0
        self.plt.rcParams['axes.grid'] = False
        self.plt.rcParams["legend.borderaxespad"] = 0.  # 凡例の箱をの位置をグラフに合わせて左に寄せる
        self.plt.rcParams["legend.fancybox"] = False  # 丸角
        self.plt.rcParams["legend.framealpha"] = 1  # 透明度の指定、0で塗りつぶしなし
        self.plt.rcParams["legend.edgecolor"] = 'gray'  # edgeの色を変更
        self.plt.rcParams["legend.handlelength"] = 1  # 凡例の線の長さを調節
        self.plt.rcParams["legend.handletextpad"] = 2.  # 凡例の線と凡例のアイコンの距離
        self.plt.rcParams["legend.markerscale"] = 1
        self.plt.rcParams['figure.dpi'] = 300  # 画質

    def plot(self, x, y, xlabel, ylabel, xisDate=False, newYaxis=False):
        if xisDate:
            new_xticks = list(range(len(x)))
            self.ax.xaxis.set_major_locator(ticker.FixedLocator(new_xticks))
            self.ax.xaxis.set_ticklabels(x)
            self.plt.xticks(rotation=90)

        if newYaxis and self.cnt > 0:
            self.ax2 = self.ax.twinx()
            self.ax2.plot(x, y,
                          marker='.',
                          markersize=10,
                          markeredgewidth=1.,
                          markeredgecolor="k",
                          label=ylabel,
                          color=self.plotcolor[self.cnt],
                          linestyle=self.linestyle[self.cnt],)
            self.ax2.set_xlabel(xlabel, fontsize=10,)
            self.ax2.set_ylabel(ylabel, fontsize=15,)

            bar, label = self.ax2.get_legend_handles_labels()

        else:
            self.ax.plot(x, y,
                         marker='.',
                         markersize=10,
                         markeredgewidth=1.,
                         markeredgecolor="k",
                         label=ylabel,
                         color=self.plotcolor[self.cnt],
                         linestyle=self.linestyle[self.cnt],)
            self.ax.set_xlabel(xlabel, fontsize=10,)
            self.ax.set_ylabel(ylabel, fontsize=15,)
            self.plt.yticks(fontsize=18)

            bar, label = self.ax.get_legend_handles_labels()
        # grid setting
        self.ax.xaxis.grid(True, which="major",
                           linestyle='-', color='#CFCFCF')
        self.ax.yaxis.grid(True, which="major",
                           linestyle='-', color='#CFCFCF')

        self.legend_bar += bar
        self.legend_label += label
        self.cnt += 1

    def save_fig(self, fig_name):
        self.legend_bar = list(dict.fromkeys(self.legend_bar))
        self.legend_label = list(dict.fromkeys(self.legend_label))
        self.ax.legend(self.legend_bar, self.legend_label,
                       loc='upper left', borderaxespad=0, bbox_to_anchor=(1.05, 1))
        self.fig.savefig(fig_name, bbox_inches="tight", pad_inches=0.5)
