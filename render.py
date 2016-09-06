import defaults

def render(graph):
	assert "node" in graph and "edges" in graph
	node = graph["node"]
	_, h = node.get_size()
	canvas_height = h+ defaults.BOX_PADDING*2
	xml = "<?xml version=\"1.0\" standalone=\"no\"?>\n"+ \
                "<!DOCTYPE svg PUBLIC \"-//W3C//DTD SVG 1.1//EN\" \"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd\">\n" + \
		"<svg height=\"%d\" width=\"%d\" xmlns=\"http://www.w3.org/2000/svg\" xmlns:xlink=\"http://www.w3.org/1999/xlink\">\n" % (800, defaults.CANVAS_WIDTH)+ \
		" <g style=\"fill-opacity:1.0; stroke:black;\n"+\
		"  stroke-width:1;\">\n"
	xml += node.draw()
        for edge in graph["edges"]:
		xml += edge.draw()           
        xml += " </g>\n</svg>\n"
	return xml
	

def render_box(x, y, w, h):
	return """<rect x="%d" y="%d" height="%d" width="%d" fill="none" stroke="black" stroke-width="2" rx="4" ry="4" />""" % (x, y, h, w)


def render_box_dashed(x, y, w, h):
	return """<rect x="%d" y="%d" height="%d" width="%d" fill="none" stroke="navy" stroke-width="2" rx="2" ry="2" stroke-dasharray="2,2" />""" % (x, y, h, w)

def render_text(x, y, text):
        return """<text x="%d" y="%d" font-family="Verdana" font-size="12" fill="blue">%s</text>""" % (x, y, text)

def render_line(x1, y1, x2, y2):
	return """<line x1="%d" y1="%d" x2="%d" y2="%d" stroke-width="2"/>""" % (x1, y1, x2, y2)
