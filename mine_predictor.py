import random
import hashlib
import json

GRID_SIZE = 5  # 5x5 board


def get_deterministic_rng(seed_str: str) -> random.Random:
    """Create a deterministic random generator using SHA-256 hash of the seed."""
    seed_hash = hashlib.sha256(seed_str.encode()).hexdigest()
    return random.Random(int(seed_hash, 16))


def predict_mines(server_seed: str, mine_count: int) -> list:
    """
    Predict mine positions using a deterministic RNG based on server seed.
    Returns a list of (row, col) tuples.
    """
    all_tiles = [(i, j) for i in range(GRID_SIZE) for j in range(GRID_SIZE)]
    rng = get_deterministic_rng(server_seed)
    return rng.sample(all_tiles, mine_count)


def render_board(mines: list, reveal_all: bool = True) -> str:
    """
    Render the 5x5 Mines board with emoji:
    💣 for mines, 🟩 for safe tiles.
    If reveal_all is False, hides all tiles as ❓.
    """
    board = ""
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if reveal_all:
                board += "💣" if (i, j) in mines else "🟩"
            else:
                board += "❓"
        board += "\n"
    return board


def get_board_structure(mines: list) -> list:
    """
    Returns a nested list structure representing the board with:
    'M' for mine, 'S' for safe.
    """
    board = []
    for i in range(GRID_SIZE):
        row = []
        for j in range(GRID_SIZE):
            row.append("M" if (i, j) in mines else "S")
        board.append(row)
    return board


def debug_board_output(seed: str, mine_count: int):
    """
    Debug function to show rendered board and JSON.
    """
    mines = predict_mines(seed, mine_count)
    print(f"🔐 Server Seed: {seed}")
    print(f"💣 Mine Count: {mine_count}\n")
    print("🎮 Rendered Board:")
    print(render_board(mines))

    print("📦 JSON Data:")
    print(json.dumps(get_board_structure(mines), indent=2))


# Debug run example
if __name__ == "__main__":
    test_seed = "b4470ea52ee0d0b7a329d333aaf41525f8b670ddde07a4a99c99037aa20cc7f0"
    test_mines = 5
    debug_board_output(test_seed, test_mines)
