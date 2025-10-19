'use client';
import { useState } from 'react';
// Import font chữ từ Google Fonts (ví dụ: Nunito)
import { Nunito } from 'next/font/google';

// Cấu hình font chữ
const nunito = Nunito({ subsets: ['latin'] });

// Giữ nguyên interface
interface PredictionResult {
  prediction: number;
  probability: string;
  error?: string;
}

export default function HomePage() {
  const [result, setResult] = useState<PredictionResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  // Giữ nguyên hàm handleSubmit
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
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      });

      const predictionResult: PredictionResult = await response.json();
      if (predictionResult.error || !response.ok) {
        throw new Error(predictionResult.error || "Có lỗi xảy ra");
      }
      setResult(predictionResult);

    } catch (err) {
      setError(err instanceof Error ? err.message : "Lỗi không xác định.");
    } finally {
      setLoading(false);
    }
  }

  // --- THAY ĐỔI GIAO DIỆN BẮT ĐẦU TỪ ĐÂY ---
  return (
    // Sử dụng font Nunito, nền màu kem (be), căn giữa
    <main className={`${nunito.className} min-h-screen bg-beige-50 flex items-center justify-center p-4 sm:p-6 lg:p-8`}>
      {/* Khung thẻ (Card) với bo góc lớn hơn, đổ bóng tinh tế, tăng padding */}
      <div className="w-full max-w-4xl bg-white rounded-xl shadow-lg p-8 sm:p-10 md:p-12">

        {/* Tiêu đề với màu sắc ấm hơn, font lớn hơn */}
        <h1 className="text-3xl sm:text-4xl font-bold text-center text-amber-800 mb-10">
          Chẩn đoán Nguy cơ Bệnh Tim
        </h1>

        {/* Form và các thành phần bên trong giữ nguyên style cũ ở bước này */}
        <form onSubmit={handleSubmit}>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-x-6 gap-y-4"> {/* Giảm khoảng cách dọc */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Tuổi (age)</label>
              <input type="number" name="age" required defaultValue="54" className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500"/> {/* Đổi màu focus */}
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Giới tính (sex: 1=Nam)</label>
              <input type="number" name="sex" required defaultValue="1" className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500"/>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Loại đau ngực (cp: 0-3)</label>
              <input type="number" name="cp" required defaultValue="0" className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500"/>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Huyết áp nghỉ (trestbps)</label>
              <input type="number" name="trestbps" required defaultValue="120" className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500"/>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Cholesterol (chol)</label>
              <input type="number" name="chol" required defaultValue="250" className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500"/>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Đường huyết 120 (fbs: 1=Có)</label>
              <input type="number" name="fbs" required defaultValue="0" className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500"/>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Điện tâm đồ nghỉ (restecg: 0-2)</label>
              <input type="number" name="restecg" required defaultValue="0" className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500"/>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Nhịp tim tối đa (thalach)</label>
              <input type="number" name="thalach" required defaultValue="150" className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500"/>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Đau ngực do gắng sức (exang: 1=Có)</label>
              <input type="number" name="exang" required defaultValue="0" className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500"/>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Oldpeak</label>
              <input type="number" step="any" name="oldpeak" required defaultValue="1.0" className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500"/>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Độ dốc ST (slope)</label>
              <input type="number" name="slope" required defaultValue="1" className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500"/>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Số mạch chính (ca: 0-4)</label>
              <input type="number" name="ca" required defaultValue="0" className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500"/>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Thal (0-3)</label>
              <input type="number" name="thal" required defaultValue="2" className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500"/>
            </div>
          </div>

          {/* Nút bấm giữ nguyên style cũ ở bước này */}
          <button type="submit" disabled={loading} className="mt-10 w-full flex justify-center py-3 px-4 border border-transparent rounded-md shadow-sm text-lg font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:bg-gray-400"> {/* Tăng margin top */}
            {loading ? 'Đang xử lý...' : 'Dự đoán'}
          </button>
        </form>

        {/* Phần kết quả giữ nguyên style cũ ở bước này */}
        {error && <p className="mt-6 text-center text-red-600">Lỗi: {error}</p>}

        {result && (
          <div className="mt-8 p-6 bg-gray-100 border border-gray-200 rounded-lg text-center">
            <h2 className="text-2xl font-semibold text-gray-800 mb-4">Kết quả Chẩn đoán</h2>
            <p className={`text-xl font-bold ${result.prediction === 1 ? 'text-red-600' : 'text-green-600'}`}>
              {result.prediction === 1 ? 'Có nguy cơ mắc bệnh tim' : 'Không có nguy cơ'}
            </p>
            <p className="text-md text-gray-600 mt-2">
              Xác suất mắc bệnh ước tính: <span className="font-bold text-gray-800">{result.probability}</span>
            </p>
          </div>
        )}
      </div>
    </main>
  );
}