import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://bailey-electrical.co.uk',
  trailingSlash: 'always',
  build: { format: 'directory' },
  integrations: [sitemap({ filter: (page) => !page.includes('/404') })],
  // Allow temporary preview links (cloudflared quick tunnels) to reach the dev server
  vite: { server: { allowedHosts: ['.trycloudflare.com'] }, preview: { allowedHosts: ['.trycloudflare.com'] } },
});
