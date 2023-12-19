"""
@Author: Joris van Vugt, Moira Berens, Leonieke van den Bulk

Entry point for the creation of the variable elimination algorithm in Python 3.
Code to read in Bayesian Networks has been provided. We assume you have installed the pandas package.

"""
from read_bayesnet import BayesNet
from variable_elim import VariableElimination
from Factor import Factor
from Logger import Logger
if __name__ == '__main__':
    # # The class BayesNet represents a Bayesian network from a .bif file in several variables
    # net = BayesNet('earthquake.bif') # Format and other networks can be found on http://www.bnlearn.com/bnrepository/

    # # Make your variable elimination code in the seperate file: 'variable_elim'. 
    # # You use this file as follows:
    # ve = VariableElimination(net)

    # #Earthquake:
    # # Set the node to be queried as follows:
    # query = 'Alarm'
    # # The evidence is represented in the following way (can also be empty when there is no evidence): 
    # evidence = {'Burglary': 'True'}


    # # Determine your elimination ordering before you call the run function. The elimination ordering   
    # # is either specified by a list or a heuristic function that determines the elimination ordering
    # # given the network. Experimentation with different heuristics will earn bonus points. The elimination
    # # ordering can for example be set as follows:
    
    # #TODO: determine elim order 
    # elim_order = net.nodes
    # elim_order.remove(query)
    # for key in evidence.keys():
    #     elim_order.remove(key)


    logger = Logger("Log.txt")
    # # Call the variable elimination function for the queried node given the evidence and the elimination ordering as follows:   
    # ve.run(evidence, elim_order, logger)
    # logger.LogMessage("-----------------------------------------------------------------------------------------------------")
    
    # The class BayesNet represents a Bayesian network from a .bif file in several variables
    net = BayesNet('tampering.bif') # Format and other networks can be found on http://www.bnlearn.com/bnrepository/
    # Make your variable elimination code in the seperate file: 'variable_elim'. 
    # You use this file as follows:
    ve = VariableElimination(net)
    # Tampering:
    # Set the node to be queried as follows:
    query = 'Tampering'
    # The evidence is represented in the following way (can also be empty when there is no evidence): 
    evidence = {'Smoke': 'True', 'Report': 'True'}
    elim_order = net.nodes
    elim_order.remove(query)
    for key in evidence.keys():
        elim_order.remove(key)
    ve.run(evidence, elim_order, logger)
    logger.LogMessage("-----------------------------------------------------------------------------------------------------")
