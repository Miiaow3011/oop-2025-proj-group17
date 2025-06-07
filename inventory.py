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

def use_item(player, item_name, enemy=None):
    for item in inventory:
        if item["name"] == item_name:
            if item["type"] == "heal":
                heal_amount = item["amount"]
                before = player["hp"]
                player["hp"] += heal_amount
                if player["hp"] > 100:
                    player["hp"] = 100
                inventory.remove(item)
                print(f"使用前玩家ＨＰ：{before}")
                print(f"你使用了「{item_name}」，恢復了 {heal_amount} 點ＨＰ！")
                print(f"使用後玩家ＨＰ：{player['hp']}")
                return True

            elif item["type"] == "attack":
                if enemy:
                    damage = item["amount"]
                    enemy.hp -= damage
                    inventory.remove(item)
                    print(f"你使用了「{item_name}」，對 {enemy.name} 造成了 {damage} 傷害！")
                    return True
                else:
                    print("這個攻擊道具無法在目前情況使用。")
                    return False

            else:
                print("這個道具的類型不支援。")
                return False

    # for 迴圈都沒有找到對應 item_name
    print(f"⚠️ 沒有可以使用的「{item_name}」。")
    return False

if __name__ == "__main__":
    player = {"hp": 50}
    potion = {"name": "治療藥水", "type": "heal", "amount": 30}
    bomb = {"name": "炸彈", "type": "attack", "amount": 25} 
    add_item(potion)
    add_item(bomb)  
    show_inventory()
    use_item(player, "治療藥水")

    


