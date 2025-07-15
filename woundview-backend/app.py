from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
import torch
from torchvision import transforms
import openai
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 환경 변수 또는 config 파일에서 실제로 관리하는 것이 좋음
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/woundview'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# ------------------- DB Models -------------------
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
## class User(테이블명 users) : 사용자 정보 DB에 저장. id/username/email/created_at(가입날짜,시간)이 담겨있음

class WoundRecord(db.Model):
    __tablename__ = 'wound_records'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  # user_id를 nullable로 변경
    image_path = db.Column(db.String(256))
    prediction = db.Column(db.String(128))
    advice = db.Column(db.Text)
    caution = db.Column(db.Text) 
    user = db.relationship('User', backref=db.backref('wound_records', lazy=True))
    width = db.Column(db.Float)
    height = db.Column(db.Float)
    area = db.Column(db.Float)
    risk_level = db.Column(db.String(16))
    cause = db.Column(db.String(256))
    body_part = db.Column(db.String(256))
    date = db.Column(db.DateTime, default=datetime.now(datetime.timezone.utc))
## class WoundRecord(테이블명 wound_records) : 상처 정보 DB에 저장. id/user_id/image_path/date/prediction/advice/user/width/height/area/risk_level/caution이 담겨있음



# ------------------- ML/LLM Functions -------------------
def predict_image(image_file):

    import os
    import numpy as np
    from sklearn.utils.class_weight import compute_class_weight
    import torch
    import torch.nn as nn
    from torchvision import datasets, transforms
    from torch.utils.data import DataLoader
    import timm  # EfficientNet용
    from tqdm import tqdm
    import matplotlib.pyplot as plt
    from collections import defaultdict

    class_names = ['찰과상', '멍', '화상', '베인 상처', '열상', '정상', '수술상처', '궤양']
    
    # 모델 로딩
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = torch.load("wound_model3.pth", map_location=device)
    model = model.to(device)
    model.eval()

    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
    ])

    target_img = transform(image_file).unsqueeze(0)

    # 예측
    with torch.no_grad():
        output = model(target_img)
        predict_result = torch.argmax(output).item()

    return {'prediction': class_names[predict_result]}


from wound_prompt import generate_advice_openai


def estimate_wound_size(image_file):
    """
    (더미 구현) 상처 가로, 세로, 면적을 mm 단위 임의 값으로 반환합니다.
    실제 YOLO 모델 적용 전까지 테스트용으로 사용하세요.
    """
    wound_width = 21.0    # mm 단위 예시값
    wound_height = 15.0   # mm 단위 예시값
    wound_area = 315.0    # mm^2 단위 임의값 (width*height 아님)
    return {
        'wound_width': wound_width,
        'wound_height': wound_height,
        'wound_area': wound_area
    }

    

# ------------------- API Endpoints -------------------


from werkzeug.utils import secure_filename
import os

@app.route('/upload', methods=['POST'])
def upload():
    """
    프론트엔드에서 전송된 이미지 파일을 서버에 저장하고,
    DB(wound_records)에 파일 정보만 저장합니다. user_id는 비워둡니다.
    실제 예측은 /predict-image에서 처리합니다.
    """
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    filename = secure_filename(file.filename)
    save_dir = 'uploads'
    os.makedirs(save_dir, exist_ok=True)
    save_path = os.path.join(save_dir, filename)
    file.save(save_path)

    new_record = WoundRecord(
        user_id=None,
        image_path=save_path
    )
    db.session.add(new_record)
    db.session.commit()

    return jsonify({
        'record_id': new_record.id,
        'filename': filename,
        'filepath': save_path
    }), 200



@app.route('/generate-advice', methods=['POST'])
def generate_advice_api():
    data = request.get_json()
    prediction = data.get('prediction', '')
    wound_width = data.get('wound_width', '')
    wound_height = data.get('wound_height', '')
    wound_area = data.get('wound_area', '')
    redness = data.get('redness', '')
    swelling = data.get('swelling', '')
    heat = data.get('heat', '')
    pain = data.get('pain', '')
    function_loss = data.get('function_loss', '')
    date = data.get('date', '')
    body_part = data.get('bodyPart', '')
    cause = data.get('cause', '')

    #선택입력사항부분
    history_data = data.get('history_data', '')
    current_season = data.get('current_season', '')
    current_climate = data.get('current_climate', '')


    advice = generate_advice_openai(
        prediction,
        wound_width,
        wound_height,
        wound_area,
        redness,
        swelling,
        heat,
        pain,
        function_loss,
        history_data,
        current_season,
        current_climate,
        date,
        body_part,
        cause
        )

    return jsonify({'advice': advice})

@app.route('/predict-image', methods=['POST'])
def predict_image_api():
    """
    record_id(int)을 JSON으로 받아 DB에서 이미지 경로를 찾아 분석합니다.
    """
    data = request.get_json()
    record_id = data.get('record_id')
    if not record_id:
        return jsonify({'error': 'No record_id provided'}), 400

    record = WoundRecord.query.get(record_id)
    if not record or not record.image_path:
        return jsonify({'error': 'No image found for this record_id'}), 404

    image_path = record.image_path
    with open(image_path, 'rb') as image_file:
        result = predict_image(image_file)
        wound_size = estimate_wound_size(image_file)

    return jsonify({
        'prediction': result['prediction'],
        'wound_width': wound_size['wound_width'],
        'wound_height': wound_size['wound_height'],
        'wound_area': wound_size['wound_area']
    })

@app.route('/record', methods=['POST'])
def record_api():
    data = request.get_json()
    user_id = data.get('user_id')
    image_path = data.get('image_path')
    prediction = data.get('prediction')
    advice = data.get('advice')
    wound_width = data.get('wound_width')
    wound_height = data.get('wound_height')
    wound_area = data.get('wound_area')
    risk_level = data.get('risk_level')
    caution = data.get('caution')
    cause = data.get('cause')
    body_part = data.get('body_part')
    date = data.get('date')
    wound_record = WoundRecord(
        user_id=user_id,
        image_path=image_path,
        prediction=prediction,
        advice=advice,
        width=wound_width,
        height=wound_height,
        area=wound_area,
        risk_level=risk_level,
        caution=caution,
        cause=cause,
        body_part=body_part,
        date=date
    )
    db.session.add(wound_record)
    db.session.commit()
    return jsonify({'message': 'Record saved', 'record_id': wound_record.id})

if __name__ == '__main__':
    app.run(debug=True)

with app.app_context():
    db.create_all()