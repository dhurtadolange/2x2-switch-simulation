import numpy as np
import pandas
import matplotlib.pyplot as plt
import csv
import math

# File to save the data
server = False
#v = '3'
case_file_list = ['C3-9', 'C5-9', 'C1-10']
epsilon_dict = {'C1-10': 0.01, 'C3-9': 0.05, 'C5-9': 0.1}

#v_list = ['0', '3', '4']
v_list = ['4']

for v in v_list:
    print('v',v)
    # if server:
    #     file = open('Mean_and_std_dev_of_variables-v{}.csv'.format(v), "w")
    # else:
    #     file = open('0Simulation cases server/Mean_and_std_dev_of_variables-v{}.csv'.format(v), "w")

    with open('Mean-and-variance-v{}.csv'.format(v), 'w') as file_mean:
        writer_mean = csv.writer(file_mean)

        for case_file in case_file_list:
            writer_mean.writerow("--- Case {} ---".format(case_file))
            print(case_file)

            epsilon = epsilon_dict[case_file]

            if server:
                Q_all = pandas.read_csv('Q_{}-v{}.csv'.format(case_file), header=None)
                U_all = pandas.read_csv('U_{}-v{}.csv'.format(case_file), header=None)
            else:
                Q_all = pandas.read_csv('0Simulation cases server/Q_{}-v{}.csv'.format(case_file,v), header=None)
                U_all = pandas.read_csv('0Simulation cases server/U_{}-v{}.csv'.format(case_file,v), header=None)

            Q = pandas.DataFrame(Q_all[:][-2*10 ** 6::]).to_numpy()
            U = pandas.DataFrame(U_all[:][-2*10 ** 6::]).to_numpy()
            n = len(Q)

            #############################
            ### Plot running average ####
            #############################

            # Initialize mean value of all variables
            q1 = 0
            q2 = 0
            q3 = 0
            q4 = 0
            q1u2 = 0
            q1u3 = 0
            q2u1 = 0
            q2u3 = 0
            q2u4 = 0
            q3u1 = 0
            q3u2 = 0
            q3u4 = 0

            # Initialize running average of all queue lengths
            sum1 = []
            sum2 = []
            sum3 = []
            sum4 = []

            for i in range(n):
                # Running average
                if i == 0:
                    sum1.append(Q[i][0])  # [col][row]
                    sum2.append(Q[i][1])
                    sum3.append(Q[i][2])
                    sum4.append(Q[i][3])
                else:
                    sum1.append((i * sum1[i - 1] + Q[i][0]) / (i + 1))
                    sum2.append((i * sum2[i - 1] + Q[i][1]) / (i + 1))
                    sum3.append((i * sum3[i - 1] + Q[i][2]) / (i + 1))
                    sum4.append((i * sum4[i - 1] + Q[i][3]) / (i + 1))

                # Mean of each variable
                q1 = q1 + Q[i][0]
                q2 = q2 + Q[i][1]
                q3 = q3 + Q[i][2]
                q4 = q4 + Q[i][3]
                q1u2 = q1u2 + Q[i][0] * U[i][1]
                q1u3 = q1u3 + Q[i][0] * U[i][2]
                q2u1 = q2u1 + Q[i][1] * U[i][0]
                q2u3 = q2u3 + Q[i][1] * U[i][2]
                q2u4 = q2u4 + Q[i][1] * U[i][3]
                q3u1 = q3u1 + Q[i][2] * U[i][0]
                q3u2 = q3u2 + Q[i][2] * U[i][1]
                q3u4 = q3u4 + Q[i][2] * U[i][3]


            # Plot running average
            p1, = plt.plot(sum1, label='Queue 1')
            p2, = plt.plot(sum2, label='Queue 2')
            p3, = plt.plot(sum3, label='Queue 3')
            p4, = plt.plot(sum4, label='Queue 4')
            plt.legend(handles=[p1, p2, p3, p4])
            plt.ylabel('Average of queue lengths')
            plt.savefig('0Simulation cases server/RunningAvg_Individual_case{}_v{}.png'.format(case_file,v))
            plt.show()

            # Compute mean
            mean_q1 = q1 / n
            mean_q2 = q2 / n
            mean_q3 = q3 / n
            mean_q4 = q4 / n

            q1 = epsilon * q1 / n
            q2 = epsilon * q2 / n
            q3 = epsilon * q3 / n
            q4 = epsilon * q4 / n
            q1u2 = q1u2 / n
            q1u3 = q1u3 / n
            q2u1 = q2u1 / n
            q2u3 = q2u3 / n
            q2u4 = q2u4 / n
            q3u1 = q3u1 / n
            q3u2 = q3u2 / n
            q3u4 = q3u4 / n

            # mean_and_variance_dict = {}
            # mean_and_variance_dict['mean-Q1'] = q1
            # mean_and_variance_dict['mean-Q2'] = q2
            # mean_and_variance_dict['mean-Q3'] = q3
            # mean_and_variance_dict['mean-Q4'] = q4
            # mean_and_variance_dict['mean-Q1U2'] = q1u2
            # mean_and_variance_dict['mean-Q1U3'] = q1u3
            # mean_and_variance_dict['mean-Q2U1'] = q2u1
            # mean_and_variance_dict['mean-Q2U3'] = q2u3
            # mean_and_variance_dict['mean-Q2U4'] = q2u4
            # mean_and_variance_dict['mean-Q3U1'] = q3u1
            # mean_and_variance_dict['mean-Q3U2'] = q3u2
            # mean_and_variance_dict['mean-Q3U4'] = q3u4

            writer_mean.writerow("Mean:")
            writer_mean.writerow("Q1 = {}".format(q1))
            writer_mean.writerow("Q2 = {}".format(q2))
            writer_mean.writerow("Q3 = {}".format(q3))
            writer_mean.writerow("Q4 = {}".format(q4))
            writer_mean.writerow("Q1U2 = {}".format(q1u2))
            writer_mean.writerow("Q1U3 = {}".format(q1u3))
            writer_mean.writerow("Q2U1 = {}".format(q2u1))
            writer_mean.writerow("Q2U3 = {}".format(q2u3))
            writer_mean.writerow("Q2U4 = {}".format(q2u4))
            writer_mean.writerow("Q3U1 = {}".format(q3u1))
            writer_mean.writerow("Q3U2 = {}".format(q3u2))
            writer_mean.writerow("Q3U4 = {}".format(q3u4))

            # file.write("Mean:\n")
            # file.write("Q1 = {}\n".format(q1))
            # file.write("Q2 = {}\n".format(q2))
            # file.write("Q3 = {}\n".format(q3))
            # file.write("Q4 = {}\n".format(q4))
            # file.write("Q1U2 = {}\n".format(q1u2))
            # file.write("Q1U3 = {}\n".format(q1u3))
            # file.write("Q2U1 = {}\n".format(q2u1))
            # file.write("Q2U3 = {}\n".format(q2u3))
            # file.write("Q2U4 = {}\n".format(q2u4))
            # file.write("Q3U1 = {}\n".format(q3u1))
            # file.write("Q3U2 = {}\n".format(q3u2))
            # file.write("Q3U4 = {}\n".format(q3u4))

            # Compute standard deviation of q1, q2, q3 and q4

            sd_q1 = 0
            sd_q2 = 0
            sd_q3 = 0
            sd_q4 = 0
            sd_q2q3 = 0  # Standard deviation of q2+q3

            for i in range(n):
                sd_q1 = sd_q1 + (Q[i][0] - mean_q1) ** 2
                sd_q2 = sd_q2 + (Q[i][1] - mean_q2) ** 2
                sd_q3 = sd_q3 + (Q[i][2] - mean_q3) ** 2
                sd_q4 = sd_q4 + (Q[i][3] - mean_q4) ** 2
                sd_q2q3 = sd_q2q3 + (Q[i][1] + Q[i][2] - mean_q2 - mean_q3) ** 2

            sd_q1 = epsilon * np.sqrt(sd_q1 / (n - 1))
            sd_q2 = epsilon * np.sqrt(sd_q2 / (n - 1))
            sd_q3 = epsilon * np.sqrt(sd_q3 / (n - 1))
            sd_q4 = epsilon * np.sqrt(sd_q3 / (n - 1))
            sd_q2q3 = epsilon * np.sqrt(sd_q2q3 / (n - 1))

            writer_mean.writerow("----------------------------------")
            writer_mean.writerow("Standard deviation:")
            writer_mean.writerow("SD Q1 = {}".format(sd_q1))
            writer_mean.writerow("SD Q2 = {}".format(sd_q2))
            writer_mean.writerow("SD Q3 = {}".format(sd_q3))
            writer_mean.writerow("SD Q4 = {}".format(sd_q4))
            writer_mean.writerow("SD Q2+Q3 = {}".format(sd_q2q3))

            # file.write("----------------------------------\n")
            # file.write("Standard deviation:\n")
            # file.write("SD Q1 = {}\n".format(sd_q1))
            # file.write("SD Q2 = {}\n".format(sd_q2))
            # file.write("SD Q3 = {}\n".format(sd_q3))
            # file.write("SD Q4 = {}\n".format(sd_q4))
            # file.write("SD Q2+Q3 = {}\n\n\n".format(sd_q2q3))