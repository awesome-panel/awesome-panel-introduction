import param
import panel as pn
import pathlib
import random

_COLORS = [
    ("#00A170", "white"),
    ("#DAA520", "white"),
    ("#2F4F4F", "white"),
    ("#F08080", "white"),
]
_LOGOS = {
    "default": "https://panel.holoviz.org/_static/logo_stacked.png",
    "dark": "https://panel.holoviz.org/_static/logo_horizontal.png",
}


_MENU_FILE = pathlib.Path(__file__).parent / "menu.html"
_MENU_TEXT = _MENU_FILE.read_text()

_ACE_THEMES={
    "default": "chrome",
    "dark": "tomorrow_night_eighties"
}

class Configuration(param.Parameterized):
    theme = param.String()
    site = param.String(default="Highly Interactive Data Apps with Panel")
    logo = param.String()
    accent_base_color = param.Color()
    header_color = param.Color()
    header_accent_base_color = param.Color("white")
    header_background = param.Color()
    ace_theme=param.String()

    def __init__(self, random=False, **params):
        """Configuration for your (Fast) Template

        Args:
            random (bool, optional): Whether or not to provide randomized values. Defaults to False.
        """
        super().__init__(**params)

        self.theme = self._get_theme()

        if random:
            color_index = self._get_random_color_index()
        else:
            color_index=0

        self.accent_base_color = _COLORS[color_index][0]
        self.header_color = _COLORS[color_index][1]
        self.header_background = self.accent_base_color

        self.logo=_LOGOS[self.theme]
        self.ace_theme=_ACE_THEMES[self.theme]

    def _get_theme(self):
        if pn.template.FastListTemplate().theme==pn.template.DarkTheme:
            return "dark"
        return "default"

    def _get_random_color_index(self):
        if not "color" in pn.state.cache:
            pn.state.cache["color"]=-1
        color = pn.state.cache["color"]+1
        if color==len(_COLORS):
            color=0
        pn.state.cache["color"]=color
        return color

    @property
    def _collapsed_icon(self) -> str:
        return f"""<svg style="stroke: { self.accent_base_color }" width="18" height="18" viewBox="0 0 18 18" fill="none" xmlns="http://www.w3.org/2000/svg" slot="collapsed-icon">
<path d="M15.2222 1H2.77778C1.79594 1 1 1.79594 1 2.77778V15.2222C1 16.2041 1.79594 17 2.77778 17H15.2222C16.2041 17 17 16.2041 17 15.2222V2.77778C17 1.79594 16.2041 1 15.2222 1Z" stroke-linecap="round" stroke-linejoin="round"></path>
<path d="M9 5.44446V12.5556" stroke-linecap="round" stroke-linejoin="round"></path>
<path d="M5.44446 9H12.5556" stroke-linecap="round" stroke-linejoin="round"></path>
</svg>"""

    @property
    def _expanded_icon(self) -> str:
        return f"""<svg style="stroke: { self.accent_base_color }" width="18" height="18" viewBox="0 0 18 18" fill="none" xmlns="http://www.w3.org/2000/svg" slot="expanded-icon">
<path d="M15.2222 1H2.77778C1.79594 1 1 1.79594 1 2.77778V15.2222C1 16.2041 1.79594 17 2.77778 17H15.2222C16.2041 17 17 16.2041 17 15.2222V2.77778C17 1.79594 16.2041 1 15.2222 1Z" stroke-linecap="round" stroke-linejoin="round"></path>
<path d="M5.44446 9H12.5556" stroke-linecap="round" stroke-linejoin="round"></path>
</svg>
"""

    @property
    def menu(self) -> str:
        """Returns a HTML Menu"""
        return _MENU_TEXT.replace("{ COLLAPSED_ICON }", self._collapsed_icon).replace("{ EXPANDED_ICON }", self._expanded_icon)

if __name__.startswith("bokeh"):
    config=Configuration()
    pn.template.FastListTemplate(
        title="Test Configuration",
        site=config.site,
        header_accent_base_color=config.header_accent_base_color,
        header_background=config.header_background,
        header_color=config.header_color,
        sidebar_footer=config.menu,
        accent_base_color=config.accent_base_color,
        main=[pn.pane.PNG(config.logo)],
    ).servable()