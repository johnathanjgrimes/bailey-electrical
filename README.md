# Bailey Electrical website

Static site for https://bailey-electrical.co.uk, hosted on GitHub Pages.

## Editing

All copy and business details (phone, email, areas, services, FAQs) live in **`src/content.py`**.
Page layouts live in `src/build.py`. The HTML files in the repo are generated — don't edit them by hand.

```bash
npm install        # first time only (installs Tailwind)
npm run build      # regenerates HTML, sitemap.xml, llms.txt and assets/styles.css
python3 -m http.server 8000   # preview at http://localhost:8000
```

Commit the generated files and push to `main`; GitHub Pages publishes them.

## What's here

| Path | What it is |
|---|---|
| `index.html` | Home page |
| `rewires-cardiff/`, `consumer-unit-upgrades-cardiff/`, `extensions-renovations-electrician-cardiff/`, `eicr-landlord-certificates-cardiff/`, `builders-trades/` | Service pages |
| `404.html` | Not-found page |
| `sitemap.xml`, `robots.txt` | For search engines |
| `llms.txt` | Plain-English summary for AI assistants |
| `assets/` | Compiled CSS, share image, icons |
| `work-*.jpeg` | Project photos |
| `SEO-CHECKLIST.md` | What's done and what still needs doing off-site |

## Adding photos

Resize to a maximum of 1600px on the long edge and strip location data before adding (phone photos often contain the customer's GPS location).
