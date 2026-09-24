"""Title screen and self-paced tutorial; independent of the live board/workers."""
from pathlib import Path
import math
import arcade

ROOT = Path(__file__).resolve().parent
FONT = ("Segoe UI", "Arial")
WHITE = (236, 244, 255)
MUTED = (157, 180, 203)
GOLD = (255, 217, 116)
CYAN = (92, 225, 239)

# The diagrams deliberately use the real game's textures and copy direction.
LESSONS = [
    ("Small moves. Big connections.", "Copy a color. Connect a line. Watch it clear.", [
        "You copy colors between stones instead of swapping them.",
        "Choose a source, then a neighbor to recolor its whole run.",
        "A straight line of 5 or more matching stones will clear."], "overview"),
    ("01 / Choose your source", "Try it: click the green stone on the left.", [
        "The source stone supplies the color you want to copy.",
        "A gold outline marks your selected stone during play.",
        "Practice here safely: this does not affect your game score."], "source"),
    ("02 / Choose a neighbor", "Try it: click green, then the yellow stone beside it.", [
        "Choose directly above, below, left or right. No diagonals.",
        "Left / right checks a row. Up / down checks a column.",
        "Click the second stone: only that yellow touches the source."], "target"),
    ("Three to copy", "The target must belong to a run of at least 3 matching stones.", [
        "The entire target run changes to match the source color.",
        "The source stays in place; the stones do not swap.",
        "1 source + 3 targets = 4 matching stones. No clear yet!"], "copy"),
    ("Five to clear", "One more connection makes all the difference.", [
        "1 source + 4 targets can create a line of 5 matching stones.",
        "Rows and columns count, including qualifying crossing lines.",
        "Diagonal lines and clusters alone do not trigger a clear."], "clear"),
    ("Let the stones settle", "Clear, fall, refill... and look for your next move.", [
        "Stones fall into empty spaces. New stones enter from above.",
        "Another line of 5 or more will clear automatically.",
        "Wait for clearing and falling to finish before clicking again."], "fall"),
    ("Bigger clears. Bigger scores.", "Each cleared group earns points based on its size, n.", [
        "5 stones: 5 points   |   6–9 stones: n squared",
        "10–13: n cubed   |   14–43: n to the fourth power",
        "44 or more: n to the fifth. 44 stones = 164,916,224 points!",
        "Two separate groups of 5 earn 5 + 5 = 10 points."], "score"),
    ("No copy? Try a new source.", "Check the direction, then count the target's matching run.", [
        "A non-neighbor or a target run shorter than 3 cannot copy.",
        "The second click resets selection. Choose a source again.",
        "Too few usable matching runs? The board clears itself.",
        "This automatic full clear earns no points. Wait for the refill."], "invalid"),
    ("Your next move awaits.", "Look for a long run, then a useful source beside it.", [
        "1. Choose a source.   2. Choose an adjacent target.",
        "3. Copy a run of 3+.   4. Clear a line of 5+.   5. Let it settle.",
        "Build longer lines and crossings. Aim for a 44-stone clear!",
        "Take your time. Go Back to review, or Esc to the main menu."], "ready"),
]


class FrontEnd:
    def __init__(self, window):
        self.window = window
        self.background = arcade.load_texture(ROOT / "images/menu-background.png")
        self.gems = [arcade.load_texture(ROOT / "images" / name) for name in (
            "stone_green_20x20.png", "stone_yellow_20x20.png",
            "stone_red_20x20.png", "stone_blue_20x20.png", "stone_20x20.png")]
        self.page = None
        self.time = 0.0
        self.mouse = (-1, -1)
        self.focus = 0
        self.practice = 0
        self.texts = {}

    def text(self, value, x, y, size=14, color=WHITE, center=False, bold=False):
        key = (value, x, y, size, color, center, bold)
        if key not in self.texts:
            self.texts[key] = arcade.Text(value, x, y, color, size,
                font_name=FONT, bold=bold, anchor_x="center" if center else "left")
        self.texts[key].draw()

    def rect(self, x, y, w, h, color):
        arcade.draw_rect_filled(arcade.XYWH(x, y, w, h), color)

    def buttons(self):
        if self.page is None:
            return [("Start Game", 300, 174, 352, 58, "start"),
                    ("Tutorial", 300, 102, 352, 52, "tutorial")]
        return [("Menu", 99, 51, 122, 44, "menu"),
                ("Back", 239, 51, 122, 44, "back"),
                ("Start Game" if self.page == len(LESSONS) - 1 else "Next",
                 445, 51, 228, 44, "start" if self.page == len(LESSONS) - 1 else "next")]

    @staticmethod
    def hit(button, x, y):
        _, cx, cy, w, h, _ = button
        return abs(x - cx) <= w / 2 and abs(y - cy) <= h / 2

    def draw_button(self, b, index):
        title, x, y, w, h, action = b
        disabled = action == "back" and self.page == 0
        active = not disabled and (self.hit(b, *self.mouse) or index == self.focus)
        primary = action in ("start", "next")
        border = GOLD if primary else CYAN
        self.rect(x, y - 4, w + 4, h + 4, (0, 3, 15, 160))
        self.rect(x, y, w + 2, h + 2, (*border, 240 if active else 110))
        fill = (34, 70, 90) if active else (17, 35, 55)
        if primary:
            fill = (255, 221, 126) if active else (227, 176, 73)
        self.rect(x, y, w, h, fill if not disabled else (22, 32, 47))
        self.rect(x, y + h / 2 - 2, w - 8, 1, (*WHITE, 100))
        self.text(title, x, y - 8, 19 if self.page is None else 13,
                  (17, 28, 46) if primary else MUTED if disabled else WHITE,
                  center=True, bold=True)

    def draw(self):
        arcade.draw_texture_rect(self.background, arcade.XYWH(300, 320, 600, 640))
        if self.page is None:
            self.rect(300, 138, 600, 250, (5, 13, 29, 105))
            self.text("C O P Y   ·   C O N N E C T   ·   C L E A R", 300, 229, 10, CYAN, True)
            for i in range(12):
                x = 30 + (i * 113) % 540
                y = 260 + (i * 67 + self.time * (5 + i % 3)) % 310
                a = int(70 + 60 * math.sin(self.time * 1.3 + i))
                arcade.draw_circle_filled(x, y, 1.5, (255, 231, 166, a))
            self.text("CLICK TO SELECT  /  UP & DOWN TO CHOOSE  /  ENTER TO CONFIRM", 300, 35, 9, MUTED, True)
        else:
            self.rect(300, 320, 600, 640, (5, 12, 28, 243))
            self.text("DELETION 44  /  HOW TO PLAY", 38, 603, 11, CYAN, bold=True)
            self.text(f"{self.page + 1:02d} / {len(LESSONS):02d}", 560, 603, 11, GOLD, True)
            title, subtitle, lines, kind = LESSONS[self.page]
            self.text(title, 38, 550, 23, WHITE, bold=True)
            self.text(subtitle, 38, 515, 13, GOLD)
            self.rect(300, 397, 524, 192, (15, 31, 51))
            arcade.draw_lrbt_rectangle_outline(38, 562, 301, 493, (42, 73, 94), 1)
            self.diagram(kind)
            for i, line in enumerate(lines):
                self.text(line, 40, 264 - i * 32, 12, WHITE if i == 0 else MUTED)
            for i in range(len(LESSONS)):
                self.rect(48 + i * 63, 106, 20 if i == self.page else 6, 4,
                          GOLD if i == self.page else (52, 73, 94))
            self.text("LEFT / RIGHT TO BROWSE  ·  ESC FOR MENU", 300, 13, 9, MUTED, True)
        for i, b in enumerate(self.buttons()):
            self.draw_button(b, i)

    def row(self, colors, y, highlight=-1, small=False):
        spacing = 64 if not small else 50
        first = 300 - (len(colors) - 1) * spacing / 2
        for i, color in enumerate(colors):
            x = first + i * spacing
            self.rect(x, y, spacing - 3, spacing - 3, (9, 21, 38))
            arcade.draw_texture_rect(self.gems[color], arcade.XYWH(x, y, spacing - 9, spacing - 9))
            if i == highlight:
                arcade.draw_circle_outline(x, y, spacing / 2 - 2, GOLD, 2)

    def diagram(self, kind):
        if kind in ("source", "target"):
            self.row([0, 1, 1, 1, 1] if self.practice < 2 else [0] * 5,
                     405, 0 if self.practice == 1 else -1)
            msg = ("Click the first green stone to select your source." if self.practice == 0 else
                   "Selected! You can continue to the next step." if kind == "source" else
                   "Now click the yellow stone immediately beside it." if self.practice == 1 else
                   "Success! Five green stones form a clearing line.")
            self.text(msg, 300, 330, 12, CYAN, True)
            self.text("SOURCE", 172, 457, 11, GOLD, True)
            self.text("COPIED / 4 GREEN" if self.practice == 2 else "TARGET RUN / 4 YELLOW",
                      342, 457, 11, MUTED, True)
        elif kind in ("copy", "clear", "overview", "ready"):
            n = 4 if kind == "copy" else 5
            self.row([0] + [1] * (n - 1), 450, small=True)
            self.text("COPY THE SOURCE COLOR", 300, 395, 11, CYAN, True)
            self.row([0] * n, 351, small=True)
            if kind != "copy":
                self.text("+5", 445, 345, 17, GOLD, True, True)
        elif kind == "fall":
            for i, x in enumerate((175, 300, 425)):
                self.text(("CLEAR", "FALL", "REFILL")[i], x, 460, 11, CYAN, True)
                for j in range(2):
                    y = 410 - j * 60
                    self.rect(x, y, 48, 48, (7, 17, 31))
                if i == 0:
                    arcade.draw_texture_rect(self.gems[0], arcade.XYWH(x, 410, 43, 43))
                elif i == 1:
                    progress = min(1, (self.time % 3) / 1.5)
                    arcade.draw_texture_rect(self.gems[0], arcade.XYWH(x, 410 - 60 * progress, 43, 43))
                else:
                    arcade.draw_texture_rect(self.gems[0], arcade.XYWH(x, 350, 43, 43))
                    arcade.draw_texture_rect(self.gems[1], arcade.XYWH(x, 410, 43, 43))
                if i < 2:
                    self.text("→", x + 62, 388, 20, GOLD, True)
        elif kind == "score":
            for i, (label, value) in enumerate((("5 STONES", "5"), ("6 STONES", "36"), ("10 STONES", "1,000"))):
                x = 133 + i * 167
                self.text(label, x, 447, 15, CYAN, True)
                self.text(value, x, 397, 25, GOLD, True, True)
            self.text("LONGER CONNECTIONS. GREATER REWARDS.", 300, 335, 12, MUTED, True)
        elif kind == "invalid":
            self.row([0, 1, 1, 2, 4], 412, 0)
            self.text("Only 2 yellow stones: no copy. Choose a source again.", 300, 335, 12, GOLD, True)

    def activate(self, action):
        if action == "start":
            self.window.start_game()
        elif action == "tutorial":
            self.page, self.practice, self.focus = 0, 0, 2
        elif action == "menu":
            self.page, self.practice, self.focus = None, 0, 0
        elif action in ("next", "back"):
            self.page = max(0, min(len(LESSONS) - 1, self.page + (1 if action == "next" else -1)))
            self.practice = 0
            self.texts.clear()

    def click(self, x, y):
        for b in self.buttons():
            if self.hit(b, x, y):
                self.activate(b[-1])
                return
        if self.page in (1, 2) and 375 <= y <= 435:
            if 142 <= x <= 202:
                self.practice = 1
            elif self.page == 2 and self.practice == 1 and 206 <= x <= 266:
                self.practice = 2
            elif self.page == 2:
                self.practice = 0

    def key(self, symbol):
        if symbol == arcade.key.ESCAPE:
            self.activate("menu")
        elif symbol in (arcade.key.UP, arcade.key.DOWN, arcade.key.TAB):
            self.focus = (self.focus + (-1 if symbol == arcade.key.UP else 1)) % len(self.buttons())
        elif symbol in (arcade.key.ENTER, arcade.key.SPACE):
            self.activate(self.buttons()[self.focus][-1])
        elif self.page is not None and symbol in (arcade.key.LEFT, arcade.key.RIGHT):
            self.activate("back" if symbol == arcade.key.LEFT else "next")
