import networkx as nx
import random

random.seed(0)

# Creation d'un graphe aleatoire ou on donne le nombre de noeuds et la probibilite de liaison
er=nx.erdos_renyi_graph(10,0.5)
nb_nodes = er.number_of_nodes()
print "NUMBER OF NODES = ",nb_nodes
nb_edges = er.number_of_edges()
print "NUMBER OF EDGES = ",
nodes = er.nodes()
print "NODE = ",nodes
edges = er.edges()
print "EDGE = ",edges


# Calcul de la fonction de cout
fonction = []
for i in xrange(nb_nodes):
	voisin = er.neighbors(i)
	print " %d : "%i
	print "voisin",voisin
	fonction.append(voisin)

print "fonction : ",fonction

# Mutation
def mutation(er,p):
	nodes = er.nodes()
	edges = er.edges()
	mutation = False
	for i in nodes:
		for j in nodes:
			if i<j:
				alea = random.random()
				if alea < p:
					mutation = False
					for k in fonction[i]:
						if k == j:
							mutation = True
							er.remove_edge(j,i)
					if mutation == False:
						er.add_edge(i,j)
	return er



print "NODE = ",nodes
edges = er.edges()
print "EDGE = ",edges


er2 = mutation(er,1)
print "nodes \n",er2.nodes()
print "edges \n",er2.edges()
#if 1 in er[0]

er.clear()