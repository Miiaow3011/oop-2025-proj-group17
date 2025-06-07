import random
from inventory import inventory, use_item

class Enemy:
    def __init__(self, name, hp, atk):
        self.name = name
        self.hp = hp
        self.atk = atk

    def is_alive(self):
        return self.hp > 0

def battle(player, enemy):
    print(f"⚔️ 你遇到了 {enemy.name}！")

    while player["hp"] > 0 and enemy.is_alive():
        print(f"\n你的 HP: {player['hp']} | {enemy.name} HP: {enemy.hp}\n")
        print("選擇行動：")
        print("1. 攻擊")
        print("2. 防禦")
        print("3. 逃跑")
        print("4. 使用道具")

        action = input("輸入選項(1/2/3/4)：").strip()

        if action == "1":
            damage = random.randint(5, 15)
            enemy.hp -= damage
            print(f"你對 {enemy.name} 造成了 {damage} 傷害！")

        elif action == "2":
            print("你準備防禦，這回合受到的傷害減半。")

        elif action == "3":
            print("你成功逃跑了！")
            return "逃跑"

        elif action == "4":
            if not inventory:
                print("你的背包是空的，沒有道具可以使用。")
                continue
            print("\n背包道具：")
            for i, item in enumerate(inventory):
                print(f"{i+1}. {item['name']}（{item['type']}）")

            choice = input("輸入要使用的道具編號：").strip()
            if not choice.isdigit() or int(choice) < 1 or int(choice) > len(inventory):
                print("輸入錯誤，請重新選擇道具。")
                continue

            item_name = inventory[int(choice) -1]["name"]
            used = use_item(player, item_name, enemy)
            if not used:
                print("道具使用失敗。")
                continue

        else:
            print("輸入錯誤，請重新選擇。")
            continue

        # 敵人回合攻擊（除非玩家逃跑）
        if enemy.is_alive() and action != "3":
            enemy_damage = enemy.atk
            if action == "2":
                enemy_damage = enemy_damage // 2
            player["hp"] -= enemy_damage
            print(f"{enemy.name} 攻擊你，造成了 {enemy_damage} 傷害！")

    if player["hp"] <= 0:
        print("你被擊敗了……")
        return "失敗"
    else:
        print(f"你打倒了 {enemy.name}！")
        return "勝利"

if __name__ == "__main__":
    player = {"hp": 100}
    enemy = Enemy("哥布林", 30, 5)
    # 這裡可以先加入一些道具
    from inventory import add_item
    potion = {"name": "治療藥水", "type": "heal", "amount": 30}
    bomb = {"name": "炸彈", "type": "attack", "amount": 25}
    add_item(potion)
    add_item(bomb)

    result = battle(player, enemy)
    print("戰鬥結束！結果：",result)



