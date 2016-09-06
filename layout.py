import defaults

def layout(node):
	# get the dimensions
	w, h = node.get_size()
	margin = (defaults.CANVAS_WIDTH - w)/2
	node.x = margin
	node.y = defaults.BOX_PADDING*2
	node.layout()
 			
	

