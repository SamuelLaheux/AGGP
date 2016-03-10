import networkx as nx
import random
import matplotlib.pyplot as plt
from math import *

# On a un probleme dans cliquishness et small_world pour les noeuds qui se retrouvent isoles apres mutation
# puisque dans cliquishness, il faut calculer le coefficient de clustering ou il y a un k (=nb de voisin) au denominateur.
# Si le k vaut 0, le coefficient de clustering vaut l'infini....... comment le modeliser ? impossible. il faut donc ne pas
# avoir ce cas la. Deux cas viennent a nous : 

# Soit on interdit qu'un noeud se retrouve isole, cad que si il y a une mutation entre 2 noeuds qui supprime le pont
# et que cela engendre qu'un des 2 noeuds n'est connecte de plus personne, alors la mutation ne doit pas avoir lieu

# Soit si une mutation supprime un pont entre 2 noeuds et qu'un noeud se retrouve isole de tout ses autres camarades,
# alors on le supprime. Ca va juste changer la taille d'un graphe. Est-ce que c'est genant ? Je ne crois pas.


#random.seed(0)
gamma = 2.2

class PopGA:
	def __init__(self,Nb_node,P_link,P_SW,P_C,P_D,Size,Tm,Tc,Nb_Generation,T_Fit):
		self.Size = Size
		self.Tm = Tm
		self.Tc = Tc
		self.P_SW = P_SW
		self.P_C = P_C
		self.P_D = P_D
		self.Nb_Generation = Nb_Generation
		self.T_Fit = T_Fit
		self.pop = [Graph(Nb_node,P_link) for i in range(Size)]
		self.Fit = [0 for i in range(Size)]
    
	def Run(self):
		stop_bool= True
		i = 0
		while stop_bool == True:
			self.fitness()
			print "\nFitness of each individual = \n",self.Fit
			#self.selection()
			self.mutation()
			self.crossing_over()
			stop_bool = self.stop(i)
			i += 1


	def fitness(self):
		for i in range(len(self.pop)):
			self.Fit[i] = self.pop[i].fitness(self.P_C,self.P_D,self.P_SW)
		return 0


	def mutation(self):
	 	for i in xrange(len(self.pop)):
	 		alea = random.random()
	 		if alea < self.Tm:
	 			self.pop[i].mutation() 
		return 0


	def crossing_over(self):
		for i in xrange(len(self.pop)):
			alea = random.random()
			if alea < self.Tc:
				indalea = i
				while indalea==i:
					indalea = random.randint(0,len(self.pop)-1)
				self.pop[i].crossing(self.pop[indalea])
		return 0

	def selection(self):
		for i in range(len(self.pop)):
			self.pop[i].selection()
		return 0

	def stop(self,n):
		o = True
		if n >= Nb_Generation:
			o = False
		if (sum(self.Fit)/len(self.Fit)) > self.T_Fit :
			o = False
		return o 



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


	def cliquishness(self):
		# k is the number of neighbors for each nodes
		# n is the number of edges between the neighbors
		list_coeff_clustering = []
		somme = 0.
		for i in self.nodes:
			n = 0
			all_possible_edges = []
			k = len(self.graphe.neighbors(i))
			if k==0 or k==1:
				C = 0
			else:
				for j in self.graphe.neighbors(i):
					for j2 in self.graphe.neighbors(i):
						if j<j2:
							all_possible_edges.append((j,j2))
				for e in self.edges:
					for f in all_possible_edges:
						if e == f:
							n += 1
							break
				C = 2*float(n)/(float(k)*(float(k)-1))
			list_coeff_clustering.append(C)
			# we compare to the law : P(k) = k^-1
			# if k==0, je ne sais pas vraiment ce qui est reellement bon
			# Pour l'instant, je mets juste une condition a revoir
			# Je pense qu'il faudrait interdire dans mutation qu'un noeud se retrouve isole (ou bien sinon il degage s'il n'est accroche a personne)
			if k==0:
				somme = somme + C**2
			else:
				somme = somme + (C -1/k)**2
		return exp(-somme)

	def degree(self):
		global gamma
		N = len(self.nodes)
		nb_neighbors = []
		for i in self.nodes :
			nb_neighbors.append(len(self.graphe.neighbors(i)))
		M = max(nb_neighbors)
		#print "neighbors", nb_neighbors
		deg = 0.0
		for k in xrange(1,M+1):
			Nk = nb_neighbors.count(k)
			deg = deg + ( (float(Nk)/N) - (k**(-gamma)) )**2
		return exp(-deg)



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

	def fitness(self,a,b,c):
		return a*self.cliquishness() + b*self.degree() + c*self.small_world()


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
er2 = g.crossing(er2)
print "ER apres croisement",er2.graphe.edges()
print "G apres croisement",g.graphe.edges()


gr = Graph(5,0.8)
gr.display()
print "\nCLIQUE = %f"%gr.cliquishness()

print "\nSMALL WORLD = %f"%gr.small_world()

print "\nDEGREE = %f"%gr.degree()

print "\nFITNESS = %f"%gr.fitness(1.,1.,1.)


Nb_node = 5
P_link = 1
P_SW = 1
P_C = 1
P_D = 1
Size = 5
Tm = 0.5
Tc = 0.2
Nb_Generation = 100
T_Fit = 10000000
pop1 = PopGA(Nb_node,P_link,P_SW,P_C,P_D,Size,Tm,Tc,Nb_Generation,T_Fit)
pop1.Run()

