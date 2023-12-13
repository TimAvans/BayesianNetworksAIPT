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


class Factor:

    def __init__(self, query: str, rows : dict):
        self.Query = query
        self.Rows = rows


#Multiplication functions/operators override of the standard multiplication functions/operators of the class
    def __mul__(self, other):
        # Self * Other
        return -1
    
    def __rmul__(self, other):
        # Other * Self
        return -1
    
    def Normalize(self):
        return -1
    
    def __str__(self):
        return ""