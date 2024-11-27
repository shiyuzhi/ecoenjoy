from flask import Flask, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import  generate_password_hash, check_password_hash
from flask_bcrypt import Bcrypt #加解密
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta, datetime, timezone  #有關token, (更新)有關歷史訂單和UTC時間
import os
from flask_jwt_extended import get_jwt
import logging
from sqlalchemy import and_
from werkzeug.exceptions import HTTPException
from werkzeug.exceptions import Unauthorized
import traceback
from sqlalchemy import func

app = Flask(__name__)
CORS(app)  # 允許所有來源的請求
# 配置 CORS，允許來自前端的跨域請求並支持攜帶憑證（如 cookies）
CORS(app, supports_credentials=True, origins=["http://localhost:5173/"])
app.config['JWT_SECRET_KEY'] = "ckdsojcaojcosajcicdsji" 
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=30)  # 設定 Token 過期時間為 30 天
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
#app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blacklist.db'
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

#使用者(更新)
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)  # 確保為 NOT NULL


    def set_password(self, password):
        """使用安全哈希設置密碼"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """檢查密碼是否正確"""
        return check_password_hash(self.password_hash, password)

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
    #record = db.relationship("Record", back_populates="foods")

class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user = db.Column(db.String(80), nullable=False)        # 用戶名稱
    data = db.Column(db.String(200), nullable=False)       # 評論內容
    likes = db.Column(db.Integer, nullable=False, default=0)  # 點讚數
    replies = db.Column(db.Integer, nullable=False, default=0)  # 回覆數
    food_id = db.Column(db.Integer, db.ForeignKey('foods.id'), nullable=False)  # 外鍵，關聯到Food表
    parent_comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'), nullable=True)  # 回覆父評論ID (可為空)

    food = db.relationship('Food', backref=db.backref('comments', lazy=True))  # 關聯到Food表，取得該食物所有評論
    parent_comment = db.relationship('Comment', remote_side=[id])  # 回覆的父評論


#歷史訂單
class Record(db.Model):
    __tablename__ = 'record'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    info_id = db.Column(db.Integer, db.ForeignKey("foods.id"), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    #foods = db.relationship("Food", back_populates="record")
    food = db.relationship('Food')

# 檢查 token 是否在黑名單中
@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_header, jwt_payload):
    jti = jwt_payload['jti']
    token = TokenBlacklist.query.filter_by(jti=jti).first()
    return token is not None


@app.errorhandler(Exception)
def handle_exception(e):
    # pass through HTTP errors
    if isinstance(e, HTTPException):
        return e

    # now you're handling non-HTTP exceptions only
    result = jsonify({"error": str(e)})
    result.status_code = 500
     # 印出完整的錯誤追蹤到終端
    print("=== Error Traceback ===")
    traceback.print_exc()
    return result

@app.errorhandler(401)
def handle_unauthorized(e):
    # pass through HTTP errors
    if isinstance(e, HTTPException):
        return e
    
    error_trace = traceback.format_exc() 
    result = jsonify({"error": str(e), "traceback": error_trace})
    result.status_code = 401

     # 印出完整的錯誤追蹤到終端
    print("=== Error Traceback ===")
    print(error_trace)
    return result

@app.teardown_request
def teardown_request(exception):
    if exception:
        db.session.rollback()
    db.session.remove()

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

    if not username or not email or not password:
        return jsonify({'message': '所有欄位都是必需的'}), 400

    # 檢查用戶名或郵箱是否已存在
    if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
        return jsonify({'message': '用戶名或郵箱已被使用'}), 400

    # 創建新用戶
    new_user = User(username=username, email=email)
    new_user.set_password(password)

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': '註冊成功'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': '註冊失敗', 'error': str(e)}), 500


#登入
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()  # 使用 request.get_json() 獲取 JSON 資料
    username = data.get('username')  # 直接從 data 取得 username
    password = data.get('password')  # 直接從 data 取得 password

    if not username or not password:
        return jsonify({'message': '用戶名和密碼都是必需的'}), 400

    # 查找用戶
    user = User.query.filter((User.username == username) | (User.email == username)).first()
    if not user or not user.check_password(password):
        return jsonify({'message': '用戶名或密碼錯誤'}), 401
    
    # 生成 JWT Token
    token = create_access_token(identity=user.id)
    return jsonify({
        'message': '登入成功',
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email
        },
        'token': token
    }), 200

    


#用戶資料
@app.route('/user', methods=['GET'])
@jwt_required()  # 確保用戶必須提供有效的 Token
def get_user():
    # 獲取當前用戶的 id
    current_user_id = get_jwt_identity()

    # 根據用戶 id 查詢用戶資料
    user = User.query.filter_by(id=current_user_id).first()

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

# #結帳
# @app.route('/checkout', methods=['GET', 'POST'])
# def checkout():
#     # 處理 checkout 的邏輯
#     return jsonify({"message": "Checkout Page"})


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
    
# 查詢每家餐廳的平均評分並排序
@app.route('/api/top-restaurants', methods=['GET'])
def get_top_restaurants():
   
    top_restaurants = db.session.query(
        Subcat.id,
        Subcat.name,
        Subcat.address,
        func.avg(Food.score).label('avg_score')
    ).join(Food, Subcat.id == Food.subcat_id)  # 連接餐廳與菜品
    
    # 此處不需要反斜線，直接將每個方法放在單獨一行
    top_restaurants = top_restaurants.group_by(Subcat.id) \
                                     .order_by(func.avg(Food.score).desc()) \
                                     .limit(5).all()

    # 組織回傳資料
    restaurants = []
    for restaurant in top_restaurants:
        # 查詢餐廳的菜品
        foods = db.session.query(Food.name, Food.score).filter(Food.subcat_id == restaurant.id).all()
        restaurant_data = {
            'name': restaurant.name,
            'address': restaurant.address,
            'avg_score': round(restaurant.avg_score, 2),
            'foods': [{'name': food.name, 'score': food.score} for food in foods]
        }
        restaurants.append(restaurant_data)

    return jsonify(restaurants)  # 返回 JSON 格式的資料


@app.route('/checkout', methods=['POST'])
@jwt_required()  # 用戶可選擇是否提供 JWT
def checkout():
    # 獲取請求的 JSON 數據
    data = request.json
    cart = data.get('cart')  # 購物車中的商品

    if not cart:
        return jsonify({"error": "購物車為空，無法結帳"}), 400

    # 獲取當前用戶身份（若為訪客則返回 None）
    current_user = get_jwt_identity()
    user = User.query.filter_by(id=current_user).first()
    if user:
        # 登入用戶，保存每個商品的訂單到資料庫
        for item in cart:
            info_id = item.get('info_id')  # 商品對應的 ID
            if not info_id:
                return jsonify({"error": "缺少商品 ID"}), 400

            # 創建訂單記錄
            record = Record(
                user_id=user.id,
                info_id=info_id,
                timestamp=datetime.now(timezone.utc)
            )
            db.session.add(record)

        # 提交到資料庫
        db.session.commit()
        return jsonify({"message": "結帳成功，訂單已儲存至歷史記錄"}), 200

    # 若未登入，僅返回成功訊息，不儲存至歷史記錄
    return jsonify({"message": "結帳成功（訪客身份，未儲存訂單）"}), 200


@app.route('/history', methods=['GET'])
@jwt_required()  # 用戶必須登入
def get_history():
    # 獲取當前用戶身份
    current_user = get_jwt_identity()
    user = User.query.filter_by(id=current_user).first()
    if not user:
        return jsonify({"error": "用戶不存在"}), 403

    # 獲取當天的日期範圍
    now = datetime.now(timezone.utc)
    start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_day = now.replace(hour=23, minute=59, second=59, microsecond=999999)

    # 查詢當天的訂單
    records = Record.query.filter(
        Record.user_id == user.id,
        Record.timestamp >= start_of_day,
        Record.timestamp <= end_of_day
    ).all()

    # 如果今天沒有訂單
    if not records:
        return jsonify({"message": "今天無紀錄"}), 404

    # 計算總營養成分並準備卡片數據
    total_carbo = total_protein = total_fat = total_calories = 0
    history = []

    for record in records:
        food = Food.query.get(record.info_id)
        if food:
            total_carbo += food.carbo
            total_protein += food.protein
            total_fat += food.fat
            total_calories += food.calories

            history.append({
                "timestamp": record.timestamp.isoformat(),
                "food_name": food.name,
                "restaurant_name": food.subcat.name,
                "price": food.price,
                "carbo": food.carbo,
                "protein": food.protein,
                "fat": food.fat,
                "calories": food.calories,
                "image_url": food.image_url or "http://localhost:5000/static/assets/CHICKEN.jpg",  # 處理圖片 URL
            })

    return jsonify({
        "history": history,
        "totals": {
            "carbo": total_carbo,
            "protein": total_protein,
            "fat": total_fat,
            "calories": total_calories,
        }
    }), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # 自動創建資料表
    app.run(debug=True)  # 確保這行存在