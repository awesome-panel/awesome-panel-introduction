import panel as pn

RAW_CSS = """
.bk-root *.bk-btn {
    font-size: 16px;
    font-weight: bold;
}
"""

def get_component_explorer(config, description, components):
    def show(component):
        component = components[component]
        return component.example(theme=config.theme, accent_base_color=config.accent_base_color)


    def reference(component):
        component = components[component]
        return f"[Panel Reference Guide]({ component.reference }), [Docs]({ component.docs })"


    def code(component):
        component = components[component]
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
        options=list(components.keys()), button_type="success", margin=(10, 0, 25, 0)
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
        main=[pn.Row(description, config.get_logo_pane(width=100)), component],
    )
    template.config.raw_css.append(RAW_CSS)
    return template


