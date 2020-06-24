import os
import sys
import time
import copy
import pickle
import numpy as np
from datetime import date
import matplotlib.pyplot as plt
from collections import Counter
from ClassAnimatorSIRS import Animator
from SIRS_Class import SIRS as sirsc
import matplotlib.animation as animation
from multiprocessing import Queue, Process
from matplotlib.animation import FuncAnimation
import pandas

def main():
    '''
    Run code in following format:
    python3 <SIRS_Main.py><lattice_size><p1><p2><p3><number of sweeps><mode><state>
    '''
    #Take in sys arguments
    lattice_size=int(sys.argv[1])
    p1=float(sys.argv[2])
    sweeps=int(sys.argv[3])
    mode=str(sys.argv[4])

###############################################################################

    #Contour method of visulisation (worse method, runs in parallel though)
    if mode=='vis':
        sirs=sirsc(p1,lattice_size)
        lattice=sirs.lattice
        #Initiates a Queue to hold different lattices to be animated
        lattice_queue = Queue()
        lattice_queue.put( (copy.deepcopy(lattice)) )       #Copies the first random lattice to the queue
        animator = Animator(lattice_queue,sweeps)                  #Instances and initiates the Animator class
        animator_proc = Process(target=animator.animate)    #Sets up a process with animate as the target
        animator_proc.start()
        #Sweeps through the update rules for the lattice
        for i in range(sweeps):
            for j in range(sirs.N):
                sirs.Update()
            lattice_queue.put( copy.deepcopy(sirs.lattice) )         #copies new lattice to Queue to be animated
################################################################################
    elif mode == 'b':
        sirs=sirsc(p1,lattice_size)
        lattice=sirs.lattice
        infected_list = []
        healthy_list = []
        time_list = []
        for i in range(sweeps):
            if i>=100 and i%100 == 0:
                infected_list.append(sirs.fraction_of_sites()[0])
                healthy_list.append(sirs.fraction_of_sites()[1])
                time_list.append(i)
            for j in range(sirs.N):
                sirs.Update()

        dfInfected = pandas.DataFrame(infected_list)
        dfInfected.to_csv('infectedlist_partb.csv', index=False, header=False)
        dfHealthy = pandas.DataFrame(healthy_list)
        dfHealthy.to_csv('healthylist_partb.csv', index=False, header=False)

        plt.plot(time_list, infected_list)
        plt.ylabel('infected fraction')
        plt.xlabel('sweep')
        plt.show()
        plt.plot(time_list, healthy_list)
        plt.xlabel('sweep')
        plt.ylabel('healthy fraction')
        plt.show()

    elif mode == 'c':
        p = np.arange(0.55, 0.7, 0.005)
        sweeps=500
        average_infected_fraction = []
        average_healthy_fraction = []
        for p_val in p:
            sirs=sirsc(p_val,lattice_size)
            lattice=sirs.lattice
            print(p_val)
            infected_list=[]
            healthy_list=[]
            for i in range(sweeps):
                if i>=50 and i%50 == 0:
                    infected_list.append(sirs.fraction_of_sites()[0])
                    healthy_list.append(sirs.fraction_of_sites()[1])
                for j in range(sirs.N):
                    sirs.Update()
            average_infected_fraction.append(np.mean(infected_list))
            average_healthy_fraction.append(np.mean(healthy_list))

        dfAvgInfectedList = pandas.DataFrame(average_infected_fraction)
        dfAvgInfectedList.to_csv('AvgInfectedList_partc.csv', index=False, header=False)

        dfAvgHealthyList = pandas.DataFrame(average_healthy_fraction)
        dfAvgHealthyList.to_csv('dfAvgHealthyList_partc.csv', index=False, header=False)

        plt.plot(p, average_infected_fraction)
        plt.ylabel('average infected fraction')
        plt.xlabel('value of p')
        plt.show()
        plt.plot(p, average_healthy_fraction)
        plt.xlabel('value of p')
        plt.ylabel('average healthy fraction')
        plt.show()

    elif mode == 'd':
        p = np.arange(0.55, 0.7, 0.005)
        sweeps=500
        infected_variance_fraction = []
        healthy_variance_fraction = []

        for p_val in p:
            sirs=sirsc(p_val,lattice_size)
            lattice=sirs.lattice

            infected_cells=[]
            infected_cells_sq=[]

            healthy_cells=[]
            healthy_cells_sq=[]

            for i in range(sweeps):
                if i>=50 and i%50 == 0:
                    infected_cells.append(sirs.fraction_of_sites()[0]*sirs.N)
                    infected_cells_sq.append((sirs.fraction_of_sites()[0]*sirs.N)**2)
                    healthy_cells.append(sirs.fraction_of_sites()[1]*sirs.N)
                    healthy_cells_sq.append((sirs.fraction_of_sites()[1]*sirs.N)**2)
                for j in range(sirs.N):
                    sirs.Update()

            infected_variance_fraction.append(sirs.Get_Variance(infected_cells, infected_cells_sq))
            healthy_variance_fraction.append(sirs.Get_Variance(healthy_cells, healthy_cells_sq))
            print(p_val)

        dfInfVarianceList = pandas.DataFrame(infected_variance_fraction)
        dfInfVarianceList.to_csv('infected_variance_fraction.csv', index=False, header=False)

        dfHealthyVarianceList = pandas.DataFrame(healthy_variance_fraction)
        dfHealthyVarianceList.to_csv('healthy_variance_fraction.csv', index=False, header=False)

        plt.plot(p, infected_variance_fraction)
        plt.ylabel('infected variance fraction')
        plt.xlabel('value of p')
        plt.show()
        plt.plot(p, healthy_variance_fraction)
        plt.xlabel('value of p')
        plt.ylabel('healthy variance fraction')
        plt.show()

    elif mode == 'e':
        simulations = 500
        num_infected_sites=[]
        time_list=[]
        for sim in range(simulations):
            sirs=sirsc(p_val,lattice_size)
            lattice=sirs.lattice
            for i in range(sweeps):
                if i>=50 and i%50 == 0:
                    no_infected_sites.append(sirs.survival_check())
                    time_list.append(i)
                for j in range(sirs.N):
                    sirs.Update()

        dfsurvivalprob = pandas.DataFrame(num_infected_sites)
        dfsurvivalprob.to_csv('survival_prob.csv', index=False, header=False)

        plt.scatter(time_list, num_infected_sites)
        plt.xlabel('sweep')
        plt.ylabel('number of infected sites')
        plt.show()

    elif mode == 'f':
        simulations = 500
        sweeps=300
        num_infected_sites_600 = [] # Empty lists for number of infected states for p = 0.600
        num_infected_sites_625 = [] # for p = 0.625
        num_infected_sites_650 = [] # for p = 0.650
        time_list = np.arange(50, 250, 50)
        p = np.array([0.600, 0.625, 0.650])
        for p_val in p:
            sirs=sirsc(p_val,lattice_size)
            lattice=sirs.lattice
            for i in range(sweeps):
                if i>=50 and i%50 == 0:
                    if p_val == 0.600:
                        num_infected_sites_600.append(sirs.survival_check())
                    elif p_val == 0.625:
                        num_infected_sites_625.append(sirs.survival_check())
                    else:
                        num_infected_sites_650.append(sirs.survival_check())
                for j in range(sirs.N):
                    sirs.Update()

        df_surv_prob_600 = pandas.DataFrame(num_infected_sites_600)
        df_surv_prob_600.to_csv('part_f_surv_prob_600.csv', index=False, header=False)
        df_surv_prob_625 = pandas.DataFrame(num_infected_sites_625)
        df_surv_prob_625.to_csv('part_f_surv_prob_625.csv', index=False, header=False)
        df_surv_prob_650 = pandas.DataFrame(num_infected_sites_650)
        df_surv_prob_650.to_csv('part_f_surv_prob_650.csv', index=False, header=False)

        plt.loglog(time_list, num_infected_sites_600)
        plt.xlabel('log sweeps')
        plt.ylabel('log survival prob')
        plt.title('log log plot of survival prob for p=0.600')
        plt.show()

        plt.loglog(time_list, num_infected_sites_625)
        plt.xlabel('log sweeps')
        plt.ylabel('log survival prob')
        plt.title('log log plot of survival prob for p=0.625')
        plt.show()

        plt.loglog(time_list, num_infected_sites_650)
        plt.xlabel('log sweeps')
        plt.ylabel('log survival prob')
        plt.title('log log plot of survival prob for p=0.650')
        plt.show()


if __name__=='__main__':
    main()
