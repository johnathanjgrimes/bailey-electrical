import biz from '../data/business.json';
import services from '../data/services.json';

export const SITE = biz.SITE;
export const BIZ_ID = `${SITE}/#business`;
export const stripTags = (s: string) =>
  s.replace(/<[^>]+>/g, '').replace(/&amp;/g, '&').replace(/&rsquo;/g, '’').replace(/&mdash;/g, '—').replace(/&ndash;/g, '–').trim();

const areas = ['Cardiff', ...biz.NEARBY_AREAS];

export function areaServed() {
  return areas.map((a) => ({ '@type': a === 'Vale of Glamorgan' ? 'AdministrativeArea' : 'City', name: a }));
}

export function businessSchema() {
  return {
    '@type': 'Electrician',
    '@id': BIZ_ID,
    name: biz.NAME,
    url: `${SITE}/`,
    logo: `${SITE}/logo.svg`,
    image: [`${SITE}/assets/og-image.jpg`, `${SITE}/work-3.jpeg`, `${SITE}/work-7.jpeg`, `${SITE}/work-1.jpeg`],
    description:
      'Local, independent electrician in Cardiff specialising in rewires, consumer unit upgrades, extension and renovation electrics, lighting, EICRs and landlord certificates. Works with homeowners, landlords, builders and other trades.',
    slogan: 'Rewires, renovations & extensions — done properly.',
    telephone: biz.PHONE_INTL,
    email: biz.EMAIL,
    address: { '@type': 'PostalAddress', addressLocality: 'Cardiff', addressRegion: 'Wales', addressCountry: 'GB' },
    areaServed: areaServed(),
    knowsLanguage: 'en-GB',
    currenciesAccepted: 'GBP',
    knowsAbout: [
      'House rewiring', 'Consumer unit replacement', 'Electrical Installation Condition Reports',
      'Landlord electrical safety certificates', 'Renting Homes (Wales) electrical safety', 'Extension and renovation electrics',
      'Kitchen and bathroom electrics', 'LED and outdoor lighting', 'Fault finding', 'BS 7671',
    ],
    contactPoint: { '@type': 'ContactPoint', contactType: 'customer service', telephone: biz.PHONE_INTL, email: biz.EMAIL, areaServed: 'GB', availableLanguage: 'en-GB' },
    hasOfferCatalog: {
      '@type': 'OfferCatalog',
      name: 'Electrical services',
      itemListElement: services.map((s: any) => ({
        '@type': 'Offer',
        itemOffered: { '@type': 'Service', name: stripTags(s.h1), url: `${SITE}/${s.slug}/` },
      })),
    },
    potentialAction: [
      { '@type': 'CommunicateAction', name: 'Request a quote', target: `${SITE}/get-a-quote/` },
      { '@type': 'CommunicateAction', name: 'Build a rewire quote', target: `${SITE}/rewire-quote-builder/` },
    ],
    sameAs: [biz.FACEBOOK],
  };
}

export function faqSchema(faq: { q: string; a: string }[], url: string) {
  return {
    '@type': 'FAQPage',
    '@id': `${url}#faq`,
    mainEntity: faq.map(({ q, a }) => ({ '@type': 'Question', name: q, acceptedAnswer: { '@type': 'Answer', text: a } })),
  };
}

export function crumbs(items: [string, string][]) {
  return {
    '@type': 'BreadcrumbList',
    itemListElement: items.map(([name, path], i) => ({ '@type': 'ListItem', position: i + 1, name, item: `${SITE}${path}` })),
  };
}

export function webPage(path: string, name: string, extra: object = {}) {
  return {
    '@type': 'WebPage', '@id': `${SITE}${path}#webpage`, url: `${SITE}${path}`, name,
    isPartOf: { '@type': 'WebSite', '@id': `${SITE}/#website`, url: `${SITE}/`, name: biz.NAME, publisher: { '@id': BIZ_ID } },
    inLanguage: 'en-GB', dateModified: new Date().toISOString().slice(0, 10), ...extra,
  };
}
