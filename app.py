# File: app.py (Phiên bản Hoàn chỉnh, tương thích với mọi mô hình UCI)
from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import joblib
import numpy as np
import pandas as pd # Cần pandas để xử lý dữ liệu đầu vào
import os

app = Flask(__name__)
CORS(app)

# --- Tải mô hình và các file phụ trợ ---
# HÃY CHỌN MÔ HÌNH TỐT NHẤT BẠN ĐÃ HUẤN LUYỆN
MODEL_NAME = 'xgboost_uci_v1' # <-- THAY ĐỔI TÊN MÔ HÌNH BẠN MUỐN DÙNG Ở ĐÂY

try:
    print(f"Đang tải mô hình '{MODEL_NAME}'...")
    model = joblib.load(f'model/{MODEL_NAME}.pkl')
    scaler = joblib.load(f'model/{MODEL_NAME}_scaler.pkl')
    feature_order = joblib.load(f'model/{MODEL_NAME}_features.pkl')
    print("Tải mô hình thành công!")
except Exception as e:
    print(f"LỖI: Không thể tải model. Vui lòng kiểm tra lại tên file. Lỗi: {e}")
    model, scaler, feature_order = None, None, []

@app.route('/api/predict', methods=['POST'])
def predict():
    

    if not all([model, scaler, feature_order]):
        return jsonify({'error': 'Mô hình chưa được tải thành công trên server.'}), 500

    try:
        # Lấy dữ liệu JSON từ frontend
        data = request.get_json(force=True)
        
        # Chuyển dữ liệu đầu vào thành DataFrame của pandas
        input_df = pd.DataFrame([data])
        
        # 'Số hóa' các cột chữ nếu có
        categorical_cols = input_df.select_dtypes(include=['object']).columns
        if len(categorical_cols) > 0:
            input_df = pd.get_dummies(input_df, columns=categorical_cols, drop_first=True, dtype=int)

        # Sắp xếp lại các cột để khớp với thứ tự lúc huấn luyện
        # Đồng thời thêm các cột còn thiếu và điền giá trị 0
        final_df = input_df.reindex(columns=feature_order, fill_value=0)
        
        # Chuẩn hóa dữ liệu
        input_scaled = scaler.transform(final_df)
        
        # Dự đoán
        prediction = model.predict(input_scaled)
        probability = model.predict_proba(input_scaled)
        
        return jsonify({
            'prediction': int(prediction[0]),
            'probability': f"{probability[0][1]*100:.2f}%"
        })
    except Exception as e:
        return jsonify({'error': f'Lỗi xử lý: {str(e)}'}), 400

if __name__ == "__main__":
    app.run(debug=True, port=5001)