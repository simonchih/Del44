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
window.setup()
try:
    assert (window.width, window.height) == (600, 640)
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
    arcade.get_image().save('/tmp/del44-preview.png')
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
    print('PASS: asset paths, rendering, input, copy, fade, score, refill, particles, alpha clamp')
finally:
    window.close()
