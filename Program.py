from Graphical_User_Interface import Graphical_User_Interface
from Reverberation_Test import Reverberation_Test

class Program:
    
    @classmethod
    def startup(self, mode):
        print('startup...')
        if mode == 'text':
            self.start_Text_Based()


    def start_Text_Based():
        print('running ASCARS')
        what_to_run = input("what do you want to run?.. 'calibration' or 'experiment'?: ")

        while not what_to_run in ['calibration', 'experiment']:
            what_to_run = input("please enter a valid option your options are: 'calibration' or 'experiment' ")
        if what_to_run == 'calibration':
            Reverberation_Test.run_Calibration()
        elif what_to_run == 'experiment':
            Reverberation_Test.run_Experiment()




