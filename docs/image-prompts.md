# Candy gemstone assets

## Main menu background

Asset: `images/menu-background.png`. Generated using the built-in imagegen
tool, with `C:/simon/icon.webp` as the visual reference. The generated image
was copied unchanged into the project. Buttons and tutorial diagrams are
rendered in Arcade, keeping labels sharp and examples faithful to the rules.

Final prompt:

> Use case: stylized-concept. Asset type: premium puzzle game main menu background, portrait 600:640 aspect ratio. Input image: reference image for Deletion 44 brand and colorful glossy jewel aesthetic. Create an exceptionally polished 3D illustrated title screen. Deep midnight navy and teal atmosphere, luminous floating candy gemstones in emerald, ruby, sapphire, gold and magenta, fine magical particles and cinematic rim lighting. Top half features large beautifully legible playful beveled logo with exact text "Deletion" and "44" beneath, matching the reference's blue-white letters and golden 44, surrounded by a sophisticated arc of jewel stones. Clear central focal point, rich dimensional materials, polished commercial game key art. Bottom 40 percent must remain calm dark navy negative space to overlay two menu buttons in code. No baked-in buttons, no other text, no watermark. Full bleed image.

## Stone sprites

Generated with the built-in imagegen tool, one call per asset, using the user-provided `del44_icon.png` as a style reference. The generated PNGs were copied into `images/` with their original alpha channel, without recoloring or background replacement.

Prompt template (replace `{color}` using the table below):

> Use case: stylized-concept. Generate one production game sprite for Deletion 44: a single {color} glossy rounded square candy gem, front facing, occupying 85% of square canvas. Style reference is the uploaded Deletion 44 icon: saturated candy colors, chunky dark outline, beveled 3D jelly volume, bright white upper left highlight, luminous colored rim and tiny integrated sparkle. Transparent background with actual alpha, no text, no other objects, no drop shadow beyond the sprite. Clear readable silhouette at 30 pixels. Save as PNG.

| Project asset | Color |
| --- | --- |
| `images/stone_green_20x20.png` | lime green |
| `images/stone_yellow_20x20.png` | golden yellow |
| `images/stone_red_20x20.png` | cherry red |
| `images/stone_blue_20x20.png` | electric cyan blue |
| `images/stone_20x20.png` | magenta pink |
