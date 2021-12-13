import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_agraph import graphviz_layout
import sys


def op(x):

    if x > 23:
        return 'red'

    if x > 20:
        return 'blue'

    return 'gray'


def color(val):
    l = map(op, val)
    print(l)
    return map(op, val)


#col = ['red']*5

df = pd.read_csv("example.csv")
# Build a dataframe with 4 connections
#df = pd.DataFrame({'from': ['A', 'B', 'C', 'A', 'A'], 'to': ['D', 'A', 'E', 'C', 'E'], 'value':[1, 10, 5, 5, 3]})

# Build your graph
G = nx.from_pandas_edgelist(
    df, 'from', 'to', edge_attr='char', create_using=nx.MultiDiGraph)

pos = nx.drawing.nx_agraph.graphviz_layout(G, prog='neato')
#pos = nx.spring_layout(G)
#pos = nx.circular_layout(G)


labels = dict([((n1, n2), d['char']) for n1, n2, d in G.edges(data=True)])
# print(labels)

# Plot it
nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=300, edge_color='red',
        width=2, edge_cmap=plt.cm.Blues, arrows=True, connectionstyle='arc3, rad = 0.1')
nx.draw_networkx_edge_labels(
    G, pos, edge_labels=labels, font_color='red', label_pos=0.2)  # label_pos=0.3
plt.show()
