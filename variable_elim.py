"""
@Author: Joris van Vugt, Moira Berens, Leonieke van den Bulk

Class for the implementation of the variable elimination algorithm.

"""
from Factor import Factor
import pandas
class VariableElimination():

    def __init__(self, network):
        """
        Initialize the variable elimination algorithm with the specified network.
        Add more initializations if necessary.

        """
        self.network = network

    def run(self, query, observed, elim_order):
        """
        Use the variable elimination algorithm to find out the probability
        distribution of the query variable given the observed variables

        Input:
            query:      The query variable
            observed:   A dictionary of the observed variables {variable: value}
            elim_order: Either a list specifying the elimination ordering
                        or a function that will determine an elimination ordering
                        given the network during the run

        Output: A variable holding the probability distribution
                for the query variable

        """
        factors = self.CreateFactors()
        for var in elim_order:
            factor = [factor for factor in factors if var == factor.Query]
            

    def CreateFactors(self):
        factors = []
        for node in self.network.nodes:
            tempFactor = Factor(node, self.network.probabilities[node])
            factors.append(tempFactor)
        return factors

        