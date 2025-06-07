# player.py - 玩家角色系統
import pygame

class Player:
    def __init__(self, start_x, start_y):
        self.x = start_x
        self.y = start_y
        self.max_hp = 100
        self.hp = 100
        self.attack = 15
        self.defense = 5
        self.level = 1
        self.exp = 0
        
        # 視覺相關
        self.sprite = None
        self.load_sprite()
    
    def load_sprite(self):
        """載入角色圖片"""
        try:
            self.sprite = pygame.image.load("assets/player.png")
            self.sprite = pygame.transform.scale(self.sprite, (32, 32))
        except:
            # 如果沒有圖片，創建一個簡單的矩形
            self.sprite = pygame.Surface((32, 32))
            self.sprite.fill((0, 255, 0))  # 綠色代表玩家
    
    def move(self, dx, dy):
        """移動玩家"""
        self.x += dx
        self.y += dy
    
    def take_damage(self, damage):
        """受到傷害"""
        actual_damage = max(1, damage - self.defense)
        self.hp = max(0, self.hp - actual_damage)
        return actual_damage
    
    def heal(self, amount):
        """恢復生命值"""
        self.hp = min(self.max_hp, self.hp + amount)
    
    def is_alive(self):
        """檢查是否存活"""
        return self.hp > 0
    
    def gain_exp(self, amount):
        """獲得經驗值"""
        self.exp += amount
        # 簡單的升級系統
        if self.exp >= self.level * 100:
            self.level_up()
    
    def level_up(self):
        """升級"""
        self.level += 1
        self.max_hp += 10
        self.hp = self.max_hp
        self.attack += 2
        self.defense += 1
        self.exp = 0
    
    def render(self, screen):
        """渲染玩家"""
        # 計算螢幕位置（以玩家為中心）
        screen_x = 400 - 16  # 螢幕中心 - 半個sprite寬度
        screen_y = 300 - 16  # 螢幕中心 - 半個sprite高度
        screen.blit(self.sprite, (screen_x, screen_y))
    
    def get_stats(self):
        """獲取玩家狀態"""
        return {
            "hp": self.hp,
            "max_hp": self.max_hp,
            "attack": self.attack,
            "defense": self.defense,
            "level": self.level,
            "exp": self.exp
        }

