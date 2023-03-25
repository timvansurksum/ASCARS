from manim import *
import numpy as np
class Graphics_Builder(Scene):

    def default(self):
        axes = Axes(
            x_range=[-10, 10.3, 1],
            y_range=[-1.5, 1.5, 1],
            x_length=10,
            axis_config={"color": BLACK},
            tips=False,
        )
        axes_labels = axes.get_axis_labels()
        sin_graph = axes.plot(lambda x: np.sin(x), color=DARK_BLUE)
        cos_graph = axes.plot(lambda x: np.cos(x), color=RED)

        sin_label = axes.get_graph_label(
            sin_graph, "\\sin(x)", x_val=-10, direction=UP / 2
        )
        cos_label = axes.get_graph_label(cos_graph, label="\\cos(x)")




        self.camera.background_color = "#FFC0CB"
        logo_black = "#343434"
        ds_m = MathTex("ASCARS", fill_color=logo_black).scale(6)
        ds_m.shift(2.25 * LEFT + 1.5 * UP)
        logo = VGroup(ds_m)  # order matters
        logo.move_to(ORIGIN)
        plot = VGroup(axes, sin_graph, cos_graph)
        labels = VGroup(axes_labels, sin_label, cos_label)
        self.add(logo, plot, labels)

    def graph_frequency(self, frequency_lines, calibrated_recording, sample_rate):
        self.camera.background_color = "#FFC0CB"
        max_y = frequency_lines['horizontal_lines']['starting_intensity']['y_value'] * 2
        graph_start = frequency_lines['vertical_lines']['stop_playing']['x_value'] - 0.0002
        graph_end = frequency_lines['vertical_lines']['reverberation_time']['x_value'] + 0.05

        axes = Axes(
            x_range=[graph_start, graph_end, 1],
            y_range=[0, max_y , 5],
            axis_config={"color": BLACK},
            y_axis_config={
                "numbers_to_include": np.arange(0, max_y, 5),
                "numbers_with_elongated_ticks": np.arange(-10, max_y, 5),
            },
            x_axis_config={
                "numbers_to_include": np.arange(graph_start, graph_end, 0.1),
                "numbers_with_elongated_ticks": np.arange(graph_start, graph_end, 0.1),
            },
            tips=False
        )
        def intensity(t):
            index = int(t * sample_rate)
            if index  <= len(calibrated_recording) - 1:
                return calibrated_recording[index]
            else:
                return 0
        axes_labels = axes.get_axis_labels()
        data_graph = axes.plot(intensity, x_range=(graph_start, graph_end, 0.0002), color=GRAY, use_smoothing = False)

        data_label = axes.get_graph_label(data_graph, label="sound intensity")

        plot = VGroup(axes, data_graph)
        labels = VGroup(data_label, axes_labels)

        vertical_lines = frequency_lines["vertical_lines"]
        horizontal_lines = frequency_lines["horizontal_lines"]

        for vertical_line_title in vertical_lines.keys():
            vertical_line = vertical_lines[vertical_line_title]
            
            x_value = vertical_line["x_value"]
            y_lower_bound = vertical_line["y_lower_bound"]
            y_upper_bound = vertical_line["y_upper_bound"]

            label_x = vertical_line["label_x"]
            label_y = vertical_line["label_y"]
            
            vert_line = axes.get_vertical_line( axes.i2gp(x_value, max_y), color=YELLOW, line_func=Line )
            line_label = axes.get_graph_label( data_graph, vertical_line_title, x_val=x_value, direction=UR, color=GRAY )
            plot.add(vert_line)
            labels.add(line_label)
                

        # for horizontal_line_title in horizontal_lines.keys():
        #     horizontal_line = horizontal_lines[horizontal_line_title]
            
        #     y_value = horizontal_line["y_value"]
        #     x_lower_bound = horizontal_line["x_lower_bound"]
        #     x_upper_bound = horizontal_line["x_upper_bound"]

        #     label_x = horizontal_line["label_x"]
        #     label_y = horizontal_line["label_y"]

        #     vert_line = axes.get_vertical_line( axes.i2gp(x_value, ), color=YELLOW, line_func=Line )
        #     line_label = axes.get_graph_label( data_graph, vertical_line_title, x_val=x_value, direction=UR, color=GRAY )
        #     plot.add(vert_line)
        #     labels.add(line_label)


        self.add(plot, labels)
