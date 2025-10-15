'use client';

import { useState } from 'react';

// Bước 1: Tạo một "khuôn mẫu" cho kết quả dự đoán
interface PredictionResult {
  prediction: number;
  probability: string;
  error?: string; // Thêm thuộc tính error (tùy chọn)
}

export default function HomePage() {
  // Bước 2: Khai báo state "result" có thể là kiểu PredictionResult hoặc là null
  const [result, setResult] = useState<PredictionResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  // Bước 3: Khai báo kiểu dữ liệu cho "event"
  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setLoading(true);
    setResult(null);
    setError('');

    const formData = new FormData(event.currentTarget);
    const data = Object.fromEntries(formData.entries());

    try {
      const response = await fetch('http://127.0.0.1:5001/api/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        throw new Error(`Lỗi mạng: ${response.statusText}`);
      }

      const predictionResult: PredictionResult = await response.json();
      if (predictionResult.error) {
        throw new Error(predictionResult.error);
      }
      setResult(predictionResult);

    } catch (err) {
        if (err instanceof Error) {
            setError(`Không thể lấy kết quả: ${err.message}`);
        } else {
            setError("Đã xảy ra lỗi không xác định.");
        }
    } finally {
      setLoading(false);
    }
  }

  return (
    <main style={{ fontFamily: 'sans-serif', maxWidth: '600px', margin: 'auto', padding: '20px' }}>
      <h1>Dự Báo Bệnh Tim (Next.js & TypeScript)</h1>
      <form onSubmit={handleSubmit}>
        {/* THÊM ĐẦY ĐỦ CÁC Ô INPUT CỦA BẠN VÀO ĐÂY */}
        <div style={{ marginBottom: '10px' }}>
          <label>Tuổi: </label>
          <input type="number" name="age" required style={{ width: '100%', padding: '8px' }} />
        </div>
        <div style={{ marginBottom: '10px' }}>
          <label>Giới tính (1: Nam, 0: Nữ): </label>
          <input type="number" name="male" required style={{ width: '100%', padding: '8px' }} />
        </div>
        {/* ... THÊM 13 TRƯỜNG CÒN LẠI VÀO ĐÂY ... */}
        <button type="submit" disabled={loading} style={{ width: '100%', padding: '10px', background: 'green', color: 'white', border: 'none', cursor: 'pointer' }}>
          {loading ? 'Đang dự đoán...' : 'Dự đoán'}
        </button>
      </form>

      {error && <p style={{ color: 'red', marginTop: '20px' }}>Lỗi: {error}</p>}

      {/* Code ở đây không còn lỗi nữa vì TypeScript đã hiểu "result" */}
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