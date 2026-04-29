import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [tailwindcss(), react()],
  // VITE_BASE is set by the GitHub Pages deploy workflow to '/repo-name/'
  // Locally it defaults to '/' so dev server works as normal.
  base: process.env.VITE_BASE ?? '/',
})
