import pygame
from font_manager import font_manager

class UI:
    def __init__(self, screen):
        self.screen = screen
        self.screen_width, self.screen_height = screen.get_size()
        
        # 使用字體管理器
        self.font_large = font_manager.get_font(32)
        self.font_medium = font_manager.get_font(24)
        self.font_small = font_manager.get_font(18)
        
        # UI狀態
        self.show_inventory = False
        self.show_map = False
        self.dialogue_active = False
        self.dialogue_data = None
        self.dialogue_text = ""
        self.dialogue_options = []
        self.selected_option = 0
        
        # 對話框設定
        self.dialogue_box_height = 150
        self.dialogue_box_y = self.screen_height - self.dialogue_box_height - 10
        
        # 訊息顯示
        self.message_display_time = 0
        self.current_message = ""
        
        # 對話狀態管理
        self.dialogue_step = 0  # 對話進度
        self.max_dialogue_steps = 1  # 最大對話步數
    
    def toggle_inventory(self):
        self.show_inventory = not self.show_inventory
        if self.show_inventory:
            self.show_map = False
    
    def toggle_map(self):
        self.show_map = not self.show_map
        if self.show_map:
            self.show_inventory = False
    
    def start_dialogue(self, interaction_data):
        self.dialogue_active = True
        self.dialogue_data = interaction_data
        self.dialogue_step = 0
        
        if interaction_data["type"] == "shop":
            self.setup_shop_dialogue(interaction_data)
        elif interaction_data["type"] == "npc":
            self.setup_npc_dialogue(interaction_data)
        
        print(f"對話開始: {interaction_data['name']}")  # 除錯訊息
    
    def setup_shop_dialogue(self, shop_data):
        shop_name = shop_data["name"]
        
        # 根據不同商店設定對話內容
        if shop_data["id"] == "A":  # 7-11
            self.dialogue_text = "歡迎來到7-11！雖然外面很危險，但這裡還算安全。需要什麼嗎？"
            self.dialogue_options = [
                "購買醫療用品",
                "詢問情況",
                "離開"
            ]
        elif shop_data["id"] == "B":  # Subway
            self.dialogue_text = "Subway已經沒有新鮮食材了，但還有一些罐頭..."
            self.dialogue_options = [
                "購買罐頭食品",
                "詢問逃生路線",
                "離開"
            ]
        elif shop_data["id"] == "C":  # 茶壜
            self.dialogue_text = "茶壜的飲料機還在運作，但店員已經不見了..."
            self.dialogue_options = [
                "搜尋飲料",
                "查看櫃台",
                "離開"
            ]
        elif shop_data["id"] == "L":  # 咖啡廳
            self.dialogue_text = "這裡可能有研究員留下的線索..."
            self.dialogue_options = [
                "仔細搜查",
                "查看櫃台",
                "離開"
            ]
        else:
            # 其他商店的通用對話
            self.dialogue_text = f"這是{shop_name}，看起來已經荒廢了..."
            self.dialogue_options = [
                "搜尋物品",
                "查看周圍",
                "離開"
            ]
        
        self.selected_option = 0
        print(f"🏪 商店對話設定完成: {shop_name}, 選項數: {len(self.dialogue_options)}")
    
    def setup_npc_dialogue(self, npc_data):
        npc_id = npc_data["id"]
        
        if npc_id == "npc1":  # 驚慌學生
            self.dialogue_text = "救命！外面到處都是殭屍！我看到研究生們往樓上跑了！"
            self.dialogue_options = [
                "冷靜一點，告訴我更多",
                "樓上有什麼？",
                "離開"
            ]
        elif npc_id == "npc2":  # 受傷職員
            self.dialogue_text = "我被咬了...但還沒完全感染。聽說三樓有解藥..."
            self.dialogue_options = [
                "解藥在哪裡？",
                "你還好嗎？",
                "離開"
            ]
        elif npc_id == "npc3":  # 神秘研究員
            self.dialogue_text = "你也在找解藥嗎？需要特殊鑰匙卡才能進入實驗室..."
            self.dialogue_options = [
                "鑰匙卡在哪？",
                "實驗室在哪裡？",
                "離開"
            ]
        elif npc_id == "npc4":  # 最後的研究者
            self.dialogue_text = "你找到了！解藥就在這裡，但要小心，外面的情況更糟了..."
            self.dialogue_options = [
                "拿取解藥",
                "詢問使用方法",
                "離開"
            ]
        
        self.selected_option = 0
    
    def select_dialogue_option(self, option_index):
        if 0 <= option_index < len(self.dialogue_options):
            self.selected_option = option_index
            selected_text = self.dialogue_options[option_index]
            print(f"選擇選項 {option_index + 1}: {selected_text}")  # 除錯訊息
            self.execute_dialogue_choice()
    
    def execute_dialogue_choice(self):
        if not self.dialogue_data:
            return
        
        option_text = self.dialogue_options[self.selected_option]
        print(f"執行選項: {option_text}")  # 除錯訊息
        
        # 根據選擇執行相應行動
        if "購買" in option_text:
            self.show_message("購買成功！")
            self.end_dialogue()
        elif "搜查" in option_text or "搜尋" in option_text:
            self.show_message("找到了一些有用的物品！")
            self.end_dialogue()
        elif "拿取解藥" in option_text:
            self.show_message("恭喜！你找到了解藥！")
            self.end_dialogue()
        elif "離開" in option_text:
            self.end_dialogue()
        elif "冷靜一點" in option_text:
            self.show_message("學生: 我看到他們拿著什麼東西往樓上跑...")
            self.end_dialogue()
        elif "樓上有什麼" in option_text:
            self.show_message("學生: 聽說研究生們在三樓做實驗...")
            self.end_dialogue()
        elif "解藥在哪" in option_text:
            self.show_message("職員: 三樓...咖啡廳附近...快去...")
            self.end_dialogue()
        elif "你還好嗎" in option_text:
            self.show_message("職員: 還撐得住...你快去找解藥...")
            self.end_dialogue()
        elif "鑰匙卡在哪" in option_text:
            self.show_message("研究員: 應該在二樓的某個商店裡...")
            self.end_dialogue()
        elif "實驗室在哪裡" in option_text:
            self.show_message("研究員: 三樓需要鑰匙卡才能進入...")
            self.end_dialogue()
        elif "詢問使用方法" in option_text:
            self.show_message("研究者: 直接使用就行了，它會拯救所有人...")
            self.end_dialogue()
        else:
            # 其他選項也結束對話
            self.show_message(f"你選擇了：{option_text}")
            self.end_dialogue()
    
    def end_dialogue(self):
        """結束對話"""
        print("對話結束")  # 除錯訊息
        self.dialogue_active = False
        self.dialogue_data = None
        self.dialogue_text = ""
        self.dialogue_options = []
        self.selected_option = 0
    
    def continue_dialogue(self):
        if self.dialogue_active:
            print("繼續對話")  # 除錯訊息
            # 如果還有更多對話內容，繼續顯示
            # 否則結束對話
            self.end_dialogue()
    
    def show_message(self, message):
        self.current_message = message
        self.message_display_time = 180  # 3秒 (60fps * 3)
    
    def render(self, game_state, player, inventory):
        # 渲染HUD
        self.render_hud(game_state, player)
        
        # 渲染訊息
        self.render_messages(game_state)
        
        # 渲染對話框
        if self.dialogue_active:
            self.render_dialogue()
        
        # 渲染背包
        if self.show_inventory:
            self.render_inventory(inventory)
        
        # 渲染地圖
        if self.show_map:
            self.render_mini_map()
        
        # 更新訊息計時器
        if self.message_display_time > 0:
            self.message_display_time -= 1
    
    def update_messages(self):
        """更新訊息顯示"""
        if self.message_display_time > 0:
            self.message_display_time -= 1
    
    def render_hud(self, game_state, player):
        # 血量條
        hp_ratio = game_state.player_stats["hp"] / game_state.player_stats["max_hp"]
        hp_bar_width = 200
        hp_bar_height = 20
        
        # 血量條背景
        hp_bg_rect = pygame.Rect(10, self.screen_height - 40, hp_bar_width, hp_bar_height)
        pygame.draw.rect(self.screen, (100, 100, 100), hp_bg_rect)
        
        # 血量條
        hp_rect = pygame.Rect(10, self.screen_height - 40, hp_bar_width * hp_ratio, hp_bar_height)
        hp_color = (255, 0, 0) if hp_ratio < 0.3 else (255, 255, 0) if hp_ratio < 0.6 else (0, 255, 0)
        pygame.draw.rect(self.screen, hp_color, hp_rect)
        
        # 血量文字
        hp_text = f"HP: {game_state.player_stats['hp']}/{game_state.player_stats['max_hp']}"
        hp_surface = font_manager.render_text(hp_text, 18, (255, 255, 255))
        self.screen.blit(hp_surface, (220, self.screen_height - 35))
        
        # 等級和經驗值
        level_text = f"Lv.{game_state.player_stats['level']}"
        level_surface = font_manager.render_text(level_text, 18, (255, 255, 255))
        self.screen.blit(level_surface, (10, self.screen_height - 65))
        
        exp_text = f"EXP: {game_state.player_stats['exp']}/{game_state.player_stats['level'] * 100}"
        exp_surface = font_manager.render_text(exp_text, 18, (255, 255, 255))
        self.screen.blit(exp_surface, (80, self.screen_height - 65))
        
        # 操作提示
        if not self.dialogue_active:
            controls = [
                "方向鍵: 移動",
                "空白鍵: 互動",
                "I: 背包",
                "M: 地圖"
            ]
            
            for i, control in enumerate(controls):
                control_surface = font_manager.render_text(control, 18, (200, 200, 200))
                self.screen.blit(control_surface, (self.screen_width - 150, 10 + i * 20))
    
    def render_messages(self, game_state):
        # 渲染遊戲訊息
        messages = game_state.get_current_messages()
        for i, message in enumerate(messages):
            message_surface = font_manager.render_text(message, 24, (255, 255, 0))
            self.screen.blit(message_surface, (10, 50 + i * 30))
        
        # 渲染臨時訊息
        if self.message_display_time > 0:
            message_surface = font_manager.render_text(self.current_message, 24, (0, 255, 255))
            message_rect = message_surface.get_rect(center=(self.screen_width//2, 100))
            
            # 訊息背景
            bg_rect = message_rect.copy()
            bg_rect.inflate(20, 10)
            pygame.draw.rect(self.screen, (0, 0, 0, 180), bg_rect)
            
            self.screen.blit(message_surface, message_rect)
    
    def render_dialogue(self):
        # 對話框背景
        dialogue_rect = pygame.Rect(10, self.dialogue_box_y, 
                                  self.screen_width - 20, self.dialogue_box_height)
        pygame.draw.rect(self.screen, (0, 0, 0, 200), dialogue_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), dialogue_rect, 2)
        
        # 對話文字
        y_offset = self.dialogue_box_y + 10
        
        # 分行顯示對話文字
        words = self.dialogue_text.split()
        lines = []
        current_line = ""
        
        for word in words:
            test_line = current_line + word + " "
            if self.font_medium.size(test_line)[0] < self.screen_width - 40:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line.strip())
                current_line = word + " "
        
        if current_line:
            lines.append(current_line.strip())
        
        for line in lines:
            text_surface = self.font_medium.render(line, True, (255, 255, 255))
            self.screen.blit(text_surface, (20, y_offset))
            y_offset += 25
        
        # 選項
        y_offset += 10
        for i, option in enumerate(self.dialogue_options):
            color = (255, 255, 0) if i == self.selected_option else (200, 200, 200)
            option_text = f"{i+1}. {option}"
            option_surface = font_manager.render_text(option_text, 18, color)
            self.screen.blit(option_surface, (30, y_offset))
            y_offset += 25
        
        # 操作提示
        hint_text = "按 1/2/3 選擇選項，按 ESC 退出對話"
        hint_surface = font_manager.render_text(hint_text, 14, (150, 150, 150))
        self.screen.blit(hint_surface, (20, self.dialogue_box_y + self.dialogue_box_height - 25))
    
    def render_inventory(self, inventory):
        # 背包視窗
        inv_width = 400
        inv_height = 300
        inv_x = (self.screen_width - inv_width) // 2
        inv_y = (self.screen_height - inv_height) // 2
        
        inv_rect = pygame.Rect(inv_x, inv_y, inv_width, inv_height)
        pygame.draw.rect(self.screen, (50, 50, 50, 240), inv_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), inv_rect, 2)
        
        # 標題
        title_surface = self.font_large.render("背包", True, (255, 255, 255))
        title_rect = title_surface.get_rect(center=(self.screen_width//2, inv_y + 30))
        self.screen.blit(title_surface, title_rect)
        
        # 物品列表
        y_offset = inv_y + 60
        items = inventory.get_items()
        
        if not items:
            no_items_surface = self.font_medium.render("背包是空的", True, (200, 200, 200))
            no_items_rect = no_items_surface.get_rect(center=(self.screen_width//2, y_offset + 50))
            self.screen.blit(no_items_surface, no_items_rect)
        else:
            for item in items:
                item_text = f"{item['name']} x{item.get('quantity', 1)}"
                item_surface = self.font_medium.render(item_text, True, (255, 255, 255))
                self.screen.blit(item_surface, (inv_x + 20, y_offset))
                y_offset += 30
        
        # 關閉提示
        close_text = "按 I 關閉"
        close_surface = self.font_small.render(close_text, True, (200, 200, 200))
        close_rect = close_surface.get_rect(center=(self.screen_width//2, inv_y + inv_height - 20))
        self.screen.blit(close_surface, close_rect)
    
    def render_mini_map(self):
        # 小地圖
        map_width = 300
        map_height = 200
        map_x = self.screen_width - map_width - 10
        map_y = 10
        
        map_rect = pygame.Rect(map_x, map_y, map_width, map_height)
        pygame.draw.rect(self.screen, (0, 0, 0, 200), map_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), map_rect, 2)
        
        # 標題
        title_surface = self.font_medium.render("地圖", True, (255, 255, 255))
        self.screen.blit(title_surface, (map_x + 10, map_y + 10))
        
        # 簡化的樓層顯示
        floor_info = [
            "1F: 7-11, Subway, 茶壜...",
            "2F: 和食宣, 素怡沅...",
            "3F: 咖啡廳, 討論室, 展覽"
        ]
        
        y_offset = map_y + 40
        for i, info in enumerate(floor_info):
            color = (255, 255, 0) if i + 1 == 1 else (200, 200, 200)  # 假設當前在1樓
            info_surface = self.font_small.render(info, True, color)
            self.screen.blit(info_surface, (map_x + 10, y_offset))
            y_offset += 25
        
        # 關閉提示
        close_text = "按 M 關閉"
        close_surface = self.font_small.render(close_text, True, (200, 200, 200))
        self.screen.blit(close_surface, (map_x + 10, map_y + map_height - 25))