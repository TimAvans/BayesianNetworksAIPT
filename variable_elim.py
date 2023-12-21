"""
@Author: Joris van Vugt, Moira Berens, Leonieke van den Bulk

Class for the implementation of the variable elimination algorithm.

"""
from Factor import Factor

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
        logger.LogMessage("Query variable: " + query)      
        logger.LogDictionary(observed, "Observed variables: ")
        logger.LogList(elim_order, "Elimination order: ")

        # Create the factors dictionary
        factors = self.CreateFactors(observed, elim_order, logger)

        # Initialize the complexity counters at 0
        multiplicationCounter = 0
        marginalizationCounter = 0
        logger.LogMessage("Algorithm started: \n\n")

        # Loop through the elimination order
        for elim in elim_order:

            # Check if the length of the factors list of the current elim node is greater than 1
            while factors[elim].__len__() > 1:
                # Take the first factor from the list and remove it
                fac1 = factors[elim].pop()
                logger.LogDataframe(fac1, "First factor to multiply:")

                # Get the factor with the most common columns to the first factor from the list and remove it
                fac2 = fac1.GetFactorWithCommonColumns(factors[elim])
                logger.LogDataframe(fac2, "Second factor to multiply:")
                factors[elim].remove(fac2)

                # Multiply the first factor with the second factor and add it back to the list
                multiplied_factor = fac1.Multiplication(fac2)
                multiplicationCounter+= len(fac1.Dataframe) * len(fac2.Dataframe)
                factors[elim].append(multiplied_factor)
                logger.LogDataframe(multiplied_factor, "Factor mutliplication result:")
            
            # If the list in the dictionary of the current elim node has only 1 factor in it we marginalize the factor
            if factors[elim].__len__() == 1:
                logger.LogDataframe(factors[elim][0], "Factor to marginalize:")
                marginalized_factor = factors[elim].pop().Marginalize(elim)
                marginalizationCounter+=1
                logger.LogDataframe(marginalized_factor, "Factor marginalized:")

                # Add the factor to the list of the next elim node and if it is the last elim node add it to the list of the last elim node
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

        # Get the list with more than 0 elements in it
        for key, value in factors.items():

            if  value.__len__() == 0:
                continue

            else:
                # Get the query factor
                query_factor = self.GetQueryFactor(query)
                logger.LogMessage("Get the query factor and multiply it by the result of the variable elimination algorithm: ")  
                        
                # Multiply the query factor with the value of the elimination done in the previous steps
                result_factor = value[0].Multiplication(query_factor)
                logger.LogDataframe(query_factor, "Query factor:")
                logger.LogDataframe(value[0], "Variable elimination algorithm result:")
                multiplicationCounter+= len(fac1.Dataframe) * len(fac2.Dataframe)

                # Normalize the result
                result_factor_normalized = result_factor.Normalize()
                logger.LogDataframe(result_factor, "Result factor is achieved:")
                logger.LogDataframe(result_factor_normalized, "Result factor normalized is achieved:")
                logger.LogMessage("Amount of multiplications: " + multiplicationCounter.__str__())
                logger.LogMessage("Amount of marginalizations: " + marginalizationCounter.__str__())
                return result_factor_normalized

    """
    Creates all factors from the nodes mentioned in the elim order list. i.e. not the observed and not the query variable
    Reduces the factors that contain a column mentioned in the observed variables dictionary
    Returns a dictionary with all factors as value to the node's name as key
    """
    def CreateFactors(self, observed, elim_order, logger):
        logger.LogMessage("Creating of Factors: \n\n")

        # Initialize an empty dict
        factorsdictionary = dict()

        # Initialize a copy of all dataframes in the network
        tempProbabilities = self.network.probabilities.copy()

        # Loop through the elimination order
        for node in elim_order:

            # Initialize empty list of probability dataframes
            probabilities = []

            # Loop through all probability dataframes
            for value, prob in self.network.probabilities.items():

                # Check if it has already been added once if not continue
                if tempProbabilities.keys().__contains__(value):

                    # Check if the columns of the probability dataframe contain the current node
                    if  prob.columns.__contains__(node):
                        #Create a factor and reduce it if neccessary
                        new_factor = Factor(prob)             
                        keys = observed.keys()

                        # Reduce the factor based on observed evidence
                        for key in keys:

                            # Check if the columns of the probability dataframe contain the current observed variable
                            if  new_factor.Dataframe.columns.__contains__(key):
                                new_factor.Reduce(key, observed[key])

                        probabilities.append(new_factor)

                        del tempProbabilities[value]
                        logger.LogDataframe(new_factor, "Factor created and added with dataframe: ")

            # Add the temporary list of factors to it's corresponding node in the dictionary            
            factorsdictionary[node] = probabilities      
        return factorsdictionary
    
    """
    Creates a Factor from the query variable and returns it marginalized until it has only the query's value
    """
    def GetQueryFactor(self, query):
        # Get the query's dataframe
        probability = self.network.probabilities[query]

        # Create a Factor from it
        query_factor = Factor(probability)

        # Marginalize it until the query's column is the only one remaining
        for col in query_factor.Dataframe.columns:
            if col != query and col != "prob":
                query_factor = query_factor.Marginalize(col)

        return query_factor
            