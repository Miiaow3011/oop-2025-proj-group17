# character_selector.py - 角色選擇系統
import pygame
import os
from font_manager import font_manager

class CharacterSelector:
    def __init__(self, screen):
        self.screen = screen
        self.screen_width, self.screen_height = screen.get_size()
        
        # 角色選擇狀態
        self.active = True
        self.selected_character = 0  # 當前選中的角色 (0, 1, 2)
        self.character_selected = False  # 是否已經選擇完成
        
        # 角色資料
        self.characters = [
            {
                "name": "學生A",
                "description": "普通的交大學生，\n有著堅強的意志力",
                "sprite_paths": {
                    "down": "assets/images/player/student_a_down.png",
                    "up": "assets/images/player/student_a_up.png",
                    "left": "assets/images/player/student_a_left.png",
                    "right": "assets/images/player/student_a_right.png"
                },
                "fallback_path": "assets/images/player/student_a.png",
                "stats": {"hp": 100, "speed": 8}
            },
            {
                "name": "學生B", 
                "description": "運動系的學生，\n體力充沛，行動敏捷",
                "sprite_paths": {
                    "down": "assets/images/player/student_b_down.png",
                    "up": "assets/images/player/student_b_up.png", 
                    "left": "assets/images/player/student_b_left.png",
                    "right": "assets/images/player/student_b_right.png"
                },
                "fallback_path": "assets/images/player/student_b.png",
                "stats": {"hp": 120, "speed": 10}
            },
            {
                "name": "學生C",
                "description": "理工科系學生，\n聰明機智，善於分析",
                "sprite_paths": {
                    "down": "assets/images/player/student_c_down.png",
                    "up": "assets/images/player/student_c_up.png",
                    "left": "assets/images/player/student_c_left.png", 
                    "right": "assets/images/player/student_c_right.png"
                },
                "fallback_path": "assets/images/player/student_c.png",
                "stats": {"hp": 90, "speed": 8}  # 🔧 修復：改為8避免移動問題
            }
        ]
        
        # 載入角色預覽圖片
        self.character_sprites = {}
        self.load_character_previews()
        
        # UI設定
        self.card_width = 200
        self.card_height = 280
        self.card_spacing = 50
        self.total_cards_width = len(self.characters) * self.card_width + (len(self.characters) - 1) * self.card_spacing
        self.cards_start_x = (self.screen_width - self.total_cards_width) // 2
        self.cards_y = 200
        
        # 動畫效果
        self.hover_scale = {}
        for i in range(len(self.characters)):
            self.hover_scale[i] = 1.0
        
        self.animation_timer = 0
        
        print("🎭 角色選擇器初始化完成")
    
    def load_character_previews(self):
        """載入角色預覽圖片"""
        print("🎨 載入角色預覽圖片...")
        
        for i, character in enumerate(self.characters):
            character_sprites = {}
            sprites_loaded = 0
            
            # 嘗試載入方向性圖片
            for direction, path in character["sprite_paths"].items():
                if os.path.exists(path):
                    try:
                        sprite = pygame.image.load(path).convert_alpha()
                        # 縮放到預覽大小 (較大一點以便顯示)
                        preview_size = (64, 80)
                        sprite = pygame.transform.scale(sprite, preview_size)
                        character_sprites[direction] = sprite
                        sprites_loaded += 1
                        print(f"  ✅ 載入角色{i+1} {direction}圖片: {path}")
                    except Exception as e:
                        print(f"  ❌ 載入角色{i+1} {direction}圖片失敗: {e}")
            
            # 如果沒有方向性圖片，嘗試載入備用圖片
            if sprites_loaded == 0:
                fallback_path = character["fallback_path"]
                if os.path.exists(fallback_path):
                    try:
                        base_sprite = pygame.image.load(fallback_path).convert_alpha()
                        preview_size = (64, 80)
                        base_sprite = pygame.transform.scale(base_sprite, preview_size)
                        
                        # 為所有方向使用同一張圖片
                        character_sprites["down"] = base_sprite
                        character_sprites["up"] = base_sprite
                        character_sprites["right"] = base_sprite
                        character_sprites["left"] = pygame.transform.flip(base_sprite, True, False)
                        sprites_loaded = 4
                        print(f"  ✅ 載入角色{i+1}備用圖片: {fallback_path}")
                    except Exception as e:
                        print(f"  ❌ 載入角色{i+1}備用圖片失敗: {e}")
            
            # 如果還是沒有圖片，創建預設圖片
            if sprites_loaded == 0:
                print(f"  ⚠️ 角色{i+1}沒有找到圖片，將使用預設外觀")
                character_sprites = self.create_default_character_sprite(i)
            
            self.character_sprites[i] = character_sprites
            print(f"  📋 角色{i+1} ({character['name']}) 載入完成")
    
    def create_default_character_sprite(self, character_index):
        """創建預設角色圖片"""
        sprites = {}
        size = (64, 80)
        
        # 不同角色使用不同顏色
        colors = [
            (100, 150, 255),  # 藍色
            (255, 150, 100),  # 橘色  
            (150, 255, 100)   # 綠色
        ]
        
        character_color = colors[character_index % len(colors)]
        
        for direction in ["down", "up", "left", "right"]:
            surface = pygame.Surface(size, pygame.SRCALPHA)
            surface.fill((0, 0, 0, 0))  # 透明背景
            
            # 繪製簡單的角色形狀
            # 頭部
            pygame.draw.circle(surface, (255, 220, 177), (32, 20), 15)
            # 身體
            pygame.draw.rect(surface, character_color, (20, 35, 24, 30))
            # 腿
            pygame.draw.rect(surface, (50, 50, 150), (22, 65, 8, 12))
            pygame.draw.rect(surface, (50, 50, 150), (32, 65, 8, 12))
            
            sprites[direction] = surface
        
        return sprites
    
    def handle_event(self, event):
        """處理角色選擇事件"""
        if not self.active:
            return False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.selected_character = (self.selected_character - 1) % len(self.characters)
                print(f"🎯 選擇角色: {self.characters[self.selected_character]['name']}")
                return True
            elif event.key == pygame.K_RIGHT:
                self.selected_character = (self.selected_character + 1) % len(self.characters)
                print(f"🎯 選擇角色: {self.characters[self.selected_character]['name']}")
                return True
            elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                self.confirm_selection()
                return True
            elif event.key == pygame.K_ESCAPE:
                # ESC鍵預設選擇第一個角色
                self.selected_character = 0
                self.confirm_selection()
                return True
        
        # 滑鼠點擊檢測
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # 左鍵
                mouse_x, mouse_y = event.pos
                clicked_character = self.get_character_at_mouse(mouse_x, mouse_y)
                if clicked_character is not None:
                    self.selected_character = clicked_character
                    self.confirm_selection()
                    return True
        
        # 滑鼠移動檢測（用於hover效果）
        elif event.type == pygame.MOUSEMOTION:
            mouse_x, mouse_y = event.pos
            hovered_character = self.get_character_at_mouse(mouse_x, mouse_y)
            if hovered_character is not None:
                self.selected_character = hovered_character
        
        return False
    
    def get_character_at_mouse(self, mouse_x, mouse_y):
        """檢測滑鼠位置對應的角色"""
        for i in range(len(self.characters)):
            card_x = self.cards_start_x + i * (self.card_width + self.card_spacing)
            card_rect = pygame.Rect(card_x, self.cards_y, self.card_width, self.card_height)
            if card_rect.collidepoint(mouse_x, mouse_y):
                return i
        return None
    
    def confirm_selection(self):
        """確認選擇"""
        selected = self.characters[self.selected_character]
        print(f"✅ 確認選擇角色: {selected['name']}")
        print(f"   屬性: HP={selected['stats']['hp']}, 速度={selected['stats']['speed']}")
        self.character_selected = True
        self.active = False
    
    def get_selected_character(self):
        """獲取選中的角色資料"""
        if self.character_selected:
            return self.characters[self.selected_character]
        return None
    
    def update(self):
        """更新動畫效果"""
        if not self.active:
            return
        
        self.animation_timer += 1
        
        # 更新hover縮放效果
        for i in range(len(self.characters)):
            target_scale = 1.1 if i == self.selected_character else 1.0
            current_scale = self.hover_scale[i]
            
            # 平滑縮放動畫
            scale_diff = target_scale - current_scale
            self.hover_scale[i] += scale_diff * 0.1
    
    def render(self):
        """渲染角色選擇畫面"""
        if not self.active:
            return
        
        # 清除背景
        background_color = (20, 30, 50)
        self.screen.fill(background_color)
        
        # 標題
        title_text = "選擇你的角色"
        title_surface = font_manager.render_text(title_text, 36, (255, 255, 255))
        title_rect = title_surface.get_rect(center=(self.screen_width//2, 80))
        self.screen.blit(title_surface, title_rect)
        
        # 副標題
        subtitle_text = "每個角色都有不同的特色和能力"
        subtitle_surface = font_manager.render_text(subtitle_text, 20, (200, 200, 200))
        subtitle_rect = subtitle_surface.get_rect(center=(self.screen_width//2, 120))
        self.screen.blit(subtitle_surface, subtitle_rect)
        
        # 渲染角色卡片
        for i, character in enumerate(self.characters):
            self.render_character_card(i, character)
        
        # 操作提示
        controls = [
            "← → 選擇角色",
            "空白鍵/Enter 確認",
            "ESC 使用預設角色"
        ]
        
        hint_y = self.screen_height - 100
        for j, control in enumerate(controls):
            control_surface = font_manager.render_text(control, 18, (150, 150, 150))
            control_rect = control_surface.get_rect(center=(self.screen_width//2, hint_y + j * 25))
            self.screen.blit(control_surface, control_rect)
    
    def render_character_card(self, index, character):
        """渲染單個角色卡片"""
        # 計算卡片位置
        card_x = self.cards_start_x + index * (self.card_width + self.card_spacing)
        card_y = self.cards_y
        
        # 縮放效果
        scale = self.hover_scale[index]
        scaled_width = int(self.card_width * scale)
        scaled_height = int(self.card_height * scale)
        scaled_x = card_x + (self.card_width - scaled_width) // 2
        scaled_y = card_y + (self.card_height - scaled_height) // 2
        
        # 卡片背景
        is_selected = (index == self.selected_character)
        
        if is_selected:
            # 選中狀態：發光邊框
            glow_size = 8
            glow_rect = pygame.Rect(scaled_x - glow_size, scaled_y - glow_size, 
                                  scaled_width + glow_size*2, scaled_height + glow_size*2)
            
            # 發光動畫
            glow_alpha = int(150 + 50 * abs((self.animation_timer % 60 - 30) / 30))
            glow_surface = pygame.Surface((glow_rect.width, glow_rect.height), pygame.SRCALPHA)
            pygame.draw.rect(glow_surface, (255, 255, 0, glow_alpha), glow_surface.get_rect(), border_radius=15)
            self.screen.blit(glow_surface, glow_rect)
            
            # 卡片背景
            card_color = (80, 120, 160)
            border_color = (255, 255, 0)
        else:
            card_color = (60, 60, 80)
            border_color = (100, 100, 100)
        
        card_rect = pygame.Rect(scaled_x, scaled_y, scaled_width, scaled_height)
        pygame.draw.rect(self.screen, card_color, card_rect, border_radius=10)
        pygame.draw.rect(self.screen, border_color, card_rect, width=2, border_radius=10)
        
        # 角色圖片
        if index in self.character_sprites:
            sprite = self.character_sprites[index].get("down")
            if sprite:
                # 計算圖片位置（置中在卡片上方）
                sprite_x = scaled_x + (scaled_width - sprite.get_width()) // 2
                sprite_y = scaled_y + 20
                
                # 繪製圖片陰影
                shadow_surface = pygame.Surface(sprite.get_size(), pygame.SRCALPHA)
                shadow_surface.fill((0, 0, 0, 100))
                self.screen.blit(shadow_surface, (sprite_x + 2, sprite_y + 2))
                
                # 繪製角色圖片
                self.screen.blit(sprite, (sprite_x, sprite_y))
        
        # 角色名稱
        name_surface = font_manager.render_text(character["name"], 24, (255, 255, 255))
        name_rect = name_surface.get_rect(center=(scaled_x + scaled_width//2, scaled_y + 130))
        self.screen.blit(name_surface, name_rect)
        
        # 角色描述
        desc_lines = character["description"].split("\n")
        desc_y = scaled_y + 160
        for line in desc_lines:
            line_surface = font_manager.render_text(line, 16, (200, 200, 200))
            line_rect = line_surface.get_rect(center=(scaled_x + scaled_width//2, desc_y))
            self.screen.blit(line_surface, line_rect)
            desc_y += 20
        
        # 角色屬性
        stats = character["stats"]
        stats_text = f"HP: {stats['hp']} | 速度: {stats['speed']}"
        stats_surface = font_manager.render_text(stats_text, 14, (150, 255, 150))
        stats_rect = stats_surface.get_rect(center=(scaled_x + scaled_width//2, scaled_y + scaled_height - 30))
        self.screen.blit(stats_surface, stats_rect)
        
        # 選擇指示器
        if is_selected:
            indicator_text = "按空白鍵確認"
            indicator_surface = font_manager.render_text(indicator_text, 16, (255, 255, 0))
            indicator_rect = indicator_surface.get_rect(center=(scaled_x + scaled_width//2, scaled_y + scaled_height + 20))
            self.screen.blit(indicator_surface, indicator_rect)
    
    def is_selection_complete(self):
        """檢查是否完成選擇"""
        return self.character_selected
    
    def reset(self):
        """重置選擇器"""
        self.active = True
        self.selected_character = 0
        self.character_selected = False
        self.animation_timer = 0
        for i in range(len(self.characters)):
            self.hover_scale[i] = 1.0
        print("🔄 角色選擇器已重置")