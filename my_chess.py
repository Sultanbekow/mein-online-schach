import tkinter as tk
from tkinter import messagebox
import chess

class InteractiveChess:
    def __init__(self, root):
        self.root = root
        self.root.title("Interaktives Python Schach")
        
        # Schach-Logik initialisieren
        self.board = chess.Board()
        
        # Spielzustand
        self.selected_square = None
        self.buttons = {}
        
        # Realistische Schachbrett-Farben
        self.light_color = "#eeeed2"  # Cremeweiß / Hell
        self.dark_color = "#769656"   # Klassisches Turnierschach-Grün
        self.select_color = "#bac466" # Sanftes Gelb/Grün für die Auswahl
        
        # Unicode-Zeichen für die Schachfiguren
        self.piece_symbols = {
            'R': '♖', 'N': '♘', 'B': '♗', 'Q': '♕', 'K': '♔', 'P': '♙',
            'r': '♜', 'n': '♞', 'b': '♝', 'q': '♛', 'k': '♚', 'p': '♟'
        }
        
        self.create_board_ui()
        self.update_board_display()

    def create_board_ui(self):
        # 1. Obere Beschriftung (Spalten A-H)
        for col in range(8):
            lbl = tk.Label(self.root, text=chr(65 + col), font=("Helvetica", 12, "bold"))
            lbl.grid(row=0, column=col + 1, pady=5)

        # 2. Hauptspielfeld mit seitlichen Zeilennummern
        for row in range(8):
            # Linke Beschriftung (Zeilen 8-1) -> HIER WURDE px ZU padx KORRIGIERT
            lbl_left = tk.Label(self.root, text=str(8 - row), font=("Helvetica", 12, "bold"))
            lbl_left.grid(row=row + 1, column=0, padx=10)
            
            for col in range(8):
                square = chess.square(col, 7 - row)
                
                # Wechselschritt für die schwarz-weißen Felder
                bg_color = self.light_color if (row + col) % 2 == 0 else self.dark_color
                
                btn = tk.Button(
                    self.root, 
                    text="", 
                    bg=bg_color, 
                    font=("Helvetica", 24), 
                    width=4, 
                    height=2,
                    relief="flat",
                    command=lambda s=square: self.handle_square_click(s)
                )
                btn.grid(row=row + 1, column=col + 1)
                self.buttons[square] = btn

            # Rechte Beschriftung (Zeilen 8-1) -> HIER WURDE px ZU padx KORRIGIERT
            lbl_right = tk.Label(self.root, text=str(8 - row), font=("Helvetica", 12, "bold"))
            lbl_right.grid(row=row + 1, column=9, padx=10)

        # 3. Untere Beschriftung (Spalten A-H)
        for col in range(8):
            lbl = tk.Label(self.root, text=chr(65 + col), font=("Helvetica", 12, "bold"))
            lbl.grid(row=9, column=col + 1, pady=5)

    def update_board_display(self):
        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
            text = self.piece_symbols.get(piece.symbol(), "") if piece else ""
            self.buttons[square].config(text=text)
            
            # Farben zurücksetzen
            file_idx = chess.square_file(square)
            rank_idx = chess.square_rank(square)
            ui_row = 7 - rank_idx
            
            bg_color = self.light_color if (ui_row + file_idx) % 2 == 0 else self.dark_color
            self.buttons[square].config(bg=bg_color)

    def handle_square_click(self, square):
        if self.selected_square is None:
            piece = self.board.piece_at(square)
            if piece and piece.color == self.board.turn:
                self.selected_square = square
                self.buttons[square].config(bg=self.select_color)
            return

        if self.selected_square == square:
            self.selected_square = None
            self.update_board_display()
            return

        move = chess.Move(self.selected_square, square)
        
        # Automatische Umwandlung in Dame bei Bauern-Promotion
        piece = self.board.piece_at(self.selected_square)
        if piece and piece.piece_type == chess.PAWN:
            if chess.square_rank(square) in [0, 7]:
                move.promotion = chess.QUEEN

        if move in self.board.legal_moves:
            self.board.push(move)
            self.selected_square = None
            self.update_board_display()
            self.check_game_status()
        else:
            target_piece = self.board.piece_at(square)
            if target_piece and target_piece.color == self.board.turn:
                self.selected_square = square
                self.update_board_display()
                self.buttons[square].config(bg=self.select_color)
            else:
                self.selected_square = None
                self.update_board_display()

    def check_game_status(self):
        if self.board.is_game_over():
            result = self.board.result()
            if self.board.is_checkmate():
                winner = "Schwarz" if self.board.turn == chess.WHITE else "Weiß"
                msg = f"Schachmatt! Gewinner: {winner}"
            elif self.board.is_stalemate():
                msg = "Unentschieden durch Patt!"
            else:
                msg = f"Spiel vorbei! Ergebnis: {result}"
                
            messagebox.showinfo("Spielende", msg)
            self.board.reset()
            self.update_board_display()

if __name__ == "__main__":
    root = tk.Tk()
    app = InteractiveChess(root)
    root.mainloop()

