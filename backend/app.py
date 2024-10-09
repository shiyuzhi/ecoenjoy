from flask import Flask, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import  generate_password_hash, check_password_hash
from flask_bcrypt import Bcrypt #加解密
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta  #有關token
import os
from config import Config  # 引入配置
from flask_jwt_extended import get_jwt



app = Flask(__name__)
CORS(app)  # 允許所有來源的請求
# 配置 CORS，允許來自前端的跨域請求並支持攜帶憑證（如 cookies）
CORS(app, supports_credentials=True, origins=[" http://localhost:5173/"])
app.config['JWT_SECRET_KEY'] = "ckdsojcaojcosajcicdsji" 
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=30)  # 設定 Token 過期時間為 30 天
jwt = JWTManager(app)  # 初始化 JWTManager

# 資料庫設置
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost:3306/ecoenjoy_db'  # 替換為正確的資料庫 URI
app.config['SECRET_KEY'] = '548755585214562255632556999369954556'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# 簡單的黑名單用於存儲無效 token
token_blacklist = set()
revoked_tokens = set()  # 儲存撤銷的 token

# 定義資料表
class MainCategory(db.Model):
    __tablename__ = 'maincat'  # 設置資料表名稱為 maincat
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

# 定義 Offer 資料表
class Offer(db.Model):
    __tablename__ = 'offers'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)

#使用者
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

# 創建資料表
with app.app_context():
    db.create_all()

@app.route('/', methods=['GET'])

# 獲取主類別 API
@app.route('/maincat', methods=['GET'])
def get_main_categories():
    try:
        maincats = MainCategory.query.all()
        return jsonify([{'id': maincat.id, 'name': maincat.name} for maincat in maincats])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 建立 API 路由來取得優惠資料
@app.route('/offers', methods=['GET'])
def get_offers():
    offers = Offer.query.all()
    offer_list = [{'id': offer.id, 'title': offer.title, 'description': offer.description} for offer in offers]
    return jsonify(offer_list)

#註冊
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    # 檢查用戶名和電子郵件是否已存在
    existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
    if existing_user:
        return jsonify({'success': False, 'message': '用戶名或電子郵件已存在！'}), 400

    # 創建新用戶
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')  # 使用 Flask-Bcrypt 進行哈希
    new_user = User(username=username, email=email, password=hashed_password)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'success': True, 'message': '註冊成功！'}), 201


#登入
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    user = User.query.filter_by(username=username).first()

    if user and bcrypt.check_password_hash(user.password, password):
        # 生成 JWT Token
        access_token = create_access_token(identity={'username': username})
        return jsonify({'success': True, 'access_token': access_token}), 200
    else:
        return jsonify({'success': False, 'message': '用戶名或密碼錯誤！'}), 401


#用戶資料
@app.route('/user', methods=['GET'])
@jwt_required()  # 確保用戶必須提供有效的 Token
def get_user():
    current_user = get_jwt_identity()  # 獲取當前用戶身份
    user = User.query.filter_by(username=current_user['username']).first()  # 根據用戶名獲取用戶資料

    if user:
        user_data = {
            'username': user.username,
            'email': user.email,  # 可以返回其他需要的資料
        }
        return jsonify({"user": user_data}), 200
    return jsonify({"error": "用戶不存在"}), 404

@app.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    jti = get_jwt()['jti']  # 獲取 token 的唯一標識
    token_blacklist.add(jti)  # 將 token 加入黑名單
    return jsonify({"msg": "登出成功！"}), 200


if __name__ == '__main__':
    app.run(debug=True)  # 確保這行存在
