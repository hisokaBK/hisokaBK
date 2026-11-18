# Hisoka GitHub Profile — Final V4

**Target:** https://github.com/hisokaBK/hisokaBK

## Installation

1. Extract `Hisoka_GitHub_Profile_V4_Final.zip`.
2. Copy `README.md` **and the complete `assets/` folder** to the root of your GitHub profile repository `hisokaBK/hisokaBK`.
3. Commit the new files (or replace the existing files with matching names).
4. Open your profile and refresh the page. GitHub may cache images temporarily.

### PowerShell (from inside the profile repository)

```powershell
git add README.md assets/
git commit -m "Finalize Hisoka profile README V4"
git push
```

If `git push` reports no upstream branch, use `git push -u origin main` for a `main` branch, or check your branch with `git branch --show-current`.

## Included features

- Original hand-fixed animated Hisoka banner (`assets/hisoka-banner.gif`).
- Both original Hisoka GIFs embedded in the About and Featured Projects sections via public external links.
- Animated card-suit separators (`assets/hisoka-cards.gif`), neon section headings and the engineering timeline.
- Four large **clickable cover images** pointing to the user's four repositories.
- C, PHP, Python, JavaScript, TypeScript, HTML/CSS, Laravel, React, Vue, Redux, Tailwind, Bootstrap, FastAPI, SQL/NoSQL, etc.
- **Postman and Swagger icons** supplied as matching local image tiles in `assets/icons/`. OpenAPI and REST API remain separate badges.
- **Backend Tools:** Composer, Apache, DBeaver, Twig, Blade.
- **DevOps & Workflow Tools:** Docker, Git, GitHub, Linux, VS Code, Figma, Nginx, Docker Compose.
- GitHub overview contains account stats and top languages only. **No streak card or contribution graph**.
- The unwanted `DESIGN • LOGIC • PRECISION` aura animation has been **removed from the repository package**.
- No traditional HTML or Markdown tables.

## Clickability and rendering notes

- Project covers and contact links use explicit `<a>` tags and are intentionally clickable.
- The banner, decorative images, icons and statistics use `<picture>` with no explicit link. This is a **best effort** to avoid GitHub's image-viewer click behavior; GitHub controls its own renderer, so it is not guaranteed for every image or future GitHub update.
- README styling uses only markup GitHub supports; there are no custom CSS/JS interactions.
- Third-party images (GitHub stats, skill icons, badges and typing SVG) require external services to be online.
- Images from Pinterest are externally hosted and could stop loading. They are not bundled in this package.
- The four illustrated project covers are **not application screenshots**.

## Project layout

```text
README.md
INSTALL.md
assets/
  hisoka-banner.gif
  hisoka-cards.gif
  engineering-flow.png
  section-about.png
  section-arsenal.png
  section-mindset.png
  section-projects.png
  section-activity.png
  section-contact.png
  icons/
    postman.png
    swagger.png
  projects/
    streaming-platform.png
    easycoloc.png
    php-orm.png
    ecoshop-api.png
```

**Important:** Do not upload the `README.md` alone. The images reference `./assets/`.
