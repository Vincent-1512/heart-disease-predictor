# File: src/training/train.py (Phiên bản Tối ưu hóa Toàn diện)
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from xgboost import XGBClassifier
from sklearn.ensemble import RandomForestClassifier
from lightgbm import LGBMClassifier
import joblib, sys, os, argparse

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
# Import tất cả các "máy móc" từ xưởng sơ chế
from src.training.preprocess import (
    handle_missing_values, handle_missing_values_knn, 
    encode_categorical_features, create_advanced_features, 
    select_best_features, scale_features
)

# --- 1. Thêm các "công tắc" tối ưu hóa ---
parser = argparse.ArgumentParser(description="Huấn luyện mô hình với các tùy chọn tối ưu hóa.")
parser.add_argument('--model', type=str, default='lightgbm', choices=['xgboost', 'random_forest', 'lightgbm'], help='Chọn mô hình.')
parser.add_argument('--output-name', type=str, default='model_uci_optimized', help='Tên file đầu ra.')
parser.add_argument('--use-knn-imputer', action='store_true', help='Bật tính năng điền khuyết bằng KNNImputer.')
parser.add_argument('--use-feature-eng', action='store_true', help='Bật tính năng tạo đặc trưng nâng cao.')
parser.add_argument('--select-k-features', type=int, help='Chọn ra K đặc trưng tốt nhất (ví dụ: 10).')
args = parser.parse_args()

# --- 2. Quy trình Xử lý Dữ liệu ---
print(f"Bắt đầu huấn luyện mô hình: {args.model.upper()} với dữ liệu UCI")
print("1. Đang tải dữ liệu...")
df = pd.read_csv('data/raw/heart_disease_uci.csv')
df.columns = df.columns.str.strip()

print("2. Chuyển đổi cột 'target' thành bài toán nhị phân...")
df['target'] = (df['num'] > 0).astype(int)
df = df.drop(columns=['id', 'dataset', 'num'], errors='ignore')

# Tách features (X) và target (y)
X = df.drop('target', axis=1)
y = df['target']

# 'Số hóa' các đặc trưng dạng chữ TRƯỚC khi xử lý giá trị thiếu
X_encoded = encode_categorical_features(X)

print("3. Đang xử lý giá trị thiếu...")
if args.use_knn_imputer:
    print("   -> Sử dụng KNNImputer...")
    X_clean = handle_missing_values_knn(X_encoded)
else:
    print("   -> Sử dụng Median/Mode Imputer (mặc định)...")
    X_clean = handle_missing_values(X_encoded)

if args.use_feature_eng:
    print("4. Đang tạo các đặc trưng mới...")
    X_clean = create_advanced_features(X_clean)

print("5. Đang chia dữ liệu train/test...")
X_train, X_test, y_train, y_test = train_test_split(X_clean, y, test_size=0.2, random_state=42)

if args.select_k_features:
    print(f"6. Đang lựa chọn {args.select_k_features} đặc trưng tốt nhất...")
    X_train, X_test = select_best_features(X_train, y_train, X_test, k=args.select_k_features)

print("7. Đang chuẩn hóa features...")
feature_names = X_train.columns.tolist()
X_train_scaled, X_test_scaled, scaler = scale_features(X_train, X_test)

# --- 3. Huấn luyện và Đánh giá ---
print(f"8. Đang huấn luyện mô hình {args.model.upper()}...")
# ... (Phần code huấn luyện 3 mô hình giữ nguyên như cũ) ...
model = None
if args.model == 'xgboost':
    model = XGBClassifier(use_label_encoder=False, eval_metric='logloss', random_state=42)
elif args.model == 'random_forest':
    model = RandomForestClassifier(random_state=42, n_estimators=100)
elif args.model == 'lightgbm':
    model = LGBMClassifier(random_state=42)

model.fit(X_train_scaled, y_train)

y_pred = model.predict(X_test_scaled)
print(f"\n--- BÁO CÁO HIỆU SUẤT ({args.model.upper()}) ---")
print(classification_report(y_test, y_pred, target_names=['Không bệnh', 'Có bệnh']))

# --- 4. Lưu kết quả ---
# ... (Phần code lưu model giữ nguyên như cũ) ...
model_output_path = f'model/{args.output_name}.pkl'
scaler_output_path = f'model/{args.output_name}_scaler.pkl'
features_output_path = f'model/{args.output_name}_features.pkl'

joblib.dump(model, model_output_path)
joblib.dump(scaler, scaler_output_path)
joblib.dump(feature_names, features_output_path)
print(f"\n✅ Hoàn tất! Mô hình đã được lưu tại '{model_output_path}'")