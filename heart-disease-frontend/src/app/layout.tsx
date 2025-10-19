// File: src/app/layout.tsx
import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css"; // <-- Dòng này cực kỳ quan trọng!

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Heart Disease Predictor",
  description: "Hệ thống dự báo bệnh tim sử dụng Machine Learning",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={inter.className}>{children}</body>
    </html>
  );
}