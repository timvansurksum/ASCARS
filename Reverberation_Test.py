from Sensor_Controller import Sensor_Controller
from Data_Processor import Data_Processor
import multiprocessing
from multiprocessing import Process
import numpy as np


class Reverberation_Test:
    
    @classmethod
    def run_Calibration():
        print('run calibration here')

    @classmethod
    def run_Sensor(self, frequencies):

        audio_device_name  = Sensor_Controller.set_Audio_Devices()
        get_Min = lambda sound_sample: float(sound_sample[0])

        manager = multiprocessing.Manager()
        return_dict_recorder = manager.dict()
        record_sound_async = Process(target=Sensor_Controller.record, args=(35, return_dict_recorder, audio_device_name['record_device_name']))
        record_sound_async.start()
        
        return_dict_playback = manager.dict()
        play_sound_async = Process(target=Sensor_Controller.play_Sounds, args=(frequencies, return_dict_playback, audio_device_name['play_device_name']))
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
        frequencies  = [400,600,800,1000,1200,1400]
        return_dict_playback, return_dict_recorder = self.run_Sensor(frequencies)
        print('\tdone running sensor')
        
        
        print('\tformatting data...')
        expirement_data = self.format_Sensor_Data(return_dict_playback, return_dict_recorder)
        print('\tdone formatting data')


        print('processing data...')
        Data_Processor.data_Analysis(expirement_data, frequencies)
        print('finished running experiment')
