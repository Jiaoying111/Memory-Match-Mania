"""
Memory Match Game
Author: Jiaoying Sui
SID: 540408140
"""

import random
import time
import sys
import os

# CONFIG
SIZE = 4  # SIZE x SIZE board
SYMBOLS = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
FLIP_DELAY = 0.6      # seconds to show selected cards before judgement
USE_COLOR = True      # set False if ANSI not supported
CLEAR_CMD = "cls" if os.name == "nt" else "clear"

# ANSI COLORS
def color(text: str, code: str) -> str:
    return f"\033[{code}m{text}\033[0m" if USE_COLOR else text

C_HEADER   = "36;1"   # bright cyan
C_GRID     = "90"     # grey
C_HIDDEN   = "90"     # grey hidden card
C_REVEAL   = "35;1"   # bright magenta revealed
C_SELECT   = "33;1"   # yellow highlight
C_SUCCESS  = "32;1"   # green
C_FAIL     = "31;1"   # red

# GAME FUNCTIONS
def generate_board(size: int):
    needed = (size * size) // 2
    if needed > len(SYMBOLS):
        print("Board too large for symbol pool.", file=sys.stderr)
        sys.exit(1)
    pool = SYMBOLS[:needed] * 2
    random.shuffle(pool)
    return [pool[i*size:(i+1)*size] for i in range(size)]

def display_board(board, revealed, temp_select=None):
    """Render the board; temp_select is a set of (r,c) being flipped now."""
    os.system(CLEAR_CMD)
    size = len(board)
    # Header row
    header = "    " + " ".join(color(f"{c:^3}", C_HEADER) for c in range(size))
    print(header)
    # Top border
    print("  " + color("┌" + "┬".join("───" for _ in range(size)) + "┐", C_GRID))
    # Rows
    for r in range(size):
        row_cells = []
        for c in range(size):
            if revealed[r][c]:
                symbol = color(f"{board[r][c]:^3}", C_REVEAL)
            elif temp_select and (r, c) in temp_select:
                symbol = color(f"{board[r][c]:^3}", C_SELECT)
            else:
                symbol = color(" ■ ", C_HIDDEN)
            row_cells.append(symbol)
        print(color(f"{r} ", C_HEADER) + color("│", C_GRID) +
              color("│", C_GRID).join(row_cells) + color("│", C_GRID))
        if r != size - 1:
            print("  " + color("├" + "┼".join("───" for _ in range(size)) + "┤", C_GRID))
    # Bottom border
    print("  " + color("└" + "┴".join("───" for _ in range(size)) + "┘", C_GRID))
    print()

def get_coords(prompt, size, revealed):
    """Ask user for row,col; validate input."""
    while True:
        raw = input(prompt).strip()
        if raw.lower() in {"q", "quit"}:
            print("Goodbye!")
            sys.exit(0)
        try:
            r, c = map(int, raw.split(","))
            assert 0 <= r < size and 0 <= c < size
            if revealed[r][c]:
                print("Card already matched, pick another.")
                continue
            return r, c
        except (ValueError, AssertionError):
            print("Enter as row,col within range, e.g. 1,2")

def all_matched(revealed):
    return all(all(row) for row in revealed)

# MAIN LOOP
def main():
    board = generate_board(SIZE)
    revealed = [[False]*SIZE for _ in range(SIZE)]
    moves = 0
    start = time.time()

    while not all_matched(revealed):
        display_board(board, revealed)
        r1, c1 = get_coords("Pick first card  (row,col) or q to quit: ", SIZE, revealed)
        r2, c2 = get_coords("Pick second card (row,col): ", SIZE, revealed)

        # Show selected cards briefly
        display_board(board, revealed, temp_select={(r1, c1), (r2, c2)})
        time.sleep(FLIP_DELAY)

        moves += 1
        if board[r1][c1] == board[r2][c2]:
            revealed[r1][c1] = revealed[r2][c2] = True
            print(color("🎉 Match!", C_SUCCESS))
            time.sleep(0.6)
        else:
            print(color("❌ Not a match...", C_FAIL))
            time.sleep(0.8)

    elapsed = round(time.time() - start, 2)
    print(color(f"🏆 You matched all pairs in {moves} moves, {elapsed}s!", C_SUCCESS))

if __name__ == "__main__":
    main()
