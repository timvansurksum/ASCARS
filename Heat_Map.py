import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

class Heat_Map:
    
    def heat_map_data(file_location, frequencie):
        general_data = pd.read_json(file_location).to_dict()

        x_positions_list = []
        y_positions_list = []
        reverberation_time_list = []

        for x_value in general_data["x_value"]:
            for y_value in general_data["x_value"][x_value]["y_value"]:
                reverberation_test = general_data["x_value"][x_value]["y_value"][y_value]
                if frequencie in reverberation_test["frequencies"]:
                    frequencie_key = str(frequencie)
            
                    reverberation_time = round(((reverberation_test["graph_lines"][frequencie_key]["vertical_lines"]["reverberation_time"]["x_value"]-reverberation_test["graph_lines"][frequencie_key]["vertical_lines"]["stop_playing"]["x_value"])*6), 2)

                    x_positions_list.append(float(x_value))
                    y_positions_list.append(float(y_value))
                    reverberation_time_list.append(float(reverberation_time))
            
        heat_map_dataframe = pd.DataFrame(list(zip(x_positions_list, y_positions_list, reverberation_time_list)), columns=["pos_x", "pos_y", "reverberation_time"])       
        return heat_map_dataframe
    

    def heat_mapped(file_location, frequencie):
        imported_data = Heat_Map.heat_map_data(file_location, frequencie)
        transformed_data = imported_data.pivot("pos_x", "pos_y", "reverberation_time")

        sns.heatmap(transformed_data, vmin=0, vmax=2)
        plt.xlabel("Afstand y (m)")
        plt.ylabel("Afstand x (m)")
        plt.show()

Heat_Map.heat_mapped("ASCARS/data/reverberation_data/general_data.json", 400)

