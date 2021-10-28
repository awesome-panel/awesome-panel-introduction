import panel as pn

from components import ipywidgets
from components.explorer import get_component_explorer

from shared import Configuration

pn.extension("ipywidgets", sizing_mode="stretch_width")

# FONTAWESOME_LINK = "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.5.0/css/font-awesome.css"
# pn.config.css_files.append(FONTAWESOME_LINK)

config = Configuration(
    title="Works with IPyWidgets",
    url="works_with_ipywidgets",
    random=True,
)

CSS = f"""
:root {{
    --accent-fill-active: yellow;
    --jp-widgets-slider-handle-background-color: {config.accent_base_color};
    --jp-widgets-slider-active-handle-color: {config.accent_base_color};
}}
"""

DARK_CSS = """
:root {{
    --jp-content-font-color1: white;
}}
"""

components = {k: v() for k,v in ipywidgets.ALL.items()}

description = """
# Works with IPyWidgets ❤️

### To use IPyWidgets with Panel just wrap the python object into a `pn.panel`, a *layout* like `pn.Column` or the `pn.pane.IPyWidgets` pane.
"""

if __name__.startswith("bokeh"):
    template = get_component_explorer(config, description, components)
    template.config.raw_css.append(CSS)
    if config.theme=="dark":
        template.config.raw_css.append(DARK_CSS)
    template.servable()