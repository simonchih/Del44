import arcade
import os
import random

stone = arcade.load_texture("images/stone_20x20.gif")
stone_green = arcade.load_texture("images/stone_green_20x20.gif")
stone_yellow = arcade.load_texture("images/stone_yellow_20x20.gif")
stone_red = arcade.load_texture("images/stone_red_20x20.gif")
stone_blue = arcade.load_texture("images/stone_blue_20x20.gif")

def index_to_texture(index):
    if 0 == index:
        return stone
    elif 1 == index:
        return stone_green
    elif 2 == index:
        return stone_yellow
    elif 3 == index:
        return stone_red
    elif 4 == index:
        return stone_blue

def main():
    # Set the working directory (where we expect to find files) to the same
    # directory this .py file is in. You can leave this out of your own
    # code, but it is needed to easily run the examples using "python -m"
    # as mentioned at the top of this program.
    file_path = os.path.dirname(os.path.abspath(__file__))
    os.chdir(file_path)
    
    h_num = 20
    w_num = 20
    
    stone_matrix = [[0 for x in range(w_num)] for y in range(h_num)]

    for i in range(h_num):
        for j in range(w_num):
            v = random.randint(0, 4)
            stone_matrix[i][j] = v
    
    s = 1.5 #scale
    top_block_h = 40
    istone = index_to_texture(stone_matrix[0][0])
    
    cell_width = int(s*istone.width)
    cell_height = int(s*istone.height)
    
    table_width = w_num * cell_width
    table_height = h_num * cell_height
    
    # Open the window. Set the window title and dimensions (width and height)
    arcade.open_window(table_width, table_height + top_block_h, "Deletion 44")
    
    # Set the background color to white
    # For a list of named colors see
    # http://arcade.academy/arcade.color.html
    # Colors can also be specified in (red, green, blue) format and
    # (red, green, blue, alpha) format.
    arcade.set_background_color(arcade.color.WHITE)
    
    # Start the render process. This must be done before any drawing commands.
    arcade.start_render()
    
    # Draw a grid
    # Draw vertical lines every 120 pixels
    for x in range(0, table_width + 1, cell_width):
        arcade.draw_line(x, 0, x, table_height, arcade.color.BLACK, 1)
    
    # Draw horizontal lines every 200 pixels
    for y in range(0, table_height + 1, cell_height):
        arcade.draw_line(0, y, table_width, y, arcade.color.BLACK, 1)
    
    base_x = cell_width  // 2
    base_y = cell_height // 2
    
    for y in range(h_num):
        for x in range(w_num):
            istone = index_to_texture(stone_matrix[y][x])
            arcade.draw_texture_rectangle(base_x + cell_width * x, base_y + cell_height * y, cell_width, cell_height, istone, 0)
       
    # Draw a point
    #arcade.draw_text("draw_point", 3, 405, arcade.color.BLACK, 12)
    #arcade.draw_point(60, 495, arcade.color.RED, 10)
    
    # Finish the render.
    # Nothing will be drawn without this.
    # Must happen after all draw commands
    arcade.finish_render()
    
    # Keep the window up until someone closes it.
    arcade.run()

if __name__ == "__main__":
    main()