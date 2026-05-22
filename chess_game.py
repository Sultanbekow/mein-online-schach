import tkinter as tk
from tkinter import messagebox
import chess

class InteractiveChess:
    def __init__(self, root):
        self.root = root
        self.root.title("Interactive Python Chess")
        
        # Initialize the chess board logic
        self.board = chess.Board()
        
        # Game state tracking
        self.selected_square = None
        self.buttons = {}
        
        # Colors for the board
        self.light_color = "#f0d9b5"
        self.dark_color = "#b58863"
        self.select_color = "#70a1ff"  # Highlight color when selected
        
        # Unicode characters for chess pieces
        self.piece_symbols = {
            'R': '♖', 'N': '♘', 'B': '♗', 'Q': '♕', 'K': '♔', 'P': '♙',
            'r': '♜', 'n': '♞', 'b': '♝', 'q': '♛', 'k': '♚', 'p': '♟'
        }
        
        self.create_board_ui()
        self.update_board_display()

    def create_board_ui(self):
        # Create an 8x8 grid of buttons
        for row in range(8):
            for col in range(8):
                # Map 2D grid to python-chess square index (0 to 63)
                # Row 0 in UI is rank 8 (index 56-63), Column 0 is file A
                square = chess.square(col, 7 - row)
                
                # Determine square color
                bg_color = self.light_color if (row + col) % 2 == 0 else self.dark_color
                
                # Create the button
                btn = tk.Button(
                    self.root, 
                    text="", 
                    bg=bg_color, 
                    font=("Helvetica", 24), 
                    width=4, 
                    height=2,
                    command=lambda s=square: self.handle_square_click(s)
                )
                btn.grid(row=row, column=col)
                self.buttons[square] = btn

    def update_board_display(self):
        # Redraw pieces and reset background colors
        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
            
            # Set piece symbol
            if piece:
                text = self.piece_symbols.get(piece.symbol(), "")
            else:
                text = ""
                
            self.buttons[square].config(text=text)
            
            # Reset background color
            file_idx = chess.square_file(square)
            rank_idx = chess.square_rank(square)
            # Invert rank for UI row mapping
            ui_row = 7 - rank_idx
            
            bg_color = self.light_color if (ui_row + file_idx) % 2 == 0 else self.dark_color
            self.buttons[square].config(bg=bg_color)

    def handle_square_click(self, square):
        # Case 1: No piece is currently selected
        if self.selected_square is None:
            piece = self.board.piece_at(square)
            if piece is not None:
                # Only allow selecting pieces belonging to the current player
                if piece.color == self.board.turn:
                    self.selected_square = square
                    self.buttons[square].config(bg=self.select_color)
            return

        # Case 2: Clicked the exact same piece again -> Deselect it
        if self.selected_square == square:
            self.selected_square = None
            self.update_board_display()
            return

        # Case 3: A piece was already selected -> Attempt to make a move
        move = chess.Move(self.selected_square, square)
        
        # Check for pawn promotion (auto-promote to Queen for simplicity)
        piece = self.board.piece_at(self.selected_square)
        if piece and piece.piece_type == chess.PAWN:
            if chess.square_rank(square) in [0, 7]:
                move.promotion = chess.QUEEN

        # Execute move if it is legal
        if move in self.board.legal_moves:
            self.board.push(move)
            self.selected_square = None
            self.update_board_display()
            self.check_game_status()
        else:
            # If target click is another player piece, change selection instead of showing error
            target_piece = self.board.piece_at(square)
            if target_piece and target_piece.color == self.board.turn:
                self.selected_square = square
                self.update_board_display()
                self.buttons[square].config(bg=self.select_color)
            else:
                # Invalid move attempted
                self.selected_square = None
                self.update_board_display()

    def check_game_status(self):
        if self.board.is_game_over():
            result = self.board.result()
            if self.board.is_checkmate():
                winner = "Black" if self.board.turn == chess.WHITE else "White"
                msg = f"Checkmate! Winner: {winner}"
            elif self.board.is_stalemate():
                msg = "Draw by Stalemate!"
            elif self.board.is_insufficient_material():
                msg = "Draw by Insufficient Material!"
            else:
                msg = f"Game Over! Result: {result}"
                
            messagebox.showinfo("Match Result", msg)
            self.board.reset()
            self.update_board_display()

if __name__ == "__main__":
    root = tk.Tk()
    app = InteractiveChess(root)
    root.mainloop()

