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
from character_selector import CharacterSelector
from sound_manager import sound_manager 

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
        
        # 🆕 遊戲流程控制
        self.show_intro = True
        self.show_character_select = False
        self.character_selector = None
        self.selected_character = None
        self.game_started = False
        
        # 遊戲組件（稍後初始化）
        self.game_state = None
        self.map_manager = None
        self.player = None
        self.ui = None
        self.combat_system = None
        self.inventory = None
        
        # 遊戲標誌
        self.running = True
        
        # 互動冷卻機制
        self.last_interaction_time = 0
        self.interaction_cooldown = 0.5  # 0.5秒冷卻時間
        
        # 除錯模式
        self.debug_mode = False
        
        # 🎵 音樂系統相關
        self.current_game_mode = "intro"  # 追蹤當前遊戲模式
        self.last_game_mode = None        # 追蹤上一個模式，避免重複播放
        
        # 🎵 啟動介紹音樂
        sound_manager.play_music("intro", loop=True)

    def initialize_game_components(self):
        """🆕 在角色選擇完成後初始化遊戲組件"""
        print("🎮 初始化遊戲組件...")
        
        # 遊戲狀態
        self.game_state = GameState()
        
        # 🆕 根據選擇的角色設定玩家血量
        if self.selected_character:
            initial_hp = self.selected_character["stats"]["hp"]
            self.game_state.player_stats["hp"] = initial_hp
            self.game_state.player_stats["max_hp"] = initial_hp
            print(f"🎭 角色初始血量設定為: {initial_hp}")
        
        # 初始化遊戲組件
        self.map_manager = MapManager()
        self.player = Player(x=400, y=300, character_data=self.selected_character)
        self.ui = UI(self.screen)
        self.combat_system = CombatSystem()
        self.inventory = Inventory()
        
        self.ui.set_player_reference(self.player)
        self.ui.set_game_state_reference(self.game_state)
        self.ui.set_inventory_reference(self.inventory)
        
        # 🪜 樓梯圖片偵錯資訊
        if self.debug_mode:
            self.map_manager.debug_print_stairs()
            self.map_manager.debug_print_floor_info()
        
        # 🎵 切換到探索音樂
        self.set_game_mode("exploration")
        
        print("✅ 遊戲組件初始化完成")

    def set_game_mode(self, mode):
        """🆕 設定遊戲模式並播放對應音樂"""
        if self.current_game_mode != mode:
            self.last_game_mode = self.current_game_mode
            self.current_game_mode = mode
            
            # 播放對應的背景音樂
            if mode == "intro":
                sound_manager.play_music("intro", loop=True)
            elif mode == "character_select":
                sound_manager.play_music("character_select", loop=True)
            elif mode == "exploration":
                sound_manager.play_music("exploration", loop=True)
            elif mode == "combat":
                sound_manager.play_music("combat", loop=True)
            elif mode == "dialogue":
                # 對話時音量降低，但保持探索音樂
                sound_manager.set_music_volume(0.3)
            elif mode == "victory":
                sound_manager.play_music("victory", loop=False)
            elif mode == "game_over":
                sound_manager.play_music("game_over", loop=False)
            
            print(f"🎵 遊戲模式切換: {self.last_game_mode} → {mode}")

    def handle_events(self):
        """修復版事件處理 - 整合角色選擇 + 音樂控制"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                # ======= 全域快捷鍵 - 任何狀態下都優先處理 =======
                if event.key == pygame.K_ESCAPE:
                    if self.show_intro:
                        # 在介紹畫面按ESC直接退出
                        self.running = False
                    elif self.show_character_select:
                        # 在角色選擇畫面按ESC選擇預設角色
                        self.character_selector.handle_event(event)
                    elif self.game_started:
                        # 遊戲中按ESC處理
                        if self.game_state.current_state == "combat":
                            print("🆘 ESC強制退出戰鬥")
                            self.force_end_combat()
                        else:
                            self.force_exploration_state()
                    continue
                elif event.key == pygame.K_r and self.game_started:
                    # R鍵: 重新開始遊戲
                    if hasattr(self.ui, 'game_over') and hasattr(self.ui, 'game_completed'):
                        if self.ui.game_over or self.ui.game_completed:
                            self.restart_game()
                    continue
                elif self.game_started and event.key == pygame.K_i:
                    # I鍵: 背包切換
                    self.handle_inventory_toggle()
                    continue
                elif self.game_started and event.key == pygame.K_m:
                    # M鍵: 地圖切換
                    self.handle_map_toggle()
                    continue
                # 🎵 音樂控制快捷鍵
                elif event.key == pygame.K_F6:
                    # F6: 切換背景音樂
                    music_status = sound_manager.toggle_music()
                    if self.game_started:
                        self.ui.show_message(f"🎵 背景音樂: {'開啟' if music_status else '關閉'}")
                    continue
                elif event.key == pygame.K_F7:
                    # F7: 切換音效
                    sfx_status = sound_manager.toggle_sfx()
                    if self.game_started:
                        self.ui.show_message(f"🔊 音效: {'開啟' if sfx_status else '關閉'}")
                    continue
                elif event.key == pygame.K_F8:
                    # F8: 調整音樂音量
                    current_volume = sound_manager.music_volume
                    new_volume = 0.2 if current_volume >= 0.8 else current_volume + 0.2
                    sound_manager.set_music_volume(new_volume)
                    if self.game_started:
                        self.ui.show_message(f"🎵 音樂音量: {int(new_volume * 100)}%")
                    continue
                elif event.key == pygame.K_F9:
                    # F9: 調整音效音量
                    current_volume = sound_manager.sfx_volume
                    new_volume = 0.2 if current_volume >= 0.8 else current_volume + 0.2
                    sound_manager.set_sfx_volume(new_volume)
                    if self.game_started:
                        self.ui.show_message(f"🔊 音效音量: {int(new_volume * 100)}%")
                    continue
                # 除錯快捷鍵（只在遊戲開始後）
                elif self.game_started and event.key == pygame.K_F1:
                    self.toggle_debug_mode()
                    continue
                elif self.game_started and event.key == pygame.K_F2:
                    self.force_exploration_state()
                    continue
                elif self.game_started and event.key == pygame.K_F3:
                    self.reset_player_position()
                    continue
                elif self.game_started and event.key == pygame.K_F4:
                    self.reload_stairs_images()
                    continue
                elif self.game_started and event.key == pygame.K_F5:
                    self.map_manager.debug_print_stairs()
                    continue
                elif self.game_started and event.key == pygame.K_F10:
                    self.reload_shop_images()
                    continue
                elif self.game_started and event.key == pygame.K_F11:
                    self.map_manager.debug_print_shop_info()
                    continue
                elif self.game_started and event.key == pygame.K_F12:
                    self.toggle_combat_zone_debug()
                    continue
                
                # ======= 狀態專用事件處理 =======
                if self.show_intro:
                    if event.key == pygame.K_SPACE:
                        self.show_intro = False
                        self.show_character_select = True
                        # 🆕 創建角色選擇器
                        self.character_selector = CharacterSelector(self.screen)
                        # 🎵 切換到角色選擇音樂
                        self.set_game_mode("character_select")
                        print("🎭 進入角色選擇畫面")
                elif self.show_character_select:
                    # 🆕 角色選擇事件處理
                    self.character_selector.handle_event(event)
                    if self.character_selector.is_selection_complete():
                        self.selected_character = self.character_selector.get_selected_character()
                        self.show_character_select = False
                        self.game_started = True
                        self.initialize_game_components()
                        print(f"🎉 角色選擇完成，開始遊戲: {self.selected_character['name']}")
                elif self.game_started:
                    if self.game_state.current_state == "exploration":
                        self.handle_exploration_input(event)
                    elif self.game_state.current_state == "combat":
                        self.handle_combat_input(event)
                    elif self.game_state.current_state == "dialogue":
                        self.handle_dialogue_input(event)

    def toggle_combat_zone_debug(self):
        """🆕 切換戰鬥區域除錯顯示"""
        debug_status = self.map_manager.toggle_combat_zone_debug()
        if debug_status:
            self.ui.show_message("🔧 戰鬥區域除錯: 開啟 (可看到紅色危險區域)")
        else:
            self.ui.show_message("🔧 戰鬥區域除錯: 關閉 (危險區域隱藏)")
        
        if self.debug_mode:
            self.map_manager.debug_print_combat_zones()

    def reload_stairs_images(self):
        """重新載入樓梯圖片"""
        print("🔄 手動重新載入樓梯圖片...")
        self.map_manager.reload_stairs_images()
        if self.debug_mode:
            self.map_manager.debug_print_stairs()

    def reload_shop_images(self):
        """🆕 重新載入商店圖片"""
        print("🔄 手動重新載入商店圖片...")
        self.map_manager.reload_shop_images()
        if self.debug_mode:
            self.map_manager.debug_print_shop_info()
        self.ui.show_message("商店圖片已重新載入！")

    def handle_inventory_toggle(self):
        """處理背包切換 - 修復版"""
        old_state = self.ui.show_inventory
        self.ui.toggle_inventory()
        
        # 🎵 播放互動音效
        sound_manager.play_sfx("interact")
        
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
        
        # 🎵 播放互動音效
        sound_manager.play_sfx("interact")
        
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
        self.ui.close_all_ui()
        
        # 🎵 確保探索音樂播放
        self.set_game_mode("exploration")
        
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
        """切換除錯模式 - 增強版"""
        self.debug_mode = not self.debug_mode
        # 🔧 同時切換移動除錯
        if self.player:
            self.player.debug_movement = self.debug_mode
        
        print(f"🔧 除錯模式: {'開啟' if self.debug_mode else '關閉'}")
        if self.debug_mode:
            self.print_debug_info()
            self.map_manager.debug_print_stairs()
            self.map_manager.debug_print_items()
            self.map_manager.debug_print_floor_info()
            self.map_manager.debug_print_combat_zones()
            if self.player:
                print(f"🚶 移動除錯: 開啟 (角色: {self.player.character_name})")
            # 🎵 顯示音效系統狀態
            status = sound_manager.get_status()
            print(f"🎵 音效系統狀態: {status}")

    def print_debug_info(self):
        """顯示除錯資訊"""
        print(f"🔍 當前狀態:")
        print(f"   遊戲狀態: {self.game_state.current_state}")
        print(f"   UI狀態: {self.ui.get_ui_status()}")
        print(f"   玩家位置: ({self.player.x}, {self.player.y})")
        print(f"   玩家移動: {self.player.is_moving}")
        print(f"   當前樓層: {self.map_manager.current_floor}")
        print(f"   戰鬥區域除錯: {self.map_manager.debug_show_combat_zones}")
        print(f"   選擇角色: {self.player.get_character_name()}")
        print(f"   🎵 當前音樂模式: {self.current_game_mode}")

    def reset_player_position(self):
        """重置玩家位置"""
        old_pos = (self.player.x, self.player.y)
        self.player.set_position(400, 300)
        # 🎵 播放移動音效
        sound_manager.play_sfx("move")
        print(f"🔄 重置玩家位置: {old_pos} → (400, 300)")

    def handle_exploration_input(self, event):
        """處理探索模式的輸入 - 修復版 + 音效"""
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
        
        # 🎵 播放移動音效
        if movement_successful:
            sound_manager.play_sfx("move")
        
        # 除錯資訊
        if self.debug_mode and event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
            if movement_successful:
                print(f"✅ 移動開始: 目標({self.player.move_target_x}, {self.player.move_target_y})")
            else:
                print(f"❌ 移動被拒絕: 可能正在移動中或邊界限制")

    def handle_combat_input(self, event):
        """處理戰鬥輸入 - 修復音效版"""
        key_name = pygame.key.name(event.key)
        print(f"⚔️ 戰鬥按鍵: {key_name}")
        
        # 如果戰鬥已經有結果，立即結束
        if self.combat_system.combat_result:
            print(f"⚠️ 戰鬥已有結果: {self.combat_system.combat_result}")
            self.handle_combat_end()
            return
        
        # 🔧 修復：確保音效系統正常
        print(f"🔊 音效系統狀態: 音效開啟={sound_manager.is_sfx_enabled}, 音量={sound_manager.sfx_volume}")
        
        # 檢查是否是正確的數字鍵並執行行動
        if event.key == pygame.K_1:
            print("🗡️ 選擇攻擊")
            # 🎵 戰鬥音效：確保播放
            print("🔊 嘗試播放 combat_hit 音效...")
            try:
                sound_manager.play_sfx("combat_hit")
                print("✅ combat_hit 音效播放指令已發送")
            except Exception as e:
                print(f"❌ combat_hit 音效播放失敗: {e}")
            
            # 執行戰鬥行動
            self.combat_system.player_action("attack")
            
        elif event.key == pygame.K_2:
            print("🛡️ 選擇防禦")
            # 🎵 防禦音效
            print("🔊 嘗試播放 combat_defend 音效...")
            try:
                sound_manager.play_sfx("combat_defend")
                print("✅ combat_defend 音效播放指令已發送")
            except Exception as e:
                print(f"❌ combat_defend 音效播放失敗: {e}")
            
            self.combat_system.player_action("defend")
            
        elif event.key == pygame.K_3:
            print("🏃 選擇逃跑")
            # 🎵 移動音效
            print("🔊 嘗試播放 move 音效...")
            try:
                sound_manager.play_sfx("move")
                print("✅ move 音效播放指令已發送")
            except Exception as e:
                print(f"❌ move 音效播放失敗: {e}")
            
            self.combat_system.player_action("escape")
        else:
            return
        
        # 行動後立即檢查結果
        if self.combat_system.combat_result:
            print(f"🎯 行動後立即檢測到結果: {self.combat_system.combat_result}")
            self.handle_combat_end()

    def handle_combat_end(self):
        """處理戰鬥結束 - 統一處理方法 + 音效"""
        if not self.combat_system.combat_result:
            return
        
        result = self.combat_system.combat_result
        print(f"🏁 處理戰鬥結束: {result}")
        
        try:
            if result == "win":
                print("✅ 處理戰鬥勝利")
                sound_manager.play_sfx("success")  # 🎵 勝利音效
                self.ui.show_message("戰鬥勝利！獲得經驗值！")
                
                # 勝利時移除戰鬥區域並給予獎勵
                if hasattr(self, 'current_combat_zone'):
                    zone = self.current_combat_zone
                    floor = self.map_manager.current_floor
                    
                    # 移除戰鬥區域
                    if hasattr(self.map_manager, 'remove_combat_zone'):
                        self.map_manager.remove_combat_zone(zone, floor)
                        print(f"🗑️ 勝利！移除戰鬥區域: {zone['name']}")
                    
                    # 給予經驗值
                    if hasattr(self.game_state, 'player_stats') and self.combat_system.current_enemy:
                        exp_gain = self.combat_system.current_enemy.get("exp_reward", 10)
                        self.game_state.player_stats["exp"] += exp_gain
                        print(f"🎯 獲得 {exp_gain} 經驗值")
                
            elif result == "escape":
                print("🏃 處理逃跑成功")
                sound_manager.play_sfx("success")  # 🎵 成功音效
                self.ui.show_message("成功逃離了危險區域！")
                
                # 🔥 關鍵：逃跑時也移除戰鬥區域 🔥
                if hasattr(self, 'current_combat_zone'):
                    zone = self.current_combat_zone
                    floor = self.map_manager.current_floor
                    
                    # 移除戰鬥區域
                    if hasattr(self.map_manager, 'remove_combat_zone'):
                        self.map_manager.remove_combat_zone(zone, floor)
                        print(f"🗑️ 逃跑成功！移除戰鬥區域: {zone['name']}")
                    else:
                        print("⚠️ map_manager 沒有 remove_combat_zone 方法")
                
            elif result == "lose":
                print("💀 處理戰鬥失敗")
                sound_manager.play_sfx("error")  # 🎵 失敗音效
                self.ui.show_message("你被擊敗了...")
        
        except Exception as e:
            print(f"❌ 處理戰鬥結果錯誤: {e}")
        
        # 🔥 關鍵：立即重置所有戰鬥狀態 🔥
        print("🔄 立即重置戰鬥狀態")
        self.combat_system.in_combat = False
        self.combat_system.combat_result = None
        self.combat_system.current_enemy = None
        self.combat_system.player_turn = True
        self.combat_system.animation_timer = 0
        if hasattr(self.combat_system, 'combat_log'):
            self.combat_system.combat_log = []
        
        # 設定遊戲狀態
        self.game_state.current_state = "exploration"
        
        # 🎵 回到探索音樂
        self.set_game_mode("exploration")
        
        # 清除戰鬥區域記錄
        if hasattr(self, 'current_combat_zone'):
            self.current_combat_zone = None
        
        print("✅ 戰鬥完全結束，立即回到探索狀態")

    def force_end_combat(self):
        """強制結束戰鬥 - 緊急版"""
        print("💥 強制結束戰鬥！")
        
        # 顯示結果訊息
        result = getattr(self.combat_system, 'combat_result', None)
        if result == "win":
            sound_manager.play_sfx("success")
            self.ui.show_message("戰鬥勝利！")
        elif result == "escape":
            sound_manager.play_sfx("success")
            self.ui.show_message("逃跑成功！")
        elif result == "lose":
            sound_manager.play_sfx("error")
            self.ui.show_message("戰鬥失敗！")
        else:
            sound_manager.play_sfx("error")
            self.ui.show_message("強制退出戰鬥！")
        
        # 立即重置所有戰鬥狀態
        self.combat_system.in_combat = False
        self.combat_system.combat_result = None
        self.combat_system.current_enemy = None
        self.combat_system.player_turn = True
        self.combat_system.animation_timer = 0
        
        # 強制設定為探索狀態
        self.game_state.current_state = "exploration"
        
        # 🎵 回到探索音樂
        self.set_game_mode("exploration")
        
        # 清除戰鬥區域
        if hasattr(self, 'current_combat_zone'):
            self.current_combat_zone = None
        
        print("✅ 強制結束完成，回到探索狀態")

    def handle_dialogue_input(self, event):
        """處理對話輸入 + 音效"""
        # 🎵 播放對話音效
        sound_manager.play_sfx("dialogue_beep")
        
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
        """檢查對話是否結束，恢復exploration狀態 + 音樂"""
        if not self.ui.dialogue_active:
            self.game_state.current_state = "exploration"
            # 🎵 對話結束，恢復探索音樂音量
            self.set_game_mode("exploration")
            if self.debug_mode:
                print("💬 對話結束，回到exploration狀態")

    def interact(self):
        """互動處理 + 音效"""
        # 檢查互動冷卻
        current_time = time.time()
        if current_time - self.last_interaction_time < self.interaction_cooldown:
            if self.debug_mode:
                print(f"⏰ 互動冷卻中，還需等待 {self.interaction_cooldown - (current_time - self.last_interaction_time):.1f} 秒")
            return
        
        # 檢查玩家附近是否有可互動物件
        current_floor = self.map_manager.get_current_floor()
        
        # 🔧 修復：優先檢查物品收集
        item_pickup = self.map_manager.check_item_pickup(
            self.player.x, self.player.y, current_floor
        )
        
        if item_pickup:
            self.collect_item_new(item_pickup)
            self.last_interaction_time = current_time
            return
        
        # 然後檢查其他互動物件
        interaction = self.map_manager.check_interaction(
            self.player.x, self.player.y, current_floor
        )
        
        if self.debug_mode:
            print(f"🔍 檢查互動: 樓層{current_floor}, 位置({self.player.x}, {self.player.y})")
        
        if interaction:
            if self.debug_mode:
                print(f"✅ 找到互動物件: {interaction}")
            self.last_interaction_time = current_time
            
            # 🎵 播放互動音效
            sound_manager.play_sfx("interact")
            
            if interaction["type"] == "shop":
                self.start_shop_interaction(interaction)
            elif interaction["type"] == "npc":
                self.start_npc_dialogue(interaction)
            elif interaction["type"] == "stairs":
                self.use_stairs(interaction)
        else:
            # 🎵 播放錯誤音效 (沒有可互動物件)
            sound_manager.play_sfx("error")
            if self.debug_mode:
                print("❌ 附近沒有可互動的物件")

    def collect_item_new(self, item_pickup):
        """🆕 新的物品收集方法 + 音效"""
        item = item_pickup["item"]
        item_id = item_pickup["item_id"]
        
        if self.debug_mode:
            print(f"📦 收集物品: {item['name']} (ID: {item_id})")
        
        # 嘗試添加到背包
        success = self.inventory.add_item(item)
        
        if success:
            # 🎵 播放收集音效
            sound_manager.play_sfx("collect_item")
            
            # 標記為已收集
            self.map_manager.collect_item(item_id)
            
            # 根據物品類型顯示不同訊息
            if item["type"] == "healing":
                self.ui.show_message(f"獲得了 {item['name']}！回復 {item.get('value', 0)} 血量")
            elif item["type"] == "key":
                self.ui.show_message(f"獲得了 {item['name']}！這看起來很重要")
                # 設定UI標記（如果需要的話）
                if item["name"] == "鑰匙卡":
                    self.ui.has_keycard = True
            elif item["type"] == "special":
                # 🎵 特殊物品播放成功音效
                sound_manager.play_sfx("success")
                self.ui.show_message(f"🎉 獲得了 {item['name']}！這可能是關鍵物品！")
                if item["name"] == "解藥":
                    self.ui.has_antidote = True
                    self.ui.show_message("🎊 恭喜！你找到了拯救世界的解藥！")
                    # 🎵 找到解藥，檢查勝利條件
                    self.check_victory_condition()
            elif item["type"] == "clue":
                self.ui.show_message(f"獲得了 {item['name']}！這提供了重要線索")
            else:
                self.ui.show_message(f"獲得了 {item['name']}！")
            
            # 給予經驗值獎勵
            exp_reward = self.get_item_exp_reward(item)
            if exp_reward > 0:
                self.game_state.add_exp(exp_reward)
                # 🎵 檢查是否升級
                if hasattr(self.game_state, 'just_leveled_up') and self.game_state.just_leveled_up:
                    sound_manager.play_sfx("level_up")
                    self.game_state.just_leveled_up = False  # 重置升級標記
                if self.debug_mode:
                    print(f"🎯 收集物品獲得 {exp_reward} 經驗值")
            
            if self.debug_mode:
                print(f"✅ 成功收集: {item['name']}")
                print(f"   背包物品數: {len(self.inventory.get_items())}")
                print(f"   玩家經驗: {self.game_state.player_stats['exp']}")
                
        else:
            # 🎵 播放錯誤音效 (背包已滿)
            sound_manager.play_sfx("error")
            self.ui.show_message("背包已滿！無法收集更多物品")
            if self.debug_mode:
                print(f"❌ 背包已滿，無法收集: {item['name']}")

    def get_item_exp_reward(self, item):
        """🆕 根據物品類型計算經驗值獎勵"""
        exp_rewards = {
            "healing": 5,
            "key": 20,
            "special": 50,
            "clue": 15
        }
        return exp_rewards.get(item["type"], 3)

    def collect_item(self, item_info):
        """舊的物品收集方法（保持兼容性）"""
        if self.debug_mode:
            print(f"📦 使用舊版收集方法: {item_info}")
        
        # 如果是新格式，轉換為舊格式處理
        if "item" in item_info and "item_id" in item_info:
            self.collect_item_new(item_info)
        else:
            # 舊格式處理
            success = self.inventory.add_item(item_info["item"])
            if success:
                sound_manager.play_sfx("collect_item")
                self.ui.show_message(f"獲得了 {item_info['item']['name']}")
                self.map_manager.remove_item(item_info["item"])
                if self.debug_mode:
                    print(f"✅ 成功收集: {item_info['item']['name']}")
            else:
                sound_manager.play_sfx("error")
                self.ui.show_message("背包已滿！")
                if self.debug_mode:
                    print(f"❌ 背包已滿，無法收集: {item_info['item']['name']}")

    def start_shop_interaction(self, shop_info):
        """開始商店互動 + 音樂"""
        if self.debug_mode:
            print(f"🏪 進入商店: {shop_info['name']}")
        
        # 檢查是否已經在對話中
        if self.game_state.current_state == "dialogue" or self.ui.dialogue_active:
            if self.debug_mode:
                print("⚠️ 已經在對話中，忽略商店互動")
            return
        
        self.game_state.set_state("dialogue")
        # 🎵 進入對話模式 (降低音樂音量)
        self.set_game_mode("dialogue")
        self.ui.start_dialogue(shop_info)

    def start_npc_dialogue(self, npc_info):
        """開始NPC對話 + 音樂"""
        if self.debug_mode:
            print(f"👤 與NPC對話: {npc_info['name']}")
        
        # 檢查是否已經在對話中
        if self.game_state.current_state == "dialogue" or self.ui.dialogue_active:
            if self.debug_mode:
                print("⚠️ 已經在對話中，忽略NPC互動")
            return
        
        self.game_state.set_state("dialogue")
        # 🎵 進入對話模式 (降低音樂音量)
        self.set_game_mode("dialogue")
        self.ui.start_dialogue(npc_info)

    def use_stairs(self, stairs_info):
        """使用樓梯 - 增強版 + 音效"""
        if self.debug_mode:
            print(f"🪜 使用樓梯: {stairs_info}")
        
        # 🎵 播放樓梯音效
        sound_manager.play_sfx("stairs")
        
        direction = stairs_info["direction"]
        current_floor = self.map_manager.current_floor
        target_floor = stairs_info.get("target_floor")
        
        if self.debug_mode:
            print(f"   方向: {direction}, 當前樓層: {current_floor}, 目標樓層: {target_floor}")
        
        if direction == "up":
            if current_floor == 1 and target_floor == 2:
                # 1樓到2樓：自由通行
                self.map_manager.change_floor(2)
                self.player.set_position(450, 600)  # 樓梯底部
                if self.debug_mode:
                    print("⬆️ 上樓到 2 樓")
                self.ui.show_message("來到了二樓")
            elif current_floor == 2 and target_floor == 3:
                # 2樓到3樓：需要鑰匙卡
                if self.game_state.get_flag("has_keycard") or self.inventory.has_item("鑰匙卡") or self.ui.has_keycard:
                    # 🎵 成功使用鑰匙卡
                    sound_manager.play_sfx("door")
                    self.map_manager.change_floor(3)
                    self.player.set_position(450, 600)
                    if self.debug_mode:
                        print("⬆️ 使用鑰匙卡上樓到 3 樓")
                    self.ui.show_message("🗝️ 使用鑰匙卡進入三樓！")
                    # 設定標記
                    self.game_state.set_flag("unlocked_third_floor", True)
                else:
                    # 🎵 錯誤音效 (沒有鑰匙卡)
                    sound_manager.play_sfx("error")
                    if self.debug_mode:
                        print("🚫 需要鑰匙卡才能上三樓")
                    self.ui.show_message("❌ 需要鑰匙卡才能進入三樓！")
            else:
                sound_manager.play_sfx("error")
                if self.debug_mode:
                    print("🚫 已經在最高樓層或無效目標")
                self.ui.show_message("已經是最高樓層了")
        elif direction == "down":
            if current_floor == 3 and target_floor == 2:
                # 3樓到2樓
                self.map_manager.change_floor(2)
                self.player.set_position(450, 100)  # 樓梯頂部
                if self.debug_mode:
                    print("⬇️ 下樓到 2 樓")
                self.ui.show_message("回到了二樓")
            elif current_floor == 2 and target_floor == 1:
                # 2樓到1樓
                self.map_manager.change_floor(1)
                self.player.set_position(450, 100)
                if self.debug_mode:
                    print("⬇️ 下樓到 1 樓")
                self.ui.show_message("回到了一樓")
            else:
                sound_manager.play_sfx("error")
                if self.debug_mode:
                    print("🚫 已經在最低樓層或無效目標")
                self.ui.show_message("已經是最低樓層了")

    def start_combat_in_zone(self, combat_zone):
        """在戰鬥區域開始戰鬥 + 音樂"""
        print(f"🔄 準備切換到戰鬥狀態")
        print(f"   當前遊戲狀態: {self.game_state.current_state}")
        
        self.game_state.current_state = "combat"
        # 🎵 切換到戰鬥音樂
        self.set_game_mode("combat")
        print(f"   設定後遊戲狀態: {self.game_state.current_state}")
        
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
        
        print(f"⚔️ 開始戰鬥: {enemy['name']} in {combat_zone['name']}")
        print(f"   戰鬥前 combat_system.in_combat: {self.combat_system.in_combat}")
        
        self.combat_system.start_combat(enemy)
        
        print(f"   戰鬥後 combat_system.in_combat: {self.combat_system.in_combat}")
        print(f"   戰鬥後 player_turn: {self.combat_system.player_turn}")

    def check_victory_condition(self):
        """檢查勝利條件 + 音樂"""
        if (self.ui.has_antidote and 
            self.game_state.player_stats["level"] >= 3 and 
            self.game_state.player_stats["hp"] >= 50):
            self.ui.game_completed = True
            # 🎵 播放勝利音樂
            self.set_game_mode("victory")
            self.ui.show_message("🎉 恭喜！你成功找到解藥並拯救了所有人！遊戲完成！")
        elif self.ui.has_antidote:
            self.ui.show_message("你有解藥了！但還需要更強的實力才能完成任務...")

    def update(self):
        if self.show_character_select:
            # 🆕 更新角色選擇器
            self.character_selector.update()
        elif self.game_started:
            if self.game_state.current_state == "combat":
                # 戰鬥狀態更新
                self.combat_system.update(self.game_state)
                
                # 檢查戰鬥是否結束（通過戰鬥結果）
                if self.combat_system.combat_result:
                    self.handle_combat_end()
                    
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
            
    def render(self):
        self.screen.fill((0, 0, 0))
        
        if self.show_intro:
            self.render_intro()
        elif self.show_character_select:
            # 🆕 渲染角色選擇畫面
            self.character_selector.render()
        elif self.game_started:
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

    def render_debug_info(self):
        """渲染除錯資訊 + 音效狀態"""
        debug_rect = pygame.Rect(10, 300, 400, 300)  # 🆕 增加寬度和高度以容納音效資訊
        pygame.draw.rect(self.screen, (0, 0, 0, 180), debug_rect)
        pygame.draw.rect(self.screen, (0, 255, 255), debug_rect, 1)
        
        debug_lines = [
            "主程式除錯 (F1關閉)",
            f"遊戲狀態: {self.game_state.current_state}",
            f"玩家位置: ({self.player.x}, {self.player.y})",
            f"玩家移動: {self.player.is_moving}",
            f"當前樓層: {self.map_manager.current_floor}",
            f"任何UI開啟: {self.ui.is_any_ui_open()}",
            f"背包: {self.ui.show_inventory}",
            f"地圖: {self.ui.show_map}",
            f"對話: {self.ui.dialogue_active}",
            f"樓梯圖片: {self.map_manager.use_sprites}",
            f"地板圖片: {self.map_manager.use_floor_sprites}",
            f"商店圖片: {self.map_manager.use_shop_sprites}",
            f"戰鬥區域除錯: {self.map_manager.debug_show_combat_zones}",
            f"已收集物品: {len(self.map_manager.collected_items)}",
            f"🎭 角色: {self.player.get_character_name()}",
            f"角色屬性: {self.player.get_character_stats()}",
            f"🎵 當前音樂模式: {self.current_game_mode}",
            f"🎵 音樂開啟: {sound_manager.is_music_enabled}",
            f"🔊 音效開啟: {sound_manager.is_sfx_enabled}",
            f"🎵 音樂音量: {int(sound_manager.music_volume * 100)}%",
            f"🔊 音效音量: {int(sound_manager.sfx_volume * 100)}%",
            f"🎵 正在播放: {pygame.mixer.music.get_busy()}",
            f"🔊 已載入音效: {len(sound_manager.loaded_sfx)}"
        ]
        
        y_offset = 305
        for line in debug_lines:
            if "True" in line and ("移動" in line or "開啟" in line):
                color = (255, 100, 100)
            elif "樓梯圖片: True" in line or "地板圖片: True" in line:
                color = (0, 255, 0)
            elif "樓梯圖片: False" in line or "地板圖片: False" in line:
                color = (255, 255, 0)
            elif "商店圖片: True" in line:
                color = (0, 255, 0)
            elif "商店圖片: False" in line:
                color = (255, 255, 0)
            elif "戰鬥區域除錯: True" in line:
                color = (255, 100, 100)
            elif "戰鬥區域除錯: False" in line:
                color = (100, 255, 100)
            elif "已收集物品:" in line:
                color = (255, 200, 100)
            elif "🎭 角色:" in line:
                color = (255, 150, 255)
            elif "角色屬性:" in line:
                color = (150, 255, 150)
            elif "🎵" in line or "🔊" in line:  # 🆕 音效相關資訊顏色
                if "True" in line or "開啟" in line:
                    color = (100, 255, 255)  # 青色表示開啟
                elif "False" in line or "關閉" in line:
                    color = (255, 100, 255)  # 紫色表示關閉
                else:
                    color = (255, 255, 100)  # 黃色表示數值
            elif self.ui.is_any_ui_open() and "UI開啟: True" in line:
                color = (255, 255, 100)
            else:
                color = (0, 255, 255)
            
            text_surface = font_manager.render_text(line, 12, color)
            self.screen.blit(text_surface, (15, y_offset))
            y_offset += 13

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
            "按 [空白鍵] 進入角色選擇",
            "",
            "📋 遊戲操作:",
            "方向鍵 移動，空白鍵 互動，I 背包，M 地圖",
            "",
            "🎵 音效控制:",
            "F6 音樂開關，F7 音效開關，F8 音樂音量，F9 音效音量"
        ]
        
        # 計算總高度來實現垂直置中，並往上調一行
        total_lines = len([line for line in intro_text if line])  # 非空行數
        line_height = 32  # 平均行高
        total_height = total_lines * line_height
        
        # 垂直置中起始位置，往上調兩行 (減少64像素)
        start_y = (self.SCREEN_HEIGHT - total_height) // 2 - 64
        y_offset = start_y
        
        for line in intro_text:
            if line:
                # 根據內容類型設定字體大小和顏色
                if line.startswith("《"):
                    text_surface = font_manager.render_text(line, 36, (255, 255, 0))
                    line_spacing = 50
                elif line.startswith("📋") or line.startswith("🎵"):
                    text_surface = font_manager.render_text(line, 24, (100, 255, 100))
                    line_spacing = 35
                elif line.startswith("方向鍵") or line.startswith("F6"):
                    text_surface = font_manager.render_text(line, 20, (200, 200, 200))
                    line_spacing = 25
                elif line.startswith("按"):
                    text_surface = font_manager.render_text(line, 26, (255, 255, 100))
                    line_spacing = 40
                else:
                    text_surface = font_manager.render_text(line, 22, (255, 255, 255))
                    line_spacing = 28
                
                # 水平置中
                text_rect = text_surface.get_rect(center=(self.SCREEN_WIDTH//2, y_offset))
                self.screen.blit(text_surface, text_rect)
                
                y_offset += line_spacing
            else:
                # 空行增加間距
                y_offset += 15

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(self.FPS)
        
        # 🎵 遊戲結束時清理音效系統
        sound_manager.cleanup()
        pygame.quit()
        sys.exit()

    def restart_game(self):
        """重新開始遊戲 - 🆕 支援角色選擇重置 + 音樂重置"""
        print("🔄 重新開始遊戲...")
        
        # 🆕 重置流程控制
        self.show_intro = True
        self.show_character_select = False
        self.game_started = False
        self.selected_character = None
        
        # 🎵 重置音樂模式
        self.current_game_mode = "intro"
        self.last_game_mode = None
        sound_manager.play_music("intro", loop=True)
        
        # 清理角色選擇器
        if self.character_selector:
            self.character_selector = None
        
        # 重置遊戲組件（如果已初始化）
        if self.game_started and self.player:
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
                    "attack": 10,
                    "defense": 5,
                    "level": 1,
                    "exp": 0
                }
            
            # 重置其他組件
            self.map_manager.current_floor = 1
            self.map_manager.reset_items()
            self.map_manager.debug_show_combat_zones = False
            self.inventory = Inventory()
            
            # 重置UI狀態
            self.ui.show_inventory = False
            self.ui.show_map = False
            self.ui.dialogue_active = False
            self.ui.has_keycard = False
            self.ui.has_antidote = False
            self.ui.game_completed = False
            self.ui.game_over = False
        
        print("✅ 遊戲重置完成！將重新開始角色選擇流程")


def main():
    """程式入口點"""
    try:
        print("🎮 啟動《末世第二餐廳》(完整修復版 + 角色選擇系統 + 音樂系統)")
        print("=" * 80)
        print("💡 遊戲功能:")
        print("   ✅ 樓梯圖片支援 (F4重新載入)")
        print("   ✅ 地板圖片支援 (F8重新載入)")
        print("   ✅ 物品收集系統修復 (F6除錯)")
        print("   ✅ 戰鬥系統完整")
        print("   ✅ UI互動修復")
        print("   ✅ 中文字體支援")
        print("   🆕 隱藏戰鬥區域 (F12切換除錯顯示)")
        print("   🎭 角色選擇系統 - 全新功能！")
        print("   🎵 動態音樂系統 - 超級新功能！")
        print("")
        print("🎵 音樂系統特色:")
        print("   - 不同遊戲狀態播放不同背景音樂")
        print("   - 豐富的音效反饋系統")
        print("   - 可調整音量和開關控制")
        print("   - 智能音樂切換 (對話時降低音量)")
        print("   - 戰鬥、探索、勝利等不同場景音樂")
        print("")
        print("🎯 音樂文件結構:")
        print("   assets/sounds/")
        print("   ├── intro_music.mp3          (開場音樂)")
        print("   ├── character_select.mp3     (角色選擇音樂)")
        print("   ├── exploration_music.mp3    (探索音樂)")
        print("   ├── combat_music.mp3         (戰鬥音樂)")
        print("   ├── dialogue_music.mp3       (對話音樂)")
        print("   ├── victory_music.mp3        (勝利音樂)")
        print("   ├── game_over_music.mp3      (遊戲結束音樂)")
        print("   └── 音效檔案...")
        print("")
        print("🔊 音效文件結構:")
        print("   assets/sounds/")
        print("   ├── move.wav                 (移動音效)")
        print("   ├── interact.wav             (互動音效)")
        print("   ├── collect_item.wav         (收集物品音效)")
        print("   ├── combat_hit.wav           (攻擊音效)")
        print("   ├── combat_defend.wav        (防禦音效)")
        print("   ├── level_up.wav             (升級音效)")
        print("   ├── dialogue_beep.wav        (對話嗶嗶聲)")
        print("   ├── error.wav                (錯誤音效)")
        print("   ├── success.wav              (成功音效)")
        print("   ├── stairs.wav               (樓梯音效)")
        print("   └── door.wav                 (開門音效)")
        print("")
        print("🎯 角色選擇系統:")
        print("   - 三種不同的角色皮膚可供選擇")
        print("   - 每個角色有不同的屬性和外觀")
        print("   - 支援圖片和程式繪製雙重模式")
        print("   - 滑鼠點擊或鍵盤操作都可以")
        print("")
        print("🎯 音樂控制快捷鍵:")
        print("   F6 - 切換背景音樂開關")
        print("   F7 - 切換音效開關")
        print("   F8 - 調整音樂音量 (20% → 40% → 60% → 80% → 100% → 20%)")
        print("   F9 - 調整音效音量 (20% → 40% → 60% → 80% → 100% → 20%)")
        print("")
        print("🎯 快捷鍵說明:")
        print("   F1 - 開啟/關閉除錯模式")
        print("   F2 - 強制重置遊戲狀態")
        print("   F3 - 重置玩家位置")
        print("   F4 - 重新載入樓梯圖片")
        print("   F5 - 顯示樓梯除錯資訊")
        print("   F10 - 重新載入商店圖片")
        print("   F11 - 顯示商店圖片除錯資訊")
        print("   F12 - 切換戰鬥區域除錯顯示")
        print("   ESC - 強制關閉所有UI / 退出")
        print("   I - 背包, M - 地圖, R - 重新開始(遊戲結束時)")
        print("")
        print("🎯 角色選擇操作:")
        print("   ← → 選擇角色")
        print("   空白鍵/Enter 確認選擇")
        print("   滑鼠點擊角色卡片直接選擇")
        print("   ESC 選擇預設角色並開始遊戲")
        print("")
        print("🎭 角色屬性:")
        print("   學生A: HP=100, 速度=8 (平衡型)")
        print("   學生B: HP=120, 速度=10 (運動型)")
        print("   學生C: HP=90, 速度=8 (理工型，修復移動問題)")
        print("")
        print("🎵 音效系統特色:")
        print("   - 移動時播放腳步聲")
        print("   - 互動時播放點擊音效")
        print("   - 收集物品時播放收集音效")
        print("   - 戰鬥中播放攻擊/防禦音效")
        print("   - 升級時播放升級音效")
        print("   - 對話時播放嗶嗶聲")
        print("   - 錯誤操作時播放錯誤音效")
        print("   - 成功操作時播放成功音效")
        print("   - 使用樓梯時播放樓梯音效")
        print("   - 開門時播放開門音效")
        print("")
        print("🎼 音樂系統智能功能:")
        print("   - 根據遊戲狀態自動切換音樂")
        print("   - 對話時自動降低音樂音量")
        print("   - 戰鬥音樂循環播放，營造緊張感")
        print("   - 勝利/失敗音樂單次播放，突出結果")
        print("   - 音樂漸入漸出效果，避免突兀切換")
        print("   - 支援熱重載，可在遊戲中更換音樂檔案")
        print("")
        print("🎨 視覺改進:")
        print("   - 支援自定義地板圖片")
        print("   - 圖片載入失敗時自動回退到程式繪製")
        print("   - 熱重載功能，可在遊戲中更新圖片")
        print("   - 完整的除錯資訊顯示")
        print("   - 戰鬥區域完美隱藏技術")
        print("   🆕 角色選擇系統與多皮膚支援")
        print("   🎵 音效狀態即時顯示 (除錯模式)")
        print("")
        print("🚀 準備啟動遊戲...")
        print("=" * 80)
        
        game = Game()
        game.run()
        
    except KeyboardInterrupt:
        print("\n👋 遊戲被用戶中斷")
    except Exception as e:
        print(f"💥 遊戲發生錯誤: {e}")
        import traceback
        traceback.print_exc()
        print("\n🔧 除錯建議:")
        print("1. 檢查是否安裝了 pygame")
        print("2. 確認所有遊戲檔案都存在")
        print("3. 嘗試執行 setup_stairs.py 創建樓梯圖片")
        print("4. 檢查 assets 資料夾結構")
        print("5. 確認地板圖片檔名是否為 'floor.png'")
        print("6. 檢查圖片檔案格式是否正確 (建議使用PNG)")
        print("7. 使用F12切換戰鬥區域顯示來除錯戰鬥系統")
        print("8. 🆕 檢查角色圖片是否放在正確路徑")
        print("9. 🆕 確認角色圖片命名符合規範")
        print("10. 🎵 檢查音樂檔案是否放在 assets/sounds/ 資料夾")
        print("11. 🎵 確認音樂格式支援 (建議MP3)")
        print("12. 🔊 確認音效格式支援 (建議WAV)")
        print("13. 🎵 如果沒有音樂檔案，遊戲仍可正常運行")
    finally:
        try:
            # 🎵 確保音效系統正確關閉
            if 'sound_manager' in globals():
                sound_manager.cleanup()
            pygame.quit()
        except:
            pass


if __name__ == "__main__":
    main()