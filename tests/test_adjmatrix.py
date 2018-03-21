import unittest
import numpy as np
import neuralkernel.adjmatrix as adjmatrix
import neuralkernel.synapse as synapse
import neuralkernel.constants as constants
import neuralkernel.neuron as neuron


class TestAdjMatrix(unittest.TestCase):
    def setUp(self):
        t = np.arange(0, 3)
        synapses = np.asarray([
            synapse.SynapseList('one', 'two', np.asarray([
                synapse.Synapse('V', constants.V_THRESHOLD, 0)
            ]))
        ])
        neurons = [neuron.Neuron(neuron_name, t) for neuron_name in ['one', 'two']]
        self.adj_matrix = adjmatrix.AdjMatrix(neurons, synapses)

    def test_synapse_prop(self):
        # actual
        n_from = 0
        n_to = 1
        tj = 0
        syn = self.adj_matrix.synapse_matrix[n_from][n_to].synapses[0]
        self.adj_matrix.synapse_prop(syn, n_to, tj)
        # expected
        expected_v = np.asarray([0, 10, 0])
        # test
        np.testing.assert_almost_equal(self.adj_matrix.neurons[n_to].v, expected_v)
