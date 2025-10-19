/** @type {import('postcss-load-config').Config} */
const config = {
  plugins: {
    // Thay đổi ở đây: Gọi plugin thông qua package mới
    '@tailwindcss/postcss': {}, 
    autoprefixer: {},
  },
};

export default config;