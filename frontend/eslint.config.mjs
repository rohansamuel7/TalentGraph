import nextPlugin from "@next/eslint-plugin-next";
import tsParser from "@typescript-eslint/parser";

export default [{
  files: ["**/*.{ts,tsx}"],
  languageOptions: { parser: tsParser, parserOptions: { ecmaFeatures: { jsx: true } } },
  plugins: { "@next/next": nextPlugin },
  rules: nextPlugin.configs.recommended.rules,
}];
