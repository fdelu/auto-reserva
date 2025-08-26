import globals from "globals";
import js from "@eslint/js";
import importPlugin from "eslint-plugin-import";
import promisePlugin from "eslint-plugin-promise";
import jsxA11yPlugin from "eslint-plugin-jsx-a11y";
import tsPlugin from "typescript-eslint";
import reactPlugin from "eslint-plugin-react";
import reactHooksPlugin from "eslint-plugin-react-hooks";
import reactRefreshPlugin from "eslint-plugin-react-refresh";
import reactCompilerPlugin from "eslint-plugin-react-compiler";
import prettierPluginRecommended from "eslint-plugin-prettier/recommended";
import securityPlugin from "eslint-plugin-security";
import viteConfigObj from "./vite.config.ts"

export default [
  { files: ["**/*.ts", "**/*.tsx"] },
  { ignores: ["**/eslint.config.mjs", "**/vite.config.ts", "**/dist"] },
  js.configs.recommended,
  importPlugin.flatConfigs.recommended,
  ...tsPlugin.configs.recommendedTypeChecked,
  ...tsPlugin.configs.stylisticTypeChecked,
  promisePlugin.configs["flat/recommended"],
  jsxA11yPlugin.flatConfigs.recommended,
  reactPlugin.configs.flat.recommended,
  reactPlugin.configs.flat["jsx-runtime"],
  reactHooksPlugin.configs["recommended-latest"],
  reactRefreshPlugin.configs.recommended,
  reactCompilerPlugin.configs.recommended,
  prettierPluginRecommended,
  securityPlugin.configs.recommended,
  {
    languageOptions: {
      globals: {
        ...globals.browser,
      },
      ecmaVersion: "latest",
      sourceType: "module",
      parserOptions: { project: "./tsconfig.json" },
    },
    settings: {
      react: {
        version: "detect"
      },
      "import/resolver": {
        node: { extensions: [".js", ".jsx", ".ts", ".tsx"] },
        typescript: { alwaysTryTypes: true, project: "./tsconfig.json" },
        vite: { viteConfig: viteConfigObj }
      },
      "import/parsers": {
        "@typescript-eslint/parser": [".ts", ".tsx"],
      },
    },
    rules: {
      "import/no-extraneous-dependencies": ["error", { devDependencies: true }],
      "@typescript-eslint/consistent-type-definitions": ["error", "type"],
      "no-console": "off",
      "security/detect-object-injection": "off",
      "promise/always-return": "off",
      "react-compiler/react-compiler": "error",
    },
  },
];
