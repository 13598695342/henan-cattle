"""
设置 Windows 定时任务
每天早上9点自动更新数据
"""

import os
import subprocess
import sys

# 获取脚本所在目录
script_dir = os.path.dirname(os.path.abspath(__file__))
bat_path = os.path.join(script_dir, 'auto_update.bat')

# Windows 计划任务命令
task_name = "河南牛价数据更新"

# 删除已存在的任务
delete_cmd = f'schtasks /delete /tn "{task_name}" /f'
try:
    subprocess.run(delete_cmd, shell=True, check=False)
    print("已删除旧任务（如果存在）")
except:
    pass

# 创建新任务
# 每天早上9点运行
create_cmd = f'''
schtasks /create /tn "{task_name}" /tr "{bat_path}" /sc daily /st 09:00 /f
'''

print("正在创建定时任务...")
print(f"任务名称: {task_name}")
print(f"运行时间: 每天 09:00")
print(f"执行脚本: {bat_path}")
print()

try:
    result = subprocess.run(create_cmd, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        print("✓ 定时任务创建成功！")
        print()
        print("=" * 50)
        print("设置完成！")
        print("=" * 50)
        print()
        print("每天早上9点会自动运行更新程序")
        print("更新后的数据会保存在 data.json 文件中")
        print()
        print("提示：部署到 Netlify 后网站会自动显示最新数据")
    else:
        print(f"✗ 创建失败: {result.stderr}")
        print()
        print("你可以手动创建定时任务：")
        print(f"1. 打开 Windows 任务计划程序")
        print(f"2. 创建基本任务")
        print(f"3. 名称: {task_name}")
        print(f"4. 触发器: 每天 09:00")
        print(f"5. 操作: 启动程序 → 选择 {bat_path}")
except Exception as e:
    print(f"错误: {e}")
    print()
    print("请手动创建定时任务")

input("\n按回车键退出...")
