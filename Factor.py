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
import re

class Factor:

    def __init__(self, dataframe : pandas.DataFrame):
        self.Dataframe = dataframe

    def Reduce(self, variable : str, value : str):
        self.Dataframe = self.Dataframe.loc[self.Dataframe[variable] == value]
        self.Dataframe = self.Dataframe.drop(variable, axis=1)
    
    def Multiplication(self, other : 'Factor'):
        # Find common columns
        common_columns = list(set(element for element in self.Dataframe.columns if element != 'prob').intersection(element for element in other.Dataframe.columns if element != 'prob'))
        
        if(common_columns.__contains__("prob")):
            common_columns.remove("prob")
            
        if not common_columns:
            print("No common columns found.")
            return self  # Return an empty dataframe

        # Merge with different suffixes for each dataframe
        merged = self.Dataframe.merge(other.Dataframe, on=common_columns, suffixes=('_self', '_other'))
        merged['prob'] = merged['prob_self'] * merged['prob_other']
        merged = merged.drop(columns=['prob_self', 'prob_other'])

        return Factor(merged)

    def Marginalize(self, variable : str):     
        if not self.Dataframe.columns.__contains__(variable):
            return self
        
        # if len([s for s in self.Dataframe.columns if re.search("prob", s) is None]) <= 1:
        #     return self

        dtf = self.Dataframe.drop(variable, axis=1)
        vars = [col for col in dtf.columns.tolist() if col != "prob"]
        dtf = dtf.groupby(vars, as_index=False)["prob"].sum()

        if isinstance(dtf, pandas.Series):
            dtf = pandas.DataFrame(dtf)
        
        return Factor(dtf)

    def Normalize(self):
        total_prob = self.Dataframe['prob'].sum()

        if total_prob != 0:
            self.Dataframe['prob'] = self.Dataframe['prob'] / total_prob

        return self
    
    def GetFactorWithCommonColumns(self, factors):
        for other in factors:
            common_columns = list(set(element for element in self.Dataframe.columns if element != 'prob').intersection(element for element in other.Dataframe.columns if element != 'prob'))
            if common_columns:
                return other
            
    def __str__(self):
        return ""