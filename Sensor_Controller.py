import sounddevice as sd
from multiprocessing import Process
import numpy as np
from pysinewave import SineWave
import time
import os



class Sensor_Controller:


    @classmethod
    def play_Frequency(self, frequency: int, audio_device_name: str, play_time: int):
        """
        Function that plays a given frequency for a set amound of time
        frequency: int, frequentie that is going to be played
        audio_device_name: str, name of the playback device
        play_time: int, time in seconds to play the frequency
        """
        # sets audio device
        sd.default.device = audio_device_name
        
        #plays tone for set time
        sinewave = SineWave()
        sinewave.set_frequency(frequency=frequency)
        sinewave.play()
        time.sleep(play_time)
        sinewave.stop()


    @classmethod
    def play_and_record_Calibration_Sound(self, audio_device_name: dict, frequency: int, sample_rate: int):
        """
        Function that both records and plays sound to calibrate your microphone.
        This function will automaticly ask questions in the console to get the necessairy callibration data.
        audio_device_name: dict, name of the audio devices
        frequency: int, frequency of the tone being calibrated
        sample_rate: int, sample rate of the microphone
        """
        # sets audio device
        sd.default.device = audio_device_name['play_device_name']
        
        sinewave = SineWave()
        sinewave.set_frequency(frequency=frequency)
        #plays tone
        sinewave.play()

        #asks user to mark the percieved db level of the microphone
        DB_level = input('please adjust the speaker level for a target db level and enter the db level here: ')
        
        #checks if imput is valid
        valid_input = False
        while not valid_input:
            try:
                DB_level = float(DB_level)
                valid_input = True
            except:
                DB_level = input('incorrect value has to be a number please re-enter the db level here: ')
        #records shortly to mark the intesity of the given sound signal
        time.sleep(0.2)
        sd.default.device = audio_device_name['record_device_name']
        recording = sd.rec(1000,samplerate=sample_rate, channels=1, dtype='float64')
        print('recording tone...')
        sd.wait()
        sinewave.stop()

        # returns recording with marked db level
        calibration_data = {
            'recording': recording,
            'DB_level': DB_level
        }
        return calibration_data

    @classmethod
    def set_Audio_Devices(self):
        """
        Function that asks users via the console which audio devices to use
        """
        
        # builds a list of recording & playback devices
        record_device_names  = []
        play_device_names  = []
        for audio_device in list(sd.query_devices()):
            if int(audio_device["max_input_channels"]) > 0:
                record_device_names.append(audio_device['name'])
            if int(audio_device["max_output_channels"]) > 0:
                play_device_names.append(audio_device['name'])
        
        # clears console
        os.system('cls')

        # asks user what recording device it wants to use and checks if the device name is valid
        record_device_names_string = '\n    '.join(record_device_names)
        record_device_name = input(f'please type the recording device you want to use your available devices are:\n {record_device_names_string}\n enter the name of the device here: ')

        while not record_device_name in record_device_names:
            record_device_name = input(f'you entered an invalid device name these are the possible device names:\n  {record_device_names_string}\n enter the name of the device here: ')

        # asks user what playback device it wants to use and checks if the device name is valid
        play_device_names_string = '\n  '.join(play_device_names)
        play_device_name = input(f'please type the playback device you want to use your available devices are:\n    {play_device_names_string}\n enter the name of the device here: ')

        while not play_device_name in play_device_names_string:
            play_device_name = input(f'you entered an invalid device name these are the possible device names:\n    {play_device_names_string}\n enter the name of the device here: ')
        
        # returns the selected recording and playback devices
        return  {
                'record_device_name': record_device_name,
                'play_device_name': play_device_name
                }

    @classmethod
    def record(self, duration: int, return_dict_recorder: dict, audio_device_name: str, sample_rate: int):
        """
        records for a given period of time and marks when it starts and stops recording
        duration: int, how long it records
        return_dict_recorder: dict, an object that stores data to be able to run this function in parallel
        audio_device_name: str, name of the audio device used to record
        sample_rate: int, sample rate the recorder records with
        """
        # sets recording device
        sd.default.device = audio_device_name
        
        # records the frequenties being played and marks start and stop times
        recording = sd.rec(duration * sample_rate, samplerate=sample_rate, channels=1, dtype='float64')
        return_dict_recorder['start_recording'] =  time.time()
        sd.wait()

        # returns recording data
        return_dict_recorder['end_recording'] =  time.time()
        return_dict_recorder['recording'] = recording


    @classmethod
    def play_Sounds(self, frequenties: list, return_dict_playback: dict, audio_device_name: str):
        """ 
        plays a list of frequenties
        frequenties: list, list of frequenties to be played
        return_dict_playback: dict, an object that stores data to be able to run this function in parallel
        audio_device_name: str, name of the playback device
        """ 
        # sets playback device
        sd.default.device = audio_device_name
        return_dict_playback['start_playback'] =  time.time()
        time.sleep(5)
        # for every frequentie plays for 2 seconds and marks all the start and stop times
        sinewave = SineWave()
        for frequency in frequenties:
            return_dict_playback[f'start_frequency_{str(frequency)}'] = time.time()
            sinewave.set_frequency(frequency=frequency)
            sinewave.play()
            time.sleep(2)
            sinewave.stop()
            return_dict_playback[f'stop_frequency_{str(frequency)}'] = time.time()
            time.sleep(3)
        # sets end playback value and returns all marked timestamps
        return_dict_playback['end_playback'] = time.time()