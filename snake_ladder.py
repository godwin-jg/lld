from abc import ABC, abstractmethod
import random
from collections import deque

# 1. Open/Closed Principle Extension Component
class Jump(ABC):
    def __init__(self, start: int, end: int):
        self.start = start
        self.end = end
    
    @abstractmethod
    def log_action(self) -> str: pass

class Snake(Jump):
    def log_action(self) -> str:
        return "🔴 Bitten by a Snake! Slid down to"

class Ladder(Jump):
    def log_action(self) -> str: 
        return "🪜 Climbed a Ladder! Advanced up to"

# 2. Board Blueprint
class Board:
    def __init__(self, size: int = 100):
        self.size = size
        self.jumps: dict[int, Jump] = {}

    def add_jump(self, jump: Jump) -> None:
        self.jumps[jump.start] = jump # starting position of the jump will have(JUMP) start and end as values

    def resolve_position(self, pos: int) -> int:
        """Recursively resolves position in case jumps chain together."""
        if pos in self.jumps:
            jump = self.jumps[pos]
            print(f"  └─> {jump.log_action()} {jump.end}")
            return self.resolve_position(jump.end) # instead of just returning jump.end
        return pos

# 3. Domain Entities
class Player:
    def __init__(self, name: str):
        self.name = name
        self.position = 0

class Dice:
    def __init__(self, sides: int = 6):
        self.sides = sides
    def roll(self) -> int: 
        return random.randint(1, self.sides)

# 4. Core Orchestrator
class SnakeAndLadderGame:
    def __init__(self, player_names: list[str]):
        self.board = Board()
        self.dice = Dice()
        self.players = deque([Player(name) for name in player_names])
        self._setup_board()

    def _setup_board(self) -> None:
        # Configuration setup matching standard LLD patterns
        for s, e in [(99, 54), (70, 55), (52, 29), (25, 6)]: 
            self.board.add_jump(Snake(s, e))
        for s, e in [(2, 38), (9, 31), (21, 42), (71, 92)]: 
            self.board.add_jump(Ladder(s, e))

    def play_turn(self) -> bool:
        curr_player = self.players[0]
        roll = self.dice.roll()
        target_pos = curr_player.position + roll
        
        print(f"\n🎲 {curr_player.name} rolled a {roll}. Current position: {curr_player.position}")
        
        if target_pos > self.board.size:
            print(f"  └─> ⚠️ Roll exceeds {self.board.size}. Stay at {curr_player.position}")
        else:
            curr_player.position = self.board.resolve_position(target_pos)
            print(f"  └─> Final position: {curr_player.position}")
            
        if curr_player.position == self.board.size:
            print(f"\n🎉🏆 {curr_player.name} WINS THE GAME! 🏆🎉")
            return True
            
        self.players.rotate(-1)
        return False


game = SnakeAndLadderGame(["Alice", "Bob"])
game_over = False
while not game_over:
    game_over = game.play_turn()
    
