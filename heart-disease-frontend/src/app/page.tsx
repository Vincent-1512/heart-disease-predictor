// File: app/page.js (ví dụ cho Next.js App Router)
'use client';

import { useState } from 'react';

export default function HomePage() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  async function handleSubmit(event) {
    event.preventDefault();
    setLoading(true);
    setResult(null);

    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData.entries());

    try {
      // Gọi đến API Flask đang chạy trên cổng 5001
      const response = await fetch('http://127.0.0.1:5001/api/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });

      const predictionResult = await response.json();
      setResult(predictionResult);
    } catch (error) {
      console.error("Error fetching prediction:", error);
      setResult({ error: "Không thể kết nối đến server dự đoán." });
    } finally {
      setLoading(false);
    }
  }

  return (
    <div>
      <h1>Dự Báo Bệnh Tim (Next.js)</h1>
      <form onSubmit={handleSubmit}>
        {/* Thêm các ô input của bạn ở đây. Ví dụ: */}
        <div>
          <label>Tuổi:</label>
          <input type="number" name="age" required />
        </div>
        <div>
          <label>Giới tính (1: Nam, 0: Nữ):</label>
          <input type="number" name="male" required />
        </div>
        {/* ...Thêm 13 trường còn lại... */}
        <button type="submit" disabled={loading}>
          {loading ? 'Đang dự đoán...' : 'Dự đoán'}
        </button>
      </form>

      {result && (
        <div>
          <h2>Kết quả:</h2>
          {result.error ? (
            <p style={{ color: 'red' }}>{result.error}</p>
          ) : (
            <>
              <p>Dự đoán: {result.prediction === 1 ? 'Có nguy cơ' : 'Không có nguy cơ'}</p>
              <p>Xác suất mắc bệnh: {result.probability}</p>
            </>
          )}
        </div>
      )}
    </div>
  );
}