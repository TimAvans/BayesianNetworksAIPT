"""
@Author: Joris van Vugt, Moira Berens, Leonieke van den Bulk

Class for the implementation of the variable elimination algorithm.

"""
from Factor import Factor
import pandas
class VariableElimination():

    """
    Initialize the variable elimination algorithm with the specified network.
    Add more initializations if necessary.

    """
    def __init__(self, network):
        self.network = network

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
    def run(self, query, observed, elim_order, logger):
        factors = self.CreateFactors(observed, elim_order, logger)
        multiplicationCounter = 0
        marginalizationCounter = 0

        for elim in elim_order:
            while factors[elim].__len__() > 1:
                fac1 = factors[elim].pop()
                logger.LogDataframe(fac1, "First factor to multiply:")
                fac2 = fac1.GetFactorWithCommonColumns(factors[elim])
                logger.LogDataframe(fac2, "Second factor to multiply:")
                factors[elim].remove(fac2)
                multiplied_factor = fac1.Multiplication(fac2)
                multiplicationCounter+=1
                factors[elim].append(multiplied_factor)
                logger.LogDataframe(multiplied_factor, "Factor mutliplication result:")
            
            if factors[elim].__len__() == 1:
                logger.LogDataframe(factors[elim][0], "Factor to marginalize:")
                marginalized_factor = factors[elim].pop().Marginalize(elim)
                marginalizationCounter+=1
                logger.LogDataframe(marginalized_factor, "Factor marginalized:")

                if elim in factors.keys():
                    if  elim_order.index(elim)+1 != elim_order.__len__():
                        next_variable = elim_order[elim_order.index(elim) + 1]
                        factors[next_variable].append(marginalized_factor)
                        logger.LogMessage("Factor added to the list of the key: " + elim)
                    else:
                        factors[elim_order[-1]].append(marginalized_factor)
                        logger.LogMessage("Factor added to the list of the key: " + elim_order[-1]) 
                else:
                    factors[elim_order[-1]].append(marginalized_factor)
                    logger.LogMessage("Factor added to the list of the key: " + elim_order[-1])

        for key, value in factors.items():
            if  value.__len__() == 0:
                continue
            else:
                query_factor = self.GetQueryFactor(query)
                logger.LogMessage("Get the query factor and multiply it by the result of the variable elimination algorithm: ")
                for col in query_factor.Dataframe.columns:
                    if col != query and col != "prob":
                        query_factor = query_factor.Marginalize(col)

                result_factor = value[0].Multiplication(query_factor)
                logger.LogDataframe(query_factor, "Query factor:")
                logger.LogDataframe(value[0], "Variable elimination algorithm result:")
                multiplicationCounter+=1
                result_factor_normalized = result_factor.Normalize()
                logger.LogDataframe(result_factor, "Result factor is achieved:")
                logger.LogDataframe(result_factor_normalized, "Result factor normalized is achieved:")
                logger.LogMessage("Amount of multiplications: " + multiplicationCounter.__str__())
                logger.LogMessage("Amount of marginalizations: " + marginalizationCounter.__str__())
                return result_factor_normalized

    def CreateFactors(self, observed, elim_order, logger):
        factorsdictionary = dict()
        tempProbabilities = self.network.probabilities.copy()
        for node in elim_order:
            probabilities = []
            for value, prob in self.network.probabilities.items():
                if tempProbabilities.keys().__contains__(value):
                    if  prob.columns.__contains__(node):
                        new_factor = Factor(prob)             
                        keys = observed.keys()
                        for key in keys:
                            if  new_factor.Dataframe.columns.__contains__(key):
                                new_factor.Reduce(key, observed[key])
                        probabilities.append(new_factor)
                        del tempProbabilities[value]
                        logger.LogDataframe(new_factor, "Factor created and added with dataframe: ")
            factorsdictionary[node] = probabilities      
        return factorsdictionary
    
    def GetQueryFactor(self, query):
        probability = self.network.probabilities[query]
        return Factor(probability)
            
        