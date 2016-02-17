import networkx as nx
import random


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
def mutation(nodes,edges,p):
	mutation = False
	for i in nodes:
		for j in nodes:
			if i!=j:
				alea = random.random()
				if alea < p:
					for k in fonction[i]:
						if k == j:
							mutation = True




mutation(nodes,edges,0.5)

er.clear()