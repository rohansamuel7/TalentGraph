"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useEffect, useState } from "react";
import type { ReactNode } from "react";

function ThemeToggle() {
  const [dark, setDark] = useState(false);
  useEffect(() => setDark(document.documentElement.dataset.theme === "dark"), []);
  const toggle = () => { const next = dark ? "light" : "dark"; document.documentElement.dataset.theme = next; localStorage.setItem("talentgraph-theme", next); setDark(!dark); };
  return <button className="theme-toggle" type="button" aria-label={`Switch to ${dark ? "light" : "dark"} mode`} onClick={toggle}><span aria-hidden="true">{dark ? "☾" : "☀"}</span><i className={dark ? "thumb dark" : "thumb"} /></button>;
}

export function Shell({ children }: { children: ReactNode }) {
  const pathname = usePathname();
  const links = [
    { href: "/network", label: "Explore Network" },
    { href: "/matches", label: "Discover Matches" },
    { href: "/insights", label: "Insights" },
  ];

  return <div className="shell"><aside className="sidebar"><div className="brand"><span className="brand-mark">T</span><span>TalentGraph</span></div><nav aria-label="Main navigation">{links.map(({ href, label }) => <Link key={href} href={href} aria-current={pathname === href ? "page" : undefined}>{label}</Link>)}</nav></aside><main><div className="app-header"><ThemeToggle /></div>{children}</main></div>;
}
