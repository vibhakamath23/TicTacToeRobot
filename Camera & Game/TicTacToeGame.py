import time
from Husky.huskylib import HuskyLensLibrary
import copy
from MQTT.mqttconnect import connect_mqtt

# Setup connection to MQTT server to allow communication with XRP
c = connect_mqtt()

# Setup HuskyLens (change usb port as needed)
hl = HuskyLensLibrary("SERIAL", "/dev/tty.usbserial-130", 3000000)

## BOARD SETUP: Map tags to numeric position, change as needed depending on tag IDs and board orientation ##

GRID_TAGS = list(range(1, 10))  # IDs from 1 to 9
tag_id_to_pos = {
    7: (0, 0), 4: (0, 1), 1: (0, 2),
    8: (1, 0), 5: (1, 1), 2: (1, 2),
    9: (2, 0), 6: (2, 1), 3: (2, 2)
}

board = [[' ' for _ in range(3)] for _ in range(3)]

## GAME FUNCTIONS ##

def print_board(board):
    for row in board:
        print(" | ".join([f" {cell:^2} " for cell in row]))  # Centering the 'B' and 'R' in their spaces
        print("-" * 18)

def is_winner(bd, player):
    for i in range(3):
        if all([bd[i][j] == player for j in range(3)]): return True
        if all([bd[j][i] == player for j in range(3)]): return True
    if all([bd[i][i] == player for i in range(3)]): return True
    if all([bd[i][2-i] == player for i in range(3)]): return True
    return False

def is_full(bd):
    return all(cell != ' ' for row in bd for cell in row)

# Minimax Algorithm: determine optimal move for XRP
def minimax(bd, depth, is_maximizing):
    if is_winner(bd, 'B'): return 10 - depth
    if is_winner(bd, 'R'): return depth - 10
    if is_full(bd): return 0

    if is_maximizing:
        best_score = -float('inf')
        for i in range(3):
            for j in range(3):
                if bd[i][j] == ' ':
                    bd[i][j] = 'B'
                    score = minimax(bd, depth + 1, False)
                    bd[i][j] = ' '
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(3):
            for j in range(3):
                if bd[i][j] == ' ':
                    bd[i][j] = 'R'
                    score = minimax(bd, depth + 1, True)
                    bd[i][j] = ' '
                    best_score = min(score, best_score)
        return best_score

def find_best_move(bd):
    best_score = -float('inf')
    best_move = None
    for i in range(3):
        for j in range(3):
            if bd[i][j] == ' ':
                bd[i][j] = 'B'
                score = minimax(bd, 0, False)
                bd[i][j] = ' '
                if score > best_score:
                    best_score = score
                    best_move = (i, j)
    return best_move

def get_visible_tags():
    tags = hl.requestAll()
    return tags

def play_game():
    print("Waiting for all 9 AprilTags to be visible...")
    while True:
        tags = get_visible_tags()
        if len(set(tag.ID for tag in tags)) == 9:
            print("Grid ready. Waiting for opponent's first move...")
            break
        time.sleep(0.5)

    previous_visible = get_visible_tags()

    while True:
        # Step 1: Wait for opponent move (one tag covered)
        while True:
            current_visible = get_visible_tags()
            prev_ids = set(tag.ID for tag in previous_visible)
            curr_ids = set(tag.ID for tag in current_visible)
            diff = prev_ids - curr_ids
            if len(diff) == 1:
                tag_id = diff.pop()
                if tag_id not in tag_id_to_pos:
                    print(f"⚠️ Unknown tag ID {tag_id} — ignoring.")
                    continue
                i, j = tag_id_to_pos[tag_id]
                if board[i][j] == ' ':
                    board[i][j] = 'R'  # Red move
                    print(f"\nOpponent 🟥 moved at: ({i}, {j}).")
                    print_board(board)
                    previous_visible = current_visible
                    break
            time.sleep(1)

        if is_winner(board, 'R'):
            print("Opponent 🟥 (R) wins!")
            break
        if is_full(board):
            print("Draw!")
            break

        # Step 2: Find and show camera move
        move = find_best_move(board)
        if move is None:
            print("No valid moves left.")
            break
        i, j = move
        move_to_movement(i,j)
        expected_tag = [k for k, v in tag_id_to_pos.items() if v == move][0]
        print(f"\nHuskyLens move: ({i}, {j}) — please cover tag {expected_tag} with a blue marker. 🟦")

        # Step 3: Wait for correct camera move
        while True:
            current_visible = get_visible_tags()
            prev_ids = set(tag.ID for tag in previous_visible)
            curr_ids = set(tag.ID for tag in current_visible)
            diff = prev_ids - curr_ids
            if len(diff) == 1:
                tag_id = diff.pop()
                if tag_id not in tag_id_to_pos:
                    print(f"⚠️ Unknown tag ID {tag_id} — ignoring.")
                    continue
                i, j = tag_id_to_pos[tag_id]
                if board[i][j] == ' ':
                    if tag_id == expected_tag:
                        board[i][j] = 'B'  # Blue move
                        print(f"\nHuskyLens moved at: ({i}, {j}) 🟦")
                        print_board(board)
                        previous_visible = current_visible
                        break
                    else:
                        print("Wrong space covered! Please place blue square correctly.")
            time.sleep(0.5)

        if is_winner(board, 'B'):
            print("HuskyLens 🟦 (B) wins!")
            break
        if is_full(board):
            print("Draw!")
            break

        print("Waiting for opponent...")

## MOVE_TO_MOVEMENT: Translate optimal move to XRP movement by sending desired position to MQTT server
def move_to_movement(i, j):
    if i == 0 and j == 0:
        position = 1
    if i == 0 and j == 1:
        position = 2
    if i == 0 and j == 2: 
        position = 3
    if i == 1 and j == 0:
        position = 4
    if i == 1 and j == 1:
        position = 5
    if i == 1 and j == 2:
        position = 6
    if i == 2 and j == 0:
        position = 7
    if i == 2 and j == 1:
        position = 8
    if i == 2 and j == 2:
        position = 9
    position = str(position).encode()  # message to bytes to match the key format
    c.publish("topic/TicTacToePosition", position, retain=True)

## RUN THE GAME
if __name__ == "__main__":
    try:
        play_game()
    except KeyboardInterrupt:
        print("\nGame interrupted.")
