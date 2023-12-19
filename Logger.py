import datetime
from Factor import Factor 
class Logger:
    def __init__(self, log_file='log.txt'):
        self.log_file = log_file

    def LogMessage(self, message):
        timestamp = datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        log_entry = f'[{timestamp}] {message}\n'

        with open(self.log_file, 'a') as file:
            file.write(log_entry)
    
    def LogDataframe(self, factor : Factor, message=''):
        timestamp = datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        log_entry = f'[{timestamp}] {message}\n'

        with open(self.log_file, 'a') as file:
            file.write(log_entry + factor.Dataframe.to_string(index=False) + '\n\n')
