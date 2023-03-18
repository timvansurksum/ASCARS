import matplotlib.pyplot as plt
import pandas as pd
import json
from Data_Processor import Data_Processor
import seaborn as sns

class Plot_Data:
    
    @classmethod
    def graph_Experiment_Data(self, x: str, y: str):
        sampling_rate = 44100
        general_data = json.loads(open("./data/reverberation_data/general_data.json", 'r').read())
        experiment_general_data = general_data["x_value"][x]["y_value"][y]
        
        frequency_to_graph_id = {}
        
        frequencies = experiment_general_data["frequencies"]
        graph_id = 1
        for frequency in  frequencies:
            frequency_to_graph_id[frequency] = graph_id
            graph_id += 1
 
        graph_data = pd.read_csv(f"./data/reverberation_data/recordings/{x}_{y}.csv")
        recording = list(graph_data['recording'])
        time_data = list(graph_data['time_data'])
        
        number_of_graphs = 1 + len(frequencies)
        fig, axs = plt.subplots(number_of_graphs, 1, constrained_layout=True)
        fig.suptitle(f"reverberation plot for position ({x}, {y})")
        
        axs[0].set_title("whole recording intesity")
        axs[0].plot(time_data, recording)

        for frequency in frequencies:
            
            graph_id = frequency_to_graph_id[frequency]
            frequency_general_data = experiment_general_data['graph_lines'][str(frequency)]
            
            start_time = int(frequency_general_data["start_time"] * sampling_rate)
            stop_time = int(frequency_general_data["stop_time"] * sampling_rate)
            
            vertical_lines = frequency_general_data["vertical_lines"]
            horizontal_lines = frequency_general_data["horizontal_lines"]
            
            subsection_of_time_data_for_this_frequency = time_data[start_time: stop_time]
            subsection_of_recording_for_this_frequency = recording[start_time: stop_time]

            axs[graph_id].plot(subsection_of_time_data_for_this_frequency, subsection_of_recording_for_this_frequency)
            axs[graph_id].set_title(f'{str(frequency)}Hz')

            for vertical_line_title in vertical_lines.keys():
                vertical_line = vertical_lines[vertical_line_title]
                
                x_value = vertical_line["x_value"]
                y_lower_bound = vertical_line["y_lower_bound"]
                y_upper_bound = vertical_line["y_upper_bound"]

                label_x = vertical_line["label_x"]
                label_y = vertical_line["label_y"]

                axs[graph_id].vlines(x_value, y_lower_bound, y_upper_bound, colors='k', linestyles='dotted')
                axs[graph_id].text(label_x, label_y, vertical_line_title)
                axs[0].text(label_x, label_y, vertical_line_title)

                axs[0].vlines(x_value, y_lower_bound, y_upper_bound, colors='k', linestyles='dotted')

            for horizontal_line_title in horizontal_lines.keys():
                horizontal_line = horizontal_lines[horizontal_line_title]
                
                y_value = horizontal_line["y_value"]
                x_lower_bound = horizontal_line["x_lower_bound"]
                x_upper_bound = horizontal_line["x_upper_bound"]

                label_x = horizontal_line["label_x"]
                label_y = horizontal_line["label_y"]

                axs[graph_id].hlines(y_value, x_lower_bound, x_upper_bound, colors='k', linestyles='dotted')
                axs[graph_id].text(label_x, label_y, horizontal_line_title)
                axs[0].text(label_x, label_y, horizontal_line_title)

                axs[0].hlines(y_value, x_lower_bound, x_upper_bound, colors='k', linestyles='dotted')
        plt.show()
           
    @classmethod
    def graph_Kalibration(self, kalibration_data: pd.DataFrame):
        frequencies = list(kalibration_data.drop_duplicates(subset=['frequency']).to_dict()['frequency'].values())
        frequency_count = len(frequencies)
        if frequency_count == 1:
            frequency = frequencies[0]
            kalibration_data_with_current_frequency = kalibration_data[kalibration_data["frequency"] == frequency] 
            kalibration_data_dictionairy = kalibration_data_with_current_frequency.sort_values(by="microphone_intensity").to_dict()
            
            microphone_intensity_values = list(kalibration_data_dictionairy['microphone_intensity'].values())
            DB_level_values = list(kalibration_data_dictionairy['DB_level'].values())
            
            plt.plot(microphone_intensity_values, DB_level_values)
            plt.title(f'kalibration graph of {str(frequency)}hz frequency')
            plt.xlabel('intensity_values')
            plt.ylabel('DB_values')
        else:
            fig, axs = plt.subplots(1, frequency_count)
            fig.suptitle('calibration graphs')
            for frequency_id in range(frequency_count):
                frequency = frequencies[frequency_id]
                kalibration_data_with_current_frequency = kalibration_data[kalibration_data["frequency"] == frequency] 
                kalibration_data_dictionairy = kalibration_data_with_current_frequency.sort_values(by="microphone_intensity").to_dict()
                
                microphone_intensity_values = list(kalibration_data_dictionairy['microphone_intensity'].values())
                DB_level_values = list(kalibration_data_dictionairy['DB_level'].values())
                title = f'{str(frequency)}hz'
                
                axs[frequency_id].plot(
                    microphone_intensity_values, DB_level_values)
                axs[frequency_id].set_title(title)
                axs[frequency_id].set_xlabel('intensity_values')
                axs[frequency_id].set_ylabel('DB_values')
                

        plt.show()
    
        
    @classmethod
    def show_Heatmap(self, file_location, frequencie):
        imported_data = Data_Processor.process_General_Data_For_Heat_Map(file_location, frequencie)
        transformed_data = imported_data.pivot("pos_x", "pos_y", "reverberation_time")

        sns.heatmap(transformed_data, vmin=0, vmax=2)
        plt.xlabel("Afstand y (m)")
        plt.ylabel("Afstand x (m)")
        plt.show()