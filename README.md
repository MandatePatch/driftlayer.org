# driftlayer.org

Static publication site for The Drift Layer. Plain HTML, no build step, no scripts, no analytics, no
external assets — every page is self-contained so that a page saved to disk still renders in ten years.
Deployed with GitHub Pages from `main`.

Site text © 2026 Matthew T. Kirby; publications carry their own licence, stated on each publication's page.

## Layout

    index.html                                     the publication
    papers/index.html                              the archive index
    papers/<slug>/index.html                       one landing page per publication
    papers/<slug>/<slug>-v<n>.pdf                  the file, never overwritten
    errata/index.html                              versioning and errata policy
    CNAME  .nojekyll  favicon.svg

## Rules this repo keeps

- A published file is never overwritten. A correction is `-v2` alongside `-v1`, with a dated line on the
  landing page. See `errata/index.html`.
- The SHA-256 printed on a landing page must match the file it names. Check before merging any change to
  a PDF.
- `papers/the-drift-layer/` is a placeholder: `noindex`, and not linked from the archive index. The entry
  for it in `papers/index.html` is commented out and is uncommented at publication.

## Deploying

1. Merge to `main`.
2. Settings → Pages → Deploy from a branch → `main` / `/` → Save.
3. DNS at the registrar: apex `A` to 185.199.108.153, 185.199.109.153, 185.199.110.153, 185.199.111.153
   (and the four `AAAA` if offered: 2606:50c0:8000::153, :8001::153, :8002::153, :8003::153);
   `www` `CNAME` to `MandatePatch.github.io`. Remove any parking or forwarding first.
4. Settings → Pages → Custom domain `driftlayer.org`; tick Enforce HTTPS once the certificate issues.

## Dates

Each publication carries its own date. The date on a landing page and the date on that
publication's entry in `papers/index.html` must agree. Dates below are taken from the
served pages, opened 7 October 2026, not invented.

- `papers/rpib-consultation-response/index.html` — Date row: 9 September 2026 (submitted),
  published here 10 September 2026. Version 1 line: 10 September 2026.
- `papers/definitions/index.html` — Date row 10 September 2026. Version 1 line: 10 September 2026.
- `papers/hmt-payment-services-consultation-response/index.html` — Date row: 13 September 2026
  (submitted), published here 13 September 2026. Version 1 line: 13 September 2026.
- `papers/the-drift-layer/index.html` — Date row 14 September 2026.
- `papers/liability-rule/index.html` — Date row: Version 1, 24 September 2026, published
  25 September 2026.

The RPIB paper also carries two dates that are not the publication date and must not be changed with it:
9 September 2026, when the response was submitted, and 11 September 2026, when the consultation closes.
