import holoviews as hv
import panel as pn

import components
from shared import Configuration

RAW_CSS = """
.bk-root *.bk-btn {
    font-size: 16px;
    font-weight: bold;
}
"""

pn.extension("vega", "deckgl", "echarts", "plotly", "vtk", sizing_mode="stretch_width")
hv.extension("bokeh")

config = Configuration(
    title="Works with the tools you know and love",
    url="works_with_the_tools_you_know_and_love",
    random=True,
)

PLOTS = {
    "ALTAIR": components.Altair(),
    "BOKEH": components.Bokeh(),
    "DATASHADER": components.DeckGL(),
    "DECKGL": components.Datashader(),
    "ECHARTS": components.ECharts(),
    "FOLIUM": components.Folium(),
    "HOLOVIEWS": components.HoloViews(),
    "HVPLOT": components.HVPlot(),
    "MATPLOTLIB": components.Matplotlib(),
    "PLOTLY": components.Plotly(),
    "PLOTNINE": components.Plotnine(),
    "PYDECK": components.PyDeck(),
    "PYECHARTS": components.PyECharts(),
    "PYVISTA": components.PyVista(),
    "SEABORN": components.Seaborn(),
    "VEGA": components.Vega(),
    "VTK": components.VTK(),
}

description = """
# Works with the tools you know and love

### To use Pythons Viz with Panel just wrap the python object into a `pn.panel`, a *layout* like `pn.Column` or a specific *pane* like `pn.pane.Matplotlib`
"""


def show(component="Altair"):
    component = PLOTS[component]
    return component.example(theme=config.theme, accent_base_color=config.accent_base_color)


def reference(component="Altair"):
    component = PLOTS[component]
    return f"[Reference Guide]({ component.reference })"


def code(component="Altair"):
    component = PLOTS[component]
    value = component.code(accent_base_color=config.accent_base_color)

    return pn.widgets.Ace(
        value=value,
        theme=config.ace_theme,
        language="python",
        min_height=400,
        sizing_mode="stretch_both",
        disabled=True,
    )


select = pn.widgets.RadioButtonGroup(
    options=list(PLOTS.keys()), button_type="success", margin=(10, 0, 25, 0)
)
try:
    pn.state.location.sync(select, {"value": "component"})
except:
    pass

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
