# 末世第二餐廳 - main.py (完整修復版 + 地板圖片支援)
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
        
        # 🪜 樓梯圖片偵錯資訊
        if self.debug_mode:
            self.map_manager.debug_print_stairs()
            self.map_manager.debug_print_floor_info()  # 🆕 新增地板偵錯

    def handle_events(self):
        """修復版事件處理 - 整合所有功能"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                # ======= 全域快捷鍵 - 任何狀態下都優先處理 =======
                if event.key == pygame.K_ESCAPE:
                    # ESC鍵: 強制關閉UI或退出戰鬥
                    if self.game_state.current_state == "combat":
                        print("🆘 ESC強制退出戰鬥")
                        self.force_end_combat()
                    else:
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
                elif event.key == pygame.K_F4:
                    # 🪜 F4: 重新載入樓梯圖片
                    self.reload_stairs_images()
                    continue
                elif event.key == pygame.K_F5:
                    # F5: 樓梯偵錯資訊
                    self.map_manager.debug_print_stairs()
                    continue
                elif event.key == pygame.K_F6:
                    # 🆕 F6: 物品偵錯資訊
                    self.map_manager.debug_print_items()
                    continue
                elif event.key == pygame.K_F7:
                    # 🆕 F7: 重置物品收集狀態
                    self.map_manager.reset_items()
                    self.ui.show_message("已重置所有物品收集狀態")
                    continue
                elif event.key == pygame.K_F8:
                    # 🆕 F8: 重新載入地板圖片
                    self.reload_floor_images()
                    continue
                elif event.key == pygame.K_F9:
                    # 🆕 F9: 地板偵錯資訊
                    self.map_manager.debug_print_floor_info()
                    continue
                elif event.key == pygame.K_F10:
                    # 🆕 F10: 重新載入商店圖片
                    self.reload_shop_images()
                    continue
                elif event.key == pygame.K_F11:
                    # 🆕 F11: 商店圖片偵錯資訊
                    self.map_manager.debug_print_shop_info()
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

    def reload_stairs_images(self):
        """重新載入樓梯圖片"""
        print("🔄 手動重新載入樓梯圖片...")
        self.map_manager.reload_stairs_images()
        if self.debug_mode:
            self.map_manager.debug_print_stairs()

    def reload_floor_images(self):
        """🆕 重新載入地板圖片"""
        print("🔄 手動重新載入地板圖片...")
        self.map_manager.reload_floor_images()
        if self.debug_mode:
            self.map_manager.debug_print_floor_info()
        self.ui.show_message("地板圖片已重新載入！")

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
        """切換除錯模式 - 增強版"""
        self.debug_mode = not self.debug_mode
        print(f"🔧 除錯模式: {'開啟' if self.debug_mode else '關閉'}")
        if self.debug_mode:
            self.print_debug_info()
            self.map_manager.debug_print_stairs()
            self.map_manager.debug_print_items()  # 新增物品除錯資訊
            self.map_manager.debug_print_floor_info()  # 🆕 新增地板除錯資訊

    def print_debug_info(self):
        """顯示除錯資訊"""
        print(f"🔍 當前狀態:")
        print(f"   遊戲狀態: {self.game_state.current_state}")
        print(f"   UI狀態: {self.ui.get_ui_status()}")
        print(f"   玩家位置: ({self.player.x}, {self.player.y})")
        print(f"   玩家移動: {self.player.is_moving}")
        print(f"   當前樓層: {self.map_manager.current_floor}")

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
        """處理戰鬥輸入 - 最終版"""
        key_name = pygame.key.name(event.key)
        print(f"⚔️ 戰鬥按鍵: {key_name}")
        
        # 如果戰鬥已經有結果，立即結束
        if self.combat_system.combat_result:
            print(f"⚠️ 戰鬥已有結果: {self.combat_system.combat_result}")
            self.handle_combat_end()
            return
        
        # 檢查是否是正確的數字鍵
        if event.key == pygame.K_1:
            print("🗡️ 選擇攻擊")
            self.combat_system.player_action("attack")
        elif event.key == pygame.K_2:
            print("🛡️ 選擇防禦")
            self.combat_system.player_action("defend")
        elif event.key == pygame.K_3:
            print("🏃 選擇逃跑")
            self.combat_system.player_action("escape")
        else:
            return
        
        # 行動後立即檢查結果
        if self.combat_system.combat_result:
            print(f"🎯 行動後立即檢測到結果: {self.combat_system.combat_result}")
            self.handle_combat_end()

    def handle_combat_end(self):
        """處理戰鬥結束 - 統一處理方法"""
        if not self.combat_system.combat_result:
            return
        
        result = self.combat_system.combat_result
        print(f"🏁 處理戰鬥結束: {result}")
        
        try:
            if result == "win":
                print("✅ 處理戰鬥勝利")
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
            self.ui.show_message("戰鬥勝利！")
        elif result == "escape":
            self.ui.show_message("逃跑成功！")
        elif result == "lose":
            self.ui.show_message("戰鬥失敗！")
        else:
            self.ui.show_message("強制退出戰鬥！")
        
        # 立即重置所有戰鬥狀態
        self.combat_system.in_combat = False
        self.combat_system.combat_result = None
        self.combat_system.current_enemy = None
        self.combat_system.player_turn = True
        self.combat_system.animation_timer = 0
        
        # 強制設定為探索狀態
        self.game_state.current_state = "exploration"
        
        # 清除戰鬥區域
        if hasattr(self, 'current_combat_zone'):
            self.current_combat_zone = None
        
        print("✅ 強制結束完成，回到探索狀態")

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
            
            if interaction["type"] == "shop":
                self.start_shop_interaction(interaction)
            elif interaction["type"] == "npc":
                self.start_npc_dialogue(interaction)
            elif interaction["type"] == "stairs":
                self.use_stairs(interaction)
        else:
            if self.debug_mode:
                print("❌ 附近沒有可互動的物件")

    def collect_item_new(self, item_pickup):
        """🆕 新的物品收集方法"""
        item = item_pickup["item"]
        item_id = item_pickup["item_id"]
        
        if self.debug_mode:
            print(f"📦 收集物品: {item['name']} (ID: {item_id})")
        
        # 嘗試添加到背包
        success = self.inventory.add_item(item)
        
        if success:
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
                self.ui.show_message(f"🎉 獲得了 {item['name']}！這可能是關鍵物品！")
                if item["name"] == "解藥":
                    self.ui.has_antidote = True
                    self.ui.show_message("🎊 恭喜！你找到了拯救世界的解藥！")
            elif item["type"] == "clue":
                self.ui.show_message(f"獲得了 {item['name']}！這提供了重要線索")
            else:
                self.ui.show_message(f"獲得了 {item['name']}！")
            
            # 給予經驗值獎勵
            exp_reward = self.get_item_exp_reward(item)
            if exp_reward > 0:
                self.game_state.add_exp(exp_reward)
                if self.debug_mode:
                    print(f"🎯 收集物品獲得 {exp_reward} 經驗值")
            
            if self.debug_mode:
                print(f"✅ 成功收集: {item['name']}")
                print(f"   背包物品數: {len(self.inventory.get_items())}")
                print(f"   玩家經驗: {self.game_state.player_stats['exp']}")
                
        else:
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
                self.ui.show_message(f"獲得了 {item_info['item']['name']}")
                self.map_manager.remove_item(item_info["item"])
                if self.debug_mode:
                    print(f"✅ 成功收集: {item_info['item']['name']}")
            else:
                self.ui.show_message("背包已滿！")
                if self.debug_mode:
                    print(f"❌ 背包已滿，無法收集: {item_info['item']['name']}")

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
        """使用樓梯 - 增強版"""
        if self.debug_mode:
            print(f"🪜 使用樓梯: {stairs_info}")
        
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
                    self.map_manager.change_floor(3)
                    self.player.set_position(450, 600)
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
                if self.debug_mode:
                    print("🚫 已經在最低樓層或無效目標")
                self.ui.show_message("已經是最低樓層了")

    def start_combat_in_zone(self, combat_zone):
        """在戰鬥區域開始戰鬥"""
        print(f"🔄 準備切換到戰鬥狀態")
        print(f"   當前遊戲狀態: {self.game_state.current_state}")
        
        self.game_state.current_state = "combat"
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

    def update(self):
        if not self.show_intro:
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

    def render_debug_info(self):
        """渲染除錯資訊"""
        debug_rect = pygame.Rect(10, 300, 300, 180)  # 🆕 增加高度以容納地板資訊
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
            f"地板圖片: {self.map_manager.use_floor_sprites}",  # 🆕 新增地板狀態
            f"商店圖片: {self.map_manager.use_shop_sprites}",  # 🆕 新增商店圖片狀態
            f"已收集物品: {len(self.map_manager.collected_items)}"
        ]
        
        y_offset = 305
        for line in debug_lines:
            if "True" in line and ("移動" in line or "開啟" in line):
                color = (255, 100, 100)
            elif "樓梯圖片: True" in line or "地板圖片: True" in line:  # 🆕 地板圖片狀態顏色
                color = (0, 255, 0)
            elif "樓梯圖片: False" in line or "地板圖片: False" in line:  # 🆕 地板圖片狀態顏色
                color = (255, 255, 0)
            elif "商店圖片: True" in line:  # 🆕 商店圖片狀態顏色
                color = (0, 255, 0)
            elif "商店圖片: False" in line:  # 🆕 商店圖片狀態顏色
                color = (255, 255, 0)
            elif "已收集物品:" in line:
                color = (255, 200, 100)
                color = (255, 200, 100)
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
            "方向鍵 移動，空白鍵 互動，I 背包，M 地圖",
            "",
            "🔧 除錯快捷鍵:",
            "F8 地板圖片，F9 地板除錯，F10 商店圖片，F11 商店除錯"  # 🆕 完整的快捷鍵說明
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
                elif line.startswith("📋") or line.startswith("🔧"):  # 🆕 除錯快捷鍵也用綠色
                    text_surface = font_manager.render_text(line, 24, (100, 255, 100))
                    line_spacing = 35
                elif line.startswith("方向鍵") or line.startswith("F8"):  # 🆕 新快捷鍵說明
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
                "attack": 10,
                "defense": 5,
                "level": 1,
                "exp": 0
            }
        
        # 重置其他組件
        self.map_manager.current_floor = 1
        self.map_manager.reset_items()  # 🆕 重置物品收集狀態
        self.inventory = Inventory()  # 重新創建背包
        
        # 重置UI狀態
        self.ui.show_inventory = False
        self.ui.show_map = False
        self.ui.dialogue_active = False
        self.ui.has_keycard = False  # 🆕 重置特殊物品標記
        self.ui.has_antidote = False
        self.ui.game_completed = False
        self.ui.game_over = False
        
        # 重新設定玩家參考（重要！）
        self.ui.set_player_reference(self.player)
        self.ui.set_game_state_reference(self.game_state)
        self.ui.set_inventory_reference(self.inventory)
        
        print("✅ 遊戲重置完成！")


def main():
    """程式入口點"""
    try:
        print("🎮 啟動《末世第二餐廳》(完整修復版 + 地板圖片支援)")
        print("=" * 70)
        print("💡 遊戲功能:")
        print("   ✅ 樓梯圖片支援 (F4重新載入)")
        print("   ✅ 地板圖片支援 (F8重新載入) - 新功能！")
        print("   ✅ 物品收集系統修復 (F6除錯)")
        print("   ✅ 戰鬥系統完整")
        print("   ✅ UI互動修復")
        print("   ✅ 中文字體支援")
        print("")
        print("🎯 快捷鍵說明:")
        print("   F1 - 開啟/關閉除錯模式")
        print("   F2 - 強制重置遊戲狀態")
        print("   F3 - 重置玩家位置")
        print("   F4 - 重新載入樓梯圖片")
        print("   F5 - 顯示樓梯除錯資訊")
        print("   F6 - 顯示物品除錯資訊")
        print("   F7 - 重置物品收集狀態")
        print("   F8 - 重新載入地板圖片 (新功能！)")
        print("   F9 - 顯示地板除錯資訊 (新功能！)")
        print("   F10 - 重新載入商店圖片 (新功能！)")
        print("   F11 - 顯示商店圖片除錯資訊 (新功能！)")
        print("   ESC - 強制關閉所有UI")
        print("   I - 背包, M - 地圖, R - 重新開始(遊戲結束時)")
        print("")
        print("🪜 樓梯圖片路徑:")
        print("   assets/images/stairs_up.png - 上樓梯圖片 (96x72)")
        print("   assets/images/stairs_down.png - 下樓梯圖片 (96x72)")
        print("")
        print("🏢 地板圖片路徑:")
        print("   assets/images/floor.png - 主要地板圖片 (會縮放到64x64)")
        print("   assets/images/神饃.png - 備用地板圖片")
        print("   assets/images/tile.png - 另一個備用選項")
        print("")
        print("🏪 商店圖片路徑 (新功能！):")
        print("   assets/images/711.png - 7-11商店圖片 (會縮放到80x60)")
        print("   assets/images/subway.png - Subway商店圖片")
        print("   assets/images/coffee.png - 咖啡廳商店圖片")
        print("")
        print("📦 物品系統改進:")
        print("   - 醫療包和能量包不再重疊")
        print("   - 每種物品有獨特的視覺效果")
        print("   - 收集後立即從地圖消失")
        print("   - 支援經驗值獎勵系統")
        print("   - 完整的物品追蹤和除錯")
        print("")
        print("🎨 視覺改進:")
        print("   - 支援自定義地板圖片")
        print("   - 圖片載入失敗時自動回退到程式繪製")
        print("   - 熱重載功能，可在遊戲中更新圖片")
        print("   - 完整的除錯資訊顯示")
        print("")
        print("🚀 準備啟動遊戲...")
        print("=" * 70)
        
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
    finally:
        try:
            pygame.quit()
        except:
            pass


if __name__ == "__main__":
    main()