import pygame

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 24
        self.height = 32
        self.speed = 4
        
        # 玩家動畫
        self.direction = "down"  # up, down, left, right
        self.animation_frame = 0
        self.animation_timer = 0
        self.animation_speed = 10  # 動畫速度
        
        # 移動狀態
        self.is_moving = False
        self.move_target_x = x
        self.move_target_y = y
        
        # 邊界限制
        self.min_x = 32
        self.min_y = 32
        self.max_x = 1024 - 64
        self.max_y = 768 - 64
    
    def move(self, dx, dy):
        # 計算新位置
        new_x = self.x + dx
        new_y = self.y + dy
        
        # 邊界檢查
        new_x = max(self.min_x, min(new_x, self.max_x))
        new_y = max(self.min_y, min(new_y, self.max_y))
        
        # 設定移動目標
        self.move_target_x = new_x
        self.move_target_y = new_y
        self.is_moving = True
        
        # 設定朝向
        if dx > 0:
            self.direction = "right"
        elif dx < 0:
            self.direction = "left"
        elif dy > 0:
            self.direction = "down"
        elif dy < 0:
            self.direction = "up"
    
    def set_position(self, x, y):
        self.x = x
        self.y = y
        self.move_target_x = x
        self.move_target_y = y
        self.is_moving = False
    
    def update(self):
        # 平滑移動
        if self.is_moving:
            # 計算移動方向
            dx = self.move_target_x - self.x
            dy = self.move_target_y - self.y
            
            # 如果距離目標很近，直接到達
            if abs(dx) < self.speed and abs(dy) < self.speed:
                self.x = self.move_target_x
                self.y = self.move_target_y
                self.is_moving = False
            else:
                # 朝目標移動
                if dx != 0:
                    self.x += self.speed if dx > 0 else -self.speed
                if dy != 0:
                    self.y += self.speed if dy > 0 else -self.speed
        
        # 更新動畫
        if self.is_moving:
            self.animation_timer += 1
            if self.animation_timer >= self.animation_speed:
                self.animation_timer = 0
                self.animation_frame = (self.animation_frame + 1) % 4
        else:
            self.animation_frame = 0
    
    def render(self, screen):
        # 玩家像素風格繪製
        player_x = int(self.x - self.width // 2)
        player_y = int(self.y - self.height // 2)
        
        # 身體顏色
        body_color = (100, 150, 255)  # 藍色衣服
        skin_color = (255, 220, 177)  # 膚色
        hair_color = (101, 67, 33)    # 頭髮
        
        # 繪製陰影
        shadow_rect = pygame.Rect(player_x + 2, player_y + self.height - 4, self.width - 2, 4)
        pygame.draw.ellipse(screen, (0, 0, 0, 100), shadow_rect)
        
        # 根據方向和動畫幀繪製玩家
        if self.direction == "down":
            self.draw_player_front(screen, player_x, player_y, body_color, skin_color, hair_color)
        elif self.direction == "up":
            self.draw_player_back(screen, player_x, player_y, body_color, skin_color, hair_color)
        elif self.direction == "left":
            self.draw_player_side(screen, player_x, player_y, body_color, skin_color, hair_color, True)
        elif self.direction == "right":
            self.draw_player_side(screen, player_x, player_y, body_color, skin_color, hair_color, False)
        
        # 繪製行走動畫效果
        if self.is_moving and self.animation_frame % 2 == 1:
            # 輕微的上下晃動
            player_y -= 1
    
    def draw_player_front(self, screen, x, y, body_color, skin_color, hair_color):
        # 頭部
        pygame.draw.rect(screen, skin_color, (x + 6, y + 2, 12, 12))
        # 頭髮
        pygame.draw.rect(screen, hair_color, (x + 4, y, 16, 6))
        # 眼睛
        pygame.draw.rect(screen, (0, 0, 0), (x + 8, y + 6, 2, 2))
        pygame.draw.rect(screen, (0, 0, 0), (x + 14, y + 6, 2, 2))
        # 嘴巴
        pygame.draw.rect(screen, (0, 0, 0), (x + 11, y + 10, 2, 1))
        
        # 身體
        pygame.draw.rect(screen, body_color, (x + 4, y + 14, 16, 12))
        
        # 手臂
        pygame.draw.rect(screen, skin_color, (x + 2, y + 16, 4, 8))
        pygame.draw.rect(screen, skin_color, (x + 18, y + 16, 4, 8))
        
        # 腿部
        pygame.draw.rect(screen, (50, 50, 150), (x + 6, y + 26, 5, 6))
        pygame.draw.rect(screen, (50, 50, 150), (x + 13, y + 26, 5, 6))
    
    def draw_player_back(self, screen, x, y, body_color, skin_color, hair_color):
        # 頭部
        pygame.draw.rect(screen, skin_color, (x + 6, y + 2, 12, 12))
        # 頭髮
        pygame.draw.rect(screen, hair_color, (x + 4, y, 16, 8))
        
        # 身體
        pygame.draw.rect(screen, body_color, (x + 4, y + 14, 16, 12))
        
        # 手臂
        pygame.draw.rect(screen, skin_color, (x + 2, y + 16, 4, 8))
        pygame.draw.rect(screen, skin_color, (x + 18, y + 16, 4, 8))
        
        # 腿部
        pygame.draw.rect(screen, (50, 50, 150), (x + 6, y + 26, 5, 6))
        pygame.draw.rect(screen, (50, 50, 150), (x + 13, y + 26, 5, 6))
    
    def draw_player_side(self, screen, x, y, body_color, skin_color, hair_color, facing_left):
        if facing_left:
            # 面向左側
            # 頭部
            pygame.draw.rect(screen, skin_color, (x + 6, y + 2, 12, 12))
            # 頭髮
            pygame.draw.rect(screen, hair_color, (x + 4, y, 14, 6))
            # 眼睛
            pygame.draw.rect(screen, (0, 0, 0), (x + 8, y + 6, 2, 2))
            
            # 身體
            pygame.draw.rect(screen, body_color, (x + 4, y + 14, 16, 12))
            
            # 手臂（一隻可見）
            pygame.draw.rect(screen, skin_color, (x + 2, y + 16, 4, 8))
            
            # 腿部
            leg_offset = 2 if self.animation_frame % 2 else 0
            pygame.draw.rect(screen, (50, 50, 150), (x + 6, y + 26 + leg_offset, 5, 6))
            pygame.draw.rect(screen, (50, 50, 150), (x + 13, y + 26 - leg_offset, 5, 6))
        else:
            # 面向右側
            # 頭部
            pygame.draw.rect(screen, skin_color, (x + 6, y + 2, 12, 12))
            # 頭髮
            pygame.draw.rect(screen, hair_color, (x + 6, y, 14, 6))
            # 眼睛
            pygame.draw.rect(screen, (0, 0, 0), (x + 14, y + 6, 2, 2))
            
            # 身體
            pygame.draw.rect(screen, body_color, (x + 4, y + 14, 16, 12))
            
            # 手臂（一隻可見）
            pygame.draw.rect(screen, skin_color, (x + 18, y + 16, 4, 8))
            
            # 腿部
            leg_offset = 2 if self.animation_frame % 2 else 0
            pygame.draw.rect(screen, (50, 50, 150), (x + 6, y + 26 - leg_offset, 5, 6))
            pygame.draw.rect(screen, (50, 50, 150), (x + 13, y + 26 + leg_offset, 5, 6))
    
    def get_rect(self):
        return pygame.Rect(self.x - self.width//2, self.y - self.height//2, 
                          self.width, self.height)