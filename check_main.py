#!/usr/bin/env python3
"""
檢查main.py的結構和內容
"""

import ast
import sys

def analyze_main_py():
    """分析main.py的結構"""
    print("🔍 分析 main.py 結構...")
    
    try:
        with open('main.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"📄 檔案大小: {len(content)} 字元")
        print(f"📄 行數: {len(content.splitlines())}")
        
        # 解析AST
        try:
            tree = ast.parse(content)
            print("✅ Python語法正確")
        except SyntaxError as e:
            print(f"❌ Python語法錯誤: {e}")
            return False
        
        # 檢查類別和函數
        classes = []
        functions = []
        imports = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                classes.append(node.name)
            elif isinstance(node, ast.FunctionDef):
                functions.append(node.name)
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                for alias in node.names:
                    imports.append(f"{module}.{alias.name}")
        
        print(f"\n📋 發現的類別: {classes}")
        print(f"📋 發現的函數: {functions[:10]}...")  # 只顯示前10個
        print(f"📋 導入的模組: {imports[:10]}...")   # 只顯示前10個
        
        # 檢查關鍵元素
        if 'Game' in classes:
            print("✅ 找到Game類別")
        else:
            print("❌ 未找到Game類別")
            print(f"可用的類別: {classes}")
        
        if 'main' in functions:
            print("✅ 找到main函數")
        else:
            print("❌ 未找到main函數")
        
        # 檢查__main__區塊
        if '__main__' in content:
            print("✅ 找到__main__區塊")
        else:
            print("❌ 未找到__main__區塊")
        
        return True
        
    except FileNotFoundError:
        print("❌ 找不到main.py檔案")
        return False
    except Exception as e:
        print(f"❌ 分析失敗: {e}")
        return False

def test_import():
    """測試導入main模組"""
    print("\n🔍 測試導入main模組...")
    
    try:
        import main
        print("✅ main模組導入成功")
        
        # 檢查屬性
        if hasattr(main, 'Game'):
            print("✅ main.Game存在")
            try:
                # 嘗試創建實例
                game = main.Game()
                print("✅ Game實例創建成功")
                return True
            except Exception as e:
                print(f"❌ Game實例創建失敗: {e}")
                import traceback
                traceback.print_exc()
                return False
        else:
            print("❌ main.Game不存在")
            print(f"main模組的屬性: {[attr for attr in dir(main) if not attr.startswith('_')]}")
            return False
            
    except Exception as e:
        print(f"❌ main模組導入失敗: {e}")
        import traceback
        traceback.print_exc()
        return False

def show_main_content():
    """顯示main.py的部分內容"""
    print("\n🔍 main.py 內容預覽...")
    
    try:
        with open('main.py', 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        print("前20行:")
        for i, line in enumerate(lines[:20], 1):
            print(f"{i:2d}: {line.rstrip()}")
        
        print("\n後20行:")
        for i, line in enumerate(lines[-20:], len(lines)-19):
            print(f"{i:2d}: {line.rstrip()}")
            
    except Exception as e:
        print(f"❌ 讀取失敗: {e}")

def main():
    """主程序"""
    print("🔍 main.py 結構檢查工具")
    print("=" * 40)
    
    # 分析檔案結構
    if not analyze_main_py():
        return
    
    # 測試導入
    if not test_import():
        print("\n💡 建議檢查main.py的內容:")
        show_main_content()
    else:
        print("\n🎉 main.py 結構正常！")
        print("問題可能在遊戲運行過程中，嘗試:")
        print("python3 main.py")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"💥 檢查工具異常: {e}")
        import traceback
        traceback.print_exc()