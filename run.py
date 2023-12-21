"""
@Author: Joris van Vugt, Moira Berens, Leonieke van den Bulk

Entry point for the creation of the variable elimination algorithm in Python 3.
Code to read in Bayesian Networks has been provided. We assume you have installed the pandas package.

"""
"""
Students: Britt Stoffels s1054953, Tim Janssen s1125701
Assignment: Programming assignment 3
Course: SOW-BKI259
"""
from read_bayesnet import BayesNet
from variable_elim import VariableElimination
from Factor import Factor
from Logger import Logger


def CreateEliminationOrder(network : BayesNet, query, evidence):
    # Initialize elimination order with all nodes in the network
    elim_order = network.nodes
    elim_order.remove(query)

    # Remove nodes corresponding to evidence variables from the elimination order
    for key in evidence.keys():
        elim_order.remove(key)
    
    return elim_order

# Entry point for the script, executing Bayesian network probabilistic inference and logging results.
if __name__ == '__main__':

    logger = Logger("Log.txt")

    # net = BayesNet('earthquake.bif') # Format and other networks can be found on http://www.bnlearn.com/bnrepository/
    # ve = VariableElimination(net)
    # query = 'Alarm'
    # evidence = {'Burglary': 'True'}
    # elim_order = CreateEliminationOrder(net, query, evidence)
    # ve.run(query, evidence, elim_order, logger)
    # logger.LogMessage("-----------------------------------------------------------------------------------------------------")

    net1 = BayesNet('tampering.bif')
    ve1 = VariableElimination(net1)
    query1 = 'Tampering'
    evidence1 = {"Smoke": 'True', "Report": 'True'}
    elim_order1 = CreateEliminationOrder(net1, query1, evidence1)
    ve1.run(query1, evidence1, elim_order1, logger)
    logger.LogMessage("-----------------------------------------------------------------------------------------------------")
