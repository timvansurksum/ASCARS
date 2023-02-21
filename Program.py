from Graphical_User_Interface import Graphical_User_Interface
from Reverberation_Test import Reverberation_Test
from Plot_Data import Plot_Data

class Program:
    
    @classmethod
    def startup(self, mode):
        
        print('Startup...')
        
        if mode == 'text':
            self.start_Text_Based()


    def start_Text_Based():
        
        print('Running ASCARS...')
        running = True

        while running:
            what_to_run = input("What do you want to run? For calibration type 'calibration', for experiment type 'experiment' or type 'end' to end the program: ")
            
            while not (what_to_run in ['calibration', 'experiment', 'end']):
                what_to_run = input("Please enter a valid option. The options are: 'calibration', 'experiment' 'end': ")
            
            if what_to_run == 'calibration':
                run_or_view_calibration = input("Do you want to run an calibration, view data or end the program?\nEnter 'run', 'view', or 'stop: ")
                
                while not (run_or_view_calibration in ['run', 'view']):
                    run_or_view_calibration = input("Invalid input, please enter either 'run' or 'view': ")
                
                if run_or_view_calibration == "run":
                    Reverberation_Test.run_Calibration()
                
                if run_or_view_calibration == "view":
                    Reverberation_Test.show_Calibration()
            
            elif what_to_run == 'experiment': 
                run_or_view_experiment = input("Do you want to run an experiment, view data or end the program?\nEnter 'run', 'view', or 'stop: ")
                
                while not (run_or_view_experiment in ['run', 'view']):
                    run_or_view_experiment = input("Invalid input, please enter either 'run' or 'view': ")
                
                if run_or_view_experiment ==  'view':
                        print('What position do you want to run an experiment on?')
                        x_position = str(input('Enter your x position: '))
                        y_position = str(input('Enter your y position: '))
                        Plot_Data.graph_Experiment_Data(x_position, y_position)
                
                if run_or_view_experiment ==  'run':
                    running_experiments = True
                    
                    while running_experiments:
                        print('What position do you want to run an experiment on?')
                        x_position = str(input('Enter your x position: '))
                        y_position = str(input('Enter your y position: '))
                        Reverberation_Test.run_Experiment(x_position, y_position)
                        keep_running = input("Do you want to run another test? 'yes' or 'no': ")
                        
                        while not (keep_running in ['yes', 'no']):
                            keep_running = input("Invalid input, please enter either 'yes' or 'no': ")
                        
                        if keep_running == 'yes':
                            running_experiments = True
                        
                        elif keep_running == 'no':
                            running_experiments = False
            
            if what_to_run ==  'end':
                running = False