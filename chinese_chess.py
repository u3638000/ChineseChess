import pygame


class ChineseChess:
    def __init__(self, window_size=(800, 900), board_margin=50):
        pygame.init()
        
        # Game state
        self.selected_piece = None
        self.turn = 'red'  # Red starts first
        self.game_over = False
        self.winner = None
        
        # Board configuration
        self.window_size = window_size
        self.board_margin = board_margin
        self.board_width = window_size[0] - 2 * board_margin
        self.board_height = window_size[0] - 2 * board_margin  # Square board area
        self.cell_size = self.board_width / 8
        
        # Screen setup
        self.screen = pygame.display.set_mode(window_size)
        pygame.display.set_caption("Chinese Chess")
        
        # Colors
        self.BACKGROUND_COLOR = (240, 217, 181)
        self.LINE_COLOR = (0, 0, 0)
        self.RED_COLOR = (200, 0, 0)
        self.BLACK_COLOR = (0, 0, 0)
        self.HIGHLIGHT_COLOR = (0, 255, 0, 128)
        self.MOVE_HINT_COLOR = (0, 0, 255, 128)
        
        # Load assets or set up piece representations
        self.setup_pieces()
        
        # Initialize board state (9x10 grid for Chinese Chess)
        self.board = self.create_initial_board()
        
        # Font for rendering text
        self.font = pygame.font.SysFont('simsun', 24)
        self.small_font = pygame.font.SysFont('simsun', 16)
        
        # Move history
        self.move_history = []
    
    def load_board(self, board, turn='red'):
        # Not Tested
        """Load a custom board state"""
        if len(board) != 10 or any(len(row) != 9 for row in board):
            raise ValueError("Board must be a 10x9 grid")
        self.reset()
        """Reset the game to its initial state"""
        self.board = board
        self.selected_piece = None
        self.turn = turn
        self.game_over = False
        self.winner = None
        self.move_history = []
        return self.get_state

    def create_initial_board(self):
        """Create the initial board setup for Chinese Chess"""
        # Create empty 9x10 board
        board = [[None for _ in range(9)] for _ in range(10)]
        
        # Place pieces - standard Xiangqi setup
        # Chariot (Rook)
        board[0][0] = {'type': 'chariot', 'color': 'black'}
        board[0][8] = {'type': 'chariot', 'color': 'black'}
        board[9][0] = {'type': 'chariot', 'color': 'red'}
        board[9][8] = {'type': 'chariot', 'color': 'red'}
        
        # Horse (Knight)
        board[0][1] = {'type': 'horse', 'color': 'black'}
        board[0][7] = {'type': 'horse', 'color': 'black'}
        board[9][1] = {'type': 'horse', 'color': 'red'}
        board[9][7] = {'type': 'horse', 'color': 'red'}
        
        # Elephant
        board[0][2] = {'type': 'elephant', 'color': 'black'}
        board[0][6] = {'type': 'elephant', 'color': 'black'}
        board[9][2] = {'type': 'elephant', 'color': 'red'}
        board[9][6] = {'type': 'elephant', 'color': 'red'}
        
        # Advisor
        board[0][3] = {'type': 'advisor', 'color': 'black'}
        board[0][5] = {'type': 'advisor', 'color': 'black'}
        board[9][3] = {'type': 'advisor', 'color': 'red'}
        board[9][5] = {'type': 'advisor', 'color': 'red'}
        
        # General (King)
        board[0][4] = {'type': 'general', 'color': 'black'}
        board[9][4] = {'type': 'general', 'color': 'red'}
        
        # Cannon
        board[2][1] = {'type': 'cannon', 'color': 'black'}
        board[2][7] = {'type': 'cannon', 'color': 'black'}
        board[7][1] = {'type': 'cannon', 'color': 'red'}
        board[7][7] = {'type': 'cannon', 'color': 'red'}
        
        # Soldier (Pawn)
        for i in range(0, 9, 2):
            board[3][i] = {'type': 'soldier', 'color': 'black'}
            board[6][i] = {'type': 'soldier', 'color': 'red'}
        
        return board
    
    def setup_pieces(self):
        """Set up piece representations - using simple Unicode characters"""
        self.pieces = {
            'red': {
                'general': '帅',
                'advisor': '仕',
                'elephant': '相',
                'horse': '马',
                'chariot': '车',
                'cannon': '炮',
                'soldier': '兵'
            },
            'black': {
                'general': '将',
                'advisor': '士',
                'elephant': '象',
                'horse': '马',
                'chariot': '车',
                'cannon': '炮',
                'soldier': '卒'
            }
        }
    
    def draw_board(self):
        """Draw the Chinese Chess board"""
        # Fill background
        self.screen.fill(self.BACKGROUND_COLOR)
        
        # Draw board area
        board_rect = pygame.Rect(
            self.board_margin, 
            self.board_margin, 
            self.board_width, 
            self.board_height + self.cell_size
        )
        pygame.draw.rect(self.screen, (220, 179, 92), board_rect)
        
        # Draw grid lines
        for i in range(10):  # Horizontal lines
            y = self.board_margin + i * self.cell_size
            pygame.draw.line(
                self.screen, 
                self.LINE_COLOR,
                (self.board_margin, y),
                (self.board_margin + self.board_width, y),
                2
            )
        
        for i in range(9):  # Vertical lines
            x = self.board_margin + i * self.cell_size
            # Top half
            pygame.draw.line(
                self.screen, 
                self.LINE_COLOR,
                (x, self.board_margin),
                (x, self.board_margin + 4 * self.cell_size),
                2
            )
            # Bottom half
            pygame.draw.line(
                self.screen, 
                self.LINE_COLOR,
                (x, self.board_margin + 5 * self.cell_size),
                (x, self.board_margin + 9 * self.cell_size),
                2
            )
        
        # Draw palace diagonal lines
        # Black palace
        pygame.draw.line(
            self.screen, 
            self.LINE_COLOR,
            (self.board_margin + 3 * self.cell_size, self.board_margin),
            (self.board_margin + 5 * self.cell_size, self.board_margin + 2 * self.cell_size),
            2
        )
        pygame.draw.line(
            self.screen, 
            self.LINE_COLOR,
            (self.board_margin + 5 * self.cell_size, self.board_margin),
            (self.board_margin + 3 * self.cell_size, self.board_margin + 2 * self.cell_size),
            2
        )
        
        # Red palace
        pygame.draw.line(
            self.screen, 
            self.LINE_COLOR,
            (self.board_margin + 3 * self.cell_size, self.board_margin + 7 * self.cell_size),
            (self.board_margin + 5 * self.cell_size, self.board_margin + 9 * self.cell_size),
            2
        )
        pygame.draw.line(
            self.screen, 
            self.LINE_COLOR,
            (self.board_margin + 5 * self.cell_size, self.board_margin + 7 * self.cell_size),
            (self.board_margin + 3 * self.cell_size, self.board_margin + 9 * self.cell_size),
            2
        )
        
        # Draw river text
        river_text = self.font.render("楚 河        汉 界", True, self.LINE_COLOR)
        text_rect = river_text.get_rect(center=(self.window_size[0] // 2, self.board_margin + 4.5 * self.cell_size))
        self.screen.blit(river_text, text_rect)
    
    def draw_pieces(self):
        """Draw all pieces on the board"""
        for row in range(10):
            for col in range(9):
                piece = self.board[row][col]
                if piece:
                    # Calculate position
                    x = self.board_margin + col * self.cell_size
                    y = self.board_margin + row * self.cell_size
                    
                    # Draw piece background
                    pygame.draw.circle(
                        self.screen,
                        (230, 200, 140),
                        (x, y),
                        self.cell_size // 2 - 4
                    )
                    pygame.draw.circle(
                        self.screen,
                        self.RED_COLOR if piece['color'] == 'red' else self.BLACK_COLOR,
                        (x, y),
                        self.cell_size // 2 - 4,
                        2
                    )
                    
                    # Draw piece text
                    piece_text = self.pieces[piece['color']][piece['type']]
                    text_surface = self.font.render(
                        piece_text, 
                        True, 
                        self.RED_COLOR if piece['color'] == 'red' else self.BLACK_COLOR
                    )
                    text_rect = text_surface.get_rect(center=(x, y))
                    self.screen.blit(text_surface, text_rect)
                    
                    # Highlight selected piece
                    if self.selected_piece and self.selected_piece == (row, col):
                        highlight_surface = pygame.Surface((self.cell_size, self.cell_size), pygame.SRCALPHA)
                        highlight_surface.fill((0, 255, 0, 80))
                        self.screen.blit(
                            highlight_surface, 
                            (x - self.cell_size // 2, y - self.cell_size // 2)
                        )
    
    def draw_game_status(self):
        """Draw game status information"""
        # Draw whose turn it is
        turn_text = f"Turn: {'Red' if self.turn == 'red' else 'Black'}"
        text_surface = self.small_font.render(turn_text, True, self.LINE_COLOR)
        self.screen.blit(text_surface, (10, 10))
        
        # Draw game over message if applicable
        if self.game_over:
            msg = f"Game Over! {self.winner.capitalize()} wins!"
            text_surface = self.font.render(msg, True, self.RED_COLOR if self.winner == 'red' else self.BLACK_COLOR)
            text_rect = text_surface.get_rect(center=(self.window_size[0] // 2, self.window_size[1] - 40))
            self.screen.blit(text_surface, text_rect)

    def get_action_space(self, player=None):
        """Get the action space for the game"""
        player = self.turn if player is None else player
        print(f"Getting action space for {player}")
        actions = []
        for row in range(10):
            for col in range(9):
                piece = self.board[row][col]
                if piece and piece['color'] == player:
                    print(f"Found piece at ({row}, {col}): {piece}")
                    valid_moves = self.get_valid_moves(row, col)
                    for move in valid_moves:
                        actions.append(((row, col), move))
        return actions

    def get_valid_moves(self, row, col):
        """Get all valid moves for the piece at the given position"""
        piece = self.board[row][col]
        print(f"Getting valid moves for piece at ({row}, {col}): {piece}")
        if not piece:
            return []
        
        valid_moves = []
        
        # Different movement rules for each piece type
        if piece['type'] == 'chariot':  # Rook movement
            # Horizontal moves
            for c in range(col + 1, 9):
                if self.board[row][c] is None:
                    valid_moves.append((row, c))
                else:
                    if self.board[row][c]['color'] != piece['color']:
                        valid_moves.append((row, c))
                    break
            
            for c in range(col - 1, -1, -1):
                if self.board[row][c] is None:
                    valid_moves.append((row, c))
                else:
                    if self.board[row][c]['color'] != piece['color']:
                        valid_moves.append((row, c))
                    break
            
            # Vertical moves
            for r in range(row + 1, 10):
                if self.board[r][col] is None:
                    valid_moves.append((r, col))
                else:
                    if self.board[r][col]['color'] != piece['color']:
                        valid_moves.append((r, col))
                    break
            
            for r in range(row - 1, -1, -1):
                if self.board[r][col] is None:
                    valid_moves.append((r, col))
                else:
                    if self.board[r][col]['color'] != piece['color']:
                        valid_moves.append((r, col))
                    break
                
        elif piece['type'] == 'horse':  # Knight movement
            # All possible knight moves
            possible_moves = [
                (row - 2, col - 1), (row - 2, col + 1),
                (row - 1, col - 2), (row - 1, col + 2),
                (row + 1, col - 2), (row + 1, col + 2),
                (row + 2, col - 1), (row + 2, col + 1)
            ]
            
            # Check for blocking pieces (horse leg)
            for move_row, move_col in possible_moves:
                if 0 <= move_row < 10 and 0 <= move_col < 9:
                    # Check if the path is blocked
                    blocked = False
                    
                    # Determine the blocking position
                    if abs(move_row - row) == 2:  # Moving vertically first
                        block_row = row + (1 if move_row > row else -1)
                        block_col = col
                    else:  # Moving horizontally first
                        block_row = row
                        block_col = col + (1 if move_col > col else -1)
                    
                    if self.board[block_row][block_col] is not None:
                        blocked = True
                    
                    if not blocked and (self.board[move_row][move_col] is None or 
                                      self.board[move_row][move_col]['color'] != piece['color']):
                        valid_moves.append((move_row, move_col))
        
        elif piece['type'] == 'elephant':  # Elephant movement
            # Elephant moves diagonally by 2 points
            possible_moves = [
                (row - 2, col - 2), (row - 2, col + 2),
                (row + 2, col - 2), (row + 2, col + 2)
            ]
            
            for move_row, move_col in possible_moves:
                # Check if in bounds and not crossing the river
                river_check = True
                if piece['color'] == 'red' and move_row < 5:
                    river_check = False
                if piece['color'] == 'black' and move_row > 4:
                    river_check = False
                
                if (0 <= move_row < 10 and 0 <= move_col < 9 and river_check):
                    # Check if the diagonal path is blocked
                    block_row = row + (1 if move_row > row else -1)
                    block_col = col + (1 if move_col > col else -1)
                    
                    if self.board[block_row][block_col] is None and (
                            self.board[move_row][move_col] is None or 
                            self.board[move_row][move_col]['color'] != piece['color']):
                        valid_moves.append((move_row, move_col))
        
        elif piece['type'] == 'advisor':  # Advisor movement
            # Advisor moves diagonally by 1 point within the palace
            possible_moves = [
                (row - 1, col - 1), (row - 1, col + 1),
                (row + 1, col - 1), (row + 1, col + 1)
            ]
            
            for move_row, move_col in possible_moves:
                # Check if in palace bounds
                in_palace = False
                if piece['color'] == 'red':
                    if 7 <= move_row <= 9 and 3 <= move_col <= 5:
                        in_palace = True
                else:  # black
                    if 0 <= move_row <= 2 and 3 <= move_col <= 5:
                        in_palace = True
                
                if in_palace and (self.board[move_row][move_col] is None or 
                                 self.board[move_row][move_col]['color'] != piece['color']):
                    valid_moves.append((move_row, move_col))
        
        elif piece['type'] == 'general':  # General movement
            # General moves orthogonally by 1 point within the palace
            possible_moves = [
                (row - 1, col), (row + 1, col),
                (row, col - 1), (row, col + 1)
            ]
            
            for move_row, move_col in possible_moves:
                # Check if in palace bounds
                in_palace = False
                if piece['color'] == 'red':
                    if 7 <= move_row <= 9 and 3 <= move_col <= 5:
                        in_palace = True
                else:  # black
                    if 0 <= move_row <= 2 and 3 <= move_col <= 5:
                        in_palace = True
                
                if in_palace and (self.board[move_row][move_col] is None or 
                                 self.board[move_row][move_col]['color'] != piece['color']):
                    valid_moves.append((move_row, move_col))
            
            # Check for flying general rule
            opposing_general_col = col
            found_piece = False
            
            if piece['color'] == 'red':
                # Look upward for black general
                for r in range(row - 1, -1, -1):
                    if self.board[r][col] is not None:
                        found_piece = True
                        if (self.board[r][col]['type'] == 'general' and 
                            self.board[r][col]['color'] != piece['color']):
                            valid_moves.append((r, col))
                        break
            else:
                # Look downward for red general
                for r in range(row + 1, 10):
                    if self.board[r][col] is not None:
                        found_piece = True
                        if (self.board[r][col]['type'] == 'general' and 
                            self.board[r][col]['color'] != piece['color']):
                            valid_moves.append((r, col))
                        break
        
        elif piece['type'] == 'cannon':  # Cannon movement
            # Horizontal moves
            found_platform = False
            for c in range(col + 1, 9):
                if not found_platform:
                    if self.board[row][c] is None:
                        valid_moves.append((row, c))
                    else:
                        found_platform = True
                else:
                    if self.board[row][c] is not None:
                        if self.board[row][c]['color'] != piece['color']:
                            valid_moves.append((row, c))
                        break
            
            found_platform = False
            for c in range(col - 1, -1, -1):
                if not found_platform:
                    if self.board[row][c] is None:
                        valid_moves.append((row, c))
                    else:
                        found_platform = True
                else:
                    if self.board[row][c] is not None:
                        if self.board[row][c]['color'] != piece['color']:
                            valid_moves.append((row, c))
                        break
            
            # Vertical moves
            found_platform = False
            for r in range(row + 1, 10):
                if not found_platform:
                    if self.board[r][col] is None:
                        valid_moves.append((r, col))
                    else:
                        found_platform = True
                else:
                    if self.board[r][col] is not None:
                        if self.board[r][col]['color'] != piece['color']:
                            valid_moves.append((r, col))
                        break
            
            found_platform = False
            for r in range(row - 1, -1, -1):
                if not found_platform:
                    if self.board[r][col] is None:
                        valid_moves.append((r, col))
                    else:
                        found_platform = True
                else:
                    if self.board[r][col] is not None:
                        if self.board[r][col]['color'] != piece['color']:
                            valid_moves.append((r, col))
                        break
        
        elif piece['type'] == 'soldier':  # Soldier movement
            if piece['color'] == 'red':
                # Red soldiers move up or horizontally if across the river
                possible_moves = [(row - 1, col)]  # Always can move forward
                
                # If crossed the river, can also move horizontally
                if row < 5:
                    possible_moves.extend([(row, col - 1), (row, col + 1)])
            else:
                # Black soldiers move down or horizontally if across the river
                possible_moves = [(row + 1, col)]  # Always can move forward
                
                # If crossed the river, can also move horizontally
                if row > 4:
                    possible_moves.extend([(row, col - 1), (row, col + 1)])
            
            for move_row, move_col in possible_moves:
                if (0 <= move_row < 10 and 0 <= move_col < 9 and
                    (self.board[move_row][move_col] is None or 
                     self.board[move_row][move_col]['color'] != piece['color'])):
                    valid_moves.append((move_row, move_col))
        
        for move in valid_moves:
            move_row, move_col = move
            # Ensure the move does not put the player's general in check
            if not self.is_move_valid((row, col), (move_row, move_col)):
                print(f"Invalid move {move} for piece at {(row, col)} to {(move_row, move_col)}")
                valid_moves.remove(move)

        print(f"End Getting valid moves for piece at ({row}, {col}): {piece}")
        print(f"Valid moves: {valid_moves}")
        return valid_moves
    
    def draw_valid_moves(self, moves):
        """Draw indicators for valid moves"""
        for row, col in moves:
            x = self.board_margin + col * self.cell_size
            y = self.board_margin + row * self.cell_size
            
            # Draw move hint
            pygame.draw.circle(
                self.screen,
                (0, 0, 255, 128),
                (x, y),
                self.cell_size // 6
            )
    
    def is_in_check(self, color):
        """Check if the given color's general is in check"""
        # Find the general
        general_pos = None
        for row in range(10):
            for col in range(9):
                piece = self.board[row][col]
                if piece and piece['type'] == 'general' and piece['color'] == color:
                    general_pos = (row, col)
                    break
            if general_pos:
                break
        
        if not general_pos:
            return False  # No general found (shouldn't happen in a valid game)
        
        # Check if any opponent piece can capture the general
        opponent_color = 'black' if color == 'red' else 'red'
        for row in range(10):
            for col in range(9):
                piece = self.board[row][col]
                if piece and piece['color'] == opponent_color:
                    valid_moves = self.get_valid_moves(row, col)
                    if general_pos in valid_moves:
                        return True
        
        return False
    
    def is_move_valid(self, from_pos, to_pos):
        # Check if the move puts or leaves the player's general in check
        from_row, from_col = from_pos
        to_row, to_col = to_pos

        piece = self.board[from_row][from_col]
        assert piece is not None, "Piece must not be None"
        assert piece['color'] == self.turn, f"Piece {piece['color']} must belong to the current player {self.turn}"
        
        old_board = [row[:] for row in self.board]

        # Move the piece
        self.board[to_row][to_col] = self.board[from_row][from_col]
        self.board[from_row][from_col] = None
        # Check if the move puts the player's general in check
        if self.is_in_check(self.turn):
            # Undo the move
            self.board = old_board
            return False
        # Restore the board
        self.board = old_board
        # If the move does not put the general in check, it's valid
        return True

    def make_move(self, from_pos, to_pos):
        """Move a piece and handle captures"""

        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        # Check if the move is valid
        valid_moves = self.get_valid_moves(from_row, from_col)
        if (to_row, to_col) not in valid_moves:
            return False
        
        # Check if the piece belongs to the current player
        piece = self.board[from_row][from_col]
        if piece['color'] != self.turn:
            return False
        
        # Save the current board state to check for check after the move
        old_board = [row[:] for row in self.board]
        captured_piece = self.board[to_row][to_col]
        
        # Move the piece
        self.board[to_row][to_col] = self.board[from_row][from_col]
        self.board[from_row][from_col] = None
        
        # Check if the move puts or leaves the player's general in check
        if self.is_in_check(self.turn):
            # Undo the move
            self.board = old_board
            return False
        
        # Record the move
        self.move_history.append({
            'piece': piece,
            'from': from_pos,
            'to': to_pos,
            'captured': captured_piece
        })
        
        # Check if the opponent's general is in checkmate
        self.turn = 'black' if self.turn == 'red' else 'red'
        
        # Check for game over conditions
        if captured_piece and captured_piece['type'] == 'general':
            self.game_over = True
            self.winner = piece['color']

        # test get_action_space
        print(f"{self.turn}'s action space: {self.get_action_space()}")
        
        # Check if the new turn's player is in checkmate
        if self.is_checkmate(self.turn):
            self.game_over = True
            self.winner = 'red' if self.turn == 'black' else 'black'
        
        return True
    
    def is_checkmate(self, color):
        """Check if the given color is in checkmate"""
        if not self.is_in_check(color):
            return False
        
        # Try all possible moves for all pieces of the given color
        for row in range(10):
            for col in range(9):
                piece = self.board[row][col]
                if piece and piece['color'] == color:
                    valid_moves = self.get_valid_moves(row, col)
                    for move_row, move_col in valid_moves:
                        # Try the move
                        old_board = [row[:] for row in self.board]
                        self.board[move_row][move_col] = self.board[row][col]
                        self.board[row][col] = None
                        
                        # Check if still in check
                        still_in_check = self.is_in_check(color)
                        
                        # Restore the board
                        self.board = old_board
                        
                        if not still_in_check:
                            return False  # Found a move that gets out of check
        
        return True  # No moves can get out of check
    
    def handle_click(self, pos):
        """Handle mouse click at the given position"""
        if self.game_over:
            return
        
        # Convert screen position to board coordinates
        x, y = pos
        col = round((x - self.board_margin) / self.cell_size)
        row = round((y - self.board_margin) / self.cell_size)
        
        # Check if click is on the board
        if not (0 <= row < 10 and 0 <= col < 9):
            return
        
        # If a piece is already selected
        if self.selected_piece:
            selected_row, selected_col = self.selected_piece
            
            # If clicking on the same piece, deselect it
            if (row, col) == (selected_row, selected_col):
                self.selected_piece = None
                return
            
            # If clicking on a valid move, make the move
            valid_moves = self.get_valid_moves(selected_row, selected_col)
            if (row, col) in valid_moves:
                move_success = self.make_move((selected_row, selected_col), (row, col))
                self.selected_piece = None
                return
            
            # If clicking on another piece of the same color, select that piece instead
            piece_at_click = self.board[row][col]
            if piece_at_click and piece_at_click['color'] == self.turn:
                self.selected_piece = (row, col)
                return
            
            # Otherwise, deselect
            self.selected_piece = None
        else:
            # Select a piece if it belongs to the current player
            piece = self.board[row][col]
            if piece and piece['color'] == self.turn:
                self.selected_piece = (row, col)
    
    def reset(self):
        """Reset the game to its initial state"""
        self.board = self.create_initial_board()
        self.selected_piece = None
        self.turn = 'red'
        self.game_over = False
        self.winner = None
        self.move_history = []
        return self.get_state


if __name__ == "__main__":
    game = ChineseChess(window_size=(400, 450))
    
    # Main game loop
    running = True
    print(f"{game.turn}'s action space: {game.get_action_space()}")
    assert None
    while running:
        # print(f"action space: {game.get_action_space()}")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    game.handle_click(event.pos)
        
        # Draw everything
        game.draw_board()
        game.draw_pieces()
        if game.selected_piece:
            valid_moves = game.get_valid_moves(*game.selected_piece)
            game.draw_valid_moves(valid_moves)
        game.draw_game_status()
        
        pygame.display.flip()
    
    pygame.quit()