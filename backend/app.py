from flask import Flask, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import  generate_password_hash, check_password_hash
from flask_bcrypt import Bcrypt #加解密
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta  #有關token
import os
from flask_jwt_extended import get_jwt
import logging
from sqlalchemy import and_



app = Flask(__name__)
CORS(app)  # 允許所有來源的請求
# 配置 CORS，允許來自前端的跨域請求並支持攜帶憑證（如 cookies）
CORS(app, supports_credentials=True, origins=["http://localhost:5173/"])
app.config['JWT_SECRET_KEY'] = "ckdsojcaojcosajcicdsji" 
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=30)  # 設定 Token 過期時間為 30 天
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blacklist.db'
jwt = JWTManager(app)  # 初始化 JWTManager

# 資料庫設置
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost:3306/ecoenjoy_db'  # 替換為正確的資料庫名字和改你的帳戶名字資料庫密碼
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
    subcats = db.relationship("Subcat", back_populates="maincat") #與 Subcat 之間的關聯
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
# 設置日誌
logging.basicConfig(level=logging.DEBUG)

#黑名單   
class TokenBlacklist(db.Model):
    __tablename__ = 'token_blacklist'  # 明確指定表名
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False, unique=True)

    def __init__(self, jti):
        self.jti = jti
#地區餐廳
class Subcat(db.Model):
    __tablename__ = 'subcat'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), nullable=False)
    address = db.Column(db.String(30), nullable=False)
    type = db.Column(db.String(30), nullable=False)
    maincat_id = db.Column(db.Integer, db.ForeignKey("maincat.id"), nullable=False)
    maincat = db.relationship("MainCategory", back_populates="subcats")  
    foods = db.relationship("Food", back_populates="subcat")  # 反向關聯
# 定義食物的資料庫模型
class Food(db.Model):
    __tablename__ = 'foods' 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Integer,nullable=False)
    carbo = db.Column(db.Float, nullable=False)
    protein = db.Column(db.Float, nullable=False)
    fat = db.Column(db.Float, nullable=False)
    calories = db.Column(db.Float, nullable=False)
    score = db.Column(db.Integer, nullable=False, default=0)  # 評分
    subcat_id = db.Column(db.Integer, db.ForeignKey("subcat.id"), nullable=False)
    subcat = db.relationship("Subcat", back_populates="foods")  # 反向關聯

#食物評論
# class Comment(db.Model):
#     __tablename__ = 'comment'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     user = db.Column(db.String(80), primary_key=True)
#     data = db.Column(db.String(100), nullable=False)
#     likes = db.Column(db.Integer, nullable=False, default=0) #點讚數
#     replies = db.Column(db.Integer, nullable=False, default=0) #回覆數
#     info_id = db.Column(db.Integer, db.ForeignKey("info.id"), nullable=False)
#     parent_comment_id = db.Column(db.Integer, db.ForeignKey("comment.id"), nullable=True)  # 父評論ID
#歷史訂單
# class Record(db.Model):
#     __tablename__ = 'record'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
#     info_id = db.Column(db.Integer, db.ForeignKey('info.id'), nullable=False)
#     timestamp = db.Column(db.DateTime, nullable=False, default=db.datetime.utcnow)


# 檢查 token 是否在黑名單中
@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_header, jwt_payload):
    jti = jwt_payload['jti']
    token = TokenBlacklist.query.filter_by(jti=jti).first()
    return token is not None


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

# 查詢 Subcat API
@app.route('/subcat/<int:maincat_id>', methods=['GET'])
def get_subcats(maincat_id):
    try:
        subcats = Subcat.query.filter_by(maincat_id=maincat_id).all()
        if subcats:
            return jsonify([{'id': subcat.id, 'name': subcat.name, 'address': subcat.address} for subcat in subcats])
        else:
            return jsonify({"message": "未找到相關的餐廳區域"}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 根據 Subcat 名稱查詢菜單
@app.route('/menu/<string:subcat_name>', methods=['GET'])
def get_menu(subcat_name):
    try:
        subcat = Subcat.query.filter_by(name=subcat_name).first()
        if subcat:
            foods = Food.query.filter_by(subcat_id=subcat.id).all()
            menu = [{
                "id": food.id,
                "name": food.name,
                "price": food.price,
                "carbo": food.carbo,
                "protein": food.protein,
                "fat": food.fat,
                "calories": food.calories,
                "score": food.score
            } for food in foods]
            return jsonify(menu)
        else:
            return jsonify({"message": "餐廳區域不存在"}), 404
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

#登出
@app.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    jti = get_jwt()['jti']
    blacklisted_token = TokenBlacklist(jti=jti)
    db.session.add(blacklisted_token)
    db.session.commit()
    return jsonify({"msg": "登出成功！"}), 200

@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    return jsonify({"msg": "這個 token 已被撤銷"}), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({"msg": "無效的 token"}), 422

@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({"msg": "請提供有效的 token"}), 401

#結帳
@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    # 處理 checkout 的邏輯
    return jsonify({"message": "Checkout Page"})


#食物分類
@app.route('/foods', methods=['GET'])
def get_foods():
    try:
        # 獲取多個 nutrient 和 level 參數
        nutrients = request.args.getlist('nutrient')
        levels = request.args.getlist('level')

        app.logger.debug(f'Nutrients: {nutrients}, Levels: {levels}')  # 日誌輸出

        # 檢查參數數量是否匹配
        if len(nutrients) != len(levels):
            return jsonify({"error": "營養素和等級參數數量不匹配"}), 400

        # 檢查 nutrient 和 level 是否為有效值
        valid_nutrients = ['protein', 'calories', 'fat', 'carbo']
        valid_levels = ['high', 'low']

        filters = []
        for nutrient, level in zip(nutrients, levels):
            app.logger.debug(f'Nutrient: {nutrient}, Level: {level}')  # 日誌輸出

            if nutrient not in valid_nutrients or level not in valid_levels:
                return jsonify({"error": f"無效的參數: {nutrient}, {level}"}), 400

            if level == 'high':
                if nutrient == 'protein':
                    filters.append(Food.protein > 20)  # 高蛋白質
                elif nutrient == 'calories':
                    filters.append(Food.calories > 400)  # 高熱量
                elif nutrient == 'fat':
                    filters.append(Food.fat > 20)  # 高脂肪
                elif nutrient == 'carbo':
                    filters.append(Food.carbo > 50)  # 高糖
            elif level == 'low':
                if nutrient == 'protein':
                    filters.append(Food.protein <= 20)  # 低蛋白質
                elif nutrient == 'calories':
                    filters.append(Food.calories <= 400)  # 低熱量
                elif nutrient == 'fat':
                    filters.append(Food.fat <= 20)  # 低脂肪
                elif nutrient == 'carbo':
                    filters.append(Food.carbo <= 50)  # 低糖

        # 將所有條件結合起來
        if filters:
            query = Food.query.filter(and_(*filters))
        else:
            query = Food.query

        # 執行查詢
        results = query.all()

        # 檢查結果是否為空
        if not results:
            return jsonify({"message": "沒有符合條件的食物"}), 200

        # 構建返回的結果列表，包含餐廳名稱
        food_list = []
        for food in results:
            # 查詢與該 food 相關的餐廳
            restaurant = Subcat.query.filter_by(id=food.subcat_id).first()

            food_data = {
                'id': food.id,
                'name': food.name,
                'protein': food.protein,
                'calories': food.calories,
                'fat': food.fat,
                'carbo': food.carbo,
                'score': food.score,
                'restaurant_name': restaurant.name if restaurant else '未知餐廳'
            }
            food_list.append(food_data)

        return jsonify(food_list), 200

    except Exception as e:
        app.logger.error(f'Error in get_foods: {str(e)}')
        return jsonify({"error": "內部伺服器錯誤"}), 500
    
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # 自動創建資料表
    app.run(debug=True)  # 確保這行存在
