import matplotlib.pyplot as plt
import pandas as pd

class Data_Processor:

    @classmethod
    def graph_Kalibration(self, kalibration_data: pd.DataFrame):
        frequencies = list(kalibration_data.drop_duplicates(subset=['frequency']).to_dict()['frequency'].values())
        frequency_count = len(frequencies)
        fig, axs = plt.subplots(frequency_count, 1)
        plt.title('calibration graphs')
        for frequency_id in range(frequency_count):
            frequency = frequencies[frequency_id]
            kalibration_data_with_current_frequency = kalibration_data[kalibration_data["frequency"] == frequency] 
            kalibration_data_dictionairy = kalibration_data_with_current_frequency.to_dict()
            
            microphone_intensity_values = list(kalibration_data_dictionairy['microphone_intensity'].values())
            DB_level_values = list(kalibration_data_dictionairy['DB_level'].values())
            
            axs[frequency_id].plot(microphone_intensity_values, DB_level_values)
            axs[frequency_id].set_title(f'kalibration graph of {str(frequency)}hz frequency')
            axs[frequency_id].set_xlabel('intensity_values')
            axs[frequency_id].set_ylabel('DB_values')
        plt.show()
        print('done showing calibration graphs')

    
    @classmethod
    def process_Calibration_Data(self, calibration_data, frequency):
            recording = list(map(abs, calibration_data['recording']))
            smooth_recording = self.smooth_Sound(recording, 441)
            intensity = self.get_Starting_intensity(smooth_recording, 0, 1)
            DB_level = calibration_data['DB_level']
            calibration_data_point = pd.DataFrame({
                'DB_level': DB_level,
                'frequency': frequency,
                'microphone_intensity': intensity
            })
            return calibration_data_point
    @classmethod
    def data_Analysis(self, expirement_data):
        time_data = expirement_data['time_data']
        recording = expirement_data['recording']
        time_stamps = expirement_data['timestamps']
        
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
    def get_Starting_intensity(self, smoothed_recording, start_frequency_time, stop_frequency_time):
        starting_intensity_value = int((start_frequency_time)*44100)-1
        last_intensity_value = int(stop_frequency_time*44100)
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