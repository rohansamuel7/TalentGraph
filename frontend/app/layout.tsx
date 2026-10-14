import type { Metadata } from "next";
import "./globals.css";
import { Shell } from "../components/Shell";

export const metadata: Metadata = { title: "TalentGraph", description: "Evidence-led talent intelligence" };

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  // This runs before hydration to avoid a theme flash. The only intentional
  // server/client difference is the root data-theme attribute set by this script.
  const themeScript = `(() => { const saved = localStorage.getItem('talentgraph-theme'); const theme = saved || (matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'); document.documentElement.dataset.theme = theme; })()`;
  return <html lang="en" suppressHydrationWarning><head><script dangerouslySetInnerHTML={{ __html: themeScript }} /></head><body><Shell>{children}</Shell></body></html>;
}
