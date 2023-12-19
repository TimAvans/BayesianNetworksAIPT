"""
@Author: Joris van Vugt, Moira Berens, Leonieke van den Bulk

Class for the implementation of the variable elimination algorithm.

"""
from Factor import Factor
import pandas
#!TODO: Logging to logfile
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
    def run(self, observed, elim_order, logger):
        factors = self.CreateFactors(observed, elim_order, logger)
        for elim in elim_order:
            while factors[elim].__len__() > 1:
                fac1 = factors[elim].pop()
                logger.LogDataframe(fac1, "First factor to multiply:")
                fac2 = self.getoverlappingfactors(factors[elim], fac1)
                logger.LogDataframe(fac2, "Second factor to multiply:")
                factors[elim].remove(fac2)
                multiplied_factor = fac1.Multiplication(fac2)
                factors[elim].append(multiplied_factor)
                logger.LogDataframe(multiplied_factor, "Factor mutliplication result:")
            if factors[elim].__len__() == 1:
                logger.LogDataframe(factors[elim][0], "Factor to marginalize:")
                marginalized_factor = factors[elim].pop().Marginalize(elim)
                logger.LogDataframe(marginalized_factor, "Factor marginalized:")

                x = False
                for item in marginalized_factor.Dataframe.columns:
                    for item2 in factors.keys():
                        if  item == item2:
                            x = True

                if x:                  
                    for col in marginalized_factor.Dataframe.columns:
                        if col != "prob":
                            if col in factors.keys():
                                factors[col].append(marginalized_factor)
                                logger.LogMessage("Factor added to the list of the key: " + col)
                else:
                    factors[elim_order[-1]].append(marginalized_factor)
                    logger.LogMessage("Factor added to the list of the key: " + elim_order[-1])

            if factors[elim].__len__() == 0:
                del factors[elim]

        for key, value in factors.items():
            if  value.__len__() == 0:
                continue
            else:
                result_factor = value[0].Normalize()
                logger.LogDataframe(result_factor, "Result factor is achieved:")
                return result_factor

    def getoverlappingfactors(self, variable_factors, factor1):
        for factor2 in variable_factors:
            intersection = list(set(factor1.Dataframe.columns).intersection(factor2.Dataframe.columns))
            if intersection:
                return factor2

    def CreateFactors(self, observed, elim_order, logger):
        factorsdictionary = dict()
        for node in elim_order:
            probabilities = []
            for value, prob in self.network.probabilities.items():
                if  prob.columns.__contains__(node):
                    new_factor = Factor(prob)
                    exists = False
                    for key, list in factorsdictionary.items():
                        for  fac in list:
                            if  fac.Dataframe.equals(new_factor.Dataframe):
                                exists = True
                    for  fac in probabilities:
                        if  fac.Dataframe.equals(new_factor.Dataframe):
                            exists = True
                    if not exists:                    
                        keys = observed.keys()
                        for key in keys:
                            if  new_factor.Dataframe.columns.__contains__(key):
                                new_factor.Reduce(key, observed[key])
                        probabilities.append(new_factor)
                        logger.LogDataframe(new_factor, "Factor created and added with dataframe: ")
            factorsdictionary[node] = probabilities
        return factorsdictionary