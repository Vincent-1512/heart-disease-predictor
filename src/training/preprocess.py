# File: src/training/preprocess.py (Phiên bản Tối ưu hóa)
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.impute import KNNImputer # Máy điền khuyết cao cấp
from sklearn.feature_selection import SelectKBest, f_classif # Máy lựa chọn tinh hoa

def handle_missing_values_knn(df):
    """Điền các giá trị bị thiếu bằng KNNImputer."""
    imputer = KNNImputer(n_neighbors=5)
    # Tạm thời chuyển đổi cột chữ thành số để imputer hoạt động
    df_numeric = pd.get_dummies(df, drop_first=True)
    df_imputed = pd.DataFrame(imputer.fit_transform(df_numeric), columns=df_numeric.columns)
    return df_imputed

def create_advanced_features(df):
    """Tạo ra các đặc trưng mới, thông minh hơn."""
    df_featured = df.copy()
    
    # Tỷ lệ Cholesterol / Tuổi
    # Giả định rằng cholesterol cao ở người trẻ nguy hiểm hơn
    df_featured['chol_age_ratio'] = df_featured['chol'] / (df_featured['age'] + 1)
    
    # Tỷ lệ Nhịp tim tối đa / Tuổi
    df_featured['thalach_age_ratio'] = df_featured['thalach'] / (df_featured['age'] + 1)

    # Kết hợp huyết áp và cholesterol
    df_featured['bp_chol_interaction'] = (df_featured['trestbps'] / 130) * (df_featured['chol'] / 200)

    return df_featured

def select_best_features(X_train, y_train, X_test, k='all'):
    """Lựa chọn K đặc trưng tốt nhất."""
    fs = SelectKBest(score_func=f_classif, k=k)
    fs.fit(X_train, y_train)
    
    X_train_fs = fs.transform(X_train)
    X_test_fs = fs.transform(X_test)
    
    # Lấy ra tên các cột đã được chọn
    selected_features = X_train.columns[fs.get_support()]
    print(f"Các đặc trưng được chọn: {list(selected_features)}")
    
    # Trả về dạng DataFrame để giữ lại tên cột
    return (
        pd.DataFrame(X_train_fs, columns=selected_features),
        pd.DataFrame(X_test_fs, columns=selected_features)
    )

# --- Các hàm cũ vẫn giữ lại để dùng khi cần ---
def encode_categorical_features(df):
    df_processed = df.copy()
    categorical_cols = df_processed.select_dtypes(include=['object']).columns
    if len(categorical_cols) > 0:
        df_processed = pd.get_dummies(df_processed, columns=categorical_cols, drop_first=True, dtype=int)
    return df_processed

def handle_missing_values(df):
    df_processed = df.copy()
    for col in df_processed.columns:
        if df_processed[col].isnull().any():
            if pd.api.types.is_numeric_dtype(df_processed[col]):
                df_processed[col] = df_processed[col].fillna(df_processed[col].median())
            else:
                df_processed[col] = df_processed[col].fillna(df_processed[col].mode()[0])
    return df_processed

def scale_features(X_train, X_test):
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    return X_train_scaled, X_test_scaled, scaler