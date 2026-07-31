import { defineConfig, globalIgnores } from "eslint/config";
import nextVitals from "eslint-config-next/core-web-vitals";
import nextTs from "eslint-config-next/typescript";

const eslintConfig = defineConfig([
  ...nextVitals,
  ...nextTs,
  {
    rules: {
      // localStorage hydration on mount is a one-time sync (not cascading renders).
      // The set-state-in-effect rule flags this legitimate SSR/CSR pattern, so
      // we disable it project-wide where the pattern is intentional and consistent.
      "react-hooks/set-state-in-effect": "off",
      // Prettier normalizes '/" back to literal quotes in JSX text,
      // making react/no-unescaped-entities unfixable alongside the formatter.
      "react/no-unescaped-entities": "off",
    },
  },
  // Override default ignores of eslint-config-next.
  globalIgnores([
    // Default ignores of eslint-config-next:
    ".next/**",
    "out/**",
    "build/**",
    "next-env.d.ts",
    // Build-time Node scripts (CommonJS, run via `npm run`); not shipped to the browser.
    "scripts/**",
  ]),
]);

export default eslintConfig;