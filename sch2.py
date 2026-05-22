import tkinter as tk
from tkinter import messagebox
import chess

class HolzSchachGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Klassisches Schachspiel mit Steuerung")
        self.root.configure(bg="#f3e5ab")
        
        self.board = chess.Board()
        self.selected_square = None
        self.labels = {}
        
        # Exakte Farbwerte
        self.light_color = "#f0d9b5"   # Cremeweiß / Beige
        self.dark_color = "#b58863"    # Klassisches Schach-Braun
        self.select_color = "#d4a373"  # Sanfter Highlight-Ton
        self.button_color = "#e6ccb2"  # Angenehmes Hellbraun für Buttons
        self.button_hover = "#ddb892"  # Dunklerer Ton beim Drüberfahren
        
        # Figuren-Definitionen
        self.white_pieces = {
            'R': '♖', 'N': '♘', 'B': '♗', 'Q': '♕', 'K': '♔', 'P': '♙'
        }
        self.black_pieces = {
            'r': '♜', 'n': '♞', 'b': '♝', 'q': '♛', 'k': '♚', 'p': '♟'
        }
        
        # Haupt-Container für das Layout
        self.main_frame = tk.Frame(self.root, bg="#f3e5ab")
        self.main_frame.pack(padx=20, pady=20)
        
        # Frame für das Schachbrett (links)
        self.board_frame = tk.Frame(self.main_frame, bg="#f3e5ab")
        self.board_frame.grid(row=0, column=0, sticky="nsew")
        
        # Frame für die Buttons (rechts)
        self.sidebar_frame = tk.Frame(self.main_frame, bg="#f3e5ab")
        self.sidebar_frame.grid(row=0, column=1, padx=(30, 10), sticky="n")
        
        self.create_board_ui()
        self.create_sidebar_ui()
        self.update_board_display()

    def create_board_ui(self):
        for col in range(8):
            lbl = tk.Label(self.board_frame, text=chr(65 + col), font=("Helvetica", 14, "bold"), bg="#f3e5ab", fg="#333333")
            lbl.grid(row=0, column=col + 1, pady=5)

        for row in range(8):
            lbl_left = tk.Label(self.board_frame, text=str(8 - row), font=("Helvetica", 14, "bold"), bg="#f3e5ab", fg="#333333")
            lbl_left.grid(row=row + 1, column=0, padx=10)
            
            for col in range(8):
                square = chess.square(col, 7 - row)
                bg_color = self.light_color if (row + col) % 2 == 0 else self.dark_color
                
                cell = tk.Label(
                    self.board_frame, 
                    text="", 
                    bg=bg_color, 
                    font=("Arial", 38), 
                    width=3, 
                    height=1,
                    relief="flat"
                )
                cell.grid(row=row + 1, column=col + 1)
                cell.bind("<Button-1>", lambda event, s=square: self.handle_square_click(s))
                self.labels[square] = cell

            lbl_right = tk.Label(self.board_frame, text=str(8 - row), font=("Helvetica", 14, "bold"), bg="#f3e5ab", fg="#333333")
            lbl_right.grid(row=row + 1, column=9, padx=10)

        for col in range(8):
            lbl = tk.Label(self.board_frame, text=chr(65 + col), font=("Helvetica", 14, "bold"), bg="#f3e5ab", fg="#333333")
            lbl.grid(row=9, column=col + 1, pady=5)

    def create_sidebar_ui(self):
        menu_title = tk.Label(self.sidebar_frame, text="Optionen", font=("Helvetica", 16, "bold"), bg="#f3e5ab", fg="#333333")
        menu_title.pack(pady=(10, 20))
        
        btn_style = {
            "font": ("Helvetica", 12, "bold"),
            "bg": self.button_color,
            "fg": "#333333",
            "activebackground": self.button_hover,
            "activeforeground": "#333333",
            "width": 18,
            "height": 2,
            "relief": "raised",
            "bd": 2,
            "cursor": "hand2"
        }
        
        self.btn_resign = tk.Button(self.sidebar_frame, text="🏳  Aufgeben", command=self.action_resign, **btn_style)
        self.btn_resign.pack(pady=10)
        self.bind_hover(self.btn_resign)
        
        self.btn_draw = tk.Button(self.sidebar_frame, text="🤝  Remis anbieten", command=self.action_draw, **btn_style)
        self.btn_draw.pack(pady=10)
        self.bind_hover(self.btn_draw)
        
        self.btn_undo = tk.Button(self.sidebar_frame, text="↩  Zug zurücknehmen", command=self.action_undo, **btn_style)
        self.btn_undo.pack(pady=10)
        self.bind_hover(self.btn_undo)

    def bind_hover(self, button):
        button.bind("<Enter>", lambda e: button.config(bg=self.button_hover))
        button.bind("<Leave>", lambda e: button.config(bg=self.button_color))

    def update_board_display(self):
        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
            
            file_idx = chess.square_file(square)
            rank_idx = chess.square_rank(square)
            ui_row = 7 - rank_idx
            bg_color = self.light_color if (ui_row + file_idx) % 2 == 0 else self.dark_color
            
            if piece:
                symbol = piece.symbol()
                if symbol.isupper():
                    text = self.white_pieces.get(symbol, "")
                else:
                    text = self.black_pieces.get(symbol, "")
            else:
                text = ""
                
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
            if chess.square_rank(square) in (0, 7):
                move.promotion = chess.QUEEN

        if move in self.board.legal_moves:
            self.board.push(move)
            self.selected_square = None
            self.update_board_display()
            self.root.update_idletasks()
            self.check_game_status()
        else:
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
            self.reset_game()

    # --- Button-Aktionen ---

    def action_resign(self):
        current_player = "Weiß" if self.board.turn == chess.WHITE else "Schwarz"
        winner = "Schwarz" if current_player == "Weiß" else "Weiß"
        
        confirm = messagebox.askyesno("Aufgeben", f"Möchte {current_player} wirklich aufgeben?")
        if confirm:
            messagebox.showinfo("Spielende", f"{current_player} hat aufgegeben. Gewinner: {winner}!")
            self.reset_game()

    def action_draw(self):
        current_player = "Weiß" if self.board.turn == chess.WHITE else "Schwarz"
        opponent = "Schwarz" if current_player == "Weiß" else "Weiß"
        
        confirm = messagebox.askyesno("Remisangebot", f"{current_player} bietet Remis an.\nNimmt {opponent} das Angebot an?")
        if confirm:
            messagebox.showinfo("Spielende", "Das Spiel endet unentschieden (Remis) durch Vereinbarung.")
            self.reset_game()

    def action_undo(self):
        if len(self.board.move_stack) == 0:
            messagebox.showwarning("Rückzug nicht möglich", "Es wurden noch keine Züge getätigt!")
            return

        # Ermitteln, wer um den Rückzug bittet
        applicant = "Weiß" if self.board.turn == chess.WHITE else "Schwarz"
        opponent = "Schwarz" if applicant == "Weiß" else "Weiß"
        
        # NEU: Bestätigungsabfrage an den Gegner
        confirm = messagebox.askyesno(
            "Zug zurücknehmen", 
            f"{applicant} möchte den letzten Zug zurücknehmen.\nErlaubt {opponent} den Rückzug?"
        )
        
        if confirm:
            # Wenn zwei oder mehr Züge auf dem Stack liegen, setzen wir beide zurück, 
            # damit der Antragsteller wieder dran ist.
            if len(self.board.move_stack) >= 2:
                self.board.pop()
                self.board.pop()
            else:
                # Falls erst ein einziger Zug im Spiel existiert
                self.board.pop()
                
            self.selected_square = None
            self.update_board_display()
            messagebox.showinfo("Rückzug", "Der Zug wurde erfolgreich zurückgenommen.")

    def reset_game(self):
        self.board.reset()
        self.selected_square = None
        self.update_board_display()

if __name__ == "__main__":
    root = tk.Tk()
    app = HolzSchachGUI(root)
    root.mainloop()

