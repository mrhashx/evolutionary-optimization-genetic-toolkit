import time as tm
import numpy as np
import typing as typ
import matplotlib.pyplot as plt

class GA:
    def __init__(self,
                 MaxGeneration:int=100,
                 PopulationSize:int=100,
                 MatingFraction:float=0.1,
                 MutationFraction:int=0.2,
                 MutationProbability:float=0.1,
                 MutationScale:float=0.04):
        self.MaxGeneration = MaxGeneration
        self.PopulationSize = PopulationSize
        self.MatingFraction = MatingFraction
        self.MutationFraction = MutationFraction
        self.MutationProbability = MutationProbability
        self.MutationScale = MutationScale
        self.MatingCount = round(PopulationSize * MatingFraction)
        self.MutationCount = round(PopulationSize * MutationFraction)
        self.History = {'Best': [],
                        'Best F': [],
                        'Worst F': [],
                        'Average F': [],
                        'FEs': []}
    def GetFitnesses(self,
                     Population:np.ndarray) -> np.ndarray:
        Fitnesses = np.array([self.F(i, *self.Args) for i in Population])
        self.History['FEs'].extend(Fitnesses)
        return Fitnesses
    def Sort(self):
        I = np.argsort(self.Fitnesses)
        I = np.flip(I)
        self.Population = self.Population[I]
        self.Fitnesses = self.Fitnesses[I]
    def GetMutants(self) -> np.ndarray:
        if self.Fitnesses.var() > 1e-9:
            p = (self.Fitnesses - self.Fitnesses.min()) / (self.Fitnesses.max() - self.Fitnesses.min())
            p /= p.sum()
            I = np.random.choice(a=self.PopulationSize,
                                 size=self.MutationCount,
                                 p=p)
        else:
            I = np.random.choice(a=self.PopulationSize,
                                 size=self.MutationCount)
        newP = self.Population[I]
        for i in range(self.MutationCount):
            for j in range(self.DimensionCount):
                if np.random.rand() < self.MutationProbability:
                    newP[i, j] += np.random.uniform(low=-self.MutationScales[j],
                                                    high=+self.MutationScales[j])
            Mask1 = newP[i] > self.UB
            Mask2 = newP[i] < self.LB
            newP[i, Mask1] = self.UB[Mask1]
            newP[i, Mask2] = self.LB[Mask2]
        return newP
    def GetChilds(self) -> np.ndarray:
        if self.Fitnesses.var() > 1e-9:
            p = (self.Fitnesses - self.Fitnesses.min()) / (self.Fitnesses.max() - self.Fitnesses.min())
            p /= p.sum()
            I = np.random.choice(a=self.PopulationSize,
                                 size=2 * self.MatingCount,
                                 p=p)
        else:
            I = np.random.choice(a=self.PopulationSize,
                                 size=2 * self.MatingCount)
        I1s = I[:self.MatingCount]
        I2s = I[self.MatingCount:]
        newP1 = np.zeros((self.MatingCount, self.DimensionCount))
        newP2 = np.zeros((self.MatingCount, self.DimensionCount))
        for i, (i1, i2) in enumerate(zip(I1s, I2s)):
            for j in range(self.DimensionCount):
                if np.random.rand() < 0.5:
                    newP1[i, j] = self.Population[i1, j]
                    newP2[i, j] = self.Population[i2, j]
                else:
                    newP1[i, j] = self.Population[i2, j]
                    newP2[i, j] = self.Population[i1, j]
        newP = np.vstack((newP1, newP2))
        return newP
    def Append(self,
               Ps:list):
        Fs = [self.GetFitnesses(i) for i in Ps]
        self.Population = np.vstack([self.Population] + Ps)
        self.Fitnesses = np.hstack([self.Fitnesses] + Fs)
    def Cut(self):
        self.Population = self.Population[:self.PopulationSize]
        self.Fitnesses = self.Fitnesses[:self.PopulationSize]
    def Maximize(self,
                 F:typ.Callable,
                 LB:np.ndarray,
                 UB:np.ndarray,
                 Args:tuple=()) -> dict:
        self.F = F
        self.LB = LB
        self.UB = UB
        self.Args = Args
        self.DimensionCount = LB.size
        self.MutationScales = self.MutationScale * (self.UB - self.LB) / 2
        self.Population = np.random.uniform(low=self.LB,
                                            high=self.UB,
                                            size=(self.PopulationSize,
                                                  self.DimensionCount))
        self.Fitnesses = self.GetFitnesses(self.Population)
        self.Sort()
        self.History['Best'].append(self.Population[0])
        self.History['Best F'].append(self.Fitnesses[0])
        self.History['Worst F'].append(self.Fitnesses[-1])
        self.History['Average F'].append(self.Fitnesses.mean())
        print('Generation 0 Best: {:.2f}'.format(self.Fitnesses[0]))
        for i in range(self.MaxGeneration):
            M = self.GetMutants()
            C = self.GetChilds()
            self.Append([M, C])
            self.Sort()
            self.Cut()
            self.History['Best'].append(self.Population[0])
            self.History['Best F'].append(self.Fitnesses[0])
            self.History['Worst F'].append(self.Fitnesses[-1])
            self.History['Average F'].append(self.Fitnesses.mean())
            print('Generation {} Best: {:.2f}'.format(i + 1, self.Fitnesses[0]))
        for k, v in self.History.items():
            self.History[k] = np.array(v)
        return self.History

def SMA(S:np.ndarray,
        L:int) -> np.ndarray:
    nD0 = S.size # Getting Input Series Size
    nD = nD0 - L + 1 # Calculating Output Series Size
    M = np.zeros(nD) # Creating Placeholder Array
    for i in range(nD): # For Each Output Data
        M[i] = S[i:i + L].mean() # Mean Over Window
    return M

def F(x:np.ndarray) -> float:
    y = (np.exp(-np.power(x, 2))).sum()
    return y

np.random.seed(0)
plt.style.use('ggplot')

LB = -2 * np.ones(10)
UB = +2 * np.ones(10)

t1 = tm.time()

Algorithm = GA()

History = Algorithm.Maximize(F, LB, UB)

t2 = tm.time()

dt = t2 - t1

print(f'Total Time: {dt:.4f} Seconds')

plt.figure(figsize=(14, 9))
plt.plot(History['FEs'],
         ls='-',
         lw=0.8,
         c='crimson',
         label='Function Evaluations')
plt.title('Function Value Over Evaluations')
plt.xlabel('Function Evaluation')
plt.ylabel('Value')
plt.savefig('Figure 1.png', dpi=384)
plt.show()

plt.figure(figsize=(14, 9))
plt.plot(History['Best F'],
         ls='--',
         lw=1.1,
         c='teal',
         label='Best')
plt.plot(History['Average F'],
         ls='-',
         lw=0.9,
         c='k',
         label='Average')
plt.plot(History['Worst F'],
         ls='--',
         lw=1.1,
         c='crimson',
         label='Worst')
plt.title('Best Function Value Over Generations')
plt.xlabel('Generation')
plt.ylabel('Value')
plt.legend()
plt.savefig('Figure 2.png', dpi=384)
plt.show()


smaFEs = SMA(History['FEs'], 100)

T1 = np.arange(start=0,
               stop=History['FEs'].size,
               step=1)
T2 = T1[-smaFEs.size:]

plt.figure(figsize=(14, 9))
plt.plot(T1,
         History['FEs'],
         ls='-',
         lw=0.8,
         c='crimson',
         label='Function Evaluations')
plt.plot(T2,
         smaFEs,
         ls='-',
         lw=1.3,
         c='k',
         label='SMA(100)')
plt.title('Function Value Over Evaluations + SMA(100)')
plt.xlabel('Function Evaluation')
plt.ylabel('Value')
plt.savefig('Figure 3.png', dpi=384)
plt.show()

Bests = History['Best']

D = Bests - np.zeros(10)

D2 = D ** 2

SD2 = np.sum(D2, axis=1)

Distances = np.sqrt(SD2)

plt.figure(figsize=(14, 9))
plt.plot(Distances,
         ls='-',
         lw=0.8,
         c='crimson',
         label='Distance')
plt.title('Generation\'s Best Solution Distance From Target Solution')
plt.xlabel('Generation')
plt.ylabel('Distance')
plt.savefig('Figure 4.png', dpi=384)
plt.show()

plt.figure(figsize=(14, 9))
plt.plot(Distances,
         ls='-',
         lw=0.8,
         c='crimson',
         label='Distance')
plt.title('Generation\'s Best Solution Distance From Target Solution')
plt.xlabel('Generation')
plt.ylabel('Distance')
plt.yscale('log')
plt.savefig('Figure 5.png', dpi=384)
plt.show()

BestSolution = History['Best'][-1]

print(np.round(BestSolution, decimals=4))
