import pygame
import sys
import random
import time

# Khởi tạo Pygame
pygame.init()

# Kích thước ô cờ và bàn cờ
CELL_SIZE = 40
BOARD_SIZE = 15
WINDOW_SIZE = BOARD_SIZE * CELL_SIZE
HEADER_HEIGHT = 50
SCREEN_HEIGHT = WINDOW_SIZE + HEADER_HEIGHT

# Màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
BLUE = (0, 0, 200)
GRAY = (128, 128, 128)

# Khởi tạo cửa sổ game
screen = pygame.display.set_mode((WINDOW_SIZE, SCREEN_HEIGHT))
pygame.display.set_caption('Caro Game vs AI')

# Khởi tạo font
pygame.font.init()
font = pygame.font.SysFont('Arial', 32)

class CaroGame:
    def __init__(self):
        self.board = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.current_player = 1  # 1 là người chơi (X), 2 là AI (O)
        self.game_over = False
        self.winner = None
        
    def make_move(self, row, col):
        if self.board[row][col] == 0 and not self.game_over:
            self.board[row][col] = self.current_player
            if self.check_winner(row, col):
                self.game_over = True
                self.winner = self.current_player
                return True
            self.current_player = 3 - self.current_player
            if not self.game_over and self.current_player == 2:
                self.ai_move()
            return True
        return False
    
    def check_winner(self, row, col):
        player = self.board[row][col]
        for dr, dc in [(0,1), (1,0), (1,1), (1,-1)]:
            count = 1
            r, c = row + dr, col + dc
            while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and self.board[r][c] == player:
                count += 1
                r += dr
                c += dc
            r, c = row - dr, col - dc
            while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and self.board[r][c] == player:
                count += 1
                r -= dr
                c -= dc
            if count >= 5:
                return True
        return False

    def evaluate_position(self, row, col, player):
        score = 0
        for dr, dc in [(0,1), (1,0), (1,1), (1,-1)]:
            count = 1
            blocks = 0
            r, c = row + dr, col + dc
            
            # Kiểm tra một hướng
            while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE:
                if self.board[r][c] == player:
                    count += 1
                elif self.board[r][c] == 0:
                    break
                else:
                    blocks += 1
                    break
                r += dr
                c += dc
            
            r, c = row - dr, col - dc
            # Kiểm tra hướng ngược lại
            while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE:
                if self.board[r][c] == player:
                    count += 1
                elif self.board[r][c] == 0:
                    break
                else:
                    blocks += 1
                    break
                r -= dr
                c -= dc
            
            # Tính điểm dựa trên số quân và số chặn
            if count >= 5:
                score += 100000
            elif count == 4:
                if blocks == 0:
                    score += 10000
                elif blocks == 1:
                    score += 1000
            elif count == 3:
                if blocks == 0:
                    score += 1000
                elif blocks == 1:
                    score += 100
            elif count == 2:
                if blocks == 0:
                    score += 100
                elif blocks == 1:
                    score += 10
            
        return score

    def ai_move(self):
        best_score = -1
        best_move = None
        
        # Tìm tất cả các ô trống có ít nhất một quân cờ lân cận
        valid_moves = []
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if self.board[i][j] == 0:
                    # Kiểm tra xung quanh ô này
                    has_neighbor = False
                    for di in [-1, 0, 1]:
                        for dj in [-1, 0, 1]:
                            ni, nj = i + di, j + dj
                            if 0 <= ni < BOARD_SIZE and 0 <= nj < BOARD_SIZE:
                                if self.board[ni][nj] != 0:
                                    has_neighbor = True
                                    break
                        if has_neighbor:
                            break
                    if has_neighbor or len(valid_moves) == 0:
                        valid_moves.append((i, j))
        
        # Nếu bàn cờ trống, đặt ở giữa
        if len(valid_moves) == 0 or (len(valid_moves) == BOARD_SIZE * BOARD_SIZE):
            self.board[BOARD_SIZE//2][BOARD_SIZE//2] = 2
            if self.check_winner(BOARD_SIZE//2, BOARD_SIZE//2):
                self.game_over = True
                self.winner = 2
            else:
                self.current_player = 1
            return
        
        # Đánh giá từng nước đi
        for row, col in valid_moves:
            # Tính điểm tấn công (cho AI)
            attack_score = self.evaluate_position(row, col, 2)
            # Tính điểm phòng thủ (chặn người chơi)
            defense_score = self.evaluate_position(row, col, 1)
            
            # Kết hợp điểm tấn công và phòng thủ
            score = attack_score + defense_score
            
            if score > best_score:
                best_score = score
                best_move = (row, col)
        
        if best_move:
            row, col = best_move
            self.board[row][col] = 2
            if self.check_winner(row, col):
                self.game_over = True
                self.winner = 2
            else:
                self.current_player = 1
    
    def draw_board(self):
        screen.fill(WHITE)
        
        # Vẽ header
        pygame.draw.rect(screen, GRAY, (0, 0, WINDOW_SIZE, HEADER_HEIGHT))
        if self.game_over:
            if self.winner == 1:
                text = "You Win!"
                color = RED
            else:
                text = "AI Wins!"
                color = BLUE
        else:
            text = "Your Turn" if self.current_player == 1 else "AI's Turn"
            color = RED if self.current_player == 1 else BLUE
        
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(WINDOW_SIZE//2, HEADER_HEIGHT//2))
        screen.blit(text_surface, text_rect)
        
        # Vẽ lưới
        for i in range(BOARD_SIZE):
            pygame.draw.line(screen, BLACK, 
                           (i * CELL_SIZE, HEADER_HEIGHT), 
                           (i * CELL_SIZE, WINDOW_SIZE + HEADER_HEIGHT))
            pygame.draw.line(screen, BLACK, 
                           (0, i * CELL_SIZE + HEADER_HEIGHT), 
                           (WINDOW_SIZE, i * CELL_SIZE + HEADER_HEIGHT))
        
        # Vẽ X và O
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if self.board[i][j] == 1:  # X - Người chơi
                    x = j * CELL_SIZE
                    y = i * CELL_SIZE + HEADER_HEIGHT
                    pygame.draw.line(screen, RED, (x + 5, y + 5), 
                                   (x + CELL_SIZE - 5, y + CELL_SIZE - 5), 2)
                    pygame.draw.line(screen, RED, (x + CELL_SIZE - 5, y + 5), 
                                   (x + 5, y + CELL_SIZE - 5), 2)
                elif self.board[i][j] == 2:  # O - AI
                    x = j * CELL_SIZE + CELL_SIZE // 2
                    y = i * CELL_SIZE + CELL_SIZE // 2 + HEADER_HEIGHT
                    pygame.draw.circle(screen, BLUE, (x, y), CELL_SIZE // 3, 2)

def main():
    game = CaroGame()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN and not game.game_over and game.current_player == 1:
                x, y = event.pos
                if y > HEADER_HEIGHT:  # Chỉ xử lý click trong vùng bàn cờ
                    row = (y - HEADER_HEIGHT) // CELL_SIZE
                    col = x // CELL_SIZE
                    if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
                        game.make_move(row, col)
            
            # Thêm phím R để reset game
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game = CaroGame()
        
        game.draw_board()
        pygame.display.flip()

if __name__ == "__main__":
    main() 