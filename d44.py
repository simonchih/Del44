import arcade
import os
import random

stone = arcade.load_texture("images/stone_20x20.gif")
stone_green = arcade.load_texture("images/stone_green_20x20.gif")
stone_yellow = arcade.load_texture("images/stone_yellow_20x20.gif")
stone_red = arcade.load_texture("images/stone_red_20x20.gif")
stone_blue = arcade.load_texture("images/stone_blue_20x20.gif")

h_num = 20
w_num = 20

s = 1.5 #scale
top_block_h = 40

cell_width = int(s*stone.width)
cell_height = int(s*stone.height)
table_width = w_num * cell_width
table_height = h_num * cell_height
    
class awindow(arcade.Window):
    def __init__(self, width: float = 600, height: float = 640, title: str = 'Arcade Window'):
        # Call the parent class initializer
        super().__init__(width, height, title)
        
        # Set the working directory (where we expect to find files) to the same
        # directory this .py file is in. You can leave this out of your own
        # code, but it is needed to easily run the examples using "python -m"
        # as mentioned at the top of this program.
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)
        
        self.selected = 0 # (w, h): selected, 0: NOT
        self.stone_matrix = [[0 for y in range(h_num)] for x in range(w_num)]
        
        # Set the background color to white
        # For a list of named colors see
        # http://arcade.academy/arcade.color.html
        # Colors can also be specified in (red, green, blue) format and
        # (red, green, blue, alpha) format.
        arcade.set_background_color(arcade.color.WHITE)
    
    def setup(self):
        for i in range(h_num):
            for j in range(w_num):
                v = random.randint(1, 5)
                self.stone_matrix[j][i] = v
    
    # True: click mouse button, False: NOT
    def on_click(self, button):
        if button == arcade.MOUSE_BUTTON_LEFT or button == arcade.MOUSE_BUTTON_RIGHT or button == arcade.MOUSE_BUTTON_MIDDLE:
            return True
        else:
            return False
    
    
    def draw_table(self):
        # Draw vertical lines every 120 pixels
        for x in range(0, table_width + 1, cell_width):
            arcade.draw_line(x, 0, x, table_height, arcade.color.BLACK, 1)
        
        # Draw horizontal lines every 200 pixels
        for y in range(0, table_height + 1, cell_height):
            arcade.draw_line(0, y, table_width, y, arcade.color.BLACK, 1)
        
    def draw_selected(self):
        if self.selected != 0:
            (w, h) = self.selected
            left = w * cell_width
            right = left + cell_width
            bottom = h * cell_height
            top = bottom + cell_height
            
            arcade.draw_lrtb_rectangle_outline(left = left, right = right, top = top, bottom = bottom, color = arcade.color.ALABAMA_CRIMSON, border_width = 2)        
    
    def draw_stone(self, stone_matrix):
        base_x = cell_width  // 2
        base_y = cell_height // 2
    
        for x in range(w_num):
            for y in range(h_num):
                istone = index_to_texture(stone_matrix[x][y])
                arcade.draw_texture_rectangle(base_x + cell_width * x, base_y + cell_height * y, cell_width, cell_height, istone, 0)
                  
    # override
    def on_draw(self):    
        arcade.start_render()
        self.draw_table()
        self.draw_stone(self.stone_matrix)
        self.draw_selected()
        
        # Finish the render.
        # Nothing will be drawn without this.
        # Must happen after all draw commands
        #arcade.finish_render()
        
    # override
    def on_mouse_press(self, x, y, button, modifiers):
        if self.on_click(button):
            if x >= table_width or y >= table_height:
                self.selected = 0
            elif 0 == self.selected:
                self.selected = (x // 30, y // 30)
            else:
                stone_mark = set()
                (dest_w, dest_h) = (x // 30, y // 30)
                (org_w, org_h) = self.selected
                
                if dest_h == org_h:
                    if dest_w == org_w + 1:
                        stone_mark = calc_seq(self.stone_matrix[dest_w][dest_h], dest_w, dest_h, self.stone_matrix, 0, stone_mark)
                        if len(stone_mark) >= 3:
                            for (dw, dh) in stone_mark:
                                self.stone_matrix[dw][dh] = self.stone_matrix[org_w][org_h]
                            #print(stone_mark)
                            stone_mark = set()
                    elif dest_w == org_w - 1:
                        stone_mark = calc_seq(self.stone_matrix[dest_w][dest_h], dest_w, dest_h, self.stone_matrix, 0, stone_mark)
                        if len(stone_mark) >= 3:
                            for (dw, dh) in stone_mark:
                                self.stone_matrix[dw][dh] = self.stone_matrix[org_w][org_h]
                            #print(stone_mark)
                            stone_mark = set()

                if dest_w == org_w:
                    if dest_h == org_h + 1:
                        stone_mark = calc_seq(self.stone_matrix[dest_w][dest_h], dest_w, dest_h, self.stone_matrix, 1, stone_mark)
                        if len(stone_mark) >= 3:
                            for (dw, dh) in stone_mark:
                                self.stone_matrix[dw][dh] = self.stone_matrix[org_w][org_h]
                            #print(stone_mark)
                            stone_mark = set()
                    elif dest_h == org_h - 1:
                        stone_mark = calc_seq(self.stone_matrix[dest_w][dest_h], dest_w, dest_h, self.stone_matrix, 1, stone_mark)
                        if len(stone_mark) >= 3:
                            for (dw, dh) in stone_mark:
                                self.stone_matrix[dw][dh] = self.stone_matrix[org_w][org_h]
                            #print(stone_mark)
                            stone_mark = set()
                        
                self.selected = 0

def index_to_texture(index):
    if 0 == index:
        return None
    elif 1 == index:
        return stone_green
    elif 2 == index:
        return stone_yellow
    elif 3 == index:
        return stone_red
    elif 4 == index:
        return stone_blue
    elif 5 == index:
        return stone

# dir: 0, horizontal. 1, vertical
def calc_seq(ovalue, ow, oh, stone_matrix, dir, stone_mark):
    stone_value = stone_matrix[ow][oh]
    
    if 0 == index_to_texture(stone_value):
        return stone_mark
    elif (ow, oh) not in stone_mark:
        if ovalue == stone_value:
            stone_mark.add((ow, oh))
            if 0 == dir:
                return calc_seq(ovalue, ow + 1, oh, stone_matrix, dir, stone_mark) | calc_seq(ovalue, ow - 1, oh, stone_matrix, dir, stone_mark)
            else:
                return calc_seq(ovalue, ow, oh + 1, stone_matrix, dir, stone_mark) | calc_seq(ovalue, ow, oh - 1, stone_matrix, dir, stone_mark)
        else:
            return stone_mark
    else:
        return stone_mark    
        
def main():
    window = awindow(table_width, table_height + top_block_h, "Deletion 44")
    window.setup()   
    
    # Keep the window up until someone closes it.
    arcade.run()

if __name__ == "__main__":
    main()