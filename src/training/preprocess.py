# File: src/training/preprocess.py

import pandas as pd
from imblearn.over_sampling import SMOTE
from sklearn.preprocessing import StandardScaler

def handle_missing_values(df):
    """Điền các giá trị bị thiếu bằng giá trị trung bình (mean) của cột."""
    
    # Tạo một bản sao của DataFrame để tránh thay đổi dữ liệu gốc.
    # Đây là một thói quen tốt để đảm bảo an toàn dữ liệu.
    df_processed = df.copy()
    
    # Bắt đầu một vòng lặp để duyệt qua tên của từng cột trong DataFrame.
    for col in df_processed.columns:
        
        # Kiểm tra xem trong cột hiện tại có tồn tại bất kỳ giá trị nào bị thiếu (null) hay không.
        if df_processed[col].isnull().any():
            
            # Nếu có giá trị thiếu, thực hiện các bước sau:
            # 1. Tính giá trị trung bình của tất cả các giá trị hiện có trong cột đó.
            mean_value = df_processed[col].mean()
            
            # 2. Lấp đầy tất cả các ô bị thiếu trong cột bằng giá trị trung bình vừa tính được.
            # `inplace=True` có nghĩa là áp dụng thay đổi trực tiếp lên df_processed.
            df_processed[col].fillna(mean_value, inplace=True)
            
    # Trả về DataFrame đã được xử lý xong, không còn giá trị thiếu.
    return df_processed

#--------------------------------------------------------------------------

def apply_smote(X, y):
    """Cân bằng dữ liệu trên tập huấn luyện bằng kỹ thuật SMOTE."""
    
    # Khởi tạo một đối tượng SMOTE. SMOTE sẽ tạo ra các mẫu dữ liệu "giả lập"
    # cho lớp thiểu số để số lượng mẫu của các lớp trở nên cân bằng.
    # `random_state=42` để đảm bảo kết quả luôn giống nhau mỗi khi chạy code.
    smote = SMOTE(random_state=42)
    
    # Áp dụng SMOTE lên dữ liệu. Phương thức này sẽ "học" và "lấy mẫu lại"
    # để tạo ra một bộ dữ liệu mới đã được cân bằng.
    X_resampled, y_resampled = smote.fit_resample(X, y)
    
    # Trả về các đặc trưng (X) và nhãn (y) của bộ dữ liệu mới đã cân bằng.
    return X_resampled, y_resampled

#--------------------------------------------------------------------------

def scale_features(X_train, X_test):
    """Chuẩn hóa dữ liệu (scaling) để các feature có cùng thang đo."""
    
    # Khởi tạo một đối tượng StandardScaler. Công cụ này sẽ biến đổi dữ liệu
    # để mỗi cột có giá trị trung bình là 0 và độ lệch chuẩn là 1.
    scaler = StandardScaler()
    
    # Bước 1: Áp dụng lên tập huấn luyện (X_train).
    # `fit_transform` thực hiện 2 việc:
    #   - `fit`: "Học" các tham số chuẩn hóa (là giá trị trung bình và độ lệch chuẩn) từ X_train.
    #   - `transform`: Áp dụng các tham số vừa học để biến đổi X_train.
    X_train_scaled = scaler.fit_transform(X_train)
    
    # Bước 2: Áp dụng lên tập kiểm tra (X_test).
    # Chỉ dùng `transform`, KHÔNG dùng `fit`.
    # Lý do: Ta phải sử dụng các tham số đã học từ tập huấn luyện để áp dụng cho tập kiểm tra.
    # Điều này giả lập rằng tập kiểm tra là dữ liệu mới mà mô hình chưa từng thấy.
    X_test_scaled = scaler.transform(X_test)
    
    # Trả về dữ liệu đã được chuẩn hóa và đối tượng scaler đã được "huấn luyện".
    # Giữ lại scaler rất hữu ích để chuẩn hóa dữ liệu mới trong tương lai.
    return X_train_scaled, X_test_scaled, scaler