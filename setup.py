#!/usr/bin/env python3
"""
末世第二餐廳 - 遊戲安裝腳本
"""

import os
import sys
import subprocess

def check_python_version():
    """檢查Python版本"""
    if sys.version_info < (3, 7):
        print("錯誤: 需要Python 3.7或更高版本")
        print(f"當前版本: {sys.version}")
        return False
    return True

def install_requirements():
    """安裝相依套件"""
    try:
        print("正在安裝相依套件...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("套件安裝完成！")
        return True
    except subprocess.CalledProcessError:
        print("錯誤: 套件安裝失敗")
        return False

def create_assets_directory():
    """創建素材資料夾"""
    assets_dirs = [
        "assets",
        "assets/images",
        "assets/sounds", 
        "assets/fonts"
    ]
    
    for directory in assets_dirs:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"創建資料夾: {directory}")
    
    # 創建素材說明檔案
    readme_content = """# 素材資料夾

## 目錄結構

- images/ : 圖片檔案 (PNG, JPG)
- sounds/ : 音效檔案 (WAV, OGG, MP3)
- fonts/  : 字體檔案 (TTF, OTF)

## 建議素材

### 圖片 (images/)
- player.png : 玩家角色
- zombie.png : 殭屍敵人
- alien.png : 外星人敵人
- tiles/ : 地圖磚塊
- ui/ : 使用者介面元素

### 音效 (sounds/)
- bgm.ogg : 背景音樂
- attack.wav : 攻擊音效
- pickup.wav : 拾取物品音效
- door.wav : 開門音效

### 字體 (fonts/)
- pixel.ttf : 像素字體
"""
    
    with open("assets/README.md", "w", encoding="utf-8") as f:
        f.write(readme_content)

def create_game_config():
    """創建遊戲設定檔"""
    config_content = """# 末世第二餐廳 - 遊戲設定檔

[display]
width = 1024
height = 768
fullscreen = false
fps = 60

[audio]
master_volume = 0.8
sfx_volume = 0.7
music_volume = 0.6

[gameplay]
difficulty = normal  # easy, normal, hard
auto_save = true
encounter_rate = 0.05

[controls]
move_up = K_UP
move_down = K_DOWN
move_left = K_LEFT
move_right = K_RIGHT
interact = K_SPACE
inventory = K_i
map = K_m
pause = K_ESCAPE
"""
    
    with open("config.ini", "w", encoding="utf-8") as f:
        f.write(config_content)

def main():
    """主安裝程序"""
    print("=== 末世第二餐廳 安裝程序 ===")
    print()
    
    # 檢查Python版本
    if not check_python_version():
        return
    
    # 安裝相依套件
    if not install_requirements():
        return
    
    # 創建素材資料夾
    create_assets_directory()
    
    # 創建設定檔
    create_game_config()
    
    print()
    print("=== 安裝完成！ ===")
    print()
    print("使用方法:")
    print("1. 將遊戲素材放入 assets/ 資料夾")
    print("2. 執行: python main.py")
    print("3. 享受遊戲！")
    print()
    print("更多資訊請參閱 README.md")

if __name__ == "__main__":
    main()