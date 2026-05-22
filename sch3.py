import tkinter as tk
from tkinter import messagebox
import chess
import socket
import threading

class OnlineHolzSchachGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Klassisches Online-Schachspiel")
        self.root.configure(bg="#f3e5ab")
        
        self.board = chess.Board()
        self.selected_square = None
        self.labels = {}
        
        # --- NETZWERK-SETUP ---
        # WICHTIG: Ersetzen Sie "127.0.0.1" durch die IP-Adresse des PCs, auf dem der C++ Server läuft!
        self.server_ip = "127.0.0.1" 
        self.server_port = 5555
        self.my_color = None # Wird vom Server zugewiesen (Weiß oder Schwarz)
        
        # Verbindung zum C++ Server aufbauen
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.server_ip, self.server_port))
            
            # Erste Nachricht vom Server empfangen (Farbe zuweisen)
            color_data = self.client_socket.recv(1024).decode()
            if "COLOR:W" in color_data:
                self.my_color = chess.WHITE
                self.root.title("Online-Schachspiel - Du bist WEISS")
            else:
                self.my_color = chess.BLACK
                self.root.title("Online-Schachspiel - Du bist SCHWARZ")
                
            # Hintergrund-Thread starten, um gegnerische Züge live zu empfangen
            threading.Thread(target=self.receive_opponent_moves, daemon=True).start()
            
        except Exception as e:
            messagebox.showerror("Verbindungsfehler", f"Konnte keine Verbindung zum C++ Server aufbauen:\n{e}\n\nDas Spiel startet im Offline-Modus.")
            self.my_color = None # Erlaubt lokales Testen ohne Server

        # --- GRAPHIK & FARBEN ---
        self.light_color = "#f0d9b5"   # Cremeweiß / Beige
        self.dark_color = "#b58863"    # Klassisches Schach-Braun
        self.select_color = "#d4a373"  # Sanfter Highlight-Ton
        self.button_color = "#e6ccb2"  # Angenehmes Hellbraun für Buttons
        self.button_hover = "#ddb892"  # Dunklerer Ton beim Drüberfahren
        
        self.white_pieces = {'R': '♖', 'N': '♘', 'B': '♗', 'Q': '♕', 'K': '♔', 'P': '♙'}
        self.black_pieces = {'r': '♜', 'n': '♞', 'b': '♝', 'q': '♛', 'k': '♚', 'p': '♟'}
        
        # Layout-Container
        self.main_frame = tk.Frame(self.root, bg="#f3e5ab")
        self.main_frame.pack(padx=20, pady=20)
        
        self.board_frame = tk.Frame(self.main_frame, bg="#f3e5ab")
        self.board_frame.grid(row=0, column=0, sticky="nsew")
        
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
                
                cell = tk.Label(self.board_frame, text="", bg=bg_color, font=("Arial", 38), width=3, height=1, relief="flat")
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
        
        btn_style = {"font": ("Helvetica", 12, "bold"), "bg": self.button_color, "fg": "#333333", 
                     "activebackground": self.button_hover, "activeforeground": "#333333", 
                     "width": 18, "height": 2, "relief": "raised", "bd": 2, "cursor": "hand2"}
        
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
            ui_row = 7 - chess.square_rank(square)
            bg_color = self.light_color if (ui_row + chess.square_file(square)) % 2 == 0 else self.dark_color
            
            if piece:
                symbol = piece.symbol()
                text = self.white_pieces.get(symbol, "") if symbol.isupper() else self.black_pieces.get(symbol, "")
            else:
                text = ""
                
            self.labels[square].config(text=text, fg="#000000", bg=bg_color)

    def handle_square_click(self, square):
        # ONLINE-REGEL: Man darf nur ziehen, wenn man an der Reihe ist UND es die eigene zugewiesene Farbe ist
        if self.my_color is not None and self.board.turn != self.my_color:
            return

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
        
        if piece and piece.piece_type == chess.PAWN and chess.square_rank(square) in (0, 7):
            move.promotion = chess.QUEEN

        if move in self.board.legal_moves:
            self.board.push(move)
            self.selected_square = None
            self.update_board_display()
            self.root.update_idletasks()
            
            # ONLINE-AKTION: Den eigenen Zug als Text (z.B. "e2e4") über den C++ Server senden
            if self.my_color is not None:
                try:
                    self.client_socket.send(f"MOVE:{move.uci()}".encode())
                except:
                    messagebox.showerror("Netzwerkfehler", "Zug konnte nicht gesendet werden.")
            
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

    # --- HINTERGRUND-THREAD: EMPFANGEN VOM C++ SERVER ---
    def receive_opponent_moves(self):
        while True:
            try:
                data = self.client_socket.recv(1024).decode()
                if not data:
                    break
                
                # Wenn der Gegner gezogen hat
                if data.startswith("MOVE:"):
                    move_uci = data.split(":")[1]
                    move = chess.Move.from_uci(move_uci)
                    self.board.push(move)
                    self.update_board_display()
                    self.check_game_status()
                
                # Wenn der Gegner aufgibt
                elif data == "CMD:RESIGN":
                    messagebox.showinfo("Spielende", "Der Gegner hat aufgegeben. Du hast gewonnen!")
                    self.reset_game()
                
                # Wenn der Gegner Remis anbietet
                elif data == "CMD:DRAW_REQUEST":
                    confirm = messagebox.askyesno("Remisangebot", "Der Gegner bietet ein Unentschieden an.\nAnnehmen?")
                    if confirm:
                        self.client_socket.send("CMD:DRAW_ACCEPT".encode())
                        messagebox.showinfo("Spielende", "Das Spiel endet unentschieden (Remis).")
                        self.reset_game()
                    else:
                        self.client_socket.send("CMD:DRAW_DECLINE".encode())
                
                elif data == "CMD:DRAW_ACCEPT":
                    messagebox.showinfo("Spielende", "Der Gegner hat das Remis angenommen. Unentschieden!")
                    self.reset_game()
                    
                elif data == "CMD:DRAW_DECLINE":
                    messagebox.showinfo("Remis abgelehnt", "Der Gegner hat das Remisangebot abgelehnt.")

                # Wenn der Gegner einen Zug zurücknehmen möchte
                elif data == "CMD:UNDO_REQUEST":
                    confirm = messagebox.askyesno("Rückzug", "Der Gegner möchte den letzten Zug zurücknehmen.\nErlauben?")
                    if confirm:
                        self.client_socket.send("CMD:UNDO_ACCEPT".encode())
                        self.execute_undo()
                    else:
                        self.client_socket.send("CMD:UNDO_DECLINE".encode())
                
                elif data == "CMD:UNDO_ACCEPT":
                    self.execute_undo()
                    messagebox.showinfo("Rückzug", "Der Gegner hat den Rückzug erlaubt.")
                    
                elif data == "CMD:UNDO_DECLINE":
                    messagebox.showinfo("Rückzug abgelehnt", "Der Gegner hat den Rückzug verweigert.")

            except:
                break
        messagebox.showwarning("Verbindung verloren", "Die Verbindung zum Server wurde unterbrochen.")

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

    # --- NETZWERK-BUTTON-AKTIONEN ---
    def action_resign(self):
        if self.my_color is None: return
        confirm = messagebox.askyesno("Aufgeben", "Möchtest du wirklich aufgeben?")
        if confirm:
            try:
                self.client_socket.send("CMD:RESIGN".encode())
            except: pass
            messagebox.showinfo("Spielende", "Du hast aufgegeben. Spiel vorbei.")
            self.reset_game()

    def action_draw(self):
        if self.my_color is None: return
        messagebox.showinfo("Remis", "Remisangebot wurde an den Gegner gesendet. Warte auf Antwort...")
        try:
            self.client_socket.send("CMD:DRAW_REQUEST".encode())
        except: pass

    def action_undo(self):
        if self.my_color is None: return
        if len(self.board.move_stack) == 0:
            messagebox.showwarning("Rückzug", "Es wurden noch keine Züge getätigt!")
            return
        messagebox.showinfo("Rückzug", "Anfrage zum Rückzug wurde gesendet. Warte auf Antwort...")
        try:
            self.client_socket.send("CMD:UNDO_REQUEST".encode())
        except: pass

    def execute_undo(self):
        # Nimmt zwei Züge zurück (den eigenen und den des Gegners)
        if len(self.board.move_stack) >= 2:
            self.board.pop()
            self.board.pop()
        elif len(self.board.move_stack) == 1:
            self.board.pop()
        self.selected_square = None
        self.update_board_display()

    def reset_game(self):
        self.board.reset()
        self.selected_square = None
        self.update_board_display()

if __name__ == "__main__":
    root = tk.Tk()
    app = OnlineHolzSchachGUI(root)
    root.mainloop()

