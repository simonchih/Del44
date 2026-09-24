The name of game is "Deletion 44" as it can delete 44 same color neighbor stones at most by copy action. 

==Rules==
1. Select a source stone by mouse button clicked.
2. Then, select a target stone that neighbors a source stone (up, down, left, right) by mouse button clicked. 
3. If target stones have more than 3 stones as same color in a row (for right or left neighbor) or in a column (for up or down neighbor), copy the color of source stone to target stones. Otherwise, go to step 1.
4. Delete stones if there are 5 stones or greater have same color in a row or in a column.

==Chinese Readme==

這個遊戲我取名叫Deletion 44，因為使用複製動作(手動)來消除時，一次最多消去44個相鄰的同色石頭。
當不是手動消除時，有一些情況可能超過44個，例如遊戲一開始、或者石頭自動下降許多同色石頭時，
有可能消除超過44個，但是此種情況非常少見。

玩法如下：
1. 用滑鼠選擇一個石頭，當作來源石
2. 接下來，用滑鼠選擇一個來源石旁邊(上、下、左、右)的石頭，當作目標石
3. 如果目標石的行(上下相鄰時)或列(左右相鄰時)，存在同顏色的連續三個以上，就把來源石複製到目標石，否則回到step 1.
4. 當行或列，存在5個或以上，同顏色的石頭，就會消除石頭

算分方式：
1. 剛好消除5個石頭，得5分。這邊的消除個數必需同色相鄰的石頭，如果開局時，一堆5個，另一堆也5個，則是5 + 5 = 10分，以下算分也是同色相鄰的石頭
2. 消除6到9個石頭，得到消除個數的平方分數，例如6個，是6 * 6=36分
3. 消除10到13個石頭，得到消除個數的三次方分數，例如10個，是10 * 10 * 10 = 1000分
4. 消除14到43個石頭，得到消除個數的四次方分數，例如15個，是15 * 15 * 15 * 15 = 50625分
5. 消除44個石頭或以上，得到五次方分數，例如44個，分數是44 * 44 * 44 * 44 * 44 = 164916224分

全部消除?
如果同色的石頭太少，造成難以消除，會啟動全部消除，但此時只消除，不記分。

==Run (Python 3.10+)==

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python d44.py
```

Run the real-window smoke test on a desktop with a display:

```sh
python tests/smoke.py
```

==Build a Windows executable==

Use the project virtual environment (Python 3.10+, verified with 3.13).
Do not invoke a global `PyInstaller` executable, which may belong to an
older Python with incompatible Arcade/pyglet packages.

```powershell
# Only if .venv does not exist yet:
py -3.13 -m venv .venv

# Installs the pinned build dependencies and builds dist/d44.exe:
.\build.cmd
```

`build.cmd` works from PowerShell and Command Prompt without changing
PowerShell's execution policy. `build.ps1` remains available for systems
where PowerShell scripts are enabled.

The spec includes images, sounds, and Arcade's package resources. The new
build uses `build/verified` so it does not reuse older global build files.
The executable includes Python; players do not need a Python installation.
Run `.\tests\smoke_exe.ps1` to verify the packaged executable starts from
outside the project directory, responds, and closes cleanly.

==Main menu and tutorial==

The game uses Arcade 3.x. Launch `python d44.py` to open the new title screen.
Click **Start Game** (upper button) to play, or **Tutorial** (lower button)
for nine self-paced lessons in English. The game board and its background
workers start only when you choose Start Game.

The tutorial covers source selection, adjacent targets, copying runs of at
least three, clearing lines of at least five, falling/refilling, scoring,
invalid moves, and automatic unscored full clears. Lessons 2 and 3 include
clickable practice using the real stone artwork. Practice does not change
the game board or score. Use **Back** / **Next** or Left / Right to browse,
and **Menu** or Esc to return to the title screen. The final lesson also
offers **Start Game**. On the menu, Up / Down selects a button and Enter
activates it; Tab and Space are also supported.

The reference-inspired title artwork is `images/menu-background.png`;
the menu and tutorial implementation is `menu.py`. All player-facing text
is in English. The existing packaging spec includes the new background.

The five sprites in `images/` were regenerated in a glossy candy-gem style.
Their historical `_20x20` names are retained for compatibility; the PNGs now
contain high-resolution RGBA artwork and are rendered in fixed 30-pixel cells.
Selection has a pulsing gold ring; clearing produces fading colored sparkles.
Generation prompts are recorded in `docs/image-prompts.md`.
