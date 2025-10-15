# File: app.py (phiên bản API)

from flask import Flask, request, jsonify
from flask_cors import CORS # Cần cài thêm thư viện này
import joblib
import numpy as np
import os

app = Flask(__name__)
CORS(app) # Cho phép Next.js gọi đến API này

# Tải model và scaler
model_path = os.path.join('model', 'model.pkl')
scaler_path = os.path.join('model', 'scaler.pkl')
model = joblib.load(model_path)
scaler = joblib.load(scaler_path)

# Thứ tự các feature
feature_order = [
    'male', 'age', 'education', 'currentSmoker', 'cigsPerDay', 'BPMeds',
    'prevalentStroke', 'prevalentHyp', 'diabetes', 'totChol', 'sysBP',
    'diaBP', 'BMI', 'heartRate', 'glucose'
]

@app.route('/api/predict', methods=['POST']) # Đổi đường dẫn thành /api/predict
def predict():
    try:
        data = request.get_json(force=True)
        
        # Lấy dữ liệu theo đúng thứ tự
        input_data = [float(data.get(feature, 0)) for feature in feature_order]
        input_array = np.array([input_data])
        
        # Chuẩn hóa và dự đoán
        input_scaled = scaler.transform(input_array)
        prediction = model.predict(input_scaled)
        probability = model.predict_proba(input_scaled)
        
        # Trả về kết quả dưới dạng JSON
        return jsonify({
            'prediction': int(prediction[0]),
            'probability': f"{probability[0][1]*100:.2f}%"
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    # Chạy API trên một cổng khác, ví dụ 5001, để tránh xung đột với Next.js
    app.run(debug=True, port=5001)