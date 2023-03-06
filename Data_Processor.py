import pandas as pd
import json

class Data_Processor:

    @classmethod
    def process_Calibration_Data(self, calibration_data, frequency):
            get_Min = lambda sound_sample: float(sound_sample[0])
            recording = list(map(get_Min, calibration_data["recording"]))
            recording = list(map(abs, recording))
            smooth_recording = self.smooth_Sound(recording, 441)
            intensity = self.get_Starting_intensity(smooth_recording, 0, 1)
            DB_level = calibration_data['DB_level']
            calibration_data_point = pd.DataFrame({
                'DB_level': [DB_level],
                'frequency': [frequency],
                'microphone_intensity': [intensity]
            })
            return calibration_data_point

    @classmethod
    def data_Analysis(self, expirement_data, frequencies, x, y):
        time_data = expirement_data['time_data']
        recording = expirement_data['recording']
        time_stamps = expirement_data['timestamps']
        start_and_stop_time_stamps = self.get_Timestamps_For_Each_Frequency(time_stamps, frequencies)
        if (
            not (recording == [] 
            or time_data == [])
            and (len(recording) == len(time_data))
            ):

            avaraging_window_in_number_of_samples = 441
            smoothed_recording = self.smooth_Sound(recording, avaraging_window_in_number_of_samples)
            calibrated_recording = self.apply_Calibration_to_recording_data(smoothed_recording, start_and_stop_time_stamps)
            graph_lines = self.get_lines(calibrated_recording, time_stamps, start_and_stop_time_stamps)
            
            self.write_Experiment_Data_to_File(frequencies, graph_lines, calibrated_recording, time_data, x, y)
            return True
            
        else:
            print('none existent or corrupt data to process please check for any problems in your input data!')
            return False
    
    @classmethod
    
    def write_Experiment_Data_to_File(self, frequencies, graph_lines, smoothed_recording, time_data, x, y):
        
        existing_general_data = open('./data/reverberation_data/general_data.json', 'r').read()

        try:
            general_data = json.loads(existing_general_data)
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
        general_data_with_experiment_run.write(json.dumps(general_data, indent='\t'))
        general_data_with_experiment_run.close()
        recording_data = pd.DataFrame({
            "recording": smoothed_recording,
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
            starting_intensity  = self.get_Starting_intensity(smoothed_recording, stop_playing_frequency_time)
            reverberation_time = self.get_Reverberation_Time(smoothed_recording, starting_intensity, stop_playing_frequency_time)
            
            lines_by_frequency['vertical_lines']['reverberation_time'] = {
                'x_value': reverberation_time,
                'y_upper_bound' : starting_intensity,
                'y_lower_bound' : starting_intensity-10,
                'label_x': reverberation_time,
                'label_y': starting_intensity-(10/2)
            }

            lines_by_frequency['vertical_lines']['start_playing'] = {
                'x_value': start_playing_frequency_time,
                'y_upper_bound' : starting_intensity*1.3,
                'y_lower_bound' : 0,
                'label_x': start_playing_frequency_time,
                'label_y': starting_intensity*1.2
            }

            lines_by_frequency['vertical_lines']['stop_playing'] = {
                'x_value': stop_playing_frequency_time,
                'y_upper_bound' : starting_intensity*1.3,
                'y_lower_bound' : 0,
                'label_x': stop_playing_frequency_time,
                'label_y': starting_intensity*1.2
            }

            lines_by_frequency['horizontal_lines']['starting_intensity']  = {
                'y_value': starting_intensity,
                'x_upper_bound' : stop_playing_frequency_time + 2,
                'x_lower_bound' : start_playing_frequency_time - 2,
                'label_x': stop_playing_frequency_time,
                'label_y': starting_intensity*1.2
            }

            lines_by_frequency['horizontal_lines']['reverberation_intensity']  = {
                'y_value': starting_intensity-10,
                'x_upper_bound' : stop_playing_frequency_time + 2,
                'x_lower_bound' : start_playing_frequency_time - 2,
                'label_x': stop_playing_frequency_time,
                'label_y': (starting_intensity-10)*1.2
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
    def get_Starting_intensity(self, smoothed_recording, stop_frequency_time):
        sampling_rate = 44100
        starting_intensity_value = int((stop_frequency_time)*sampling_rate)-1*sampling_rate
        last_intensity_value = int(stop_frequency_time*sampling_rate)
        values_to_get_avarage_over = smoothed_recording[starting_intensity_value:last_intensity_value]
        starting_intensity = sum(values_to_get_avarage_over)/len(values_to_get_avarage_over)
        return starting_intensity

    @classmethod
    def get_Timestamps_For_Each_Frequency(self, timestamps, frequencies):
        
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
    
    @classmethod
    def process_General_Data_For_Heat_Map(self, file_location: str, frequency: int):
        general_data = open(file_location, 'r').read()
        general_data = json.loads(general_data)

        x_positions_list = []
        y_positions_list = []
        reverberation_time_list = []
        data = general_data["x_value"]
        
        for x_value in data:
            
            column = data[x_value]["y_value"]
            for y_value in column:
                reverberation_test = general_data["x_value"][x_value]["y_value"][y_value]
                
                if int(frequency) in reverberation_test["frequencies"]:
                    frequency_key = str(frequency)
                    
                    time_of_reverberation = reverberation_test["graph_lines"][frequency_key]["vertical_lines"]["reverberation_time"]["x_value"]
                    stop_frequency_time = reverberation_test["graph_lines"][frequency_key]["vertical_lines"]["stop_playing"]["x_value"]
                    reverberation_time = round(((time_of_reverberation-stop_frequency_time)*6), 2)

                    x_positions_list.append(float(x_value))
                    y_positions_list.append(float(y_value))
                    reverberation_time_list.append(float(reverberation_time))
            
        heat_map_dataframe = pd.DataFrame(
            list(
                zip(
                    x_positions_list, 
                    y_positions_list, 
                    reverberation_time_list
                    )
                ), 
            columns=["pos_x", "pos_y", "reverberation_time"]
        )       
        return heat_map_dataframe
    
    @classmethod
    def apply_Calibration_to_recording_data(self, smoothed_recording: list, start_and_stop_time_stamps: dict):
        calibration_data = pd.read_csv("data\calibration\calibration_data.csv").to_dict()
        calibrated_data = []
        start_time = 0
        for start_and_stop_time_stamp in start_and_stop_time_stamps.keys():
            stop_time = start_and_stop_time_stamps[start_and_stop_time_stamp]["stop_frequency_time"]
            for datapoint in smoothed_recording[int(start_time*44100):int(stop_time*44100)]:
                index = -1
                for intensity_point in calibration_data['microphone_intensity'].values():
                    index += 1
                    if intensity_point > datapoint:
                        upper_bound = intensity_point           
                        if index == 0:
                            lower_bound = 0
                        elif index == len(calibration_data['microphone_intensity']) - 1:
                            lower_bound = calibration_data['microphone_intensity'][index-1]
                        else:
                            lower_bound = calibration_data['microphone_intensity'][index-1]
                            
                        
                        span =  upper_bound - lower_bound
                        point = datapoint - lower_bound
                        portion = point/span
                        break
                if index == 0:
                    upper_DB_bound = calibration_data['DB_level'][index]
                    DB_value = upper_DB_bound*portion
                else:
                    lower_DB_bound = calibration_data['DB_level'][index-1]
                    upper_DB_bound = calibration_data['DB_level'][index]
                    DB_value = lower_DB_bound + (upper_DB_bound-lower_DB_bound)*portion
                if DB_value > 100:
                    y = 3
                calibrated_data.append(DB_value)
            start_time = start_and_stop_time_stamps[start_and_stop_time_stamp]["stop_frequency_time"]

        return calibrated_data