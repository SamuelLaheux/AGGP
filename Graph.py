import networkx as nx
import random
import matplotlib.pyplot as plt
from math import *
import numpy as np

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
		self.pop = [Graph(Nb_node,random.choice(P_link),0,1) for i in range(Size)]
		self.Fit = [0. for i in range(Size)]
		self.moyFit = []
		self.minFit = []
		self.maxFit = []

		self.coeff_sw = [] #evolution de valeur du coeff sw pour le meilleur graphe a chaque generation
		self.moyEnVueSw = 0 #stockee pour calcul moyenne sur les graphes a une gene donnee
		self.moy_sw = [] #moyenne pour les graphes sur ttes les gene

		self.coeff_c = [] #idem pour pc
		self.moyEnVueC = 0
		self.moy_c = []

		self.coeff_d = [] #idem pour pd
		self.moyEnVueD = 0
		self.moy_d = []

		# self.moy_d = []
    
	def Run(self):
		stop_bool= True
		i = 0
		# self.pop[0].display("Tree_Initial_psw=%f_pd=%f_tc=%f.png"%(self.P_SW,self.P_D,self.Tc))
		while stop_bool == True:
			indice_best=self.fitness()

			#print "\nFitness of each individual = \n",self.Fit

			#FITNESS stockage
			moy = (sum(self.Fit))/(len(self.Fit))
			self.moyFit.append(moy)
			#print "Moyenne : %f\n"%moy
			self.minFit.append(min(self.Fit))
			self.maxFit.append(max(self.Fit))

			#COEFFS stockage
			self.coeff_sw.append((self.pop[indice_best]).sw)
			self.coeff_c.append((self.pop[indice_best]).clique)
			self.coeff_d.append((self.pop[indice_best]).degre)

			self.moy_sw.append(self.moyEnVueSw)
			self.moy_c.append(self.moyEnVueC)
			self.moy_d.append(self.moyEnVueD)


			#SUITE RUN

			self.selection()
			self.mutation()
			self.crossing_over()
			stop_bool = self.stop(i)

			i += 1
		# Recuperer l'indice du meilleur graphe
		Indice_maxFit = self.Fit.index(self.maxFit[-1])
		# Display du meilleur graphe
		# self.pop[Indice_maxFit].display("Tree_Final_psw=%f_pd=%f_tc=%f.png"%(self.P_SW,self.P_D,self.Tc))
		self.export(i)



	def export(self,i):
		plt.figure()
		plt.plot(xrange(i),self.moyFit,label='moy')
		plt.plot(xrange(i),self.minFit,'g',label='min')
		plt.plot(xrange(i),self.maxFit,'r',label='max')
		plt.legend()
		plt.xlabel("nb generation")
		plt.ylabel("fitness")
		plt.savefig("psw=%f_pd=%f_tc=%f_tm=%f_Fitness.png"%(self.P_SW,self.P_D,self.Tc,self.Tm))
		plt.title("100 nodes, 80 individus")
		#plt.show()

		plt.figure()
		plt.plot(xrange(i),self.coeff_sw,'b',label='best sw')
		plt.plot(xrange(i),self.moy_sw,'b--',label='moy sw')

		plt.plot(xrange(i),self.coeff_c,'r',label='best clique')
		plt.plot(xrange(i),self.moy_c,'r--',label='moy clique')

		plt.plot(xrange(i),self.coeff_d,'g',label='best degree')
		plt.plot(xrange(i),self.moy_d,'g--',label='moy degree')



		plt.xlabel=("nb generation")
		plt.legend()
		plt.savefig("psw=%f_pd=%f_tc=%f_tm=%f_Criteres.png"%(self.P_SW,self.P_D,self.Tc,self.Tm))



	#maj les fitness
	#renvoie l'indice de l'ind avec la meilleure fitness
	def fitness(self):
		# degL = []
		# SWL = []
		# cliqL = []
		best_ind=-1 #initialisation de l'indice pour le meilleur individu
		best_fitness=0 #initialisation de la meilleur fitness

		self.moyEnVueSw=0
		self.moyEnVueC=0
		self.moyEnVueD=0

		for i in range(len(self.pop)):
			print i 
			self.Fit[i] = self.pop[i].fit(self.P_C,self.P_D,self.P_SW)
			print i 
			self.moyEnVueSw+=self.pop[i].sw
			self.moyEnVueC+=self.pop[i].clique
			self.moyEnVueD+=self.pop[i].degre


			if self.Fit[i]>best_fitness:
				best_fitness=self.Fit[i]
				best_ind=i
			# val = self.pop[i].fit(self.P_C,self.P_D,self.P_SW)
			# cliqL.append(val[0])
			# degL.append(val[1])
			# SWL.append(val[2])
		#print "Moy Clique : %g, Moy SW : %g, Moy deg : %g"%(sum(cliqL)/len(cliqL), sum(SWL)/len(SWL), sum(degL)/len(degL))
		print "best",best_fitness
		print "ind fit",i
		self.moyEnVueSw/=self.Size
		self.moyEnVueC/=self.Size
		self.moyEnVueD/=self.Size
		print i 
		return best_ind


	def mutation(self):
	 	for i in xrange(len(self.pop)): # On parcourt chaque graphe
	 		#self.pop[i] = self.pop[i].mutation(self.Tm) # on appelle la fonction mutation
	 		self.pop[i].mutation(self.Tm)
		return 0


	def crossing_over(self):

		for i in xrange(len(self.pop)):
			alea = random.random()
			if alea < self.Tc:
				indalea = i
				# Pour ne pas selectionne deux fois le meme graphe a crossing
				while indalea==i:
					indalea = random.randint(0,len(self.pop)-1)
				#print type(self.pop[i])
				self.pop[i].crossing(self.pop[indalea])

		return 0

	def selection(self):
		# Calcul la somme des fitness
		tot = sum(self.Fit)
		# Tirage multivarie : retourne une liste de taille de la population contenant le nombre de fois que l'indiv est selectionne
		# en fonction de la fitness de l'indiv
		alea = np.random.multinomial(self.Size, list(np.array(self.Fit)/tot), size=1)
		# Creation de la nouvelle pop
		New_Pop = []
		# On utilise alea[0] car alea est une liste de liste
		for ind,val in enumerate(alea[0]):
			# Permet d'ajouter val fois le nombre d'indiv a la nouvelle pop
			# si val = 0, extend ne rajoute pas l'indiv (car pas selectionne)
			if val != 0:
				for i in xrange(val):
					G = self.pop[ind].graphe
					New_Pop.append(Graph(0,0,G,2))
		self.pop = []
		self.pop = New_Pop

		return 0

	def stop(self,n):
		o = True
		if n >= Nb_Generation:
			o = False
		if (sum(self.Fit)/len(self.Fit)) > self.T_Fit :
			o = False
		return o 



class Graph:
	def __init__(self,nb_node,link_proba, unGraph, init):
		if init==1:
			self.graphe = nx.erdos_renyi_graph(nb_node,link_proba)
		else :
			self.graphe = unGraph.copy()
		# Pour recuperer les nodes et edges faire self.graphe.nodes() et self.graphe.edges()

		self.sw = 0 #carre de l'ecart entre la valeur observee et theorique
		self.clique = 0 #valeur observee
		self.degre = 0
		

	def display(self,name):
		plt.figure()
		nx.draw(self.graphe)
		plt.savefig(name)

	def genere2nb(self,a,b):
		alea1 = random.randint(a,b)
		alea2 = random.randint(a,b)
		while alea2 == alea1:
			alea2 = random.randint(a,b)
		if alea1 > alea2:
			return [alea2,alea1]
		else:
			return [alea1,alea2]

	




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



	def mutation(self, Tm):

		for i in self.graphe.nodes() :
			for j in self.graphe.nodes() :
				alea = random.random()
				if i < j and alea < Tm:
					if (i,j) in self.graphe.edges():
						if len(self.graphe.neighbors(i))>1 and len(self.graphe.neighbors(j))>1:
							self.graphe.remove_edge(i,j)
					else :
						self.graphe.add_edge(i,j)


	def fit(self,a,b,c):
		global gamma  #degree
		#global coeff_exp # Attenuation de la pente de l'exponentielle (faibles valeurs)
		N = len(self.graphe.nodes())
		nb_neighbors = []
		dmoy=0.

		# k is the number of neighbors for each nodes
		# n is the number of edges between the neighbors
		if nx.is_connected(self.graphe) == True :
			list_coeff_clustering = []
			somme = 0.
			edges = self.graphe.edges()
			for i in self.graphe.nodes():

				#CLIQUE
				neighbors = self.graphe.neighbors(i)

				k = len(neighbors)

				nb_neighbors.append(k)
				n = 0
				if k <= 1:
					C = 0
				else:
					for j in neighbors:
						for j2 in neighbors:
							if j<j2 and (j,j2) in edges:
								n += 1
				

				# k is the number of neighbors for each nodes
				# n is the number of edges between the neighbors
					C = 2*float(n)/(float(k)*(float(k)-1))
				list_coeff_clustering.append(C)
				# we compare to the law : P(k) = k^-1
				somme = somme + (C -1/k)**2


				#SW
				d=0.
				for j in self.graphe.nodes():  #on regarde tous les autres noeuds
					if i!=j:
						d+=len(nx.shortest_path(self.graphe,source=i,target=j))-1 #distance entre ces 2 noeuds pour le calcul de small world

				d=float(d/(N-1)) #distance observee entre le noeud i et N-1 autres noeuds
				dmoy+=d
			
			#Clique norme N
			somme=float(somme/N)
			self.clique=somme*2.5

			# SW
			dobs= float(dmoy/N) #distance moy sur tous les noeuds
			coeff= (dobs-log(N))**2
			e=exp(-coeff/10)
			self.sw=coeff/10

			# Degre

			M = max(nb_neighbors)
			deg = 0.0

			for k in xrange(1,M+1):
				Nk = nb_neighbors.count(k)

				deg = deg + ( (float(Nk)/N) - (k**(-gamma)) )**2  # Est ce qu'on diviserait pas par M--
			
			self.degre=deg*0.9
			#print "Clique : %g, SW : %g, deg : %g\n"%(somme*1.5, ((dobs-log(N))**2)/10, deg*0.9)
			return a*exp(-somme*2.5) + b*exp(-deg*0.9) + c*e
			#return (somme*2.5, deg*0.9, ((dobs-log(N))**2)/10)

		else :
			# graphe pas connexe donc on ne peut calculer que
			
			# for i in self.graphe.nodes() :
			# 	nb_neighbors.append(len(self.graphe.neighbors(i)))
			# M = max(nb_neighbors)
			# deg = 0.0
			# for k in xrange(1,M+1):
			# 	Nk = nb_neighbors.count(k)
			# 	deg = deg + ( (float(Nk)/N) - (k**(-gamma)) )**2
			# self.sw=0
			# self.clique=0
			# self.degre=deg*0.9

			return 0.001*0.9
			#return (0,deg*0.9,0)



# MAIN
## Parametres

Nb_node = 100 #100 avant

P_link = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1] #Bien 
P_SW = 50./100 
P_C = 25./100 #Parisot
P_D = 25./100
Size = 50
Tm = 1/Size#Parisot
Tc = 0.01
Nb_Generation = 50 #50

T_Fit = 1 # valeur seuil de la fitness (critere d'arret)

## Creation de la population

pop1 = PopGA(Nb_node,P_link,P_SW,P_C,P_D,Size,Tm,Tc,Nb_Generation,T_Fit)


print "----------------- RUN -----------------------"
pop1.Run()

#Test de plusieurs parametres


tc1=[0.05, 0.15]
tc2 = [0.03,0.05,0.07,0.08]

k=1
psw = 0.3
for j in tc1:
	print "k=",k
	pd=1-P_C-psw
	pop1 = PopGA(Nb_node,P_link,psw,P_C,pd,Size,Tm,j,Nb_Generation,T_Fit)
	pop1.Run()
	k=k+1

# k=1
# psw = 0.1
# for j in tc1:
# 	print "k=",k
# 	pd=1-P_C-psw
# 	pop1 = PopGA(Nb_node,P_link,psw,P_C,pd,Size,Tm,j,Nb_Generation,T_Fit)
# 	pop1.Run()
# 	k=k+1


# k=1
# psw = 0.01
# for j in tc1:
# 	print "k=",k
# 	pd=1-P_C-psw
# 	pop1 = PopGA(Nb_node,P_link,psw,P_C,pd,Size,Tm,j,Nb_Generation,T_Fit)
# 	pop1.Run()
# 	k=k+1
















######fonction de fitness

	# def cliquishness(self):
	# 	# k is the number of neighbors for each nodes
	# 	# n is the number of edges between the neighbors
	# 	if nx.is_connected(self.graphe) == True :
	# 		list_coeff_clustering = []
	# 		somme = 0.
	# 		for i in self.graphe.nodes():
	# 			n = 0
	# 			all_possible_edges = []
	# 			k = len(self.graphe.neighbors(i))
	# 			if k==0 or k==1:
	# 				C = 0
	# 			else:
	# 				for j in self.graphe.neighbors(i):
	# 					for j2 in self.graphe.neighbors(i):
	# 						if j<j2:
	# 							all_possible_edges.append((j,j2))
	# 				for e in self.graphe.edges():
	# 					for f in all_possible_edges:
	# 						if e == f:
	# 							n += 1
	# 							break
	# 				C = 2*float(n)/(float(k)*(float(k)-1))
	# 			list_coeff_clustering.append(C)
	# 			# we compare to the law : P(k) = k^-1
	# 			somme = somme + (C -1/k)**2
	# 		return exp(-somme)
	# 	else :
	# 		return 0

	# def degree(self):
	# 	global gamma
	# 	N = len(self.graphe.nodes())
	# 	nb_neighbors = []
	# 	for i in self.graphe.nodes() :
	# 		nb_neighbors.append(len(self.graphe.neighbors(i)))
	# 	M = max(nb_neighbors)
	# 	#print "neighbors", nb_neighbors
	# 	deg = 0.0
	# 	for k in xrange(1,M+1):
	# 		Nk = nb_neighbors.count(k)
	# 		deg = deg + ( (float(Nk)/N) - (k**(-gamma)) )**2
	# 	return exp(-deg)



	# #calculate the small world criteria
	# def small_world(self):
	# 	N=len(self.graphe.nodes())
	# 	dmoy=0.

	# 	if nx.is_connected(self.graphe)==True:

	# 		for i in self.graphe.nodes(): #on parcourt tous les noeuds du graphe
	# 			d=0.
	# 			for j in self.graphe.nodes():  #on regarde tous les autres noeuds
	# 				if i<j:
	# 					d+=len(nx.shortest_path(self.graphe,source=i,target=j))-1 #distance entre ces 2 noeuds

	# 			d=float(d/(N-1)) #distance observee entre le noeud i et N-1 autres noeuds
	# 			dmoy+=d

	# 		dobs=float(dmoy/N) #distance moy sur tous les noeuds

	# 		e=exp(-(dobs-log(N))**2)
	# 		return e

	# 	else: #si graphe pas connecte
	# 		e=0
	# 		return e


