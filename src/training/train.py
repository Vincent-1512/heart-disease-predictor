# File: src/training/train.py (Phiên bản Sửa lỗi cuối cùng)
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from xgboost import XGBClassifier
from sklearn.ensemble import RandomForestClassifier
from lightgbm import LGBMClassifier
import joblib, sys, os, argparse

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.training.preprocess import handle_missing_values, encode_categorical_features, scale_features

# --- 1. "Công tắc" chọn mô hình ---
parser = argparse.ArgumentParser(description="Huấn luyện mô hình với bộ dữ liệu Heart Disease UCI.")
parser.add_argument('--model', type=str, default='lightgbm', choices=['xgboost', 'random_forest', 'lightgbm'], help='Chọn mô hình.')
parser.add_argument('--output-name', type=str, default='model_uci', help='Tên file đầu ra.')
args = parser.parse_args()

# --- 2. Quy trình Xử lý Dữ liệu ---
print(f"Bắt đầu huấn luyện mô hình: {args.model.upper()} với dữ liệu UCI")
print("1. Đang tải dữ liệu...")
# SỬA LỖI: Thêm na_values='?' để đọc đúng dữ liệu thiếu
df = pd.read_csv('data/raw/heart_disease_uci.csv', na_values='?')
df.columns = df.columns.str.strip()

print("2. Đang xử lý giá trị thiếu...")
df_clean = handle_missing_values(df)

print("3. Chuyển đổi cột 'target' thành bài toán nhị phân...")
df_clean['target'] = (df_clean['num'] > 0).astype(int)
df_clean = df_clean.drop(columns=['id', 'dataset', 'num'], errors='ignore')

# Tách features (X) và target (y)
X = df_clean.drop('target', axis=1)
y = df_clean['target']

print("4. 'Số hóa' các đặc trưng dạng chữ...")
X_encoded = encode_categorical_features(X)

print("5. Đang chia dữ liệu train/test...")
X_train, X_test, y_train, y_test = train_test_split(X_encoded, y, test_size=0.2, random_state=42)

print("6. Đang chuẩn hóa features...")
feature_names = X_train.columns.tolist()
X_train_scaled, X_test_scaled, scaler = scale_features(X_train, X_test)

# --- 3. Huấn luyện và Đánh giá ---
print(f"7. Đang huấn luyện mô hình {args.model.upper()}...")
model = None
if args.model == 'xgboost':
    model = XGBClassifier(use_label_encoder=False, eval_metric='logloss', random_state=42)
elif args.model == 'random_forest':
    model = RandomForestClassifier(random_state=42, n_estimators=100)
elif args.model == 'lightgbm':
    model = LGBMClassifier(random_state=42)

model.fit(X_train_scaled, y_train)

y_pred = model.predict(X_test_scaled)
print(f"\n--- BÁO CÁO HIỆU SUẤT VỚI DỮ LIỆU UCI ({args.model.upper()}) ---")
print(classification_report(y_test, y_pred, target_names=['Không bệnh', 'Có bệnh']))

# --- 4. Lưu kết quả ---
model_output_path = f'model/{args.output_name}.pkl'
scaler_output_path = f'model/{args.output_name}_scaler.pkl'
features_output_path = f'model/{args.output_name}_features.pkl'

joblib.dump(model, model_output_path)
joblib.dump(scaler, scaler_output_path)
joblib.dump(feature_names, features_output_path)
print(f"\n✅ Hoàn tất! Mô hình đã được lưu tại '{model_output_path}'")