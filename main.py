#!/usr/bin/env python3
"""
修復版主程式 - 確保正確的結構和導入
"""

import pygame
import sys
import time

# 導入遊戲模組
try:
    from game_state import GameState
    from map_manager import MapManager
    from player import Player
    from ui import UI
    from combat import CombatSystem
    from inventory import Inventory
    from font_manager import font_manager
    print("✅ 所有模組導入成功")
except ImportError as e:
    print(f"❌ 模組導入失敗: {e}")
    sys.exit(1)

class Game:
    def __init__(self):
        print("🎮 初始化遊戲...")
        
        # 初始化Pygame
        pygame.init()
        print("✅ Pygame初始化完成")
        
        # 檢查中文字體（但不讓它阻止遊戲啟動）
        try:
            if not font_manager.install_chinese_font():
                print("⚠️ 中文字體檢查未通過，將使用預設字體")
        except Exception as e:
            print(f"⚠️ 字體檢查錯誤: {e}")
        
        # 遊戲設定
        self.SCREEN_WIDTH = 1024
        self.SCREEN_HEIGHT = 768
        self.FPS = 60
        
        # 初始化畫面
        try:
            self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
            pygame.display.set_caption("末世第二餐廳")
            self.clock = pygame.time.Clock()
            print("✅ 視窗創建完成")
        except Exception as e:
            print(f"❌ 視窗創建失敗: {e}")
            raise
        
        # 遊戲狀態
        try:
            self.game_state = GameState()
            print("✅ 遊戲狀態初始化完成")
        except Exception as e:
            print(f"❌ 遊戲狀態初始化失敗: {e}")
            raise
        
        # 初始化遊戲組件
        try:
            self.map_manager = MapManager()
            self.player = Player(x=400, y=300)
            self.ui = UI(self.screen)
            self.combat_system = CombatSystem()
            self.inventory = Inventory()
            print("✅ 所有遊戲組件初始化完成")
        except Exception as e:
            print(f"❌ 遊戲組件初始化失敗: {e}")
            raise
        
        # 遊戲標誌
        self.running = True
        self.show_intro = True
        
        # 互動冷卻機制
        self.last_interaction_time = 0
        self.interaction_cooldown = 0.5
        
        print("🎉 遊戲初始化完成！")
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            elif event.type == pygame.KEYDOWN:
                # 全域快捷鍵
                if event.key == pygame.K_F1:
                    print(f"🔍 當前狀態: 遊戲={self.game_state.current_state}, 對話={self.ui.dialogue_active}")
                elif event.key == pygame.K_F2:
                    self.force_exploration_state()
                
                # 遊戲事件處理
                elif self.show_intro:
                    if event.key == pygame.K_SPACE:
                        self.show_intro = False
                        print("📖 跳過開場動畫")
                        
                elif self.game_state.current_state == "exploration":
                    self.handle_exploration_input(event)
                    
                elif self.game_state.current_state == "combat":
                    self.handle_combat_input(event)
                    
                elif self.game_state.current_state == "dialogue":
                    self.handle_dialogue_input(event)
    
    def handle_exploration_input(self, event):
        if event.key == pygame.K_UP:
            self.player.move(0, -32)
        elif event.key == pygame.K_DOWN:
            self.player.move(0, 32)
        elif event.key == pygame.K_LEFT:
            self.player.move(-32, 0)
        elif event.key == pygame.K_RIGHT:
            self.player.move(32, 0)
        elif event.key == pygame.K_SPACE:
            self.interact()
        elif event.key == pygame.K_i:
            self.ui.toggle_inventory()
        elif event.key == pygame.K_m:
            self.ui.toggle_map()
    
    def handle_combat_input(self, event):
        if event.key == pygame.K_1:
            self.combat_system.player_action("attack")
        elif event.key == pygame.K_2:
            self.combat_system.player_action("defend")
        elif event.key == pygame.K_3:
            self.combat_system.player_action("escape")
    
    def handle_dialogue_input(self, event):
        if not self.ui.dialogue_active:
            self.game_state.current_state = "exploration"
            return
        
        if event.key == pygame.K_1 and len(self.ui.dialogue_options) >= 1:
            self.ui.select_dialogue_option(0)
        elif event.key == pygame.K_2 and len(self.ui.dialogue_options) >= 2:
            self.ui.select_dialogue_option(1)
        elif event.key == pygame.K_3 and len(self.ui.dialogue_options) >= 3:
            self.ui.select_dialogue_option(2)
        elif event.key == pygame.K_SPACE:
            self.ui.continue_dialogue()
        elif event.key == pygame.K_ESCAPE:
            self.ui.end_dialogue()
            self.game_state.current_state = "exploration"
        
        # 檢查對話是否結束
        if not self.ui.dialogue_active and self.game_state.current_state == "dialogue":
            self.game_state.current_state = "exploration"
    
    def interact(self):
        # 檢查互動冷卻
        current_time = time.time()
        if current_time - self.last_interaction_time < self.interaction_cooldown:
            return
        
        # 檢查互動
        current_floor = self.map_manager.get_current_floor()
        interaction = self.map_manager.check_interaction(
            self.player.x, self.player.y, current_floor
        )
        
        if interaction:
            self.last_interaction_time = current_time
            
            if interaction["type"] == "shop":
                if self.game_state.current_state != "dialogue":
                    self.game_state.current_state = "dialogue"
                    self.ui.start_dialogue(interaction)
            elif interaction["type"] == "npc":
                if self.game_state.current_state != "dialogue":
                    self.game_state.current_state = "dialogue"
                    self.ui.start_dialogue(interaction)
            elif interaction["type"] == "stairs":
                self.use_stairs(interaction)
            elif interaction["type"] == "item":
                self.collect_item(interaction)
    
    def use_stairs(self, stairs_info):
        direction = stairs_info["direction"]
        current_floor = self.map_manager.current_floor
        
        if direction == "up" and current_floor < 3:
            self.map_manager.change_floor(current_floor + 1)
            self.player.set_position(400, 600)
        elif direction == "down" and current_floor > 1:
            self.map_manager.change_floor(current_floor - 1)
            self.player.set_position(400, 100)
    
    def collect_item(self, item_info):
        success = self.inventory.add_item(item_info["item"])
        if success:
            self.ui.show_message(f"獲得了 {item_info['item']['name']}")
            current_floor = self.map_manager.get_current_floor()
            self.map_manager.remove_item_from_floor(item_info["item"], current_floor)
        else:
            self.ui.show_message("背包已滿！")
    
    def force_exploration_state(self):
        """強制恢復exploration狀態"""
        print("🔧 強制恢復exploration狀態")
        self.game_state.current_state = "exploration"
        self.ui.dialogue_active = False
        self.ui.show_inventory = False
        self.ui.show_map = False
    
    def update(self):
        if not self.show_intro:
            # 同步狀態
            if not self.ui.dialogue_active and self.game_state.current_state == "dialogue":
                self.game_state.current_state = "exploration"
            
            # 更新系統
            self.player.update()
            self.map_manager.update()
            
            # 根據狀態更新
            if self.game_state.current_state == "exploration":
                self.update_exploration()
            elif self.game_state.current_state == "combat":
                self.update_combat()
            
            # 更新遊戲狀態
            self.game_state.update_messages()
    
    def update_exploration(self):
        """更新exploration狀態"""
        # 檢查戰鬥區域
        current_floor = self.map_manager.get_current_floor()
        combat_zone = self.map_manager.check_combat_zone(
            self.player.x, self.player.y, current_floor
        )
        
        if combat_zone:
            if not hasattr(self, '_last_combat_zone') or self._last_combat_zone != combat_zone:
                self._last_combat_zone = combat_zone
                self.start_combat_in_zone(combat_zone)
        else:
            if hasattr(self, '_last_combat_zone'):
                self._last_combat_zone = None
    
    def start_combat_in_zone(self, combat_zone):
        """開始戰鬥"""
        self.game_state.current_state = "combat"
        enemy = self.game_state.get_random_enemy()
        self.combat_system.start_combat(enemy)
    
    def update_combat(self):
        """更新戰鬥"""
        self.combat_system.update(self.game_state)
        
        if not self.combat_system.in_combat:
            self.game_state.current_state = "exploration"
    
    def render(self):
        self.screen.fill((0, 0, 0))
        
        if self.show_intro:
            self.render_intro()
        else:
            # 渲染地圖
            self.map_manager.render(self.screen)
            
            # 渲染玩家
            self.player.render(self.screen)
            
            # 渲染UI
            self.ui.render(self.game_state, self.player, self.inventory)
            
            # 渲染戰鬥
            if self.game_state.current_state == "combat":
                self.combat_system.render(self.screen, self.game_state)
        
        pygame.display.flip()
    
    def render_intro(self):
        intro_text = [
            "《末世第二餐廳》",
            "",
            "按 [空白鍵] 開始遊戲",
            "",
            "操作說明:",
            "方向鍵 - 移動",
            "空白鍵 - 互動",
            "I鍵 - 背包",
            "F1 - 狀態檢查",
            "F2 - 強制修復"
        ]
        
        y_offset = 200
        for line in intro_text:
            if line:
                try:
                    text_surface = font_manager.render_text(line, 24, (255, 255, 255))
                    text_rect = text_surface.get_rect(center=(self.SCREEN_WIDTH//2, y_offset))
                    self.screen.blit(text_surface, text_rect)
                except:
                    # 備用渲染
                    font = pygame.font.Font(None, 24)
                    text_surface = font.render(line, True, (255, 255, 255))
                    text_rect = text_surface.get_rect(center=(self.SCREEN_WIDTH//2, y_offset))
                    self.screen.blit(text_surface, text_rect)
            y_offset += 30
    
    def run(self):
        print("🎮 開始遊戲主迴圈")
        
        while self.running:
            try:
                self.handle_events()
                self.update()
                self.render()
                self.clock.tick(self.FPS)
            except Exception as e:
                print(f"💥 遊戲迴圈錯誤: {e}")
                import traceback
                traceback.print_exc()
                break
        
        print("👋 遊戲結束")
        pygame.quit()
        sys.exit()

def main():
    """程式入口點"""
    print("🎮 啟動《末世第二餐廳》")
    print("=" * 40)
    
    try:
        game = Game()
        game.run()
    except KeyboardInterrupt:
        print("\n👋 遊戲被用戶中斷")
    except Exception as e:
        print(f"💥 遊戲發生錯誤: {e}")
        import traceback
        traceback.print_exc()
    finally:
        try:
            pygame.quit()
        except:
            pass

if __name__ == "__main__":
    main()