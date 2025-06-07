# ui.py - UI管理系統
import pygame

class UIManager:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 24)
        self.big_font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 18)
        
        # UI顏色
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GRAY = (128, 128, 128)
        self.GREEN = (0, 255, 0)
        self.RED = (255, 0, 0)
        self.YELLOW = (255, 255, 0)
        self.BLUE = (0, 0, 255)
        
        # UI區域
        self.text_box_rect = pygame.Rect(50, 400, 700, 150)
        self.status_rect = pygame.Rect(10, 10, 200, 100)
    
    def render_exploration_ui(self):
        """渲染探索界面UI"""
        # 渲染狀態欄
        pygame.draw.rect(self.screen, self.BLACK, self.status_rect)
        pygame.draw.rect(self.screen, self.WHITE, self.status_rect, 2)
        
        # 渲染控制提示
        help_text = [
            "方向鍵: 移動",
            "Enter: 互動",
            "I: 背包"
        ]
        
        for i, text in enumerate(help_text):
            text_surface = self.small_font.render(text, True, self.WHITE)
            self.screen.blit(text_surface, (15, 15 + i * 20))
    
    def render_story_ui(self, story_event):
        """渲染劇情UI"""
        if not story_event:
            return
        
        # 渲染對話框背景
        pygame.draw.rect(self.screen, self.BLACK, self.text_box_rect)
        pygame.draw.rect(self.screen, self.WHITE, self.text_box_rect, 3)
        
        # 渲染標題
        if "title" in story_event:
            title_surface = self.big_font.render(story_event["title"], True, self.YELLOW)
            self.screen.blit(title_surface, (self.text_box_rect.x + 10, self.text_box_rect.y + 10))
        
        # 渲染劇情文字
        if "text" in story_event:
            text_lines = self.wrap_text(story_event["text"], self.text_box_rect.width - 20)
            for i, line in enumerate(text_lines):
                text_surface = self.font.render(line, True, self.WHITE)
                self.screen.blit(text_surface, (self.text_box_rect.x + 10, self.text_box_rect.y + 50 + i * 25))
        
        # 渲染選項
        if "choices" in story_event:
            choices_y = self.text_box_rect.y + 100
            for i, choice in enumerate(story_event["choices"]):
                choice_text = f"{i+1}. {choice['text']}"
                text_surface = self.font.render(choice_text, True, self.GREEN)
                self.screen.blit(text_surface, (self.text_box_rect.x + 10, choices_y + i * 25))
    
    def render_combat_ui(self, combat_data):
        """渲染戰鬥UI"""
        if not combat_data:
            return
        
        # 清除背景
        self.screen.fill(self.BLACK)
        
        # 渲染敵人信息
        enemy = combat_data["enemy"]
        enemy_text = f"敵人: {enemy['name']}"
        enemy_hp_text = f"HP: {enemy['hp']}/{enemy['max_hp']}"
        
        enemy_surface = self.big_font.render(enemy_text, True, self.RED)
        enemy_hp_surface = self.font.render(enemy_hp_text, True, self.WHITE)
        
        self.screen.blit(enemy_surface, (50, 50))
        self.screen.blit(enemy_hp_surface, (50, 90))
        
        # 渲染敵人血條
        enemy_hp_bar_rect = pygame.Rect(50, 120, 300, 20)
        enemy_hp_percent = enemy['hp'] / enemy['max_hp']
        enemy_hp_fill = pygame.Rect(50, 120, int(300 * enemy_hp_percent), 20)
        
        pygame.draw.rect(self.screen, self.GRAY, enemy_hp_bar_rect)
        pygame.draw.rect(self.screen, self.RED, enemy_hp_fill)
        pygame.draw.rect(self.screen, self.WHITE, enemy_hp_bar_rect, 2)
        
        # 渲染玩家信息
        player = combat_data["player"]
        player_text = f"玩家 HP: {player['hp']}/{player['max_hp']}"
        player_surface = self.font.render(player_text, True, self.GREEN)
        self.screen.blit(player_surface, (450, 90))
        
        # 渲染玩家血條
        player_hp_bar_rect = pygame.Rect(450, 120, 300, 20)
        player_hp_percent = player['hp'] / player['max_hp'] if player['max_hp'] > 0 else 0
        player_hp_fill = pygame.Rect(450, 120, int(300 * player_hp_percent), 20)
        
        pygame.draw.rect(self.screen, self.GRAY, player_hp_bar_rect)
        pygame.draw.rect(self.screen, self.GREEN, player_hp_fill)
        pygame.draw.rect(self.screen, self.WHITE, player_hp_bar_rect, 2)
        
        # 渲染戰鬥選項
        choices = combat_data["choices"]
        choices_y = 200
        for i, choice in enumerate(choices):
            choice_text = f"{i+1}. {choice}"
            text_surface = self.font.render(choice_text, True, self.YELLOW)
            self.screen.blit(text_surface, (50, choices_y + i * 30))
        
        # 渲染戰鬥記錄
        combat_log = combat_data.get("log", [])
        log_y = 350
        for i, log_entry in enumerate(combat_log):
            log_surface = self.small_font.render(log_entry, True, self.WHITE)
            self.screen.blit(log_surface, (50, log_y + i * 20))
    
    def render_inventory_ui(self, inventory):
        """渲染背包UI"""
        # 清除背景
        overlay = pygame.Surface((800, 600))
        overlay.set_alpha(128)
        overlay.fill(self.BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # 渲染背包窗口
        inventory_rect = pygame.Rect(200, 100, 400, 400)
        pygame.draw.rect(self.screen, self.BLACK, inventory_rect)
        pygame.draw.rect(self.screen, self.WHITE, inventory_rect, 3)
        
        # 標題
        title_surface = self.big_font.render("背包", True, self.WHITE)
        self.screen.blit(title_surface, (inventory_rect.x + 10, inventory_rect.y + 10))
        
        # 渲染物品
        items = inventory.get_items()
        for i, (item_name, quantity) in enumerate(items.items()):
            if quantity > 0:
                item_text = f"{item_name}: {quantity}"
                item_surface = self.font.render(item_text, True, self.WHITE)
                self.screen.blit(item_surface, (inventory_rect.x + 20, inventory_rect.y + 50 + i * 30))
        
        # 提示文字
        hint_surface = self.small_font.render("按 I 或 ESC 關閉", True, self.GRAY)
        self.screen.blit(hint_surface, (inventory_rect.x + 10, inventory_rect.y + 360))
    
    def wrap_text(self, text, max_width):
        """文字換行"""
        words = text.split(' ')
        lines = []
        current_line = ""
        
        for word in words:
            test_line = current_line + word + " "
            if self.font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line.strip())
                current_line = word + " "
        
        if current_line:
            lines.append(current_line.strip())
        
        return lines
    
    def render_health_bar(self, x, y, current_hp, max_hp, width=100, height=10):
        """渲染血條"""
        # 背景
        bg_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self.screen, self.GRAY, bg_rect)
        
        # 血條
        if max_hp > 0:
            hp_percent = current_hp / max_hp
            hp_width = int(width * hp_percent)
            hp_rect = pygame.Rect(x, y, hp_width, height)
            
            # 根據血量決定顏色
            if hp_percent > 0.6:
                color = self.GREEN
            elif hp_percent > 0.3:
                color = self.YELLOW
            else:
                color = self.RED
            
            pygame.draw.rect(self.screen, color, hp_rect)
        
        # 邊框
        pygame.draw.rect(self.screen, self.WHITE, bg_rect, 1)

