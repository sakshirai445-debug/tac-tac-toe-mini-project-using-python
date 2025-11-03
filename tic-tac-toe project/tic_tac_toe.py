import tkinter as tk
from tkinter import messagebox
import random

EMPTY = ""
PLAYER1 = "X"
PLAYER2 = "O"
FONT_BIG = ("Courier", 40, "bold")
FONT_MED = ("Helvetica", 14, "bold")
BG_COLOR = "#1e1e2f"
CARD_COLOR = "#33334d"
PRIMARY = "#00bfff"
SECONDARY = "#ff1493"
TEXT = "white"
TITLE = "Tic Tac Toe"

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.root.minsize(700, 900)
        self.center_window(700, 900)
        self.root.config(bg=BG_COLOR)
        self.root.resizable(False, False)

        self.score = {PLAYER1: 0, PLAYER2: 0, "Draws": 0}
        self.create_main_menu()

    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def create_main_menu(self):
        self.clear_window()
        main_frame = tk.Frame(self.root, bg=BG_COLOR, padx=20, pady=20)
        main_frame.pack(expand=True, fill="both")

        title_label = tk.Label(main_frame, text=TITLE, font=("Courier", 48, "bold"), bg=BG_COLOR, fg=TEXT)
        title_label.pack(pady=30)

        tk.Button(main_frame, text="Play vs Human", font=FONT_MED, width=20, bg=PRIMARY, fg=TEXT,
                  command=lambda: self.start_game(False)).pack(pady=10)
        tk.Button(main_frame, text="Play vs AI", font=FONT_MED, width=20, bg=SECONDARY, fg=TEXT,
                  command=self.choose_difficulty).pack(pady=10)
        tk.Button(main_frame, text="How to Play", font=FONT_MED, width=20, bg="gray", fg=TEXT,
                  command=self.show_how_to_play).pack(pady=10)

    def choose_difficulty(self):
        self.clear_window()
        frame = tk.Frame(self.root, bg=BG_COLOR, padx=20, pady=20)
        frame.pack(expand=True, fill="both")

        tk.Label(frame, text="Choose Difficulty", font=("Courier", 28, "bold"), bg=BG_COLOR, fg=TEXT).pack(pady=30)

        tk.Button(frame, text="Easy", font=FONT_MED, width=20, bg="lightgray", fg=TEXT,
                  command=lambda: self.start_game(True, "Easy")).pack(pady=10)
        tk.Button(frame, text="Medium", font=FONT_MED, width=20, bg="orange", fg=TEXT,
                  command=lambda: self.start_game(True, "Medium")).pack(pady=10)
        tk.Button(frame, text="Hard", font=FONT_MED, width=20, bg=SECONDARY, fg=TEXT,
                  command=lambda: self.start_game(True, "Hard")).pack(pady=10)
        tk.Button(frame, text="Back", font=FONT_MED, width=20, bg="gray", fg=TEXT,
                  command=self.create_main_menu).pack(pady=10)

    def show_how_to_play(self):
        instructions = (
            "Tic Tac Toe Rules:\n\n"
            "1. The game is played on a 3x3 grid.\n"
            "2. Player 1 is 'X' and Player 2 is 'O'.\n"
            "3. Players take turns placing their mark in an empty cell.\n"
            "4. The first player to get 3 in a row (vertically, horizontally, or diagonally) wins.\n"
            "5. If the grid is full and no player has won, it's a draw.\n"
            "\nEnjoy the game!"
        )
        messagebox.showinfo("How to Play", instructions)

    def start_game(self, vs_ai, difficulty=None):
        self.vs_ai = vs_ai
        self.difficulty = difficulty
        self.current_player = PLAYER1
        self.board = [[EMPTY]*3 for _ in range(3)]
        self.buttons = [[None]*3 for _ in range(3)]
        self.create_game_ui()

    def create_game_ui(self):
        self.clear_window()

        game_frame = tk.Frame(self.root, bg=BG_COLOR, padx=20, pady=20)
        game_frame.pack(expand=True, fill="both")

        title = tk.Label(game_frame, text=f"{TITLE} - {self.difficulty if self.vs_ai else 'Human vs Human'}",
                         font=("Courier", 28, "bold"), bg=BG_COLOR, fg=TEXT)
        title.pack(pady=10)

        self.score_frame = tk.Frame(game_frame, bg=BG_COLOR)
        self.score_frame.pack(pady=10)
        self.update_scoreboard()

        board_card = tk.Frame(game_frame, bg=CARD_COLOR, padx=10, pady=10)
        board_card.pack()

        canvas_size = 375
        cell_size = canvas_size // 3
        self.canvas = tk.Canvas(board_card, width=canvas_size, height=canvas_size, bg=CARD_COLOR, highlightthickness=0)
        self.canvas.grid(row=0, column=0)

        for i in range(1, 3):
            self.canvas.create_line(0, i * cell_size, canvas_size, i * cell_size, width=3, fill=PRIMARY)
            self.canvas.create_line(i * cell_size, 0, i * cell_size, canvas_size, width=3, fill=PRIMARY)

        board_frame = tk.Frame(board_card, bg=CARD_COLOR)
        board_frame.place(x=0, y=0)

        for r in range(3):
            for c in range(3):
                btn = tk.Button(board_frame, text="", font=FONT_BIG, width=3, height=1, bg=CARD_COLOR, fg=TEXT,
                                command=lambda row=r, col=c: self.on_cell_click(row, col))
                btn.grid(row=r, column=c, padx=10, pady=10)
                self.buttons[r][c] = btn

        control_frame = tk.Frame(game_frame, bg=BG_COLOR)
        control_frame.pack(pady=20)

        tk.Button(control_frame, text="Reset Game", font=FONT_MED, bg="orange", fg=TEXT,
                  command=self.reset_game).grid(row=0, column=0, padx=10)
        tk.Button(control_frame, text="Back to Menu", font=FONT_MED, bg="gray", fg=TEXT,
                  command=self.create_main_menu).grid(row=0, column=1, padx=10)

    def update_scoreboard(self):
        for widget in self.score_frame.winfo_children():
            widget.destroy()

        tk.Label(self.score_frame, text=f"Player X Wins: {self.score[PLAYER1]}", font=FONT_MED, bg=BG_COLOR, fg=PRIMARY).pack(side="left", padx=10)
        tk.Label(self.score_frame, text=f"Player O Wins: {self.score[PLAYER2]}", font=FONT_MED, bg=BG_COLOR, fg=SECONDARY).pack(side="left", padx=10)
        tk.Label(self.score_frame, text=f"Draws: {self.score['Draws']}", font=FONT_MED, bg=BG_COLOR, fg=TEXT).pack(side="left", padx=10)

    def on_cell_click(self, row, col):
        if self.board[row][col] != EMPTY or (self.vs_ai and self.current_player == PLAYER2):
            return

        self.make_move(row, col)

        if self.vs_ai and self.current_player == PLAYER2:
            self.root.after(300, self.ai_move)

    def ai_move(self):
        if self.difficulty == "Easy":
            row, col = self.get_random_move()
        elif self.difficulty == "Medium":
            row, col = self.get_medium_move()
        else:
            row, col = self.get_best_move()
        self.make_move(row, col)

    def make_move(self, row, col):
        self.board[row][col] = self.current_player
        self.buttons[row][col].config(text=self.current_player, fg=PRIMARY if self.current_player == PLAYER1 else SECONDARY)

        if self.check_winner(self.current_player):
            self.animate_winner(self.get_winning_cells(self.current_player))
            messagebox.showinfo("Game Over", f"Player {self.current_player} wins!")
            self.score[self.current_player] += 1
            self.update_scoreboard()
            self.reset_game()
        elif self.is_board_full():
            messagebox.showinfo("Game Over", "It's a draw!")
            self.score["Draws"] += 1
            self.update_scoreboard()
            self.reset_game()
        else:
            self.current_player = PLAYER2 if self.current_player == PLAYER1 else PLAYER1

    def get_random_move(self):
        available = [(r, c) for r in range(3) for c in range(3) if self.board[r][c] == EMPTY]
        return random.choice(available)

    def get_medium_move(self):
        # 1. Try to win
        for r in range(3):
            for c in range(3):
                if self.board[r][c] == EMPTY:
                    self.board[r][c] = PLAYER2
                    if self.check_winner(PLAYER2):
                        self.board[r][c] = EMPTY
                        return r, c
                    self.board[r][c] = EMPTY

        # 2. Block opponent win
        for r in range(3):
            for c in range(3):
                if self.board[r][c] == EMPTY:
                    self.board[r][c] = PLAYER1
                    if self.check_winner(PLAYER1):
                        self.board[r][c] = EMPTY
                        return r, c
                    self.board[r][c] = EMPTY

        # 3. Otherwise random
        return self.get_random_move()

    def get_best_move(self):
        best_score = -float('inf')
        best_move = None
        for r in range(3):
            for c in range(3):
                if self.board[r][c] == EMPTY:
                    self.board[r][c] = PLAYER2
                    score = self.minimax(False)
                    self.board[r][c] = EMPTY
                    if score > best_score:
                        best_score = score
                        best_move = (r, c)
        return best_move

    def minimax(self, is_maximizing):
        if self.check_winner(PLAYER2):
            return 1
        if self.check_winner(PLAYER1):
            return -1
        if self.is_board_full():
            return 0

        scores = []
        for r in range(3):
            for c in range(3):
                if self.board[r][c] == EMPTY:
                    self.board[r][c] = PLAYER2 if is_maximizing else PLAYER1
                    score = self.minimax(not is_maximizing)
                    self.board[r][c] = EMPTY
                    scores.append(score)
        return max(scores) if is_maximizing else min(scores)

    def check_winner(self, player):
        return any(
            all(self.board[r][c] == player for c in range(3)) or
            all(self.board[c][r] == player for c in range(3))
            for r in range(3)
        ) or \
        all(self.board[i][i] == player for i in range(3)) or \
        all(self.board[i][2-i] == player for i in range(3))

    def get_winning_cells(self, player):
        for r in range(3):
            if all(self.board[r][c] == player for c in range(3)):
                return [(r, c) for c in range(3)]
        for c in range(3):
            if all(self.board[r][c] == player for r in range(3)):
                return [(r, c) for r in range(3)]
        if all(self.board[i][i] == player for i in range(3)):
            return [(i, i) for i in range(3)]
        if all(self.board[i][2-i] == player for i in range(3)):
            return [(i, 2-i) for i in range(3)]

    def animate_winner(self, cells):
        for r, c in cells:
            self.buttons[r][c].config(bg=PRIMARY if self.current_player == PLAYER1 else SECONDARY)

    def is_board_full(self):
        return all(cell != EMPTY for row in self.board for cell in row)

    def reset_game(self):
        for r in range(3):
            for c in range(3):
                self.board[r][c] = EMPTY
                self.buttons[r][c].config(text="", bg=CARD_COLOR)
        self.current_player = PLAYER1

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()
