import panel as pn
from ipyleaflet import Map, VideoOverlay

pn.extension("ipywidget")

m = Map(center=(25, -115), zoom=4)

video = VideoOverlay(
    url="https://www.mapbox.com/bites/00188/patricia_nasa.webm",
    bounds=((13, -130), (32, -100))
)
m.add_layer(video)
pn.pane.IPyWidget(m, height=500, width=500).servable()