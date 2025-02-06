import tkinter as tk
from tkinter import messagebox
from game import TicTacToe
from player import HumanPlayer, RandomComputerPlayer

class TicTacToeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.root.geometry("500x500")
        self.root.configure(bg="#2c3e50")
        self.root.iconphoto(False, tk.PhotoImage(file="avatar.png"))
        self.mode = None  # "human" cho Human vs Human, "computer" cho Human vs Computer
        
        # Tạo màn hình chính (Main Menu)
        self.main_menu_frame = tk.Frame(root, bg="#2c3e50")
        self.main_menu_frame.pack(expand=True)
        
        title_label = tk.Label(self.main_menu_frame, text="Tic Tac Toe", font=('Arial', 32, 'bold'), bg="#2c3e50", fg="#ecf0f1")
        title_label.pack(pady=20)
        
        mode_label = tk.Label(self.main_menu_frame, text="Select Game Mode", font=('Arial', 18), bg="#2c3e50", fg="#ecf0f1")
        mode_label.pack(pady=10)
        
        human_button = tk.Button(self.main_menu_frame, text="Human vs Human", font=('Arial', 16), bg="#3498db", fg="#ecf0f1", 
                                 command=self.start_human_game, width=20, bd=0, relief="raised")
        human_button.pack(pady=10)
        
        computer_button = tk.Button(self.main_menu_frame, text="Human vs Computer", font=('Arial', 16), bg="#e74c3c", fg="#ecf0f1", 
                                    command=self.start_computer_game, width=20, bd=0, relief="raised")
        computer_button.pack(pady=10)
        
    def start_human_game(self):
        self.mode = "human"
        self.main_menu_frame.pack_forget()
        self.start_game()
        
    def start_computer_game(self):
        self.mode = "computer"
        self.main_menu_frame.pack_forget()
        self.start_game()
        
    def start_game(self):
        # Khởi tạo trò chơi Tic Tac Toe
        self.game = TicTacToe()
        # Người chơi X luôn là Human
        self.x_player = HumanPlayer('X')
        # Với chế độ "computer", O là máy tính, ngược lại là Human
        if self.mode == "computer":
            self.o_player = RandomComputerPlayer('O')
        else:
            self.o_player = HumanPlayer('O')
        self.current_player = 'X'
        
        # Tạo giao diện bàn cờ
        self.game_frame = tk.Frame(self.root, bg="#2c3e50")
        self.game_frame.pack(pady=20)
        
        self.buttons = []
        for i in range(3):
            row_buttons = []
            for j in range(3):
                btn = tk.Button(self.game_frame, text="", font=('Arial', 24, 'bold'), height=2, width=5,
                                bg="#ecf0f1", fg="#2c3e50", relief="raised", bd=5,
                                command=lambda row=i, col=j: self.on_click(row, col))
                btn.grid(row=i, column=j, padx=5, pady=5)
                row_buttons.append(btn)
            self.buttons.append(row_buttons)
        
        self.status_label = tk.Label(self.root, text="Player X's Turn", font=('Arial', 18, 'bold'), bg="#2c3e50", fg="#ecf0f1")
        self.status_label.pack(pady=10)
        
    def on_click(self, row, col):
        square = row * 3 + col
        if self.game.board[square] == ' ':
            self.game.make_move(square, self.current_player)
            self.buttons[row][col].config(text=self.current_player, fg="#e74c3c" if self.current_player=='X' else "#3498db")
            
            # Kiểm tra chiến thắng hoặc hòa
            if self.game.current_winner:
                messagebox.showinfo("Game Over", f"Player {self.current_player} wins!")
                self.root.quit()
                return
            elif not self.game.empty_squares():
                messagebox.showinfo("Game Over", "It's a tie!")
                self.root.quit()
                return
                
            # Đổi lượt người chơi
            self.current_player = 'O' if self.current_player == 'X' else 'X'
            self.status_label.config(text=f"Player {self.current_player}'s Turn")
            
            # Nếu chế độ chơi máy và đến lượt máy, gọi hàm di chuyển của máy sau 500ms để tạo hiệu ứng\n            
            if self.mode == "computer" and self.current_player == 'O':
                self.root.after(500, self.computer_move)
    
    def computer_move(self):
        square = self.o_player.get_move(self.game)
        row, col = divmod(square, 3)
        self.on_click(row, col)
        
if __name__ == "__main__":
    root = tk.Tk()
    gui = TicTacToeGUI(root)
    root.mainloop()
