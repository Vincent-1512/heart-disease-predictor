# File: app.py (Phiên bản API mới)

from flask import Flask, request, jsonify, make_response
from flask_cors import CORS # Thư viện để cho phép Next.js gọi đến
import joblib
import numpy as np
import os

app = Flask(__name__)

# Cấu hình CORS để chấp nhận request từ frontend (chạy ở port 3000)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

# Tải model và scaler
try:
    model_path = os.path.join('model', 'model.pkl')
    scaler_path = os.path.join('model', 'scaler.pkl')
    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
except FileNotFoundError:
    print("Lỗi: Không tìm thấy file model/model.pkl hoặc model/scaler.pkl.")
    model, scaler = None, None

# Định nghĩa thứ tự các feature
feature_order = [
    'male', 'age', 'education', 'currentSmoker', 'cigsPerDay', 'BPMeds',
    'prevalentStroke', 'prevalentHyp', 'diabetes', 'totChol', 'sysBP',
    'diaBP', 'BMI', 'heartRate', 'glucose'
]

@app.route('/api/predict', methods=['POST', 'OPTIONS'])
def predict():
    # 1. Xử lý yêu cầu "thăm dò" OPTIONS trước tiên
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "http://localhost:3000")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        response.headers.add("Access-Control-Allow-Methods", "POST")
        return response

    # 2. Từ đây trở đi, code chỉ xử lý cho yêu cầu POST
    
    # Kiểm tra model chỉ một lần là đủ
    if not model or not scaler:
        return jsonify({'error': 'Mô hình chưa được tải thành công, vui lòng kiểm tra server backend.'}), 500

    try:
        data = request.get_json(force=True)

        input_data = [float(data.get(feature, 0)) for feature in feature_order]
        input_array = np.array([input_data])

        input_scaled = scaler.transform(input_array)
        prediction = model.predict(input_scaled)
        probability = model.predict_proba(input_scaled)

        return jsonify({
            'prediction': int(prediction[0]),
            'probability': f"{probability[0][1]*100:.2f}%"
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True, port=5001)