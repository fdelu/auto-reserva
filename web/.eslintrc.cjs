module.exports = {
  root: true,
  env: { browser: true, es2020: true },
  extends: [
    "eslint:recommended",
    "plugin:import/recommended",
    "plugin:promise/recommended",
    "plugin:jsx-a11y/recommended",
    "plugin:@typescript-eslint/eslint-recommended",
    "plugin:@typescript-eslint/recommended-type-checked",
    "plugin:@typescript-eslint/stylistic-type-checked",
    "plugin:react-hooks/recommended",
    "plugin:react/recommended",
    "plugin:react/jsx-runtime",
    "prettier",
    "plugin:prettier/recommended",
    "plugin:security/recommended-legacy",
  ],
  ignorePatterns: ["dist", ".eslintrc.cjs", "vite.config.ts"],
  plugins: ["react", "react-refresh"],
  rules: {
    "@typescript-eslint/consistent-type-definitions": ["error", "type"],
    "no-console": "off",
    "security/detect-object-injection": "off",
  },
  parser: "@typescript-eslint/parser",
  parserOptions: {
    ecmaVersion: "latest",
    sourceType: "module",
    project: "./tsconfig.json",
    tsconfigRootDir: ".",
  },
  settings: {
    react: { version: "detect" },
    "import/resolver": {
      node: { extensions: [".js", ".jsx", ".ts", ".tsx"] },
      typescript: {
        alwaysTryTypes: true,
        project: "./tsconfig.json",
      },
      alias: {
        map: [["", "./public"]],
      },
    },
    "import/parsers": {
      "@typescript-eslint/parser": [".ts", ".tsx"],
    },
  },
};
