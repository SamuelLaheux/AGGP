import networkx as nx
import random
import matplotlib.pyplot as plt
from math import *

#random.seed(0)

class Graph:
	def __init__(self,nb_node,link_proba):
		self.nb_node = nb_node
		self.link_proba = link_proba
		self.graphe = nx.erdos_renyi_graph(self.nb_node,self.link_proba)
		self.nodes = self.graphe.nodes()
		self.edges = self.graphe.edges()

	def display(self):
		i=0
		plt.figure(i)
		nx.draw(self.graphe)
		nx.draw_networkx_labels(self.graphe,pos=nx.spring_layout(self.graphe))
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


	#calculate the small world criteria
	def small_world(self):
		N=len(self.graphe.nodes())
		dmoy=0.

		for i in self.graphe.nodes(): #on parcourt tous les noeuds du graphe
			d=0.
			for j in self.graphe.nodes():  #on regarde tous les autres noeuds
				if i!=j:
					d+=len(nx.shortest_path(self.graphe,source=i,target=j))-1 #distance entre ces 2 noeuds

			d=float(d/(N-1)) #distance observee entre le noeud i et N-1 autres noeuds
			dmoy+=d

		dobs=float(dmoy/N) #distance moy sur tous les noeuds

		e=exp(-(dobs-log(N))**2)
		return e



#Grapj(nb_nodes,link_proba)
g = Graph(5,1)
g.display()
print g.small_world()

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
g.crossing(er2)
print "ER apres croisement",er2.graphe.edges()
print "G apres croisement",g.graphe.edges()


print g.small_world()