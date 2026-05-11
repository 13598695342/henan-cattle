"""
河南牛价数据 - 自动更新
部署需要手动操作（只需30秒）
"""

import os
import sys
import subprocess
import zipfile

FOLDER = os.path.dirname(os.path.abspath(__file__))

def update_data():
    """更新数据"""
    print("[1/2] 正在获取最新数据...")
    try:
        sys.path.insert(0, FOLDER)
        import data_update
        print("  ✓ 数据更新成功")
        return True
    except Exception as e:
        print(f"  ✗ 数据更新失败: {e}")
        return False

def deploy_manual():
    """手动部署提示"""
    print()
    print("[2/2] 部署到 Netlify")
    print("  1. 打开浏览器访问: https://app.netlify.com/drop")
    print("  2. 拖入整个文件夹到页面中")
    print("  3. 等待2-3秒自动部署完成")
    print()
    print("  ✓ 完成！网站将自动更新")
    print()
    print("  网站地址: https://dulcet-daifuku-4f5ffe.netlify.app/")
    return True

def main():
    print("=" * 50)
    print("  河南牛价数据 - 自动更新")
    print("=" * 50)
    print()

    # 1. 更新数据
    if not update_data():
        input("\n按回车键退出...")
        return

    # 2. 部署提示
    print()
    deploy_manual()

    print()
    print("=" * 50)
    print("  完成!")
    print("=" * 50)

if __name__ == '__main__':
    main()
    input("\n按回车键退出...")
