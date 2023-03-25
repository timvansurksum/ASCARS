from manim import *

class Graphics_Builder(Scene):

    def construct(self):
        
        self.camera.background_color = "#FFC0CB"
        logo_green = "#87c2a5"
        logo_blue = "#525893"
        logo_red = "#e07a5f"
        logo_black = "#343434"
        ds_m = MathTex("ASCARS", fill_color=logo_black).scale(6)
        ds_m.shift(2.25 * LEFT + 1.5 * UP)
        # circle = Circle(color=logo_green, fill_opacity=1).shift(LEFT)
        # square = Square(color=logo_blue, fill_opacity=1).shift(UP)
        # triangle = Triangle(color=logo_red, fill_opacity=1).shift(RIGHT)
        logo = VGroup(ds_m)  # order matters
        logo.move_to(ORIGIN)
        self.add(logo)

