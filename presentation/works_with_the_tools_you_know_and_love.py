import panel as pn
import param

from shared import Configuration
import components
import inspect
import textwrap

RAW_CSS = """
.bk-root *.bk-btn {
    font-size: 18px;
    font-weight: bold;
}
"""

pn.extension("vega", "deckgl", "echarts", "ipywidgets", "plotly", sizing_mode="stretch_width")

config = Configuration(
    title="Works with the tools you know and love",
    url="works_with_the_tools_you_know_and_love",
    random=True,
)

altair = components.Altair()
bokeh = components.Bokeh()
deckgl = components.DeckGL()
echarts = components.ECharts()
holoviews = components.HoloViews()
hvplot = components.HVPlot()
matplotlib = components.Matplotlib()
plotly = components.Plotly()
plotnine = components.Plotnine()
pydeck = components.PyDeck()
pyecharts = components.PyECharts()
seaborn = components.Seaborn()
vega = components.Vega()

TOOLS = {
    "ALTAIR": altair,
    "BOKEH": bokeh,
    "DECKGL": deckgl,
    "ECHARTS": echarts,
    "HOLOVIEWS": holoviews,
    "HVPLOT": hvplot,
    # "ipywidget": # ipywidget,
    "MATPLOTLIB": matplotlib,
    "PLOTLY": plotly,
    "PLOTNINE": plotnine,
    "PYDECK": pydeck,
    "PYECHARTS": pyecharts,
    "SEABORN": seaborn,
    "VEGA": vega,
}

description = """
# Works with the tools you know and love

### To use Pythons Viz with Panel just wrap the python object into a `pn.panel`, a *layout* like `pn.Column` or a specific *pane* like `pn.pane.Matplotlib`
"""


def show(component="Altair"):
    component = TOOLS[component]
    return component.example(theme=config.theme, accent_base_color=config.accent_base_color)


def reference(component="Altair"):
    component = TOOLS[component]
    return f"[Reference Guide]({ component.reference })"


def code(component="Altair"):
    component = TOOLS[component]
    value = textwrap.dedent(inspect.getsource(component.example))
    # value += f"\n\n{component.component.name}"

    return pn.widgets.Ace(
        value=value,
        theme=config.ace_theme,
        language="python",
        min_height=400,
        sizing_mode="stretch_both",
        disabled=True,
    )


select = pn.widgets.RadioButtonGroup(
    options=list(TOOLS.keys()), button_type="success", margin=(10, 0, 25, 0)
)

pn.state.location.sync(select, {"value": "component"})

show = pn.bind(show, component=select)
reference = pn.bind(reference, component=select)
code = pn.bind(code, component=select)
component = pn.Column(
    select,
    pn.Tabs(
        pn.panel(show, sizing_mode="stretch_both", name="Component", margin=(25, 5, 0, 5)),
        pn.panel(code, name="Code", sizing_mode="stretch_both"),
        sizing_mode="stretch_both",
    ),
    pn.panel(reference),
    sizing_mode="stretch_both",
)

panel_logo = config.get_logo_pane(width=100)


template = pn.template.FastListTemplate(
    site=config.site,
    title=config.title,
    header_accent_base_color=config.header_accent_base_color,
    header_background=config.header_background,
    header_color=config.header_color,
    accent_base_color=config.accent_base_color,
    sidebar_footer=config.menu,
    sidebar_width=config.sidebar_width,
    main_max_width="95%",
    main=[pn.Row(description, panel_logo), component],
)
template.config.raw_css.append(RAW_CSS)
template.servable()
