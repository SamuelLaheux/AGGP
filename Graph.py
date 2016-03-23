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
gamma = 2.3

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
		self.moyFit = []
    
	def Run(self):
		stop_bool= True
		i = 0
		while stop_bool == True:
			self.fitness()
			#print "\nFitness of each individual = \n",self.Fit
			moy = (sum(self.Fit)/len(self.Fit))
			self.moyFit.append(moy)
			print "Moyenne : %f\n"%moy
			self.selection()
			self.mutation()
			self.crossing_over()
			stop_bool = self.stop(i)
			i += 1
		plt.figure()
		plt.plot(xrange(i),self.moyFit)
		plt.xlabel("nb generation")
		plt.ylabel("moyenne fitness")
		plt.show()


	def fitness(self):
		for i in range(len(self.pop)):
			self.Fit[i] = self.pop[i].fitness(self.P_C,self.P_D,self.P_SW)
		return 0


	def mutation(self):
	 	for i in xrange(len(self.pop)):
	 		self.pop[i].mutation(self.Tm) 
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
		# Creation de la fitness normee
		Fit_norm = []
		for i in self.Fit :
			Fit_norm.append((i*100)/sum(self.Fit))
		# Creation de la roulette proportionnee contenant les indices des graphes
		roulette = []
		for ind,j in enumerate(Fit_norm) :
			val = int(round(j,0))
			for k in xrange(val):
				roulette.append(ind)
		# Creation de liste des indices des enfants
		New_Ind = random.sample(roulette, self.Size)
		# Creation de la nouvelle liste d'objets graphe
		New_Pop = list()
		for j in New_Ind:
			New_Pop.append(self.pop[j])
		# Suppression de l'ancienne population de graphe et remplacement par la nouvelle
		self.pop = []
		self.pop = New_Pop
		New_Pop = []

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
		self.graphe = nx.erdos_renyi_graph(nb_node,link_proba)
		# Pour recuperer les nodes et edges faire self.graphe.nodes() et self.graphe.edges()

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

	def mutation(self, Tm):
		for i in self.graphe.nodes() :
			for j in self.graphe.nodes() :
				if i < j:
					alea = random.random()
					if alea < Tm :
						if (i,j) in self.graphe.edges():
							if len(self.graphe.neighbors(i))>1 and len(self.graphe.neighbors(j))>1:
								self.graphe.remove_edge(i,j)
						else :
							self.graphe.add_edge(i,j)



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
		if nx.is_connected(self.graphe) == True :
			list_coeff_clustering = []
			somme = 0.
			for i in self.graphe.nodes():
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
					for e in self.graphe.edges():
						for f in all_possible_edges:
							if e == f:
								n += 1
								break
					C = 2*float(n)/(float(k)*(float(k)-1))
				list_coeff_clustering.append(C)
				# we compare to the law : P(k) = k^-1
				somme = somme + (C -1/k)**2
			return exp(-somme)
		else :
			return 0

	def degree(self):
		global gamma
		N = len(self.graphe.nodes())
		nb_neighbors = []
		for i in self.graphe.nodes() :
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

		if nx.is_connected(self.graphe)==True:

			for i in self.graphe.nodes(): #on parcourt tous les noeuds du graphe
				d=0.
				for j in self.graphe.nodes():  #on regarde tous les autres noeuds
					if i<j:
						d+=len(nx.shortest_path(self.graphe,source=i,target=j))-1 #distance entre ces 2 noeuds

				d=float(d/(N-1)) #distance observee entre le noeud i et N-1 autres noeuds
				dmoy+=d

			dobs=float(dmoy/N) #distance moy sur tous les noeuds

			e=exp(-(dobs-log(N))**2)
			return e

		else: #si graphe pas connecte
			e=0
			return e

	def fitness(self,a,b,c):
		return a*self.cliquishness() + b*self.degree() + c*self.small_world()


# MAIN
## Parametres
Nb_node = 30
P_link = 0.8
P_SW = 1./20
P_C = 1./20
P_D = 18./20
Size = 100
Tm = 0.5
Tc = 0.2
Nb_Generation = 50
T_Fit = 1 # valeur seuil de la fitness (critere d'arret)

## Creation de la population
pop1 = PopGA(Nb_node,P_link,P_SW,P_C,P_D,Size,Tm,Tc,Nb_Generation,T_Fit)


print "----------------- RUN -----------------------"
pop1.Run()

