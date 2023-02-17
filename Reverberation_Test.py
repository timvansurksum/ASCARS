from Sensor_Controller import Sensor_Controller
from Data_Processor import Data_Processor
import multiprocessing
from multiprocessing import Process
import numpy as np
import pandas as pd


class Reverberation_Test:
    
    @classmethod
    def run_Calibration(self, audio_device_name, frequency):
        existing_calibration_data = pd.read_csv('./data/calibration/calibration_data.csv')

        
        done = 0
        print(f'starting the calibration of the frequency {str(frequency)}')
        while not done:
            print(f'starting playing sound with frequency {str(frequency)}')
            calibration_data = Sensor_Controller.play_Calibration_Sound(audio_device_name, frequency)
            
            recording = list(map(abs, calibration_data['recording']))
            smooth_recording = Data_Processor.smooth_Sound(recording, 441)
            intensity = Data_Processor.get_Starting_intensity(smooth_recording, 441)
            DB_level = calibration_data
            # DB_level,frequency,microphone_intensity
            calibration_data_point = pd.DataFrame({
                'DB_level': DB_level,
                'frequency': frequency,
                'microphone_intensity': intensity
            })
            existing_calibration_data.append(calibration_data_point)

            new_DB_test = input("do you want to test another DB level? 'yes' or 'no'?")
            while new_DB_test in ['yes', 'no']:
                if new_DB_test == 'yes':
                    done = 0
                elif new_DB_test == 'no':
                    done = 1
                else:
                    new_DB_test = input("invalid input please enter a valid input either 'yes' or 'no'?")
        
        existing_calibration_data.to_csv('./data/calibration/calibration_data.csv', sep=',', encoding='utf-8', index=False)

    @classmethod
    def run_Sensor(self):

        audio_device_name  = Sensor_Controller.set_Audio_Devices()
        get_Min = lambda sound_sample: float(sound_sample[0])

        manager = multiprocessing.Manager()
        return_dict_recorder = manager.dict()
        record_sound_async = Process(target=Sensor_Controller.record, args=(35, return_dict_recorder, audio_device_name['record_device_name']))
        record_sound_async.start()
        
        return_dict_playback = manager.dict()
        play_sound_async = Process(target=Sensor_Controller.play_Sounds, args=([400,600,800,1000,1200,1400], return_dict_playback, audio_device_name['play_device_name']))
        play_sound_async.start()
        play_sound_async.join()
        record_sound_async.join()
        
        return_dict_recorder['recording'] = list(map(get_Min, return_dict_recorder['recording']))
        return return_dict_playback, return_dict_recorder
    
    @classmethod
    def format_Sensor_Data(self, return_dict_playback, return_dict_recorder):
        time_data = np.linspace(0,35,35*44100)
        

        get_time_relative_from_start = lambda time, time_name: {'time_name': time_name,'time': time-return_dict_recorder['start_recording']}
        time_stamps = list(map(get_time_relative_from_start, return_dict_playback.values(), return_dict_playback.keys()))

        expirement_data = {**return_dict_recorder, 'timestamps': time_stamps}
        expirement_data['time_data'] = time_data

        return expirement_data
    
    @classmethod
    def run_Experiment(self):
        print('running experiment...:')
        print('\trunning sensor...')
        return_dict_playback, return_dict_recorder = self.run_Sensor()
        print('\tdone running sensor')
        
        
        print('\tformatting data...')
        expirement_data = self.format_Sensor_Data(return_dict_playback, return_dict_recorder)
        print('\tdone formatting data')


        print('processing data...')
        Data_Processor.data_Analysis(expirement_data)
        print('finished running experiment')
