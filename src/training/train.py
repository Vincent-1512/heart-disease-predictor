# File: src/training/train.py (Phiên bản cải tiến)

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from xgboost import XGBClassifier
from sklearn.ensemble import RandomForestClassifier
from lightgbm import LGBMClassifier # Thêm mô hình LightGBM
import joblib
import sys
import os
import argparse

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
# Thêm các hàm mới vào import
from src.training.preprocess import handle_missing_values, handle_outliers, create_features, apply_smote, scale_features

# --- 1. Định nghĩa các "công tắc" ---
parser = argparse.ArgumentParser(description="Huấn luyện mô hình dự đoán bệnh tim.")
parser.add_argument(
    '--model', type=str, default='lightgbm', 
    choices=['xgboost', 'random_forest', 'lightgbm'], # Thêm lightgbm
    help='Chọn mô hình để huấn luyện.'
)
parser.add_argument(
    '--output-name', type=str, default='model',
    help='Tên file cho model và scaler đầu ra.'
)
args = parser.parse_args()

# --- 2. Bắt đầu quy trình ---
print(f"Bắt đầu quy trình huấn luyện cho mô hình: {args.model.upper()}")
print("1. Đang tải dữ liệu...")
df = pd.read_csv('data/raw/framingham_heart_stud.csv')

print("2. Đang xử lý giá trị thiếu...")
df_clean = handle_missing_values(df)

print("3. Đang xử lý giá trị ngoại lai (outliers)...")
df_clean = handle_outliers(df_clean)

print("4. Đang tạo các đặc trưng mới (feature engineering)...")
df_featured = create_features(df_clean)

X = df_featured.drop('TenYearCHD', axis=1)
y = df_featured['TenYearCHD']

print("5. Đang chia dữ liệu train/test...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

print("6. Đang áp dụng SMOTE và chuẩn hóa...")
X_train_resampled, y_train_resampled = apply_smote(X_train, y_train)

# Quan trọng: Lưu lại thứ tự cột trước khi scale
feature_names = X_train_resampled.columns.tolist()
X_train_scaled, X_test_scaled, scaler = scale_features(X_train_resampled, X_test)

# --- 3. Lựa chọn và Huấn luyện ---
print(f"7. Đang huấn luyện mô hình {args.model.upper()}...")
model = None

if args.model == 'xgboost':
    model = XGBClassifier(use_label_encoder=False, eval_metric='logloss', random_state=42, scale_pos_weight=5) # scale_pos_weight giúp tập trung vào lớp "Có bệnh"
    
elif args.model == 'random_forest':
    model = RandomForestClassifier(random_state=42, n_estimators=200, class_weight='balanced')

elif args.model == 'lightgbm':
    model = LGBMClassifier(random_state=42, class_weight='balanced')

model.fit(X_train_scaled, y_train_resampled)

# --- 4. Đánh giá và Lưu ---
y_pred = model.predict(X_test_scaled)
print(f"\n--- BÁO CÁO HIỆU SUẤT MỚI ({args.model.upper()}) ---")
print(classification_report(y_test, y_pred, target_names=['Không bệnh', 'Có bệnh']))

model_output_path = f'model/{args.output_name}.pkl'
scaler_output_path = f'model/{args.output_name}_scaler.pkl'
joblib.dump(model, model_output_path)
joblib.dump(scaler, scaler_output_path)

# Lưu lại thứ tự và tên các feature
joblib.dump(feature_names, f'model/{args.output_name}_features.pkl')


print(f"\n✅ Hoàn tất! Mô hình đã được lưu tại '{model_output_path}'")