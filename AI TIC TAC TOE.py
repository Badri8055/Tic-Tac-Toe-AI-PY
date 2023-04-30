from tkinter import *
import math

class TicTacToe:
    def __init__(self, master):
        self.master = master
        self.master.title("Tic Tac Toe")

        # Initialize game board and other variables
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.game_over = False

        # Initialize GUI elements
        self.canvas = Canvas(self.master, width=600, height=600)
        self.canvas.pack(side=BOTTOM)
        self.canvas.bind("<Button-1>", self.handle_click)
        self.draw_board()
        self.status_label = Label(self.master, text="Player X's turn")
        self.status_label.pack()

    def draw_board(self):
        # Draw game board on canvas
        for i in range(1, 3):
            self.canvas.create_line(i * 100, 0, i * 100, 300)
            self.canvas.create_line(0, i * 100, 300, i * 100)
        for i in range(3):
            for j in range(3):
                x1 = j * 100 + 10
                y1 = i * 100 + 10
                x2 = j * 100 + 90
                y2 = i * 100 + 90
                if self.board[i][j] == 'X':
                    self.canvas.create_line(x1, y1, x2, y2, width=2)
                    self.canvas.create_line(x1, y2, x2, y1, width=2)
                elif self.board[i][j] == 'O':
                    self.canvas.create_oval(x1, y1, x2, y2, width=2)

    def handle_click(self, event):
        # Handle mouse clicks on the canvas
        if not self.game_over:
            row = math.floor(event.y / 100)
            col = math.floor(event.x / 100)
            if self.board[row][col] == ' ':
                self.board[row][col] = self.current_player
                self.draw_board()
                winner = self.check_winner()
                if winner:
                    self.game_over = True
                    self.status_label.config(text="Player " + winner + " wins!")
                elif self.check_tie():
                    self.game_over = True
                    self.status_label.config(text="It's a tie!")
                else:
                    self.switch_player()
                    self.make_computer_move()

    def switch_player(self):
        # Switch current player between X and O
        if self.current_player == 'X':
            self.current_player = 'O'
            self.status_label.config(text="Player O's turn")
        else:
            self.current_player = 'X'
            self.status_label.config(text="Player X's turn")

    def make_computer_move(self):
        # Use Minimax algorithm with alpha-beta pruning to make the computer's move
        alpha = -math.inf
        beta = math.inf
        best_score = -math.inf
        best_move = None
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == ' ':
                    self.board[i][j] = 'O'
                    score = self.minimax(False, alpha, beta)
                    self.board[i][j] = ' '
                    if score > best_score:
                        best_score = score
                        best_move = (i, j)
        if best_move:
            self.board[best_move[0]][best_move[1]] = 'O'
            self.draw_board()
            winner = self.check_winner()
            if winner:
                self.game_over = True
                self.status_label.config(text="Player " + winner + " wins!")
            elif self.check_tie():
                self.game_over = True
                self.status_label.config(text="It's a tie!")
            else:
                self.switch_player()

    def minimax(self, is_maximizing_player, alpha, beta):
        # Recursively search game tree using Minimax algorithm with alpha-beta pruning
        winner = self.check_winner()
        if winner:
            if winner == 'X':
                return -1
            else:
                return 1
        elif self.check_tie():
            return 0
        elif is_maximizing_player:
            best_score = -math.inf
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == ' ':
                        self.board[i][j] = 'O'
                        score = self.minimax(False, alpha, beta)
                        self.board[i][j] = ' '
                        best_score = max(score, best_score)
                        alpha = max(alpha, best_score)
                        if beta <= alpha:
                            break
            return best_score
        else:
            best_score = math.inf
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == ' ':
                        self.board[i][j] = 'X'
                        score = self.minimax(True, alpha, beta)
                        self.board[i][j] = ' '
                        best_score = min(score, best_score)
                        beta = min(beta, best_score)
                        if beta <= alpha:
                            break
            return best_score

    def check_winner(self):
        # Check if a player has won the game
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != ' ':
                return self.board[i][0]
            elif self.board[0][i] == self.board[1][i] == self.board[2][i] != ' ':
                return self.board[0][i]
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != ' ':
            return self.board[0][0]
        elif self.board[0][2] == self.board[1][1] == self.board[2][0] != ' ':
            return self.board[0][2]
        else:
            return None

    def check_tie(self):
        # Check if the game has ended in a tie
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == ' ':
                    return False
        return True

root = Tk()
game = TicTacToe(root)
root.mainloop()