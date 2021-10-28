import holoviews as hv
import panel as pn

from components import indicators

from shared import Configuration

pn.extension(sizing_mode="stretch_width")
hv.extension("bokeh")

config = Configuration(
    title="Indicators",
    url="indicators",
    random=True,
)

description = """
# Indicators

Panel provides several [built in indicators]\
(https://panel.holoviz.org/reference/index.html#indicators). If that is not enough for example
Plotly provides additional indicators [here](https://plotly.com/javascript/indicator/).
"""

template = pn.template.FastGridTemplate(
    site=config.site,
    title=config.title,
    header_accent_base_color=config.header_accent_base_color,
    header_background=config.header_background,
    header_color=config.header_color,
    accent_base_color=config.accent_base_color,
    sidebar_footer=config.menu,
    sidebar_width=config.sidebar_width,
    main_max_width="95%",
    row_height=10
)

import numpy as np
import param
class Trend(indicators.ComponentBase):
    component = param.Parameter(pn.indicators.Trend)
    reference = param.String("https://panel.holoviz.org/reference/indicators/Trend.html#indicators-gallery-trend")
    imports = """\
import panel as pn
import numpy as np

pn.extension(sizing_mode="stretch_width")
"""

    def example(self, theme="default", accent_base_color="blue"):
        def get_widget(theme="default", accent_base_color="blue"):
            data = {'x': np.arange(50), 'y': np.random.randn(50).cumsum()}
            trend = pn.indicators.Trend(
                title='Price', data=data, plot_color=accent_base_color, sizing_mode="stretch_both",
                name="Trend",
            )
            return trend

        component=get_widget(theme=theme, accent_base_color=accent_base_color)
        return component

trend= Trend()
component =trend.example(accent_base_color=config.accent_base_color)
template.main[0:8,:]=pn.Row(description, config.get_logo_pane(width=100))
template.main[8:24,0:4]=component
template.main[8:24,4:8]=pn.Column(component.controls(), scrollable=True)
template.main[8:24,8:12]=pn.widgets.Ace(value=trend.code(), scrollable=True, sizing_mode="stretch_both")

if __name__.startswith("bokeh"):
    template.servable()