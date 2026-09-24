import arcade
import random
import time
import copy
import math
from pathlib import Path
from _thread import *

ASSET_ROOT = Path(__file__).resolve().parent

def asset_path(name):
    return str(ASSET_ROOT / name)

stone = arcade.load_texture(asset_path("images/stone_20x20.png"))
stone_green = arcade.load_texture(asset_path("images/stone_green_20x20.png"))
stone_yellow = arcade.load_texture(asset_path("images/stone_yellow_20x20.png"))
stone_red = arcade.load_texture(asset_path("images/stone_red_20x20.png"))
stone_blue = arcade.load_texture(asset_path("images/stone_blue_20x20.png"))

# Get play more than once defect while streaming=True
sclick = arcade.Sound(asset_path("sounds/Sound_CLICK.WAV"))
sclean = arcade.Sound(asset_path("sounds/message_send_009.wav"))
sall_clean = arcade.Sound(asset_path("sounds/alert_gen_echo_011.wav"))

h_num = 20
w_num = 20

top_block_h = 40

# Keep board geometry independent of the high-resolution sprite assets.
cell_width = 30
cell_height = 30
table_width = w_num * cell_width
table_height = h_num * cell_height

base_x = cell_width  // 2
base_y = cell_height // 2

alpha_begin_minus = 200

stone_matrix = [[0 for y in range(h_num)] for x in range(w_num)]
stone_alpha = [[255 for y in range(h_num)] for x in range(w_num)]
stone_center_cor = [[(0, 0) for y in range(h_num)] for x in range(w_num)]
default_center_cor = [[(0, 0) for y in range(h_num)] for x in range(w_num)]
do_clean = 0 # 1: clean, 0: NOT
down_occur = 0 # 0: NOT down, 1: stone down
score = 0
calc_del_score = []
game_begin = True
    
class awindow(arcade.Window):
    def __init__(self, width: float = 600, height: float = 640, title: str = 'Arcade Window'):
        # Call the parent class initializer
        super().__init__(width, height, title)
        
        self.first_sel = True
        self.selected = 0 # (w, h): selected, 0: NOT
        
        arcade.set_background_color((12, 17, 35))
        self.effect_time = 0.0
        self.particles = []
        self._fading_cells = set()
        self._effect_random = random.Random()
    
    

        # --- Fast text rendering (avoid arcade.draw_text each frame) ---
        self._last_score = None
        self.score_text = arcade.Text(
            text="",
            x=table_width - 170,
            y=table_height + 10,
            color=(255, 223, 110),
            font_size=12,
        )
        self.title_text = arcade.Text("DELETION 44", 14, table_height + 10,
                                      (100, 223, 255), 15, bold=True)

    def setup(self):
        global stone_matrix
        
        for j in range(w_num):
            for i in range(h_num):
                v = random.randint(1, 5)
                stone_matrix[j][i] = v
                
                w = base_x + cell_width * j
                h = base_y + cell_height * i
                stone_center_cor[j][i] = (w, h)
                default_center_cor[j][i] = (w, h)
    
    # True: click mouse button, False: NOT
    def on_click(self, button):
        if button == arcade.MOUSE_BUTTON_LEFT or button == arcade.MOUSE_BUTTON_RIGHT or button == arcade.MOUSE_BUTTON_MIDDLE:
            return True
        else:
            return False
    
    
    def draw_table(self):
        # Draw vertical lines
        for x in range(0, table_width + 1, cell_width):
            arcade.draw_line(x, 0, x, table_height, (30, 43, 64), 1)
        
        # Draw horizontal lines
        for y in range(0, table_height + 1, cell_height):
            arcade.draw_line(0, y, table_width, y, (30, 43, 64), 1)
        
    def draw_selected(self):
        if self.selected != 0:
            if True == self.first_sel:
                #arcade.play_sound(sclick)
                sclick.play()
                self.first_sel = False
        
            (w, h) = self.selected
            left = w * cell_width
            right = left + cell_width
            bottom = h * cell_height
            top = bottom + cell_height
            
            pulse = 0.5 + 0.5 * math.sin(self.effect_time * 6)
            cx, cy = (left + right) / 2, (bottom + top) / 2
            arcade.draw_circle_outline(cx, cy, 13 + pulse * 2,
                                       (255, 218, 80, int(120 + pulse * 100)), 3)
            arcade.draw_lrbt_rectangle_outline(left=left + 1, right=right - 1,
                bottom=bottom + 1, top=top - 1, color=(255, 245, 185), border_width=1)
    
    def draw_stone(self, stone_matrix):
        global stone_center_cor
    
        for x in range(w_num):
            for y in range(h_num):
                istone = index_to_texture(stone_matrix[x][y])
                if istone != None:
                    (w_cor, h_cor) = stone_center_cor[x][y]
                    draw_tex(w_cor, h_cor, cell_width, cell_height, istone, 0, stone_alpha[x][y])
                  
    def clean(self):
        global stone_matrix
        global stone_alpha
        global do_clean
        global calc_del_score
                
        alpha_mark = set()
        do_cl = 0
        for w in range(w_num):
            for h in range(h_num):
                if stone_matrix[w][h] < 1:
                    do_cl = 1
                    do_clean = 1
                
                stone_mark = set()
                stone_mark = calc_seq(stone_matrix[w][h], w, h, stone_matrix, 0, stone_mark)
                if len(stone_mark) >= 5:
                    do_cl = 1
                    do_clean = 1
                    
                    for st in stone_mark:
                        (sw, sh) = st
                        stone_mark2 = set()
                        stone_mark2 = calc_seq(stone_matrix[sw][sh], sw, sh, stone_matrix, 1, stone_mark2)
                    
                        if len(stone_mark2) >= 5:
                            stone_mark = stone_mark | stone_mark2
                else:
                    stone_mark = set()
                    stone_mark = calc_seq(stone_matrix[w][h], w, h, stone_matrix, 1, stone_mark)
                    if len(stone_mark) >= 5:
                        do_cl = 1
                        do_clean = 1
                        
                        for st in stone_mark:
                            (sw, sh) = st
                            stone_mark2 = set()
                            stone_mark2 = calc_seq(stone_matrix[sw][sh], sw, sh, stone_matrix, 0, stone_mark2)
                        
                            if len(stone_mark2) >= 5:
                                stone_mark = stone_mark | stone_mark2
                    else:
                        stone_mark = set()
                
                if (alpha_mark & stone_mark) == set() and stone_mark != set() and stone_mark not in calc_del_score:
                    calc_del_score.append(stone_mark)
                    alpha_mark = alpha_mark | stone_mark
                    
                # clean
                for (sw, sh) in stone_mark:
                    if 255 == stone_alpha[sw][sh]:
                        stone_alpha[sw][sh] = alpha_begin_minus
                    
        if 0 == do_cl:
            do_clean = 0
        else:
            do_clean = 1
    
    def draw_top(self):
        draw_rect_center_filled(
            table_width // 2,
            table_height + top_block_h // 2,
            table_width,
            top_block_h,
            (19, 28, 49),
        )

        # Update text only when score changes (much faster than draw_text every frame)
        if score != self._last_score:
            self.score_text.text = f"SCORE   {(score % 10000000000):10d}"
            self._last_score = score

        self.title_text.draw()
        self.score_text.draw()
        arcade.draw_line(0, table_height, table_width, table_height, (58, 164, 207), 2)

    # override
    def on_draw(self):    
        self.clear()          # 或 arcade.get_window().clear()
        self.draw_table()
        self.draw_stone(stone_matrix)
        self.draw_selected()
        self.draw_effects()
        
        if 0 == down_occur:
            self.clean()
        self.draw_top()
        
        # Finish the render.
        # Nothing will be drawn without this.
        # Must happen after all draw commands
        #arcade.finish_render()
        
    def on_update(self, delta_time):
        self.effect_time += delta_time
        fading = {(x, y) for x in range(w_num) for y in range(h_num)
                  if 0 < stone_alpha[x][y] < 255}
        palette = [(112, 255, 56), (255, 212, 45), (255, 67, 88),
                   (44, 207, 255), (255, 73, 207)]
        for x, y in sorted(fading - self._fading_cells):
            color = palette[max(1, stone_matrix[x][y]) - 1]
            cx, cy = stone_center_cor[x][y]
            for _ in range(5):
                angle = self._effect_random.uniform(0, math.tau)
                speed = self._effect_random.uniform(18, 60)
                self.particles.append([cx, cy, math.cos(angle) * speed,
                    math.sin(angle) * speed, 0.65, color])
        self._fading_cells = fading
        # Cap bursts during a full-board clear.
        self.particles = self.particles[-600:]
        for p in self.particles:
            p[0] += p[2] * delta_time
            p[1] += p[3] * delta_time
            p[3] -= 65 * delta_time
            p[4] -= delta_time
        self.particles = [p for p in self.particles if p[4] > 0]

    def draw_effects(self):
        for x, y, vx, vy, life, color in self.particles:
            if not (0 <= x < table_width and 0 <= y < table_height):
                continue
            alpha = int(255 * life / 0.65)
            arcade.draw_circle_filled(x, y, 3, (*color, alpha // 4))
            arcade.draw_line(x - 2, y, x + 2, y, (*color, alpha), 1)
            arcade.draw_line(x, y - 2, x, y + 2, (255, 255, 225, alpha), 1)

    # override
    def on_mouse_press(self, x, y, button, modifiers):
        global stone_matrix
        
        if 0 == do_clean and 0 == down_occur and self.on_click(button):
        #if self.on_click(button):
            if x < 0 or y < 0 or x >= table_width or y >= table_height:
                self.selected = 0
                self.first_sel = True
            elif 0 == self.selected:
                self.selected = (int(x // cell_width), int(y // cell_height))
            else:
                stone_mark = set()
                (dest_w, dest_h) = (int(x // cell_width), int(y // cell_height))
                dest_w = int(round(dest_w))
                dest_h = int(round(dest_h))
                (org_w, org_h) = self.selected
                org_w = int(round(org_w))
                org_h = int(round(org_h))
                
                if dest_h == org_h:
                    if dest_w == org_w + 1:
                        stone_mark = calc_seq(stone_matrix[dest_w][dest_h], dest_w, dest_h, stone_matrix, 0, stone_mark)
                        if len(stone_mark) >= 3:
                            for (dw, dh) in stone_mark:
                                stone_matrix[dw][dh] = stone_matrix[org_w][org_h]
                            #print(stone_mark)
                            stone_mark = set()
                    elif dest_w == org_w - 1:
                        stone_mark = calc_seq(stone_matrix[dest_w][dest_h], dest_w, dest_h, stone_matrix, 0, stone_mark)
                        if len(stone_mark) >= 3:
                            for (dw, dh) in stone_mark:
                                stone_matrix[dw][dh] = stone_matrix[org_w][org_h]
                            #print(stone_mark)
                            stone_mark = set()

                if dest_w == org_w:
                    if dest_h == org_h + 1:
                        stone_mark = calc_seq(stone_matrix[dest_w][dest_h], dest_w, dest_h, stone_matrix, 1, stone_mark)
                        if len(stone_mark) >= 3:
                            for (dw, dh) in stone_mark:
                                stone_matrix[dw][dh] = stone_matrix[org_w][org_h]
                            #print(stone_mark)
                            stone_mark = set()
                    elif dest_h == org_h - 1:
                        stone_mark = calc_seq(stone_matrix[dest_w][dest_h], dest_w, dest_h, stone_matrix, 1, stone_mark)
                        if len(stone_mark) >= 3:
                            for (dw, dh) in stone_mark:
                                stone_matrix[dw][dh] = stone_matrix[org_w][org_h]
                            #print(stone_mark)
                            stone_mark = set()
                        
                self.selected = 0
                self.first_sel = True

def index_to_texture(index):
    if -1 == index:
        return None
    elif 0 == index:
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

def add_score(num):
    if 5 == num:
        return 5
    elif 10 > num > 5:
        return num * num
    elif 14 > num >= 10:
        return num * num * num
    elif 44 > num >= 14:
        return num * num * num * num
    else:
        return num * num * num * num * num

# dir: 0, horizontal. 1, vertical
def calc_seq(ovalue, ow, oh, stone_matrix, dir, stone_mark):

    if ow >= w_num or oh >= h_num or ow < 0 or oh < 0:
        return stone_mark
    elif None == index_to_texture(stone_matrix[ow][oh]):
        return stone_mark
    elif (ow, oh) not in stone_mark:
        stone_value = stone_matrix[ow][oh]
        
        if ovalue == stone_value:
            stone_mark.add((ow, oh))
            if 0 == dir:
                return calc_seq(ovalue, ow + 1, oh, stone_matrix, dir, stone_mark) | calc_seq(ovalue, ow - 1, oh, stone_matrix, dir, stone_mark)
            else:
                return calc_seq(ovalue, ow, oh + 1, stone_matrix, dir, stone_mark) | calc_seq(ovalue, ow, oh - 1, stone_matrix, dir, stone_mark)
        else:
            return stone_mark
    else:
        return set() 

def stone_alpha_zero():
    global stone_alpha
    global score
    global calc_del_score

    alpha_minus = 25
    dtime = 0.1

    while(True):
        time.sleep(dtime)
        
        for w in range(w_num):
            for h in range(h_num):
                if stone_alpha[w][h] != 255 and stone_alpha[w][h] > 0:
                    stone_alpha[w][h] = stone_alpha[w][h] - alpha_minus if stone_alpha[w][h] - alpha_minus >= 0 else 0
                    dtime = 0.1
                elif stone_alpha[w][h] <= 0:
                    stone_matrix[w][h] = 0
                    stone_alpha[w][h] = 255
                    dtime = 0.1
        
        if calc_del_score != []:
            #print(calc_del_score)
            copy_del_score = copy.deepcopy(calc_del_score)
            #print(len(copy_del_score))
            
            for s in copy_del_score:
                add_done = True # NOT add score
                
                # Check only one element in set s
                for (w, h) in s:
                    if 255 == stone_alpha[w][h] and 0 == stone_matrix[w][h]:
                        add_done = False # wait to add score
                    break
                        
                if not add_done:
                    #arcade.play_sound(sclean)
                    sclean.play()
                    score += add_score(len(s))
                    calc_del_score.remove(s)
                    dtime = 0.5
        
        

def down():
    global down_occur
    movement = 5# for stone down
    dtime = 0.07

    while(True):
        time.sleep(dtime)
        move_process = 0
        
        if [] == calc_del_score:
            for w in range(w_num):
                for h in range(h_num):
                    if stone_center_cor[w][h] != default_center_cor[w][h]:
                        move_process = 1
                        down_occur = 1
                        (x, y) = stone_center_cor[w][h]
                        stone_center_cor[w][h] = (x, y - movement)
                        dtime = 0.07
                        
            if 1 == move_process:
                continue
            
            for w in range(w_num):
                for h in range(h_num):
                    if 0 == stone_matrix[w][h]:
                        move_process = 1
                        down_occur = 1
                        new = random.randint(1, 5)
                        stone_matrix[w].append(new)
                        stone_matrix[w][h:] = stone_matrix[w][h+1:]
                        
                        (nx, ny) = default_center_cor[w][h_num - 1]
                        ny += cell_height
                        stone_center_cor[w].append((nx, ny))
                        stone_center_cor[w][h:] = stone_center_cor[w][h+1:]
                        dtime = 0.07
                        break
                        
            if 0 == move_process:
                down_occur = 0
                do_clean = 0
                dtime = 1

def check_hard_del():
    global stone_alpha
    
    while True:
        time.sleep(2)
        
        del_num = 0
        
        if 1 == do_clean or 1 == down_occur:
            continue
        
        for w in range(w_num):
            for h in range(h_num):
                stone_mw = set()
                stone_mh = set()
                stone_mw = calc_seq(stone_matrix[w][h], w, h, stone_matrix, 0, stone_mw)
                stone_mh = calc_seq(stone_matrix[w][h], w, h, stone_matrix, 1, stone_mh)
                
                if len(stone_mw) >= 3:
                    del_num += 1
                if len(stone_mh) >= 3:
                    del_num += 1
                    
        #print(del_num)
        #if True:
        if del_num < 9:
            # delete all
            #arcade.play_sound(sall_clean)
            sall_clean.play()
            
            for w in range(w_num):
                for h in range(h_num):
                    stone_alpha[w][h] = alpha_begin_minus
            
            time.sleep(5)

def draw_rect_center_filled(cx, cy, w, h, color, angle=0):
    # Arcade 3.x：用 Rect + draw_rect_filled
    if hasattr(arcade, "draw_rect_filled") and hasattr(arcade, "XYWH"):
        arcade.draw_rect_filled(arcade.XYWH(cx, cy, w, h), color, tilt_angle=angle)
    # 舊版 Arcade（如果你哪天換回去）
    else:
        arcade.draw_rectangle_filled(cx, cy, w, h, color, angle)

def draw_tex(w, h, cw, ch, tex, angle=0, alpha=255):
    # 確保 alpha 是 0~255 的 int
    alpha = max(0, min(255, int(alpha)))

    # Arcade 3.x: draw_texture_rect(texture, rect, *, angle=..., alpha=...)
    if hasattr(arcade, "draw_texture_rect"):
        rect = arcade.XYWH(w, h, cw, ch)   # 通常 w,h 直接用「中心座標」
        arcade.draw_texture_rect(tex, rect, angle=angle, alpha=alpha)
    else:
        # 舊版 Arcade
        arcade.draw_texture_rectangle(w, h, cw, ch, tex, angle, alpha)
    
def main():
    window = awindow(table_width, table_height + top_block_h, "Deletion 44")
    window.setup()
    start_new_thread(stone_alpha_zero, ())
    start_new_thread(down, ())
    start_new_thread(check_hard_del, ())
    
    # Keep the window up until someone closes it.
    arcade.run()

if __name__ == "__main__":
    main()