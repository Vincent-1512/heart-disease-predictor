# File: tests/test_inference.py

import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import các hàm từ app.py vì logic dự đoán đã có sẵn ở đó
from app import scaler, model, feature_order

def test_prediction_with_sample_data():
    """
    Kiểm tra trực tiếp logic dự đoán với dữ liệu mẫu đầy đủ.
    Đây là cách test đáng tin cậy hơn.
    """
    # Dữ liệu mẫu hợp lệ, đầy đủ 15 thuộc tính
    sample_data = {
        'male': 1.0, 'age': 60.0, 'education': 2.0, 'currentSmoker': 1.0,
        'cigsPerDay': 20.0, 'BPMeds': 0.0, 'prevalentStroke': 0.0,
        'prevalentHyp': 1.0, 'diabetes': 0.0, 'totChol': 250.0,
        'sysBP': 140.0, 'diaBP': 90.0, 'BMI': 28.5,
        'heartRate': 75.0, 'glucose': 110.0
    }

    # Chắc chắn rằng dữ liệu đầu vào có đủ 15 thuộc tính
    assert len(sample_data) == len(feature_order)

    # Chuyển đổi dữ liệu thành một list theo đúng thứ tự
    input_data = [sample_data[feature] for feature in feature_order]
    
    # Chuẩn hóa và dự đoán
    input_scaled = scaler.transform([input_data])
    prediction = model.predict(input_scaled)

    # Kết quả phải là 0 hoặc 1
    assert prediction[0] in [0, 1]