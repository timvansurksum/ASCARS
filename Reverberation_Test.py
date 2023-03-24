from Sensor_Controller import Sensor_Controller
from Data_Processor import Data_Processor
from Plot_Data import Plot_Data
import multiprocessing
from multiprocessing import Process
import numpy as np
import pandas as pd
import json


class Reverberation_Test:
    
    @classmethod
    def show_Calibration(self, settings):
        kalibration_data = pd.read_csv('./data/calibration/calibration_data.csv')
        print('showing calibration graphs...')
        Plot_Data.graph_Kalibration(kalibration_data)

    @classmethod
    def run_Calibration(self, settings):
        existing_calibration_data = pd.read_csv('./data/calibration/calibration_data.csv')
        done_running_this_frequency = False
        while not done_running_this_frequency:
            audio_device_names = Sensor_Controller.set_Audio_Devices()
            frequency = input("what frequency do you want to calibrate?: ")
            valid_frequency = False
            try:
                frequency = int(frequency)
            except:
                while not valid_frequency:
                    frequency = input("invalid input please enter a valid frequency?: ")
                    try:
                        frequency = int(frequency)
                        valid_frequency = True
                    except:
                        valid_frequency = False
            
                

            print(f'starting the calibration')
            frequency = frequency
            print(f'starting playing sound with frequency {str(frequency)}')
            calibration_data = Sensor_Controller.play_and_record_Calibration_Sound(audio_device_names, frequency, settings["sampling_rate"])
            print('processing data...')
            calibration_data_point = Data_Processor.process_Calibration_Data(calibration_data, frequency, settings["sampling_rate"])
            
            existing_calibration_data = pd.concat([existing_calibration_data, calibration_data_point])

            new_DB_test = input("do you want to test another DB level? 'yes' or 'no'? ")
            while not new_DB_test in ['yes', 'no']:
                    new_DB_test = input("invalid input please enter a valid input either 'yes' or 'no'? ")

            if new_DB_test == 'yes':
                done_running_this_frequency = False
            elif new_DB_test == 'no':
                done_running_this_frequency = True

        existing_calibration_data.to_csv('./data/calibration/calibration_data.csv', sep=',', encoding='utf-8', index=False)

    @classmethod
    def run_Sensor(self, frequencies, sample_rate):

        audio_device_name  = Sensor_Controller.set_Audio_Devices()
        get_Min = lambda sound_sample: float(sound_sample[0])

        manager = multiprocessing.Manager()
        return_dict_recorder = manager.dict()
        recording_time = len(frequencies) * 5 + 5

        record_sound_async = Process(target=Sensor_Controller.record, args=(recording_time, return_dict_recorder, audio_device_name['record_device_name'], sample_rate))
        record_sound_async.start()
        
        return_dict_playback = manager.dict()
        play_sound_async = Process(target=Sensor_Controller.play_Sounds, args=(frequencies, return_dict_playback, audio_device_name['play_device_name']))
        play_sound_async.start()
        
        play_sound_async.join()
        record_sound_async.join()
        
        return_dict_recorder['recording'] = list(map(get_Min, return_dict_recorder['recording']))
        return return_dict_playback, return_dict_recorder
    
    @classmethod
    def format_Sensor_Data(self, return_dict_playback, return_dict_recorder, settings):
        playtime = 5 * len(settings["frequenties"]) + 5
        time_data = np.linspace(0, playtime, playtime*settings["sampling_rate"])
        

        get_time_relative_from_start = lambda time, time_name: {'time_name': time_name,'time': time-return_dict_recorder['start_recording']}
        time_stamps = list(map(get_time_relative_from_start, return_dict_playback.values(), return_dict_playback.keys()))

        expirement_data = {**return_dict_recorder, 'timestamps': time_stamps}
        expirement_data['time_data'] = time_data

        return expirement_data
    
    @classmethod
    def run_Experiment(self, x, y, settings):
        print('running experiment...:')
        print('\trunning sensor...')
        frequencies  = settings["frequenties"]
        return_dict_playback, return_dict_recorder = self.run_Sensor(frequencies, settings["sampling_rate"])
        print('\tdone running sensor')
        
        
        print('\tformatting data...')
        expirement_data = self.format_Sensor_Data(return_dict_playback, return_dict_recorder, settings)
        print('\tdone formatting data')


        print('processing data...')
        Data_Processor.data_Analysis(expirement_data, frequencies, x, y, settings)
        print('finished running experiment')
