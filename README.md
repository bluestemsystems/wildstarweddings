# Wildstar Weddings — wildstarweddings.com

A static website for Wildstar Weddings (New Braunfels / Texas Hill Country wedding
officiant), hand-built in plain HTML/CSS/JS and hosted free on **GitHub Pages**.
Migrated off Squarespace.

## Structure

```
.
├── index.html              # Home
├── about/                  # About Wren
├── wedding-packages/       # Packages & pricing
├── gallery/                # Photo grid + Instagram embeds
├── faqs/                   # FAQ accordion
├── contact/                # Formspree contact form
├── text-me/                # SMS quick-contact
├── links/                  # Link-in-bio style page
├── privacy-and-tos/        # Privacy Policy & Terms
├── 404.html
├── assets/
│   ├── css/style.css       # All styles (design system)
│   ├── js/main.js          # Mobile nav + footer year
│   └── img/                # All images
├── CNAME                   # Custom domain (www.wildstarweddings.com)
├── sitemap.xml  robots.txt  .nojekyll
```

## Editing

Everything is plain HTML — open any `index.html` and edit the text directly.
The header and footer are repeated on each page; if you change navigation or
contact info, update it on each page (or re-run `tools/` if regenerating).
Global colors and fonts live at the top of `assets/css/style.css` (`:root`).

## Preview locally

GitHub Pages uses clean URLs (`/about/`), so preview with a local server:

```bash
cd WildstarWeddings.com
python3 -m http.server 8000
# then open http://localhost:8000
```

## Deploy (GitHub Pages)

The repo is published from the `main` branch root. Pushing to `main` updates the
live site within a minute or two.

## Contact form

The contact form posts to **Formspree** (`https://formspree.io/f/meebjpyb`).
Submissions arrive in the Formspree dashboard / email on file.

## Custom domain & DNS

`CNAME` is set to `www.wildstarweddings.com`. At the domain registrar, point DNS to
GitHub Pages:

- `www`  → CNAME → `bluestemsystems.github.io`
- apex `@` → four A records → `185.199.108.153`, `185.199.109.153`,
  `185.199.110.153`, `185.199.111.153`

Then enable **Enforce HTTPS** in the repo's Pages settings.
