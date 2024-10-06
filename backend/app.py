from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import select
from sqlalchemy import create_engine

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3306/cclo'  # 請根據您的配置調整
db = SQLAlchemy(app)
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])

class Maincat(db.Model):
    __tablename__ = 'maincat'  # 數據庫中的表名

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

def all_route(app):
    @app.route("/maincat", methods=['GET'])
    def get_all_maincat_json():
        # 使用 SQLAlchemy 的 select 函數
        statement = select(Maincat)
        # 連接並執行查詢
        with engine.connect() as connection:
            rows = connection.execute(statement).scalars().all()

        res = [{"id": cat.id, "name": cat.name} for cat in rows]
        return jsonify(res)  # 返回 JSON 格式的響應

all_route(app)

if __name__ == '__main__':
    app.run(debug=True)
