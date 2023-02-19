import matplotlib.pyplot as plt
from Sensor_Controller import Sensor_Controller
import pandas as pd
import json

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
    def data_Analysis(self, expirement_data, frequencies, x, y):
        time_data = expirement_data['time_data']
        recording = expirement_data['recording']
        time_stamps = expirement_data['timestamps']
        start_and_stop_time_stamps = self.get_Timestamps_For_Each_Frequency_Test(time_stamps, frequencies)
        
        if not (recording == [] or time_data == []) or not (len(recording) == len(time_data)):

            avaraging_window_in_number_of_samples = 441
            smoothed_recording = self.smooth_Sound(recording, avaraging_window_in_number_of_samples)
            graph_lines = self.get_lines(smoothed_recording, time_stamps, start_and_stop_time_stamps)
            
            self.write_Experiment_Data_to_File(frequencies, graph_lines, recording, time_data, x, y)
            return True
            
        else:
            print('none existent or corrupt data to process please check for any problems in your input data!')
            return False
    
    @classmethod
    def write_Experiment_Data_to_File(self, frequencies, graph_lines, recording, time_data, x, y):
        general_data = open('./data/reverberation_data/general_data.json', 'r').read()
        try:
            general_data = json.loads(general_data)
        except:
            general_data = {}

        if not 'x_value' in general_data.keys():
            general_data["x_value"] = {}
        if not str(x) in general_data["x_value"].keys():
            general_data["x_value"][str(x)] = {'y_value': {}}
        if not 'y_value' in general_data["x_value"][str(x)]:
            general_data["x_value"][str(x)] = {'y_value': {}}
        
        general_data["x_value"][str(x)]['y_value'][str(y)] = {
            "recording_file_name": f"{x}_{y}.csv",
            "frequencies": frequencies,
            "graph_lines": graph_lines
        }
        general_data_with_experiment_run = open('./data/reverberation_data/general_data.json', 'w')
        general_data_with_experiment_run.write(json.dumps(general_data))
        general_data_with_experiment_run.close()
        recording_data = pd.DataFrame({
            "recording": recording,
            "time_data": time_data
        })
        recording_data.to_csv(f"./data/reverberation_data/recordings/{x}_{y}.csv", ',', index=False)

    @classmethod
    def get_lines(self, smoothed_recording, time_stamps, start_and_stop_time_stamps):
        lines = {}

        for frequency in start_and_stop_time_stamps.keys():
            start_and_stop_time_stamp = start_and_stop_time_stamps[frequency]
            lines_by_frequency = {
                'start_time': start_and_stop_time_stamp['start_frequency_time'],
                'stop_time': start_and_stop_time_stamp['stop_frequency_time'],
                'vertical_lines': {},
                'horizontal_lines': {}
            }


            start_playing_frequency_time = int
            stop_playing_frequency_time  = int
            for timestamp in time_stamps:
                if timestamp['time_name'] == f'start_frequency_{frequency}':
                    start_playing_frequency_time = timestamp['time']
                if timestamp['time_name'] == f'stop_frequency_{frequency}':
                    stop_playing_frequency_time = timestamp['time']
            starting_intensity  = self.get_Starting_intensity(smoothed_recording, start_playing_frequency_time, stop_playing_frequency_time)
            reverberation_time = self.get_Reverberation_Time(smoothed_recording, starting_intensity, stop_playing_frequency_time)
            
            lines_by_frequency['vertical_lines']['reverberation_time'] = {
                'x_value': reverberation_time,
                'y_upper_bound' : starting_intensity,
                'y_lower_bound' : starting_intensity-10,
                'label_y': starting_intensity-(10/2),
                'label_x': reverberation_time
            }

            lines_by_frequency['vertical_lines']['start_playing'] = {
                'x_value': start_playing_frequency_time,
                'y_upper_bound' : starting_intensity*1.3,
                'y_lower_bound' : 0,
                'label_y': starting_intensity*1.2,
                'label_x': start_playing_frequency_time
            }

            lines_by_frequency['vertical_lines']['stop_playing'] = {
                'x_value': stop_playing_frequency_time,
                'y_upper_bound' : starting_intensity*1.3,
                'y_lower_bound' : 0,
                'label_y': starting_intensity*1.2,
                'label_x': stop_playing_frequency_time
            }

            lines_by_frequency['horizontal_lines']['starting_intensity']  = {
                'y_value': starting_intensity,
                'label_y': starting_intensity*1.2,
                'label_y': stop_playing_frequency_time,
                'x_upper_bound' : stop_playing_frequency_time + 2,
                'x_lower_bound' : start_playing_frequency_time - 2
            }

            lines_by_frequency['horizontal_lines']['reverberation_intensity']  = {
                'y_value': starting_intensity-10,
                'label_height': (starting_intensity-10)*1.2,
                'x_upper_bound' : stop_playing_frequency_time + 2,
                'x_lower_bound' : start_playing_frequency_time - 2
            }

            lines[str(frequency)] = lines_by_frequency
        return lines

    @classmethod
    def get_Reverberation_Time(self, smooth_recording, starting_intensity, stop_playing_frequency_time):
        sampling_rate = 44100
        start_point = int(stop_playing_frequency_time*sampling_rate)
        stop_point = int(start_point+2*sampling_rate)
        time_id = 0
        for point in smooth_recording[start_point:stop_point]:
            if point < starting_intensity - 10:
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
    def graph_Experiment_Data(self, time_data, smoothed_recording, time_stamps, start_and_stop_time_stamps, graph_lines):
        fig, axs = plt.subplots(1, 1 + len(start_and_stop_time_stamps))
            

        #define horizontal and vertical lines
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
        #make graphs per frequency
        
        #make full graph
        axs[0].plot(time_data, smoothed_recording)
        plt.show()


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
    def smooth_Sound(self, recording, avaraging_window_in_number_of_samples):
        recording = list(map(abs, recording))
        amplify = lambda datapoint: datapoint*100
        recording = list(map(amplify, recording))

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