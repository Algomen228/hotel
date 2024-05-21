import tkinter as tk
from tkinter import messagebox
import random

class TicTacToe(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Крестики-нолики")
        self.geometry("300x300")
        self.current_player = "X"
        self.game_mode = None
        self.create_widgets()

    def create_widgets(self):
        self.mode_label = tk.Label(self, text="Выберите режим игры:", font=("Arial", 10))
        self.mode_label.pack()

        self.singleplayer_button = tk.Button(self, text="Против компьютера", command=self.start_singleplayer_game)
        self.singleplayer_button.pack(pady=5)

        self.multiplayer_button = tk.Button(self, text="Против друга", command=self.start_multiplayer_game)
        self.multiplayer_button.pack(pady=5)

    def start_singleplayer_game(self):
        self.game_mode = "singleplayer"
        self.create_board()

    def start_multiplayer_game(self):
        self.game_mode = "multiplayer"
        self.create_board()

    def create_board(self):
        for widget in self.winfo_children():
            widget.destroy()

        self.message_label = tk.Label(self, text=f"Ход игрока {self.current_player}", font=("Arial", 12))
        self.message_label.pack()

        self.board_frame = tk.Frame(self)
        self.board_frame.pack()

        cell_size = min(self.winfo_width(), self.winfo_height()) // 3  # Размер клетки
        button_font = ("Arial", max(cell_size // 3, 10))  # Размер шрифта кнопки

        self.buttons = [[None]*3 for _ in range(3)]
        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.Button(self.board_frame, text="", font=button_font, width=2, height=1,
                                               command=lambda row=i, col=j: self.on_click(row, col))
                self.buttons[i][j].grid(row=i, column=j, padx=1, pady=1)

    def on_click(self, row, col):
        if self.buttons[row][col]["text"] == "":
            self.buttons[row][col].config(text=self.current_player, bg="#ff0066" if self.current_player == "X" else "#33ccff")
            if self.check_winner():
                messagebox.showinfo("Победа!", f"Игрок {self.current_player} победил!")
                self.reset_board()
            elif self.is_board_full():
                messagebox.showinfo("Ничья!", "Ничья!")
                self.reset_board()
            else:
                self.current_player = "O" if self.current_player == "X" else "X"
                self.message_label.config(text=f"Ход игрока {self.current_player}")
                if self.game_mode == "singleplayer" and self.current_player == "O":
                    self.after(500, self.computer_move)

    def computer_move(self):
        while True:
            row = random.randint(0, 2)
            col = random.randint(0, 2)
            if self.buttons[row][col]["text"] == "":
                self.buttons[row][col].config(text="O", bg="#33ccff")
                self.current_player = "X"
                if self.check_winner():
                    messagebox.showinfo("Победа!", "Компьютер победил!")
                    self.reset_board()
                elif self.is_board_full():
                    messagebox.showinfo("Ничья!", "Ничья!")
                    self.reset_board()
                break

    def check_winner(self):
        board = [[self.buttons[i][j]["text"] for j in range(3)] for i in range(3)]
        # Проверка строк
        for row in board:
            if all(cell == self.current_player for cell in row):
                return True

        # Проверка столбцов
        for col in range(3):
            if all(board[row][col] == self.current_player for row in range(3)):
                return True

        # Проверка диагоналей
        if all(board[i][i] == self.current_player for i in range(3)) or \
                all(board[i][2 - i] == self.current_player for i in range(3)):
            return True

        return False

    def is_board_full(self):
        return all(self.buttons[i][j]["text"] != "" for i in range(3) for j in range(3))

    def reset_board(self):
        self.current_player = "X"
        self.message_label.config(text=f"Ход игрока {self.current_player}")
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text="", bg="SystemButtonFace")
        self.create_widgets()

if __name__ == "__main__":
    app = TicTacToe()
    app.mainloop()
