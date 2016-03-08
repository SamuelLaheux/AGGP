import networkx as nx
import random
import matplotlib.pyplot as plt
import math

#random.seed(0)
gamma = 2.2

class Graph:
	def __init__(self,nb_node,link_proba):
		self.nb_node = nb_node
		self.link_proba = link_proba
		self.graphe = nx.erdos_renyi_graph(self.nb_node,self.link_proba)
		self.nodes = self.graphe.nodes()
		self.edges = self.graphe.edges()

	def display(self):
		nx.draw(self.graphe)
		plt.show()

	def genere2nb(self,a,b):
		alea1 = random.randint(a,b)
		alea2 = random.randint(a,b)
		while alea2 == alea1:
			alea2 = random.randint(a,b)
		if alea1 > alea2:
			return [alea2,alea1]
		else:
			return [alea1,alea2]

	def mutation(self):
		nodes = self.graphe.nodes()
		edges = self.graphe.edges()
		alea = self.genere2nb(0,nodes[-1])
		alea1 = alea[0]
		alea2 = alea[1]
		mutation = False
		for i in edges:
			if i==(nodes[alea1],nodes[alea2]):
				mutation = True
				self.graphe.remove_edge(nodes[alea1],nodes[alea2])
		if mutation == False:
			self.graphe.add_edge(nodes[alea1],nodes[alea2])

	def crossing(self,er):
		alea = random.randint(0,self.graphe.nodes()[-1])
		tmp1 = []
		tmp2 = []
		for i in range(alea,er.graphe.nodes()[-1]):
			for j in er.graphe.edges():
				if i==j[0] or i==j[1]:
					tmp1.append(j)
					er.graphe.remove_edge(j[0],j[1])

		for i2 in range(alea,self.graphe.nodes()[-1]):
			for j2 in self.graphe.edges():
				if i2==j2[0] or i2==j2[1]:
					tmp2.append(j2)
					self.graphe.remove_edge(j2[0],j2[1])

		for ed in tmp1:
			self.graphe.add_edge(ed[0],ed[1])

		for edg in tmp2:
			er.graphe.add_edge(edg[0],edg[1])

		return er

	def degree(self):
		global gamma
		N = len(self.nodes)
		nb_neighbors = []
		for i in self.nodes :
			nb_neighbors.append(len(self.graphe.neighbors(i)))
		M = max(nb_neighbors)
		print "neighbors", nb_neighbors
		deg = 0.0
		for k in xrange(1,M+1):
			Nk = nb_neighbors.count(k)
			deg = deg + ( (float(Nk)/N) - (k**(-gamma)) )**2
		return math.exp(-deg)




g = Graph(5,1)
g.display()
print "Graphe G de depart = ",g.graphe.edges()
print "\n"
for i in range(5):
	g.mutation()
	print "MUTATION de G a la %dere generation"%(i+1)
	print "\t",g.graphe.edges()
g.display()

er2 = Graph(5,1)
print "\nER avant croisement",er2.graphe.edges()
print "G avant croisement",g.graphe.edges()
er2 = g.crossing(er2)
print "ER apres croisement",er2.graphe.edges()
print "G apres croisement",g.graphe.edges()

er2.display()
deg = er2.degree()
print "Valeur degree : %f"%deg