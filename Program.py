from Reverberation_Test import Reverberation_Test
from Plot_Data import Plot_Data
import json 
class Program:
    
    @classmethod
    def startup(self, mode: str):
        """
        starts the ascars program with the given mode

        mode: str, gives the way you want the program to run text based or graphic

        """
        # gets the global settingsfile
        settingsfile = open('./appsettings.json', 'r')
        settings = json.loads(settingsfile.read())
        settingsfile.close()

        # starts ascars with given mode currently only supports text based
        print('startup...')
        if mode == 'text':
            self.start_Text_Based(settings)

    @classmethod
    def start_Text_Based(self, settings: dict):
        """
        runs ascars in text based mode

        settings: dict, holds al the settings from appsettings.json as a dictionairy
        """
        print('running ASCARS...')


        running = True
        while running:
            # asks user questions to navigate actions in ascars
            what_to_run = input("what do you want to run?.. 'calibration', 'experiment' or 'end' to end the program?: ")
            while not (what_to_run in ['calibration', 'experiment', 'end']):
                what_to_run = input("please enter a valid option your options are: 'calibration', 'experiment' 'end': ")
            if what_to_run == 'calibration':
                run_or_view_calibration = input("do you want to run an calibration, view data or end the program?\nenter 'run', 'view', or 'stop: ")
                while not (run_or_view_calibration in ['run', 'view']):
                    run_or_view_calibration = input("invalid input enter either 'run' or 'view': ")
                
                if run_or_view_calibration == "run":
                    Reverberation_Test.run_Calibration(settings)
                if run_or_view_calibration == "view":
                    Reverberation_Test.show_Calibration(settings)
            
            elif what_to_run == 'experiment': 
                experiment_option = input("Do you want to run an experiment, view data or end the program?\nEnter 'run', 'view', 'heatmap', or 'stop: ")
                
                while not (experiment_option in ['run', 'view', 'heatmap']):
                    experiment_option = input("Invalid input, please enter either 'run' or 'view': ")
                
                if experiment_option ==  'view':
                        print('What position do you want to run an experiment on?')
                        x_position = str(input('Enter your x position: '))
                        y_position = str(input('Enter your y position: '))
                        Plot_Data.graph_Experiment_Data(x_position, y_position, settings)
                
                if experiment_option ==  'run':
                    running_experiments = True
                    while running_experiments:
                    
                        print('what position do you want to run an experiment on?')
                        x_position = str(input('enter your x position: '))
                        y_position = str(input('enter your y position: '))
                        Reverberation_Test.run_Experiment(x_position, y_position, settings)
                        
                        keep_running = input("do you want to run another test? 'yes' or 'no': ")
                        while not (keep_running in ['yes', 'no']):
                            keep_running = input("invalid input enter either 'yes' or 'no': ")
                        
                        if keep_running == 'yes':
                            running_experiments = True
                        elif keep_running == 'no':
                            running_experiments = False
                
                if experiment_option ==  'heatmap':
                    frequency = input("what frequency do you want to run?: ")
            
                    while not (frequency.isdigit()):
                        frequency = input("invalid input!\nplease enter an integer: ")
                    

                    file_location = './data/reverberation_data/general_data.json'
                    print('showing heatmap...')
                    Plot_Data.show_Heatmap(file_location, frequency)
                    print('done showing heatmap!')
                
            if what_to_run ==  'end':
                running = False
