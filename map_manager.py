import pygame
import os
import random
from font_manager import font_manager

class MapManager:
    def __init__(self):
        self.current_floor = 1  # 初始樓層
        self.tile_size = 32
        
        # 🆕 地板圖片
        self.floor_sprites = {}
        self.load_floor_images()
        
        # 樓梯圖片
        self.stairs_sprites = {}
        self.load_stairs_images()
        
        # 🆕 物品圖片
        self.item_sprites = {}
        self.load_item_images()
        
        # 🆕 NPC圖片
        self.npc_sprites = {}
        self.load_npc_images()
        
        # 🆕 商店圖片
        self.shop_sprites = {}
        self.load_shop_images()
        
        # 樓層地圖數據
        self.floor_maps = {
            1: self.create_floor_1(),
            2: self.create_floor_2(),
            3: self.create_floor_3()
        }
        
        # 互動區域（商店、NPC等）
        self.interactions = {
            1: [  # 1樓
                {"type": "shop", "id": "A", "name": "7-11", "x": 50, "y": 350, "width": 80, "height": 60},
                {"type": "shop", "id": "B", "name": "Subway", "x": 200, "y": 250, "width": 80, "height": 60},
                {"type": "shop", "id": "C", "name": "茶壜", "x": 350, "y": 300, "width": 80, "height": 60},
                {"type": "npc", "id": "npc1", "name": "驚慌學生", "x": 500, "y": 400, "width": 30, "height": 30},
                {"type": "stairs", "direction": "up", "x": 450, "y": 100, "width": 96, "height": 48, "target_floor": 2}  # 🆕 加大樓梯尺寸
            ],
            2: [  # 2樓
                {"type": "shop", "id": "D", "name": "和食軒", "x": 100, "y": 200, "width": 80, "height": 60},
                {"type": "shop", "id": "E", "name": "素怡沅", "x": 300, "y": 150, "width": 80, "height": 60},
                {"type": "npc", "id": "npc2", "name": "受傷職員", "x": 200, "y": 300, "width": 30, "height": 30},
                {"type": "stairs", "direction": "up", "x": 450, "y": 90, "width": 96, "height": 48, "target_floor": 3},    # 🆕 加大樓梯尺寸
                {"type": "stairs", "direction": "down", "x": 450, "y": 590, "width": 96, "height": 48, "target_floor": 1}  # 🆕 往上移10個像素：600→590
            ],
            3: [  # 3樓
                {"type": "shop", "id": "L", "name": "咖啡廳", "x": 150, "y": 250, "width": 80, "height": 60},
                {"type": "npc", "id": "npc3", "name": "神秘研究員", "x": 400, "y": 200, "width": 30, "height": 30},
                {"type": "npc", "id": "npc4", "name": "最後的研究者", "x": 300, "y": 350, "width": 30, "height": 30},
                {"type": "stairs", "direction": "down", "x": 450, "y": 600, "width": 96, "height": 48, "target_floor": 2}  # 🆕 加大樓梯尺寸
            ]
        }
        
        # 戰鬥區域 - 🔧 完全隱藏，玩家無法察覺
        self.combat_zones = {
            1: [
                {"name": "走廊1", "x": 150, "y": 150, "width": 100, "height": 80, "enemies": ["zombie_student"]},
                {"name": "角落", "x": 540, "y": 300, "width": 80, "height": 80, "enemies": ["infected_staff"]}  # 🔧 從545再往左調整5像素到540
            ],
            2: [
                {"name": "走廊2", "x": 500, "y": 200, "width": 120, "height": 80, "enemies": ["zombie_student", "infected_staff"]},
                {"name": "廚房", "x": 250, "y": 400, "width": 100, "height": 60, "enemies": ["mutant_zombie"]}
            ],
            3: [
                {"name": "實驗室入口", "x": 100, "y": 100, "width": 150, "height": 100, "enemies": ["alien", "mutant_zombie"]},
                {"name": "研究室", "x": 500, "y": 400, "width": 120, "height": 80, "enemies": ["alien"]}
            ]
        }
        
        # 🔧 修復：物品位置分散，避免重疊
        self.items = {
            1: [
                # 分散在1樓不同區域，避免重疊
                {"name": "醫療包", "type": "healing", "value": 30, "x": 120, "y": 180, "description": "專業醫療包，恢復30血量"},
                {"name": "能量飲料", "type": "healing", "value": 15, "x": 380, "y": 450, "description": "補充體力的能量飲料"},
                {"name": "小型藥劑", "type": "healing", "value": 20, "x": 550, "y": 250, "description": "基礎治療藥劑"}
            ],
            2: [
                # 2樓物品位置
                {"name": "鑰匙卡", "type": "key", "x": 150, "y": 380, "description": "進入三樓實驗室的鑰匙卡"},
                {"name": "研究筆記", "type": "clue", "x": 420, "y": 280, "description": "記錄了重要研究資料的筆記"},
                {"name": "急救包", "type": "healing", "value": 40, "x": 80, "y": 450, "description": "大型急救包，恢復40血量"}
            ],
            3: [
                # 3樓最重要的物品
                {"name": "解藥", "type": "special", "x": 250, "y": 180, "description": "拯救世界的神秘解藥！"},
                {"name": "實驗資料", "type": "clue", "x": 480, "y": 350, "description": "關於病毒研究的重要資料"},
                {"name": "超級藥劑", "type": "healing", "value": 60, "x": 350, "y": 480, "description": "最強效的治療藥劑"}
            ]
        }
        
        # 🆕 新增：物品收集狀態追蹤
        self.collected_items = set()  # 已收集的物品ID
        
        # 🔧 新增：除錯模式控制戰鬥區域顯示
        self.debug_show_combat_zones = False  # 預設關閉除錯顯示
    
    def load_floor_images(self):
        """🆕 載入地板圖片"""
        floor_paths = {
            "floor": "assets/images/floor.png",  # 主要檔名
            "floor_alt": "assets/images/神饃.png",  # 備用檔名
            "tile": "assets/images/tile.png"  # 另一個備用選項
        }
        
        print("🏢 載入地板圖片...")
        
        for floor_type, path in floor_paths.items():
            if os.path.exists(path):
                try:
                    # 載入地板圖片
                    image = pygame.image.load(path).convert_alpha()
                    original_size = image.get_size()
                    print(f"   原始地板圖片尺寸: {original_size}")
                    
                    # 🎨 縮放到64x64像素（配合地板磚塊大小）
                    target_size = 64
                    image = pygame.transform.scale(image, (target_size, target_size))
                    self.floor_sprites[floor_type] = image
                    print(f"✅ 成功載入地板圖片: {floor_type} - {path}")
                    print(f"   縮放後尺寸: {target_size}x{target_size}")
                    break  # 找到第一個可用的圖片就停止
                except Exception as e:
                    print(f"❌ 載入地板圖片失敗: {floor_type} - {e}")
        
        # 檢查是否成功載入地板圖片
        self.use_floor_sprites = len(self.floor_sprites) > 0
        
        if not self.use_floor_sprites:
            print("📦 未找到地板圖片，將使用程式繪製地板")
            print("💡 請將地板圖片放在以下任一位置:")
            for path in floor_paths.values():
                print(f"   - {path}")
        else:
            print(f"🎨 成功載入地板圖片！使用圖片渲染地板")
    
    def load_shop_images(self):
        """🆕 載入商店圖片 - 新增茶壜、素怡沅和和食軒支援"""
        shop_paths = {
            "711": "assets/images/711.png",  # 你的7-11圖片
            "subway": "assets/images/subway.png",  # 可選的Subway圖片
            "coffee": "assets/images/coffee.png",  # 可選的咖啡廳圖片
            "tea": "assets/images/tea.png",  # 🆕 新增茶壜圖片
            "vegetarian": "assets/images/vegetarian_second_floor.png",  # 🆕 新增素怡沅圖片
            "restaurant": "assets/images/restaurant_second_floor.png"  # 🆕 新增和食軒圖片
        }
        
        print("🏪 載入商店圖片...")
        
        for shop_type, path in shop_paths.items():
            if os.path.exists(path):
                try:
                    # 載入商店圖片
                    image = pygame.image.load(path).convert_alpha()
                    original_size = image.get_size()
                    print(f"   原始商店圖片尺寸: {original_size}")
                    
                    # 🎨 根據商店類型設定不同尺寸
                    if shop_type == "711":
                        # 7-11 調小一點：110x90像素
                        target_width = 110
                        target_height = 90
                    elif shop_type == "subway":
                        # Subway 調大一點：100x78像素
                        target_width = 100
                        target_height = 78
                    elif shop_type == "tea":
                        # 🆕 茶壜設定合適尺寸：100x75像素
                        target_width = 100
                        target_height = 75
                    elif shop_type == "vegetarian":
                        # 🆕 素怡沅設定尺寸：128x96像素
                        target_width = 128
                        target_height = 96
                    elif shop_type == "restaurant":
                        # 🆕 和食軒設定尺寸：120x90像素
                        target_width = 120
                        target_height = 90
                    else:
                        # 其他商店維持原尺寸：80x60像素
                        target_width = 80
                        target_height = 60
                    
                    image = pygame.transform.scale(image, (target_width, target_height))
                    self.shop_sprites[shop_type] = image
                    print(f"✅ 成功載入商店圖片: {shop_type} - {path}")
                    print(f"   縮放後尺寸: {target_width}x{target_height}")
                except Exception as e:
                    print(f"❌ 載入商店圖片失敗: {shop_type} - {e}")
        
        # 檢查是否成功載入商店圖片
        self.use_shop_sprites = len(self.shop_sprites) > 0
        
        if not self.use_shop_sprites:
            print("📦 未找到商店圖片，將使用程式繪製商店")
        else:
            print(f"🎨 成功載入 {len(self.shop_sprites)} 個商店圖片")
    
    def load_npc_images(self):
        """🆕 載入NPC圖片"""
        npc_paths = {
            "npc3_2floor": "assets/images/npc3_2floor.png",  # 🆕 你的NPC圖片
            "default_npc": "assets/images/npc.png"  # 可選的通用NPC圖片
        }
        
        print("👤 載入NPC圖片...")
        
        for npc_type, path in npc_paths.items():
            if os.path.exists(path):
                try:
                    # 載入NPC圖片
                    image = pygame.image.load(path).convert_alpha()
                    original_size = image.get_size()
                    print(f"   原始NPC圖片尺寸: {original_size}")
                    
                    # 🎨 NPC圖片統一縮放到55x70像素
                    target_width = 55
                    target_height = 70
                    image = pygame.transform.scale(image, (target_width, target_height))
                    self.npc_sprites[npc_type] = image
                    print(f"✅ 成功載入NPC圖片: {npc_type} - {path}")
                    print(f"   縮放後尺寸: {target_width}x{target_height}")
                except Exception as e:
                    print(f"❌ 載入NPC圖片失敗: {npc_type} - {e}")
        
        # 檢查是否成功載入NPC圖片
        self.use_npc_sprites = len(self.npc_sprites) > 0
        
        if not self.use_npc_sprites:
            print("📦 未找到NPC圖片，將使用程式繪製NPC")
        else:
            print(f"🎨 成功載入 {len(self.npc_sprites)} 個NPC圖片")
    
    def load_item_images(self):
        """🆕 載入物品圖片"""
        item_paths = {
            "key_2floor": "assets/images/key_2floor.png",  # 🆕 你的鑰匙卡圖片
            "healing": "assets/images/healing.png",  # 可選的醫療包圖片
            "special": "assets/images/special.png"  # 可選的特殊物品圖片
        }
        
        print("🗝️ 載入物品圖片...")
        
        for item_type, path in item_paths.items():
            if os.path.exists(path):
                try:
                    # 載入物品圖片
                    image = pygame.image.load(path).convert_alpha()
                    original_size = image.get_size()
                    print(f"   原始物品圖片尺寸: {original_size}")
                    
                    # 🎨 物品圖片統一縮放到32x32像素
                    target_size = 32
                    image = pygame.transform.scale(image, (target_size, target_size))
                    self.item_sprites[item_type] = image
                    print(f"✅ 成功載入物品圖片: {item_type} - {path}")
                    print(f"   縮放後尺寸: {target_size}x{target_size}")
                except Exception as e:
                    print(f"❌ 載入物品圖片失敗: {item_type} - {e}")
        
        # 檢查是否成功載入物品圖片
        self.use_item_sprites = len(self.item_sprites) > 0
        
        if not self.use_item_sprites:
            print("📦 未找到物品圖片，將使用程式繪製物品")
        else:
            print(f"🎨 成功載入 {len(self.item_sprites)} 個物品圖片")
    
    def load_stairs_images(self):
        """載入樓梯圖片"""
        stairs_paths = {
            "up": "assets/images/stairs_up.png",
            "down": "assets/images/stairs_down.png"
        }
        
        print("🪜 載入樓梯圖片...")
        
        for direction, path in stairs_paths.items():
            if os.path.exists(path):
                try:
                    # 載入你自己的樓梯圖片
                    image = pygame.image.load(path).convert_alpha()
                    original_size = image.get_size()
                    print(f"   原始圖片尺寸: {original_size}")
                    
                    # 🎨 保持原圖比例，縮放到合適大小
                    # 你可以調整這個目標尺寸來改變樓梯大小
                    target_width = 96  # 可以調整這個數值
                    target_height = 72  # 可以調整這個數值
                    
                    # 縮放到目標尺寸
                    image = pygame.transform.scale(image, (target_width, target_height))
                    self.stairs_sprites[direction] = image
                    print(f"✅ 成功載入樓梯圖片: {direction} - {path}")
                    print(f"   縮放後尺寸: {target_width}x{target_height}")
                except Exception as e:
                    print(f"❌ 載入樓梯圖片失敗: {direction} - {e}")
                    self.stairs_sprites[direction] = None
            else:
                print(f"⚠️ 找不到樓梯圖片: {path}")
                print(f"   請確認你的樓梯圖片已放在正確位置")
                self.stairs_sprites[direction] = None
        
        # 如果沒有載入到圖片，設定標記
        self.use_sprites = any(sprite is not None for sprite in self.stairs_sprites.values())
        
        if not self.use_sprites:
            print("📦 未找到樓梯圖片，將使用像素繪製樓梯")
        else:
            print(f"🎨 成功載入 {len([s for s in self.stairs_sprites.values() if s is not None])} 個樓梯圖片")
            print("💡 如果樓梯太小或太大，可以在 load_stairs_images() 方法中調整 target_width 和 target_height")

    def create_floor_1(self):
        """創建1樓地圖"""
        return {
            "name": "第二餐廳 1樓",
            "background_color": (40, 40, 60),
            "walls": [
                # 外牆
                {"x": 0, "y": 0, "width": 1024, "height": 32},      # 上牆
                {"x": 0, "y": 736, "width": 1024, "height": 32},    # 下牆
                {"x": 0, "y": 0, "width": 32, "height": 768},       # 左牆
                {"x": 992, "y": 0, "width": 32, "height": 768},     # 右牆
                
                # 內部隔間
                {"x": 150, "y": 200, "width": 200, "height": 20},   # 商店隔間
                {"x": 400, "y": 150, "width": 20, "height": 200},   # 垂直隔間
            ]
        }

    def create_floor_2(self):
        """創建2樓地圖"""
        return {
            "name": "第二餐廳 2樓",
            "background_color": (60, 40, 40),
            "walls": [
                # 外牆
                {"x": 0, "y": 0, "width": 1024, "height": 32},
                {"x": 0, "y": 736, "width": 1024, "height": 32},
                {"x": 0, "y": 0, "width": 32, "height": 768},
                {"x": 992, "y": 0, "width": 32, "height": 768},
                
                # 內部隔間
                {"x": 200, "y": 100, "width": 150, "height": 20},
                {"x": 250, "y": 300, "width": 20, "height": 150},
            ]
        }

    def create_floor_3(self):
        """創建3樓地圖"""
        return {
            "name": "第二餐廳 3樓",
            "background_color": (40, 60, 40),
            "walls": [
                # 外牆
                {"x": 0, "y": 0, "width": 1024, "height": 32},
                {"x": 0, "y": 736, "width": 1024, "height": 32},
                {"x": 0, "y": 0, "width": 32, "height": 768},
                {"x": 992, "y": 0, "width": 32, "height": 768},
                
                # 實驗室隔間
                {"x": 100, "y": 200, "width": 300, "height": 20},
                {"x": 350, "y": 200, "width": 20, "height": 200},
            ]
        }

    def change_floor(self, new_floor):
        """切換樓層"""
        if new_floor in self.floor_maps:
            old_floor = self.current_floor
            self.current_floor = new_floor
            print(f"🏢 從 {old_floor} 樓切換到 {new_floor} 樓")
            return True
        return False

    def get_current_floor(self):
        """獲取當前樓層"""
        return self.current_floor

    def check_interaction(self, player_x, player_y, floor):
        """檢查玩家位置是否有互動物件"""
        if floor not in self.interactions:
            return None

        for interaction in self.interactions[floor]:
            # 檢查碰撞
            if (interaction["x"] <= player_x <= interaction["x"] + interaction["width"] and
                interaction["y"] <= player_y <= interaction["y"] + interaction["height"]):
                return interaction

        return None

    def check_combat_zone(self, player_x, player_y, floor):
        """檢查是否進入戰鬥區域"""
        if floor not in self.combat_zones:
            return None

        for zone in self.combat_zones[self.current_floor]:
            if (zone["x"] <= player_x <= zone["x"] + zone["width"] and
                zone["y"] <= player_y <= zone["y"] + zone["height"]):
                return zone

        return None

    def remove_combat_zone(self, zone, floor):
        """移除戰鬥區域（戰鬥結束後）"""
        if floor in self.combat_zones and zone in self.combat_zones[floor]:
            self.combat_zones[floor].remove(zone)
            print(f"🗑️ 移除戰鬥區域: {zone['name']} (樓層 {floor})")

    def check_item_pickup(self, player_x, player_y, floor):
        """🆕 檢查是否可以拾取物品"""
        if floor not in self.items:
            return None

        pickup_distance = 30  # 拾取距離

        for item in self.items[floor]:
            # 創建物品ID來追蹤是否已收集
            item_id = f"{floor}_{item['name']}_{item['x']}_{item['y']}"

            # 檢查是否已經收集過
            if item_id in self.collected_items:
                continue

            # 計算距離
            distance = ((player_x - item["x"])**2 + (player_y - item["y"])**2)**0.5

            if distance <= pickup_distance:
                return {"item": item, "item_id": item_id}

        return None

    def collect_item(self, item_id):
        """🆕 收集物品"""
        self.collected_items.add(item_id)
        print(f"📦 收集物品: {item_id}")

    def remove_item(self, item):
        """移除已收集的物品（舊方法，保持兼容性）"""
        for floor_items in self.items.values():
            if item in floor_items:
                floor_items.remove(item)
                break

    def update(self):
        """更新地圖狀態"""
        # 這裡可以添加動態元素的更新邏輯
        pass

    def render(self, screen):
        """渲染當前樓層"""
        current_map = self.floor_maps[self.current_floor]

        # 清除背景
        screen.fill(current_map["background_color"])

        # 渲染地板
        self.render_floor(screen)

        # 渲染牆壁
        self.render_walls(screen, current_map["walls"])

        # 渲染互動區域
        self.render_interactions(screen)

        # 🔧 只有在除錯模式下才渲染戰鬥區域
        if self.debug_show_combat_zones:
            self.render_combat_zones(screen)
        else:
            # 🆕 在戰鬥區域渲染普通地板，完全隱藏危險性
            self.render_combat_zones_hidden(screen)

        # 渲染物品
        self.render_items(screen)

        # 渲染樓層資訊
        self.render_floor_info(screen)

    def render_floor(self, screen):
        """🆕 渲染地板 - 支援圖片和程式繪製"""
        if self.use_floor_sprites and self.floor_sprites:
            self.render_floor_with_sprites(screen)
        else:
            self.render_floor_with_code(screen)

    def render_floor_with_sprites(self, screen):
        """🆕 使用圖片渲染地板"""
        # 獲取第一個可用的地板圖片
        floor_sprite = None
        for sprite in self.floor_sprites.values():
            if sprite:
                floor_sprite = sprite
                break

        if not floor_sprite:
            # 如果沒有圖片，回退到程式繪製
            self.render_floor_with_code(screen)
            return

        # 使用圖片鋪滿地板
        sprite_size = 64  # 圖片大小

        # 計算需要多少個圖片來填滿螢幕
        cols = (1024 // sprite_size) + 1
        rows = (768 // sprite_size) + 1

        for col in range(cols):
            for row in range(rows):
                x = col * sprite_size
                y = row * sprite_size

                # 確保不超出邊界
                if x < 1024 and y < 768:
                    screen.blit(floor_sprite, (x, y))

    def render_floor_with_code(self, screen):
        """🆕 使用程式繪製地板（備用方法）"""
        # 簡單的地板磚塊效果
        tile_color = (80, 80, 80)
        for x in range(32, 992, 64):
            for y in range(32, 736, 64):
                if (x // 64 + y // 64) % 2 == 0:
                    pygame.draw.rect(screen, tile_color, (x, y, 64, 64))
                    pygame.draw.rect(screen, (60, 60, 60), (x, y, 64, 64), 1)

    def render_walls(self, screen, walls):
        """渲染牆壁"""
        wall_color = (100, 100, 100)
        for wall in walls:
            pygame.draw.rect(screen, wall_color,
                           (wall["x"], wall["y"], wall["width"], wall["height"]))
            # 牆壁邊框
            pygame.draw.rect(screen, (120, 120, 120),
                           (wall["x"], wall["y"], wall["width"], wall["height"]), 2)

    def render_interactions(self, screen):
        """渲染互動區域"""
        if self.current_floor not in self.interactions:
            return

        for interaction in self.interactions[self.current_floor]:
            if interaction["type"] == "shop":
                self.render_shop(screen, interaction)
            elif interaction["type"] == "npc":
                self.render_npc(screen, interaction)
            elif interaction["type"] == "stairs":
                self.render_stairs(screen, interaction)

    def render_shop(self, screen, shop):
        """渲染商店 - 支援圖片和程式繪製"""
        # 🎨 優先使用圖片渲染
        if self.use_shop_sprites and self.render_shop_with_sprite(screen, shop):
            # 圖片渲染成功，添加商店名稱
            self.render_shop_name(screen, shop)
        else:
            # 備用：程式繪製
            self.render_shop_with_code(screen, shop)
    
    def render_shop_with_sprite(self, screen, shop):
        """🆕 使用圖片渲染商店 - 新增茶壜和素怡沅支援"""
        shop_id = shop["id"]
        shop_name = shop["name"]
        
        # 根據商店名稱或ID選擇對應圖片
        sprite = None
        draw_x = shop["x"]
        draw_y = shop["y"]
        
        if shop_id == "A" and "711" in self.shop_sprites:  # 7-11
            sprite = self.shop_sprites["711"]
            # 7-11 圖片調整位置和大小
            sprite_width = 135
            sprite_height = 101
            # 計算位置：置中但往右移動30像素（15+15）
            x_offset = (shop["width"] - sprite_width) // 2 + 30  # 往右移30像素
            y_offset = (shop["height"] - sprite_height) // 2
            draw_x = shop["x"] + x_offset
            draw_y = shop["y"] + y_offset
        elif shop_name == "Subway" and "subway" in self.shop_sprites:
            sprite = self.shop_sprites["subway"]
        elif shop_name == "咖啡廳" and "coffee" in self.shop_sprites:
            sprite = self.shop_sprites["coffee"]
        elif shop_name == "茶壜" and "tea" in self.shop_sprites:
            # 🆕 茶壜圖片渲染
            sprite = self.shop_sprites["tea"]
            # 茶壜圖片位置微調（可根據需要調整）
            x_offset = (shop["width"] - 100) // 2  # 100是茶壜圖片寬度
            y_offset = (shop["height"] - 75) // 2  # 75是茶壜圖片高度
            draw_x = shop["x"] + x_offset
            draw_y = shop["y"] + y_offset
        elif shop_name == "素怡沅" and "vegetarian" in self.shop_sprites:
            # 🆕 素怡沅圖片渲染 - 調整為128x96尺寸
            sprite = self.shop_sprites["vegetarian"]
            # 素怡沅圖片位置微調
            x_offset = (shop["width"] - 128) // 2  # 128是素怡沅圖片寬度
            y_offset = (shop["height"] - 96) // 2  # 96是素怡沅圖片高度
            draw_x = shop["x"] + x_offset
            draw_y = shop["y"] + y_offset
        elif shop_name == "和食軒" and "restaurant" in self.shop_sprites:
            # 🆕 和食軒圖片渲染 - 120x90尺寸
            sprite = self.shop_sprites["restaurant"]
            # 和食軒圖片位置微調
            x_offset = (shop["width"] - 120) // 2  # 120是和食軒圖片寬度
            y_offset = (shop["height"] - 90) // 2  # 90是和食軒圖片高度
            draw_x = shop["x"] + x_offset
            draw_y = shop["y"] + y_offset
        
        if sprite:
            # 繪製商店圖片
            screen.blit(sprite, (draw_x, draw_y))
            return True
        
        return False
    
    def render_shop_with_code(self, screen, shop):
        """🆕 程式繪製商店（備用方法）"""
        # 商店背景
        shop_color = (100, 150, 200)
        pygame.draw.rect(screen, shop_color,
                        (shop["x"], shop["y"], shop["width"], shop["height"]))
        pygame.draw.rect(screen, (150, 200, 255),
                        (shop["x"], shop["y"], shop["width"], shop["height"]), 2)

        # 商店名稱
        self.render_shop_name(screen, shop)
    
    def render_shop_name(self, screen, shop):
        """🆕 渲染商店名稱"""
        # 根據商店名稱調整文字位置
        if shop["name"] == "素怡沅":
            # 素怡沅的文字往下移2個像素
            text_y = shop["y"] + shop["height"]//2 + 62
        elif shop["name"] == "茶壜":
            # 茶壜的文字往上移6個像素（原本-3，再-3）
            text_y = shop["y"] + shop["height"]//2 + 54
        elif shop["name"] == "7-11":
            # 7-11的文字往上移3個像素
            text_y = shop["y"] + shop["height"]//2 + 57
        elif shop["name"] == "Subway":
            # Subway的文字往下移2個像素（原本+1，再+1）
            text_y = shop["y"] + shop["height"]//2 + 62
        else:
            # 其他商店維持原位置
            text_y = shop["y"] + shop["height"]//2 + 60
        
        name_surface = font_manager.render_text(shop["name"], 18, (255, 255, 255))
        name_rect = name_surface.get_rect(center=(shop["x"] + shop["width"]//2, text_y))
        
        # 名稱背景（讓文字更清楚）
        bg_rect = name_rect.copy()
        bg_rect.inflate(8, 4)
        bg_surface = pygame.Surface(bg_rect.size, pygame.SRCALPHA)
        bg_surface.fill((0, 0, 0, 150))
        screen.blit(bg_surface, bg_rect)
        
        screen.blit(name_surface, name_rect)

    def render_npc(self, screen, npc):
        """渲染NPC - 支援圖片和程式繪製"""
        center_x = npc["x"] + npc["width"] // 2
        center_y = npc["y"] + npc["height"] // 2

        # 🎨 優先使用圖片渲染
        if self.use_npc_sprites and self.render_npc_with_sprite(screen, npc, center_x, center_y):
            # 圖片渲染成功，添加NPC名稱（使用調整後的位置）
            if npc.get("name") == "受傷職員":
                # 受傷職員使用調整後的位置
                adjusted_center_y = center_y + 5
                self.render_npc_name(screen, npc, center_x, adjusted_center_y)
            else:
                # 其他NPC使用原位置
                self.render_npc_name(screen, npc, center_x, center_y)
        else:
            # 備用：程式繪製圓形NPC
            self.render_npc_with_code(screen, npc, center_x, center_y)
    
    def render_npc_with_sprite(self, screen, npc, center_x, center_y):
        """🆕 使用圖片渲染NPC"""
        npc_id = npc.get("id", "")
        npc_name = npc.get("name", "")
        
        # 🆕 根據NPC名稱調整圖片位置
        if npc_name == "受傷職員":
            # 受傷職員的圖片往下5個像素
            adjusted_center_y = center_y + 5
        else:
            # 其他NPC維持原位置
            adjusted_center_y = center_y
        
        # 根據NPC ID或名稱選擇對應圖片
        sprite = None
        
        # 🎯 優先使用你的專用NPC圖片
        if "npc3_2floor" in self.npc_sprites:
            sprite = self.npc_sprites["npc3_2floor"]
        elif "default_npc" in self.npc_sprites:
            sprite = self.npc_sprites["default_npc"]
        
        if sprite:
            # 計算圖片繪製位置（55x70像素，置中）
            sprite_width = 55
            sprite_height = 70
            draw_x = center_x - sprite_width // 2
            draw_y = adjusted_center_y - sprite_height // 2
            
            # 繪製NPC圖片
            screen.blit(sprite, (draw_x, draw_y))
            return True
        
        return False
    
    def render_npc_with_code(self, screen, npc, center_x, center_y):
        """🆕 程式繪製NPC（備用方法）"""
        # NPC圓形（原本的樣式）
        npc_color = (255, 200, 100)
        pygame.draw.circle(screen, npc_color, (center_x, center_y), 15)
        pygame.draw.circle(screen, (255, 255, 255), (center_x, center_y), 15, 2)
        
        # NPC名稱
        self.render_npc_name(screen, npc, center_x, center_y)
    
    def render_npc_name(self, screen, npc, center_x, center_y):
        """🆕 渲染NPC名稱"""
        # 根據NPC名稱調整文字位置
        if npc["name"] == "受傷職員":
            # 受傷職員的文字往下移10個像素（圖片已經下移5個，文字相對再下移5個，總共-30）
            text_y = center_y - 30
        elif npc["name"] == "驚慌學生":
            # 驚慌學生的文字往下移5個像素
            text_y = center_y - 40
        else:
            # 其他NPC維持原位置
            text_y = center_y - 45
        
        name_surface = font_manager.render_text(npc["name"], 14, (255, 255, 255))
        name_rect = name_surface.get_rect(center=(center_x, text_y))
        
        # 名稱背景（讓文字更清楚）
        bg_rect = name_rect.copy()
        bg_rect.inflate(8, 4)
        bg_surface = pygame.Surface(bg_rect.size, pygame.SRCALPHA)
        bg_surface.fill((0, 0, 0, 150))
        screen.blit(bg_surface, bg_rect)
        
        screen.blit(name_surface, name_rect)
        
        screen.blit(name_surface, name_rect)
        
        screen.blit(name_surface, name_rect)
        
        screen.blit(name_surface, name_rect)
        
        screen.blit(name_surface, name_rect)

    def render_stairs(self, screen, stairs):
        """渲染樓梯 - 支援圖片和像素繪製"""
        x, y = stairs["x"], stairs["y"]
        width, height = stairs["width"], stairs["height"]
        direction = stairs["direction"]

        # 🎨 優先使用圖片渲染
        if self.use_sprites and direction in self.stairs_sprites and self.stairs_sprites[direction]:
            self.render_stairs_sprite(screen, stairs)
        else:
            # 備用：像素風格樓梯
            self.render_stairs_pixel(screen, stairs)

        # 互動提示
        hint_surface = font_manager.render_text("空白鍵", 12, (255, 255, 0))
        hint_rect = hint_surface.get_rect(center=(x + width//2, y - 20))  # 🆕 調整提示位置
        screen.blit(hint_surface, hint_rect)

    def render_stairs_sprite(self, screen, stairs):
        """使用圖片渲染樓梯"""
        direction = stairs["direction"]
        sprite = self.stairs_sprites[direction]

        if sprite:
            # 繪製樓梯圖片
            screen.blit(sprite, (stairs["x"], stairs["y"]))

            # 添加方向箭頭（保留箭頭，移除圓圈光效）
            if direction == "up":
                # 向上箭頭
                arrow_points = [
                    (stairs["x"] + 48, stairs["y"] - 8),   # 🆕 調整箭頭位置
                    (stairs["x"] + 40, stairs["y"] + 8),
                    (stairs["x"] + 56, stairs["y"] + 8)
                ]
                pygame.draw.polygon(screen, (255, 255, 0), arrow_points)
            else:
                # 向下箭頭
                arrow_points = [
                    (stairs["x"] + 48, stairs["y"] + 60),  # 🆕 調整箭頭位置
                    (stairs["x"] + 40, stairs["y"] + 45),
                    (stairs["x"] + 56, stairs["y"] + 45)
                ]
                pygame.draw.polygon(screen, (0, 255, 255), arrow_points)

    def render_stairs_pixel(self, screen, stairs):
        """像素風格渲染樓梯"""
        x, y = stairs["x"], stairs["y"]
        width, height = stairs["width"], stairs["height"]
        direction = stairs["direction"]

        if direction == "up":
            # 上樓梯：階梯向上
            stair_color = (160, 140, 100)
            highlight_color = (200, 180, 140)

            # 繪製多個階梯
            step_height = height // 4
            for i in range(4):
                step_y = y + (3 - i) * step_height
                step_width = width - i * 8
                step_x = x + i * 4

                # 階梯面
                pygame.draw.rect(screen, stair_color,
                               (step_x, step_y, step_width, step_height))
                # 階梯高光
                pygame.draw.rect(screen, highlight_color,
                               (step_x, step_y, step_width, 2))
                # 階梯邊框
                pygame.draw.rect(screen, (100, 80, 60),
                               (step_x, step_y, step_width, step_height), 1)

            # 上樓箭頭（保留）
            arrow_points = [
                (x + width//2, y - 8),      # 🆕 調整箭頭位置和大小
                (x + width//2 - 12, y + 8),
                (x + width//2 + 12, y + 8)
            ]
            pygame.draw.polygon(screen, (255, 255, 0), arrow_points)

        else:
            # 下樓梯：階梯向下
            stair_color = (140, 120, 80)
            shadow_color = (100, 80, 60)

            # 繪製向下的階梯
            step_height = height // 4
            for i in range(4):
                step_y = y + i * step_height
                step_width = width - i * 8
                step_x = x + i * 4

                # 階梯面
                pygame.draw.rect(screen, stair_color,
                               (step_x, step_y, step_width, step_height))
                # 階梯陰影
                pygame.draw.rect(screen, shadow_color,
                               (step_x, step_y + step_height - 2, step_width, 2))
                # 階梯邊框
                pygame.draw.rect(screen, (120, 100, 80),
                               (step_x, step_y, step_width, step_height), 1)

            # 下樓箭頭（保留）
            arrow_points = [
                (x + width//2, y + height + 12),    # 🆕 調整箭頭位置和大小
                (x + width//2 - 12, y + height - 3),
                (x + width//2 + 12, y + height - 3)
            ]
            pygame.draw.polygon(screen, (0, 255, 255), arrow_points)

    def render_combat_zones_hidden(self, screen):
        """🆕 渲染隱藏的戰鬥區域 - 看起來像普通地板"""
        if self.current_floor not in self.combat_zones:
            return

        for zone in self.combat_zones[self.current_floor]:
            # 🔧 在戰鬥區域渲染普通地板紋理，完全隱藏危險性
            if self.use_floor_sprites and self.floor_sprites:
                self.render_hidden_zone_with_sprites(screen, zone)
            else:
                self.render_hidden_zone_with_code(screen, zone)

    def render_hidden_zone_with_sprites(self, screen, zone):
        """🆕 使用地板圖片渲染隱藏的戰鬥區域"""
        # 獲取第一個可用的地板圖片
        floor_sprite = None
        for sprite in self.floor_sprites.values():
            if sprite:
                floor_sprite = sprite
                break

        if not floor_sprite:
            # 如果沒有圖片，使用程式繪製
            self.render_hidden_zone_with_code(screen, zone)
            return

        # 在戰鬥區域範圍內重複鋪地板圖片
        sprite_size = 64
        
        # 計算區域內需要的圖片數量
        start_x = (zone["x"] // sprite_size) * sprite_size
        start_y = (zone["y"] // sprite_size) * sprite_size
        end_x = zone["x"] + zone["width"]
        end_y = zone["y"] + zone["height"]

        x = start_x
        while x < end_x:
            y = start_y
            while y < end_y:
                # 只在戰鬥區域範圍內繪製
                if (x >= zone["x"] and x < zone["x"] + zone["width"] and
                    y >= zone["y"] and y < zone["y"] + zone["height"]):
                    screen.blit(floor_sprite, (x, y))
                y += sprite_size
            x += sprite_size

    def render_hidden_zone_with_code(self, screen, zone):
        """🆕 使用程式繪製隱藏的戰鬥區域"""
        # 使用與正常地板相同的顏色和樣式
        tile_color = (80, 80, 80)
        
        # 在戰鬥區域內繪製地板磚塊
        for x in range(zone["x"], zone["x"] + zone["width"], 64):
            for y in range(zone["y"], zone["y"] + zone["height"], 64):
                # 確保磚塊在區域範圍內
                tile_width = min(64, zone["x"] + zone["width"] - x)
                tile_height = min(64, zone["y"] + zone["height"] - y)
                
                if (x // 64 + y // 64) % 2 == 0:
                    pygame.draw.rect(screen, tile_color, (x, y, tile_width, tile_height))
                    pygame.draw.rect(screen, (60, 60, 60), (x, y, tile_width, tile_height), 1)

    def render_combat_zones(self, screen):
        """渲染戰鬥區域 - 只在除錯模式下顯示紅色框"""
        if self.current_floor not in self.combat_zones:
            return

        for zone in self.combat_zones[self.current_floor]:
            # 危險區域標示 - 只在除錯模式下顯示
            danger_color = (255, 0, 0, 50)
            danger_rect = pygame.Rect(zone["x"], zone["y"], zone["width"], zone["height"])

            # 創建半透明表面
            danger_surface = pygame.Surface((zone["width"], zone["height"]))
            danger_surface.set_alpha(50)
            danger_surface.fill((255, 0, 0))
            screen.blit(danger_surface, (zone["x"], zone["y"]))

            # 危險區域邊框
            pygame.draw.rect(screen, (255, 0, 0), danger_rect, 2)

            # 警告文字
            warning_surface = font_manager.render_text("危險區域", 14, (255, 255, 255))
            warning_rect = warning_surface.get_rect(center=(zone["x"] + zone["width"]//2,
                                                          zone["y"] + zone["height"]//2))
            screen.blit(warning_surface, warning_rect)

    def render_items(self, screen):
        """🔧 修復：渲染物品，避免重疊顯示"""
        if self.current_floor not in self.items:
            return

        current_time = pygame.time.get_ticks()

        for item in self.items[self.current_floor]:
            # 創建物品ID檢查是否已收集
            item_id = f"{self.current_floor}_{item['name']}_{item['x']}_{item['y']}"

            # 如果已收集，跳過渲染
            if item_id in self.collected_items:
                continue

            # 🎨 改善：物品渲染效果
            self.render_single_item(screen, item, current_time)

    def render_single_item(self, screen, item, current_time):
        """🆕 渲染單個物品，帶有動畫效果"""
        x, y = item["x"], item["y"]
        item_type = item["type"]
        item_name = item.get("name", "")

        # 🎨 優先使用圖片渲染特定物品
        if self.use_item_sprites and self.render_item_with_sprite(screen, item, x, y, current_time):
            # 圖片渲染成功，添加物品名稱
            self.render_item_name(screen, item, x, y)
        else:
            # 備用：程式繪製物品
            self.render_item_with_code(screen, item, x, y, current_time)
    
    def render_item_with_sprite(self, screen, item, x, y, current_time):
        """🆕 使用圖片渲染物品"""
        item_name = item.get("name", "")
        item_type = item.get("type", "")
        
        # 根據物品名稱選擇對應圖片
        sprite = None
        
        if item_name == "鑰匙卡" and "key_2floor" in self.item_sprites:
            sprite = self.item_sprites["key_2floor"]
        elif item_type == "healing" and "healing" in self.item_sprites:
            sprite = self.item_sprites["healing"]
        elif item_type == "special" and "special" in self.item_sprites:
            sprite = self.item_sprites["special"]
        
        if sprite:
            # 物品光暈效果（呼吸燈）
            pulse = abs((current_time % 2000 - 1000) / 1000.0)  # 0-1-0循環
            glow_alpha = int(100 + 100 * pulse)
            glow_radius = int(25 + 10 * pulse)

            # 物品類型顏色
            item_colors = {
                "healing": (255, 100, 100),
                "key": (255, 255, 0),
                "special": (0, 255, 0),
                "clue": (100, 100, 255)
            }
            base_color = item_colors.get(item_type, (255, 255, 255))

            # 繪製光暈
            glow_surface = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(glow_surface, (*base_color, glow_alpha//2),
                              (glow_radius, glow_radius), glow_radius)
            screen.blit(glow_surface, (x - glow_radius, y - glow_radius))

            # 繪製物品圖片（32x32像素，置中）
            sprite_size = 32
            draw_x = x - sprite_size // 2
            draw_y = y - sprite_size // 2
            screen.blit(sprite, (draw_x, draw_y))
            
            return True
        
        return False
    
    def render_item_with_code(self, screen, item, x, y, current_time):
        """🆕 程式繪製物品（備用方法）"""
        item_type = item["type"]

        # 物品光暈效果（呼吸燈）
        pulse = abs((current_time % 2000 - 1000) / 1000.0)  # 0-1-0循環
        glow_alpha = int(100 + 100 * pulse)
        glow_radius = int(25 + 10 * pulse)

        # 物品類型顏色
        item_colors = {
            "healing": (255, 100, 100),
            "key": (255, 255, 0),
            "special": (0, 255, 0),
            "clue": (100, 100, 255)
        }

        base_color = item_colors.get(item_type, (255, 255, 255))

        # 繪製光暈
        glow_surface = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(glow_surface, (*base_color, glow_alpha//2),
                          (glow_radius, glow_radius), glow_radius)
        screen.blit(glow_surface, (x - glow_radius, y - glow_radius))

        # 繪製物品圖示（原本的程式繪製）
        if item_type == "healing":
            # 醫療包/能量包圖示
            if "醫療" in item["name"]:
                # 紅十字醫療包
                pygame.draw.rect(screen, (255, 255, 255), (x-8, y-8, 16, 16))
                pygame.draw.rect(screen, (255, 0, 0), (x-6, y-6, 12, 12))
                pygame.draw.rect(screen, (255, 255, 255), (x-1, y-6, 2, 12))
                pygame.draw.rect(screen, (255, 255, 255), (x-6, y-1, 12, 2))
            else:
                # 能量飲料瓶
                pygame.draw.rect(screen, (0, 150, 255), (x-4, y-10, 8, 20))
                pygame.draw.rect(screen, (100, 200, 255), (x-3, y-8, 6, 3))
                pygame.draw.circle(screen, (255, 255, 255), (x, y-11), 2)

        elif item_type == "key":
            # 鑰匙卡圖示
            pygame.draw.rect(screen, (255, 255, 0), (x-8, y-6, 16, 12))
            pygame.draw.rect(screen, (200, 200, 0), (x-8, y-6, 16, 12), 1)
            pygame.draw.rect(screen, (255, 255, 255), (x-6, y-4, 12, 8))
            pygame.draw.rect(screen, (100, 100, 100), (x-2, y-2, 4, 4))

        elif item_type == "special":
            # 特殊物品（解藥）
            pygame.draw.circle(screen, (0, 255, 0), (x, y), 12)
            pygame.draw.circle(screen, (0, 200, 0), (x, y), 12, 2)
            pygame.draw.circle(screen, (255, 255, 255), (x, y), 8)
            pygame.draw.circle(screen, (0, 255, 0), (x, y), 6)
            # 添加閃爍的十字
            if (current_time // 200) % 2:  # 閃爍效果
                pygame.draw.rect(screen, (255, 255, 255), (x-1, y-6, 2, 12))
                pygame.draw.rect(screen, (255, 255, 255), (x-6, y-1, 12, 2))

        elif item_type == "clue":
            # 線索物品（筆記）
            pygame.draw.rect(screen, (255, 255, 255), (x-6, y-8, 12, 16))
            pygame.draw.rect(screen, (100, 100, 255), (x-6, y-8, 12, 16), 1)
            # 文字線條
            for i in range(3):
                pygame.draw.rect(screen, (100, 100, 255), (x-4, y-6+i*3, 8, 1))

        # 物品名稱
        self.render_item_name(screen, item, x, y)
    
    def render_item_name(self, screen, item, x, y):
        """🆕 渲染物品名稱"""
        # 物品名稱（帶背景）
        name_surface = font_manager.render_text(item["name"], 12, (255, 255, 255))
        name_rect = name_surface.get_rect(center=(x, y - 35))

        # 名稱背景
        bg_rect = name_rect.copy()
        bg_rect.inflate(8, 4)
        bg_surface = pygame.Surface(bg_rect.size, pygame.SRCALPHA)
        bg_surface.fill((0, 0, 0, 150))
        screen.blit(bg_surface, bg_rect)

        screen.blit(name_surface, name_rect)

        # 物品描述（如果有的話）
        if hasattr(item, 'description') and item.get('description'):
            desc_surface = font_manager.render_text(item['description'], 10, (200, 200, 200))
            desc_rect = desc_surface.get_rect(center=(x, y + 25))

            # 描述背景
            desc_bg_rect = desc_rect.copy()
            desc_bg_rect.inflate(6, 2)
            desc_bg_surface = pygame.Surface(desc_bg_rect.size, pygame.SRCALPHA)
            desc_bg_surface.fill((0, 0, 0, 120))
            screen.blit(desc_bg_surface, desc_bg_rect)

            screen.blit(desc_surface, desc_rect)

    def get_item_color(self, item_type):
        """獲取物品類型對應的顏色"""
        colors = {
            "healing": (255, 100, 100),
            "key": (255, 255, 0),
            "special": (0, 255, 0),
            "clue": (100, 100, 255)
        }
        return colors.get(item_type, (255, 255, 255))

    def render_floor_info(self, screen):
        """渲染樓層資訊"""
        current_map = self.floor_maps[self.current_floor]

        # 樓層名稱
        floor_text = f"{current_map['name']}"
        floor_surface = font_manager.render_text(floor_text, 24, (255, 255, 255))
        screen.blit(floor_surface, (10, 10))

        # 樓層數字
        floor_num_text = f"{self.current_floor}F"
        floor_num_surface = font_manager.render_text(floor_num_text, 32, (255, 255, 0))
        screen.blit(floor_num_surface, (screen.get_width() - 80, 10))

        # 🆕 顯示當前樓層物品統計
        if self.current_floor in self.items:
            total_items = len(self.items[self.current_floor])
            collected_count = len([item for item in self.items[self.current_floor]
                                 if f"{self.current_floor}_{item['name']}_{item['x']}_{item['y']}" in self.collected_items])

            item_stats = f"物品: {collected_count}/{total_items}"
            stats_surface = font_manager.render_text(item_stats, 18, (200, 200, 200))
            screen.blit(stats_surface, (10, 40))

        # 🆕 顯示地板渲染狀態
        if self.use_floor_sprites:
            floor_status = "地板: 圖片模式 ✓"
            status_color = (0, 255, 0)
        else:
            floor_status = "地板: 程式繪製"
            status_color = (255, 255, 0)

        status_surface = font_manager.render_text(floor_status, 16, status_color)
        screen.blit(status_surface, (10, 65))

        # 🔧 在除錯模式下顯示戰鬥區域狀態
        if self.debug_show_combat_zones:
            debug_status = "除錯: 戰鬥區域可見"
            debug_color = (255, 100, 100)
        else:
            debug_status = "戰鬥區域: 隱藏"
            debug_color = (100, 255, 100)
        
        debug_surface = font_manager.render_text(debug_status, 16, debug_color)
        screen.blit(debug_surface, (10, 85))

    def toggle_combat_zone_debug(self):
        """🆕 切換戰鬥區域除錯顯示"""
        self.debug_show_combat_zones = not self.debug_show_combat_zones
        status = "開啟" if self.debug_show_combat_zones else "關閉"
        print(f"🔧 戰鬥區域除錯顯示: {status}")
        return self.debug_show_combat_zones

    def reload_stairs_images(self):
        """重新載入樓梯圖片（用於熱更新）"""
        print("🔄 重新載入樓梯圖片...")
        self.stairs_sprites.clear()
        self.load_stairs_images()

    def reload_floor_images(self):
        """🆕 重新載入地板圖片（用於熱更新）"""
        print("🔄 重新載入地板圖片...")
        self.floor_sprites.clear()
        self.load_floor_images()
    
    def reload_shop_images(self):
        """🆕 重新載入商店圖片（用於熱更新）"""
        print("🔄 重新載入商店圖片...")
        self.shop_sprites.clear()
        self.load_shop_images()
    
    def reload_npc_images(self):
        """🆕 重新載入NPC圖片（用於熱更新）"""
        print("🔄 重新載入NPC圖片...")
        self.npc_sprites.clear()
        self.load_npc_images()
    
    def reload_item_images(self):
        """🆕 重新載入物品圖片（用於熱更新）"""
        print("🔄 重新載入物品圖片...")
        self.item_sprites.clear()
        self.load_item_images()

    def get_stairs_info(self, floor=None):
        """獲取樓梯資訊"""
        if floor is None:
            floor = self.current_floor

        if floor not in self.interactions:
            return []

        stairs = [item for item in self.interactions[floor] if item["type"] == "stairs"]
        return stairs

    def debug_print_stairs(self):
        """除錯：印出所有樓梯資訊"""
        print("🪜 樓梯偵錯資訊:")
        print(f"   圖片載入狀態: {self.use_sprites}")
        print(f"   載入的圖片: {list(self.stairs_sprites.keys())}")

        for floor, interactions in self.interactions.items():
            stairs = [item for item in interactions if item["type"] == "stairs"]
            if stairs:
                print(f"   {floor}樓樓梯:")
                for stair in stairs:
                    print(f"     - {stair['direction']}: ({stair['x']}, {stair['y']}) -> {stair.get('target_floor', '?')}樓")

    def debug_print_items(self):
        """🆕 除錯：印出所有物品資訊"""
        print("📦 物品偵錯資訊:")
        for floor, items in self.items.items():
            print(f"   {floor}樓物品:")
            for item in items:
                item_id = f"{floor}_{item['name']}_{item['x']}_{item['y']}"
                status = "已收集" if item_id in self.collected_items else "未收集"
                print(f"     - {item['name']}: ({item['x']}, {item['y']}) [{status}]")

        print(f"   總收集數: {len(self.collected_items)}")

    def debug_print_floor_info(self):
        """🆕 除錯：印出地板資訊"""
        print("🏢 地板偵錯資訊:")
        print(f"   使用圖片渲染: {self.use_floor_sprites}")
        print(f"   載入的地板圖片: {list(self.floor_sprites.keys())}")
        if self.use_floor_sprites:
            for floor_type, sprite in self.floor_sprites.items():
                if sprite:
                    size = sprite.get_size()
                    print(f"     - {floor_type}: {size[0]}x{size[1]} 像素")
    
    def debug_print_shop_info(self):
        """🆕 除錯：印出商店圖片資訊"""
        print("🏪 商店圖片偵錯資訊:")
        print(f"   使用圖片渲染: {self.use_shop_sprites}")
        print(f"   載入的商店圖片: {list(self.shop_sprites.keys())}")
        if self.use_shop_sprites:
            for shop_type, sprite in self.shop_sprites.items():
                if sprite:
                    size = sprite.get_size()
                    print(f"     - {shop_type}: {size[0]}x{size[1]} 像素")
    
    def debug_print_npc_info(self):
        """🆕 除錯：印出NPC圖片資訊"""
        print("👤 NPC圖片偵錯資訊:")
        print(f"   使用圖片渲染: {self.use_npc_sprites}")
        print(f"   載入的NPC圖片: {list(self.npc_sprites.keys())}")
        if self.use_npc_sprites:
            for npc_type, sprite in self.npc_sprites.items():
                if sprite:
                    size = sprite.get_size()
                    print(f"     - {npc_type}: {size[0]}x{size[1]} 像素")
    
    def debug_print_item_info(self):
        """🆕 除錯：印出物品圖片資訊"""
        print("🗝️ 物品圖片偵錯資訊:")
        print(f"   使用圖片渲染: {self.use_item_sprites}")
        print(f"   載入的物品圖片: {list(self.item_sprites.keys())}")
        if self.use_item_sprites:
            for item_type, sprite in self.item_sprites.items():
                if sprite:
                    size = sprite.get_size()
                    print(f"     - {item_type}: {size[0]}x{size[1]} 像素")

    def debug_print_combat_zones(self):
        """🆕 除錯：印出戰鬥區域資訊"""
        print("⚔️ 戰鬥區域偵錯資訊:")
        print(f"   除錯顯示狀態: {self.debug_show_combat_zones}")
        for floor, zones in self.combat_zones.items():
            print(f"   {floor}樓戰鬥區域:")
            for zone in zones:
                print(f"     - {zone['name']}: ({zone['x']}, {zone['y']}) {zone['width']}x{zone['height']}")
                print(f"       敵人類型: {zone.get('enemies', [])}")

    def get_available_items(self, floor=None):
        """🆕 獲取可用物品列表"""
        if floor is None:
            floor = self.current_floor

        if floor not in self.items:
            return []

        available_items = []
        for item in self.items[floor]:
            item_id = f"{floor}_{item['name']}_{item['x']}_{item['y']}"
            if item_id not in self.collected_items:
                available_items.append(item)

        return available_items

    def reset_items(self):
        """🆕 重置所有物品收集狀態"""
        self.collected_items.clear()
        print("🔄 已重置所有物品收集狀態")