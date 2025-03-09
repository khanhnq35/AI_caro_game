import pygame
from ai_player import AI

# Kích thước ô cờ
CELL_SIZE = 40  
BOARD_SIZE = 15 

# Màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
BLUE = (0, 0, 200)

# Khởi tạo Pygame
pygame.init()
screen = pygame.display.set_mode((BOARD_SIZE * CELL_SIZE, BOARD_SIZE * CELL_SIZE))
pygame.display.set_caption("Cờ Caro 15x15 - Người vs AI")

# Khởi tạo AI
ai = AI(BOARD_SIZE)

# Bàn cờ lưu trạng thái (0: trống, 1: X, 2: O)
board = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)] 
turn = 1  # Người chơi luôn đi trước với X (1), AI sẽ là O (2)

# Vẽ bàn cờ
def draw_board():
    screen.fill(WHITE)
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            x, y = i * CELL_SIZE, j * CELL_SIZE
            pygame.draw.rect(screen, BLACK, (x, y, CELL_SIZE, CELL_SIZE), 1)

# Vẽ quân cờ (X,O) tại hàng row, cột col
def draw_piece(row, col):
    x, y = col * CELL_SIZE, row * CELL_SIZE
    if board[row][col] == 1:
        pygame.draw.line(screen, RED, (x+5, y+5), (x+CELL_SIZE-5, y+CELL_SIZE-5), 2)
        pygame.draw.line(screen, RED, (x+CELL_SIZE-5, y+5), (x+5, y+CELL_SIZE-5), 2)
    elif board[row][col] == 2:
        pygame.draw.circle(screen, BLUE, (x+CELL_SIZE//2, y+CELL_SIZE//2), CELL_SIZE//3, 2)
    pygame.display.update((x, y, CELL_SIZE, CELL_SIZE))  # Cập nhật chỉ vùng vừa vẽ

def check_winner(row, col):
    directions = [
        (1, 0),  # Hàng ngang
        (0, 1),  # Hàng dọc
        (1, 1),  # Đường chéo chính
        (1, -1)  # Đường chéo phụ
    ]
    for dr, dc in directions:
        count = 1
        for delta in [-1, 1]:
            r, c = row + delta * dr, col + delta * dc
            while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and board[r][c] == board[row][col]:
                count += 1
                r += delta * dr
                c += delta * dc
        if count >= 5:
            return True
    return False

# Hiển thị thông báo kết quả
def show_message(text):
    font = pygame.font.Font(None, 50)
    text_surface = font.render(text, True, (0, 0, 0))
    text_rect = text_surface.get_rect(center=(BOARD_SIZE * CELL_SIZE // 2, BOARD_SIZE * CELL_SIZE // 2))
    screen.blit(text_surface, text_rect)
    pygame.display.update()

# Kiểm tra sự kiện chuột
running = True
game_over = False
draw_board()
pygame.display.flip()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and not game_over and turn == 1:  # Chỉ cho phép người chơi đánh khi đến lượt
            mx, my = pygame.mouse.get_pos()
            row, col = my // CELL_SIZE, mx // CELL_SIZE
            if board[row][col] == 0:
                print(f"Người chơi đánh tại vị trí: ({row}, {col})")
                board[row][col] = turn
                draw_piece(row, col)
                if check_winner(row, col):
                    show_message("Ban da thang!")
                    game_over = True
                elif all(board[i][j] != 0 for i in range(BOARD_SIZE) for j in range(BOARD_SIZE)):
                    show_message("Hoa!")
                    game_over = True
                else:
                    turn = 2  # Chuyển lượt cho AI
                    print("Đến lượt AI...")
                    
                    # AI đánh
                    ai_row, ai_col = ai.get_best_move(board)
                    print(f"AI đánh tại vị trí: ({ai_row}, {ai_col})")
                    if ai_row is not None and ai_col is not None:
                        board[ai_row][ai_col] = 2
                        draw_piece(ai_row, ai_col)
                        if check_winner(ai_row, ai_col):
                            show_message("AI thang!")
                            game_over = True
                        elif all(board[i][j] != 0 for i in range(BOARD_SIZE) for j in range(BOARD_SIZE)):
                            show_message("Hoa!")
                            game_over = True
                        else:
                            turn = 1  # Chuyển lượt lại cho người chơi
                    else:
                        print("Lỗi: AI không thể tìm được nước đi!")
                        turn = 1
        
        # Nếu game over, chờ người chơi nhấn nút để thoát
        elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
            if game_over:
                running = False

pygame.quit()
