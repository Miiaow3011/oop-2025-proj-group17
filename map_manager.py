import pygame
import os
from font_manager import font_manager

class MapManager:
    def __init__(self):
        self.current_floor = 1
        self.tile_size = 32
        
        # 地圖數據 - 使用字典存儲每層的商店和NPC位置
        self.floor_data = {
            1: {  # 一樓
                "shops": {
                    "A": {"name": "7-11", "pos": (64, 96), "size": (128, 96), "chinese_name": "7-11"},
                    "B": {"name": "Subway", "pos": (320, 64), "size": (160, 64), "chinese_name": "Subway"},
                    "C": {"name": "Tea_Shop", "pos": (544, 96), "size": (96, 96), "chinese_name": "茶壜"},
                    "D": {"name": "Health_Food", "pos": (224, 96), "size": (96, 96), "chinese_name": "強泥兄弟健康餐"},
                    "E": {"name": "Squid_Soup", "pos": (64, 192), "size": (96, 64), "chinese_name": "太祖魷魚羹"},
                    "F": {"name": "Braised_Food", "pos": (64, 256), "size": (64, 64), "chinese_name": "滷味"},
                    "G": {"name": "Rice_Bucket", "pos": (64, 320), "size": (64, 96), "chinese_name": "阿罵的飯桶"}
                },
                "npcs": [
                    {"id": "npc1", "pos": (200, 250), "name": "驚慌學生"},
                    {"id": "npc2", "pos": (350, 300), "name": "受傷職員"}
                ],
                "stairs": [
                    {"pos": (600, 200), "direction": "up"},
                    {"pos": (600, 350), "direction": "up"}
                ],
                "items": [
                    {"pos": (150, 400), "item": {"name": "醫療包", "type": "healing", "value": 30}},
                    {"pos": (450, 150), "item": {"name": "手電筒", "type": "tool", "value": 1}}
                ],
                "combat_zones": [
                    {"pos": (300, 250), "radius": 50, "enemies": ["zombie_student"], "name": "餐廳走廊"},
                    {"pos": (500, 350), "radius": 40, "enemies": ["zombie_student"], "name": "樓梯口"}
                ]
            },
            2: {  # 二樓
                "shops": {
                    "H": {"name": "Japanese_Rice", "pos": (544, 96), "size": (128, 96), "chinese_name": "和食宣丼飯"},
                    "I": {"name": "Vegetarian", "pos": (320, 96), "size": (160, 96), "chinese_name": "素怡沅"},
                    "J": {"name": "Fruit_Juice", "pos": (544, 256), "size": (96, 64), "chinese_name": "水果大亨"},
                    "K": {"name": "Porridge_Kingdom", "pos": (64, 96), "size": (160, 256), "chinese_name": "名松聯合大公國"}
                },
                "npcs": [
                    {"id": "npc3", "pos": (350, 250), "name": "神秘研究員"}
                ],
                "stairs": [
                    {"pos": (600, 200), "direction": "up"},
                    {"pos": (600, 350), "direction": "down"}
                ],
                "items": [
                    {"pos": (100, 400), "item": {"name": "能量飲料", "type": "healing", "value": 20}},
                    {"pos": (500, 400), "item": {"name": "鑰匙卡", "type": "key", "value": 1}}
                ],
                "combat_zones": [
                    {"pos": (250, 200), "radius": 60, "enemies": ["infected_staff"], "name": "二樓中央"},
                    {"pos": (450, 300), "radius": 45, "enemies": ["zombie_student", "infected_staff"], "name": "餐廳後方"}
                ]
            },
            3: {  # 三樓
                "shops": {
                    "L": {"name": "Cafe", "pos": (320, 192), "size": (160, 128), "chinese_name": "咖啡廳"},
                    "M": {"name": "Discussion_Room", "pos": (64, 192), "size": (160, 128), "chinese_name": "討論室"},
                    "N": {"name": "Exhibition", "pos": (544, 256), "size": (128, 96), "chinese_name": "展覽廳"}
                },
                "npcs": [
                    {"id": "npc4", "pos": (250, 250), "name": "最後的研究者"}
                ],
                "stairs": [
                    {"pos": (600, 350), "direction": "down"}
                ],
                "items": [
                    {"pos": (400, 100), "item": {"name": "研究筆記", "type": "clue", "value": 1}},
                    {"pos": (150, 350), "item": {"name": "解藥", "type": "special", "value": 1}}
                ],
                "combat_zones": [
                    {"pos": (200, 300), "radius": 70, "enemies": ["mutant_zombie"], "name": "研究室入口"},
                    {"pos": (400, 250), "radius": 50, "enemies": ["alien", "mutant_zombie"], "name": "神秘區域"}
                ]
            }
        }
        
        # 載入像素風格字體
        self.font = font_manager.get_font(16)
        
        # 地圖背景色彩
        self.floor_colors = {
            1: (100, 80, 60),    # 棕色系
            2: (80, 100, 60),    # 綠色系  
            3: (60, 80, 100)     # 藍色系
        }
    
    def get_current_floor(self):
        return self.current_floor
    
    def change_floor(self, new_floor):
        if 1 <= new_floor <= 3:
            self.current_floor = new_floor
    
    def check_interaction(self, player_x, player_y, floor):
        current_data = self.floor_data.get(floor, {})
        
        # 檢查商店互動
        for shop_id, shop_data in current_data.get("shops", {}).items():
            shop_rect = pygame.Rect(shop_data["pos"], shop_data["size"])
            player_rect = pygame.Rect(player_x, player_y, 32, 32)
            
            if shop_rect.colliderect(player_rect):
                return {
                    "type": "shop",
                    "id": shop_id,
                    "name": shop_data["chinese_name"],
                    "data": shop_data
                }
        
        # 檢查NPC互動
        for npc in current_data.get("npcs", []):
            npc_rect = pygame.Rect(npc["pos"][0]-16, npc["pos"][1]-16, 32, 32)
            player_rect = pygame.Rect(player_x, player_y, 32, 32)
            
            if npc_rect.colliderect(player_rect):
                return {
                    "type": "npc",
                    "id": npc["id"],
                    "name": npc["name"],
                    "data": npc
                }
        
        # 檢查樓梯互動
        for stairs in current_data.get("stairs", []):
            stairs_rect = pygame.Rect(stairs["pos"][0]-16, stairs["pos"][1]-16, 32, 32)
            player_rect = pygame.Rect(player_x, player_y, 32, 32)
            
            if stairs_rect.colliderect(player_rect):
                return {
                    "type": "stairs",
                    "direction": stairs["direction"]
                }
        
        # 檢查道具互動
        for item in current_data.get("items", []):
            item_rect = pygame.Rect(item["pos"][0]-16, item["pos"][1]-16, 32, 32)
            player_rect = pygame.Rect(player_x, player_y, 32, 32)
            
            if item_rect.colliderect(player_rect):
                return {
                    "type": "item",
                    "item": item["item"]
                }
        
        return None
    
    def check_combat_zone(self, player_x, player_y, floor):
        """檢查玩家是否進入戰鬥區域"""
        current_data = self.floor_data.get(floor, {})
        combat_zones = current_data.get("combat_zones", [])
        
        for zone in combat_zones:
            zone_x, zone_y = zone["pos"]
            radius = zone["radius"]
            
            # 計算玩家與戰鬥區域中心的距離
            distance = ((player_x - zone_x)**2 + (player_y - zone_y)**2)**0.5
            
            if distance <= radius:
                return zone
        
        return None
    
    def remove_item_from_floor(self, item_data, floor):
        """從指定樓層移除已收集的物品"""
        current_data = self.floor_data.get(floor, {})
        items = current_data.get("items", [])
        
        # 尋找並移除對應的物品
        for i, item in enumerate(items):
            if item["item"]["name"] == item_data["name"]:
                removed_item = items.pop(i)
                print(f"🗑️ 從{floor}樓地圖移除物品: {item_data['name']}")
                return True
        return False
    
    def remove_item(self, item_data):
        """從當前樓層移除已收集的物品（保持向後相容）"""
        return self.remove_item_from_floor(item_data, self.current_floor)
    
    def render(self, screen):
        # 清除背景
        bg_color = self.floor_colors.get(self.current_floor, (50, 50, 50))
        screen.fill(bg_color)
        
        current_data = self.floor_data.get(self.current_floor, {})
        
        # 繪製商店區域
        for shop_id, shop_data in current_data.get("shops", {}).items():
            # 商店背景
            shop_rect = pygame.Rect(shop_data["pos"], shop_data["size"])
            pygame.draw.rect(screen, (120, 120, 120), shop_rect)
            pygame.draw.rect(screen, (200, 200, 200), shop_rect, 2)
            
            # 商店標籤
            label_text = f"{shop_id}: {shop_data['chinese_name']}"
            text_surface = font_manager.render_text(label_text, 16, (255, 255, 255))
            text_pos = (shop_data["pos"][0] + 5, shop_data["pos"][1] + 5)
            screen.blit(text_surface, text_pos)
        
        # 繪製NPC
        for npc in current_data.get("npcs", []):
            npc_pos = npc["pos"]
            # NPC身體 (像素風格)
            pygame.draw.rect(screen, (255, 200, 150), (npc_pos[0]-8, npc_pos[1]-16, 16, 24))
            # NPC頭部
            pygame.draw.rect(screen, (255, 220, 177), (npc_pos[0]-6, npc_pos[1]-24, 12, 12))
            # NPC眼睛
            pygame.draw.rect(screen, (0, 0, 0), (npc_pos[0]-4, npc_pos[1]-20, 2, 2))
            pygame.draw.rect(screen, (0, 0, 0), (npc_pos[0]+2, npc_pos[1]-20, 2, 2))
            
            # NPC名稱
            name_surface = font_manager.render_text(npc["name"], 16, (255, 255, 0))
            name_pos = (npc_pos[0] - name_surface.get_width()//2, npc_pos[1] + 10)
            screen.blit(name_surface, name_pos)
        
        # 繪製樓梯
        for stairs in current_data.get("stairs", []):
            stairs_pos = stairs["pos"]
            direction = stairs["direction"]
            
            # 樓梯顏色
            stair_color = (150, 150, 50) if direction == "up" else (100, 100, 200)
            
            # 繪製樓梯（像素風格）
            for i in range(6):
                y_offset = i * 4 if direction == "up" else -i * 4
                pygame.draw.rect(screen, stair_color, 
                               (stairs_pos[0] - 12 + i*2, stairs_pos[1] + y_offset, 8, 4))
            
            # 樓梯標籤
            label = "↑" if direction == "up" else "↓"
            label_surface = font_manager.render_text(label, 16, (255, 255, 255))
            label_pos = (stairs_pos[0] - 8, stairs_pos[1] - 30)
            screen.blit(label_surface, label_pos)
        
        # 繪製道具
        for item in current_data.get("items", []):
            item_pos = item["pos"]
            item_data = item["item"]
            
            # 道具圖示（像素風格）
            if item_data["type"] == "healing":
                pygame.draw.rect(screen, (255, 0, 0), (item_pos[0]-6, item_pos[1]-6, 12, 12))
                pygame.draw.rect(screen, (255, 255, 255), (item_pos[0]-1, item_pos[1]-4, 2, 8))
                pygame.draw.rect(screen, (255, 255, 255), (item_pos[0]-4, item_pos[1]-1, 8, 2))
            elif item_data["type"] == "tool":
                pygame.draw.rect(screen, (200, 200, 0), (item_pos[0]-8, item_pos[1]-4, 16, 8))
            elif item_data["type"] == "key":
                pygame.draw.rect(screen, (255, 215, 0), (item_pos[0]-6, item_pos[1]-3, 8, 6))
                pygame.draw.rect(screen, (255, 215, 0), (item_pos[0]+2, item_pos[1]-1, 4, 2))
            elif item_data["type"] == "clue":
                pygame.draw.rect(screen, (255, 255, 255), (item_pos[0]-6, item_pos[1]-8, 12, 16))
                pygame.draw.rect(screen, (0, 0, 0), (item_pos[0]-4, item_pos[1]-6, 8, 2))
                pygame.draw.rect(screen, (0, 0, 0), (item_pos[0]-4, item_pos[1]-3, 6, 1))
            elif item_data["type"] == "special":
                # 解藥 - 特殊閃爍效果
                import time
                if int(time.time() * 4) % 2:  # 閃爍效果
                    pygame.draw.rect(screen, (0, 255, 0), (item_pos[0]-8, item_pos[1]-8, 16, 16))
                    pygame.draw.rect(screen, (255, 255, 255), (item_pos[0]-6, item_pos[1]-6, 12, 12))
                    pygame.draw.rect(screen, (0, 255, 0), (item_pos[0]-4, item_pos[1]-4, 8, 8))
        
        # 繪製戰鬥區域 (半透明紅色圓圈)
        for zone in current_data.get("combat_zones", []):
            zone_x, zone_y = zone["pos"]
            radius = zone["radius"]
            zone_name = zone["name"]
            
            # 繪製戰鬥區域範圍 (半透明)
            combat_surface = pygame.Surface((radius*2, radius*2))
            combat_surface.set_alpha(50)  # 半透明
            combat_surface.fill((255, 0, 0))  # 紅色
            pygame.draw.circle(combat_surface, (255, 0, 0), (radius, radius), radius)
            screen.blit(combat_surface, (zone_x - radius, zone_y - radius))
            
            # 繪製戰鬥區域邊界
            pygame.draw.circle(screen, (255, 100, 100), (zone_x, zone_y), radius, 2)
            
            # 戰鬥區域名稱
            zone_surface = font_manager.render_text(zone_name, 14, (255, 100, 100))
            zone_pos = (zone_x - zone_surface.get_width()//2, zone_y - radius - 20)
            screen.blit(zone_surface, zone_pos)
        
        # 繪製樓層資訊
        floor_text = f"第{self.current_floor}樓"
        floor_surface = font_manager.render_text(floor_text, 16, (255, 255, 255))
        screen.blit(floor_surface, (10, 10))
        
        # 繪製網格線（可選）
        self.draw_grid(screen)
    
    def draw_grid(self, screen):
        # 繪製淡淡的網格線幫助定位
        grid_color = (80, 80, 80)
        screen_width, screen_height = screen.get_size()
        
        # 垂直線
        for x in range(0, screen_width, self.tile_size):
            pygame.draw.line(screen, grid_color, (x, 0), (x, screen_height))
        
        # 水平線  
        for y in range(0, screen_height, self.tile_size):
            pygame.draw.line(screen, grid_color, (0, y), (screen_width, y))
    
    def update(self):
        pass  # 預留給動態效果