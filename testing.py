class Testing:
    '''Simple Testing class to put a banner around your Classes.run_test() method
       Just create your testing instance at the beginning of your run_tests() method
       test = Testing('Classname')
       #... body of run_tests() code
       # test.end()  
    '''
    def __init__(self, name:str):
        self.name = name
        Testing.print_message(f'Running tests on {self.name.upper()}')
    def end(self):
        Testing.print_message(f'Ending tests on class {self.name.upper()}', end=True)
    @staticmethod
    def print_message(msg, end=False):
        if not end: 
            print()
        print('=' * 50)
        print(msg)
        print('=' * 50)
