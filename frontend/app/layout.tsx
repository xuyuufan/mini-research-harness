import "./globals.css";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Mini Research Harness",
  description: "A multi-agent research workflow tool",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
