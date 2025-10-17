# File: src/training/preprocess.py (Phiên bản nâng cấp)

import pandas as pd
from imblearn.over_sampling import SMOTE
from sklearn.preprocessing import StandardScaler
import numpy as np

def handle_missing_values(df):
    """Điền các giá trị bị thiếu bằng giá trị trung vị (median) để giảm ảnh hưởng của outliers."""
    df_processed = df.copy()
    for col in df_processed.columns:
        if df_processed[col].isnull().any():
            # Dùng median thay cho mean
            median_value = df_processed[col].median()
            df_processed[col].fillna(median_value, inplace=True)
    return df_processed

def handle_outliers(df):
    """Xử lý các giá trị ngoại lai bằng phương pháp IQR."""
    df_processed = df.copy()
    for col in df_processed.columns:
        if df_processed[col].dtype in ['int64', 'float64']:
            Q1 = df_processed[col].quantile(0.25)
            Q3 = df_processed[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            # Giới hạn các giá trị ngoại lai thay vì xóa bỏ
            df_processed[col] = np.clip(df_processed[col], lower_bound, upper_bound)
            
    return df_processed

def create_features(df):
    """Tạo ra các đặc trưng mới (Feature Engineering)."""
    df_featured = df.copy()
    
    # 1. Pulse Pressure (Huyết áp mạch): Hiệu số giữa huyết áp tâm thu và tâm trương
    df_featured['pulsePressure'] = df_featured['sysBP'] - df_featured['diaBP']
    
    # 2. Phân loại huyết áp
    conditions = [
        (df_featured['sysBP'] < 120) & (df_featured['diaBP'] < 80),
        (df_featured['sysBP'] >= 140) | (df_featured['diaBP'] >= 90),
        (df_featured['sysBP'] >= 130) | (df_featured['diaBP'] >= 80)
    ]
    choices = [0, 2, 1] # 0: Normal, 1: Elevated, 2: Hypertension
    df_featured['bpCategory'] = np.select(conditions, choices, default=0)
    
    return df_featured

# --- Các hàm cũ vẫn giữ nguyên ---
def apply_smote(X, y):
    smote = SMOTE(random_state=42)
    X_resampled, y_resampled = smote.fit_resample(X, y)
    return X_resampled, y_resampled

def scale_features(X_train, X_test):
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    return X_train_scaled, X_test_scaled, scaler