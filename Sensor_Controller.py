import sounddevice as sd
from multiprocessing import Process
import numpy as np
import os
import time
from pysinewave import SineWave


class Sensor_Controller:


    @classmethod
    def play_Frequency(self, frequency, audio_device_name, play_time):
        sd.default.device = audio_device_name
        
        sinewave = SineWave()
        sinewave.set_frequency(frequency=frequency)
        sinewave.play()
        time.sleep(play_time)
        sinewave.stop()


    @classmethod
    def play_and_record_Calibration_Sound(self, audio_device_name, frequency, sample_rate):
        sd.default.device = audio_device_name['play_device_name']
        sinewave = SineWave()
        sinewave.set_frequency(frequency=frequency)
        sinewave.play()

        DB_level = input('please adjust the speaker level for a target db level and enter the db level here: ')
        valid_input = False
        while not valid_input:
            try:
                DB_level = float(DB_level)
                valid_input = True
            except:
                DB_level = input('incorrect value has to be a number please re-enter the db level here: ')
        time.sleep(0.2)
        sd.default.device = audio_device_name['record_device_name']
        recording = sd.rec(1000,samplerate=sample_rate, channels=1, dtype='float64')
        print('recording tone...')
        sd.wait()
        sinewave.stop()
        calibration_data = {
            'recording': recording,
            'DB_level': DB_level
        }
        return calibration_data

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


        play_device_names_string = '\n  '.join(play_device_names)
        play_device_name = input(f'please type the playback device you want to use your available devices are:\n    {play_device_names_string}\n enter the name of the device here: ')

        while not play_device_name in play_device_names_string:
            play_device_name = input(f'you entered an invalid device name these are the possible device names:\n    {play_device_names_string}\n enter the name of the device here: ')
        
        return  {
                'record_device_name': record_device_name,
                'play_device_name': play_device_name
                }

    @classmethod
    def record(self, duration, return_dict_recorder, audio_device_name, sample_rate):
        sd.default.device = audio_device_name
        recording = sd.rec(duration * sample_rate, samplerate=sample_rate, channels=1, dtype='float64')
        return_dict_recorder['start_recording'] =  time.time()
        sd.wait()
        return_dict_recorder['end_recording'] =  time.time()
        return_dict_recorder['recording'] = recording


    @classmethod
    def play_Sounds(self, frequenties, return_dict_playback, audio_device_name):
        
        sd.default.device = audio_device_name
        return_dict_playback['start_playback'] =  time.time()
        time.sleep(5)
        sinewave = SineWave()
        
        for frequency in frequenties:
            return_dict_playback[f'start_frequency_{str(frequency)}'] = time.time()
            sinewave.set_frequency(frequency=frequency)
            sinewave.play()
            time.sleep(2)
            sinewave.stop()
            return_dict_playback[f'stop_frequency_{str(frequency)}'] = time.time()
            time.sleep(3)
        return_dict_playback['end_playback'] = time.time()