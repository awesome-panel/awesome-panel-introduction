import panel as pn
import numpy as np

from matplotlib.figure import Figure
from matplotlib import cm
from matplotlib.backends.backend_agg import FigureCanvas  # not needed for mpl >= 3.1
import matplotlib.pyplot as plt
from shared import Configuration

config=Configuration(random=True)
pn.extension("ace", sizing_mode="stretch_width")

# Define the Text

text="""# Works in your Notebook and IDE

One of the many super powers of Panel is that it works in your Notebook and IDE. I.e. it **supports
most use cases and work flows** for exploratory data analysis and data science apps.

For it to work in VS Code you will need to install the `jupyter_bokeh` package.
"""

# Define the Image Component

image_component = pn.layout.FlexBox(
    pn.pane.SVG("https://raw.githubusercontent.com/MarcSkovMadsen/awesome-panel-introduction/2b74c2dd1f996a8c8c229870bdd2b14035007ecb/assets/logos/jupyter-logo.svg", sizing_mode="fixed", height=200, margin=25),
    pn.pane.PNG("https://assets-global.website-files.com/5f1c75e63b2f950eb473d3e4/6074a3132bdc2e3119909dc1_6063796730397e49added231_google-colab-200x200.png", sizing_mode="fixed", height=200, margin=25),
    pn.pane.PNG("https://images.prismic.io/launchdarkly/ZWQ2YzRhNTItYzg4Ny00NjA0LWI0NzItZWI5Mzg5ZDc3NDIy_visualstudio_code-card.png", sizing_mode="fixed", height=200, margin=25),
    pn.pane.SVG("https://raw.githubusercontent.com/MarcSkovMadsen/awesome-panel-introduction/master/assets/logos/pycharm-logo.svg", sizing_mode="fixed", height=200, margin=25),
    justify_content  ="center", margin=25
)

# Define the Plot Component

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
get_plot_interactive=pn.bind(get_plot, cmap=select, theme=config.theme)

component=pn.Column(
    select,
    pn.panel(get_plot_interactive, sizing_mode="stretch_both", loading_indicator=True),
    sizing_mode="stretch_both", name="Example", margin=(20,5,10,5),
)

# Code Component

code="""\
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
"""

code_component=pn.Column(
    pn.widgets.Ace(value=code, theme=config.ace_theme, language="python", min_height=600, sizing_mode="stretch_both", disabled=True),
    sizing_mode="stretch_both", name="Code", margin=(20,5,10,5),
)

# Layout the App

pn.template.FastListTemplate(
    site=config.site,
    title="Works in your Notebook and IDE",
    header_accent_base_color=config.header_accent_base_color,
    header_background=config.header_background,
    header_color=config.header_color,
    accent_base_color=config.accent_base_color,
    sidebar_footer=config.menu,
    sidebar_width=400,
    main_max_width="80%",
    main=[text, image_component, pn.Tabs(component,code_component, sizing_mode="stretch_both")],
).servable()