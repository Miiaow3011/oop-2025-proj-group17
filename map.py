# map_manager.py - 地圖管理系統
import pygame

class MapManager:
    def __init__(self):
        self.map_width = 20
        self.map_height = 15
        self.tile_size = 32
        
        # 地圖類型定義
        self.FLOOR = 0
        self.WALL = 1
        self.COUNTER = 2
        self.SHELF = 3
        self.DOOR = 4
        self.FREEZER = 5
        self.STORAGE = 6
        
        # 創建便利商店地圖
        self.game_map = self.create_store_map()
        self.load_tile_sprites()
    
    def create_store_map(self):
        """創建便利商店地圖布局"""
        # 創建空地圖
        game_map = [[self.WALL for _ in range(self.map_width)] for _ in range(self.map_height)]
        
        # 創建房間
        for y in range(2, 13):
            for x in range(2, 18):
                game_map[y][x] = self.FLOOR
        
        # 放置收銀台
        game_map[11][8] = self.COUNTER
        game_map[11][9] = self.COUNTER
        
        # 放置貨架
        for x in range(4, 7):
            game_map[4][x] = self.SHELF
            game_map[6][x] = self.SHELF
            game_map[8][x] = self.SHELF
        
        for x in range(12, 15):
            game_map[4][x] = self.SHELF
            game_map[6][x] = self.SHELF
            game_map[8][x] = self.SHELF
        
        # 放置冷凍櫃
        game_map[3][16] = self.FREEZER
        game_map[4][16] = self.FREEZER
        game_map[5][16] = self.FREEZER
        
        # 放置儲藏室門
        game_map[10][3] = self.STORAGE
        
        # 放置出入口
        game_map[12][1] = self.DOOR
        game_map[2][10] = self.DOOR
        
        return game_map
    
    def load_tile_sprites(self):
        """載入地圖圖塊"""
        self.tile_sprites = {}
        
        # 創建簡單的彩色方塊代表不同地形
        for tile_type in [self.FLOOR, self.WALL, self.COUNTER, self.SHELF, self.DOOR, self.FREEZER, self.STORAGE]:
            sprite = pygame.Surface((self.tile_size, self.tile_size))
            
            if tile_type == self.FLOOR:
                sprite.fill((200, 200, 200))  # 灰色地板
            elif tile_type == self.WALL:
                sprite.fill((100, 100, 100))  # 深灰色牆壁
            elif tile_type == self.COUNTER:
                sprite.fill((139, 69, 19))    # 棕色收銀台
            elif tile_type == self.SHELF:
                sprite.fill((160, 82, 45))    # 淺棕色貨架
            elif tile_type == self.DOOR:
                sprite.fill((255, 255, 0))    # 黃色門
            elif tile_type == self.FREEZER:
                sprite.fill((173, 216, 230))  # 淺藍色冷凍櫃
            elif tile_type == self.STORAGE:
                sprite.fill((255, 165, 0))    # 橙色儲藏室
            
            self.tile_sprites[tile_type] = sprite
    
    def get_tile_type(self, x, y):
        """獲取指定位置的地圖類型"""
        if 0 <= x < self.map_width and 0 <= y < self.map_height:
            return self.game_map[y][x]
        return self.WALL
    
    def is_valid_position(self, x, y):
        """檢查位置是否可通行"""
        tile_type = self.get_tile_type(x, y)
        return tile_type in [self.FLOOR, self.DOOR, self.COUNTER, self.STORAGE]
    
    def render(self, screen, player_x, player_y):
        """渲染地圖"""
        # 計算相機偏移（以玩家為中心）
        camera_x = player_x * self.tile_size - 400 + 16
        camera_y = player_y * self.tile_size - 300 + 16
        
        # 渲染可見範圍內的地圖
        for y in range(max(0, player_y - 10), min(self.map_height, player_y + 10)):
            for x in range(max(0, player_x - 13), min(self.map_width, player_x + 13)):
                tile_type = self.game_map[y][x]
                sprite = self.tile_sprites[tile_type]
                
                screen_x = x * self.tile_size - camera_x
                screen_y = y * self.tile_size - camera_y
                
                if -32 <= screen_x <= 800 and -32 <= screen_y <= 600:
                    screen.blit(sprite, (screen_x, screen_y))
