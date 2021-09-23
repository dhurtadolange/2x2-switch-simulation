### Simulation ###
### Suppose Bernoulli arrivals ###

import numpy as np
import csv

transient = 0.95 #Percentage of the simulation to delete

# Possible schedules
s1 = np.array([1,0,0,1])
s2 = np.array([0,1,1,0])

for case in range(1,2):
    if case == 1:
        epsilon = 0.01
        v_lambda = np.array([(1-epsilon)/2, (1-epsilon)/2, (1-epsilon)/2, (1-epsilon)/2]) # Vector of mean arrival rates
        K = 5*10**9 # Number of time slots to simulate
    elif case == 2:
        epsilon = 0.01
        v_lambda = np.array([(1-epsilon)*3/4, (1-epsilon)/4, (1-epsilon)/4, (1-epsilon)*3/4]) # Vector of mean arrival rates
        K = 5*10**8 # Number of time slots to simulate
    elif case == 3:
        epsilon = 0.05
        v_lambda = np.array([(1-epsilon)/2, (1-epsilon)/2, (1-epsilon)/2, (1-epsilon)/2]) # Vector of mean arrival rates
        K = 2*10**8 # Number of time slots to simulate
    elif case == 4:
        epsilon = 0.05
        v_lambda = np.array([(1-epsilon)*3/4, (1-epsilon)/4, (1-epsilon)/4, (1-epsilon)*3/4]) # Vector of mean arrival rates
        K = 2*10**8 # Number of time slots to simulate
    elif case == 5:
        epsilon = 0.1
        v_lambda = np.array([(1-epsilon)/2, (1-epsilon)/2, (1-epsilon)/2, (1-epsilon)/2]) # Vector of mean arrival rates
        K = 2*10**8 # Number of time slots to simulate
    elif case == 6:
        epsilon = 0.1
        v_lambda = np.array([(1-epsilon)*3/4, (1-epsilon)/4, (1-epsilon)/4, (1-epsilon)*3/4]) # Vector of mean arrival rates
        K = 2*10**8 # Number of time slots to simulate

    q_current = np.array([0,0,0,0])
    u = np.array([0,0,0,0])

    # Vector of variances
    v_var = np.zeros(4)

    for i in range(4):
        v_var[i] = v_lambda[i]*(1-v_lambda[i])

    print("Case {}".format(case))
    print("Variance vector {}".format(v_var))


    with open('Q_case{}.csv'.format(case),'w') as file_Q, open('U_case{}.csv'.format(case),'w') as file_U:
        writerQ = csv.writer(file_Q)
        writerU = csv.writer(file_U)
        ### Simulation ###
        for k in range(K-1):
            q_previous = q_current
            u = np.array([0,0,0,0])
            if np.mod(k,10**6)==0:
                print("Case {}".format(case))
                print(k/(10**6))

            # Solve scheduling problem using MaxWeight algorithm
            s = np.zeros(4)
            w1 = np.dot(s1,q_previous)
            w2 = np.dot(s2,q_previous)
            if w1>w2:
                s = s1
            elif w2>w1:
                s = s2
            else: # break ties at random
                r = np.random.uniform(0,1)
                if r<0.5:
                    s = s1
                else:
                    s = s2
            # End scheduling

            # Generate arrivals
            a = np.zeros(4)
            for i in range(4):
                a[i] = np.random.binomial(1,v_lambda[i])

            # Update queue lenghts
            aux_q = q_previous+a-s
            for i in range(4):
                if aux_q[i]<0:
                    u[i] = -aux_q[i]
                    q_current[i] = 0
                else:
                    q_current[i] = aux_q[i]
            #print("Schedule {}".format(s))
            #print("Unused service {}".format(U_all[k]))
            #print("Queue lengths {}".format(Q_all[k+1]))
            if k >= transient*K-1: # Save only what we believe is the steady-state
                writerQ.writerow(q_current)
                writerU.writerow(u)
