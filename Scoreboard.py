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


def update_scoreboard(winner):
    if winner == "X":
        st.session_state.scores["X"]["wins"] += 1
        st.session_state.scores["O"]["losses"] += 1
    elif winner == "O":
        st.session_state.scores["O"]["wins"] += 1
        st.session_state.scores["X"]["losses"] += 1
    else:
        st.session_state.scores["X"]["draws"] += 1
        st.session_state.scores["O"]["draws"] += 1


def reset_scores():
    st.session_state.scores = {
        "X": {"name": st.session_state.name_x, "wins": 0, "losses": 0, "draws": 0},
        "O": {"name": st.session_state.name_o, "wins": 0, "losses": 0, "draws": 0}
    }


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

    if 'scores' not in st.session_state:
        st.session_state.scores = {
            "X": {"name": "Player X", "wins": 0, "losses": 0, "draws": 0},
            "O": {"name": "Player O", "wins": 0, "losses": 0, "draws": 0}
        }

    if 'name_x' not in st.session_state:
        st.session_state.name_x = st.session_state.scores["X"]["name"]
    if 'name_o' not in st.session_state:
        st.session_state.name_o = st.session_state.scores["O"]["name"]

    with st.sidebar:
        st.header("Player Settings")
        name_x_input = st.text_input('Player X Name', value=st.session_state.name_x, key="name_x_input")
        name_o_input = st.text_input('Player O Name', value=st.session_state.name_o, key="name_o_input")

        if st.button("Update Names"):
            st.session_state.name_x = name_x_input
            st.session_state.name_o = name_o_input
            st.session_state.scores["X"]["name"] = name_x_input
            st.session_state.scores["O"]["name"] = name_o_input

        st.header("Scoreboard")
        st.write(f"**{st.session_state.scores['X']['name']}**")
        st.write(f"Wins: {st.session_state.scores['X']['wins']}")
        st.write(f"Losses: {st.session_state.scores['X']['losses']}")
        st.write(f"Draws: {st.session_state.scores['X']['draws']}")
        st.write("---")
        st.write(f"**{st.session_state.scores['O']['name']}**")
        st.write(f"Wins: {st.session_state.scores['O']['wins']}")
        st.write(f"Losses: {st.session_state.scores['O']['losses']}")
        st.write(f"Draws: {st.session_state.scores['O']['draws']}")
        st.write("---")
        if st.button("Reset Scores"):
            reset_scores()

    if game_mode == "Standard":
        play_standard()
    else:
        play_modified()


def play_standard():
    if 'board' not in st.session_state:
        st.session_state.board = np.array([["" for _ in range(3)] for _ in range(3)])
    if 'current_player' not in st.session_state:
        st.session_state.current_player = "X"
    if 'game_over' not in st.session_state:
        st.session_state.game_over = False

    board = st.session_state.board
    current_player = st.session_state.current_player
    winner = check_winner(board)

    if winner is not None:
        if not st.session_state.game_over:
            st.success(f"🎉 Player {winner} wins!")
            update_scoreboard(winner)
            st.session_state.game_over = True
    elif check_draw(board):
        if not st.session_state.game_over:
            st.warning("It's a draw!")
            update_scoreboard(None)
            st.session_state.game_over = True
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

    if st.button("Reset game"):
        st.session_state.board = np.array([["" for _ in range(3)] for _ in range(3)])
        st.session_state.current_player = "X"
        st.session_state.game_over = False
        st.rerun()


def play_modified():
    if 'board' not in st.session_state:
        st.session_state.board = np.array([["" for _ in range(3)] for _ in range(3)])
    if 'current_player' not in st.session_state:
        st.session_state.current_player = "X"
    if 'game_over' not in st.session_state:
        st.session_state.game_over = False
    if 'moves' not in st.session_state:
        st.session_state.moves = {'X': [], 'O': []}

    board = st.session_state.board
    current_player = st.session_state.current_player
    winner = check_winner(board)

    if winner is not None:
        if not st.session_state.game_over:
            st.success(f"🎉 Player {winner} wins!")
            update_scoreboard(winner)
            st.session_state.game_over = True
    elif check_draw(board):
        if not st.session_state.game_over:
            st.warning("It's a draw!")
            update_scoreboard(None)
            st.session_state.game_over = True
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

    if st.button("Reset game"):
        st.session_state.board = np.array([["" for _ in range(3)] for _ in range(3)])
        st.session_state.current_player = "X"
        st.session_state.game_over = False
        st.session_state.moves = {'X': [], 'O': []}
        st.rerun()


if __name__ == "__main__":
    main()