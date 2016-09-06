import parser
import render
import layout
import sys

def convert(jsonfile, outfile):
	f = open(jsonfile, 'r')
	jsonstr = f.read()
	graph = parser.parse(jsonstr)
	layout.layout(graph["node"])
	svg = render.render(graph)	
	
	of = open(outfile, 'w')
	of.write(svg)

if __name__ == "__main__":
	if len(sys.argv)<3:
		print "usage: python diajson.py infile outfile"
	else:
		convert(sys.argv[1], sys.argv[2])
		
	
	
