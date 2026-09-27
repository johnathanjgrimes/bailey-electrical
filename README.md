# Bailey Electrical website

Built with [Astro](https://astro.build) (static output) and Tailwind CSS. Hosted free on GitHub Pages, deployed automatically by GitHub Actions on every push to `main`.

## Run it locally

```bash
npm install
npm run dev        # http://localhost:4321 – live preview while editing
npm run build      # builds the static site into dist/
npm run preview    # preview the built site
```

## Where things live

| What | Where |
|---|---|
| Phone, email, areas, review links | `src/data/business.json` |
| Service pages (copy, FAQs, images) | `src/data/services.json` → rendered by `src/pages/[service].astro` |
| Home page FAQs | `src/data/home-faq.json` |
| **Mark's guide prices** (quote builder + prices page) | `src/data/pricing.json` – set `"enabled": true` once real figures are in |
| **Form email key** | `src/data/config.json` → `web3formsKey` |
| Guides (Markdown) | `src/content/guides/*.md` – add a file to add a guide |
| Project case studies (Markdown) | `src/content/projects/*.md` – add a file + photos to add a project |
| Photos, logo, icons, robots.txt, CNAME | `public/` |
| Quote builder / rewire checker / form + postcode logic | `public/js/quote-builder.js`, `rewire-check.js`, `site.js` |
| Page layout, nav, footer, structured data | `src/layouts/Base.astro`, `src/components/`, `src/lib/schema.ts` |

## Enquiry forms

Forms send through [Web3Forms](https://web3forms.com) (free, no server needed). Sign up with the email enquiries should go to, copy the access key into `src/data/config.json` → `web3formsKey`, and push. Until a key is set, forms fall back to opening the visitor's email app.

## Postcode check

Quote forms look up the postcode with [postcodes.io](https://postcodes.io) (free, no key) and show the distance from Cardiff. The base point and radius are in `src/data/config.json`. The distance is included in every enquiry.

## Guide prices in the quote builder

`src/data/pricing.json` holds a simple model: a base price per property type, plus per room, per double socket, per lighting type, per extra, and an uplift if the house is occupied. The builder shows a range (± `spread`). Keep `enabled: false` until Mark has filled in real numbers.

## Adding photos

Resize to a maximum of 1600px on the long edge and strip location data first (phone photos often contain the customer's GPS location).
