
import numpy as np
import math
import matplotlib.pyplot as plt

from constants.constants import *
from neural.syn import *
from neural.neuron import *
from neural.predefined_models import *

class adj_matrix(object):

    def __init__(self, neurons, synapses, neuron_names):
        self.neurons = neurons
        self.neuron_names = neuron_names
        self.synapse_matrix = np.empty((neurons.size, neurons.size),
            dtype = object)

        # fill in synapse matrix
        for synapse_list in synapses:
            i = self.neuron_names.index(synapse_list.n_from)
            j = self.neuron_names.index(synapse_list.n_to)
            self.synapse_matrix[i][j] = synapse_list

    def simulate(self): # update voltages for neurons
        global V_t
        t = (self.neurons[0].t) # retrieve time window
        for tj in range(1, t.size):
            for ni in range(self.neurons.size):
                self.neurons[ni].next_v(tj)
                if self.neurons[ni].v[tj] >= V_t:
                    # check adjacency matrix for synapses to send out
                    for n_to in range(0, self.neurons.size):
                        if self.synapse_matrix[ni][n_to] is not None:
                            for syn in self.synapse_matrix[ni][n_to].synapses:
                                self.synapse_prop(syn, n_to, tj)

    def synapse_prop(self, syn, n_to, tj):
        global T_TO_POS

        t_delay = tj + int(T_TO_POS * (syn.s_delay + T_neu))

        if syn.s_type is "V":
            self.neurons[n_to].v[t_delay] += syn.s_weight
        elif syn.s_type is "g_e":
            self.neurons[n_to].g_e[t_delay] += syn.s_weight
        elif syn.s_type is "g_f":
            self.neurons[n_to].g_f[t_delay] += syn.s_weight
        else: # gate synapse
            if syn.s_weight is 1:
                self.neurons[n_to].gate[t_delay] = 1
            elif syn.s_weight is -1:
                self.neurons[n_to].gate[t_delay] = 0
            else:
                pass # throw error

def plot_v(neurons):

    f, axarr = plt.subplots(neurons.size, 1, figsize=(15,10), squeeze=False)
    for i in range(neurons.size):
        axarr[i,0].plot(neurons[i].t, neurons[i].v)
        axarr[i,0].set_title('voltage for ' + neurons[i].ID)
    plt.setp([a.get_xticklabels() for a in axarr[:,0]], visible = False)
    plt.setp([axarr[neurons.size - 1,0].get_xticklabels()], visible = True)
    plt.show()

def initialize_neurons(neuron_names, t, data = None):
    '''initialize neurons with some data, if necessary'''

    neurons = np.asarray([neuron(label, t) for label in neuron_names])

    # setting stimuli spikes
    if data is not None:
        for key, value in data.items(): # for each neuron
            for j in list(value):
                neurons[neuron_names.index(key)].v[j] = V_t

    return(neurons)

def simulate_neurons(f_name, data = {}):
    '''implementation of a neural model'''

    f_p = functions[f_name] # parameters

    # time frame & neurons
    t = np.multiply(TO_MS, np.arange(0, f_p["t"], 1e-4)) # time in MS
    neurons = initialize_neurons(
        f_p["neuron_names"], t, data)

    # initial adjacency matrix (without subnets)
    syn_matrix = adj_matrix(neurons, f_p["synapses"], f_p["neuron_names"])

    # augmented adjacency matrix (with subnets)
    if "subnets" in f_p: # model supports subnets?
        for subnet in f_p["subnets"]:

            subnet_names = subnet["neuron_names"]

            curr_offset = (syn_matrix.synapse_matrix).shape[0]
            new_sze = len(subnet_names) + curr_offset

            # neurons
            subnet_neurons = initialize_neurons(subnet_names, t)
            neurons = np.concatenate((neurons, subnet_neurons), axis = 0)

            # sub matrix
            sub_matrix = adj_matrix(subnet_neurons,
                functions[subnet["name"]]["synapses"],
                functions[subnet["name"]]["neuron_names"]
            )

            # augmented matrix
            aug_matrix = np.empty((new_sze, new_sze), dtype = object)
            aug_matrix[:curr_offset, :curr_offset] = syn_matrix.synapse_matrix
            aug_matrix[curr_offset:, curr_offset:] = sub_matrix.synapse_matrix

            # neurons & neuron names set for synapse matrix
            syn_matrix.neurons = neurons
            syn_matrix.neuron_names += subnet_names

            # iterate over synapses & add them to preexisting adj matrix
            for synlist in subnet["synapses"]:
                i = syn_matrix.neuron_names.index(synlist.n_from)
                j = syn_matrix.neuron_names.index(synlist.n_to)
                aug_matrix[i][j] = synlist

            # synapse matrix set for synapse matrix
            syn_matrix.synapse_matrix = aug_matrix

    syn_matrix.simulate()

    return((f_p["output_idx"], neurons))