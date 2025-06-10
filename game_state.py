import random
import time

class GameState:
    def __init__(self):
        self.current_state = "exploration"  # exploration, combat, dialogue, menu
        self.player_stats = {
            "hp": 100,
            "max_hp": 100,
            "attack": 10,
            "defense": 5,
            "level": 1,
            "exp": 0
        }
        
        # 遊戲進度標記
        self.flags = {
            "has_keycard": False,
            "talked_to_npc1": False,
            "talked_to_npc2": False,
            "talked_to_npc3": False,
            "found_clue1": False,
            "found_clue2": False,
            "found_clue3": False,
            "unlocked_third_floor": False,
            "found_antidote": False,
            "game_completed": False
        }
        
        # 敵人資料
        self.enemies = [
            {
                "name": "殭屍學生",
                "hp": 30,
                "attack": 8,
                "defense": 2,
                "exp_reward": 15,
                "description": "一個被感染的學生，眼神空洞地遊蕩著..."
            },
            {
                "name": "感染職員",
                "hp": 45,
                "attack": 12,
                "defense": 4,
                "exp_reward": 25,
                "description": "餐廳的工作人員，現在只剩下進食的本能..."
            },
            {
                "name": "變異殭屍",
                "hp": 60,
                "attack": 15,
                "defense": 6,
                "exp_reward": 40,
                "description": "病毒變異後的產物，比普通殭屍更加危險..."
            },
            {
                "name": "神秘外星人",
                "hp": 80,
                "attack": 20,
                "defense": 8,
                "exp_reward": 60,
                "description": "身穿銀色制服的外星生物，似乎在尋找什麼..."
            }
        ]
        
        # 隨機遭遇機率
        self.encounter_chance = 0.05  # 5%機率
        self.last_encounter_time = time.time()
        self.min_encounter_interval = 10  # 最少10秒間隔
        
        # 遊戲訊息
        self.messages = []
        self.message_timer = 0
    
    def set_state(self, new_state):
        self.current_state = new_state
    
    def set_flag(self, flag_name, value=True):
        if flag_name in self.flags:
            self.flags[flag_name] = value
    
    def get_flag(self, flag_name):
        return self.flags.get(flag_name, False)
    
    def add_exp(self, exp_amount):
        self.player_stats["exp"] += exp_amount
        
        # 檢查升級
        exp_needed = self.player_stats["level"] * 100
        if self.player_stats["exp"] >= exp_needed:
            self.level_up()
    
    def level_up(self):
        self.player_stats["level"] += 1
        self.player_stats["exp"] = 0
        
        # 提升能力值
        hp_increase = random.randint(8, 15)
        attack_increase = random.randint(2, 5)
        defense_increase = random.randint(1, 3)
        
        self.player_stats["max_hp"] += hp_increase
        self.player_stats["hp"] = self.player_stats["max_hp"]  # 升級時回滿血
        self.player_stats["attack"] += attack_increase
        self.player_stats["defense"] += defense_increase
        
        self.add_message(f"升級了！等級 {self.player_stats['level']}")
        self.add_message(f"HP +{hp_increase}, 攻擊 +{attack_increase}, 防禦 +{defense_increase}")
    
    def heal_player(self, amount):
        self.player_stats["hp"] = min(
            self.player_stats["hp"] + amount,
            self.player_stats["max_hp"]
        )
    
    def damage_player(self, amount):
        actual_damage = max(1, amount - self.player_stats["defense"])
        self.player_stats["hp"] -= actual_damage
        return actual_damage
    
    def is_player_dead(self):
        return self.player_stats["hp"] <= 0
    
    def should_trigger_encounter(self):
        """檢查是否應該觸發隨機遭遇"""
        current_time = time.time()
        
        # 檢查時間間隔和機率
        time_check = current_time - self.last_encounter_time > self.min_encounter_interval
        random_check = random.random() < self.encounter_chance
        
        if time_check and random_check:
            self.last_encounter_time = current_time
            return True
        return False
    
    def get_random_enemy(self):
        # 根據玩家等級調整敵人出現機率
        level = self.player_stats["level"]
        
        if level == 1:
            # 只會遇到殭屍學生
            return self.enemies[0].copy()
        elif level <= 3:
            # 殭屍學生和感染職員
            return random.choice(self.enemies[:2]).copy()
        elif level <= 5:
            # 前三種敵人
            return random.choice(self.enemies[:3]).copy()
        else:
            # 所有敵人
            return random.choice(self.enemies).copy()
    
    def add_message(self, message):
        self.messages.append(message)
        self.message_timer = 180  # 3秒顯示時間 (60fps * 3)
    
    def update_messages(self):
        if self.message_timer > 0:
            self.message_timer -= 1
        else:
            if self.messages:
                self.messages.pop(0)
                if self.messages:
                    self.message_timer = 180
    
    def get_current_messages(self):
        return self.messages[:3]  # 最多顯示3條訊息
    
    def save_game(self, filename="savegame.json"):
        import json
        save_data = {
            "player_stats": self.player_stats,
            "flags": self.flags,
            "current_state": self.current_state
        }
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"存檔失敗: {e}")
            return False
    
    def load_game(self, filename="savegame.json"):
        import json
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                save_data = json.load(f)
            
            self.player_stats = save_data.get("player_stats", self.player_stats)
            self.flags = save_data.get("flags", self.flags)
            self.current_state = save_data.get("current_state", "exploration")
            return True
        except Exception as e:
            print(f"讀檔失敗: {e}")
            return False
    
    def check_win_condition(self):
        # 檢查是否找到解藥並完成遊戲
        return self.flags["found_antidote"]
    
    def get_game_progress(self):
        # 計算遊戲進度百分比
        total_flags = len([f for f in self.flags.keys() if f != "game_completed"])
        completed_flags = len([f for f, v in self.flags.items() if v and f != "game_completed"])
        return (completed_flags / total_flags) * 100