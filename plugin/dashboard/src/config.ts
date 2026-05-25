export const REPO_URL = "https://github.com/archugunov/pm-job-search";
export const INSTALL_URL = `${REPO_URL}#install`;
export const AUTHOR_NAME = "Arkadii Chugunov";
export const AUTHOR_LINKEDIN_URL = "https://www.linkedin.com/in/a-chugunov/";
export const SUPPORT_URL = "https://ko-fi.com/archugunov";

export const DEMO_MODE = import.meta.env.VITE_DEMO_MODE === "true";

// Vite's base is "/" in dev and "/pm-job-search/" in the GitHub Pages build.
// Use this to construct paths to assets in /public/, which Vite rewrites at build.
export const BASE_URL = import.meta.env.BASE_URL;
