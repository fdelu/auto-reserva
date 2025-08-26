import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import checker from "vite-plugin-checker";

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    react(
      {
        babel: {
          plugins: [["babel-plugin-react-compiler", { target: "19" }]]
        }
      }
    ),
    checker({
      typescript: true,
    }),
  ],
});
