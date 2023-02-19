import matplotlib.pyplot as plt
import pandas as pd

class Plot_Data:
    
    @classmethod
    def graph_Experiment_Data(self, time_data, smoothed_recording, time_stamps, start_and_stop_time_stamps, graph_lines):
        fig, axs = plt.subplots(1, 1 + len(start_and_stop_time_stamps))
                
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