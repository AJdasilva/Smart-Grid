
"""
    Code to visualize the OSM data set.
    First plot shows the vertices, color-coded by their type.
    Second plot shows the edges that connect the vertices, color-coded by their voltage.
    Third plot is a combination of the two. The color of each vertex is given by its type, color of the edge given by the voltage of the connection
    
"""

import numpy as np
from numpy import *
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from matplotlib.lines import Line2D
import pandas as pd
import sys

# import the list of vertices as numpy arrays: empty fields are represented by "NaN"
data = pd.read_csv("vertices_de_power_160718.csv", quotechar="'")
v_id = np.array(data["v_id"])
long = np.array(data["lon"])
lat = np.array(data["lat"])
type = np.array(data["typ"])
volt = np.array(data["voltage"])
freq = np.array(data["frequency"])
name = np.array(data["name"])
op = np.array(data["operator"])
ref = np.array(data["ref"])
srid = np.array(data["wkt_srid_4326"])

# Assign a color to each type of vertex, for plotting:
vertex_color = []
for i in range(len(type)):
    if type[i] == 'substation':
        vertex_color.append('b')
    elif type[i] == 'plant':
        vertex_color.append('r')
    elif type[i] == 'auxillary_T_node':
        vertex_color.append('g')
    elif type[i] == 'generator':
        vertex_color.append('c')
    else: # catch any missed types (lazy)
        print type[i]

# Plot vertices, color-coordinated by their type:
plt.figure(1)
for i in range(len(v_id)):
    plt.plot(lat[i], long[i], color=vertex_color[i], marker=".", ls="None")
plt.xlim([46,56])
mx = MultipleLocator(.1)
plt.axes().xaxis.set_minor_locator(mx)
plt.ylim([5,16])
my = MultipleLocator(.1)
plt.axes().yaxis.set_minor_locator(my)
plt.grid(b=True, which="both")
plt.ylabel("Longitude")
plt.xlabel("Latitude")
plt.title("OSM Data - Vertices")
legend_vertices = [Line2D([0], [0], marker='o', ls='None', color='b', label='Substation'),
                  Line2D([0], [0], marker='o', ls='None', color='r', label='Plant'),
                  Line2D([0], [0], marker='o', ls='None', color='g', label='Auxillary T Node'),
                  Line2D([0], [0], marker='o', ls='None', color='c', label='Generator')]
plt.legend(handles=legend_vertices, bbox_to_anchor=(0.75, 1.1))
plt.savefig("vertices.pdf")
#plt.show()
plt.close()

###########################################################

# import the edges:
data = pd.read_csv("links_de_power_160718.csv", quotechar="'")
edge_id = np.array(data["l_id"])
edge_v1 = np.array(data["v_id_1"])
edge_v2 = np.array(data["v_id_2"])
edge_volt = np.array(data["voltage"])

# assign edge colors for plotting (different color for each voltage):
edge_color = []
for i in range(len(edge_volt)):
    if edge_volt[i] == 220000:
        edge_color.append('b')
    elif edge_volt[i] == 300000:
        edge_color.append('c')
    elif edge_volt[i] == 380000:
        edge_color.append('r')
    elif edge_volt[i] == 400000:
        edge_color.append('g')
    elif edge_volt[i] == 450000:
        edge_color.append('y')
    else: # catch any missed types (lazy)
        print edge_volt[i]

# get lat/long of edges:
edge_lats, edge_longs = np.empty((len(edge_id),2)), np.empty((len(edge_id),2))
for i in range(len(edge_id)):
    v1index, v2index = np.where(v_id == edge_v1[i])[0][0], np.where(v_id == edge_v2[i])[0][0]
    edge_lats[i] = [lat[v1index],lat[v2index]]
    edge_longs[i] = [long[v1index],long[v2index]]

# Plot the edges, color-coordinated by voltage:
plt.figure(2)
for i in range(len(edge_id)):
    plt.plot(edge_lats[i], edge_longs[i], marker=".", c=edge_color[i])
plt.xlim([46,56])
mx = MultipleLocator(.1)
plt.axes().xaxis.set_minor_locator(mx)
plt.ylim([5,16])
my = MultipleLocator(.1)
plt.axes().yaxis.set_minor_locator(my)
plt.grid(b=True, which="both")
plt.ylabel("Longitude")
plt.xlabel("Latitude")
plt.title("OSM Data - Edges")
legend_edges = [Line2D([0], [0], marker='o', color='b', label='220000'),
                Line2D([0], [0], marker='o', color='c', label='300000'),
                Line2D([0], [0], marker='o', color='r', label='380000'),
                Line2D([0], [0], marker='o', color='g', label='400000'),
                Line2D([0], [0], marker='o', color='y', label='450000')]
plt.legend(handles=legend_edges, bbox_to_anchor=(0.8, 0.8))
plt.savefig("edges.pdf")
#plt.show()
plt.close()

# Plot both the edges & the vertices. Both are color coordinated so it's pretty busy.
plt.figure(3)
for i in range(len(edge_id)):
    plt.plot(edge_lats[i], edge_longs[i], c=edge_color[i], marker="None")
for i in range(len(v_id)):
    plt.plot(lat[i], long[i], color=vertex_color[i], marker=".", ls="None")
plt.xlim([46,56])
mx = MultipleLocator(.1)
plt.axes().xaxis.set_minor_locator(mx)
plt.ylim([5,16])
my = MultipleLocator(.1)
plt.axes().yaxis.set_minor_locator(my)
plt.grid(b=False, which="both")
plt.ylabel("Longitude")
plt.xlabel("Latitude")
plt.title("OSM Data - Vertices & Edges")
# legend the same as prev. 2 plots
plt.savefig("vertices_and_edges.pdf")
#plt.show()
plt.close()
