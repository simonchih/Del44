"""Exercise a real Arcade window, textures, input, fade and particle rendering."""
import os
from pathlib import Path
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
os.chdir(tempfile.gettempdir())  # Assets must also load outside the repository.
import d44 as game
import arcade

window = game.awindow(game.table_width, game.table_height + game.top_block_h)
try:
    assert (window.width, window.height) == (600, 640)
    # The menu must not initialize a board or start the background workers.
    import copy
    original_board = copy.deepcopy(game.stone_matrix)
    window.on_draw()
    window.on_update(3)
    assert not window.playing and not window.workers_started
    assert game.stone_matrix == original_board
    arcade.get_image().save(str(Path(tempfile.gettempdir()) / 'del44-menu.png'))
    window.on_mouse_press(300, 102, arcade.MOUSE_BUTTON_LEFT, 0)
    assert window.front_end.page == 0
    for page in range(9):
        window.front_end.page = page
        window.front_end.practice = 0
        window.on_draw()
        for text in window.front_end.texts.values():
            left = text.x - text.content_width / 2 if text.anchor_x == 'center' else text.x
            assert left >= 0 and left + text.content_width <= 600, text.text
        if page in (1, 2):
            window.on_mouse_press(172, 405, arcade.MOUSE_BUTTON_LEFT, 0)
            assert window.front_end.practice == 1
            if page == 2:
                window.on_mouse_press(364, 405, arcade.MOUSE_BUTTON_LEFT, 0)
                assert window.front_end.practice == 0  # Not an adjacent target.
                window.on_mouse_press(172, 405, arcade.MOUSE_BUTTON_LEFT, 0)
                window.on_mouse_press(236, 405, arcade.MOUSE_BUTTON_LEFT, 0)
                assert window.front_end.practice == 2
            window.on_draw()
        arcade.get_image().save(str(Path(tempfile.gettempdir()) / f'del44-tutorial-{page + 1}.png'))
    assert game.stone_matrix == original_board and not window.workers_started
    window.on_key_press(arcade.key.ESCAPE, 0)
    assert window.front_end.page is None
    window.on_key_press(arcade.key.DOWN, 0)
    window.on_key_press(arcade.key.ENTER, 0)
    assert window.front_end.page == 0
    window.on_key_press(arcade.key.RIGHT, 0)
    assert window.front_end.page == 1
    window.on_key_press(arcade.key.LEFT, 0)
    assert window.front_end.page == 0
    window.on_key_press(arcade.key.ESCAPE, 0)
    # Exercise the actual Start Game button without workers racing deterministic checks.
    start_game = window.start_game
    window.start_game = lambda: start_game(start_workers=False)
    window.on_mouse_press(300, 174, arcade.MOUSE_BUTTON_LEFT, 0)
    assert window.playing
    window.start_game = start_game
    for x in range(20):
        for y in range(20):
            game.stone_matrix[x][y] = (x + y) % 5 + 1
    window.on_draw()
    assert game.do_clean == 0
    window.on_mouse_press(-1, 0, arcade.MOUSE_BUTTON_LEFT, 0)
    assert window.selected == 0
    window.on_mouse_press(15, 15, arcade.MOUSE_BUTTON_LEFT, 0)
    assert window.selected == (0, 0)
    window.on_update(1 / 60)
    window.on_draw()
    # Copy into an adjacent run of four: five greens must fade and score five.
    for x in range(1, 5):
        game.stone_matrix[x][0] = 2
    window.on_mouse_press(45, 15, arcade.MOUSE_BUTTON_LEFT, 0)
    assert [game.stone_matrix[x][0] for x in range(5)] == [1] * 5
    window.clean()
    assert all(game.stone_alpha[x][0] == game.alpha_begin_minus for x in range(5))
    assert game.calc_del_score and game.add_score(5) == 5
    window.on_update(0.05)
    assert window.particles
    window.on_draw()
    arcade.get_image().save(str(Path(tempfile.gettempdir()) / 'del44-preview.png'))
    window.on_update(1)
    assert not window.particles
    # Stress the full-board effect limit and alpha clamp.
    for column in game.stone_alpha:
        column[:] = [100] * 20
    window.on_update(0.01)
    assert len(window.particles) <= 600
    window.on_draw()
    game.draw_tex(15, 15, 30, 30, game.stone, alpha=65025)
    # Run the real event loop and existing fade/fall workers through one clear.
    game.calc_del_score.clear()
    game.score = 0
    for x in range(20):
        for y in range(20):
            game.stone_matrix[x][y] = (x + y) % 5 + 1
            game.stone_alpha[x][y] = 255
    for x in range(5):
        game.stone_matrix[x][0] = 1
    window.clean()
    game.start_new_thread(game.stone_alpha_zero, ())
    game.start_new_thread(game.down, ())
    result = []
    def finish(delta_time):
        result.append(game.score >= 5 and not game.calc_del_score
                      and all(v > 0 for col in game.stone_matrix for v in col)
                      and game.stone_center_cor == game.default_center_cor)
        window.close()
    import pyglet
    pyglet.clock.schedule_once(finish, 5)
    arcade.run()
    assert result == [True], "Clear, score and refill did not complete"
    print('PASS: menu, all tutorial pages, English text bounds, practice, keyboard, start, asset paths, rendering, input, copy, fade, score, refill, particles, alpha clamp')
finally:
    window.close()
