# 末世第二餐廳 - main.py
import pygame
import sys
import time
import random
from game_state import GameState
from map_manager import MapManager
from player import Player
from ui import UI
from combat import CombatSystem
from inventory import Inventory
from font_manager import font_manager

class Game:
    def __init__(self):
        pygame.init()
        
        # 檢查中文字體
        if not font_manager.install_chinese_font():
            print("警告: 中文字體可能無法正常顯示")
            print("建議將中文TTF字體檔案放入 assets/fonts/ 資料夾")
        
        # 遊戲設定
        self.SCREEN_WIDTH = 1024
        self.SCREEN_HEIGHT = 768
        self.FPS = 60
        
        # 初始化畫面
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("末世第二餐廳")
        self.clock = pygame.time.Clock()
        
        # 遊戲狀態
        self.game_state = GameState()
        
        # 初始化遊戲組件
        self.map_manager = MapManager()
        self.player = Player(x=400, y=300)  # 初始位置在7-11
        self.ui = UI(self.screen)
        self.combat_system = CombatSystem()
        self.inventory = Inventory()
        self.ui.set_player_reference(self.player)
        self.ui.set_game_state_reference(self.game_state)
        self.ui.set_inventory_reference(self.inventory)
        
        # 遊戲標誌
        self.running = True
        self.show_intro = True
        
        # 互動冷卻機制
        self.last_interaction_time = 0
        self.interaction_cooldown = 0.5  # 0.5秒冷卻時間
        
        # 除錯模式
        self.debug_mode = False
        
    def handle_events(self):
        """修復版事件處理 - 解決UI卡住問題"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            elif event.type == pygame.KEYDOWN:
                # ======= 全域快捷鍵 - 任何狀態下都優先處理 =======
                if event.key == pygame.K_ESCAPE:
                    # ESC: 強制關閉所有UI並恢復exploration狀態
                    self.force_exploration_state()
                    continue
                    
                elif event.key == pygame.K_r:
                    # R鍵: 重新開始遊戲
                    if hasattr(self.ui, 'game_over') and hasattr(self.ui, 'game_completed'):
                        if self.ui.game_over or self.ui.game_completed:
                            self.restart_game()
                            continue

                elif event.key == pygame.K_i:
                    # I鍵: 背包切換
                    self.handle_inventory_toggle()
                    continue
                    
                elif event.key == pygame.K_m:
                    # M鍵: 地圖切換
                    self.handle_map_toggle()
                    continue
                
                # 除錯快捷鍵
                elif event.key == pygame.K_F1:
                    self.toggle_debug_mode()
                    continue
                elif event.key == pygame.K_F2:
                    self.force_exploration_state()
                    continue
                elif event.key == pygame.K_F3:
                    self.reset_player_position()
                    continue
                
                # ======= 狀態專用事件處理 =======
                if self.show_intro:
                    if event.key == pygame.K_SPACE:
                        self.show_intro = False
                        
                elif self.game_state.current_state == "exploration":
                    self.handle_exploration_input(event)
                    
                elif self.game_state.current_state == "combat":
                    self.handle_combat_input(event)
                    
                elif self.game_state.current_state == "dialogue":
                    self.handle_dialogue_input(event)
    
    def handle_inventory_toggle(self):
        """處理背包切換 - 修復版"""
        old_state = self.ui.show_inventory
        self.ui.toggle_inventory()
        
        if self.debug_mode:
            print(f"🎒 背包切換: {old_state} → {self.ui.show_inventory}")
            print(f"   當前遊戲狀態: {self.game_state.current_state}")
            print(f"   UI狀態: 背包={self.ui.show_inventory}, 地圖={self.ui.show_map}, 對話={self.ui.dialogue_active}")
        
        # 關鍵修復：確保遊戲狀態正確
        if self.ui.show_inventory:
            # 背包開啟時，確保在exploration狀態
            if self.game_state.current_state != "exploration":
                self.game_state.set_state("exploration")
                if self.debug_mode:
                    print("   ➤ 強制設為exploration狀態")
        else:
            # 背包關閉時，檢查並確保回到exploration狀態
            if not self.ui.is_any_ui_open():
                self.game_state.set_state("exploration")
                if self.debug_mode:
                    print("   ➤ 背包關閉，回到exploration狀態")
    
    def handle_map_toggle(self):
        """處理地圖切換 - 修復版"""
        old_state = self.ui.show_map
        self.ui.toggle_map()
        
        if self.debug_mode:
            print(f"🗺️ 地圖切換: {old_state} → {self.ui.show_map}")
            print(f"   當前遊戲狀態: {self.game_state.current_state}")
        
        # 關鍵修復：確保遊戲狀態正確
        if self.ui.show_map:
            # 地圖開啟時，確保在exploration狀態
            if self.game_state.current_state != "exploration":
                self.game_state.set_state("exploration")
                if self.debug_mode:
                    print("   ➤ 強制設為exploration狀態")
        else:
            # 地圖關閉時，檢查並確保回到exploration狀態
            if not self.ui.is_any_ui_open():
                self.game_state.set_state("exploration")
                if self.debug_mode:
                    print("   ➤ 地圖關閉，回到exploration狀態")
    
    def force_exploration_state(self):
        """強制恢復到exploration狀態 - 增強版"""
        print("🔧 強制恢復exploration狀態")
        
        # 重置所有狀態
        self.game_state.current_state = "exploration"
        self.ui.close_all_ui()  # 使用UI的新方法
        
        # 強制停止玩家移動
        if hasattr(self.player, 'force_stop_movement'):
            self.player.force_stop_movement()
        else:
            self.player.is_moving = False
            self.player.move_target_x = self.player.x
            self.player.move_target_y = self.player.y
        
        print("✅ 狀態已完全重置")
        if self.debug_mode:
            print(f"   遊戲狀態: {self.game_state.current_state}")
            print(f"   UI狀態: {self.ui.get_ui_status()}")
            print(f"   玩家移動: {self.player.is_moving}")
    
    def toggle_debug_mode(self):
        """切換除錯模式"""
        self.debug_mode = not self.debug_mode
        print(f"🔧 除錯模式: {'開啟' if self.debug_mode else '關閉'}")
        if self.debug_mode:
            self.print_debug_info()
    
    def print_debug_info(self):
        """顯示除錯資訊"""
        print(f"🔍 當前狀態:")
        print(f"   遊戲狀態: {self.game_state.current_state}")
        print(f"   UI狀態: {self.ui.get_ui_status()}")
        print(f"   玩家位置: ({self.player.x}, {self.player.y})")
        print(f"   玩家移動: {self.player.is_moving}")
    
    def reset_player_position(self):
        """重置玩家位置"""
        old_pos = (self.player.x, self.player.y)
        self.player.set_position(400, 300)
        print(f"🔄 重置玩家位置: {old_pos} → (400, 300)")
    
    def handle_exploration_input(self, event):
        """處理探索模式的輸入 - 修復版"""
        if self.debug_mode:
            print(f"🎮 exploration輸入: {pygame.key.name(event.key)}")
            print(f"   UI開啟: {self.ui.is_any_ui_open()}")
            print(f"   玩家移動中: {self.player.is_moving}")
        
        # 檢查UI狀態，如果有UI開啟就不處理移動
        if self.ui.is_any_ui_open():
            if self.debug_mode:
                print("⚠️ UI開啟中，忽略移動輸入")
            return
        
        # 移動處理
        movement_successful = False
        
        if event.key == pygame.K_UP:
            movement_successful = self.player.move(0, -32)
        elif event.key == pygame.K_DOWN:
            movement_successful = self.player.move(0, 32)
        elif event.key == pygame.K_LEFT:
            movement_successful = self.player.move(-32, 0)
        elif event.key == pygame.K_RIGHT:
            movement_successful = self.player.move(32, 0)
        elif event.key == pygame.K_SPACE:
            self.interact()
        
        # 除錯資訊
        if self.debug_mode and event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
            if movement_successful:
                print(f"✅ 移動開始: 目標({self.player.move_target_x}, {self.player.move_target_y})")
            else:
                print(f"❌ 移動被拒絕: 可能正在移動中或邊界限制")
    
    def handle_combat_input(self, event):
        """處理戰鬥輸入"""
        if event.key == pygame.K_1:
            self.combat_system.player_action("attack")
        elif event.key == pygame.K_2:
            self.combat_system.player_action("defend")
        elif event.key == pygame.K_3:
            self.combat_system.player_action("escape")
        
        # 檢查戰鬥是否結束
        if hasattr(self.combat_system, 'combat_result') and self.combat_system.combat_result:
            if self.debug_mode:
                print(f"⚔️ 戰鬥結束: {self.combat_system.combat_result}")
            
            # 處理戰鬥結果
            self.end_combat_zone(self.combat_system.combat_result)
            
            # 回到探索狀態
            self.game_state.current_state = "exploration"
    
    def handle_dialogue_input(self, event):
        if event.key == pygame.K_1 and len(self.ui.dialogue_options) >= 1:
            self.ui.select_dialogue_option(0)
            self.check_dialogue_end()
        elif event.key == pygame.K_2 and len(self.ui.dialogue_options) >= 2:
            self.ui.select_dialogue_option(1)
            self.check_dialogue_end()
        elif event.key == pygame.K_3 and len(self.ui.dialogue_options) >= 3:
            self.ui.select_dialogue_option(2)
            self.check_dialogue_end()
        elif event.key == pygame.K_SPACE:
            self.ui.continue_dialogue()
            self.check_dialogue_end()
    
    def check_dialogue_end(self):
        """檢查對話是否結束，恢復exploration狀態"""
        if not self.ui.dialogue_active:
            self.game_state.current_state = "exploration"
            if self.debug_mode:
                print("💬 對話結束，回到exploration狀態")
    
    def interact(self):
        # 檢查互動冷卻
        current_time = time.time()
        if current_time - self.last_interaction_time < self.interaction_cooldown:
            if self.debug_mode:
                print(f"⏰ 互動冷卻中，還需等待 {self.interaction_cooldown - (current_time - self.last_interaction_time):.1f} 秒")
            return
        
        # 檢查玩家附近是否有可互動物件
        current_floor = self.map_manager.get_current_floor()
        interaction = self.map_manager.check_interaction(
            self.player.x, self.player.y, current_floor
        )
        
        if self.debug_mode:
            print(f"🔍 檢查互動: 樓層{current_floor}, 位置({self.player.x}, {self.player.y})")
        
        if interaction:
            if self.debug_mode:
                print(f"✅ 找到互動物件: {interaction}")
            self.last_interaction_time = current_time
            
            if interaction["type"] == "shop":
                self.start_shop_interaction(interaction)
            elif interaction["type"] == "npc":
                self.start_npc_dialogue(interaction)
            elif interaction["type"] == "stairs":
                self.use_stairs(interaction)
            elif interaction["type"] == "item":
                self.collect_item(interaction)
        else:
            if self.debug_mode:
                print("❌ 附近沒有可互動的物件")
    
    def start_shop_interaction(self, shop_info):
        if self.debug_mode:
            print(f"🏪 進入商店: {shop_info['name']}")
        
        # 檢查是否已經在對話中
        if self.game_state.current_state == "dialogue" or self.ui.dialogue_active:
            if self.debug_mode:
                print("⚠️ 已經在對話中，忽略商店互動")
            return
            
        self.game_state.set_state("dialogue")
        self.ui.start_dialogue(shop_info)
    
    def start_npc_dialogue(self, npc_info):
        if self.debug_mode:
            print(f"👤 與NPC對話: {npc_info['name']}")
        
        # 檢查是否已經在對話中
        if self.game_state.current_state == "dialogue" or self.ui.dialogue_active:
            if self.debug_mode:
                print("⚠️ 已經在對話中，忽略NPC互動")
            return
            
        self.game_state.set_state("dialogue")
        self.ui.start_dialogue(npc_info)
    
    def use_stairs(self, stairs_info):
        if self.debug_mode:
            print(f"🪜 使用樓梯: {stairs_info['direction']}")
        direction = stairs_info["direction"]
        current_floor = self.map_manager.current_floor
        
        if direction == "up":
            if current_floor == 1:
                # 1樓到2樓：自由通行
                self.map_manager.change_floor(2)
                self.player.set_position(400, 600)  # 樓梯底部
                if self.debug_mode:
                    print("⬆️ 上樓到 2 樓")
                self.ui.show_message("來到了二樓")
                
            elif current_floor == 2:
                # 2樓到3樓：需要鑰匙卡
                if self.game_state.get_flag("has_keycard") or self.inventory.has_item("鑰匙卡"):
                    self.map_manager.change_floor(3)
                    self.player.set_position(400, 600)
                    if self.debug_mode:
                        print("⬆️ 使用鑰匙卡上樓到 3 樓")
                    self.ui.show_message("🗝️ 使用鑰匙卡進入三樓！")
                    
                    # 設定標記
                    self.game_state.set_flag("unlocked_third_floor", True)
                else:
                    if self.debug_mode:
                        print("🚫 需要鑰匙卡才能上三樓")
                    self.ui.show_message("❌ 需要鑰匙卡才能進入三樓！")
                    
            else:
                if self.debug_mode:
                    print("🚫 已經在最高樓層")
                self.ui.show_message("已經是最高樓層了")
                
        elif direction == "down":
            if current_floor == 3:
                # 3樓到2樓
                self.map_manager.change_floor(2)
                self.player.set_position(400, 100)  # 樓梯頂部
                if self.debug_mode:
                    print("⬇️ 下樓到 2 樓")
                self.ui.show_message("回到了二樓")
                
            elif current_floor == 2:
                # 2樓到1樓
                self.map_manager.change_floor(1)
                self.player.set_position(400, 100)
                if self.debug_mode:
                    print("⬇️ 下樓到 1 樓")
                self.ui.show_message("回到了一樓")
                
            else:
                if self.debug_mode:
                    print("🚫 已經在最低樓層")
                self.ui.show_message("已經是最低樓層了")
    
    def collect_item(self, item_info):
        if self.debug_mode:
            print(f"📦 收集物品: {item_info['item']['name']}")
        success = self.inventory.add_item(item_info["item"])
        if success:
            self.ui.show_message(f"獲得了 {item_info['item']['name']}")
            # 從地圖上移除物品
            self.map_manager.remove_item(item_info["item"])
            if self.debug_mode:
                print(f"✅ 成功收集: {item_info['item']['name']}")
        else:
            self.ui.show_message("背包已滿！")
            if self.debug_mode:
                print(f"❌ 背包已滿，無法收集: {item_info['item']['name']}")
    
    def update(self):
        if not self.show_intro:
            # 只有在沒有UI開啟時才更新遊戲邏輯
            if not self.ui.is_any_ui_open() or self.game_state.current_state != "exploration":
                self.player.update()
                self.map_manager.update()
                
                # 戰鬥區域檢查 - 進入紅圈立即觸發戰鬥
                if self.game_state.current_state == "exploration":
                    combat_zone = self.map_manager.check_combat_zone(
                        self.player.x, self.player.y, self.map_manager.current_floor
                    )
                    
                    if combat_zone:
                        if self.debug_mode:
                            print(f"⚔️ 進入戰鬥區域: {combat_zone['name']}")
                        # 立即開始戰鬥
                        self.start_combat_in_zone(combat_zone)
            
            # 更新戰鬥系統
            if self.game_state.current_state == "combat":
                self.combat_system.update(self.game_state)
    
    def start_combat(self):
        self.game_state.current_state = "combat"
        enemy = self.game_state.get_random_enemy()
        self.combat_system.start_combat(enemy)
        if self.debug_mode:
            print(f"⚔️ 開始戰鬥: {enemy['name']}")
    
    def start_combat_in_zone(self, combat_zone):
        """在戰鬥區域開始戰鬥"""
        if self.debug_mode:
            print(f"🔄 切換到戰鬥狀態")
        
        self.game_state.current_state = "combat"
        
        # 從戰鬥區域選擇敵人
        enemy_types = combat_zone.get("enemies", ["zombie_student"])
        enemy_type = random.choice(enemy_types)
        
        # 根據敵人類型獲取敵人數據
        enemy = None
        for e in self.game_state.enemies:
            if enemy_type in e["name"].lower().replace(" ", "_"):
                enemy = e.copy()
                break
        
        if not enemy:
            enemy = self.game_state.enemies[0].copy()  # 備用敵人
        
        # 記錄當前戰鬥區域
        self.current_combat_zone = combat_zone
        
        if self.debug_mode:
            print(f"⚔️ 開始戰鬥: {enemy['name']} in {combat_zone['name']}")
            print(f"   戰鬥系統狀態: {self.combat_system.in_combat}")
        
        self.combat_system.start_combat(enemy)

    def end_combat_zone(self, result):
        """戰鬥結束處理"""
        if result == "win" and hasattr(self, 'current_combat_zone'):
            zone = self.current_combat_zone
            floor = self.map_manager.current_floor
            
            # 從地圖移除戰鬥區域
            self.map_manager.remove_combat_zone(zone, floor)
            
            # 獲得獎勵
            rewards = zone.get("rewards", [])
            if rewards:
                for reward in rewards:
                    self.inventory.add_item(reward)
                    self.ui.show_message(f"獲得了 {reward['name']}！")
            else:
                # 預設獎勵
                default_reward = {"name": "戰鬥線索", "type": "clue", "value": 1}
                self.inventory.add_item(default_reward)
                self.ui.show_message("獲得了重要線索！")
            
            if self.debug_mode:
                print(f"✅ 戰鬥區域 {zone['name']} 已清除")
            
            # 清除當前戰鬥區域記錄
            self.current_combat_zone = None

    def render(self):
        self.screen.fill((0, 0, 0))
        
        if self.show_intro:
            self.render_intro()
        else:
            # 根據遊戲狀態渲染不同畫面
            if self.game_state.current_state == "combat":
                # 戰鬥畫面
                self.combat_system.render(self.screen, self.game_state)
            else:
                # 探索畫面
                # 渲染地圖
                self.map_manager.render(self.screen)
                
                # 渲染玩家
                self.player.render(self.screen)
            
            # UI總是在最上層渲染
            self.ui.render(self.game_state, self.player, self.inventory)
            
            # 渲染除錯資訊
            if self.debug_mode:
                self.render_debug_info()
        
        pygame.display.flip()

    def update(self):
        if not self.show_intro:
            if self.game_state.current_state == "combat":
                # 戰鬥狀態更新
                self.combat_system.update(self.game_state)
                
                # 檢查戰鬥是否結束
                if not self.combat_system.in_combat:
                    if self.debug_mode:
                        print(f"⚔️ 戰鬥結束，回到探索模式")
                    
                    # 處理戰鬥結果
                    if hasattr(self, 'current_combat_zone'):
                        self.end_combat_zone("win")  # 假設玩家勝利
                    
                    self.game_state.current_state = "exploration"
            
            elif self.game_state.current_state == "exploration":
                # 只有在沒有UI開啟時才更新遊戲邏輯
                if not self.ui.is_any_ui_open():
                    self.player.update()
                    self.map_manager.update()
                    
                    # 戰鬥區域檢查
                    combat_zone = self.map_manager.check_combat_zone(
                        self.player.x, self.player.y, self.map_manager.current_floor
                    )
                    
                    if combat_zone:
                        if self.debug_mode:
                            print(f"⚔️ 進入戰鬥區域: {combat_zone['name']}")
                        self.start_combat_in_zone(combat_zone)
    
    def render_debug_info(self):
        """渲染除錯資訊"""
        debug_rect = pygame.Rect(10, 300, 250, 120)
        pygame.draw.rect(self.screen, (0, 0, 0, 180), debug_rect)
        pygame.draw.rect(self.screen, (0, 255, 255), debug_rect, 1)
        
        debug_lines = [
            "主程式除錯 (F1關閉)",
            f"遊戲狀態: {self.game_state.current_state}",
            f"玩家位置: ({self.player.x}, {self.player.y})",
            f"玩家移動: {self.player.is_moving}",
            f"任何UI開啟: {self.ui.is_any_ui_open()}",
            f"背包: {self.ui.show_inventory}",
            f"地圖: {self.ui.show_map}",
            f"對話: {self.ui.dialogue_active}"
        ]
        
        y_offset = 305
        for line in debug_lines:
            if "True" in line and ("移動" in line or "開啟" in line):
                color = (255, 100, 100)
            elif self.ui.is_any_ui_open() and "UI開啟: True" in line:
                color = (255, 255, 100)
            else:
                color = (0, 255, 255)
                
            text_surface = font_manager.render_text(line, 12, color)
            self.screen.blit(text_surface, (15, y_offset))
            y_offset += 14
    
    def render_intro(self):
        intro_text = [
            "《末世第二餐廳》",
            "",
            "沒有人知道這一切是怎麼開始的。",
            "有一天，一種可怕的殭屍病毒突然席捲全球。",
            "只要被咬傷，感染者便會在三分鐘內失去理智...",
            "",
            "傳聞中，一群國立陽明交通大學的天才學生，",
            "憑著超凡的智慧，研發出了一種能夠治癒病毒的神秘藥劑。",
            "他們已將解藥藏於交大第二餐廳三樓的某個隱密角落...",
            "",
            "而你，作為同樣來自交大的普通學生，",
            "原本只是在便利商店買午餐，",
            "卻在殭屍攻進校園的瞬間被困其中。",
            "",
            "現在，全人類的命運，落在你手中。",
            "",
            "按 [空白鍵] 開始遊戲",
            "",
            "📋 遊戲操作:",
            "方向鍵移動，空白鍵互動，I背包，M地圖",
            "ESC強制關閉UI，F1除錯模式，F2重置狀態"
        ]
        
        y_offset = 30
        for line in intro_text:
            if line:
                if line.startswith("《"):
                    text_surface = font_manager.render_text(line, 28, (255, 255, 0))
                elif line.startswith("📋"):
                    text_surface = font_manager.render_text(line, 22, (100, 255, 100))
                elif line.startswith("方向鍵") or line.startswith("ESC"):
                    text_surface = font_manager.render_text(line, 18, (200, 200, 200))
                else:
                    text_surface = font_manager.render_text(line, 24, (255, 255, 255))
                    
                text_rect = text_surface.get_rect(center=(self.SCREEN_WIDTH//2, y_offset))
                self.screen.blit(text_surface, text_rect)
            y_offset += 25 if line.startswith("方向鍵") or line.startswith("ESC") else 30
    
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(self.FPS)
        
        pygame.quit()
        sys.exit()

    def restart_game(self):
        """重新開始遊戲"""
        print("🔄 重新開始遊戲...")
        
        # 重置玩家
        self.player.reset()
        
        # 重置UI
        if hasattr(self.ui, 'reset_game'):
            self.ui.reset_game()
        
        # 重置遊戲狀態
        if hasattr(self.game_state, 'reset'):
            self.game_state.reset()
        else:
            # 如果沒有reset方法，手動重置
            self.game_state.current_state = "exploration"
            self.game_state.player_stats = {
                "hp": 100,
                "max_hp": 100,
                "level": 1,
                "exp": 0
            }
        
        # 重置其他組件
        self.map_manager.current_floor = 1
        self.inventory = Inventory()  # 重新創建背包
        
        # 重置UI狀態
        self.ui.show_inventory = False
        self.ui.show_map = False
        self.ui.dialogue_active = False
        
        # 重新設定玩家參考（重要！）
        self.ui.set_player_reference(self.player)
        self.ui.set_game_state_reference(self.game_state)
        self.ui.set_inventory_reference(self.inventory)
        
        print("✅ 遊戲重置完成！")

def main():
    """程式入口點"""
    try:
        print("🎮 啟動《末世第二餐廳》(修復版)")
        print("💡 提示:")
        print("   F1 - 開啟/關閉除錯模式")
        print("   ESC - 強制關閉所有UI")
        print("   如果移動卡住，按ESC後再試")
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