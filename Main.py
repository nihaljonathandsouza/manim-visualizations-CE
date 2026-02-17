from manim import *

class Chocolatte(Scene):
    def construct(self):
        num_rows = 6
        num_cols = 4
        bar_width = 3.5 / num_cols
        bar_height = 5.0 / num_rows  
        plane=NumberPlane()
        chocolate_bar = Rectangle(
            width=bar_width * num_cols,
            height=bar_height * num_rows,
            stroke_width=1,
            color=WHITE,
            fill_color="#7B3F00",
            fill_opacity=1,
        )
         #DO NOT TOUCH THIS PART , INDENTED WITH CARE!!!
        text0=Text('The Infinite Chocolate Trick.')
        text3=Text('''
                      Consider this chocolate bar,  
                      having 6 rows and 4 columns,                      
                      resulting in 24 equally divided
                      pieces of the same.''',line_spacing=1.5).shift(UP * 0.2 +LEFT * 3 ).scale(0.6)
        text4=Text('''
                        
                   
                     Now we cut the 
                        bar diagonally 
                                                        
                   
                                                                                                    
                   
                   
                                                                                        across the 4th row 
                                                                                         from the top ''',line_spacing=0.5).shift(UP * 0.4+LEFT* 0.1 ).scale(0.6)
        text5=Text('''
                        
                We are then left with   
                   
                                                                               

                   

                   
                                 And
                    
                                                                                            
                                                      
    The Lower half                                                        ''',).shift(UP *0.6 + LEFT * 1.5).scale(0.75)
        
        
         # Create the grid lines for the larger chocolate bar
        grid_lines = VGroup(
            *[Line(start=chocolate_bar.get_corner(UL) + i * bar_width * RIGHT, end=chocolate_bar.get_corner(DL) + i * bar_width * RIGHT, stroke_color=BLACK) for i in range(1, num_cols)],
            *[Line(start=chocolate_bar.get_corner(UL) - i * bar_height * UP, end=chocolate_bar.get_corner(UR) - i * bar_height * UP, stroke_color=BLACK) for i in range(1, num_rows)]
        )

        # Create a group to combine the chocolate bar and grid lines
        chocolate_group = VGroup(chocolate_bar, grid_lines).shift(RIGHT * 3)
        
        self.play(AddTextLetterByLetter(text0))
        
        self.wait(1)

        self.play(FadeOut(text0))

        
        # Animate the creation of the larger chocolate bar and grid lines
        self.play(AnimationGroup(Create(chocolate_group),rate_func=linear),Create(text3),run_time=7)
       
        #Animate the numbers
        # Calculate the centers of each chocolate piece
        centers = [] 
        for i in range(num_rows):
            for j in range(num_cols):
                center_x = chocolate_bar.get_x() + (j + 0.5) * bar_width - chocolate_bar.width / 2
                center_y = chocolate_bar.get_y() - (i + 0.5) * bar_height + chocolate_bar.height / 2
                centers.append(np.array([center_x, center_y, 0]))  # Add a z-coordinate to make it 3D

        # Create text elements and place them at the center of each chocolate piece
        texts = []
        for i in range(1, 25):
            text = Text(str(i), font_size=30)
            text.move_to(centers[i-1])
            texts.append(text)

        # Create a VGroup to hold all the text objects
        text_group = VGroup(*texts)
             
        self.play(Create(text_group), run_time=5)
        self.wait(1)  # Wait for 1 second
        self.play(FadeOut(text_group),FadeOut(text3),run_time=1)

        # Calculate the starting and ending points for the diagonal cut on the 3rd grid
        grid_start = chocolate_bar.get_corner(UL) - 4 * bar_height * UP  # Start from the 3rd grid
        grid_end = chocolate_bar.get_corner(DR) + 3 * bar_height * UP # End at the bottom-right corner

        arrow_1 = Arrow(start=LEFT * 2.85 + DOWN * 0.82, end=LEFT * 1.75 + DOWN * 0.82, buff=0)
        arrow_2 = Arrow(start=RIGHT * 2.85,end=RIGHT * 1.75,buff=0)
        
        self.play(ApplyMethod(chocolate_group.shift,LEFT*3))
        #Made the arrows come in at the same time and the Script4 too
        self.play(AnimationGroup(Create(arrow_1),Create(arrow_2),rate_func=rush_from),Create(text4),run_time=2)

        self.wait(3)
    
        # Dashed diagonal line to simulate cutting
        diagonal1 = DashedLine(grid_start, grid_end, color=WHITE, stroke_width=2)  
        diagonal = DashedLine(arrow_1.get_end(), arrow_2.get_end(), color=WHITE, stroke_width=2)

        #self.play(Create(diagonal1),TransformFromCopy(arrow_1, diagonal), TransformFromCopy(arrow_2, diagonal), rate_func=smooth, run_time=2)
        self.play(Create(diagonal))
        self.play(FadeOut(arrow_1), FadeOut(arrow_2),rate_func=rush_into,run_time=0.5)

        self.play(AnimationGroup(Uncreate(diagonal),rate_func=there_and_back),FadeOut(text4),run_time=2)
        self.play(FadeOut(chocolate_group))
        
        # Define the shapes of the new polygon (P) as lists of vertices
        P = [
            [-4, -3, 0],  
            [4, -3, 0],   
            [4, 3, 0],    
            [-4, 1, 0],
        ]

        # Lower half
        outline_poly_P = Polygon(*[np.array(vertex) for vertex in P], fill_opacity=1, fill_color="#7B3F00", stroke_color=YELLOW, stroke_opacity=1)
        outline_poly_P.move_to(ORIGIN)

        # Define the shapes of the second polygon (C) as lists of vertices
        C = [
            [-4, -4.5, 0], 
            [4, -3, 0],   
            [4, 3, 0],    
            [-4, 3, 0],
        ]

        # upper half
        outline_poly_C = Polygon(*[np.array(vertex) for vertex in C], fill_opacity=1, fill_color="#7B3F00", stroke_color=WHITE, stroke_opacity=1)
        outline_poly_C.move_to(ORIGIN)

        # grid lines of the new polygons
        grid_lines_P = VGroup(
            *[Line(start=outline_poly_P.get_corner(UL) + i * (8 / 4) * RIGHT, end=outline_poly_P.get_corner(DL) + i * (8 / 4) * RIGHT , stroke_color=BLACK) for i in range(1, 4)],
            *[Line(start=outline_poly_P.get_corner(UL) - i * (6 / 3) * UP, end=outline_poly_P.get_corner(UR) - i * (6 / 3) * UP , stroke_color=BLACK) for i in range(1, 3)]
        )
        # Calculate the coordinates for the grid lines of the second polygon (C)
        grid_lines_C = VGroup(
            *[Line(start=outline_poly_C.get_corner(UL) + i * (8 / 4) * RIGHT, end=outline_poly_C.get_corner(DL) + i * (8 / 4) * RIGHT , stroke_color=BLACK) for i in range(1, 4)],
            *[Line(start=outline_poly_C.get_corner(UL) - i * (6 / 3) * UP, end=outline_poly_C.get_corner(UR) - i * (6 / 3) * UP , stroke_color=BLACK) for i in range(1, 4)]
        )
        
        # scaling down the polygons and grid lines proportionally
        scale_factor = 0.5  
        outline_poly_P.scale(scale_factor)
        grid_lines_P.scale(scale_factor)
        outline_poly_C.scale(scale_factor)
        grid_lines_C.scale(scale_factor)

        # side by side placement
        poly_group_B = VGroup(outline_poly_P, grid_lines_P)
        poly_group_B.move_to(LEFT * 3)
        poly_group_C = VGroup(outline_poly_C, grid_lines_C)
        poly_group_C.move_to(RIGHT * 3)

        vg = VGroup(poly_group_C,poly_group_B)

        self.play(FadeIn(poly_group_B),FadeIn(poly_group_C))

        text7=Text("The Upper half").next_to(poly_group_C,UP).scale(0.75)

        self.play(Create(text5),run_time=1.5)

        self.play(Create(text7))

        self.wait(2)
        
        # Fade out poly_group_B and poly_group_C)
    
        self.play(FadeOut(text5),FadeOut(poly_group_B))
        
        self.play(ApplyMethod(poly_group_C.shift,3 * LEFT),ApplyMethod(text7.shift,3 * LEFT),rate_func=linear,run_time=2)
        
        self.wait(2)

        self.play(FadeOut(text7))  

        # Define the vertices for the cut
        D = [
            [-1, -3.75, 0],  # Bottom-left corner
            [1, -3.25, 0],   # Bottom-right corner
            [1, 3.25, 0],    # Top-right corner
            [-1, 3.25, 0],   # Top-left corner
        ]

        # Create poly D and its grid lines
        outline_poly_D = Polygon(*[np.array(vertex) for vertex in D], fill_opacity=1, fill_color="#7B3F00", stroke_color=WHITE, stroke_opacity=1)
        outline_poly_D.move_to(ORIGIN)

        grid_lines_D = VGroup(
            *[Line(start=outline_poly_D.get_corner(UL) + i * (0) * RIGHT, end=outline_poly_D.get_corner(DL) + i * (0) * RIGHT, stroke_color=WHITE, stroke_opacity=0) for i in range(1, 2)],
            *[Line(start=outline_poly_D.get_corner(UL) - i * (7 / 4) * UP, end=outline_poly_D.get_corner(UR) - i * (7 / 4) * UP, stroke_color=BLACK) for i in range(1, 4)]
        )
        grid_lines_D.scale(scale_factor)
        outline_poly_D.scale(scale_factor)

        # Create a group for poly D and its grid lines
        poly_group_D = VGroup(outline_poly_D, grid_lines_D)
        poly_group_D.move_to(ORIGIN)
        
        # Perform the straight cut through the first column of poly_group_C
        cut_start = outline_poly_C.get_corner(UL) + RIGHT * (1 / 1)  # Start of the first column
        cut_end = outline_poly_C.get_corner(DL) + RIGHT * (1 / 1)  # End of the first column
        cut_line = DashedLine(cut_start, cut_end, color=WHITE, stroke_width=2)
        
        text8=Text('''
                        Our objective here is to remove a piece of Chocolate 
                             from the top left corner of the Chocolate Bar''',line_spacing=1).scale(0.75).shift(UP * 3.15)
        
        self.play(Create(cut_line),Create(text8),run_time=3)
        self.wait(1)
        self.play(Uncreate(cut_line),rate_func=there_and_back)

        # Transform poly_group_C to poly_group_D
        self.play(Transform(poly_group_C, poly_group_D), rate_func=linear, run_time=1)
        self.add(poly_group_D)
        self.wait(2)
        
        # Define the vertices for poly E
        E = [
            [-1, -3.25, 0],  # Bottom-left corner
            [1, -2.75, 0],   # Bottom-right corner
            [1, 2.75, 0],    # Top-right corner
            [-1, 2.75, 0],   # Top-left corner
        ]

        # Create poly E and its grid lines
        outline_poly_E = Polygon(*[np.array(vertex) for vertex in E], fill_opacity=1, fill_color="#7B3F00", stroke_color=RED, stroke_opacity=1)
        grid_lines_E = VGroup(
            *[Line(start=outline_poly_E.get_corner(UL) + i * (0) * RIGHT, end=outline_poly_E.get_corner(DL) + i * (0) * RIGHT, stroke_color=BLACK) for i in range(1, 1)],
            *[Line(start=outline_poly_E.get_corner(UL) - i * (4 / 2) * UP, end=outline_poly_E.get_corner(UR) - i * (4 / 2) * UP, stroke_color=BLACK) for i in range(1, 3)]
        )
        grid_lines_E.scale(scale_factor)
        outline_poly_E.scale(scale_factor)

        # Create a group for poly E and its grid lines
        poly_group_E = VGroup(outline_poly_E, grid_lines_E)
        poly_group_E.move_to(ORIGIN)

        # Perform the straight cut through the second column of poly_group_D to get poly_group_E
        cut_start = outline_poly_D.get_corner(UL) + DOWN * 0.87  # Start of the second row
        cut_end = outline_poly_D.get_corner(UR) + DOWN * 0.87 # End of the second row
        cut_line = DashedLine(cut_start, cut_end, color=WHITE, stroke_width=2)
        self.play(Create(cut_line))
        self.wait(1)
        self.play(Uncreate(cut_line),rate_func=there_and_back)

        F = [
            [-1, -1, 0],  # Bottom-left corner
            [1, -1, 0],   # Bottom-right corner
            [1, 1, 0],    # Top-right corner
            [-1, 1, 0],   # Top-left corner
        ]

        outline_poly_F = Polygon(*[np.array(vertex) for vertex in F], fill_opacity=1, fill_color="#7B3F00", stroke_color=WHITE, stroke_opacity=1)
        outline_poly_F.scale(scale_factor)
        outline_poly_F.move_to(LEFT * 4 + UP * 1)
        poly_group_E.move_to(RIGHT * 4 )

        self.remove(poly_group_C)
        
        text8d=Text('''
                                                  Finally we have   
                        ''').scale(0.75).move_to(ORIGIN + UP * 3.6)
        text8a=Text("The Corner piece").scale(0.65).next_to(outline_poly_F,UP)
        text8b=Text("And").move_to(ORIGIN).scale(0.75)
        text8c=Text("The Remaining piece ").next_to(poly_group_E,UP).scale(0.65)
      
        # Transform poly_group_D to poly_group_E
        self.play(AnimationGroup(FadeOut(poly_group_D), rate_func=smooth),FadeOut(text8), run_time=1)
        self.play(FadeIn(poly_group_E),FadeIn(outline_poly_F),rate_func=smooth, run_time=1)
        self.play(Create(text8d),Create(text8a),Create(text8b),Create(text8c))

        self.wait(4)
        
        self.play(FadeOut(poly_group_E),FadeOut(outline_poly_F),FadeOut(text8d),FadeOut(text8a),FadeOut(text8b),FadeOut(text8c))

        A = [
            [-3, -4.49, 0],  
            [3, -3, 0],   
            [3, 3, 0],    
            [-3, 3, 0],
        ]

        outline_poly_A = Polygon(*[np.array(vertex) for vertex in A], fill_opacity=1, fill_color="#7B3F00", stroke_color=BLUE, stroke_opacity=1)
        grid_lines_A = VGroup(
            *[Line(start=outline_poly_A.get_corner(UL) + i * (8 / 4) * RIGHT, end=outline_poly_A.get_corner(DL) + i * (8 / 4) * RIGHT, stroke_color=BLACK) for i in range(1, 3)],
            *[Line(start=outline_poly_A.get_corner(UL) - i * (6 / 3) * UP, end=outline_poly_A.get_corner(UR) - i * (6 / 3) * UP, stroke_color=BLACK) for i in range(1, 4)]
        )

        # Create a group for poly A and its grid lines
        poly_group_A = VGroup(outline_poly_A, grid_lines_A)
        poly_group_A.scale(scale_factor)
    
        self.wait(2)

        texme = Text('''
                                                    Putting it all together   
                        ''').scale(0.75).move_to(ORIGIN + UP * 3.6)
        
        poly_group_B.move_to(LEFT * 4)
        poly_group_E.move_to(ORIGIN)
        outline_poly_F.move_to(RIGHT * 2)
        poly_group_A.move_to(RIGHT * 5)

        self.play(Create(texme))

        # Display the polygons
        self.play(Create(poly_group_B),rate_func=linear,run_time=3)
        self.play(Create(poly_group_A),rate_func=linear,run_time=2)
        self.play(Create(poly_group_E),rate_func=linear,run_time=1)
        self.play(Create(outline_poly_F),rate_func=smooth,run_time=1)
        
        text9=Text(''' 
                                Let us now rearrange the pieces to get an 
                                       Extra Piece from the Chocolate Bar!''',line_spacing=0.5).scale(0.6).shift(3.2 * UP+LEFT * 0.6)
        

        self.wait(2)
      
        self.play(ApplyMethod(poly_group_B.shift,4 * RIGHT,2 * DOWN),rate_func=smooth,run_time=1)
        self.play(ApplyMethod(poly_group_E.shift,LEFT * 1.5,0.003 * UP),rate_func=smooth,run_time=1)
        self.play(ApplyMethod(outline_poly_F.shift,3.5 * LEFT,2.005 * UP),rate_func=smooth,run_time=1)
        self.play(ApplyMethod(poly_group_A.shift,4.495 * LEFT,0.635 * UP),rate_func=rush_into,run_time=1)
        self.wait(2)
        self.play(Uncreate(texme))
        self.wait(2)

        self.play(Create(text9),run_time=2)

        self.wait(1)

        self.play(FadeOut(text9))
        
        self.play(ApplyMethod(outline_poly_F.shift,4 * LEFT,),rate_func=smooth,run_time=1)
        self.play(ApplyMethod(poly_group_A.shift,1.008 * LEFT,0.225 * DOWN),rate_func=smooth,run_time=2)
        self.play(ApplyMethod(poly_group_E.shift,RIGHT * 3, 0.775 * UP),rate_func=smooth,run_time=1)

        self.wait(2)

        polys=VGroup(poly_group_B,poly_group_E,poly_group_A)
        self.play(ApplyMethod(polys.shift,RIGHT * 3),rate_func=smooth,run_time=2)
        self.play(ApplyMethod(outline_poly_F.shift,2 * RIGHT,2*DOWN),rate_func=smooth,run_time=1)
        text10=Text("Voila! We have an Extra piece for ourselves now!").scale(0.75).shift(3.2*UP)
        self.play(Create(text10),run_time=2)
        self.wait(1)
        self.play(FadeOut(text10))
        texyou = Text('''And thats how you can have a piece of chocolate
                           without anyone noticing, ヽ(^o^)丿 !! ''').scale(0.7).shift(3.2*UP)
        self.play(AddTextLetterByLetter(texyou))
        self.wait(3) 
