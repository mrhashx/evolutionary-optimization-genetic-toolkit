import numpy as np
import pandas as pd
from Individual import Individual
import math
import random
import matplotlib.pyplot as plt

class GA:
    def __init__(self,M_G=50,P_S = 7):
        
        self.Max_Generation = int(M_G)
        self.Population_Size = int(P_S)
    
        self.Crossover_Percentage = float(0.8)
        self.Mutation_Percentage = float(0.2)
        
        self._number_Offspringe = int(2*round((self.Crossover_Percentage*self.Population_Size)/2))
        self._number_Mutants = int(round(self.Mutation_Percentage*self.Population_Size))
        
        self.Population = np.array([Individual() for i in range(self.Population_Size)])
        
        self.sort(len(self.Population))
        self.list_fitness = [self.Population[i].fitness for i in range(self.Population_Size)]
        self.information = dict(
                Best_Individual = [self.Population[0].ind],
                Best_fitness = [self.Population[0].fitness],
                mean_fitness =list()
                )

    def main(self):
        for i in range(self.Max_Generation):
            Parent_Percentage= [math.exp(2*(k/np.max(self.list_fitness))) for k in self.list_fitness]
            Parent_Percentage = Parent_Percentage / np.sum(Parent_Percentage)
            pc = self.crossover(Parent_Percentage)
            if self.probably_mutation():
                pm = self.mutation()
                self.Population = np.concatenate((self.Population, pc,pm))
                del pc ,pm
            else:
                self.Population = np.concatenate((self.Population, pc))
                del pc

            self.sort(len(self.Population))

            self.Population = self.Population[:self.Population_Size+1]

            self.list_fitness = [self.Population[i].fitness for i in range(self.Population_Size)]
            self.information['Best_Individual'].append(self.Population[0].ind)
            self.information['Best_fitness'].append(self.Population[0].fitness)
            self.information['mean_fitness'].append(self.mean_fitness())
            self.show_Population(self.Population,7)
            print()

            
        #print(self.information['Best_Individual'][len(self.information['Best_Individual'])-1])
        self.showPlot()
    def sort(self,new_size):
        for i in range(new_size):
            for j in range(new_size-i-1):
                if self.Population[j]<self.Population[j+1]:
                    self.Population[j],self.Population[j+1] = self.Population[j+1] , self.Population[j]

    def probably_mutation(self):
        return np.random.rand() <= 0.2
    
    def mean_fitness(self):
        count=0
        for i in range(self.Population_Size):
            count= count+ self.Population[i].fitness
        count= count / self.Population_Size
        return count
    def show_Population(self,pop,s):
        for i in range(s):
            print(pop[i].ind,pop[i].fitness)
       
    def showPlot(self):
        g = [i for i in range(self.Max_Generation)]
        plt.plot(g, self.information['mean_fitness'], label='My Line')

        plt.title('Line Plot Example')
        plt.xlabel('Generation')
        plt.ylabel('Fitness')
        plt.legend()
        plt.show()
            
    def _doublePointCrossover(self,p1,p2):
        #nvar = len(p1) - 1 # or len(p2)
        position_cut = random.sample(range(1, len(p1)), 2)
        c1 = min(position_cut)
        c2 = max(position_cut)
        offspring1 = np.concatenate((p1[:c1],p2[c1:c2],p1[c2:]))
        offspring2 = np.concatenate((p2[:c1],p1[c1:c2],p2[c2:]))
        return list([offspring1,offspring2])
    def _singlePointCrossover(self,p1,p2):
        #nvar = len(p1) - 1 # or len(p2)
        position_cut = random.randint(1,len(p1))
        offspring1 = np.concatenate((p1[:position_cut],p2[position_cut:]))
        offspring2 = np.concatenate((p2[:position_cut],p1[position_cut:]))
        return list([offspring1,offspring2])
    def RoulettewheelSelection(self,p):
        random_i = np.random.rand()
        cumsum = np.cumsum(p)
        for i in cumsum:
            if random_i<=i:
                return np.where(cumsum == i)[0][0]    
    def crossover(self,p):
        Population_crossover = np.array([Individual() for i in range(self._number_Offspringe)])
        for i in range(0,self._number_Offspringe,2):
            
            rand_Individual_1 = self.RoulettewheelSelection(p)
            parent1 = self.Population[rand_Individual_1]
            
            rand_Individual_2 = self.RoulettewheelSelection(p)
            parent2 = self.Population[rand_Individual_2]
            
            r1= self._doublePointCrossover(parent1.ind, parent2.ind)

            Population_crossover[i].Set_Posision(r1[0])
            Population_crossover[i].Set_fitness()

            Population_crossover[i+1].Set_Posision(r1[1])
            Population_crossover[i+1].Set_fitness() 
       
        return Population_crossover
    def _mutants(self,p):
        position_mutants = np.random.randint(0,len(p))
        mutants = p.copy()
        mutants[position_mutants] = 1-p[position_mutants]
        return mutants
    def mutation(self):
        Population_mutation = np.array([Individual() for i in range(self._number_Mutants)])
        for i in range(self._number_Mutants):
            rand_Individual = np.random.randint(0,self.Population_Size,dtype = int)
            parent = self.Population[rand_Individual]
            Population_mutation[i].Set_Posision(self._mutants(parent.ind))
            Population_mutation[i].Set_fitness()
        return Population_mutation  
        
        
        
        
    
        
        
        