#!/usr/bin/env python3
"""
末世第二餐廳 - 測試運行器
運行所有測試並生成詳細報告
"""

import sys
import os
import time
import subprocess
import importlib.util
from datetime import datetime

# 添加項目根目錄到 Python 路徑
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

class TestRunner:
    """測試運行器"""
    
    def __init__(self):
        self.test_files = [
            'tests/test_game_state.py',
            'tests/test_combat.py', 
            'tests/test_inventory.py',
            'tests/test_main.py',
            'tests/test_integration.py',
            'tests/test_performance.py'
        ]
        self.results = {}
        self.start_time = None
        self.end_time = None

    def print_header(self):
        """顯示測試標題"""
        print("=" * 80)
        print("🎮 末世第二餐廳 - 完整測試套件")
        print("=" * 80)
        print(f"📅 測試時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🐍 Python 版本: {sys.version}")
        print(f"📁 項目路徑: {project_root}")
        print("=" * 80)

    def check_dependencies(self):
        """檢查測試依賴"""
        print("\n🔍 檢查測試依賴...")
        
        dependencies = {
            'pygame': '遊戲引擎',
            'pytest': '測試框架 (可選)',
            'psutil': '性能監控 (可選)'
        }
        
        available = {}
        for dep, desc in dependencies.items():
            try:
                __import__(dep)
                available[dep] = True
                print(f"✅ {dep}: {desc}")
            except ImportError:
                available[dep] = False
                if dep == 'pytest':
                    print(f"⚠️  {dep}: {desc} - 將使用內建測試運行器")
                elif dep == 'psutil':
                    print(f"⚠️  {dep}: {desc} - 跳過記憶體監控測試")
                else:
                    print(f"❌ {dep}: {desc} - 必需但未安裝")
        
        return available

    def run_single_test(self, test_file):
        """運行單個測試文件"""
        print(f"\n📝 運行測試: {test_file}")
        print("-" * 50)
        
        if not os.path.exists(test_file):
            print(f"❌ 測試文件不存在: {test_file}")
            return {"status": "missing", "passed": 0, "failed": 1, "duration": 0}
        
        start_time = time.time()
        
        try:
            # 嘗試直接導入和運行測試
            module_name = test_file.replace('/', '.').replace('.py', '')
            spec = importlib.util.spec_from_file_location(module_name, test_file)
            module = importlib.util.module_from_spec(spec)
            
            # 捕獲輸出
            import io
            from contextlib import redirect_stdout, redirect_stderr
            
            stdout_capture = io.StringIO()
            stderr_capture = io.StringIO()
            
            with redirect_stdout(stdout_capture), redirect_stderr(stderr_capture):
                spec.loader.exec_module(module)
            
            stdout_output = stdout_capture.getvalue()
            stderr_output = stderr_capture.getvalue()
            
            # 顯示輸出
            if stdout_output:
                print(stdout_output)
            if stderr_output:
                print("STDERR:", stderr_output)
            
            # 分析輸出來確定結果
            lines = stdout_output.split('\n')
            passed = 0
            failed = 0
            
            for line in lines:
                if '✅' in line and ('通過' in line or 'passed' in line):
                    passed += 1
                elif '❌' in line and ('失敗' in line or 'failed' in line):
                    failed += 1
                elif 'passed' in line.lower() and 'failed' in line.lower():
                    # 解析總結行，如 "✅ 通過: 5"
                    try:
                        if '通過:' in line:
                            passed = int(line.split('通過:')[1].strip().split()[0])
                        if '失敗:' in line:
                            failed = int(line.split('失敗:')[1].strip().split()[0])
                    except:
                        pass
            
            duration = time.time() - start_time
            status = "passed" if failed == 0 else "failed"
            
            return {
                "status": status,
                "passed": passed,
                "failed": failed,
                "duration": duration,
                "output": stdout_output
            }
            
        except Exception as e:
            duration = time.time() - start_time
            print(f"❌ 測試執行錯誤: {e}")
            import traceback
            print(f"詳細錯誤: {traceback.format_exc()}")
            
            return {
                "status": "error",
                "passed": 0,
                "failed": 1,
                "duration": duration,
                "error": str(e)
            }

    def run_with_pytest(self, test_file):
        """使用 pytest 運行測試"""
        try:
            result = subprocess.run([
                sys.executable, '-m', 'pytest', test_file, '-v', '--tb=short'
            ], capture_output=True, text=True, timeout=300)
            
            return {
                "status": "passed" if result.returncode == 0 else "failed",
                "output": result.stdout,
                "error": result.stderr,
                "returncode": result.returncode
            }
        except subprocess.TimeoutExpired:
            return {
                "status": "timeout",
                "error": "測試執行超時 (5分鐘)"
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }

    def run_all_tests(self, use_pytest=False):
        """運行所有測試"""
        self.start_time = time.time()
        
        print(f"\n🚀 開始運行所有測試 ({'使用 pytest' if use_pytest else '使用內建運行器'})")
        
        for test_file in self.test_files:
            if use_pytest:
                result = self.run_with_pytest(test_file)
            else:
                result = self.run_single_test(test_file)
            
            self.results[test_file] = result
        
        self.end_time = time.time()

    def generate_report(self):
        """生成測試報告"""
        total_duration = self.end_time - self.start_time
        
        print("\n" + "=" * 80)
        print("📊 測試報告")
        print("=" * 80)
        
        total_passed = 0
        total_failed = 0
        total_errors = 0
        
        for test_file, result in self.results.items():
            status_icon = {
                "passed": "✅",
                "failed": "❌", 
                "error": "💥",
                "missing": "📄",
                "timeout": "⏰"
            }.get(result["status"], "❓")
            
            print(f"\n{status_icon} {test_file}")
            print(f"   狀態: {result['status']}")
            
            if "passed" in result and "failed" in result:
                print(f"   通過: {result['passed']}")
                print(f"   失敗: {result['failed']}")
                total_passed += result["passed"]
                total_failed += result["failed"]
            
            if "duration" in result:
                print(f"   耗時: {result['duration']:.2f} 秒")
            
            if result["status"] == "error" and "error" in result:
                print(f"   錯誤: {result['error']}")
                total_errors += 1
        
        print("\n" + "-" * 80)
        print("📈 總結")
        print("-" * 80)
        print(f"🏃 測試文件: {len(self.test_files)}")
        print(f"✅ 總通過: {total_passed}")
        print(f"❌ 總失敗: {total_failed}")
        print(f"💥 執行錯誤: {total_errors}")
        print(f"⏱️  總耗時: {total_duration:.2f} 秒")
        
        if total_passed + total_failed > 0:
            success_rate = (total_passed / (total_passed + total_failed)) * 100
            print(f"📊 成功率: {success_rate:.1f}%")
        
        # 評估等級
        if total_failed == 0 and total_errors == 0:
            print("\n🎉 測試狀態: 優秀 - 所有測試通過！")
        elif total_failed <= 2:
            print("\n👍 測試狀態: 良好 - 大部分測試通過")
        elif total_failed <= 5:
            print("\n⚠️  測試狀態: 普通 - 需要關注失敗的測試")
        else:
            print("\n🔧 測試狀態: 需要改進 - 多個測試失敗")

    def save_report_to_file(self, filename="test_report.txt"):
        """保存報告到文件"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"末世第二餐廳 - 測試報告\n")
                f.write(f"生成時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 50 + "\n\n")
                
                for test_file, result in self.results.items():
                    f.write(f"測試文件: {test_file}\n")
                    f.write(f"狀態: {result['status']}\n")
                    
                    if "passed" in result and "failed" in result:
                        f.write(f"通過: {result['passed']}\n")
                        f.write(f"失敗: {result['failed']}\n")
                    
                    if "duration" in result:
                        f.write(f"耗時: {result['duration']:.2f} 秒\n")
                    
                    if "output" in result:
                        f.write("輸出:\n")
                        f.write(result["output"])
                        f.write("\n")
                    
                    f.write("-" * 30 + "\n\n")
                
                total_duration = self.end_time - self.start_time
                f.write(f"總耗時: {total_duration:.2f} 秒\n")
            
            print(f"\n💾 報告已保存到: {filename}")
            
        except Exception as e:
            print(f"❌ 保存報告失敗: {e}")

    def provide_recommendations(self):
        """提供測試建議"""
        print("\n" + "=" * 80)
        print("💡 測試建議")
        print("=" * 80)
        
        failed_tests = [test for test, result in self.results.items() 
                       if result["status"] in ["failed", "error"]]
        
        if not failed_tests:
            print("🎉 太棒了！所有測試都通過了。")
            print("建議:")
            print("• 定期運行測試以確保代碼品質")
            print("• 在添加新功能時編寫對應的測試")
            print("• 考慮增加更多邊界條件測試")
        else:
            print("🔧 有一些測試需要關注:")
            for test in failed_tests:
                print(f"• {test}")
            
            print("\n建議的修復步驟:")
            print("1. 檢查失敗測試的具體錯誤訊息")
            print("2. 確認相關的遊戲邏輯是否正確")
            print("3. 更新測試以匹配當前的實現")
            print("4. 檢查是否有遺漏的依賴或設置")
        
        print("\n📚 測試最佳實踐:")
        print("• 保持測試簡潔和專注")
        print("• 使用清晰的測試命名")
        print("• 定期更新測試以反映代碼變更")
        print("• 考慮添加性能基準測試")


def main():
    """主函數"""
    runner = TestRunner()
    
    runner.print_header()
    
    # 檢查依賴
    dependencies = runner.check_dependencies()
    
    # 決定使用哪種測試運行器
    use_pytest = dependencies.get('pytest', False)
    
    if len(sys.argv) > 1:
        if '--pytest' in sys.argv:
            use_pytest = True
        elif '--builtin' in sys.argv:
            use_pytest = False
        elif '--help' in sys.argv or '-h' in sys.argv:
            print("\n使用方法:")
            print("  python run_all_tests.py           # 自動選擇測試運行器")
            print("  python run_all_tests.py --pytest  # 強制使用 pytest")
            print("  python run_all_tests.py --builtin # 強制使用內建運行器")
            print("  python run_all_tests.py --help    # 顯示此幫助")
            return
    
    # 運行測試
    runner.run_all_tests(use_pytest=use_pytest)
    
    # 生成報告
    runner.generate_report()
    
    # 保存報告
    if '--save-report' in sys.argv:
        runner.save_report_to_file()
    
    # 提供建議
    runner.provide_recommendations()
    
    print("\n" + "=" * 80)
    print("測試完成！感謝使用末世第二餐廳測試套件。")
    print("=" * 80)


if __name__ == "__main__":
    main()