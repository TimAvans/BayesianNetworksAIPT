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

#Dataframes!

import pandas 

class Factor:

    def __init__(self, query: str, dataframe : pandas.DataFrame):
        self.Query = query
        self.Dataframe = dataframe


#Multiplication functions/operators override of the standard multiplication functions/operators of the class
    def __mul__(self, other):
        # Self * Other dataframe merge method
        return -1
    
    def __rmul__(self, other):
        # Other * Self dataframe merge method
        return -1
    
    def Multiplication(self, other : 'Factor', variable : str):
        # Find common columns
        common_columns = list(self.Dataframe.columns.intersection(other.Dataframe.columns))
        if(common_columns.__contains__("prob")):
            common_columns.remove("prob")
            
        if not common_columns:
            print("No common columns found.")
            return pandas.DataFrame()  # Return an empty dataframe

        # Merge with different suffixes for each dataframe
        merged = pandas.merge(self.Dataframe, other.Dataframe, on=common_columns, suffixes=('_self', '_other'))
        merged['prob'] = merged['prob_self'] * merged['prob_other']
        merged = merged.drop(columns=['prob_self', 'prob_other'])

        return Factor(self.Query, merged)

    def Marginalize(self, variable : str):     
        if(not self.Dataframe.columns.__contains__(variable)):
            return -1
        dtf = self.Dataframe.drop(variable, axis=1)
        vars = [col for col in dtf.columns.tolist() if col != "prob"]
        return Factor(self.Query, dtf.groupby(vars)["prob"].sum())

    def Normalize(self):
        return -1
    
    def __str__(self):
        return ""