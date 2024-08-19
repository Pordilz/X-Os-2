import streamlit as st
import numpy as np

def check_winner(board):
    for row in board:
        if len(set(row)) == 1 and row[0] != "":
            return row[0]
    for col in board.T:
        if len(set(col)) == 1 and col[0] != "":
            return col[0]
    if len(set(board.diagonal())) == 1 and board[0, 0] != "":
        return board[0, 0]
    if len(set(np.fliplr(board).diagonal())) == 1 and board[0, 2] != "":
        return board[0, 2]
    return None

def check_draw(board):
    return not np.any(board == "")

def record_move(player, row, col):
    if 'moves' not in st.session_state:
        st.session_state.moves = {'X': [], 'O': []}
    if len(st.session_state.moves[player]) >= 3:
        oldest_move = st.session_state.moves[player].pop(0)
        st.session_state.board[oldest_move[0], oldest_move[1]] = ""
    st.session_state.moves[player].append((row, col))

def main():
    st.title("Tic-Tac-Toe")

    game_mode = st.radio("Choose game mode:", ["Standard", "Modified"])

    if game_mode == "Standard":
        play_standard()
    else:
        play_modified()

def play_standard():
    # Initialize or retrieve game state
    if 'board' not in st.session_state:
        st.session_state.board = np.array([["" for _ in range(3)] for _ in range(3)])
    if 'current_player' not in st.session_state:
        st.session_state.current_player = "X"

    board = st.session_state.board
    current_player = st.session_state.current_player
    winner = check_winner(board)

    if winner is not None:
        st.success(f"🎉 Player {winner} wins!")
    elif check_draw(board):
        st.warning("It's a draw!")
    else:
        st.write(f"Current turn: {current_player}")
        for row in range(3):
            cols = st.columns(3)
            for col in range(3):
                if board[row, col] == "":
                    if cols[col].button(" ", key=f"button_{row}_{col}"):
                        board[row, col] = current_player
                        st.session_state.board = board
                        st.session_state.current_player = "O" if current_player == "X" else "X"
                        st.rerun()
                else:
                    cols[col].write(board[row, col], key=f"button_{row}_{col}")

    # Add a reset button
    if st.button("Reset game"):
        st.session_state.board = np.array([["" for _ in range(3)] for _ in range(3)])
        st.session_state.current_player = "X"
        st.rerun()

def play_modified():
    # Initialize or retrieve game state
    if 'board' not in st.session_state:
        st.session_state.board = np.array([["" for _ in range(3)] for _ in range(3)])
    if 'current_player' not in st.session_state:
        st.session_state.current_player = "X"

    if 'moves' not in st.session_state:
        st.session_state.moves = {'X': [], 'O': []}

    board = st.session_state.board
    current_player = st.session_state.current_player
    winner = check_winner(board)

    if winner is not None:
        st.success(f"🎉 Player {winner} wins!")
    elif check_draw(board):
        st.warning("It's a draw!")
    else:
        st.write(f"Current turn: {current_player}")
        for row in range(3):
            cols = st.columns(3)
            for col in range(3):
                if board[row, col] == "":
                    if cols[col].button(" ", key=f"button_{row}_{col}"):
                        board[row, col] = current_player
                        record_move(current_player, row, col)
                        st.session_state.board = board
                        st.session_state.current_player = "O" if current_player == "X" else "X"
                        st.rerun()
                else:
                    cols[col].write(board[row, col], key=f"button_{row}_{col}")

    # Add a reset button
    if st.button("Reset game"):
        st.session_state.board = np.array([["" for _ in range(3)] for _ in range(3)])
        st.session_state.current_player = "X"
        st.session_state.moves = {'X': [], 'O': []}
        st.rerun()

if __name__ == "__main__":
    main()