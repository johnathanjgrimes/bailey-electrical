import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const guides = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/guides' }),
  schema: z.object({
    title: z.string(),
    seoTitle: z.string(),
    description: z.string(),
    kicker: z.string().default('Guide'),
    updated: z.coerce.date(),
    image: z.string().optional(),
    faq: z.array(z.object({ q: z.string(), a: z.string() })).default([]),
    sources: z.array(z.object({ name: z.string(), url: z.string() })).default([]),
    cta: z.object({ text: z.string(), href: z.string() }).optional(),
  }),
});

const projects = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/projects' }),
  schema: z.object({
    title: z.string(),
    category: z.string(),
    summary: z.string(),
    location: z.string().optional(),
    services: z.array(z.string()),
    images: z.array(z.object({ src: z.string(), alt: z.string() })),
    order: z.number().default(0),
  }),
});

export const collections = { guides, projects };
