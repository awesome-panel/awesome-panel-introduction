import panel as pn
import param
from .base import ComponentBase
import numpy as np

class Trend(ComponentBase):
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
                title='Price', data=data, plot_color=accent_base_color, sizing_mode="stretch_width", height=500
            )
            return "Hello"

        # trend = get_widget(theme=theme, accent_base_color=accent_base_color)
        # component = pn.Column(
        #     trend,
        #     sizing_mode="stretch_both",
        # )
        component=get_widget(theme=theme, accent_base_color=accent_base_color)
        return component