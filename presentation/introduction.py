import panel as pn

from shared import Configuration

RAW_CSS="""
.bk-root h1 {
    font-size: 3vw;
    line-height: 5vw;
}
.bk-root h2 {
    font-size: 2vw;
    line-height: 3vw;
}
.bk-root .bk {
    font-size: 0.8vw;
    line-height: 1.2vw;
}
"""

pn.extension(sizing_mode="stretch_width")




config = Configuration(title="Introduction", url="introduction", random=True)

top = f"""
# { config.site }

## Beautiful and Powerful too! ❤️💪"""

gif = pn.pane.PNG(
    config.logo,
    height=422,
    width=500,
    link_url="https://panel.holoviz.org",
    embed=False,
    sizing_mode="scale_height",
    align="center",
    margin=25,
)

bottom = pn.pane.Markdown(
    f"""**Marc Skov Madsen**, PhD, CFA®, [datamodelsanalytics.com](https://datamodelsanalytics.com),
[marc.skov.madsen@gmail.com](mailto:marc.skov.madsen@gmail)

This presentation is of course **made with Panel**. You can find the code on **Github** at
[marcskovmadsen/awesome-panel-introduction]\
(https://github.com/marcskovmadsen/awesome-panel-introduction).

For more about Panel check out my site [awesome-panel.org](https://awesome-panel.org)"""
)

component = pn.Column(top, gif, bottom, sizing_mode="stretch_both")

template=pn.template.FastListTemplate(
    site=config.site,
    title=config.title,
    header_accent_base_color=config.header_accent_base_color,
    header_background=config.header_background,
    header_color=config.header_color,
    accent_base_color=config.accent_base_color,
    sidebar_footer=config.menu,
    sidebar_width=config.sidebar_width,
    main_max_width="95%",
    main=[component],
)
template.config.raw_css.append(RAW_CSS)
template.servable()