import numpy as np

class AI:
    def __init__(self, board_size=15):
        self.board_size = board_size
        self.max_depth = 2  # Giảm độ sâu để tăng tốc độ
        self.directions = [(0, 1), (1, 0), (1, 1), (1, -1)]  # Các hướng để kiểm tra

    def evaluate_window(self, window, piece):
        """Đánh giá một cửa sổ gồm 5 ô"""
        score = 0
        opp_piece = 1 if piece == 2 else 2

        # Điểm cho các trường hợp tấn công
        if window.count(piece) == 5:
            score += 1000000
        elif window.count(piece) == 4 and window.count(0) == 1:
            score += 10000
        elif window.count(piece) == 3 and window.count(0) == 2:
            score += 1000
        elif window.count(piece) == 2 and window.count(0) == 3:
            score += 100

        # Điểm cho các trường hợp phòng thủ
        if window.count(opp_piece) == 4 and window.count(0) == 1:
            score -= 9000
        elif window.count(opp_piece) == 3 and window.count(0) == 2:
            score -= 900
        elif window.count(opp_piece) == 2 and window.count(0) == 3:
            score -= 90

        return score

    def get_windows(self, board, row, col):
        """Lấy tất cả các cửa sổ 5 ô có chứa vị trí (row, col)"""
        windows = []
        for dr, dc in self.directions:
            # Kiểm tra các cửa sổ có thể có chứa vị trí hiện tại
            for start in range(-4, 1):
                window = []
                valid = True
                for i in range(5):
                    r, c = row + (start + i) * dr, col + (start + i) * dc
                    if 0 <= r < self.board_size and 0 <= c < self.board_size:
                        window.append(board[r][c])
                    else:
                        valid = False
                        break
                if valid and len(window) == 5:
                    windows.append(window)
        return windows

    def score_position(self, board, piece):
        """Đánh giá toàn bộ bàn cờ"""
        score = 0
        # Chỉ đánh giá các vị trí có quân cờ và vùng xung quanh
        for r in range(self.board_size):
            for c in range(self.board_size):
                if board[r][c] != 0:
                    windows = self.get_windows(board, r, c)
                    for window in windows:
                        score += self.evaluate_window(window, piece)
        return score

    def get_valid_moves(self, board):
        """Lấy danh sách các nước đi hợp lệ trong phạm vi 2 ô xung quanh các quân đã đánh"""
        valid_moves = set()  # Sử dụng set để tránh trùng lặp
        has_pieces = False
        
        # Tìm các ô đã được đánh
        for r in range(self.board_size):
            for c in range(self.board_size):
                if board[r][c] != 0:
                    has_pieces = True
                    # Kiểm tra các ô xung quanh trong phạm vi 2 ô
                    for dr in range(-2, 3):
                        for dc in range(-2, 3):
                            new_r, new_c = r + dr, c + dc
                            if (0 <= new_r < self.board_size and 
                                0 <= new_c < self.board_size and 
                                board[new_r][new_c] == 0):
                                valid_moves.add((new_r, new_c))
        
        # Nếu bàn cờ trống, đánh vào giữa
        if not has_pieces:
            center = self.board_size // 2
            valid_moves.add((center, center))
            
        return list(valid_moves)

    def minimax(self, board, depth, alpha, beta, maximizing_player):
        """Thuật toán minimax với alpha-beta pruning"""
        valid_moves = self.get_valid_moves(board)
        
        if depth == 0 or len(valid_moves) == 0:
            return None, self.score_position(board, 2)

        if maximizing_player:
            value = float('-inf')
            column = valid_moves[0] if valid_moves else None
            for move in valid_moves:
                board_copy = [row[:] for row in board]
                board_copy[move[0]][move[1]] = 2
                new_score = self.minimax(board_copy, depth-1, alpha, beta, False)[1]
                if new_score > value:
                    value = new_score
                    column = move
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return column, value
        else:
            value = float('inf')
            column = valid_moves[0] if valid_moves else None
            for move in valid_moves:
                board_copy = [row[:] for row in board]
                board_copy[move[0]][move[1]] = 1
                new_score = self.minimax(board_copy, depth-1, alpha, beta, True)[1]
                if new_score < value:
                    value = new_score
                    column = move
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return column, value

    def get_best_move(self, board):
        """Lấy nước đi tốt nhất cho AI"""
        print("AI đang tính toán nước đi...")
        move, score = self.minimax(board, self.max_depth, float('-inf'), float('inf'), True)
        print(f"AI đã chọn nước đi với điểm số: {score}")
        return move 