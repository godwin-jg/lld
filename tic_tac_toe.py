from enum import Enum

class Piece(Enum):
    X = 'X'
    O = 'O'
    EMPTY = ' '    
class Player:
    def __init__(self, name, piece) -> None:
        self.name = name
        self.piece = piece
        
class Board:
    def __init__(self, size) -> None:
        self.size = size
        self.grid = [[Piece.EMPTY for _ in range(size)] for _ in range(size)]
    
    def is_valid_move(self, r, c):
        return 0 <= r < self.size and 0 <= c < self.size and self.grid[r][c] == Piece.EMPTY

    def place_piece(self, r, c, piece):
        self.grid[r][c] = piece
    
    def is_board_full(self):
        for row in self.grid:
            for cell in row:
                if cell == Piece.EMPTY:
                    return False
        return True

    def display(self):
        for row in self.grid:
            print(' | '.join(cell.value for cell in row))
            print('-' * 9)

        
class Game:
    def __init__(self, player1, player2, size) -> None:  
        self.board : Board = Board(size)
        self.players : list[Player] = [Player(player1, Piece.X), Player(player2, Piece.O)]
        
        self.turn_count = 0
        self.current_player : Player = self.players[0]
    
    def is_game_won(self, r, c):
        size = self.board.size
        grid = self.board.grid
        piece = self.current_player.piece
        
        if all(grid[r][i] ==  piece for i in range(len(grid))):
            return True

        if all(grid[i][c] ==  piece for i in range(len(grid))):
            return True
        
        if r == c and all(grid[i][i] == piece for i in range(size)):
            return True
        
        if r + c == size - 1 and all(grid[i][size - i - 1] == piece for i in range(size)):
            return True

        return False
    
    def play(self):
        while True:
            self.board.display()
            self.current_player = self.players[self.turn_count % 2]
            try:
                row, col = map(int, input("enter 'row col': ").split(" "))
                if not self.board.is_valid_move(row, col):
                    print("❌ Invalid move!")
                    continue
                
                self.board.place_piece(row, col, self.current_player.piece)
                
                if self.is_game_won(row, col):
                    self.board.display()
                    print(f"🎉 {self.current_player.name} WINS!")
                    return
                
                if self.board.is_board_full():
                    self.board.display()
                    print("🤝 Game Over! It's a DRAW!")
                    return
                
                self.turn_count += 1
                
            except Exception as e:
                print(e, "❌ Input format error.")

game = Game("Alice", "Bob", size=3)
game.play()