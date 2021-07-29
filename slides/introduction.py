import panel as pn

from shared import Configuration

pn.extension(sizing_mode="stretch_width")

config=Configuration(random=True)

component=f"""
# { config.site }

<img alt="logo" src="{ config.logo }" style="height:200px">

Marc Skov Madsen, PhD, CFA, [marc.skov.madsen@gmail.com](mailto:marc.skov.madsen@gmail),
awesome-panel.org

This talk is on Github: [MarcSkovMadsen/awesome-panel-introduction]\
(https://github.com/marcskovmadsen/awesome-panel-introduction)
"""


pn.template.FastListTemplate(
    site=config.site,
    title="Overview",
    header_accent_base_color=config.header_accent_base_color,
    header_background=config.header_background,
    header_color=config.header_color,
    accent_base_color=config.accent_base_color,
    sidebar_footer=config.menu,
    sidebar_width=400,
    main_max_width="800px",
    main=[component],
).servable()
