import random

class Enemy:
    def __init__(self, name, hp, attack, defense=0, ai_type="basic"):
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.ai_type = ai_type
        self.status_effects = {}  # 狀態效果：毒、麻痺等
        self.temp_defense = 0  # 臨時防禦加成
    
    def take_damage(self, damage):
        """受到傷害"""
        actual_damage = max(1, damage - (self.defense + self.temp_defense))
        self.hp = max(0, self.hp - actual_damage)
        return actual_damage
    
    def is_alive(self):
        """檢查是否存活"""
        return self.hp > 0
    
    def get_ai_action(self, player):
        """AI決定行動"""
        if self.ai_type == "basic":
            return random.choice(["attack", "defend"])
        elif self.ai_type == "aggressive":
            return "attack" if random.random() > 0.2 else "defend"
        elif self.ai_type == "defensive":
            return "defend" if self.hp < self.max_hp * 0.3 else "attack"
        elif self.ai_type == "smart":
            # 智能AI：根據血量和玩家狀態決定
            if self.hp < self.max_hp * 0.2:
                return "defend"
            elif player["hp"] < player.get("max_hp", 100) * 0.3:
                return "attack"  # 玩家血量低時積極攻擊
            else:
                return random.choice(["attack", "defend"])
        else:
            return "attack"
    
    def reset_temp_effects(self):
        """重置臨時效果"""
        self.temp_defense = 0

class CombatSystem:
    def __init__(self):
        self.in_combat = False
        self.current_enemy = None
        self.player = None
        self.combat_log = []
        self.turn_count = 0
        self.combat_choices = ["攻擊", "防禦", "使用道具", "逃跑"]
        self.enemy_templates = self.load_enemy_templates()
        self.player_temp_defense = 0
        self.defend_next_turn = False  # 防禦狀態標記
    
    def load_enemy_templates(self):
        """載入敵人模板"""
        return {
            "zombie": {
                "name": "殭屍",
                "hp": 30,
                "attack": 8,
                "defense": 2,
                "ai_type": "aggressive"
            },
            "zombie_group": {
                "name": "殭屍群",
                "hp": 50,
                "attack": 12,
                "defense": 1,
                "ai_type": "aggressive"
            },
            "infected_customer": {
                "name": "感染的顧客",
                "hp": 25,
                "attack": 6,
                "defense": 1,
                "ai_type": "basic"
            },
            "mutant_rat": {
                "name": "變異老鼠",
                "hp": 15,
                "attack": 5,
                "defense": 0,
                "ai_type": "aggressive"
            },
            "alien_scout": {
                "name": "外星偵察兵",
                "hp": 40,
                "attack": 15,
                "defense": 5,
                "ai_type": "smart"
            },
            "boss_infected": {
                "name": "感染者首領",
                "hp": 80,
                "attack": 20,
                "defense": 8,
                "ai_type": "smart"
            },
            "survivor": {
                "name": "瘋狂倖存者",
                "hp": 35,
                "attack": 12,
                "defense": 3,
                "ai_type": "defensive"
            },
            "goblin": {
                "name": "哥布林",
                "hp": 30,
                "attack": 5,
                "defense": 1,
                "ai_type": "basic"
            }
        }
    
    def start_combat(self, enemy_type):
        """開始戰鬥"""
        if enemy_type in self.enemy_templates:
            template = self.enemy_templates[enemy_type]
            self.current_enemy = Enemy(
                template["name"],
                template["hp"],
                template["attack"],
                template["defense"],
                template["ai_type"]
            )
            self.in_combat = True
            self.turn_count = 0
            self.player_temp_defense = 0
            self.defend_next_turn = False
            self.combat_log = [f"⚔️ 你遭遇了 {self.current_enemy.name}！"]
            return True
        return False
    
    def battle(self, player, enemy_type_or_enemy):
        """簡化的戰鬥函數，兼容第二個版本的調用方式"""
        # 如果傳入的是Enemy對象，直接使用
        if isinstance(enemy_type_or_enemy, Enemy):
            self.current_enemy = enemy_type_or_enemy
            self.in_combat = True
            self.turn_count = 0
            self.player_temp_defense = 0
            self.defend_next_turn = False
            self.combat_log = [f"⚔️ 你遭遇了 {self.current_enemy.name}！"]
        else:
            # 否則按敵人類型創建
            if not self.start_combat(enemy_type_or_enemy):
                return "錯誤"
        
        self.player = player
        
        # 戰鬥主循環
        while self.player["hp"] > 0 and self.current_enemy.is_alive():
            print(f"\n你的 HP: {self.player['hp']} | {self.current_enemy.name} HP: {self.current_enemy.hp}\n")
            print("選擇行動：")
            for i, choice in enumerate(self.combat_choices):
                print(f"{i+1}. {choice}")
            
            try:
                action = input("輸入選項(1/2/3/4)：").strip()
                action_index = int(action) - 1
                
                if action_index < 0 or action_index >= len(self.combat_choices):
                    print("輸入錯誤，請重新選擇。")
                    continue
                
                result = self.process_action(action_index, self.player)
                
                # 顯示戰鬥日誌
                for log in self.combat_log[-3:]:  # 顯示最近3條訊息
                    print(log)
                
                if result == "victory":
                    return "勝利"
                elif result == "defeat":
                    return "失敗"
                elif result == "flee_success":
                    return "逃跑"
                elif result == "invalid":
                    print("無效的行動，請重新選擇。")
                    continue
                
                self.combat_log = []  # 清空日誌避免重複顯示
                
            except (ValueError, IndexError):
                print("輸入錯誤，請重新選擇。")
                continue
        
        # 戰鬥結束判定
        if self.player["hp"] <= 0:
            return "失敗"
        else:
            return "勝利"
    
    def process_action(self, action_index, player):
        """處理戰鬥行動"""
        if not self.in_combat or not self.current_enemy or not self.current_enemy.is_alive():
            return "invalid"
        
        self.player = player
        
        # 處理玩家行動
        if action_index == 0:  # 攻擊
            result = self.player_attack()
        elif action_index == 1:  # 防禦
            result = self.player_defend()
        elif action_index == 2:  # 使用道具
            result = self.player_use_item()
        elif action_index == 3:  # 逃跑
            result = self.player_flee()
        else:
            result = "invalid"
        
        # 檢查敵人是否死亡
        if not self.current_enemy.is_alive():
            exp_reward = self.calculate_exp_reward()
            # 檢查玩家是否有經驗值系統
            if hasattr(self.player, 'gain_exp'):
                self.player.gain_exp(exp_reward)
                self.combat_log.append(f"獲得 {exp_reward} 經驗值！")
            self.combat_log.append(f"你打倒了 {self.current_enemy.name}！")
            self.end_combat()
            return "victory"
        
        # 敵人回合（如果玩家沒有逃跑）
        if self.in_combat and result != "flee_success":
            self.enemy_turn()
            
            # 檢查玩家是否死亡
            if self.player["hp"] <= 0:
                self.combat_log.append("你被擊敗了...")
                self.end_combat()
                return "defeat"
        
        self.turn_count += 1
        return result if result in ["flee_success", "flee_failed"] else "continue"
    
    def calculate_exp_reward(self):
        """計算經驗值獎勵"""
        base_exp = self.current_enemy.max_hp // 5
        level_bonus = max(1, self.current_enemy.max_hp // 20)
        return base_exp + level_bonus
    
    def player_attack(self):
        """玩家攻擊"""
        # 計算傷害（加入隨機性）
        base_damage = random.randint(5, 15)  # 兼容第二個版本的傷害範圍
        
        # 如果玩家有攻擊力屬性，使用它
        if "attack" in self.player:
            base_damage = self.player["attack"] + random.randint(-2, 3)
        
        # 暴擊機率
        crit_chance = 0.1
        if random.random() < crit_chance:
            base_damage = int(base_damage * 1.5)
            self.combat_log.append("暴擊！")
        
        actual_damage = self.current_enemy.take_damage(base_damage)
        self.combat_log.append(f"你對 {self.current_enemy.name} 造成了 {actual_damage} 點傷害！")
        
        return "attack_success"
    
    def player_defend(self):
        """玩家防禦"""
        # 標記下次受到傷害減半
        self.defend_next_turn = True
        self.player_temp_defense = 5
        heal_amount = random.randint(2, 5)
        
        # 簡單的治療
        if "max_hp" in self.player:
            self.player["hp"] = min(self.player["max_hp"], self.player["hp"] + heal_amount)
        else:
            self.player["hp"] += heal_amount
        
        self.combat_log.append("你準備防禦，這回合受到的傷害減半。")
        if heal_amount > 0:
            self.combat_log.append(f"恢復了 {heal_amount} 點生命值")
        return "defend_success"
    
    def player_use_item(self):
        """玩家使用道具"""
        # 嘗試導入inventory模組
        try:
            from inventory import inventory, use_item
            
            if not inventory:
                self.combat_log.append("你的背包是空的，沒有道具可以使用。")
                return "item_failed"
            
            print("\n背包道具：")
            for i, item in enumerate(inventory):
                print(f"{i+1}. {item['name']}（{item['type']}）")
            
            choice = input("輸入要使用的道具編號：").strip()
            
            if not choice.isdigit() or int(choice) < 1 or int(choice) > len(inventory):
                self.combat_log.append("輸入錯誤，請重新選擇道具。")
                return "item_failed"
            
            item_name = inventory[int(choice) - 1]["name"]
            used = use_item(self.player, item_name, self.current_enemy)
            
            if used:
                self.combat_log.append(f"使用了 {item_name}")
                return "item_used"
            else:
                self.combat_log.append("道具使用失敗。")
                return "item_failed"
                
        except ImportError:
            # 如果沒有inventory模組，使用備用方案
            if self.player["hp"] < self.player.get("max_hp", 100):
                heal_amount = random.randint(10, 20)
                max_hp = self.player.get("max_hp", 100)
                self.player["hp"] = min(max_hp, self.player["hp"] + heal_amount)
                self.combat_log.append(f"你使用了應急醫療用品，恢復了 {heal_amount} 點生命值")
                return "item_used"
            else:
                self.combat_log.append("你目前不需要治療")
                return "item_failed"
    
    def player_flee(self):
        """玩家逃跑"""
        # 逃跑成功率根據敵人類型調整
        base_flee_chance = 0.7
        
        if self.current_enemy.ai_type == "aggressive":
            flee_chance = base_flee_chance - 0.2
        elif self.current_enemy.ai_type == "defensive":
            flee_chance = base_flee_chance + 0.1
        else:
            flee_chance = base_flee_chance
        
        if random.random() < flee_chance:
            self.combat_log.append("你成功逃跑了！")
            self.end_combat()
            return "flee_success"
        else:
            self.combat_log.append("逃跑失敗！")
            return "flee_failed"
    
    def enemy_turn(self):
        """敵人回合"""
        action = self.current_enemy.get_ai_action(self.player)
        
        if action == "attack":
            self.enemy_attack()
        elif action == "defend":
            self.enemy_defend()
        
        # 重置臨時效果
        self.player_temp_defense = 0
        self.current_enemy.reset_temp_effects()
        self.defend_next_turn = False
    
    def enemy_attack(self):
        """敵人攻擊"""
        enemy_damage = self.current_enemy.attack
        damage_variance = random.randint(-1, 2)
        total_damage = max(1, enemy_damage + damage_variance)
        
        # 如果玩家上回合防禦，傷害減半
        if self.defend_next_turn:
            total_damage = total_damage // 2
            self.combat_log.append("防禦生效！傷害減半")
        
        # 計算玩家實際受到的傷害
        player_defense = self.player.get("defense", 0) + self.player_temp_defense
        actual_damage = max(1, total_damage - player_defense)
        
        self.player["hp"] = max(0, self.player["hp"] - actual_damage)
        self.combat_log.append(f"{self.current_enemy.name} 攻擊你，造成了 {actual_damage} 傷害！")
    
    def enemy_defend(self):
        """敵人防禦"""
        self.current_enemy.temp_defense = 3
        heal_amount = random.randint(1, 3)
        self.current_enemy.hp = min(self.current_enemy.max_hp, self.current_enemy.hp + heal_amount)
        self.combat_log.append(f"{self.current_enemy.name} 進入防禦姿態")
    
    def end_combat(self):
        """結束戰鬥"""
        self.in_combat = False
        self.current_enemy = None
        self.player = None
        self.turn_count = 0
        self.player_temp_defense = 0
        self.defend_next_turn = False
    
    def get_combat_data(self):
        """獲取戰鬥數據用於UI顯示"""
        if not self.in_combat:
            return None
        
        return {
            "enemy": {
                "name": self.current_enemy.name,
                "hp": self.current_enemy.hp,
                "max_hp": self.current_enemy.max_hp
            },
            "player": {
                "hp": self.player["hp"] if self.player else 0,
                "max_hp": self.player.get("max_hp", 100) if self.player else 0
            },
            "choices": self.combat_choices,
            "log": self.combat_log[-4:],  # 顯示最近4條訊息
            "message": self.combat_log[-1] if self.combat_log else "",
            "turn": self.turn_count
        }
    
    def add_enemy_template(self, enemy_type, template):
        """新增敵人模板"""
        self.enemy_templates[enemy_type] = template
    
    def get_random_enemy(self, area_name="normal"):
        """根據區域獲取隨機敵人"""
        area_enemies = {
            "normal": ["zombie", "infected_customer", "goblin"],
            "storage": ["mutant_rat", "zombie"],
            "outside": ["zombie_group", "alien_scout", "survivor"],
            "boss": ["boss_infected"],
            "freezer": ["mutant_rat"],
            "counter": ["infected_customer"]
        }
        
        possible_enemies = area_enemies.get(area_name, ["zombie"])
        return random.choice(possible_enemies)
    
    def get_enemy_info(self, enemy_type):
        """獲取敵人資訊"""
        if enemy_type in self.enemy_templates:
            return self.enemy_templates[enemy_type].copy()
        return None

# 為了向後兼容，提供簡化的戰鬥函數
def battle(player, enemy):
    """簡化的戦鬥函數，兼容第二個版本"""
    combat_system = CombatSystem()
    return combat_system.battle(player, enemy)

# 測試代碼
if __name__ == "__main__":
    # 測試新系統
    combat_system = CombatSystem()
    player = {"hp": 100, "max_hp": 100, "attack": 10, "defense": 2}
    
    # 方法1：使用Enemy對象（兼容第二個版本）
    enemy = Enemy("哥布林", 30, 5)
    result1 = combat_system.battle(player, enemy)
    print(f"戰鬥結果：{result1}")
    
    # 方法2：使用敵人類型
    player["hp"] = 100  # 重置血量
    result2 = combat_system.battle(player, "goblin")
    print(f"戰鬥結果：{result2}")
    
    # 方法3：使用舊版本的battle函數
    player["hp"] = 100  # 重置血量
    enemy2 = Enemy("殭屍", 30, 8)
    result3 = battle(player, enemy2)
    print(f"戰鬥結果：{result3}")