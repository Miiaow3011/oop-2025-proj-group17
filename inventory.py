inventory = []

def add_item(item):
    inventory.append(item)
    print(f"你獲得了道具：{item['name']}")

def show_inventory():
    if not inventory:
        print("背包是空的。")
        return
    print("\n👜 背包道具：")
    for i, item in enumerate(inventory):    
        print(f"{i+1}. {item['name']}（{item['type']}）")

def use_item(player, item_name):
    for item in inventory:
        if item["name"] == item_name:
            if item["type"] == "heal":
                heal_amount = item["amount"]
                player["hp"] += heal_amount
                inventory.remove(item)
                if player["hp"] > 100:
                    player["hp"] = 100
                print(f"使用前玩家HP：{player['hp'] - heal_amount}")
                print(f"你使用了 {item_name}，恢復了 {heal_amount} HP！")
                print("使用後玩家HP：", player["hp"])
                return True
        print(f"⚠️ 沒有可以使用的「{item_name}」。")
        return False
if __name__ == "__main__":
    player = {"hp": 50}
    potion = {"name": "治療藥水", "type": "heal", "amount": 30}
    bomb = {"name": "炸彈", "type": "attack", "amount": 50} 
    add_item(potion)
    add_item(bomb)  
    show_inventory()
    use_item(player, "治療藥水")
    


