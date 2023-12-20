# https://www.youtube.com/watch?v=dkeUDOzoC30
# A factor is a function from some set of variables into a specific value
# Variable elimination works by eliminating all variables in turn until
# there is a factor with only the query variable 

# to eliminate a variable 
# 1: Join all factors containing that variable
# 2: Sum out the influence of the variable
# 3: Exploits product form of joint distribution

# What do we need in the factor class to be able to do this:
# What we query over
# Table with probabilities (See video)
# 

# How to represent a table ; thinking about a dictionary  
# Have to normalize at the end (Video)


# Network has probabilities in dictionary: e.g.
# Dict with key "MaryCalls" has value: MaryCalls True False True False 
#                                      Alarm     True True False False
#                                      prob      0.7  0.3  0.01  0.99

import pandas 

class Factor:

    """
    Initialize the factor class with a dataframe from the pandas package
    """
    def __init__(self, dataframe : pandas.DataFrame):
        self.Dataframe = dataframe

    """
    Reduce the current factor's dataframe by the given variable and value
    """
    def Reduce(self, variable : str, value : str):
        self.Dataframe = self.Dataframe.loc[self.Dataframe[variable] == value]
        self.Dataframe = self.Dataframe.drop(variable, axis=1)
    
    """
    Multiply the current factor with another factor
    Multiplication is in essence the merging of 2 pandas dataframes on the columns they have in common
    From both dataframes the probability columns are multiplied
    """
    def Multiplication(self, other : 'Factor'):
        # Find common columns
        common_columns = list(set(element for element in self.Dataframe.columns if element != 'prob')
                              .intersection(element for element in other.Dataframe.columns if element != 'prob'))
        
        # Make sure probability column is not in the common columns list
        if(common_columns.__contains__("prob")):
            common_columns.remove("prob")

        # If there are no common columns return self
        if not common_columns:
            print("No common columns found.")
            return self  # Return self

        # Merge with different suffixes for each dataframe
        merged = self.Dataframe.merge(other.Dataframe, on=common_columns, suffixes=('_self', '_other'))
        merged['prob'] = merged['prob_self'] * merged['prob_other']
        merged = merged.drop(columns=['prob_self', 'prob_other'])

        return Factor(merged)

    """
    Marginalize the current factor and return a new Marginalized factor
    Marginalize it with the variable given as parameter
    """
    def Marginalize(self, variable : str):     
        # Check if the dataframe contains the variable as column
        if not self.Dataframe.columns.__contains__(variable):
            return self # If niet return itself not marginalized
        
        # Drop the column of variable 
        dtf = self.Dataframe.drop(variable, axis=1)
        # Group the other columns and sum the probability
        vars = [col for col in dtf.columns.tolist() if col != "prob"]
        dtf = dtf.groupby(vars, as_index=False)["prob"].sum()

        # If the previous actions return a pandas.series instead of dataframe make a dataframe from the series
        if isinstance(dtf, pandas.Series):
            dtf = pandas.DataFrame(dtf)
        
        return Factor(dtf)

    """
    Normalize the current Factor and return it
    """
    def Normalize(self):
        # Calculate the total probability by summing the probability column
        total_prob = self.Dataframe['prob'].sum()

        # If the total probability is not 0 divide each value in the probability column by the total probability
        if total_prob != 0:
            self.Dataframe['prob'] = self.Dataframe['prob'] / total_prob

        return self
    
    """
    Return a factor existing in the list given as parameter which has columns in common with the current factor
    """
    def GetFactorWithCommonColumns(self, factors):
        # Loop throught the factors list
        for other in factors:
            # Get the columns they have in common
            common_columns = list(set(element for element in self.Dataframe.columns if element != 'prob').intersection(element for element in other.Dataframe.columns if element != 'prob'))
            # Return the factor with more than 0 columns in common
            if common_columns.__len__() > 0:
                return other
            