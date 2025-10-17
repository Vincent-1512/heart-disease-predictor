'use client';

import { useState, useEffect } from 'react';

// Định nghĩa một "khuôn mẫu" cho kết quả dự đoán
interface PredictionResult {
  prediction: number;
  probability: string;
  error?: string;
}

export default function HomePage() {
  const [result, setResult] = useState<PredictionResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  // "Camera" 1: Giám sát sự thay đổi của state 'result'
  useEffect(() => {
    console.log("Giá trị mới của state 'result':", result);
  }, [result]);

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setLoading(true);
    setResult(null);
    setError('');

    const formData = new FormData(event.currentTarget);
    const data = Object.fromEntries(formData.entries());

    console.log("Bước 1: Dữ liệu gửi đi từ form:", data); // Camera 2

    try {
      const response = await fetch('http://127.0.0.1:5001/api/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      });

      console.log("Bước 2: Trạng thái phản hồi từ server:", response.status, response.statusText); // Camera 3

      if (!response.ok) {
        throw new Error(`Lỗi mạng: ${response.statusText}`);
      }

      const predictionResult: PredictionResult = await response.json();
      
      console.log("Bước 3: Dữ liệu JSON nhận được từ backend:", predictionResult); // Camera 4

      setResult(predictionResult);
      
      console.log("Bước 4: Đã gọi setResult để cập nhật giao diện."); // Camera 5

    } catch (err) {
      if (err instanceof Error) {
        setError(`Không thể lấy kết quả: ${err.message}`);
      } else {
        setError("Đã xảy ra lỗi không xác định.");
      }
      console.error("LỖI:", err); // Camera 6
    } finally {
      setLoading(false);
    }
  }

  return (
    <main style={{ fontFamily: 'sans-serif', maxWidth: '600px', margin: 'auto', padding: '20px' }}>
      <h1>Dự Báo Bệnh Tim (Next.js & TypeScript)</h1>
      <form onSubmit={handleSubmit}>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '15px' }}>
            <div style={{ marginBottom: '10px' }}>
                <label>Tuổi:</label>
                <input type="number" name="age" required style={{ width: '100%', padding: '8px' }} defaultValue="50"/>
            </div>
            <div style={{ marginBottom: '10px' }}>
                <label>Giới tính (1: Nam, 0: Nữ):</label>
                <input type="number" name="male" min="0" max="1" required style={{ width: '100%', padding: '8px' }} defaultValue="1"/>
            </div>
            <div style={{ marginBottom: '10px' }}>
                <label>Học vấn (1-4):</label>
                <input type="number" name="education" style={{ width: '100%', padding: '8px' }} defaultValue="2"/>
            </div>
            <div style={{ marginBottom: '10px' }}>
                <label>Hút thuốc (1: Có, 0: Không):</label>
                <input type="number" name="currentSmoker" min="0" max="1" required style={{ width: '100%', padding: '8px' }} defaultValue="1"/>
            </div>
            <div style={{ marginBottom: '10px' }}>
                <label>Số điếu thuốc/ngày:</label>
                <input type="number" name="cigsPerDay" style={{ width: '100%', padding: '8px' }} defaultValue="20"/>
            </div>
            <div style={{ marginBottom: '10px' }}>
                <label>Dùng thuốc huyết áp (1: Có, 0: Không):</label>
                <input type="number" name="BPMeds" min="0" max="1" style={{ width: '100%', padding: '8px' }} defaultValue="0"/>
            </div>
            <div style={{ marginBottom: '10px' }}>
                <label>Tiền sử đột quỵ (1: Có, 0: Không):</label>
                <input type="number" name="prevalentStroke" min="0" max="1" required style={{ width: '100%', padding: '8px' }} defaultValue="0"/>
            </div>
            <div style={{ marginBottom: '10px' }}>
                <label>Tiền sử tăng huyết áp (1: Có, 0: Không):</label>
                <input type="number" name="prevalentHyp" min="0" max="1" required style={{ width: '100%', padding: '8px' }} defaultValue="1"/>
            </div>
            <div style={{ marginBottom: '10px' }}>
                <label>Tiểu đường (1: Có, 0: Không):</label>
                <input type="number" name="diabetes" min="0" max="1" required style={{ width: '100%', padding: '8px' }} defaultValue="0"/>
            </div>
            <div style={{ marginBottom: '10px' }}>
                <label>Cholesterol toàn phần:</label>
                <input type="number" step="any" name="totChol" style={{ width: '100%', padding: '8px' }} defaultValue="250"/>
            </div>
            <div style={{ marginBottom: '10px' }}>
                <label>Huyết áp tâm thu (sysBP):</label>
                <input type="number" step="any" name="sysBP" required style={{ width: '100%', padding: '8px' }} defaultValue="140"/>
            </div>
            <div style={{ marginBottom: '10px' }}>
                <label>Huyết áp tâm trương (diaBP):</label>
                <input type="number" step="any" name="diaBP" required style={{ width: '100%', padding: '8px' }} defaultValue="90"/>
            </div>
            <div style={{ marginBottom: '10px' }}>
                <label>Chỉ số BMI:</label>
                <input type="number" step="any" name="BMI" style={{ width: '100%', padding: '8px' }} defaultValue="28.5"/>
            </div>
            <div style={{ marginBottom: '10px' }}>
                <label>Nhịp tim:</label>
                <input type="number" name="heartRate" style={{ width: '100%', padding: '8px' }} defaultValue="75"/>
            </div>
            <div style={{ marginBottom: '10px' }}>
                <label>Nồng độ Glucose:</label>
                <input type="number" step="any" name="glucose" style={{ width: '100%', padding: '8px' }} defaultValue="110"/>
            </div>
        </div>
        <button type="submit" disabled={loading} style={{ width: '100%', padding: '10px', marginTop: '20px', background: 'green', color: 'white', border: 'none', cursor: 'pointer', fontSize: '16px' }}>
            {loading ? 'Đang dự đoán...' : 'Dự đoán'}
        </button>
    </form>

      {error && <p style={{ color: 'red', marginTop: '20px' }}>Lỗi: {error}</p>}

      {result && (
        <div style={{ marginTop: '20px' }}>
          <h2>Kết quả:</h2>
          <p>Dự đoán: <strong>{result.prediction === 1 ? 'Có nguy cơ mắc bệnh tim' : 'Không có nguy cơ'}</strong></p>
          <p>Xác suất mắc bệnh: <strong>{result.probability}</strong></p>
        </div>
      )}
    </main>
  );
}