"""
河南牛业数据自动更新脚本
从多个数据源自动获取最新数据
"""

import requests
from bs4 import BeautifulSoup
import re
import json
import os
from datetime import datetime

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
}

def get_latest_price():
    """从中国农业信息网获取最新价格"""
    print("正在获取最新价格数据...")

    # 最新几周的数据页面
    urls = [
        'http://www.agri.cn/sj/jcyj/202605/t20260509_8834182.htm',  # 4月第5周
        'http://www.agri.cn/sj/jcyj/202605/t20260509_8834183.htm',  # 4月第4周
    ]

    all_data = []

    for url in urls:
        try:
            resp = requests.get(url, headers=headers, timeout=30)
            if resp.status_code == 200:
                resp.encoding = 'utf-8'
                soup = BeautifulSoup(resp.text, 'html.parser')
                content = soup.find('div', class_='TRS_Editor')
                if content:
                    text = content.get_text()

                    # 提取日期
                    date_match = re.search(r'(\d{4})年(\d{1,2})月第(\d+)周', text)
                    if date_match:
                        year, month, week = date_match.groups()
                        date_str = f"{year}年{month}月第{week}周"
                    else:
                        date_str = "未知日期"

                    # 提取价格数据
                    data = {'日期': date_str}

                    # 活牛价格
                    match = re.search(r'活牛价格(\d+\.?\d*)元/公斤', text)
                    if match:
                        data['活牛价格'] = match.group(1)

                    # 牛肉价格
                    match = re.search(r'牛肉平均价格(\d+\.?\d*)元/公斤', text)
                    if match:
                        data['牛肉价格'] = match.group(1)

                    # 羊肉价格
                    match = re.search(r'羊肉平均价格(\d+\.?\d*)元/公斤', text)
                    if match:
                        data['羊肉价格'] = match.group(1)

                    # 猪肉价格
                    match = re.search(r'猪肉平均价格(\d+\.?\d*)元/公斤', text)
                    if match:
                        data['猪肉价格'] = match.group(1)

                    # 鸡蛋价格
                    match = re.search(r'鸡蛋平均价格(\d+\.?\d*)元/公斤', text)
                    if match:
                        data['鸡蛋价格'] = match.group(1)

                    # 同比环比
                    if '活牛' in text:
                        # 提取活牛同比环比
                        match = re.search(r'活牛价格.*?同比(.[+-]?\d+\.?\d*%).*?环比(.[+-]?\d+\.?\d*%)', text)
                        if match:
                            data['活牛同比'] = match.group(1)
                            data['活牛环比'] = match.group(2)

                    if data.get('活牛价格'):
                        all_data.append(data)
                        print(f"  ✓ {date_str}: 活牛 {data.get('活牛价格')} 元/公斤")

        except Exception as e:
            print(f"  ✗ 获取失败: {str(e)[:50]}")

    return all_data

def get_henan_data():
    """获取河南省数据"""
    print("\n正在获取河南省数据...")

    # 这里可以添加河南省统计局的数据源
    # 目前使用示例数据

    henan_data = {
        '河南省存栏量': '3256万头',
        '河南省产量': '全国前三',
        '主要产地': ['驻马店', '南阳', '商丘', '周口', '开封']
    }

    return henan_data

def update_website(data_list):
    """更新网站数据"""
    print("\n正在更新网站数据...")

    if not data_list:
        print("  ✗ 没有数据可更新")
        return

    latest = data_list[0]  # 最新一周的数据

    # 读取HTML模板
    html_path = os.path.join(os.path.dirname(__file__), 'index.html')
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # 更新数据
    if latest.get('活牛价格'):
        html = re.sub(r'id="cowPrice">[\d.]+', f'id="cowPrice">{latest["活牛价格"]}', html)

    if latest.get('牛肉价格'):
        html = re.sub(r'id="beefPrice">[\d.]+', f'id="beefPrice">{latest["牛肉价格"]}', html)

    if latest.get('羊肉价格'):
        html = re.sub(r'id="sheepPrice">[\d.]+', f'id="sheepPrice">{latest["羊肉价格"]}', html)

    # 更新日期
    if latest.get('日期'):
        html = html.replace('数据更新：2026年4月第5周', f'数据更新：{latest["日期"]}')

    # 保存
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"  ✓ 网站已更新: 活牛 {latest.get('活牛价格')} 元/公斤")

    return latest

def save_data_json(data_list):
    """保存数据到JSON文件"""
    output_path = os.path.join(os.path.dirname(__file__), 'data.json')

    save_data = {
        '更新时间': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        '价格数据': data_list
    }

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(save_data, f, ensure_ascii=False, indent=2)

    print(f"  ✓ 数据已保存: {output_path}")

def main():
    print("=" * 50)
    print("河南牛业数据自动更新工具")
    print("=" * 50)
    print()

    # 1. 获取最新价格
    price_data = get_latest_price()

    # 2. 获取河南省数据
    henan_data = get_henan_data()

    # 3. 保存数据
    save_data_json(price_data)

    # 4. 更新网站
    if price_data:
        update_website(price_data)

    print()
    print("=" * 50)
    print("更新完成！")
    print("请重新部署到 Netlify")
    print("=" * 50)

if __name__ == '__main__':
    main()
