import matplotlib.pyplot as plt
from Sound_Manager import Sound_Manager

class Data_Processor:
    @classmethod
    def data_Analysis(self):
        all_data_from_expirement = Sound_Manager.run_Experiment()
        time_data = all_data_from_expirement['time_data']
        recording = all_data_from_expirement['recording']
        time_stamps = all_data_from_expirement['timestamps']
        if not (recording == [] or time_data == []) or not (len(recording) == len(time_data)):
            fig, axs = plt.subplots(2)
            axs[0].plot(time_data, recording)
            recording = list(map(abs, recording))
            
            avaraging_window_in_number_of_samples = 441
            smoothed_recording = self.smooth_Sound(recording, avaraging_window_in_number_of_samples)
            axs[1].plot(time_data, smoothed_recording)
            for time_stamp in time_stamps:
                label = time_stamp['time_name']
                time = time_stamp['time']
                axs[1].vlines(time, 0, 1, label=label, linestyles='dotted', colors='g')
            
            plt.show()
        else:
            print('no or corrupt data to process please check for any problems in your input data!')
    
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