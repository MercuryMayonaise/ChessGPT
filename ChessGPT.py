import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
from openai import OpenAI
import chess
import os
import anthropic

SQUARE_SIZE = 40  # Constant for square size
LIGHT_COLOR = "#F0D9B5"  # Light square color
DARK_COLOR = "#B58863"   # Dark square color
HIGHLIGHT_COLOR = "#FFFF00"  # Highlight color (yellow)

def play_chess_gpt(board, api_key):
    client = OpenAI(api_key=api_key)
    legal_moves = [move.uci() for move in board.legal_moves]
    completion = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a grandmaster chess player. You only respond with a single move in UCI chess notation (e.g., e2e4)."},
            {"role": "user", "content": f"You are playing black. The board position in FEN is: {board.fen()}. "
                                        f"The legal moves are: {', '.join(legal_moves)}. Make your move."}
        ]
    )
    return completion.choices[0].message.content

def play_chess_claude(board, api_key):
    client = anthropic.Anthropic(api_key=api_key)
    legal_moves = [move.uci() for move in board.legal_moves]
    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=100,
        temperature=0,
        system="You are a grandmaster chess player. Respond only with a single move in UCI chess notation (e.g., e2e4).",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"You are playing black. The board position in FEN is: {board.fen()}. "
                                f"The legal moves are: {', '.join(legal_moves)}. Make your move."
                    }
                ]
            }
        ]
    )
    return message.content[0].text.strip()

class ChessGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Chess Game vs AI")
        self.master.geometry("600x700")  # Set window size
        self.master.configure(bg='#f0f0f0')  # Light gray background
        self.style = ttk.Style()
        self.style.theme_use('clam')  # Use 'clam' theme for a modern look
        
        self.board = chess.Board()
        self.buttons = [[None for _ in range(8)] for _ in range(8)]
        self.selected_square = None
        self.piece_images = {}
        self.empty_images = {}
        self.ai_opponent = None
        self.api_key = None
        self.load_images()
        self.create_opponent_selection()

    def load_images(self):
        piece_files = {
            'p': 'black_pawn.png', 'r': 'black_rook.png', 'n': 'black_knight.png',
            'b': 'black_bishop.png', 'q': 'black_queen.png', 'k': 'black_king.png',
            'P': 'white_pawn.png', 'R': 'white_rook.png', 'N': 'white_knight.png',
            'B': 'white_bishop.png', 'Q': 'white_queen.png', 'K': 'white_king.png'
        }
        for piece, file_name in piece_files.items():
            img = Image.open(os.path.join("pieces", file_name)).convert("RGBA")
            img = img.resize((SQUARE_SIZE, SQUARE_SIZE), Image.LANCZOS)
            self.piece_images[piece] = {
                'light': ImageTk.PhotoImage(self.overlay_image(img, LIGHT_COLOR)),
                'dark': ImageTk.PhotoImage(self.overlay_image(img, DARK_COLOR)),
                'highlight': ImageTk.PhotoImage(self.overlay_image(img, HIGHLIGHT_COLOR))
            }
        
        for color, color_value in [('light', LIGHT_COLOR), ('dark', DARK_COLOR), ('highlight', HIGHLIGHT_COLOR)]:
            empty_img = Image.new('RGBA', (SQUARE_SIZE, SQUARE_SIZE), color_value)
            self.empty_images[color] = ImageTk.PhotoImage(empty_img)

    def overlay_image(self, img, color):
        background = Image.new("RGBA", img.size, color)
        return Image.alpha_composite(background, img)

    def create_opponent_selection(self):
        self.opponent_frame = ttk.Frame(self.master, padding="20")
        self.opponent_frame.pack(expand=True)

        ttk.Label(self.opponent_frame, text="Choose your opponent:", font=('Helvetica', 16)).pack(pady=10)

        self.opponent_var = tk.StringVar()
        ttk.Radiobutton(self.opponent_frame, text="ChatGPT", variable=self.opponent_var, value="gpt", style='TRadiobutton').pack(pady=5)
        ttk.Radiobutton(self.opponent_frame, text="Claude 3.5 Sonnet", variable=self.opponent_var, value="claude", style='TRadiobutton').pack(pady=5)

        ttk.Button(self.opponent_frame, text="Next", command=self.show_api_key_input, style='TButton').pack(pady=20)

        # Configure styles
        self.style.configure('TRadiobutton', font=('Helvetica', 12))
        self.style.configure('TButton', font=('Helvetica', 12), padding=10)

    def show_api_key_input(self):
        self.ai_opponent = self.opponent_var.get()
        if not self.ai_opponent:
            messagebox.showerror("Error", "Please select an opponent.")
            return

        self.opponent_frame.destroy()

        self.api_frame = ttk.Frame(self.master, padding="20")
        self.api_frame.pack(expand=True)

        api_label = "OpenAI" if self.ai_opponent == "gpt" else "Anthropic"
        ttk.Label(self.api_frame, text=f"Enter your {api_label} API Key:", font=('Helvetica', 16)).pack(pady=10)

        self.api_key_entry = ttk.Entry(self.api_frame, width=50, show="*")
        self.api_key_entry.pack(pady=10)

        ttk.Button(self.api_frame, text="Start Game", command=self.start_game, style='TButton').pack(pady=20)

    def start_game(self):
        self.api_key = self.api_key_entry.get()
        if not self.api_key:
            messagebox.showerror("Error", "Please enter an API key.")
            return

        self.api_frame.destroy()
        self.create_board()

    def create_board(self):
        self.board_frame = ttk.Frame(self.master, padding="20")
        self.board_frame.pack(expand=True)

        for row in range(8):
            for col in range(8):
                color = 'light' if (row + col) % 2 == 0 else 'dark'
                button = tk.Button(self.board_frame, image=self.empty_images[color], width=SQUARE_SIZE, height=SQUARE_SIZE, 
                                   command=lambda r=row, c=col: self.on_square_click(r, c), bd=0, highlightthickness=0)
                button.grid(row=row, column=col)
                self.buttons[row][col] = button
        self.update_board()

        # Add a status label
        self.status_label = ttk.Label(self.master, text="Your turn", font=('Helvetica', 14))
        self.status_label.pack(pady=10)

    def update_board(self):
        for row in range(8):
            for col in range(8):
                square = chess.square(col, 7-row)
                piece = self.board.piece_at(square)
                color = 'light' if (row + col) % 2 == 0 else 'dark'
                if piece:
                    self.buttons[row][col].config(image=self.piece_images[piece.symbol()][color])
                else:
                    self.buttons[row][col].config(image=self.empty_images[color])

    def on_square_click(self, row, col):
        square = chess.square(col, 7-row)
        if self.selected_square is None:
            if self.board.piece_at(square) and self.board.piece_at(square).color == chess.WHITE:
                self.selected_square = square
                self.highlight_square(row, col)
        else:
            move = chess.Move(self.selected_square, square)
            if move in self.board.legal_moves:
                self.make_move(move)
            self.clear_highlights()
            self.selected_square = None
            self.update_board()

    def highlight_square(self, row, col):
        piece = self.board.piece_at(chess.square(col, 7-row))
        if piece:
            self.buttons[row][col].config(image=self.piece_images[piece.symbol()]['highlight'])
        else:
            self.buttons[row][col].config(image=self.empty_images['highlight'])

    def clear_highlights(self):
        for row in range(8):
            for col in range(8):
                color = 'light' if (row + col) % 2 == 0 else 'dark'
                piece = self.board.piece_at(chess.square(col, 7-row))
                if piece:
                    self.buttons[row][col].config(image=self.piece_images[piece.symbol()][color])
                else:
                    self.buttons[row][col].config(image=self.empty_images[color])

    def make_move(self, move):
        self.board.push(move)
        self.update_board()
        self.status_label.config(text="AI is thinking...")
        if not self.board.is_game_over():
            self.master.after(100, self.make_ai_move)
        else:
            self.game_over()

    def make_ai_move(self):
        try:
            if self.ai_opponent == "gpt":
                ai_move = play_chess_gpt(self.board, self.api_key)
            else:
                ai_move = play_chess_claude(self.board, self.api_key)

            move = chess.Move.from_uci(ai_move)
            if move in self.board.legal_moves:
                self.board.push(move)
                self.update_board()
                self.status_label.config(text="Your turn")
                if self.board.is_game_over():
                    self.game_over()
            else:
                raise ValueError("Invalid move")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            self.master.quit()

    def game_over(self):
        result = self.board.result()
        if result == "1-0":
            message = "You win!"
        elif result == "0-1":
            message = "AI wins!"
        else:
            message = "It's a draw!"
        messagebox.showinfo("Game Over", message)
        self.master.quit()

def main():
    root = tk.Tk()
    ChessGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()