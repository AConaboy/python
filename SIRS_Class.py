import copy
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
from scipy import ndimage
import warnings
import random

class SIRS():
    def __init__(self,p1,lattice_size=50):
        '''
        p1 is probability of S=>I,
        p2 is probability of I=>R
        p3 is probability of R=>S
        '''
        self.lattice_size=lattice_size
        self.p1=p1
        #self.p2=p2
        #self.p3=p3
        self.N=int(lattice_size**2)

        # See comments for what initial lattice to use - please comment out the OTHER type of initial lattice

        #self.lattice=np.random.choice([-1,1],size=(lattice_size,lattice_size)) # Lattice for parts a-d
        self.lattice=np.full((lattice_size, lattice_size), -1) # Lattice for part e
        self.lattice[np.random.randint(0, lattice_size), np.random.randint(0, lattice_size)] = 1

    def RandPoint(self):
        '''
        Generates a random coordinate
        within the lattice
        '''
        x=np.random.randint(0,self.lattice_size)
        y=np.random.randint(0,self.lattice_size)
        return (x,y)

    def FindNN(self,x,y):
        '''
        Finds the nearest neighbours of
        randomly pick spin at coordinate x,y
        '''
        nn_xl=(x-1)%self.lattice_size
        nn_xr=(x+1)%self.lattice_size
        nn_yu=(y+1)%self.lattice_size
        nn_yd=(y-1)%self.lattice_size
        nn = [[nn_xl,y], [nn_xr,y], [x,nn_yu], [x,nn_yd]]
        return nn

    @staticmethod
    def Acceptor(p):
        '''
        Static method to allow
        for probability calculations
        '''
        a=np.random.uniform(0,1)
        if p>a:return 1
        else: return 0

    def Rules(self,x,y,random_x, random_y):
        '''
        Infected/active: 1
        healthy/inactive: -1
        '''
        #Counter takes in the list of nearest neighbours so that number of alive neighbours can be counted
        if self.lattice[x,y]==1:
            if self.lattice[random_x, random_y]== -1 and SIRS.Acceptor(self.p1)==True:
                 self.lattice[random_x, random_y] = 1
            if SIRS.Acceptor(1-self.p1)==True:
                self.lattice[x,y]=-1
        else:
            pass
        # cnt=Counter(nnList)
        # if self.lattice[x,y]== -1 and cnt[0]>=1 and SIRS.Acceptor(self.p1)==True:
        #     self.lattice[x,y]=0
        # elif self.lattice[x,y]==0 and SIRS.Acceptor(self.p2)==True:
        #     self.lattice[x,y]=1
        # elif self.lattice[x,y]==1 and SIRS.Acceptor(self.p3)==True:
        #     self.lattice[x,y]=-1

    def Update(self):
        x,y = self.RandPoint()
        nn = self.FindNN(x,y)
        choices_indices = np.random.choice(len(nn))
        random_nn = nn[choices_indices]
        random_x = random_nn[0]
        random_y = random_nn[1]
        #print(x, y, random_x, random_y)
        self.Rules(x,y,random_x, random_y)
        return self.lattice

    def fraction_of_sites(self):
        infected = 0
        for i in range(self.lattice_size):
            for j in range(self.lattice_size):
                if self.lattice[i,j] == 1:
                    infected+=1
        infected_fraction = infected/self.N
        return infected_fraction, (1-infected_fraction)

    def Get_Variance(self,vals,vals_sq):
        av_vals=np.mean(vals)
        av_vals_sq=np.mean(vals_sq)
        variance=(av_vals_sq - av_vals**2. )/self.N
        return variance

    def survival_check():
        infected = 0
        for i in range(self.lattice_size):
            for j in range(self.lattice_size):
                if self.lattice[i, j] == 1:
                    infected += 1
        return infected


    # def FracImmune(self,fraction):
    #     '''
    #     Immune: 2
    #     randomly selects points in the
    #     lattice to become immune until
    #     a passed in fraction has been
    #     converted to have immunity
    #     '''
    #     indices=[]
    #     L=list(range(self.lattice_size))
    #     while len(indices)<int(self.N*fraction):
    #         x=random.choice(L)
    #         y=random.choice(L)
    #         item=[x,y]
    #         if item not in indices:
    #             indices.append(item)
    #     for i in indices:
    #         self.lattice[i[0],i[1]]=2
