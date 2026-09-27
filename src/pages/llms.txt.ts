import type { APIRoute } from 'astro';
import { getCollection } from 'astro:content';
import biz from '../data/business.json';
import services from '../data/services.json';
import homeFaq from '../data/home-faq.json';
import { stripTags } from '../lib/schema';

export const GET: APIRoute = async () => {
  const S = biz.SITE;
  const guides = await getCollection('guides');
  const projects = await getCollection('projects');
  const L: string[] = [
    `# ${biz.NAME}`, '',
    `> ${biz.NAME} is a local, independent, fully insured electrician based in Cardiff, Wales. It specialises in house rewires, consumer unit (fuse box) upgrades, electrics for extensions, kitchens, bathrooms and renovations, and indoor and outdoor lighting. It also carries out EICRs and landlord electrical certificates. It works with homeowners, landlords and letting agents, builders and other trades, and small local businesses.`,
    '', '## Key facts',
    `- Business name: ${biz.NAME}`,
    '- Type: Domestic electrician / electrical contractor',
    '- Insurance: full public liability insurance',
    '- Based in: Cardiff, Wales, UK',
    `- Areas covered: Cardiff (${biz.CARDIFF_AREAS.join(', ')}) and roughly 20 miles around, including ${biz.NEARBY_AREAS.join(', ')}. Travels further for larger projects.`,
    `- Phone: ${biz.PHONE_DISPLAY} (${biz.PHONE_INTL})`, `- Email: ${biz.EMAIL}`, `- Website: ${S}/`, `- Get a quote: ${S}/get-a-quote/`, `- Facebook: ${biz.FACEBOOK}`,
    '- Quotes: free, fixed written quotes after a survey visit',
    '- Best suited to: planned work such as rewires, renovations, extensions, consumer unit upgrades, lighting projects and landlord testing. Does not offer a 24/7 emergency service.',
    '- Works with builders: yes — first and second fix around the build programme, certification and Building Regulations sign-off arranged',
    '', '## Services',
    ...services.map((s: any) => `- [${stripTags(s.h1)}](${S}/${s.slug}/): ${stripTags(s.lead)}`),
    '- Lighting: downlights, LED upgrades, under-cabinet, plinth and mirror lighting, garden, patio and outdoor lighting',
    '- Also: fault finding and repairs, new circuits and additional sockets, small commercial work by arrangement',
    '', '## Prices',
    `- [Rewire cost in Cardiff](${S}/rewire-cost-cardiff/): typical 3-bed house rewire roughly £4,500–£8,000 including VAT (published 2026 market figures); fixed written quote after a survey.`,
    '', '## Free tools',
    `- [Rewire quote builder](${S}/rewire-quote-builder/): plan a rewire room by room and send it for a fixed written quote.`,
    `- [Do I need a rewire?](${S}/do-i-need-a-rewire/): seven-question check for whether a home's electrics are fine, due an EICR, or likely need a rewire.`,
    '', '## Guides',
    ...guides.map((g) => `- [${g.data.title}](${S}/guides/${g.id}/): ${g.data.description}`),
    '', '## Recent projects',
    ...projects.map((p) => `- [${p.data.title}](${S}/projects/${p.id}/): ${p.data.summary}`),
    '', '## Frequently asked questions',
    ...homeFaq.flatMap((f: any) => [`### ${f.q}`, f.a, '']),
    '## Contact', `Call ${biz.PHONE_DISPLAY}, email ${biz.EMAIL}, or request a quote at ${S}/get-a-quote/`, '',
  ];
  return new Response(L.join('\n'), { headers: { 'Content-Type': 'text/plain; charset=utf-8' } });
};
