#!/usr/bin/env python3
"""
《末世第二餐廳》專案結構建立工具
自動建立完整的遊戲專案目錄結構
"""

import os
import sys
from pathlib import Path

def create_directory_structure():
    """建立完整的專案目錄結構"""
    
    # 定義目錄結構
    directories = [
        # 素材資料夾
        "assets",
        "assets/images",
        "assets/images/characters",
        "assets/images/enemies", 
        "assets/images/tiles",
        "assets/images/shops",
        "assets/images/items",
        "assets/images/ui",
        "assets/images/ui/buttons",
        "assets/images/ui/icons",
        "assets/images/backgrounds",
        "assets/sounds",
        "assets/sounds/bgm",
        "assets/sounds/sfx",
        "assets/sounds/voice",
        "assets/fonts",
        "assets/data",
        
        # 功能資料夾
        "saves",
        "logs", 
        "docs",
        "docs/screenshots",
        "tools",
        "tests",
        "build",
        "build/dist",
        "build/build"
    ]
    
    print("=== 《末世第二餐廳》專案建立工具 ===\n")
    print("正在建立專案目錄結構...\n")
    
    # 建立資料夾
    created_count = 0
    for directory in directories:
        try:
            Path(directory).mkdir(parents=True, exist_ok=True)
            print(f"✅ 建立資料夾: {directory}")
            created_count += 1
        except Exception as e:
            print(f"❌ 建立失敗: {directory} - {e}")
    
    print(f"\n📁 成功建立 {created_count} 個資料夾")
    return created_count > 0

def create_readme_files():
    """建立各資料夾的說明檔案"""
    
    readme_contents = {
        "assets/images/README.md": """# 圖片素材資料夾

## 目錄說明
- **characters/**: 角色圖片 (玩家、NPC)
- **enemies/**: 敵人圖片 (殭屍、外星人)
- **tiles/**: 地圖磚塊 (地板、牆壁、樓梯)
- **shops/**: 商店圖示
- **items/**: 道具圖片
- **ui/**: 使用者介面元素
- **backgrounds/**: 背景圖片

## 建議格式
- PNG (支援透明度)
- 32x32 像素 (角色和道具)
- 16x16 像素 (小圖示)
""",

        "assets/sounds/README.md": """# 音效素材資料夾

## 目錄說明
- **bgm/**: 背景音樂 (.ogg 格式推薦)
- **sfx/**: 音效檔案 (.wav 格式推薦)
- **voice/**: 語音檔案 (可選)

## 建議音效
- footsteps.wav: 腳步聲
- door_open.wav: 開門聲
- pickup_item.wav: 拾取物品
- attack.wav: 攻擊音效
- zombie_growl.wav: 殭屍聲音
- level_up.wav: 升級音效
""",

        "assets/fonts/README.md": """# 字體資料夾

## 推薦中文字體
1. **思源黑體** (Source Han Sans)
   - 檔案: SourceHanSans-Regular.ttf
   - 下載: Google Fonts

2. **文泉驛微米黑**
   - 檔案: wqy-microhei.ttc
   - 下載: wenq.org

3. **Noto Sans CJK**
   - 檔案: NotoSansCJK-Regular.ttc
   - 下載: Google Noto Fonts

## 使用方式
將TTF/OTF字體檔案放入此資料夾，遊戲會自動檢測使用。
""",

        "assets/data/README.md": """# 遊戲數據資料夾

## JSON 數據檔案
- **dialogues.json**: 對話內容
- **shop_data.json**: 商店資訊
- **enemy_stats.json**: 敵人數據
- **item_database.json**: 道具資料庫

## 格式範例
```json
{
  "npc1": {
    "name": "驚慌學生",
    "dialogues": ["救命！外面都是殭屍！"]
  }
}
```
""",

        "saves/README.md": """# 存檔資料夾

此資料夾用於存放玩家的遊戲存檔：
- autosave.json: 自動存檔
- quicksave.json: 快速存檔  
- manual_save_*.json: 手動存檔

⚠️ 請勿手動修改存檔檔案
""",

        "logs/README.md": """# 日誌資料夾

遊戲運行日誌：
- game.log: 一般運行日誌
- error.log: 錯誤日誌
- debug.log: 除錯日誌

用於問題診斷和效能分析。
""",

        "tools/README.md": """# 開發工具資料夾

包含遊戲開發和維護工具：
- map_editor.py: 地圖編輯器
- dialogue_editor.py: 對話編輯器
- asset_manager.py: 素材管理
- build_game.py: 遊戲打包

執行方式: python tools/工具名稱.py
""",

        "tests/README.md": """# 測試檔案資料夾

單元測試檔案：
- test_game_state.py: 遊戲狀態測試
- test_combat.py: 戰鬥系統測試
- test_inventory.py: 背包系統測試

執行測試: python -m pytest tests/
"""
    }
    
    print("正在建立說明檔案...\n")
    
    created_files = 0
    for file_path, content in readme_contents.items():
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ 建立說明: {file_path}")
            created_files += 1
        except Exception as e:
            print(f"❌ 建立失敗: {file_path} - {e}")
    
    print(f"\n📄 成功建立 {created_files} 個說明檔案")
    return created_files > 0

def create_sample_data_files():
    """建立範例數據檔案"""
    
    sample_data = {
        "assets/data/dialogues.json": {
            "npc1": {
                "name": "驚慌學生",
                "dialogues": [
                    "救命！外面到處都是殭屍！",
                    "我看到研究生們往樓上跑了！",
                    "聽說三樓有什麼重要的東西..."
                ],
                "options": [
                    "冷靜一點，告訴我更多",
                    "樓上有什麼？", 
                    "離開"
                ]
            },
            "npc2": {
                "name": "受傷職員",
                "dialogues": [
                    "我被咬了...但還沒完全感染。",
                    "聽說三樓有解藥...",
                    "你一定要找到它！"
                ]
            }
        },
        
        "assets/data/shop_data.json": {
            "A": {
                "name": "7-11",
                "chinese_name": "7-11",
                "items": [
                    {"name": "醫療包", "price": 50, "stock": 3},
                    {"name": "能量飲料", "price": 20, "stock": 5}
                ]
            },
            "B": {
                "name": "Subway",
                "chinese_name": "Subway", 
                "items": [
                    {"name": "三明治", "price": 30, "stock": 2}
                ]
            }
        },
        
        "assets/data/enemy_stats.json": {
            "zombie_student": {
                "name": "殭屍學生",
                "hp": 30,
                "attack": 8,
                "defense": 2,
                "exp_reward": 15
            },
            "infected_staff": {
                "name": "感染職員",
                "hp": 45,
                "attack": 12,
                "defense": 4,
                "exp_reward": 25
            }
        },
        
        "assets/data/item_database.json": {
            "醫療包": {
                "type": "healing",
                "value": 30,
                "description": "回復30點血量"
            },
            "鑰匙卡": {
                "type": "key",
                "value": 1,
                "description": "開啟特殊區域的鑰匙"
            },
            "解藥": {
                "type": "special",
                "value": 1,
                "description": "拯救世界的神秘藥劑"
            }
        }
    }
    
    print("正在建立範例數據檔案...\n")
    
    created_files = 0
    for file_path, data in sample_data.items():
        try:
            import json
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"✅ 建立數據: {file_path}")
            created_files += 1
        except Exception as e:
            print(f"❌ 建立失敗: {file_path} - {e}")
    
    print(f"\n📊 成功建立 {created_files} 個數據檔案")
    return created_files > 0

def create_gitignore():
    """建立 .gitignore 檔案"""
    
    gitignore_content = """# 《末世第二餐廳》Git忽略檔案

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# 遊戲特定檔案
saves/
logs/
config.ini

# 素材檔案 (太大不適合版本控制)
assets/images/*.png
assets/images/*.jpg
assets/sounds/*.wav
assets/sounds/*.ogg
assets/sounds/*.mp3
assets/fonts/*.ttf
assets/fonts/*.ttc
assets/fonts/*.otf

# 但保留README檔案
!assets/*/README.md

# IDE
.vscode/
.idea/
*.swp
*.swo

# 作業系統
.DS_Store
Thumbs.db

# 建置檔案
build/
dist/
*.exe
*.msi
"""
    
    try:
        with open('.gitignore', 'w', encoding='utf-8') as f:
            f.write(gitignore_content)
        print("✅ 建立 .gitignore 檔案")
        return True
    except Exception as e:
        print(f"❌ 建立 .gitignore 失敗: {e}")
        return False

def main():
    """主程序"""
    
    print("開始建立《末世第二餐廳》專案結構...\n")
    
    # 檢查是否在空的資料夾中
    current_files = list(Path('.').glob('*'))
    if len(current_files) > 0:
        print("⚠️ 當前目錄不是空的")
        print("建議在新的空資料夾中執行此腳本")
        
        response = input("是否繼續? (y/n): ")
        if response.lower() != 'y':
            print("操作已取消")
            return
    
    success_count = 0
    
    # 1. 建立目錄結構
    if create_directory_structure():
        success_count += 1
    
    # 2. 建立說明檔案
    if create_readme_files():
        success_count += 1
    
    # 3. 建立範例數據
    if create_sample_data_files():
        success_count += 1
    
    # 4. 建立 .gitignore
    if create_gitignore():
        success_count += 1
    
    print(f"\n=== 專案建立完成 ===")
    print(f"成功執行 {success_count}/4 個建立步驟")
    
    print(f"\n📋 接下來的步驟:")
    print(f"1. 將所有 .py 遊戲檔案複製到此目錄")
    print(f"2. 執行: pip install -r requirements.txt")
    print(f"3. 執行: python setup.py (建立配置)")
    print(f"4. 將遊戲素材放入 assets/ 對應資料夾")
    print(f"5. 執行: python test_fonts.py (測試字體)")
    print(f"6. 執行: python main.py (啟動遊戲)")
    
    print(f"\n💡 提示:")
    print(f"- 查看各資料夾的 README.md 了解用途")
    print(f"- 建議使用 Git 進行版本控制")
    print(f"- 定期備份 saves/ 存檔資料夾")
    
    print(f"\n🎮 準備開始你的末世冒險吧！")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n操作被用戶中斷")
    except Exception as e:
        print(f"\n建立過程發生錯誤: {e}")
        print("請檢查目錄權限或手動建立資料夾")