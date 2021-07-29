import panel as pn
import numpy as np

from matplotlib.figure import Figure
from matplotlib import cm
from matplotlib.backends.backend_agg import FigureCanvas  # not needed for mpl >= 3.1
import matplotlib.pyplot as plt

pn.extension(sizing_mode="stretch_width")

COLOR_MAPS = {
    "Autumn": cm.autumn,
    'Spring': cm.spring,
    'Summer': cm.summer,
    'Winter': cm.winter,
}

def get_plot(cmap="autumn", theme="default"):
    plt.style.use("default")
    if theme=="dark":
        plt.style.use("dark_background")
    Y, X = np.mgrid[-3:3:100j, -3:3:100j]
    U = -1 - X**2 + Y
    V = 1 + X - Y**2
    speed = np.sqrt(U*U + V*V)

    fig0 = Figure(figsize=(12, 6))
    ax0 = fig0.subplots()
    FigureCanvas(fig0)  # not needed for mpl >= 3.1

    strm = ax0.streamplot(X, Y, U, V, color=U, linewidth=2, cmap=COLOR_MAPS[cmap])
    fig0.colorbar(strm.lines)

    return fig0


select = pn.widgets.Select(name="Color Map", options=list(COLOR_MAPS.keys()))
get_plot_interactive=pn.bind(get_plot, cmap=select, theme="default")

component=pn.Column(
    "# Example",
    select,
    pn.panel(get_plot_interactive, sizing_mode="stretch_both", loading_indicator=True),
    sizing_mode="stretch_both"
)