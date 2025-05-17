from flask import Flask, render_template, request, redirect
import os
import csv
from datetime import datetime

app = Flask(__name__)
DATA_FILE = 'data.csv'
goal_item1 = 1000  # 最終目標

# データ初期化
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['date', 'item1'])

def load_data():
    data = []
    with open(DATA_FILE, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append({'date': row['date'], 'item1': int(row['item1'])})
    return data

@app.route('/', methods=['GET', 'POST'])
def index():
    today = datetime.now().strftime('%m/%d')
    data = load_data()

    if request.method == 'POST':
        count1 = int(request.form['count1'])

        # 今日の行があれば更新、なければ追加
        updated = False
        for row in data:
            if row['date'] == today:
                row['item1'] += count1
                updated = True
                break
        if not updated:
            data.append({'date': today, 'item1': count1})

        # 保存
        with open(DATA_FILE, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['date', 'item1'])
            writer.writeheader()
            writer.writerows(data)

        return redirect('/')

    # 表示用の値
    dates = [row['date'] for row in data]
    item1 = [row['item1'] for row in data]

    total1 = sum(item1)
    avg1 = round(total1 / len(item1), 2) if item1 else 0
    max1 = max(item1) if item1 else 0
    min1 = min(item1) if item1 else 0
    remaining = max(goal_item1 - total1, 0)

    return render_template('index.html',
                           dates=dates,
                           item1=item1,
                           total1=total1,
                           avg1=avg1,
                           max1=max1,
                           min1=min1,
                           remaining=remaining,
                           goal_item1=goal_item1)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
