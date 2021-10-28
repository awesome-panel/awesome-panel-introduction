import holoviews as hv
import panel as pn

from components import holoviz
from components.explorer import get_component_explorer

from shared import Configuration

pn.extension(sizing_mode="stretch_width")
hv.extension("bokeh")

config = Configuration(
    title="Works with HoloViz",
    url="works_with_holoviz",
    random=True,
)

components = {k: v() for k,v in holoviz.ALL.items()}

description = """
# Works with HoloViz ❤️

### [HoloViz](https://holoviz.org/) makes browser-based data visualization in Python easier learn, easier to use and more powerful.
"""

if __name__.startswith("bokeh"):
    get_component_explorer(config, description, components).servable()