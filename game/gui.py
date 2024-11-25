import tkinter as tk
from tkinter import ttk
from .constants import Move, MOVE_IMAGES
from .game_logic import GameLogic
from .ai_player import AIPlayer

class GameGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Rock Paper Scissors Lizard Spock")
        self.window.geometry("800x600")
        
        self.ai_player = AIPlayer()
        self.game_logic = GameLogic()
        self.score = {"WIN": 0, "LOSE": 0, "TIE": 0}
        
        self._create_widgets()
        
    def _create_widgets(self):
        # Score display
        score_frame = ttk.Frame(self.window)
        score_frame.pack(pady=20)
        
        self.score_label = ttk.Label(
            score_frame, 
            text="Score - Wins: 0 | Losses: 0 | Ties: 0",
            font=("Arial", 14)
        )
        self.score_label.pack()
        
        # Game status
        self.status_label = ttk.Label(
            self.window,
            text="Choose your move!",
            font=("Arial", 16)
        )
        self.status_label.pack(pady=20)
        
        # Move buttons
        buttons_frame = ttk.Frame(self.window)
        buttons_frame.pack(pady=20)
        
        for move in Move:
            btn = ttk.Button(
                buttons_frame,
                text=f"{MOVE_IMAGES[move]} {move.value}",
                command=lambda m=move: self.play_round(m)
            )
            btn.pack(side=tk.LEFT, padx=10)
            
        # History display
        history_frame = ttk.Frame(self.window)
        history_frame.pack(pady=20, fill=tk.BOTH, expand=True)
        
        self.history_text = tk.Text(
            history_frame,
            height=10,
            width=50,
            font=("Arial", 12)
        )
        self.history_text.pack(padx=20)
        
    def play_round(self, player_move: Move):
        ai_move = self.ai_player.make_move()
        result, description = self.game_logic.determine_winner(player_move, ai_move)
        
        # Update score and display
        self.score[result] += 1
        self.score_label.config(
            text=f"Score - Wins: {self.score['WIN']} | Losses: {self.score['LOSE']} | Ties: {self.score['TIE']}"
        )
        
        # Update status
        status_text = f"You chose {MOVE_IMAGES[player_move]}, AI chose {MOVE_IMAGES[ai_move]}\n{description}"
        self.status_label.config(text=status_text)
        
        # Update history
        self.history_text.insert(
            "1.0",
            f"Round: You {player_move.value} vs AI {ai_move.value} - {result}\n"
        )
        
        # AI learns from this round
        self.ai_player.learn_from_game(player_move, ai_move, result)
        
    def run(self):
        self.window.mainloop()