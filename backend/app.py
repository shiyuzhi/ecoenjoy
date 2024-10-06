
from flask import Flask, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import create_engine, select
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # 允許所有來源

# 資料庫設置
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost:3306/ecoenjoy_db'  # 替換為正確的資料庫 URI
app.config['SECRET_KEY'] = '51718' 
db = SQLAlchemy(app)
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])

# 主類別

# 創建數據表
with app.app_context():
    db.create_all()

# 根路由
@app.route('/')
def home():
    return "歡迎來到點餐系統！"



if __name__ == '__main__':
    app.run(debug=True)
