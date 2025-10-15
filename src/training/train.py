# File: src/training/train.py

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import xgboost as xgb
import joblib
import sys
import os

# Thêm đường dẫn thư mục gốc vào hệ thống để import các module từ src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.training.preprocess import handle_missing_values, apply_smote, scale_features

# --- 1. Tải Dữ liệu ---
print("Bắt đầu quy trình huấn luyện...")
print("1/7: Đang tải dữ liệu...")
df = pd.read_csv('data/raw/framingham_heart_study.csv')

# --- 2. Xử lý Giá trị thiếu ---
print("2/7: Đang xử lý giá trị thiếu...")
df_processed = handle_missing_values(df)

# --- 3. Tách Features (X) và Target (y) ---
print("3/7: Đang tách features và target...")
X = df_processed.drop('TenYearCHD', axis=1)
y = df_processed['TenYearCHD']

# --- 4. Chia Dữ liệu Train/Test ---
print("4/7: Đang chia dữ liệu thành tập train và test...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# --- 5. Cân bằng và Chuẩn hóa Dữ liệu (chỉ trên tập train) ---
print("5/7: Đang áp dụng SMOTE để cân bằng tập train...")
X_train_resampled, y_train_resampled = apply_smote(X_train, y_train)

print("6/7: Đang chuẩn hóa features...")
X_train_scaled, X_test_scaled, scaler = scale_features(X_train_resampled, X_test)


# --- 6. Huấn luyện Mô hình XGBoost ---
print("7/7: Đang huấn luyện mô hình XGBoost...")
model = xgb.XGBClassifier(learning_rate=0.4, use_label_encoder=False, eval_metric='logloss', random_state=42)
model.fit(X_train_scaled, y_train_resampled)

# Đánh giá mô hình trên tập test đã được scale
y_pred = model.predict(X_test_scaled)
print("\n--- Báo cáo Phân loại trên Tập Test ---")
print(classification_report(y_test, y_pred))

# --- 7. Lưu Mô hình và Scaler ---
print("Đang lưu mô hình và scaler...")
joblib.dump(model, 'model/model.pkl')
joblib.dump(scaler, 'model/scaler.pkl') # Rất quan trọng: phải lưu cả scaler

print("\n✅ Hoàn tất! Mô hình đã được lưu tại 'model/model.pkl' và scaler tại 'model/scaler.pkl'.")
