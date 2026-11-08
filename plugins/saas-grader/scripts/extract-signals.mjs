#!/usr/bin/env node
// extract-signals.mjs — deterministic signal extraction for the saas-grader plugin.
// Input:  path to an HTML file produced by `chrome --headless=new --dump-dom <url>`
// Output: compact JSON on stdout. Zero dependencies; regex-based on purpose so it
// runs on any stock Node >= 14 with no install step.
//
// Usage: node extract-signals.mjs page.html

import { readFileSync } from 'node:fs';

const file = process.argv[2];
if (!file) {
  console.error('usage: node extract-signals.mjs <dumped-dom.html>');
  process.exit(1);
}
const raw = readFileSync(file, 'utf8');

// ---------- helpers ----------

const decode = (s) =>
  s
    .replace(/&amp;/g, '&')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"')
    .replace(/&#39;|&apos;/g, "'")
    .replace(/&nbsp;/g, ' ')
    .replace(/&#(\d+);/g, (_, n) => String.fromCharCode(Number(n)));

const clean = (s) => decode(s.replace(/<[^>]*>/g, ' ')).replace(/\s+/g, ' ').trim();

const uniq = (arr) => [...new Set(arr)];

// Remove script/svg/noscript bodies (keep <style> for font analysis).
const noScript = raw
  .replace(/<script\b[\s\S]*?<\/script>/gi, ' ')
  .replace(/<noscript\b[\s\S]*?<\/noscript>/gi, ' ')
  .replace(/<svg\b[\s\S]*?<\/svg>/gi, ' ');

// Visible-ish text: also drop styles.
const visible = noScript.replace(/<style\b[\s\S]*?<\/style>/gi, ' ');
const visibleText = clean(visible);

const tagTexts = (html, tag, limit = 100) => {
  const re = new RegExp(`<${tag}\\b[^>]*>([\\s\\S]*?)<\\/${tag}>`, 'gi');
  const out = [];
  let m;
  while ((m = re.exec(html)) && out.length < limit) {
    const t = clean(m[1]);
    if (t) out.push(t);
  }
  return out;
};

const contexts = (re, limit = 40, span = 60) => {
  const out = [];
  let m;
  while ((m = re.exec(visibleText)) && out.length < limit) {
    const start = Math.max(0, m.index - span);
    out.push({
      match: m[0].trim(),
      context: visibleText.slice(start, m.index + m[0].length + span).trim(),
    });
  }
  return out;
};

// ---------- extraction ----------

const title = (raw.match(/<title[^>]*>([\s\S]*?)<\/title>/i) || [, ''])[1];
const metaDescription = (raw.match(/<meta[^>]+name=["']description["'][^>]+content=["']([^"']*)["']/i) ||
  raw.match(/<meta[^>]+content=["']([^"']*)["'][^>]+name=["']description["']/i) || [, ''])[1];

const headings = [];
for (const level of ['h1', 'h2', 'h3']) {
  for (const t of tagTexts(noScript, level)) headings.push({ level, text: t });
}

// CTAs: <button> text + <a> whose class/role smells like a button.
const buttons = tagTexts(noScript, 'button', 60);
const ctaLinks = [];
{
  const re = /<a\b([^>]*)>([\s\S]*?)<\/a>/gi;
  let m;
  while ((m = re.exec(noScript)) && ctaLinks.length < 60) {
    const attrs = m[1];
    const text = clean(m[2]);
    if (!text || text.length > 60) continue;
    if (/class=["'][^"']*(btn|button|cta)[^"']*["']/i.test(attrs) || /role=["']button["']/i.test(attrs)) {
      ctaLinks.push(text);
    }
  }
}

// Nav links (header/nav scope) — used to find the pricing page.
const navLinks = [];
{
  const navBlocks = [...noScript.matchAll(/<(?:nav|header)\b[\s\S]*?<\/(?:nav|header)>/gi)].map((m) => m[0]);
  for (const block of navBlocks) {
    const re = /<a\b[^>]*href=["']([^"']*)["'][^>]*>([\s\S]*?)<\/a>/gi;
    let m;
    while ((m = re.exec(block)) && navLinks.length < 60) {
      const text = clean(m[2]);
      if (text && text.length <= 40) navLinks.push({ text, href: m[1] });
    }
  }
}

const prices = contexts(/(?:\$|€|£)\s?\d[\d,]*(?:\.\d+)?/g, 60);
const perUnitPricing = contexts(/(?:per\s+(?:seat|user|month|year|GB|credit|contact)|\/\s?(?:mo|month|yr|year|seat|user))/gi, 30);

const socialProofNumbers = contexts(
  /\b[\d][\d,.]*\s?(?:k|K|m|M)?\+?\s*(?:users|customers|teams|companies|businesses|brands|developers|marketers|founders|analysts|creators|agencies|reviews|ratings|downloads|installs|sites|projects|countries)\b/g,
  30
);
const trustedBy = contexts(/\btrusted by\b[^.]{0,80}/gi, 10);

const starRatings = contexts(/\b([0-5](?:\.\d)?)\s*(?:\/\s*5|stars?|★)/gi, 20);
const starGlyphs = (visibleText.match(/★/g) || []).length;

const trialMentions = contexts(/\b(\d+)[-\s]?day(?:s)?\s+(?:free\s+)?trial\b/gi, 10);
const freeTrialMentioned = /\bfree trial\b/i.test(visibleText);
const freemiumSignals = contexts(/\$0\b|\bfree plan\b|\bfree forever\b|\bat no cost\b/gi, 10);

const video = {
  videoTags: (noScript.match(/<video\b/gi) || []).length,
  embeds: uniq(
    (raw.match(/(?:youtube\.com\/embed|youtu\.be|player\.vimeo|wistia|loom\.com)[^"'\s]*/gi) || []).map((s) =>
      s.slice(0, 80)
    )
  ).slice(0, 10),
  mp4orWebm: (raw.match(/\.(?:mp4|webm)\b/gi) || []).length,
  gifs: (raw.match(/\.gif\b/gi) || []).length,
};

// Fonts declared in inline <style> blocks (external CSS is not in a DOM dump —
// treat this as partial evidence, not proof).
const fontFamilies = uniq(
  [...raw.matchAll(/font-family\s*:\s*([^;}{]+)[;}]/gi)]
    .map((m) => m[1].replace(/["']/g, '').trim())
    .filter((f) => f && !/inherit|var\(/.test(f))
).slice(0, 15);

// Testimonial candidates: blockquotes + elements whose class mentions testimonial/review/quote.
const testimonialCandidates = tagTexts(noScript, 'blockquote', 10);
{
  const re = /<(div|p|li|figure)\b[^>]*class=["'][^"']*(?:testimonial|review|quote)[^"']*["'][^>]*>([\s\S]*?)<\/\1>/gi;
  let m;
  while ((m = re.exec(noScript)) && testimonialCandidates.length < 10) {
    const t = clean(m[2]);
    if (t && t.length > 20) testimonialCandidates.push(t.slice(0, 300));
  }
}

// Text stats for succinctness checks (PD-12).
const paragraphs = tagTexts(visible, 'p', 400);
const wordCount = (t) => (t ? t.split(/\s+/).length : 0);
const paragraphWordCounts = paragraphs.map(wordCount);
const textStats = {
  totalVisibleWords: wordCount(visibleText),
  paragraphCount: paragraphs.length,
  longestParagraphWords: Math.max(0, ...paragraphWordCounts),
  paragraphsOver60Words: paragraphWordCounts.filter((n) => n > 60).length,
};

// Founding / newness signals (BM-4).
const foundingSignals = contexts(/\b(?:founded|established|since|launched)\b[^.]{0,40}\b(19|20)\d{2}\b/gi, 10);
const copyrightYears = uniq((visibleText.match(/(?:©|\(c\)|copyright)\s*(?:19|20)\d{2}/gi) || [])).slice(0, 5);

const result = {
  extractedAt: 'run',
  file,
  title: clean(title),
  metaDescription: clean(metaDescription),
  headings: headings.slice(0, 60),
  ctas: { buttons: uniq(buttons).slice(0, 30), buttonLikeLinks: uniq(ctaLinks).slice(0, 30) },
  navLinks: navLinks.slice(0, 40),
  pricing: { prices, perUnitPricing },
  socialProof: { numbers: socialProofNumbers, trustedBy, starRatings, starGlyphs },
  trial: { trialMentions, freeTrialMentioned, freemiumSignals },
  video,
  fontFamilies,
  testimonialCandidates,
  textStats,
  brandAge: { foundingSignals, copyrightYears },
};

console.log(JSON.stringify(result, null, 2));
