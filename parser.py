from bs4 import BeautifulSoup as soup
import sys
import math
from numpy import zeros
from numpy import savetxt

class Parser:
	def __init__(self, inputFileName): 
		print("Start Parsing...")
		self.inputFileName = inputFileName

		# get graphml file
		infile = open(self.inputFileName ,"r")
		contents = infile.read()

		# call it in beautifulSoup
		self.page_soup = soup(contents,'xml')

		self.nodes_dict = {}
		self.table = []

		self.getNodes()
		self.getEdges()

		print("Complete parsing")


	def getNodes(self):
		#csv file for nodes
		nodesFileName = self.inputFileName.replace(".graphml", "") + "_nodes.csv"
		nodesFile = open(nodesFileName, "w")
		headers = "id, label, x, y\n"
		nodesFile.write(headers)

		# get all nodes
		nodes = self.page_soup.graphml.findAll('node')
		if(nodes != None):
			for node in nodes:
				# x_coord, y_coord, id 
				node_id = node['id']
				if len(nodes) == 1: 
					node_data = node.findAll("data")[0].findAll("y:ShapeNode")[0]
				else:
					node_data = node.findAll("data")[1].findAll("y:ShapeNode")[0]
				label = node_data.findAll("y:NodeLabel")[0].text 
				if label.replace(" ", "") == "": print("empty: " + label)
				x = str(int(float(node_data.findAll("y:Geometry")[0]['x'])))
				y = str(int(float(node_data.findAll("y:Geometry")[0]['y'])))

				#store values in the node dictionary
				self.nodes_dict[node_id] = [x,y]

				nodesFile.write(node_id + "," + label + "," + x + "," + y + "\n")
				print("id " + node_id + ",label " + label + ",x " + x + ",y " + y)
		else:
			print("No nodes in the file")

		nodesFile.close()

	# add distance
	def getEdges(self):
		#csv file for esges
		edgesFileName = self.inputFileName.replace(".graphml", "") + "_edges.csv"
		edgesFile = open(edgesFileName, "w")
		headers = "id, source, target, distance\n"
		edgesFile.write(headers)
		self.table = zeros((len(self.nodes_dict), len(self.nodes_dict)), dtype=float)

		# get all edges
		edges = self.page_soup.graphml.findAll("edge")
		if edges != None:
			for edge in edges:
				# id, source, target
				edge_id = edge['id']
				source = edge['source']
				target = edge['target']

				#calculate distance
				source_xy = self.nodes_dict[source]
				target_xy = self.nodes_dict[target]
				distance = self.distance(source_xy, target_xy)

				self.table[self.getIndex(source)][self.getIndex(target)] = distance

				edgesFile.write(edge_id + "," + source + "," + target + "," + str(distance) + "\n")
				print("id " + edge_id + ",source " + source + ",target " + target + ", distance " + str(distance))
		else:
			print("No edges in the file")

		# write out matrix
		# since we are graphing directed graph, row represents from and column represents to
		matrixFileName = self.inputFileName.replace(".graphml", "") + "_matrix.csv"
		matrixFile = open(matrixFileName, "w")
		savetxt(matrixFileName, self.table, fmt='%.2f')
		matrixFile.close()

		edgesFile.close()

	# return the distance between two points
	def distance(self, source_xy, target_xy):
		x_dist = int(math.pow((int(source_xy[0]) - int(target_xy[0])), 2))
		y_dist = int(math.pow((int(source_xy[1]) - int(target_xy[1])), 2))
		distance = round(math.sqrt(x_dist+y_dist), 2)
		return distance

	def getIndex(self, node_id):
		return int(node_id[1:])



if __name__ == '__main__':
    Parser(sys.argv[1])
