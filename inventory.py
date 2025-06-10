class Inventory:
    def __init__(self):
        self.items = []
        self.max_slots = 20
        
        # 物品類型定義
        self.item_types = {
            "healing": {
                "description": "回復道具",
                "usable": True
            },
            "weapon": {
                "description": "武器",
                "usable": False
            },
            "tool": {
                "description": "工具",
                "usable": False
            },
            "key": {
                "description": "鑰匙道具",
                "usable": True
            },
            "clue": {
                "description": "線索道具",
                "usable": True
            },
            "special": {
                "description": "特殊道具",
                "usable": True
            }
        }
    
    def add_item(self, item):
        """添加物品到背包"""
        # 檢查是否已有相同物品（可堆疊的情況）
        existing_item = self.find_item(item["name"])
        
        if existing_item and self.is_stackable(item):
            existing_item["quantity"] = existing_item.get("quantity", 1) + item.get("quantity", 1)
            return True
        
        # 檢查背包空間
        if len(self.items) >= self.max_slots:
            return False  # 背包已滿
        
        # 添加新物品
        item_copy = item.copy()
        if "quantity" not in item_copy:
            item_copy["quantity"] = 1
        
        self.items.append(item_copy)
        return True
    
    def remove_item(self, item_name, quantity=1):
        """從背包移除物品"""
        item = self.find_item(item_name)
        if not item:
            return False
        
        if item.get("quantity", 1) <= quantity:
            self.items.remove(item)
        else:
            item["quantity"] -= quantity
        
        return True
    
    def find_item(self, item_name):
        """尋找物品"""
        for item in self.items:
            if item["name"] == item_name:
                return item
        return None
    
    def has_item(self, item_name, quantity=1):
        """檢查是否擁有物品"""
        item = self.find_item(item_name)
        if not item:
            return False
        return item.get("quantity", 1) >= quantity
    
    def is_stackable(self, item):
        """檢查物品是否可堆疊"""
        stackable_types = ["healing", "tool"]
        return item.get("type") in stackable_types
    
    def use_item(self, item_name, game_state):
        """使用物品"""
        item = self.find_item(item_name)
        if not item:
            return False, "沒有這個物品"
        
        item_type = item.get("type", "")
        
        if not self.item_types.get(item_type, {}).get("usable", False):
            return False, "這個物品無法使用"
        
        # 根據物品類型執行不同效果
        if item_type == "healing":
            return self.use_healing_item(item, game_state)
        elif item_type == "key":
            return self.use_key_item(item, game_state)
        elif item_type == "clue":
            return self.use_clue_item(item, game_state)
        elif item_type == "special":
            return self.use_special_item(item, game_state)
        
        return False, "未知的物品類型"
    
    def use_healing_item(self, item, game_state):
        """使用回復道具"""
        heal_amount = item.get("value", 0)
        
        if game_state.player_stats["hp"] >= game_state.player_stats["max_hp"]:
            return False, "血量已滿"
        
        game_state.heal_player(heal_amount)
        self.remove_item(item["name"], 1)
        
        return True, f"回復了 {heal_amount} 點血量"
    
    def use_key_item(self, item, game_state):
        """使用鑰匙道具"""
        if item["name"] == "鑰匙卡":
            game_state.set_flag("has_keycard", True)
            self.remove_item(item["name"], 1)
            return True, "獲得了進入實驗室的權限"
        
        return False, "這把鑰匙現在還用不上"
    
    def use_clue_item(self, item, game_state):
        """使用線索道具"""
        if item["name"] == "研究筆記":
            game_state.set_flag("found_clue1", True)
            return True, "閱讀了研究筆記，得到了重要線索"
        
        return True, f"仔細查看了 {item['name']}"
    
    def use_special_item(self, item, game_state):
        """使用特殊道具"""
        if item["name"] == "解藥":
            game_state.set_flag("found_antidote", True)
            game_state.set_flag("game_completed", True)
            return True, "你找到了解藥！人類有救了！"
        
        return False, "這個物品很特殊，現在還不知道怎麼使用"
    
    def get_items(self):
        """獲取所有物品"""
        return self.items.copy()
    
    def get_items_by_type(self, item_type):
        """根據類型獲取物品"""
        return [item for item in self.items if item.get("type") == item_type]
    
    def get_item_count(self):
        """獲取物品總數"""
        return sum(item.get("quantity", 1) for item in self.items)
    
    def is_full(self):
        """檢查背包是否已滿"""
        return len(self.items) >= self.max_slots
    
    def get_item_description(self, item_name):
        """獲取物品描述"""
        item = self.find_item(item_name)
        if not item:
            return "未知物品"
        
        base_desc = item.get("description", "")
        item_type = item.get("type", "")
        type_desc = self.item_types.get(item_type, {}).get("description", "")
        
        if base_desc:
            return base_desc
        elif type_desc:
            return type_desc
        else:
            return "一個神秘的物品"
    
    def sort_items(self):
        """整理背包 - 按類型和名稱排序"""
        type_order = ["weapon", "healing", "tool", "key", "clue", "special"]
        
        def sort_key(item):
            item_type = item.get("type", "")
            type_index = type_order.index(item_type) if item_type in type_order else 999
            return (type_index, item["name"])
        
        self.items.sort(key=sort_key)
    
    def clear(self):
        """清空背包"""
        self.items.clear()
    
    def save_to_dict(self):
        """保存背包數據到字典"""
        return {
            "items": self.items,
            "max_slots": self.max_slots
        }
    
    def load_from_dict(self, data):
        """從字典載入背包數據"""
        self.items = data.get("items", [])
        self.max_slots = data.get("max_slots", 20)
    
    def get_healing_items(self):
        """獲取所有回復道具"""
        return self.get_items_by_type("healing")
    
    def get_key_items(self):
        """獲取所有鑰匙道具"""
        return self.get_items_by_type("key")
    
    def get_weapons(self):
        """獲取所有武器"""
        return self.get_items_by_type("weapon")
    
    def auto_use_healing(self, game_state, threshold=0.3):
        """自動使用回復道具（當血量低於閾值時）"""
        current_hp_ratio = game_state.player_stats["hp"] / game_state.player_stats["max_hp"]
        
        if current_hp_ratio > threshold:
            return False, "血量充足，無需回復"
        
        # 找到最小的回復道具
        healing_items = self.get_healing_items()
        if not healing_items:
            return False, "沒有回復道具"
        
        # 按回復量排序，使用最小的
        healing_items.sort(key=lambda x: x.get("value", 0))
        best_item = healing_items[0]
        
        return self.use_item(best_item["name"], game_state)