#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  1 15:38:50 2020

@author: Justin
"""

ccs = list((local.subgraph(c) for c in nx.connected_components(local)))

# Helper function to be used in the below plot method --------------------------
def find_severity_household_infection(final_status_dict):
    num_infect_dict = dict()
    num_not_infect_dict = dict()
    for cc_dex in list(range(len(ccs))):
        nodes_of_cc = ccs[cc_dex].nodes()
        num_infect = 0
        num_not_infect = 0
        for node in nodes_of_cc:
            status_of_node = final_status_dict[node]
            if status_of_node == 'R':
                num_infect += 1
            else:
                num_not_infect += 1
        num_infect_dict[cc_dex] = num_infect
        num_not_infect_dict[cc_dex] = num_not_infect
    return [num_infect_dict, num_not_infect_dict]

def plot_final_status(final_status_dict_list):
    num_infect_dict_list = list()
    num_not_infect_dict_list = list()
    for sim_num in list(range(len(final_status_dict_list))):
        returned = find_severity_household_infection(final_status_dict_list[sim_num])
        num_infect_dict_list.append(returned[0])
        num_not_infect_dict_list.append(returned[1])
    
    # Current inefficiency in that not all simulations are plotted -------------
    num_infect_dict = num_infect_dict_list[0]
    num_not_infect_dict = num_not_infect_dict_list[0]

    # Order by size of connected component -------------------------------------
    to_plot_infect = list()
    to_plot_not_infect = list()
    for cc_dex in list(range(len(ccs))):
        to_plot_infect.append(num_infect_dict[cc_dex])
        to_plot_not_infect.append(num_not_infect_dict[cc_dex])

    ind = np.arange(len(ccs))
    width = 0.35
    
    p1 = plt.bar(ind, to_plot_infect, width)
    p2 = plt.bar(ind, to_plot_not_infect, width, bottom=to_plot_infect)
    
    plt.xlabel('household number')
    plt.ylabel('# individuals in household')
    plt.title('infection severity by household')
    plt.yticks(np.arange(0, 18, 10))
    plt.legend((p1[0], p2[0]), ('infected', 'not infected'))

    if not (path.exists(directory_plots)):
        os.mkdir(directory_plots)

    file_name = directory_plots + 'infection_severity.png'
    plt.savefig(file_name, dpi=500)
    plt.clf()

plot_final_status(final_status_EQ)