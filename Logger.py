import datetime
from Factor import Factor 

class Logger:
    """
    Initialize the logger
    Log_file has the standard value of "log.txt"
    """
    def __init__(self, log_file='log.txt'):
        self.log_file = log_file

    """
    LogMessage logs the parameter message in the log_file 
    It prints a timestamp of when the message is logged in combination with the message in the format "[TIMESTAMP] message\n"
    """
    def LogMessage(self, message):
        timestamp = datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        log_entry = f'[{timestamp}] {message}\n'

        with open(self.log_file, 'a') as file:
            file.write(log_entry)
    
    """
    LogDataframe logs the parameter message above the parameter factor's dataframe in the log_file 
    It prints a timestamp of when the message is logged in combination with the message in the format 
    "[TIMESTAMP] message\n
    COLUMN1     COLUMN2
    val1        val1
    val2        val2"    
    """
    def LogDataframe(self, factor : Factor, message=''):
        timestamp = datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        log_entry = f'[{timestamp}] {message}\n'

        with open(self.log_file, 'a') as file:
            file.write(log_entry + factor.Dataframe.to_string(index=False) + '\n\n')

    """
    Log a dictionary of key value pairs in format:
    [{timestamp}] {message}\n 
    {Key:Value}
    """
    def LogDictionary(self, dictionary : dict, message=''):
        timestamp = datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        log_entry = f'[{timestamp}] {message}\n'
        dict_string = ""
        for key, value in dictionary.items():
            dict_string += key + " : " + value + "\n"

        with open(self.log_file, 'a') as file:
            file.write(log_entry + "" + dict_string + " " + '\n')

    """
    Log a list of strings in format:
    [{timestamp}] {message}\n 
    {str}
    """
    def LogList(self, values : [], message=''):
        timestamp = datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        log_entry = f'[{timestamp}] {message}\n'
        list_string = ""
        for value in values:
            list_string += value + "\n"

        with open(self.log_file, 'a') as file:
            file.write(log_entry + "" + list_string + " " + '\n')