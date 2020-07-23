import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import itertools
import random
import numpy as np
import mpld3


#Generate Graph
G = nx.scale_free_graph(10)
# Convert Graph to a list of lists of edges with no self edges
edgeList = nx.to_edgelist(G)
edgeListNew = []
for x in edgeList:
	y = list(x)
	if y[0] != y[1]:
		edgeListNew.append([y[0],y[1]])
k = sorted(edgeListNew)
edgeList = list(k for k, _ in itertools.groupby(k))

source, destination = random.sample(G.nodes, 2)
queue = [[source]]

#Make a dictionary to indicate if a particular node has been visited
# 0 indicates not been visited yet

visited_dict = {}
for x in range(min(G.nodes),max(G.nodes)+1):
	visited_dict[x] = 0


#make a final path list
paths = []


while len(queue)!=0:
	current_path = queue.pop(0)
	current_node = current_path[-1]

	possible_edges = []
	for x in edgeList:
		if current_node in x:
			possible_edges.append(x)

	for x in possible_edges:
		if x[0] == current_node:
			new_node = x[1]
		else:
			new_node = x[0]
		if new_node == destination:
			new_current_path = current_path + [new_node]
			paths.append(new_current_path)
		elif not(new_node in current_path):
			new_current_path = current_path + [new_node]
			queue.append(new_current_path)



 # now need to search for colliders on all paths

d_connected = 0

# a path is d_connected if there is any active path between them
for x in paths:

	path_edges = []
	for y in range(0,len(x)-1):
		if [x[y],x[y+1]] in edgeList:
			path_edges.append([x[y],x[y+1]])
		else:
			path_edges.append([x[y+1],x[y]])

	left = np.asarray(path_edges)[:,0]
	right = np.asarray(path_edges)[:,1]
	
	if len(set(list(left))) == len(list(left)) and len(set(list(right))) == len(list(right)):
		# no collider on path so path is active
		d_connected = 1
	else:
		d_connected = 0
		# colliders on path so path is inactive



if d_connected == 0:
	output_string = "node " + str(source) + " and node " + str(destination) + " are d-separated"
else:
	output_string = "node " + str(source) + " and node " + str(destination)  + " are d-connected"

plt.title(output_string)
nx.draw_planar(G, with_labels=True, font_weight='bold',node_size=400)
plt.show()


