import networkx as nx

# Creation d'un graphe aleatoire ou on donne le nombre de noeuds et la probibilite de liaison
er=nx.erdos_renyi_graph(10,0.5)
print "NUMBER OF NODES = ",er.number_of_nodes()
print "NUMBER OF EDGES = ",er.number_of_edges()
print "NODE = ",er.nodes()
print "EDGE = ",er.edges()
print "VOISIN DE 1 = ",er.neighbors(1)
er.clear()