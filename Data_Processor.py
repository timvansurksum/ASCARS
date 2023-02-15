import matplotlib.pyplot as plt
from Sound_Manager import Sound_Manager

class Data_Processor:
    @classmethod
    def data_Analysis(self):
        recording, timestamps = Sound_Manager.run_Test_Experiment()
        if not (recording == [] or timestamps == []):
            fig, axs = plt.subplots(2)
            axs[0].plot(timestamps, recording)
            recording = list(map(abs, recording))
            avaraging_window_in_number_of_samples = 441
            smoothed_recording = self.smooth_Sound(recording, avaraging_window_in_number_of_samples)
            axs[1].plot(timestamps, smoothed_recording)
            plt.show()
            print('done')
        else:
            print('no data')
    
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