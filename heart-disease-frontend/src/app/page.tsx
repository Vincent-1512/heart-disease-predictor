'use client'

import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useState } from "react";

// Statically defining the initial form state for clarity and safety
const initialFormData = {
  age: '',
  sex: '',
  cigsPerDay: '',
  BPMeds: '',
  prevalentStroke: '',
  prevalentHyp: '',
  diabetes: '',
  totChol: '',
  sysBP: '',
  diaBP: '',
  BMI: '',
  heartRate: '',
  glucose: '',
};

type FormFieldConfig = {
  id: keyof typeof initialFormData;
  label: string;
  placeholder: string;
};

// Configuration for form fields for better maintainability and clearer labels
const formFieldsConfig: FormFieldConfig[] = [
  { id: 'age', label: 'Age', placeholder: 'e.g., 52' },
  { id: 'sex', label: 'Sex', placeholder: '1 for male, 0 for female' },
  { id: 'cigsPerDay', label: 'Cigarettes Per Day', placeholder: 'e.g., 0' },
  { id: 'BPMeds', label: 'On BP Medication', placeholder: '1 for yes, 0 for no' },
  { id: 'prevalentStroke', label: 'Prevalent Stroke', placeholder: '1 for yes, 0 for no' },
  { id: 'prevalentHyp', label: 'Prevalent Hypertension', placeholder: '1 for yes, 0 for no' },
  { id: 'diabetes', label: 'Diabetes', placeholder: '1 for yes, 0 for no' },
  { id: 'totChol', label: 'Total Cholesterol', placeholder: 'e.g., 250' },
  { id: 'sysBP', label: 'Systolic Blood Pressure', placeholder: 'e.g., 120' },
  { id: 'diaBP', label: 'Diastolic Blood Pressure', placeholder: 'e.g., 80' },
  { id: 'BMI', label: 'BMI', placeholder: 'e.g., 28.5' },
  { id: 'heartRate', label: 'Heart Rate', placeholder: 'e.g., 75' },
  { id: 'glucose', label: 'Glucose', placeholder: 'e.g., 85' },
];

// Helper component for a single form field
interface FormFieldProps {
  id: string;
  label: string;
  placeholder: string;
  value: string;
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  type?: string;
}

const FormField = ({ id, label, placeholder, value, onChange, type = "number" }: FormFieldProps) => (
  <div className="grid w-full items-center gap-1.5">
    <Label htmlFor={id}>{label}</Label>
    <Input
      type={type}
      id={id}
      name={id}
      placeholder={placeholder}
      value={value}
      onChange={onChange}
      required
    />
  </div>
);

interface PredictionResult {
  prediction: number;
  probability: number;
}

export default function Home() {
  const [formData, setFormData] = useState(initialFormData);
  const [result, setResult] = useState<PredictionResult | null>(null);
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prevState => ({
      ...prevState,
      [name]: value
    }));
  };

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setIsLoading(true);
    setResult(null);
    setError('');

    try {
      const processedData = Object.entries(formData).reduce((acc, [key, value]) => {
        // Ensure empty strings are converted to numbers (e.g., 0), or handle as needed
        acc[key] = Number(value);
        return acc;
      }, {} as {[key: string]: number});

      const response = await fetch('http://localhost:5001/api/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(processedData),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'An error occurred during prediction.');
      }

      setResult(data);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-8 bg-background">
      <div className="w-full max-w-2xl">
        <Card>
          <CardHeader>
            <CardTitle className="text-3xl font-bold text-center">Heart Disease Prediction</CardTitle>
            <CardDescription className="text-center text-lg">Enter the patient's details below to predict the risk of heart disease.</CardDescription>
          </CardHeader>
          <form onSubmit={handleSubmit}>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {formFieldsConfig.map(field => (
                  <FormField 
                    key={field.id}
                    id={field.id}
                    label={field.label}
                    placeholder={field.placeholder}
                    value={formData[field.id]}
                    onChange={handleChange}
                  />
                ))}
              </div>
            </CardContent>
            <CardFooter className="flex flex-col items-center gap-4 pt-6">
              <Button type="submit" className="w-full md:w-1/2 lg:w-1/3" disabled={isLoading}>
                {isLoading ? 'Predicting...' : 'Predict'}
              </Button>
              {error && (
                <div className="mt-4 p-4 rounded-md bg-destructive w-full">
                  <p className="text-center font-semibold text-destructive-foreground">Error: {error}</p>
                </div>
              )}
              {result && (
                <div className="mt-4 p-4 rounded-md bg-secondary w-full text-center">
                  <h3 className="text-lg font-bold text-secondary-foreground">Prediction Result</h3>
                  <p className={`text-2xl font-bold ${result.prediction === 1 ? 'text-red-500' : 'text-green-500'}`}>
                    {result.prediction === 1 ? 'High Risk' : 'Low Risk'}
                  </p>
                  <p className="text-md text-muted-foreground">Probability of Heart Disease: {result.probability}</p>
                </div>
              )}
            </CardFooter>
          </form>
        </Card>
      </div>
    </main>
  );
}