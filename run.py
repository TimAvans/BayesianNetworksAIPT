"""
@Author: Joris van Vugt, Moira Berens, Leonieke van den Bulk

Entry point for the creation of the variable elimination algorithm in Python 3.
Code to read in Bayesian Networks has been provided. We assume you have installed the pandas package.

"""
from read_bayesnet import BayesNet
from variable_elim import VariableElimination
from Factor import Factor
from Logger import Logger


def CreateEliminationOrder(network : BayesNet, query, evidence):
    elim_order = network.nodes
    elim_order.remove(query)

    for key in evidence.keys():
        elim_order.remove(key)
    
    return elim_order

if __name__ == '__main__':

    logger = Logger("Log.txt")

    # net = BayesNet('earthquake.bif') # Format and other networks can be found on http://www.bnlearn.com/bnrepository/

    # # Make your variable elimination code in the seperate file: 'variable_elim'. 
    # # You use this file as follows:
    # ve = VariableElimination(net)

    # # Set the node to be queried as follows:
    # query = 'Alarm'

    # # The evidence is represented in the following way (can also be empty when there is no evidence): 
    # evidence = {'Burglary': 'True'}

    # # Determine your elimination ordering before you call the run function. The elimination ordering   
    # # is either specified by a list or a heuristic function that determines the elimination ordering
    # # given the network. Experimentation with different heuristics will earn bonus points. The elimination
    # # ordering can for example be set as follows:
    # elim_order = CreateEliminationOrder(net, query, evidence)

    # # Call the variable elimination function for the queried node given the evidence and the elimination ordering as follows:   
    # ve.run(query, evidence, elim_order, logger)
    # logger.LogMessage("-----------------------------------------------------------------------------------------------------")

    net1 = BayesNet('tampering.bif')
    ve1 = VariableElimination(net1)
    query1 = 'Tampering'
    evidence1 = {"Smoke": 'True', "Report": 'True'}
    elim_order1 = CreateEliminationOrder(net1, query1, evidence1)
    ve1.run(query1, evidence1, elim_order1, logger)
    logger.LogMessage("-----------------------------------------------------------------------------------------------------")
