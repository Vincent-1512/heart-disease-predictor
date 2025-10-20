'use client'

import { useState } from 'react';

// Defines the structure for the form data, ensuring type safety.
interface HeartDiseaseFormData {
    age: string;
    sex: string;
    cigarettes: string;
    'bp-meds': string;
    'prevalent-stroke': string;
    'prevalent-hypertension': string;
    diabetes: string;
    cholesterol: string;
    'sys-bp': string;
    'dia-bp': string;
    bmi: string;
    'heart-rate': string;
    glucose: string;
}

// Defines the structure for the prediction result state.
interface ResultState {
    riskLevel: 'high' | 'medium' | 'low';
    title: string;
    message: string;
    detailsHtml: string;
}

export default function Home() {
    const [result, setResult] = useState<ResultState | null>(null);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        setIsLoading(true);
        setError(null);
        setResult(null);

        const formData = new FormData(e.currentTarget);
        const formProps = Object.fromEntries(formData.entries());

        // Safely construct the data object for display and logic
        const displayData: HeartDiseaseFormData = {
            age: (formProps.age as string) || '0',
            sex: (formProps.sex as string) || '0',
            cigarettes: (formProps.cigarettes as string) || '0',
            cholesterol: (formProps.cholesterol as string) || '0',
            'sys-bp': (formProps['sys-bp'] as string) || '0',
            'dia-bp': (formProps['dia-bp'] as string) || '0',
            bmi: (formProps.bmi as string) || '0',
            'heart-rate': (formProps['heart-rate'] as string) || '0',
            glucose: (formProps.glucose as string) || '0',
            'bp-meds': formProps['bp-meds'] ? '1' : '0',
            'prevalent-stroke': formProps['prevalent-stroke'] ? '1' : '0',
            'prevalent-hypertension': formProps['prevalent-hypertension'] ? '1' : '0',
            diabetes: formProps.diabetes ? '1' : '0',
        };

        // Convert fields to numbers for the backend API
        const apiData = Object.fromEntries(
            Object.entries(displayData).map(([key, value]) => [key, Number(value)])
        );

        try {
            const response = await fetch('http://localhost:5001/api/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(apiData),
            });

            const apiResult = await response.json();

            if (!response.ok) {
                throw new Error(apiResult.error || 'Đã có lỗi xảy ra từ server.');
            }

            // Parse probability from string like "75.20%" to a number 75.20
            const probability = parseFloat(apiResult.probability.replace('%', ''));

            let riskLevel: 'high' | 'medium' | 'low';
            if (probability > 50) {
                riskLevel = 'high';
            } else if (probability > 15) {
                riskLevel = 'medium';
            } else {
                riskLevel = 'low';
            }

            displayResult(riskLevel, displayData);

        } catch (err: any) {
            setError(err.message || 'Không thể kết nối tới server dự đoán.');
        } finally {
            setIsLoading(false);
        }
    };

    const displayResult = (riskLevel: 'high' | 'medium' | 'low', data: HeartDiseaseFormData) => {
        let title: string;
        let message: string;
        let detailsHtml = '<h4 class="font-semibold">Các yếu tố nguy cơ chính:</h4><ul>';

        if (riskLevel === 'high') {
            title = 'NGUY CƠ CAO';
            message = 'Bệnh nhân có nguy cơ cao mắc bệnh tim. Nên tham khảo ý kiến bác sĩ chuyên khoa tim mạch.';
        } else if (riskLevel === 'medium') {
            title = 'NGUY CƠ TRUNG BÌNH';
            message = 'Bệnh nhân có nguy cơ trung bình mắc bệnh tim. Nên theo dõi sức khỏe định kỳ và điều chỉnh lối sống.';
        } else {
            title = 'NGUY CƠ THẤP';
            message = 'Bệnh nhân có nguy cơ thấp mắc bệnh tim. Tiếp tục duy trì lối sống lành mạnh.';
        }

       

        setResult({ riskLevel, title, message, detailsHtml });
    };

    return (
        <div className="container">
            <header>
                <h1>Dự đoán nguy cơ bệnh tim</h1>
                <p>Nhập thông tin bệnh nhân để đánh giá nguy cơ mắc bệnh tim</p>
            </header>
            
            <div className="form-container">
                <form id="heart-disease-form" onSubmit={handleSubmit}>
                    {/* Form fields remain the same */}
                    <div className="form-row">
                        <div className="form-col">
                            <label htmlFor="age">Tuổi</label>
                            <input type="number" id="age" name="age" min="18" max="100" placeholder="Ví dụ: 52" required />
                        </div>
                        
                        <div className="form-col">
                            <label htmlFor="sex">Giới tính</label>
                            <select id="sex" name="sex" defaultValue="" required>
                                <option value="" disabled>Chọn giới tính</option>
                                <option value="1">Nam</option>
                                <option value="0">Nữ</option>
                            </select>
                        </div>
                        
                        <div className="form-col">
                            <label htmlFor="cigarettes">Số điếu thuốc/ngày</label>
                            <input type="number" id="cigarettes" name="cigarettes" min="0" max="100" placeholder="Ví dụ: 0" required />
                        </div>
                    </div>
                    
                    <div className="form-group">
                        <label>Tình trạng sức khỏe</label>
                        <div className="checkbox-group">
                            <div className="checkbox-item">
                                <input type="checkbox" id="bp-meds" name="bp-meds" value="1" />
                                <label htmlFor="bp-meds">Đang dùng thuốc huyết áp</label>
                            </div>
                            
                            <div className="checkbox-item">
                                <input type="checkbox" id="prevalent-stroke" name="prevalent-stroke" value="1" />
                                <label htmlFor="prevalent-stroke">Tiền sử đột quỵ</label>
                            </div>
                            
                            <div className="checkbox-item">
                                <input type="checkbox" id="prevalent-hypertension" name="prevalent-hypertension" value="1" />
                                <label htmlFor="prevalent-hypertension">Tiền sử cao huyết áp</label>
                            </div>
                            
                            <div className="checkbox-item">
                                <input type="checkbox" id="diabetes" name="diabetes" value="1" />
                                <label htmlFor="diabetes">Tiểu đường</label>
                            </div>
                        </div>
                    </div>
                    
                    <div className="form-row">
                        <div className="form-col">
                            <label htmlFor="cholesterol">Cholesterol toàn phần (mg/dL)</label>
                            <input type="number" id="cholesterol" name="cholesterol" min="100" max="400" placeholder="Ví dụ: 250" required />
                        </div>
                        
                        <div className="form-col">
                            <label htmlFor="sys-bp">Huyết áp tâm thu (mmHg)</label>
                            <input type="number" id="sys-bp" name="sys-bp" min="80" max="200" placeholder="Ví dụ: 120" required />
                        </div>
                    </div>
                    
                    <div className="form-row">
                        <div className="form-col">
                            <label htmlFor="dia-bp">Huyết áp tâm trương (mmHg)</label>
                            <input type="number" id="dia-bp" name="dia-bp" min="50" max="130" placeholder="Ví dụ: 80" required />
                        </div>
                        
                        <div className="form-col">
                            <label htmlFor="bmi">Chỉ số khối cơ thể (BMI)</label>
                            <input type="number" id="bmi" name="bmi" min="15" max="50" step="0.1" placeholder="Ví dụ: 25.5" required />
                        </div>
                    </div>
                    
                    <div className="form-row">
                        <div className="form-col">
                            <label htmlFor="heart-rate">Nhịp tim (lần/phút)</label>
                            <input type="number" id="heart-rate" name="heart-rate" min="40" max="150" placeholder="Ví dụ: 75" required />
                        </div>
                        
                        <div className="form-col">
                            <label htmlFor="glucose">Đường huyết (mg/dL)</label>
                            <input type="number" id="glucose" name="glucose" min="50" max="300" placeholder="Ví dụ: 85" required />
                        </div>
                    </div>
                    
                    <button type="submit" className="btn" disabled={isLoading}>
                        {isLoading ? 'Đang dự đoán...' : 'Dự đoán nguy cơ'}
                    </button>
                </form>
                
                {error && (
                    <div className="result-container result-high" style={{display: 'block'}}>
                         <div className="result-title">Lỗi</div>
                         <p>{error}</p>
                    </div>
                )}

                {result && (
                    <div id="result" className={`result-container result-${result.riskLevel}`} style={{display: 'block'}}>
                        <div className="result-title" id="result-title">{result.title}</div>
                        <div id="result-message">{result.message}</div>
                        <div className="result-details" id="result-details" dangerouslySetInnerHTML={{ __html: result.detailsHtml }}></div>
                    </div>
                )}
            </div>
        </div>
    );
}