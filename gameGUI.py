import tkinter as tk
from tkinter import messagebox
from game import TicTacToe
from player import HumanPlayer, RandomComputerPlayer

class TicTacToeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.root.configure(bg="#2c3e50")
        
        self.game = TicTacToe()
        self.x_player = HumanPlayer('X')
        self.o_player = RandomComputerPlayer('O')
        self.current_player = 'X'
        
        self.buttons = []
        self.create_board()
    
    def create_board(self):
        frame = tk.Frame(self.root, bg="#2c3e50")
        frame.pack(pady=20)
        
        for i in range(3):
            row = []
            for j in range(3):
                btn = tk.Button(frame, text="", font=('Arial', 24, 'bold'), height=2, width=5,
                                bg="#ecf0f1", fg="#2c3e50", relief="raised", bd=5,
                                command=lambda row=i, col=j: self.on_click(row, col))
                btn.grid(row=i, column=j, padx=5, pady=5)
                row.append(btn)
            self.buttons.append(row)
        
        self.status_label = tk.Label(self.root, text="Player X's Turn", font=('Arial', 14, 'bold'),
                                     bg="#2c3e50", fg="#ecf0f1")
        self.status_label.pack(pady=10)
    
    def on_click(self, row, col):
        square = row * 3 + col
        if self.game.board[square] == ' ':
            self.game.make_move(square, self.current_player)
            self.buttons[row][col].config(text=self.current_player, fg="#e74c3c" if self.current_player == 'X' else "#3498db")
            
            if self.game.current_winner:
                messagebox.showinfo("Game Over", f"{self.current_player} wins!")
                self.root.quit()
                return
            
            self.current_player = 'O' if self.current_player == 'X' else 'X'
            self.status_label.config(text=f"Player {self.current_player}'s Turn")
            
            if self.current_player == 'O':
                self.root.after(500, self.computer_move)
    
    def computer_move(self):
        square = self.o_player.get_move(self.game)
        row, col = divmod(square, 3)
        self.on_click(row, col)

if __name__ == "__main__":
    root = tk.Tk()
    gui = TicTacToeGUI(root)
    root.mainloop()
