/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                'nvidia-green': '#76B900',
                'nvidia-black': '#000000',
                'nvidia-dark-gray': '#1A1A1A',
                'nvidia-gray': '#333333',
                'nvidia-light-gray': '#E0E0E0',
            },
            fontFamily: {
                sans: ['Inter', 'system-ui', 'sans-serif'],
            },
            borderRadius: {
                'nvidia': '12px',
            },
            boxShadow: {
                'glow-green': '0 0 20px rgba(118, 185, 0, 0.3)',
                'glow-green-strong': '0 0 30px rgba(118, 185, 0, 0.5)',
            },
            animation: {
                'fade-in': 'fadeIn 0.3s ease-in',
                'slide-up': 'slideUp 0.4s ease-out',
                'shimmer': 'shimmer 2s linear infinite',
                'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
            },
            keyframes: {
                fadeIn: {
                    '0%': { opacity: '0' },
                    '100%': { opacity: '1' },
                },
                slideUp: {
                    '0%': { transform: 'translateY(20px)', opacity: '0' },
                    '100%': { transform: 'translateY(0)', opacity: '1' },
                },
                shimmer: {
                    '0%': { backgroundPosition: '-1000px 0' },
                    '100%': { backgroundPosition: '1000px 0' },
                },
            },
            backdropBlur: {
                'nvidia': '10px',
            },
        },
    },
    plugins: [],
}
