# File: tests/test_app.py

import sys
import os
import pytest

# Thêm đường dẫn thư mục gốc để import được 'app'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app as flask_app

@pytest.fixture
def client():
    """Tạo một client giả để gửi request tới app."""
    with flask_app.test_client() as client:
        yield client

def test_home_page(client):
    """Kiểm tra xem trang chủ có tải được không (trả về status code 200)."""
    response = client.get('/')
    assert response.status_code == 200
    # SỬA Ở ĐÂY: Dùng chuỗi có dấu và mã hóa sang utf-8
    assert "Nhập Thông Tin Bệnh Nhân".encode('utf-8') in response.data

def test_prediction_logic(client):
    """Kiểm tra logic dự đoán với một bộ dữ liệu mẫu."""
    sample_data = {
        'male': '1', 'age': '60', 'education': '2.0', 'currentSmoker': '1',
        'cigsPerDay': '20.0', 'BPMeds': '0.0', 'prevalentStroke': '0',
        'prevalentHyp': '1', 'diabetes': '0', 'totChol': '250.0',
        'sysBP': '140.0', 'diaBP': '90.0', 'BMI': '28.5',
        'heartRate': '75.0', 'glucose': '110.0'
    }
    
    response = client.post('/predict', data=sample_data)
    assert response.status_code == 200
    # SỬA Ở ĐÂY: Dùng chuỗi có dấu và mã hóa sang utf-8
    assert "Kết Quả Dự Đoán".encode('utf-8') in response.data
    assert "Xác suất mắc bệnh".encode('utf-8') in response.data