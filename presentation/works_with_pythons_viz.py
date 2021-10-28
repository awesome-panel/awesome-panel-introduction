import holoviews as hv
import panel as pn

from components import pyviz
from components.explorer import get_component_explorer

from shared import Configuration

pn.extension("vega", "deckgl", "echarts", "plotly", "vtk", sizing_mode="stretch_width")
hv.extension("bokeh")

config = Configuration(
    title="Works with Pythons Viz",
    url="works_with_pythons_viz",
    random=True,
)

components = {k: v() for k,v in pyviz.ALL.items()}

description = """
# Works with Pythons Viz ❤️

### To use Pythons Viz with Panel just wrap the python object into a `pn.panel`, a *layout* like `pn.Column` or a specific *pane* like `pn.pane.Matplotlib`
"""

if __name__.startswith("bokeh"):
    get_component_explorer(config, description, components).servable()