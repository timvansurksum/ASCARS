import matplotlib.pyplot as plt
from Sensor_Controller import Sensor_Controller
import pandas as pd

class Data_Processor:
    
    @classmethod
    def calibrate_Sensor(self, audio_device_name, playtime, frequency):
        existing_calibration_data = pd.read_csv('./data/calibration/calibration_data.csv')

        
        done = 0
        print(f'starting the calibration of the frequency {str(frequency)}')
        while not done:
            print(f'starting playing sound with frequency {str(frequency)}')
            calibration_data = Sensor_Controller.play_Calibration_Sound(audio_device_name, frequency)
            
            recording = list(map(abs, calibration_data['recording']))
            smooth_recording = self.smooth_Sound(recording, 441)
            intensity = self.get_Starting_intensity(smooth_recording, 441)
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
    def data_Analysis(self, expirement_data, frequencies):
        time_data = expirement_data['time_data']
        recording = expirement_data['recording']
        time_stamps = expirement_data['timestamps']
        start_and_stop_time_stamps = self.get_Timestamps_For_Each_Frequency_Test(time_stamps, frequencies)
        
        if not (recording == [] or time_data == []) or not (len(recording) == len(time_data)):
            fig, axs = plt.subplots(1)
            
            avaraging_window_in_number_of_samples = 441
            smoothed_recording = self.smooth_Sound(recording, avaraging_window_in_number_of_samples)
            axs[0].plot(time_data, smoothed_recording)
            label_height = 1
            frequency_timings = {}

            for time_stamp in time_stamps:
                label = time_stamp['time_name']
                time = time_stamp['time']
                if (str(label).find('start_frequency_') + 1):
                    frequency = str(label).strip('start_frequency_')
                    frequency_timings[frequency] = {}
                    frequency_timings[frequency]['start_time'] = time
                if (str(label).find('stop_frequency_') + 1):
                    frequency = str(label).strip('stop_frequency_')
                    frequency_timings[frequency]['stop_time'] = time

                axs[0].vlines(time, 0, 100, label=label, linestyles='dotted', colors='g')


                if label_height:
                    axs[0].text(time, 60, label, backgroundcolor='dimgray', color='white')
                    label_height = 0
                else:
                    axs[0].text(time, 50, label, backgroundcolor='grey', color='white')
                    label_height = 1
            for frequency_timing in frequency_timings.values():
                starting_intesity = self.get_Starting_intensity(smoothed_recording, frequency_timing['start_time']+0.5, frequency_timing['stop_time'])
                axs[0].hlines(
                            starting_intesity, 
                            frequency_timing['start_time'] - 0.5, 
                            frequency_timing['stop_time'] + 0.5, 
                            label=label, 
                            linestyles='dotted', 
                            colors='g'
                            )
            plt.show()
        else:
            print('none existent or corrupt data to process please check for any problems in your input data!')
    
    @classmethod
    def get_Timestamps_For_Each_Frequency_Test(self, timestamps, frequencies):
        
        start_and_stop_time_stamps = {}
        for frequency in frequencies:
            start_frequency_time = int
            stop_frequency_time = int
            
            got_start_time = False
            got_stop_time = False

            for timestamp in timestamps:
                if not got_start_time or not got_stop_time:
                    time_name  = timestamp['time_name']
                    if time_name.find(str(frequency)) + 1:
                        if time_name.find('start') + 1:
                            start_frequency_time = timestamp['time'] - 2
                            got_start_time  = True
                        if time_name.find('stop') + 1:
                            stop_frequency_time = timestamp['time'] + 2
                            got_stop_time  = True
                else:
                    start_and_stop_time_stamps[str(frequency)] = {
                        'start_frequency_time': start_frequency_time,
                        'stop_frequency_time': stop_frequency_time,
                    }
        return start_and_stop_time_stamps





    @classmethod
    def get_Reverberation_Time(self, starting_intensity, stop_playing_frequency_time, data):
        sampling_rate = 44100
        start_point = stop_playing_frequency_time*sampling_rate
        stop_point = start_point+2*sampling_rate
        time_id = 0
        for point in data[start_point:stop_point]:
            if point < starting_intensity - 30:
                break
            else:
                time_id += 1
        reveberation_time = stop_playing_frequency_time + time_id/sampling_rate
        return reveberation_time
    
    @classmethod
    def get_Starting_intensity(self, smoothed_recording, start_frequency_time, stop_frequency_time):
        sampling_rate = 44100
        starting_intensity_value = int((start_frequency_time)*sampling_rate)-1
        last_intensity_value = int(stop_frequency_time*sampling_rate)
        values_to_get_avarage_over = smoothed_recording[starting_intensity_value:last_intensity_value]
        starting_intensity = sum(values_to_get_avarage_over)/len(values_to_get_avarage_over)
        return starting_intensity
    
    
    @classmethod
    def smooth_Sound(self, recording, avaraging_window_in_number_of_samples):
        smoothed_recording = []
        sample_count = len(recording)
        index = 0
        for _ in recording:
            if index < avaraging_window_in_number_of_samples:
                list_of_values = recording[0:avaraging_window_in_number_of_samples+1]
                
                smoothed_recording.append(sum(list_of_values)/len(list_of_values))
            elif sample_count - index < avaraging_window_in_number_of_samples:
                list_of_values = recording[avaraging_window_in_number_of_samples:-1]
                
                smoothed_recording.append(sum(list_of_values)/len(list_of_values))
            else:
                lower_limit = int(round(index-avaraging_window_in_number_of_samples/2, 0))
                upper_limit = int(round(index+avaraging_window_in_number_of_samples/2, 0))
                list_of_values = recording[lower_limit:upper_limit]
                
                smoothed_recording.append(sum(list_of_values)/len(list_of_values))
            index += 1
        return smoothed_recording