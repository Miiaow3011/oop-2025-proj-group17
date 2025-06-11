import pygame
import random
from font_manager import font_manager  # 添加這行導入

class CombatSystem:
    def __init__(self):
        self.in_combat = False
        self.current_enemy = None
        self.player_turn = True
        self.combat_log = []
        self.animation_timer = 0
        self.combat_result = None  # "win", "lose", "escape"
        
        # 戰鬥動畫
        self.shake_timer = 0
        self.shake_intensity = 0
        
        # 修復：使用 font_manager 而不是直接使用 pygame.font
        # 這樣可以確保中文字體正常顯示
        # self.font_large = pygame.font.Font(None, 32)  # 刪除這行
        # self.font_medium = pygame.font.Font(None, 24)  # 刪除這行
        # self.font_small = pygame.font.Font(None, 18)   # 刪除這行

    def start_combat(self, enemy):
        self.in_combat = True
        self.current_enemy = enemy.copy()
        self.current_enemy["max_hp"] = enemy["hp"]
        self.player_turn = True
        self.combat_log = [f"遭遇了 {enemy['name']}！"]
        self.animation_timer = 0
        self.combat_result = None

    def player_action(self, action):
        if not self.in_combat or not self.player_turn:
            return

        if action == "attack":
            self.player_attack()
        elif action == "defend":
            self.player_defend()
        elif action == "escape":
            self.player_escape()

        # 檢查敵人是否死亡
        if self.current_enemy["hp"] <= 0:
            self.combat_result = "win"
            self.end_combat()
            return

        # 敵人回合
        if self.in_combat and action != "escape":
            self.player_turn = False
            self.animation_timer = 60  # 1秒延遲

    def player_attack(self):
        # 計算傷害
        base_damage = random.randint(8, 15)
        damage = max(1, base_damage - self.current_enemy["defense"])
        
        # 暴擊機率
        is_critical = random.random() < 0.15  # 15%暴擊率
        if is_critical:
            damage = int(damage * 1.5)
            self.combat_log.append(f"暴擊！造成 {damage} 點傷害！")
        else:
            self.combat_log.append(f"造成 {damage} 點傷害！")
        
        self.current_enemy["hp"] -= damage
        self.shake_timer = 30
        self.shake_intensity = 5

    def player_defend(self):
        # 防禦回復少量血量
        heal_amount = random.randint(5, 10)
        self.combat_log.append(f"防禦姿態，回復 {heal_amount} 點血量！")
        # 這裡需要game_state來回復血量，暫時記錄
        self.combat_log.append("下回合受到傷害減半！")

    def player_escape(self):
        escape_chance = 0.6  # 60%逃跑成功率
        if random.random() < escape_chance:
            self.combat_log.append("成功逃跑了！")
            self.combat_result = "escape"
            self.end_combat()
        else:
            self.combat_log.append("逃跑失敗！")

    def enemy_turn(self, game_state):
        if not self.in_combat or self.player_turn:
            return

        # 敵人攻擊
        enemy_damage = random.randint(
            self.current_enemy["attack"] - 2,
            self.current_enemy["attack"] + 2
        )
        actual_damage = game_state.damage_player(enemy_damage)
        self.combat_log.append(f"{self.current_enemy['name']} 攻擊你，造成 {actual_damage} 點傷害！")

        # 檢查玩家是否死亡
        if game_state.is_player_dead():
            self.combat_result = "lose"
            self.end_combat()
            return

        self.player_turn = True
        self.shake_timer = 20
        self.shake_intensity = 3

    def end_combat(self):
        if self.combat_result == "win":
            exp_reward = self.current_enemy["exp_reward"]
            self.combat_log.append(f"獲得 {exp_reward} 經驗值！")
        
        self.animation_timer = 120  # 2秒後結束戰鬥畫面
        # 添加這行 - 通知主遊戲戰鬥結束
        self.combat_ended = True

    def update(self, game_state):
        if not self.in_combat:
            return

        # 更新動畫計時器
        if self.animation_timer > 0:
            self.animation_timer -= 1

        # 敵人回合延遲
        if not self.player_turn and self.animation_timer == 0:
            self.enemy_turn(game_state)

        # 戰鬥結束延遲
        if self.combat_result and self.animation_timer == 0:
            self.in_combat = False
            if self.combat_result == "win":
                game_state.add_exp(self.current_enemy["exp_reward"])
            game_state.set_state("exploration")

        # 更新震動效果
        if self.shake_timer > 0:
            self.shake_timer -= 1

        # 限制戰鬥日誌長度
        if len(self.combat_log) > 8:
            self.combat_log.pop(0)

    def render(self, screen, game_state):
        if not self.in_combat:
            return

        screen_width, screen_height = screen.get_size()

        # 戰鬥背景
        combat_bg = pygame.Rect(0, 0, screen_width, screen_height)
        pygame.draw.rect(screen, (20, 20, 40), combat_bg)

        # 震動效果
        shake_x = 0
        shake_y = 0
        if self.shake_timer > 0:
            shake_x = random.randint(-self.shake_intensity, self.shake_intensity)
            shake_y = random.randint(-self.shake_intensity, self.shake_intensity)

        # 敵人顯示
        enemy_x = screen_width // 2 + shake_x
        enemy_y = 150 + shake_y
        self.render_enemy(screen, enemy_x, enemy_y)

        # 敵人血量條
        self.render_enemy_health(screen, enemy_x, enemy_y)

        # 玩家血量條
        self.render_player_health(screen, game_state)

        # 戰鬥選項
        if self.player_turn and not self.combat_result:
            self.render_combat_options(screen)

        # 戰鬥日誌
        self.render_combat_log(screen)

        # 戰鬥結果
        if self.combat_result:
            self.render_combat_result(screen)

    def render_enemy(self, screen, x, y):
        enemy_name = self.current_enemy["name"]
        
        # 根據敵人類型繪製不同外觀
        if "殭屍" in enemy_name:
            self.draw_zombie(screen, x, y)
        elif "外星人" in enemy_name:
            self.draw_alien(screen, x, y)
        else:
            self.draw_generic_enemy(screen, x, y)

        # 修復：敵人名稱使用 font_manager
        name_surface = font_manager.render_text(enemy_name, 24, (255, 255, 255))
        name_rect = name_surface.get_rect(center=(x, y - 80))
        screen.blit(name_surface, name_rect)

    def draw_zombie(self, screen, x, y):
        # 殭屍外觀 (像素風格)
        # 身體
        pygame.draw.rect(screen, (100, 100, 100), (x-20, y-20, 40, 50))
        # 頭部
        pygame.draw.rect(screen, (150, 150, 100), (x-15, y-40, 30, 25))
        # 眼睛 (紅色)
        pygame.draw.rect(screen, (255, 0, 0), (x-10, y-35, 4, 4))
        pygame.draw.rect(screen, (255, 0, 0), (x+6, y-35, 4, 4))
        # 嘴巴
        pygame.draw.rect(screen, (100, 0, 0), (x-5, y-25, 10, 3))
        # 手臂
        pygame.draw.rect(screen, (120, 120, 80), (x-25, y-10, 10, 20))
        pygame.draw.rect(screen, (120, 120, 80), (x+15, y-10, 10, 20))

    def draw_alien(self, screen, x, y):
        # 外星人外觀
        # 身體 (銀色)
        pygame.draw.rect(screen, (150, 150, 200), (x-18, y-15, 36, 40))
        # 頭部 (大頭)
        pygame.draw.rect(screen, (200, 200, 220), (x-20, y-45, 40, 35))
        # 大眼睛 (黑色)
        pygame.draw.rect(screen, (0, 0, 0), (x-15, y-35, 8, 12))
        pygame.draw.rect(screen, (0, 0, 0), (x+7, y-35, 8, 12))
        # 觸角
        pygame.draw.rect(screen, (200, 200, 220), (x-10, y-50, 2, 8))
        pygame.draw.rect(screen, (200, 200, 220), (x+8, y-50, 2, 8))

    def draw_generic_enemy(self, screen, x, y):
        # 一般敵人外觀
        pygame.draw.rect(screen, (150, 50, 50), (x-16, y-16, 32, 40))
        pygame.draw.rect(screen, (180, 80, 80), (x-12, y-32, 24, 20))
        pygame.draw.rect(screen, (50, 50, 50), (x-8, y-28, 4, 4))
        pygame.draw.rect(screen, (50, 50, 50), (x+4, y-28, 4, 4))

    def render_enemy_health(self, screen, enemy_x, enemy_y):
        # 敵人血量條
        hp_ratio = self.current_enemy["hp"] / self.current_enemy["max_hp"]
        bar_width = 100
        bar_height = 8
        bar_x = enemy_x - bar_width // 2
        bar_y = enemy_y + 60

        # 背景
        bg_rect = pygame.Rect(bar_x, bar_y, bar_width, bar_height)
        pygame.draw.rect(screen, (100, 100, 100), bg_rect)

        # 血量
        hp_rect = pygame.Rect(bar_x, bar_y, bar_width * hp_ratio, bar_height)
        hp_color = (255, 0, 0) if hp_ratio < 0.3 else (255, 165, 0) if hp_ratio < 0.6 else (255, 255, 0)
        pygame.draw.rect(screen, hp_color, hp_rect)

        # 修復：血量文字使用 font_manager
        hp_text = f"{self.current_enemy['hp']}/{self.current_enemy['max_hp']}"
        hp_surface = font_manager.render_text(hp_text, 18, (255, 255, 255))
        hp_rect = hp_surface.get_rect(center=(enemy_x, bar_y + 20))
        screen.blit(hp_surface, hp_rect)

    def render_player_health(self, screen, game_state):
        screen_width = screen.get_width()
        
        # 玩家血量條
        hp_ratio = game_state.player_stats["hp"] / game_state.player_stats["max_hp"]
        bar_width = 200
        bar_height = 20
        bar_x = 20
        bar_y = screen.get_height() - 100

        # 背景
        bg_rect = pygame.Rect(bar_x, bar_y, bar_width, bar_height)
        pygame.draw.rect(screen, (100, 100, 100), bg_rect)

        # 血量
        hp_rect = pygame.Rect(bar_x, bar_y, bar_width * hp_ratio, bar_height)
        hp_color = (255, 0, 0) if hp_ratio < 0.3 else (255, 255, 0) if hp_ratio < 0.6 else (0, 255, 0)
        pygame.draw.rect(screen, hp_color, hp_rect)

        # 修復：血量文字使用 font_manager
        hp_text = f"HP: {game_state.player_stats['hp']}/{game_state.player_stats['max_hp']}"
        hp_surface = font_manager.render_text(hp_text, 24, (255, 255, 255))
        screen.blit(hp_surface, (bar_x, bar_y - 25))

    def render_combat_options(self, screen):
        screen_width, screen_height = screen.get_size()
        
        # 戰鬥選項框
        options_rect = pygame.Rect(screen_width - 250, screen_height - 200, 230, 180)
        pygame.draw.rect(screen, (0, 0, 0, 200), options_rect)
        pygame.draw.rect(screen, (255, 255, 255), options_rect, 2)

        # 修復：選項文字使用 font_manager
        options = [
            "1. 攻擊",
            "2. 防禦", 
            "3. 逃跑"
        ]
        
        y_offset = options_rect.y + 20
        for option in options:
            option_surface = font_manager.render_text(option, 24, (255, 255, 255))
            screen.blit(option_surface, (options_rect.x + 10, y_offset))
            y_offset += 30

        # 修復：提示文字使用 font_manager
        hint_text = "選擇你的行動:"
        hint_surface = font_manager.render_text(hint_text, 18, (200, 200, 200))
        screen.blit(hint_surface, (options_rect.x + 10, options_rect.y + 120))

    def render_combat_log(self, screen):
        # 戰鬥日誌
        log_rect = pygame.Rect(20, 200, 400, 200)
        pygame.draw.rect(screen, (0, 0, 0, 180), log_rect)
        pygame.draw.rect(screen, (255, 255, 255), log_rect, 1)

        # 修復：日誌標題使用 font_manager
        log_title = font_manager.render_text("戰鬥記錄:", 24, (255, 255, 255))
        screen.blit(log_title, (log_rect.x + 10, log_rect.y + 5))

        # 修復：日誌內容使用 font_manager
        y_offset = log_rect.y + 30
        for message in self.combat_log[-6:]:  # 只顯示最後6條
            msg_surface = font_manager.render_text(message, 18, (255, 255, 255))
            screen.blit(msg_surface, (log_rect.x + 10, y_offset))
            y_offset += 20

    def render_combat_result(self, screen):
        screen_width, screen_height = screen.get_size()
        
        # 結果顯示
        if self.combat_result == "win":
            result_text = "勝利！"
            result_color = (0, 255, 0)
        elif self.combat_result == "lose":
            result_text = "失敗..."
            result_color = (255, 0, 0)
        elif self.combat_result == "escape":
            result_text = "逃跑成功"
            result_color = (255, 255, 0)

        # 修復：結果文字使用 font_manager
        result_surface = font_manager.render_text(result_text, 32, result_color)
        result_rect = result_surface.get_rect(center=(screen_width//2, screen_height//2))

        # 結果背景
        bg_rect = result_rect.copy()
        bg_rect.inflate(40, 20)
        pygame.draw.rect(screen, (0, 0, 0, 200), bg_rect)
        screen.blit(result_surface, result_rect)