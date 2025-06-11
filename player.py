import pygame

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 24
        self.height = 32
        self.speed = 8
        
        # 玩家動畫
        self.direction = "down"  # up, down, left, right
        self.animation_frame = 0
        self.animation_timer = 0
        self.animation_speed = 10  # 動畫速度
        
        # 移動狀態
        self.is_moving = False
        self.move_target_x = x
        self.move_target_y = y
        self.move_threshold = 2  # 到達目標的容錯距離
        
        # 邊界限制
        self.min_x = 32
        self.min_y = 32
        self.max_x = 1024 - 64
        self.max_y = 768 - 64
        
        # 新增：樓層系統
        self.current_floor = 1  # 當前樓層
        self.floor_positions = {
            1: {"x": 100, "y": 400},  # 1樓預設位置
            2: {"x": 300, "y": 150},  # 2樓預設位置
            3: {"x": 400, "y": 200},  # 3樓預設位置
            4: {"x": 500, "y": 50}    # 頂樓預設位置
        }
        
        # 新增：無敵時間（避免重複傷害）
        self.invulnerable_time = 0
        self.max_invulnerable_time = 60  # 1秒無敵時間
    
    def move(self, dx, dy):
        # 如果玩家正在移動中，忽略新的移動指令
        if self.is_moving:
            return False
        
        # 計算新位置
        new_x = self.x + dx
        new_y = self.y + dy
        
        # 邊界檢查
        new_x = max(self.min_x, min(new_x, self.max_x))
        new_y = max(self.min_y, min(new_y, self.max_y))
        
        # 檢查是否真的移動了
        if new_x == self.x and new_y == self.y:
            return False
        
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
        
        return True
    
    def set_position(self, x, y):
        """設置玩家位置（用於傳送）"""
        self.x = x
        self.y = y
        self.move_target_x = x
        self.move_target_y = y
        self.is_moving = False
        print(f"玩家傳送到: ({x}, {y})")
    
    def teleport_to_floor(self, floor):
        """傳送到指定樓層"""
        if floor in self.floor_positions:
            self.current_floor = floor
            pos = self.floor_positions[floor]
            self.set_position(pos["x"], pos["y"])
            print(f"玩家傳送到 {floor} 樓")
            return True
        return False
    
    def teleport_to_coordinates(self, x, y, floor=None):
        """傳送到指定座標"""
        # 邊界檢查
        x = max(self.min_x, min(x, self.max_x))
        y = max(self.min_y, min(y, self.max_y))
        
        self.set_position(x, y)
        
        if floor is not None:
            self.current_floor = floor
            print(f"玩家傳送到 {floor} 樓 ({x}, {y})")
        else:
            print(f"玩家傳送到 ({x}, {y})")
        
        return True
    
    def take_damage(self, amount):
        """受到傷害（有無敵時間保護）"""
        if self.invulnerable_time <= 0:
            self.invulnerable_time = self.max_invulnerable_time
            print(f"玩家受到 {amount} 點傷害！")
            return True
        return False
    
    def update(self):
        # 平滑移動
        if self.is_moving:
            # 計算移動方向
            dx = self.move_target_x - self.x
            dy = self.move_target_y - self.y
            
            # 計算距離
            distance = (dx**2 + dy**2)**0.5
            
            # 如果距離目標很近，直接到達
            if distance <= self.move_threshold:
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
        
        # 更新無敵時間
        if self.invulnerable_time > 0:
            self.invulnerable_time -= 1
    
    def render(self, screen):
        # 玩家像素風格繪製
        player_x = int(self.x - self.width // 2)
        player_y = int(self.y - self.height // 2)
        
        # 身體顏色（受傷時閃爍紅色）
        if self.invulnerable_time > 0 and self.invulnerable_time % 10 < 5:
            body_color = (255, 100, 100)  # 受傷閃爍紅色
            skin_color = (255, 200, 150)
        else:
            body_color = (100, 150, 255)  # 正常藍色衣服
            skin_color = (255, 220, 177)  # 正常膚色
        
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
        
        # 如果在無敵時間，繪製保護光環
        if self.invulnerable_time > 0:
            pygame.draw.circle(screen, (255, 255, 0, 50), 
                             (int(self.x), int(self.y)), 
                             self.width, 2)
    
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
    
    def force_stop_movement(self):
        """強制停止移動"""
        self.is_moving = False
        self.move_target_x = self.x
        self.move_target_y = self.y
    
    def get_movement_info(self):
        """獲取移動狀態資訊"""
        return {
            "position": (self.x, self.y),
            "target": (self.move_target_x, self.move_target_y),
            "is_moving": self.is_moving,
            "direction": self.direction,
            "distance_to_target": ((self.move_target_x - self.x)**2 + (self.move_target_y - self.y)**2)**0.5,
            "current_floor": self.current_floor
        }
    
    def get_rect(self):
        """獲取玩家碰撞矩形"""
        return pygame.Rect(self.x - self.width//2, self.y - self.height//2, 
                          self.width, self.height)
    
    def get_position(self):
        """獲取玩家當前位置"""
        return (self.x, self.y)
    
    def get_floor(self):
        """獲取當前樓層"""
        return self.current_floor
    
    def is_at_position(self, x, y, tolerance=10):
        """檢查玩家是否在指定位置附近"""
        distance = ((self.x - x)**2 + (self.y - y)**2)**0.5
        return distance <= tolerance
    
    def reset(self):
        """重置玩家狀態（用於遊戲重新開始）"""
        self.x = 100
        self.y = 400
        self.move_target_x = self.x
        self.move_target_y = self.y
        self.is_moving = False
        self.current_floor = 1
        self.direction = "down"
        self.animation_frame = 0
        self.animation_timer = 0
        self.invulnerable_time = 0
        print("玩家狀態已重置")