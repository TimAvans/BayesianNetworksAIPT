"""
@Author: Joris van Vugt, Moira Berens, Leonieke van den Bulk

Representation of a Bayesian network read in from a .bif file.

"""

import pandas as pd

class BayesNet():
    """
    This class represents a Bayesian network.
    It can read files in a .bif format (if the formatting is
    along the lines of http://www.bnlearn.com/bnrepository/)

    Uses pandas DataFrames for representing conditional probability tables
    """

    # Possible values per variable
    values = {}

    # Probability distributions per variable
    probabilities = {}

    # Parents per variable
    parents = {}


    def __init__(self, filename):
        """
        Construct a bayesian network from a .bif file

        """
        with open(filename, 'r') as file:
            line_number = 0

            # Iterate through each line in the file
            for line in file:

                # Check if the line starts with 'network,' indicating the network name
                if line.startswith('network'):
                    self.name = ' '.join(line.split()[1:-1])

                # Check if the line starts with 'variable,' indicating variable information
                elif line.startswith('variable'):
                    self.parse_variable(line_number, filename)

                 # Check if the line starts with 'probability,' indicating probability distribution
                elif line.startswith('probability'):
                    self.parse_probability(line_number, filename)
                line_number = line_number + 1


    def parse_probability(self, line_number, filename):
        """
        Parse the probability distribution
        """

        # get line
        line = open(filename, 'r').readlines()[line_number]

        # Find out what variable(s) we are talking about
        variable, parents = self.parse_parents(line)
        next_line = open(filename, 'r').readlines()[line_number + 1].strip()

        # If a variable has no parents, its probabilities start with table
        if next_line.startswith('table'):
            comma_sep_probs = next_line.split('table')[1].split(';')[0].strip()
            probs = [float(p) for p in comma_sep_probs.split(',')]

            # Create a DataFrame with columns for the variable and 'prob'
            df = pd.DataFrame(columns=[variable, 'prob'])   

            # Populate the DataFrame with values and their corresponding probabilities
            for value, p in zip(self.values[variable], probs):
                df.loc[len(df)] = [value, p]
                self.probabilities[variable] = df

        else:
            #create dataFrame to store the variables
            df = pd.DataFrame(columns=[variable] + parents + ['prob'])

            #loop over the lines until a line is the same as "}" 
            with open(filename, 'r') as file:

                # Move the file pointer to the appropriate line
                for i in range(line_number + 1):
                    file.readline()

                # Iterate through the lines in the file
                for line in file:

                    if '}' in line:
                        # Done reading this probability distribution
                        break
                    
                    # Get the values for the parents
                    comma_sep_values = line.split('(')[1].split(')')[0]
                    values = [v.strip() for v in comma_sep_values.split(',')]

                    # Get the probabilities for the variable
                    comma_sep_probs = line.split(')')[1].split(';')[0].strip()
                    probs = [float(p) for p in comma_sep_probs.split(',')]

                	# Create a row in the df for each value combination
                    for value, p in zip(self.values[variable], probs):
                        df.loc[len(df)] = [value] + values + [p]

            self.probabilities[variable] = df # Store the DataFrame for the variable in the probabilities dictionary


    def parse_variable(self, line_number, filename):
        """
        Parse the name of a variable and its possible values
        """
        variable = open(filename, 'r').readlines()[line_number].split()[1]
        line = open(filename, 'r').readlines()[line_number+1]

        # Find the indices of the opening and closing curly braces to isolate the values
        start = line.find('{') + 1
        end = line.find('}')

        # Extract and strip each value, storing them in a list
        values = [value.strip() for value in line[start:end].split(',')]
        self.values[variable] = values


    def parse_parents(self, line):
        """
        Find out what variables are the parents
        Returns the variable and its parents
        """
        start = line.find('(') + 1
        end = line.find(')')
        variables = line[start:end].strip().split('|')
        variable = variables[0].strip()

        # If there are parents, extract and store them
        if len(variables) > 1:
            parents = variables[1]
            self.parents[variable] = [v.strip() for v in parents.split(',')]
            
        # If there are no parents, set an empty list for the variable
        else:
            self.parents[variable] = []

        return variable, self.parents[variable]


    @property
    def nodes(self):
        """Returns the names of the variables in the network"""
        return list(self.values.keys())
