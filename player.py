import pygame
import os

class Player:
    def __init__(self, x, y, character_data=None):
        self.x = x
        self.y = y
        self.width = 24
        self.height = 32
        self.speed = 8
        
        # 🆕 角色資料
        self.character_data = character_data
        if character_data:
            self.speed = character_data["stats"]["speed"]
            self.character_name = character_data["name"]
            print(f"🎭 創建角色: {self.character_name}")
            print(f"   屬性: HP={character_data['stats']['hp']}, 速度={self.speed}")
        else:
            self.character_name = "預設角色"
            print("🎭 創建預設角色")
        
        # 🔧 移動除錯標記
        self.debug_movement = False
        
        # 玩家動畫
        self.direction = "down"  # up, down, left, right
        self.animation_frame = 0
        self.animation_timer = 0
        self.animation_speed = 10  # 動畫速度
        
        # 移動狀態
        self.is_moving = False
        self.move_target_x = x
        self.move_target_y = y
        self.move_threshold = 3  # 🔧 增加容錯距離，避免跳動
        
        # 邊界限制
        self.min_x = 32
        self.min_y = 32
        self.max_x = 1024 - 64
        self.max_y = 768 - 64
        
        # 樓層系統
        self.current_floor = 1  # 當前樓層
        self.floor_positions = {
            1: {"x": 100, "y": 400},  # 1樓預設位置
            2: {"x": 300, "y": 150},  # 2樓預設位置
            3: {"x": 400, "y": 200},  # 3樓預設位置
            4: {"x": 500, "y": 50}    # 頂樓預設位置
        }
        
        # 無敵時間（避免重複傷害）
        self.invulnerable_time = 0
        self.max_invulnerable_time = 60  # 1秒無敵時間
        
        # 🎨 圖片資源載入
        self.sprites = {}
        self.use_sprites = True  # 是否使用圖片（如果載入失敗會自動切換為像素繪製）
        self.load_sprites()
    
    def load_sprites(self):
        """載入玩家角色圖片 - 支援多角色"""
        print(f"🎨 載入角色圖片: {self.character_name}")
        
        # 🆕 如果有角色資料，使用角色專用的圖片路徑
        if self.character_data:
            sprite_paths = self.character_data["sprite_paths"].copy()
            single_sprite_path = self.character_data["fallback_path"]
        else:
            # 備用：使用原本的路徑
            sprite_paths = {
                "down": "assets/images/player/player_down.png",
                "up": "assets/images/player/player_up.png", 
                "left": "assets/images/player/player_left.png",
                "right": "assets/images/player/player_right.png"
            }
            single_sprite_path = "assets/images/player.png"
        
        try:
            # 嘗試載入方向性圖片
            sprites_loaded = 0
            for direction, path in sprite_paths.items():
                if os.path.exists(path):
                    try:
                        sprite = pygame.image.load(path).convert_alpha()
                        # 縮放到適當大小
                        sprite = pygame.transform.scale(sprite, (self.width, self.height))
                        self.sprites[direction] = sprite
                        sprites_loaded += 1
                        print(f"  ✅ 載入 {direction} 圖片: {path}")
                    except Exception as e:
                        print(f"  ❌ 載入 {direction} 圖片失敗: {e}")
            
            # 如果沒有載入到方向性圖片，嘗試單一圖片
            if sprites_loaded == 0 and os.path.exists(single_sprite_path):
                try:
                    base_sprite = pygame.image.load(single_sprite_path).convert_alpha()
                    base_sprite = pygame.transform.scale(base_sprite, (self.width, self.height))
                    
                    # 為所有方向使用同一張圖片（可以加上翻轉效果）
                    self.sprites["down"] = base_sprite
                    self.sprites["up"] = base_sprite
                    self.sprites["right"] = base_sprite
                    self.sprites["left"] = pygame.transform.flip(base_sprite, True, False)  # 水平翻轉
                    
                    sprites_loaded = 4
                    print(f"  ✅ 載入單一圖片: {single_sprite_path}")
                except Exception as e:
                    print(f"  ❌ 載入單一圖片失敗: {e}")
            
            # 檢查載入結果
            if sprites_loaded == 0:
                print(f"  ⚠️ 未找到 {self.character_name} 圖片，使用像素繪製模式")
                self.use_sprites = False
            else:
                print(f"  🎨 成功載入 {sprites_loaded} 個 {self.character_name} 圖片")
                self.use_sprites = True
                
        except Exception as e:
            print(f"  ❌ 圖片載入系統錯誤: {e}")
            self.use_sprites = False
    
    def get_character_colors(self):
        """🆕 根據角色資料獲取專屬顏色"""
        if not self.character_data:
            # 預設角色顏色
            return {
                "body": (100, 150, 255),
                "skin": (255, 220, 177),
                "hair": (101, 67, 33)
            }
        
        # 根據角色名稱設定不同顏色
        character_colors = {
            "學生A": {
                "body": (100, 150, 255),  # 藍色
                "skin": (255, 220, 177),
                "hair": (101, 67, 33)
            },
            "學生B": {
                "body": (255, 150, 100),  # 橘色
                "skin": (255, 200, 160),
                "hair": (139, 69, 19)
            },
            "學生C": {
                "body": (150, 255, 100),  # 綠色
                "skin": (255, 235, 190),
                "hair": (160, 82, 45)
            }
        }
        
        return character_colors.get(self.character_name, character_colors["學生A"])
    
    def move(self, dx, dy):
        # 如果玩家正在移動中，忽略新的移動指令
        if self.is_moving:
            if self.debug_movement:
                print(f"⚠️ {self.character_name} 正在移動中，忽略新指令")
            return False
        
        # 計算新位置
        new_x = self.x + dx
        new_y = self.y + dy
        
        # 邊界檢查
        new_x = max(self.min_x, min(new_x, self.max_x))
        new_y = max(self.min_y, min(new_y, self.max_y))
        
        # 檢查是否真的移動了
        if new_x == self.x and new_y == self.y:
            if self.debug_movement:
                print(f"❌ {self.character_name} 邊界限制，無法移動")
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
        
        if self.debug_movement:
            print(f"🎯 {self.character_name} 開始移動: ({self.x}, {self.y}) -> ({new_x}, {new_y})")
            print(f"   移動距離: {abs(dx) + abs(dy)}, 速度: {self.speed}")
        
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
        # 平滑移動 - 修復版
        if self.is_moving:
            # 計算移動方向
            dx = self.move_target_x - self.x
            dy = self.move_target_y - self.y
            
            # 計算距離
            distance = (dx**2 + dy**2)**0.5
            
            # 🔧 修復：增加容錯距離並確保速度合理
            # 如果距離目標很近，直接到達
            if distance <= max(self.move_threshold, self.speed + 1):
                self.x = self.move_target_x
                self.y = self.move_target_y
                self.is_moving = False
                if hasattr(self, 'debug_movement') and self.debug_movement:
                    print(f"🎯 {self.character_name} 到達目標: ({self.x}, {self.y})")
            else:
                # 朝目標移動 - 確保每次移動不超過剩餘距離
                move_x = 0
                move_y = 0
                
                if dx != 0:
                    move_x = min(abs(dx), self.speed) * (1 if dx > 0 else -1)
                if dy != 0:
                    move_y = min(abs(dy), self.speed) * (1 if dy > 0 else -1)
                
                self.x += move_x
                self.y += move_y
                
                if hasattr(self, 'debug_movement') and self.debug_movement:
                    print(f"🚶 {self.character_name} 移動: ({self.x}, {self.y}) -> 目標({self.move_target_x}, {self.move_target_y}), 距離:{distance:.1f}")
        
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
        """渲染玩家 - 支援圖片和像素繪製"""
        player_x = int(self.x - self.width // 2)
        player_y = int(self.y - self.height // 2)
        
        # 🎨 優先使用圖片渲染
        if self.use_sprites and self.direction in self.sprites:
            self.render_sprite(screen, player_x, player_y)
        else:
            # 備用：像素風格繪製
            self.render_pixel_art(screen, player_x, player_y)
    
    def render_sprite(self, screen, x, y):
        """使用圖片渲染玩家"""
        sprite = self.sprites[self.direction]
        
        # 受傷閃爍效果
        if self.invulnerable_time > 0 and self.invulnerable_time % 10 < 5:
            # 創建紅色覆蓋效果
            red_sprite = sprite.copy()
            red_sprite.fill((255, 100, 100), special_flags=pygame.BLEND_MULT)
            sprite = red_sprite
        
        # 行走動畫 - 輕微上下晃動
        animation_offset_y = 0
        if self.is_moving and self.animation_frame % 2 == 1:
            animation_offset_y = -1
        
        # 繪製陰影
        shadow_rect = pygame.Rect(x + 2, y + self.height - 4, self.width - 2, 4)
        pygame.draw.ellipse(screen, (0, 0, 0, 100), shadow_rect)
        
        # 繪製角色圖片
        screen.blit(sprite, (x, y + animation_offset_y))
        
        # 無敵時間保護光環
        if self.invulnerable_time > 0:
            pygame.draw.circle(screen, (255, 255, 0, 50), 
                             (int(self.x), int(self.y)), 
                             self.width, 2)
    
    def render_pixel_art(self, screen, x, y):
        """像素風格繪製玩家（備用方法） - 🆕 支援多角色顏色"""
        # 🆕 獲取角色專屬顏色
        colors = self.get_character_colors()
        
        # 身體顏色（受傷時閃爍紅色）
        if self.invulnerable_time > 0 and self.invulnerable_time % 10 < 5:
            body_color = (255, 100, 100)  # 受傷閃爍紅色
            skin_color = (255, 200, 150)
        else:
            body_color = colors["body"]    # 使用角色專屬顏色
            skin_color = colors["skin"]    # 使用角色專屬膚色
        
        hair_color = colors["hair"]        # 使用角色專屬髮色
        
        # 繪製陰影
        shadow_rect = pygame.Rect(x + 2, y + self.height - 4, self.width - 2, 4)
        pygame.draw.ellipse(screen, (0, 0, 0, 100), shadow_rect)
        
        # 根據方向和動畫幀繪製玩家
        if self.direction == "down":
            self.draw_player_front(screen, x, y, body_color, skin_color, hair_color)
        elif self.direction == "up":
            self.draw_player_back(screen, x, y, body_color, skin_color, hair_color)
        elif self.direction == "left":
            self.draw_player_side(screen, x, y, body_color, skin_color, hair_color, True)
        elif self.direction == "right":
            self.draw_player_side(screen, x, y, body_color, skin_color, hair_color, False)
        
        # 繪製行走動畫效果
        if self.is_moving and self.animation_frame % 2 == 1:
            # 輕微的上下晃動已在調用方處理
            pass
        
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
            "current_floor": self.current_floor,
            "character": self.character_name
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
    
    def get_character_name(self):
        """🆕 獲取角色名稱"""
        return self.character_name
    
    def get_character_stats(self):
        """🆕 獲取角色屬性"""
        if self.character_data:
            return self.character_data["stats"].copy()
        return {"hp": 100, "speed": 8}
    
    def is_at_position(self, x, y, tolerance=10):
        """檢查玩家是否在指定位置附近"""
        distance = ((self.x - x)**2 + (self.y - y)**2)**0.5
        return distance <= tolerance
    
    def reload_sprites(self):
        """重新載入圖片（用於熱更新）"""
        print(f"🔄 重新載入 {self.character_name} 圖片...")
        self.sprites.clear()
        self.load_sprites()
    
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
        print(f"{self.character_name} 狀態已重置")