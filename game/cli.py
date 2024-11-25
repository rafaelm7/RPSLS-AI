from .constants import Move, MOVE_SYMBOLS
from .game_logic import GameLogic
from .ai_player import AIPlayer

class GameCLI:
    def __init__(self):
        self.ai_player = AIPlayer()
        self.game_logic = GameLogic()
        self.score = {"WIN": 0, "LOSE": 0, "TIE": 0}
        
    def display_welcome(self):
        print("\n=== Rock Paper Scissors Lizard Spock ===")
        print("\nControls:")
        for move in Move:
            print(f"{MOVE_SYMBOLS[move]} - {move.value}")
        print("Q - Quit")
        
    def display_score(self):
        print(f"\nScore - Wins: {self.score['WIN']} | Losses: {self.score['LOSE']} | Ties: {self.score['TIE']}")
        
    def get_player_move(self) -> Move:
        valid_inputs = {MOVE_SYMBOLS[move]: move for move in Move}
        while True:
            choice = input("\nEnter your move: ").upper()
            if choice == 'Q':
                return None
            if choice in valid_inputs:
                return valid_inputs[choice]
            print("Invalid move! Try again.")
            
    def play_round(self, player_move: Move):
        ai_move = self.ai_player.make_move()
        result, description = self.game_logic.determine_winner(player_move, ai_move)
        
        print(f"\nYou chose: {player_move.value}")
        print(f"AI chose: {ai_move.value}")
        print(f"Result: {description}")
        
        self.score[result] += 1
        self.ai_player.learn_from_game(player_move, ai_move, result)
        
    def run(self):
        self.display_welcome()
        
        while True:
            self.display_score()
            player_move = self.get_player_move()
            
            if player_move is None:
                break
                
            self.play_round(player_move)
            
        print("\nThanks for playing! Final score:")
        self.display_score()