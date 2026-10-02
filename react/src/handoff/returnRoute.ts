const key = "handoff.return";
export function rememberReturnRoute() {
  const base = import.meta.env.BASE_URL.replace(/\/$/, "");
  const path = window.location.pathname.slice(base.length);
  if (path === "/" || /^\/handoffs\/[^/?#]+$/.test(path)) {
    try {
      sessionStorage.setItem(key, path);
    } catch {
      /* Navigation still works without storage. */
    }
  }
}
export function takeReturnRoute(): string {
  try {
    const value = sessionStorage.getItem(key);
    sessionStorage.removeItem(key);
    return value && (value === "/" || /^\/handoffs\/[^/?#]+$/.test(value)) ? value : "/";
  } catch {
    return "/";
  }
}
