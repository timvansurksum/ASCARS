import winsound
import sounddevice as sd
from multiprocessing import Process
import multiprocessing
import numpy as np
import os
import time


class Sound_Manager:
    #example change
    @classmethod
    def set_Audio_Devices(self):
        record_device_names  = []
        play_device_names  = []
        for audio_device in list(sd.query_devices()):
            if int(audio_device["max_input_channels"]) > 0:
                record_device_names.append(audio_device['name'])
            if int(audio_device["max_output_channels"]) > 0:
                play_device_names.append(audio_device['name'])
        
        os.system('cls')
        record_device_names_string = '\n    '.join(record_device_names)
        record_device_name = input(f'please type the recording device you want to use your available devices are:\n {record_device_names_string}\n enter the name of the device here: ')

        while not record_device_name in record_device_names:
            record_device_name = input(f'you entered an invalid device name these are the possible device names:\n  {record_device_names_string}\n enter the name of the device here: ')


        os.system('cls')
        play_device_names_string = '\n  '.join(play_device_names)
        play_device_name = input(f'please type the playback device you want to use your available devices are:\n    {play_device_names_string}\n enter the name of the device here: ')

        while not play_device_name in play_device_names_string:
            play_device_name = input(f'you entered an invalid device name these are the possible device names:\n    {play_device_names_string}\n enter the name of the device here: ')
        os.system('cls')
        
        return  {
                'record_device_name': record_device_name,
                'play_device_name': play_device_name
                }

    @classmethod
    def record(self, duration, return_dict_recorder, audio_device_name):
        sd.default.device = audio_device_name
        fs = 44100
        recording = sd.rec(duration * fs, samplerate=fs, channels=1, dtype='float64')
        return_dict_recorder['start_recording'] =  time.time()
        sd.wait()
        return_dict_recorder['end_recording'] =  time.time()
        return_dict_recorder['recording'] = recording


    @classmethod
    def play_Sounds(self, frequenties, return_dict_playback, audio_device_name):
        sd.default.device = audio_device_name
        return_dict_playback['start_playback'] =  time.time()
        time.sleep(5)
        for frequency in frequenties:
            return_dict_playback[f'start_frequency_{str(frequency)}'] = time.time()
            sd.
            winsound.Beep(frequency, 1000)
            return_dict_playback[f'stop_frequency_{str(frequency)}'] = time.time()
            time.sleep(4)
        return_dict_playback['end_playback'] = time.time()

    @classmethod
    def run_Experiment(self):
        print('running experiment...')
        audio_device_name  = self.set_Audio_Devices()
        get_Min = lambda sound_sample: float(sound_sample[0])
        time_data = np.linspace(0,35,35*44100)
        
        manager = multiprocessing.Manager()
        return_dict_recorder = manager.dict()
        record_sound_async = Process(target=self.record, args=(35, return_dict_recorder, audio_device_name['record_device_name']))
        record_sound_async.start()
        
        return_dict_playback = manager.dict()
        play_sound_async = Process(target=self.play_Sounds, args=([400,600,800,1000,1200,1400], return_dict_playback, audio_device_name['play_device_name']))
        play_sound_async.start()
        play_sound_async.join()
        record_sound_async.join()
        
        return_dict_recorder['recording'] = list(map(get_Min, return_dict_recorder['recording']))

        get_time_relative_from_start = lambda time, time_name: {'time_name': time_name,'time': time-return_dict_recorder['start_recording']}
        time_stamps = list(map(get_time_relative_from_start, return_dict_playback.values(), return_dict_playback.keys()))

        all_data_from_expirement = {**return_dict_recorder, 'timestamps': time_stamps}
        all_data_from_expirement['time_data'] = time_data

        print('done running experiment')
        return all_data_from_expirement
