import defaults
from render import *
import copy	

class Node(object):
	def __init__(self, id):
		self.id = id

	def get_size(self):
		return None
	
	def set_pos(self, x, y):
		self.x = x
		self.y = y

	def draw(self):
		pass
	
class BoxNode(Node):
	def __init__(self, id, label):
		self.id = id
		self.label = label
		self.size = None

	def get_size(self):
		if self.size is None:
			text_width = len(self.label)*defaults.CHARACTER_WIDTH
			width = 2*defaults.BOX_PADDING + text_width
			height = 2*defaults.BOX_PADDING + defaults.CHARACTER_HEIGHT
			self.size = (width, height)
		return self.size

	def draw(self):
		# first draw the rectangle
		w, h = self.get_size()
		box_node = render_box(self.x, self.y, w, h)
		text_node = render_text(self.x+defaults.BOX_PADDING, self.y+defaults.BOX_PADDING+defaults.CHARACTER_HEIGHT, self.label)
		return box_node + "\n" + text_node

	def layout(self):
		pass
	
class EdgeNode(Node):
	def __init__(self, src, dst):
		self.id = "edge"
		self.src = src
		self.dst = dst

	def get_size(self):
		return None
	
	def draw(self):
		src, dst = self.src, self.dst
		# check which is on top
		src_w, src_h = src.get_size()
		dst_w, dst_h = dst.get_size()
		src_bottom = src.y + src_h
		dst_bottom = dst.y + dst_h
		src_right = src.x + src_w
		dst_right = dst.x + dst_w
		if src_bottom < dst.y:
			x1 = src.x + src_w/2
			y1 = src_bottom
			x2 = dst.x + dst_w/2
			y2 = dst.y	
		elif dst_bottom < src.y:
			x1 = dst.x + dst_w/2
			y1 = dst_bottom
			x2 = src.x + src_w/2
			y2 = src.y
		elif src_right < dst.x:
			x1 = src_right
			y1 = src.y + src_h/2
			x2 = dst.x
			y2 = dst.y + dst_h/2
		elif dst_right < src.x:
			x1 = dst_right
			y1 = dst.y + dst_h/2
			x2 = src.x
			y2 = src.y + src_h/2
		else:
			raise Exception("Fail to draw edge")
		edge_node = render_line(x1, y1, x2, y2)
		return edge_node

class ClusterNode(Node):
	def __init__(self, id, children):
		self.id = id
		self.children = children
	
	def get_size(self):
		width = 0
		height = 0
		for child in self.children:
			w, h = child.get_size()
			width += w
			height = max(height, h)
		width += defaults.BOX_PADDING*(len(self.children)+1) 
		height += defaults.BOX_PADDING * 2
		return width, height
	
	def draw(self):
		result = ""
		for child in self.children:
			result += child.draw()+"\n"
		return result
	
	def layout(self):
		# from left to right
		offset = self.x
		for child in self.children:
			child.x = offset + defaults.BOX_PADDING	
			child.y = self.y + defaults.BOX_PADDING
			w, h = child.get_size()
			offset = child.x + w
			child.layout()

class RepeatedClusterNode(ClusterNode):
	def __init__(self, id, child, count):
		self.id = id
		self.children = [copy.copy(child) for i in range(4)]
		self.count = count
		self.omitted = "...%d..."%self.count
	
	def get_size(self):
		omitted_width = len(self.omitted) * defaults.CHARACTER_WIDTH
		w, h = super(RepeatedClusterNode, self).get_size()
		return w + defaults.BOX_PADDING+omitted_width, h

	def layout(self):
		omitted_width = len(self.omitted) * defaults.CHARACTER_WIDTH
		super(RepeatedClusterNode, self).layout()
		self.children[2].x += defaults.BOX_PADDING+omitted_width
		self.children[3].x += defaults.BOX_PADDING+omitted_width

	def draw(self):
		result = super(RepeatedClusterNode, self).draw()
		w, h = self.get_size()
		
		omitted_width = len(self.omitted) * defaults.CHARACTER_WIDTH
		many = render_text(self.x+w/2-omitted_width/2, self.y+h/2, self.omitted)
		return result + "\n" + many
			
class LayerNode(Node):
	def __init__(self, id, children):
		self.id = id
		self.children = children
	
	def get_size(self):
		width = 0
		height = 0
		for child in self.children:
			w, h = child.get_size()
			width = max(width, w)
			height += height + defaults.BOX_PADDING
		height += defaults.BOX_PADDING
		return width, height

	def draw(self):
		result = ""
		for child in self.children:
			result += child.draw()
		return result
	
	def layout(self):
		yoffset = self.y
		_w, _ = self.get_size()
		for child in self.children:
			w, h = child.get_size()
			child.y = yoffset + defaults.BOX_PADDING
			yoffset = child.y + h
			child.x = self.x + (_w-w)/2
			child.layout()
	
class ContainerNode(Node):
	def __init__(self, id, child, label=None):
		self.id = id
		self.child = child
		if not isinstance(child, LayerNode) and not isinstance(child, ClusterNode):
			raise Exception("Container can only contain Layer or Cluster") 
		self.label = label
			
	def get_size(self):
		w, h = self.child.get_size()
		return w+defaults.BOX_PADDING*2, h+defaults.BOX_PADDING*3
	
	def draw(self):
		w, h = self.get_size()
		box_node = render_box_dashed(self.x, self.y, w, h)
		if self.label is not None:
			label_node = render_text(self.x+defaults.BOX_PADDING, self.y + defaults.BOX_PADDING+defaults.CHARACTER_HEIGHT, self.label)
		return box_node +"\n" + label_node +"\n"+ self.child.draw()
	
	def layout(self):
		self.child.x = self.x + defaults.BOX_PADDING
		self.child.y = self.y + defaults.BOX_PADDING*2
		self.child.layout()
		 

