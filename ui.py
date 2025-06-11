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
        self.dialogue_step = 0
        self.max_dialogue_steps = 1
        
        # 遊戲狀態追蹤
        self.has_keycard = False
        self.has_antidote = False
        self.game_completed = False
        self.game_over = False
        
        # 玩家初始位置記錄 (用於傳送)
        self.player_reference = None
        self.inventory_reference = None
        self._game_state_ref = None  # 遊戲狀態參考
    
    def set_player_reference(self, player):
        """設定玩家物件參考，用於修改位置"""
        self.player_reference = player
    
    def is_any_ui_open(self):
        """檢查是否有任何UI開啟"""
        return self.show_inventory or self.show_map or self.dialogue_active

    def close_all_ui(self):
        """關閉所有UI"""
        self.show_inventory = False
        self.show_map = False
        self.dialogue_active = False
        print("🚪 關閉所有UI")

    def get_ui_status(self):
        """獲取UI狀態資訊"""
        return {
            "inventory": self.show_inventory,
            "map": self.show_map,
            "dialogue": self.dialogue_active,
            "any_open": self.is_any_ui_open()
        }
    
    def set_inventory_reference(self, inventory):
        """設定背包物件參考，用於檢查和消耗物品"""
        self.inventory_reference = inventory
    
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
        
        print(f"對話開始: {interaction_data['name']}")
    
    def setup_shop_dialogue(self, shop_data):
        shop_name = shop_data["name"]
        
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
            if self.has_keycard:
                self.dialogue_text = "你使用鑰匙卡進入了秘密區域，這裡可能有解藥..."
                self.dialogue_options = [
                    "深入搜查",
                    "查看實驗設備",
                    "離開"
                ]
            else:
                self.dialogue_text = "這裡需要特殊的鑰匙卡才能進入深處..."
                self.dialogue_options = [
                    "仔細搜查",
                    "查看櫃台",
                    "離開"
                ]
        else:
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
                "給予醫療用品",
                "離開"
            ]
        elif npc_id == "npc3":  # 神秘研究員
            self.dialogue_text = "你也在找解藥嗎？需要特殊鑰匙卡才能進入實驗室..."
            self.dialogue_options = [
                "鑰匙卡在哪？",
                "實驗室在哪裡？",
                "我可以幫你什麼？",
                "離開"
            ]
        elif npc_id == "npc4":  # 最後的研究者
            if self.has_antidote:
                self.dialogue_text = "太好了！你已經有解藥了，現在可以拯救所有人！"
                self.dialogue_options = [
                    "如何使用解藥？",
                    "還有其他倖存者嗎？",
                    "離開"
                ]
            else:
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
            print(f"選擇選項 {option_index + 1}: {selected_text}")
            self.execute_dialogue_choice()
    
    def check_has_medical_item(self, inventory):
        """檢查背包中是否有醫療用品"""
        if hasattr(inventory, 'get_items'):
            items = inventory.get_items()
            for item in items:
                if "醫療" in item.get('name', '') or "藥" in item.get('name', '') or "治療" in item.get('name', ''):
                    return item.get('quantity', 0) > 0
        return False
    
    def consume_medical_item(self, inventory):
        """消耗一個醫療用品"""
        if hasattr(inventory, 'get_items') and hasattr(inventory, 'remove_item'):
            items = inventory.get_items()
            for item in items:
                if "醫療" in item.get('name', '') or "藥" in item.get('name', '') or "治療" in item.get('name', ''):
                    if item.get('quantity', 0) > 0:
                        inventory.remove_item(item['name'], 1)
                        print(f"消耗了 {item['name']}")
                        return True
        return False
    
    def execute_dialogue_choice(self):
        if not self.dialogue_data:
            return
        
        option_text = self.dialogue_options[self.selected_option]
        print(f"執行選項: {option_text}")
        
        # 獲取遊戲狀態參考和背包參考
        game_state = self.get_game_state()
        inventory = self.get_inventory()  # 需要新增這個方法來獲取背包
        
        # 根據選擇執行相應行動
        if "購買醫療用品" in option_text:
            if game_state.player_stats["hp"] < game_state.player_stats["max_hp"]:
                game_state.player_stats["hp"] = min(
                    game_state.player_stats["max_hp"],
                    game_state.player_stats["hp"] + 30
                )
                game_state.player_stats["exp"] += 10
                self.show_message("購買成功！HP +30, EXP +10")
            else:
                self.show_message("你的血量已滿！")
            self.end_dialogue()
            
        elif "購買罐頭食品" in option_text:
            game_state.player_stats["hp"] = min(
                game_state.player_stats["max_hp"],
                game_state.player_stats["hp"] + 20
            )
            game_state.player_stats["exp"] += 5
            self.show_message("食物補充！HP +20, EXP +5")
            self.end_dialogue()
            
        elif "搜尋飲料" in option_text:
            game_state.player_stats["hp"] = min(
                game_state.player_stats["max_hp"],
                game_state.player_stats["hp"] + 15
            )
            game_state.player_stats["exp"] += 8
            self.show_message("找到能量飲料！HP +15, EXP +8")
            self.end_dialogue()
            
        elif "深入搜查" in option_text and self.has_keycard:
            if not self.has_antidote:
                self.has_antidote = True
                game_state.player_stats["exp"] += 100
                game_state.player_stats["level"] += 1
                self.show_message("找到解藥！等級提升！經驗值大幅增加！")
                self.check_victory_condition(game_state)
            else:
                self.show_message("你已經有解藥了！")
            self.end_dialogue()
            
        elif "仔細搜查" in option_text or "搜查" in option_text or "搜尋物品" in option_text:
            import random
            if random.random() < 0.3:  # 30% 機率找到鑰匙卡
                if not self.has_keycard:
                    self.has_keycard = True
                    game_state.player_stats["exp"] += 50
                    self.show_message("找到了鑰匙卡！這應該能開啟特殊區域！EXP +50")
                else:
                    game_state.player_stats["exp"] += 15
                    self.show_message("找到了一些有用的物品！EXP +15")
            else:
                game_state.player_stats["exp"] += 10
                self.show_message("搜查完畢，找到了一些小物品。EXP +10")
            self.end_dialogue()
            
        elif "拿取解藥" in option_text:
            if game_state.player_stats["level"] >= 3:  # 需要等級3以上才能安全拿取
                self.has_antidote = True
                game_state.player_stats["exp"] += 100
                game_state.player_stats["level"] += 1
                self.show_message("成功取得解藥！等級提升！")
                self.check_victory_condition(game_state)
            else:
                game_state.player_stats["hp"] -= 20
                self.show_message("等級不足！受到傷害！HP -20")
                self.check_game_over(game_state)
            self.end_dialogue()
            
        elif "離開" in option_text:
            self.end_dialogue()
            
        elif "冷靜一點" in option_text:
            game_state.player_stats["exp"] += 5
            self.show_message("學生: 我看到他們拿著什麼東西往樓上跑... (EXP +5)")
            self.end_dialogue()
            
        elif "樓上有什麼" in option_text:
            game_state.player_stats["exp"] += 5
            self.show_message("學生: 聽說研究生們在三樓做實驗... (EXP +5)")
            self.end_dialogue()
            
        elif "解藥在哪" in option_text:
            game_state.player_stats["exp"] += 10
            self.show_message("職員: 三樓...咖啡廳附近...快去... (EXP +10)")
            self.end_dialogue()
            
        elif "你還好嗎" in option_text:
            game_state.player_stats["exp"] += 5
            self.show_message("職員: 還撐得住...你快去找解藥... (EXP +5)")
            self.end_dialogue()
            
        elif "給予醫療用品" in option_text:
            # 檢查玩家是否有醫療用品（這裡假設背包中有醫療用品）
            has_medical_item = self.check_has_medical_item(inventory)
            
            if has_medical_item:
                # 消耗醫療用品來幫助別人
                self.consume_medical_item(inventory)
                game_state.player_stats["exp"] += 25
                self.show_message("你給了職員醫療用品！EXP +25, 獲得重要情報！")
                # 傳送到3樓咖啡廳附近
                if self.player_reference:
                    self.player_reference.teleport_to_coordinates(400, 200, 3)
                    self.show_message("職員告訴了你秘密通道的位置！你被傳送到3樓！")
            else:
                self.show_message("你沒有醫療用品可以給予！先去商店購買一些吧。")
            self.end_dialogue()
            
        elif "鑰匙卡在哪" in option_text:
            game_state.player_stats["exp"] += 15
            self.show_message("研究員: 應該在二樓的某個商店裡... (EXP +15)")
            # 提示傳送到2樓
            if self.player_reference:
                self.player_reference.x = 300
                self.player_reference.y = 150
                self.show_message("研究員指引你到2樓搜尋！")
            self.end_dialogue()
            
        elif "實驗室在哪裡" in option_text:
            game_state.player_stats["exp"] += 15
            self.show_message("研究員: 三樓需要鑰匙卡才能進入... (EXP +15)")
            self.end_dialogue()
            
        elif "我可以幫你什麼" in option_text:
            if game_state.player_stats["level"] >= 2:
                game_state.player_stats["exp"] += 30
                self.has_keycard = True
                self.show_message("研究員感謝你的幫助，給了你鑰匙卡！EXP +30")
            else:
                game_state.player_stats["exp"] += 10
                self.show_message("研究員: 你還太弱了，先去提升實力吧... (EXP +10)")
            self.end_dialogue()
            
        elif "詢問使用方法" in option_text:
            game_state.player_stats["exp"] += 20
            self.show_message("研究者: 直接使用就行了，它會拯救所有人... (EXP +20)")
            self.end_dialogue()
            
        elif "如何使用解藥" in option_text:
            if self.has_antidote:
                self.show_message("研究者: 在建築物頂樓使用，它會擴散到整個區域！")
                # 傳送到頂樓
                if self.player_reference:
                    self.player_reference.x = 500
                    self.player_reference.y = 50
                    self.show_message("你被帶到了頂樓！準備拯救所有人！")
                self.check_victory_condition(game_state)
            self.end_dialogue()
            
        else:
            # 其他選項也結束對話
            if "離開" in option_text:
                # 確保離開選項總是有效
                self.show_message("你離開了對話。")
            else:
                game_state.player_stats["exp"] += 2
                self.show_message(f"你選擇了：{option_text} (EXP +2)")
            self.end_dialogue()
        
        # 檢查升級
        self.check_level_up(game_state)
    
    def get_inventory(self):
        """獲取背包物件 - 需要根據實際的遊戲架構來修改"""
        # 返回已設定的背包參考
        return self.inventory_reference
    
    def get_game_state(self):
        """獲取遊戲狀態 - 返回真正的遊戲狀態"""
        if hasattr(self, '_game_state_ref') and self._game_state_ref:
            return self._game_state_ref
        else:
            # 如果沒有設定遊戲狀態參考，使用假的狀態
            print("⚠️ 警告：使用假的遊戲狀態，請確保已設定 game_state_reference")
            class MockGameState:
                def __init__(self):
                    self.player_stats = {
                        "hp": 80,
                        "max_hp": 100,
                        "level": 1,
                        "exp": 0
                    }
            return MockGameState()
    
    def check_level_up(self, game_state):
        """檢查是否升級"""
        required_exp = game_state.player_stats["level"] * 100
        if game_state.player_stats["exp"] >= required_exp:
            game_state.player_stats["level"] += 1
            game_state.player_stats["exp"] -= required_exp
            game_state.player_stats["max_hp"] += 20
            game_state.player_stats["hp"] = game_state.player_stats["max_hp"]  # 升級時回滿血
            self.show_message(f"恭喜升級到 Lv.{game_state.player_stats['level']}！血量上限增加！")
    
    def check_victory_condition(self, game_state):
        """檢查勝利條件"""
        if (self.has_antidote and 
            game_state.player_stats["level"] >= 3 and 
            game_state.player_stats["hp"] >= 50):
            self.game_completed = True
            self.show_message("🎉 恭喜！你成功找到解藥並拯救了所有人！遊戲完成！")
        elif self.has_antidote:
            self.show_message("你有解藥了！但還需要更強的實力才能完成任務...")
    
    def check_game_over(self, game_state):
        """檢查遊戲結束條件"""
        if game_state.player_stats["hp"] <= 0:
            self.game_over = True
            self.show_message("💀 你倒下了...遊戲結束！")
    
    def end_dialogue(self):
        """結束對話"""
        print("對話結束")
        self.dialogue_active = False
        self.dialogue_data = None
        self.dialogue_text = ""
        self.dialogue_options = []
        self.selected_option = 0
    
    def continue_dialogue(self):
        if self.dialogue_active:
            print("繼續對話")
            self.end_dialogue()
    
    def show_message(self, message):
        self.current_message = message
        self.message_display_time = 180  # 3秒 (60fps * 3)
    
    def render(self, game_state, player, inventory):
        # 檢查遊戲狀態
        if self.game_over:
            self.render_game_over()
            return
        elif self.game_completed:
            self.render_victory()
            return
        
        # 正常遊戲渲染
        self.render_hud(game_state, player)
        self.render_messages(game_state)
        
        if self.dialogue_active:
            self.render_dialogue()
        
        if self.show_inventory:
            self.render_inventory(inventory)
        
        if self.show_map:
            self.render_mini_map()
        
        if self.message_display_time > 0:
            self.message_display_time -= 1
    
    def render_game_over(self):
        """渲染遊戲結束畫面"""
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        game_over_text = self.font_large.render("GAME OVER", True, (255, 0, 0))
        game_over_rect = game_over_text.get_rect(center=(self.screen_width//2, self.screen_height//2 - 50))
        self.screen.blit(game_over_text, game_over_rect)
        
        restart_text = self.font_medium.render("按 R 重新開始", True, (255, 255, 255))
        restart_rect = restart_text.get_rect(center=(self.screen_width//2, self.screen_height//2 + 50))
        self.screen.blit(restart_text, restart_rect)
    
    def render_victory(self):
        """渲染勝利畫面"""
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(200)
        overlay.fill((0, 50, 0))
        self.screen.blit(overlay, (0, 0))
        
        victory_text = self.font_large.render("VICTORY!", True, (0, 255, 0))
        victory_rect = victory_text.get_rect(center=(self.screen_width//2, self.screen_height//2 - 50))
        self.screen.blit(victory_text, victory_rect)
        
        complete_text = self.font_medium.render("你成功拯救了所有人！", True, (255, 255, 255))
        complete_rect = complete_text.get_rect(center=(self.screen_width//2, self.screen_height//2))
        self.screen.blit(complete_text, complete_rect)
        
        restart_text = self.font_medium.render("按 R 重新開始", True, (255, 255, 255))
        restart_rect = restart_text.get_rect(center=(self.screen_width//2, self.screen_height//2 + 50))
        self.screen.blit(restart_text, restart_rect)
    
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
        
        required_exp = game_state.player_stats['level'] * 100
        exp_text = f"EXP: {game_state.player_stats['exp']}/{required_exp}"
        exp_surface = font_manager.render_text(exp_text, 18, (255, 255, 255))
        self.screen.blit(exp_surface, (80, self.screen_height - 65))
        
        # 道具狀態
        item_y = 10
        if self.has_keycard:
            keycard_text = "🔑 鑰匙卡"
            keycard_surface = font_manager.render_text(keycard_text, 18, (255, 255, 0))
            self.screen.blit(keycard_surface, (10, item_y))
            item_y += 25
        
        if self.has_antidote:
            antidote_text = "💉 解藥"
            antidote_surface = font_manager.render_text(antidote_text, 18, (0, 255, 0))
            self.screen.blit(antidote_surface, (10, item_y))
        
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
        messages = game_state.get_current_messages() if hasattr(game_state, 'get_current_messages') else []
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
        items = inventory.get_items() if hasattr(inventory, 'get_items') else []
        
        # 顯示特殊道具
        special_items = []
        if self.has_keycard:
            special_items.append("🔑 特殊鑰匙卡")
        if self.has_antidote:
            special_items.append("💉 解藥")
        
        all_items = special_items + [f"{item['name']} x{item.get('quantity', 1)}" for item in items]
        
        if not all_items:
            no_items_surface = self.font_medium.render("背包是空的", True, (200, 200, 200))
            no_items_rect = no_items_surface.get_rect(center=(self.screen_width//2, y_offset + 50))
            self.screen.blit(no_items_surface, no_items_rect)
        else:
            for item in all_items:
                item_surface = self.font_medium.render(item, True, (255, 255, 255))
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
        
        # 樓層資訊
        floor_info = [
            "1F: 7-11, Subway, 茶壜...",
            "2F: 和食宣, 素怡沅...",
            "3F: 咖啡廳, 討論室, 展覽",
            "頂樓: 最終目標"
        ]
        
        y_offset = map_y + 40
        for i, info in enumerate(floor_info):
            color = (255, 255, 0) if i + 1 == 1 else (200, 200, 200)  # 假設當前在1樓
            info_surface = self.font_small.render(info, True, color)
            self.screen.blit(info_surface, (map_x + 10, y_offset))
            y_offset += 25
        
        # 任務進度
        progress_text = "任務進度:"
        progress_surface = self.font_small.render(progress_text, True, (255, 255, 0))
        self.screen.blit(progress_surface, (map_x + 10, y_offset + 10))
        y_offset += 25
        
        tasks = [
            f"鑰匙卡: {'✓' if self.has_keycard else '✗'}",
            f"解藥: {'✓' if self.has_antidote else '✗'}",
            f"任務完成: {'✓' if self.game_completed else '✗'}"
        ]
        
        for task in tasks:
            color = (0, 255, 0) if '✓' in task else (255, 100, 100)
            task_surface = self.font_small.render(task, True, color)
            self.screen.blit(task_surface, (map_x + 20, y_offset))
            y_offset += 20
        
        # 關閉提示
        close_text = "按 M 關閉"
        close_surface = self.font_small.render(close_text, True, (200, 200, 200))
        self.screen.blit(close_surface, (map_x + 10, map_y + map_height - 25))
    
    def reset_game(self):
        """重置遊戲狀態"""
        self.has_keycard = False
        self.has_antidote = False
        self.game_completed = False
        self.game_over = False
        self.dialogue_active = False
        self.show_inventory = False
        self.show_map = False
        self.message_display_time = 0
        self.current_message = ""
        print("遊戲狀態已重置")