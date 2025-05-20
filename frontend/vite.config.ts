import {defineConfig} from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
    plugins: [react()],
    resolve: {
        alias: {
            '@': path.resolve(__dirname, 'src')
        }
    },
    server: {
        proxy: {
            '/api': 'http://localhost:8000'
        },
        host: true, // bu albatta bo'lishi kerak
        port: 5174, // sening local frontaend porting
        allowedHosts: ['.trycloudflare.com'], // barcha ngrok subdomenlarini ruxsat beramiz
    },
})