from flask import Flask, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import  check_password_hash
from flask_bcrypt import Bcrypt
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # 允許所有來源的請求

bcrypt = Bcrypt(app)
# 資料庫設置
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost:3306/ecoenjoy_db'  # 替換為正確的資料庫 URI
app.config['SECRET_KEY'] = '51718'
db = SQLAlchemy(app)

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
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

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
    data = request.get_json()
    
    username = data.get('username').strip()
    password = data.get('password').strip()

    user = User.query.filter_by(username=username).first()

    # 檢查用戶是否存在，並驗證密碼
    if user and bcrypt.check_password_hash(user.password, password):
        session['user_id'] = user.id  # 儲存用戶ID
        return jsonify({'success': True, 'message': '登入成功！'}), 200
    else:
        return jsonify({'success': False, 'message': '用戶名或密碼錯誤！'}), 401

def get_user_info():
    user_id = session.get('user_id')
    if user_id is None:
        return jsonify({'error': '用戶未登入'}), 401

    # 其他邏輯處理
    return jsonify({'success': '用戶已登入'})

if __name__ == '__main__':
    app.run(debug=True)
 