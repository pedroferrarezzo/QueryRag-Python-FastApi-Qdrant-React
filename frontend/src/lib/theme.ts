
/**
 * Inicializa o tema do aplicativo com base na preferência do usuário ou na configuração do sistema operacional.
 */
export function initTheme() {
    document.documentElement.classList.toggle(
    "dark",
    localStorage.theme === "dark" ||
        (!("theme" in localStorage) && window.matchMedia("(prefers-color-scheme: dark)").matches),
    );
}