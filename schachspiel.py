import tkinter as tk
from tkinter import messagebox
import chess

class HolzSchachGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Klassisches Schachspiel")
        self.root.configure(bg="#f3e5ab") # Passender heller Hintergrund für das Fenster
        
        self.board = chess.Board()
        self.selected_square = None
        self.labels = {}  # Labels verhindern Mac-Anzeigefehler vollständig
        
        # Exakte Farbwerte aus dem Screenshot
        self.light_color = "#f0d9b5"   # Cremeweiß / Beige
        self.dark_color = "#b58863"    # Klassisches Schach-Braun
        self.select_color = "#d4a373"  # Sanfter Highlight-Ton für die Auswahl
        
        # Figuren-Definitionen exakt wie im Screenshot:
        # Weiß = Konturenfiguren (innen weiß, schwarzer Rand)
        # Schwarz = Vollständig ausgefüllte schwarze Figuren
        self.white_pieces = {
            'R': '♖', 'N': '♘', 'B': '♗', 'Q': '♕', 'K': '♔', 'P': '♙'
        }
        self.black_pieces = {
            'r': '♜', 'n': '♞', 'b': '♝', 'q': '♛', 'k': '♚', 'p': '♟'
        }
        
        self.create_board_ui()
        self.update_board_display()

    def create_board_ui(self):
        # Spaltenbeschriftung oben (A-H)
        for col in range(8):
            lbl = tk.Label(self.root, text=chr(65 + col), font=("Helvetica", 14, "bold"), bg="#f3e5ab", fg="#333333")
            lbl.grid(row=0, column=col + 1, pady=5)

        for row in range(8):
            # Zeilenbeschriftung links (8-1)
            lbl_left = tk.Label(self.root, text=str(8 - row), font=("Helvetica", 14, "bold"), bg="#f3e5ab", fg="#333333")
            lbl_left.grid(row=row + 1, column=0, padx=10)
            
            for col in range(8):
                square = chess.square(col, 7 - row)
                bg_color = self.light_color if (row + col) % 2 == 0 else self.dark_color
                
                cell = tk.Label(
                    self.root, 
                    text="", 
                    bg=bg_color, 
                    font=("Arial", 38), 
                    width=3, 
                    height=1,
                    relief="flat"
                )
                cell.grid(row=row + 1, column=col + 1)
                
                # Klick-Event an das Feld binden
                cell.bind("<Button-1>", lambda event, s=square: self.handle_square_click(s))
                self.labels[square] = cell

            # Zeilenbeschriftung rechts (8-1)
            lbl_right = tk.Label(self.root, text=str(8 - row), font=("Helvetica", 14, "bold"), bg="#f3e5ab", fg="#333333")
            lbl_right.grid(row=row + 1, column=9, padx=10)

        # Spaltenbeschriftung unten (A-H)
        for col in range(8):
            lbl = tk.Label(self.root, text=chr(65 + col), font=("Helvetica", 14, "bold"), bg="#f3e5ab", fg="#333333")
            lbl.grid(row=9, column=col + 1, pady=5)

    def update_board_display(self):
        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
            
            # Standard-Feldfarbe ermitteln
            file_idx = chess.square_file(square)
            rank_idx = chess.square_rank(square)
            ui_row = 7 - rank_idx
            bg_color = self.light_color if (ui_row + file_idx) % 2 == 0 else self.dark_color
            
            if piece:
                symbol = piece.symbol()
                if symbol.isupper():  # Weiße Figuren
                    text = self.white_pieces.get(symbol, "")
                else:  # Schwarze Figuren
                    text = self.black_pieces.get(symbol, "")
            else:
                text = ""
                
            # Alle Linien und Konturen werden in sattem Schwarz ("#000000") gezeichnet
            self.labels[square].config(text=text, fg="#000000", bg=bg_color)

    def handle_square_click(self, square):
        if self.selected_square is None:
            piece = self.board.piece_at(square)
            if piece and piece.color == self.board.turn:
                self.selected_square = square
                self.labels[square].config(bg=self.select_color)
            return

        if self.selected_square == square:
            self.selected_square = None
            self.update_board_display()
            return

        move = chess.Move(self.selected_square, square)
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
            # Falls auf eine eigene Figur geklickt wird, Auswahl dorthin wechseln
            target_piece = self.board.piece_at(square)
            if target_piece and target_piece.color == self.board.turn:
                self.selected_square = square
                self.update_board_display()
                self.labels[square].config(bg=self.select_color)
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
    app = HolzSchachGUI(root)
    root.mainloop()

