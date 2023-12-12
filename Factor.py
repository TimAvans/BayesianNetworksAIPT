
class Factor:

    def __init__(self, name : str, variables : [int]):
        self.Name = name
        self.Variables = variables

#Multiplication functions/operators override of the standard multiplication functions/operators of the class
    def __mul__(self, other):
        # Self * Other
        return -1
    
    def __rmul__(self, other):
        # Other * Self
        return -1