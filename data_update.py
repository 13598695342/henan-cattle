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

    # 先获取最新数据列表页面
    list_url = 'http://www.agri.cn/sj/jcyj/'
    urls = []

    try:
        resp = requests.get(list_url, headers=headers, timeout=30)
        if resp.status_code == 200:
            resp.encoding = 'utf-8'
            soup = BeautifulSoup(resp.text, 'html.parser')
            # 提取所有5月的畜产品价格页面链接
            for link in soup.find_all('a', href=True):
                href = link['href']
                if '202605/t202605' in href and 'jcyj' in href:
                    full_url = 'http://www.agri.cn/sj/jcyj/' + href.replace('./', '')
                    if full_url not in urls:
                        urls.append(full_url)
    except Exception as e:
        print(f"  ✗ 获取列表失败: {str(e)[:50]}")

    # 如果没找到，使用备用URL列表
    if not urls:
        urls = [
            'http://www.agri.cn/sj/jcyj/202605/t20260520_8837884.htm',
            'http://www.agri.cn/sj/jcyj/202605/t20260514_8836323.htm',
            'http://www.agri.cn/sj/jcyj/202605/t20260509_8834182.htm',
        ]

    all_data = []

    for url in urls[:5]:  # 最多取5个
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

def push_to_wechat(data_list):
    """通过企业微信群机器人推送到微信"""
    if not data_list:
        return

    webhook_url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=854fa99f-2d73-47f5-b37f-e250d20100a8"

    latest = data_list[0]
    previous = data_list[1] if len(data_list) > 1 else None

    # 计算涨跌
    trend_text = ""
    if previous and latest.get('活牛价格') and previous.get('活牛价格'):
        diff = float(latest['活牛价格']) - float(previous['活牛价格'])
        if diff > 0:
            trend_text = f"↑+{diff:.2f}"
        elif diff < 0:
            trend_text = f"↓{diff:.2f}"
        else:
            trend_text = "→持平"

    date_str = latest.get('日期', '--')
    cow_price = latest.get('活牛价格', '--')
    beef_price = latest.get('牛肉价格', '--')
    sheep_price = latest.get('羊肉价格', '--')
    pig_price = latest.get('猪肉价格', '--')
    egg_price = latest.get('鸡蛋价格', '--')

    content = f"【河南牛价更新】{date_str}\n\n"
    content += f"🐄 活牛：{cow_price} 元/公斤 {trend_text}\n"
    content += f"🥩 牛肉：{beef_price} 元/公斤\n"
    content += f"🐑 羊肉：{sheep_price} 元/公斤\n"
    content += f"🐖 猪肉：{pig_price} 元/公斤\n"
    content += f"🥚 鸡蛋：{egg_price} 元/公斤\n"

    if previous:
        content += f"\n上周对比（{previous.get('日期', '--')}）：\n"
        content += f"活牛：{previous.get('活牛价格', '--')} → {cow_price} 元/公斤\n"

    content += f"\n🌐 https://dulcet-daifuku-4f5ffe.netlify.app/"
    content += f"\n更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}"

    payload = {
        "msgtype": "text",
        "text": {
            "content": content
        }
    }

    print("\n正在推送到企业微信群...")
    try:
        resp = requests.post(webhook_url, json=payload, timeout=30)
        result = resp.json()
        if result.get('errcode') == 0:
            print(f"  ✓ 推送成功")
        else:
            print(f"  ✗ 推送失败: {result.get('errmsg', '未知错误')}")
    except Exception as e:
        print(f"  ✗ 推送异常: {str(e)[:100]}")

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

    # 5. 推送到微信
    if price_data:
        push_to_wechat(price_data)

    print()
    print("=" * 50)
    print("更新完成！")
    print("请重新部署到 Netlify")
    print("=" * 50)

if __name__ == '__main__':
    main()
