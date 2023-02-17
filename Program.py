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
            what_to_run = input("please enter a valid option your options are: 'calibration' or 'experiment': ")
        if what_to_run == 'calibration':
            calibration_option  = input("enter 'run' if you want to run a callibration if you want to see de kalibration data press enter: ")
            while not calibration_option in ['', 'run']:
                calibration_option  = input(f"incorrect input: '{calibration_option}'\n\tenter 'run' if you want to run a callibration if you want to see de kalibration data press enter: ")
            
            running_calibration = True
            while running_calibration:
                if calibration_option == 'run':
                    Reverberation_Test.run_Calibration()
                    running_calibration = False
                    #code for rerun or exit
                if calibration_option == '':
                    Reverberation_Test.show_Calibration()
                    running_calibration = False
                    #code for rerun or exit

        elif what_to_run == 'experiment':
            Reverberation_Test.run_Experiment()




