# Bailey Electrical – SEO & AI checklist

What's already done on the website, and what still needs doing by a person (mostly Google accounts and reviews). The things not yet done matter **more** than the website itself for local leads.

---

## ✅ Done on the website

### Pages & content
- [x] Home page rewritten around the work Mark wants (rewires, renovations, extensions, consumer units, lighting)
- [x] Separate page for each main service, each with 1,000+ words of useful, specific content:
  - `/rewires-cardiff/`
  - `/consumer-unit-upgrades-cardiff/`
  - `/extensions-renovations-electrician-cardiff/`
  - `/eicr-landlord-certificates-cardiff/` (includes the Renting Homes (Wales) EICR rules)
  - `/builders-trades/`
- [x] FAQ sections on every page, written as the questions people actually type or ask AI
- [x] "Who we work with" section (homeowners, builders, landlords, small businesses)
- [x] Areas we cover section naming the Cardiff neighbourhoods and nearby towns
- [x] Clearly states what the business *doesn't* do (24/7 emergencies) so AI answers and customers get it right
- [x] Placeholder testimonials and unverified stats removed (Google and AI tools penalise invented reviews and claims)
- [x] Captioned project photos with descriptive alt text

### Technical SEO
- [x] Unique `<title>` and meta description on every page, with "Cardiff" and the service in them
- [x] Canonical URLs
- [x] One `<h1>` per page and a sensible heading structure
- [x] `sitemap.xml` listing every page
- [x] `robots.txt` allowing all search engines and pointing to the sitemap
- [x] Custom `404.html` page (not indexed)
- [x] Internal links between the home page and service pages, plus breadcrumbs
- [x] Open Graph and Twitter card tags with a proper 1200×630 share image (`assets/og-image.jpg`) for nice previews on WhatsApp, Facebook and so on
- [x] Favicon, Apple touch icon and web manifest
- [x] `lang="en-GB"` and `geo` region tags for Cardiff

### Structured data (schema.org JSON-LD)
- [x] `Electrician` (LocalBusiness) with phone, email, area served, services offered and Facebook link
- [x] `Service` schema on every service page
- [x] `FAQPage` schema on every page
- [x] `BreadcrumbList` on service pages
- [x] `WebSite` and `WebPage`

### Speed & mobile (Google ranks on these)
- [x] Tailwind now compiled to a small static CSS file (`assets/styles.css`, about 17 KB) instead of the ~300 KB Tailwind Play CDN script, which Tailwind says not to use in production
- [x] Icons load without blocking the page
- [x] Photos resized, compressed and stripped of metadata (EXIF/GPS)
- [x] Hero image preloaded; other images lazy-loaded; image dimensions set so the layout doesn't jump
- [x] Mobile menu, and a Call / Get a quote bar fixed to the bottom on phones
- [x] Accessible labels, skip link and `aria` attributes

### AI assistants (ChatGPT, Claude, Perplexity, Gemini, Google AI Overviews)
- [x] `llms.txt` – a plain-English Markdown summary of the business, its services, areas and FAQs for AI tools to read
- [x] `robots.txt` explicitly allows AI crawlers (GPTBot, OAI-SearchBot, ClaudeBot, PerplexityBot, Google-Extended, Applebot and others)
- [x] Content written as clear, factual statements ("Bailey Electrical is a NICEIC registered electrician in Cardiff that specialises in…"), which AI tools quote more readily
- [x] Business name, phone and area identical everywhere on the site

> Honest note: no major AI company has confirmed it reads `llms.txt`. It's cheap to have, but what really gets a business named by AI assistants and in Google AI Overviews is the same as normal local SEO: being indexed by Google **and Bing** (ChatGPT search uses Bing), a strong Google Business Profile, reviews, and consistent details across the web. That's the list below.

---

## ⬜ To do – needs Mark, John or Mark's partner

### 1. Check the facts on the site (before anything else)
- [ ] Confirm **NICEIC registration** is current, and send John the registration number to display (the site says it in several places)
- [ ] Confirm the **areas list** (remove anywhere Mark doesn't want to go)
- [ ] Confirm **services**: EV chargers? Small commercial? Emergency work? (EV and 24/7 are left off for now)
- [ ] Add **town names** to the three project write-ups if possible (e.g. "Kitchen extension, Penarth")

### 2. Google Business Profile – the single biggest thing for local leads
This is what shows up in Google Maps, the "map pack" at the top of local searches, and it feeds Google AI Overviews.
- [ ] Claim or verify the profile at <https://business.google.com>
- [ ] Primary category: **Electrician**. Add secondary categories only if they're true (e.g. Lighting contractor)
- [ ] Set as a **service-area business** (hide the home address) and add the service areas: Cardiff, Penarth, Barry, Vale of Glamorgan, Caerphilly, Pontypridd, Llantrisant, Cowbridge, Newport
- [ ] Website: `https://bailey-electrical.co.uk`
- [ ] Phone: `07590 275205`, written exactly as on the site
- [ ] Add every service (Rewires, Consumer unit upgrades, EICR, Landlord certificates, Lighting, Extensions & renovations) with a short description
- [ ] Opening hours (and add these to the website too – currently not listed)
- [ ] Business description (copy the first paragraph of `llms.txt`)
- [ ] Upload **lots of real job photos**, and keep adding them – before/after, consumer units, finished kitchens and bathrooms
- [ ] Post an update every couple of weeks (a finished job with a photo is enough)
- [ ] Add the Q&A: copy the FAQs from the website

### 3. Reviews – the second biggest thing
- [ ] Ask **every** happy customer, and the builders he works with, for a Google review. Send them the "Leave a review" link from the site
- [ ] Ask them to mention the job and the area ("Rewired our house in Whitchurch…") – this helps rankings and AI answers
- [ ] Reply to every review
- [ ] Once there are good reviews, John can add a few **word-for-word** to the website (never edit or invent them – it's against UK consumer law and Google's policies)

### 4. Search engines
- [ ] **Google Search Console** – <https://search.google.com/search-console>: add `bailey-electrical.co.uk` (verify with a DNS TXT record), submit `https://bailey-electrical.co.uk/sitemap.xml`, then use "URL inspection → Request indexing" on each page
- [ ] **Bing Webmaster Tools** – <https://www.bing.com/webmasters>: import from Search Console and submit the sitemap. **This is what ChatGPT search draws on**, so it's worth the five minutes
- [ ] **Bing Places for Business** – <https://www.bingplaces.com>: import from the Google Business Profile
- [ ] **Apple Business Connect** – <https://businessconnect.apple.com>: gets the business into Apple Maps and Siri

### 5. Consistent listings ("citations")
Same name, phone and website everywhere. Pick the ones that are free and relevant:
- [ ] NICEIC "Find a contractor" listing – make sure the website link is on it
- [ ] Facebook page – add the website link, services and service area; use the same phone number
- [ ] Yell, Thomson Local, FreeIndex, Cylex (free listings)
- [ ] Checkatrade / MyBuilder / Rated People – optional and paid, and they tend to bring small, price-shopping jobs, so only if they suit

### 6. Domain and email
- [ ] In GitHub → Settings → Pages: tick **Enforce HTTPS**
- [ ] Make sure `www.bailey-electrical.co.uk` redirects to `bailey-electrical.co.uk` (add the `www` CNAME at the domain registrar)
- [ ] Set up a business email on the domain (e.g. `info@bailey-electrical.co.uk`, via Google Workspace or the registrar) and update `EMAIL` in `src/content.py`

### 7. Ongoing (monthly, 20 minutes)
- [ ] Add new project photos to the site and Google Business Profile
- [ ] Check Search Console for errors and the searches people use to find the site
- [ ] Ask for reviews after every job
- [ ] Try asking ChatGPT, Gemini and Perplexity "best electrician for a rewire in Cardiff" to see what they say

---

## Why there are no separate pages for each town
Pages like "Electrician Penarth", "Electrician Barry" and so on that only swap the town name are called **doorway pages** in Google's spam policies, and they can hurt the whole site. The better approach, which is what's here:
- one strong page for each **service**, each naming the areas covered
- an Areas section on the home page
- a Google Business Profile with the service areas set

If Mark later does several jobs in one town and has photos and reviews from there, a genuine page about that work (e.g. "Recent rewires in Penarth") is fine to add.
