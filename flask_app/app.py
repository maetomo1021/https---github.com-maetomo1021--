from flask import Flask, render_template, redirect, url_for, request, flash, jsonify
from flask_mail import Mail, Message
from discord_webhook import DiscordWebhook
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy,session
from werkzeug.security import generate_password_hash, check_password_hash
from models import db,Item
from bs4 import BeautifulSoup
import requests
import discord
import asyncio
import subprocess


app = Flask(__name__)
app.secret_key = 'maetomo1021-secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# UserModelはそのままに、新たにItemModelを追加
class UserModel(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(150), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)  # 場所のカラム
    link = db.Column(db.String(200), nullable=False)  # リンクのカラム

    def __repr__(self):
        return f"<Item {self.name}>"

@login_manager.user_loader
def load_user(user_id):
    return UserModel.query.get(int(user_id))

# データベース初期化
def create_tables():
    with app.app_context():
        db.create_all()
create_tables()

app.config['MAIL_USERNAME'] = 'maetomoda@gmail.com'
app.config['MAIL_PASSWORD'] = 'vktnjqzobcojryxj'



#######
@app.route('/')
@login_required
def index():
    items = Item.query.all()  # データベースから全アイテムを取得
    return render_template('index.html', username=current_user.username, items=items)

@app.route('/omake', methods=['GET'])
def omake():
    return render_template('omake.html')

@app.route('/ocr', methods=['GET'])
def ocr():
    return render_template('ocr.html')

@app.route('/calculator')
def calculator():
    return render_template('calculator.html')

@app.route('/game')
def game():
    return render_template('game.html')

@app.route('/weather')
def weather():
    return render_template('weather.html')




@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if UserModel.query.filter_by(username=username).first():
            flash('Username already exists.')
            return redirect(url_for('register'))
        new_user = UserModel(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful. Please log in.')
        return redirect(url_for('login'))
    return render_template('register.html')

# アイテム追加処理
@app.route('/add_item', methods=['POST'])
@login_required
def add_item():
    data = request.get_json()  # JSONデータを取得
    item_name = data.get('item_name')
    location = data.get('location')  # 場所
    link = data.get('link')          # リンク

    if item_name and location and link:
        new_item = Item(name=item_name, location=location, link=link)
        db.session.add(new_item)
        db.session.commit()
        # 新しいアイテムをレスポンスに含める
        return jsonify({
            "status": "success",
            "message": "Item added successfully!",
            "item_id": new_item.id,
            "item_name": new_item.name,
            "location": new_item.location,
            "link": new_item.link
        }), 201  # 成功のステータスコード
    return jsonify({"status": "error", "message": "Invalid data provided"}), 400  # エラー処理

# アイテム削除処理
@app.route('/delete_item/<int:item_id>', methods=['DELETE'])
@login_required
def delete_item(item_id):
    try:
        # データベースからアイテムを取得
        item = Item.query.get(item_id)
        if not item:
            return jsonify({"status": "error", "message": "アイテムが見つかりませんでした。"}), 404
        
        # アイテムを削除
        db.session.delete(item)
        db.session.commit()
        return jsonify({"status": "success", "message": "アイテムが削除されました。"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": f"削除中にエラーが発生しました: {e}"}), 500

# アイテム編集処理
@app.route('/edit_item/<int:item_id>', methods=['PUT'])
@login_required
def edit_item(item_id):
    try:
        data = request.get_json()
        print(f"Received data: {data}")  # リクエストデータの確認

        name = data.get('name')
        location = data.get('location')
        link = data.get('link')

        if not all([name, location, link]):
            return jsonify({"status": "error", "message": "すべての項目を入力してください"}), 400

        item = db.session.get(Item, item_id)
        if not item:
            return jsonify({"status": "error", "message": "アイテムが見つかりません"}), 404

        # データを更新
        item.name = name
        item.location = location
        item.link = link
        db.session.commit()

        # 成功時のレスポンス
        response = jsonify({"status": "success", "message": "アイテムが編集されました！"})
        print(f"Success response: {response.json}")
        return response, 200

    except Exception as e:
        # 例外が発生した場合
        error_message = f"エラーが発生しました: {str(e)}"
        print(error_message)
        return jsonify({"status": "error", "message": error_message}), 500


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = UserModel.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('index'))
        flash('Invalid username or password')
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

###########BOTの操作変編～～～～～～～～～～～～～～～～～
@app.route('/run_discord_bot', methods=['POST'])
@login_required
def run_discord_bot():
    try:
        # bot.py をバックグラウンドで実行
        subprocess.Popen(["python", "bot.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return jsonify({"status": "success", "message": "Discord Botを起動しました"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": f"エラー: {e}"}), 500

@app.route('/send_json_to_discord', methods=['POST'])
def send_json_to_discord():
    try:
        data = request.json  # HTMLから送られてきたJSONデータ
        json_str = json.dumps(data, ensure_ascii=False, indent=2)  # 日本語対応

        # JSON を bot.py に渡して起動
        subprocess.Popen(["python", "bot.py", json_str], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        return jsonify({"status": "success", "message": "JSONをDiscordに送信しました"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": f"エラー: {e}"}), 500


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5800)
