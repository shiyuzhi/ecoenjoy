from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # 允許所有來源的請求

# 資料庫設置
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost:3306/ecoenjoy_db'  # 替換為正確的資料庫 URI
app.config['SECRET_KEY'] = '51718'
db = SQLAlchemy(app)

# 定義資料表模型
class MainCategory(db.Model):
    __tablename__ = 'maincat'  # 設置資料表名稱為 maincat
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

# 創建資料表
with app.app_context():
    db.create_all()

# 根路由
@app.route('/')
def home():
    return "歡迎來到點餐系統！"

# 獲取主類別 API
@app.route('/maincat', methods=['GET'])
def get_main_categories():
    try:
        maincats = MainCategory.query.all()
        return jsonify([{'id': maincat.id, 'name': maincat.name} for maincat in maincats])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
