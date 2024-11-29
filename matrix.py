import random
import os

# Constants
GRID_SIZE = 7
SHIP_SIZES = [3, 2, 2, 1, 1, 1, 1]  # Ship sizes
HIT = 'X'
MISS = 'O'
SUNK = 'S'
EMPTY = '.'

# Helper functions
def clear_screen():
    """Clear the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def create_empty_board():
    """Create an empty 7x7 grid."""
    return [[EMPTY for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

def print_board(board):
    """Print the game board to the screen."""
    print("  A B C D E F G")
    for i in range(GRID_SIZE):
        print(f"{i + 1} {' '.join(board[i])}")

def convert_coords(coords):
    """Convert a coordinate like 'B5' to row, col indices."""
    col = ord(coords[0].upper()) - ord('A')
    row = int(coords[1]) - 1
    return row, col

def valid_coords(row, col):
    """Check if coordinates are within the grid bounds."""
    return 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE

def place_ship(board, size):
    """Place a ship of a given size randomly on the board."""
    placed = False
    while not placed:
        orientation = random.choice(['H', 'V'])
        if orientation == 'H':
            row = random.randint(0, GRID_SIZE - 1)
            col = random.randint(0, GRID_SIZE - size)
            if all(board[row][col + i] == EMPTY for i in range(size)):
                for i in range(size):
                    board[row][col + i] = HIT
                placed = True
        else:  # Vertical
            row = random.randint(0, GRID_SIZE - size)
            col = random.randint(0, GRID_SIZE - 1)
            if all(board[row + i][col] == EMPTY for i in range(size)):
                for i in range(size):
                    board[row + i][col] = HIT
                placed = True

def take_shot(board, row, col):
    """Take a shot at the given coordinates, return hit/miss."""
    if board[row][col] == HIT:
        board[row][col] = SUNK
        return "hit"
    elif board[row][col] == EMPTY:
        board[row][col] = MISS
        return "miss"
    return None

def all_ships_sunk(board):
    """Check if all ships are sunk."""
    return all(cell != HIT for row in board for cell in row)

def start_new_game():
    """Start a new game or quit."""
    response = input("Do you want to play again? (y/n): ").strip().lower()
    if response == 'y':
        return True
    return False

def battleship_game():
    """Main game function."""
    print("Welcome to Battleship!")
    player_name = input("Enter your name: ")

    # Generate empty board and place ships
    board = create_empty_board()

    for size in SHIP_SIZES:
        place_ship(board, size)

    # Main game loop
    total_shots = 0
    while not all_ships_sunk(board):
        clear_screen()
        print_board(board)

        shot = input(f"{player_name}, enter your shot (e.g., B5): ").strip().upper()
        if len(shot) != 2 or not shot[0].isalpha() or not shot[1].isdigit():
            print("Invalid input, try again.")
            continue

        try:
            row, col = convert_coords(shot)
        except ValueError:
            print("Invalid coordinates. Please try again.")
            continue

        if not valid_coords(row, col):
            print("Shot out of bounds. Try again.")
            continue

        if board[row][col] in [MISS, HIT, SUNK]:
            print("You've already shot here. Try again.")
            continue

        total_shots += 1
        result = take_shot(board, row, col)

        if result == "hit":
            print("Hit!")
        elif result == "miss":
            print("Miss!")

        if all_ships_sunk(board):
            print(f"Congratulations, {player_name}! You've sunk all ships.")
            print(f"Total shots: {total_shots}")
            break

    # Ask if player wants to play again
    if start_new_game():
        battleship_game()
    else:
        print("Thanks for playing! Goodbye!")

# Run the game
battleship_game()
