# inventory.py - 合併的背包系統

class Inventory:
    def __init__(self):
        # 使用字典存儲物品，每個物品包含數量和詳細信息
        self.items = {}
        self.max_capacity = 20
        
        # 預設初始物品
        self.add_item_with_details("食物", {"type": "heal", "amount": 15}, 3)
        self.add_item_with_details("醫療包", {"type": "heal", "amount": 30}, 1)
        self.add_item_with_details("手電筒", {"type": "tool", "amount": 0}, 1)

    def add_item(self, item_name, quantity=1):
        """添加簡單物品（只有名稱和數量）"""
        if self.get_total_items() + quantity <= self.max_capacity:
            if item_name in self.items:
                self.items[item_name]["quantity"] += quantity
            else:
                self.items[item_name] = {
                    "quantity": quantity,
                    "type": "misc",
                    "amount": 0
                }
            print(f"你獲得了道具：{item_name}")
            return True
        print("背包已滿，無法添加物品！")
        return False

    def add_item_with_details(self, item_name, item_details, quantity=1):
        """添加詳細物品（包含類型和效果）"""
        if self.get_total_items() + quantity <= self.max_capacity:
            if item_name in self.items:
                self.items[item_name]["quantity"] += quantity
            else:
                self.items[item_name] = {
                    "quantity": quantity,
                    "type": item_details.get("type", "misc"),
                    "amount": item_details.get("amount", 0)
                }
            print(f"你獲得了道具：{item_name}")
            return True
        print("背包已滿，無法添加物品！")
        return False

    def remove_item(self, item_name, quantity=1):
        """移除物品"""
        if item_name in self.items and self.items[item_name]["quantity"] >= quantity:
            self.items[item_name]["quantity"] -= quantity
            if self.items[item_name]["quantity"] == 0:
                del self.items[item_name]
            return True
        return False

    def has_item(self, item_name, quantity=1):
        """檢查是否有指定物品"""
        return self.items.get(item_name, {}).get("quantity", 0) >= quantity

    def show_inventory(self):
        """顯示背包內容"""
        if not self.items:
            print("背包是空的。")
            return
        
        print("\n👜 背包道具：")
        for i, (item_name, item_data) in enumerate(self.items.items()):
            item_type = item_data["type"]
            quantity = item_data["quantity"]
            if quantity > 1:
                print(f"{i+1}. {item_name}（{item_type}）x{quantity}")
            else:
                print(f"{i+1}. {item_name}（{item_type}）")

    def use_item(self, item_name, player, enemy=None):
        """使用物品"""
        if not self.has_item(item_name):
            print(f"⚠️ 沒有可以使用的「{item_name}」。")
            return False

        item_data = self.items[item_name]
        item_type = item_data["type"]
        item_amount = item_data["amount"]

        # 治療類物品
        if item_type == "heal":
            # 檢查是否需要治療
            if hasattr(player, 'max_hp') and player.hp >= player.max_hp:
                print("你的生命值已滿，不需要使用治療物品。")
                return False
            elif not hasattr(player, 'max_hp') and player.get("hp", 0) >= 100:
                print("你的生命值已滿，不需要使用治療物品。")
                return False

            # 執行治療
            if hasattr(player, 'heal'):  # 如果 player 是物件
                before_hp = player.hp
                player.heal(item_amount)
                after_hp = player.hp
            else:  # 如果 player 是字典
                before_hp = player.get("hp", 0)
                player["hp"] += item_amount
                max_hp = player.get("max_hp", 100)
                if player["hp"] > max_hp:
                    player["hp"] = max_hp
                after_hp = player["hp"]

            self.remove_item(item_name)
            print(f"使用前玩家ＨＰ：{before_hp}")
            print(f"你使用了「{item_name}」，恢復了 {item_amount} 點ＨＰ！")
            print(f"使用後玩家ＨＰ：{after_hp}")
            return True

        # 攻擊類物品
        elif item_type == "attack":
            if enemy is None:
                print("這個攻擊道具無法在目前情況使用。")
                return False
            
            # 對敵人造成傷害
            if hasattr(enemy, 'hp'):  # 如果 enemy 是物件
                enemy.hp -= item_amount
                enemy_name = getattr(enemy, 'name', '敵人')
            else:  # 如果 enemy 是字典
                enemy["hp"] -= item_amount
                enemy_name = enemy.get("name", "敵人")

            self.remove_item(item_name)
            print(f"你使用了「{item_name}」，對 {enemy_name} 造成了 {item_amount} 傷害！")
            return True

        # 武器類物品
        elif item_type == "weapon" or item_name == "武器":
            print("你裝備了武器，攻擊力提升！")
            return True

        # 工具類物品
        elif item_type == "tool":
            if item_name == "手電筒":
                print("你打開了手電筒，照亮了周圍。")
                return True
            elif item_name == "鑰匙":
                print("你使用了鑰匙。")
                return True

        # 其他未知類型
        else:
            print("這個道具的類型不支援。")
            return False

    def get_items(self):
        """獲取所有物品"""
        return {name: data["quantity"] for name, data in self.items.items()}

    def get_total_items(self):
        """獲取物品總數"""
        return sum(data["quantity"] for data in self.items.values())

    def is_full(self):
        """檢查背包是否已滿"""
        return self.get_total_items() >= self.max_capacity

    def get_item_descriptions(self):
        """獲取物品描述"""
        descriptions = {
            "食物": "可以恢復少量生命值 (15 HP)",
            "醫療包": "可以恢復大量生命值 (30 HP)",
            "治療藥水": "可以恢復中等生命值 (30 HP)",
            "手電筒": "在黑暗中提供照明",
            "武器": "提升攻擊力",
            "鑰匙": "可以開啟某些門",
            "炸彈": "攻擊道具，造成大量傷害 (25 傷害)"
        }
        return descriptions


# 測試代碼
if __name__ == "__main__":
    # 創建背包和玩家
    inventory = Inventory()
    player = {"hp": 50, "max_hp": 100}
    
    # 添加第一個版本中的物品
    potion = {"name": "治療藥水", "type": "heal", "amount": 30}
    bomb = {"name": "炸彈", "type": "attack", "amount": 25}
    
    inventory.add_item_with_details("治療藥水", {"type": "heal", "amount": 30})
    inventory.add_item_with_details("炸彈", {"type": "attack", "amount": 25})
    
    # 顯示背包
    inventory.show_inventory()
    
    # 使用道具
    print("\n=== 使用治療藥水 ===")
    inventory.use_item("治療藥水", player)
    
    print("\n=== 顯示使用後的背包 ===")
    inventory.show_inventory()
    
    print("\n=== 嘗試使用攻擊道具（沒有敵人）===")
    inventory.use_item("炸彈", player)
    
    print("\n=== 創建敵人並使用攻擊道具 ===")
    enemy = {"name": "哥布林", "hp": 50}
    inventory.use_item("炸彈", player, enemy)
    print(f"敵人剩餘血量：{enemy['hp']}")
    
    print("\n=== 最終背包狀態 ===")
    inventory.show_inventory()