# main.py - 主程式
import pygame
import sys
from player import Player
from map import MapManager
from story import StoryManager
from ui import UIManager
from combat import CombatSystem
from inventory import Inventory

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("末日第二餐廳")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # 遊戲系統初始化
        self.player = Player(5, 5)  # 起始位置
        self.map_manager = MapManager()
        self.story_manager = StoryManager()
        self.ui_manager = UIManager(self.screen)
        self.combat_system = CombatSystem()
        self.inventory = Inventory()
        
        # 遊戲狀態
        self.game_state = "exploration"  # exploration, story, combat, inventory
        self.current_story_event = None
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                if self.game_state == "exploration":
                    self.handle_exploration_input(event.key)
                elif self.game_state == "story":
                    self.handle_story_input(event.key)
                elif self.game_state == "combat":
                    self.handle_combat_input(event.key)
                elif self.game_state == "inventory":
                    self.handle_inventory_input(event.key)
    
    def handle_exploration_input(self, key):
        old_x, old_y = self.player.x, self.player.y
        
        if key == pygame.K_UP:
            self.player.move(0, -1)
        elif key == pygame.K_DOWN:
            self.player.move(0, 1)
        elif key == pygame.K_LEFT:
            self.player.move(-1, 0)
        elif key == pygame.K_RIGHT:
            self.player.move(1, 0)
        elif key == pygame.K_RETURN:
            self.interact_with_current_tile()
        elif key == pygame.K_i:
            self.game_state = "inventory"
        
        # 檢查地圖邊界
        if not self.map_manager.is_valid_position(self.player.x, self.player.y):
            self.player.x, self.player.y = old_x, old_y
        else:
            # 檢查是否觸發事件
            self.check_tile_events()
    
    def interact_with_current_tile(self):
        """與當前位置互動"""
        tile_type = self.map_manager.get_tile_type(self.player.x, self.player.y)
        event = self.story_manager.get_event_by_location(self.player.x, self.player.y, tile_type)
        
        if event:
            self.trigger_story_event(event)
    
    def check_tile_events(self):
        """檢查腳下是否有自動觸發事件"""
        tile_type = self.map_manager.get_tile_type(self.player.x, self.player.y)
        auto_event = self.story_manager.get_auto_event(self.player.x, self.player.y, tile_type)
        
        if auto_event:
            self.trigger_story_event(auto_event)
    
    def trigger_story_event(self, event):
        """觸發劇情事件"""
        self.current_story_event = event
        self.game_state = "story"
        
        # 如果是戰鬥事件
        if event.get("type") == "combat":
            enemy_type = event.get("enemy_type", "zombie")
            if self.combat_system.start_combat(enemy_type):
                self.game_state = "combat"
    
    def handle_story_input(self, key):
        """處理劇情選擇輸入"""
        if key == pygame.K_1:
            self.story_manager.choose_option(0)
        elif key == pygame.K_2:
            self.story_manager.choose_option(1)
        elif key == pygame.K_3:
            self.story_manager.choose_option(2)
        elif key == pygame.K_RETURN:
            # 繼續劇情或回到探索
            if self.story_manager.is_story_finished():
                self.game_state = "exploration"
                self.current_story_event = None
    
    def handle_combat_input(self, key):
        """處理戰鬥輸入"""
        if key == pygame.K_1:
            result = self.combat_system.process_action(0, self.player)
        elif key == pygame.K_2:
            result = self.combat_system.process_action(1, self.player)
        elif key == pygame.K_3:
            result = self.combat_system.process_action(2, self.player)
        elif key == pygame.K_4:
            result = self.combat_system.process_action(3, self.player)
        else:
            return
        
        # 處理戰鬥結果
        if result in ["victory", "defeat", "flee_success"]:
            self.game_state = "exploration"
    
    def handle_inventory_input(self, key):
        """處理背包輸入"""
        if key == pygame.K_ESCAPE or key == pygame.K_i:
            self.game_state = "exploration"
    
    def update(self):
        """更新遊戲邏輯"""
        if self.game_state == "combat":
            self.combat_system.update()
    
    def render(self):
        """渲染遊戲畫面"""
        self.screen.fill((0, 0, 0))
        
        if self.game_state == "exploration":
            self.map_manager.render(self.screen, self.player.x, self.player.y)
            self.player.render(self.screen)
            self.ui_manager.render_exploration_ui()
            
        elif self.game_state == "story":
            self.map_manager.render(self.screen, self.player.x, self.player.y)
            self.player.render(self.screen)
            self.ui_manager.render_story_ui(self.current_story_event)
            
        elif self.game_state == "combat":
            combat_data = self.combat_system.get_combat_data()
            self.ui_manager.render_combat_ui(combat_data)
            
        elif self.game_state == "inventory":
            self.ui_manager.render_inventory_ui(self.inventory)
        
        pygame.display.flip()
    
    def run(self):
        """主遊戲循環"""
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
