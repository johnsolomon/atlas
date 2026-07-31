---
type: reference
title: Accessibility
chapter: boards
order: 93
subtitle: The accessibility features built in, the standard we aim for, known limits, and how to report a barrier
aliases: [accessibility, a11y, screen reader, keyboard, contrast, wcag, accessible, disability]
review_status: physician-reviewed
last_updated: 2026-07-30
tags: [reference, accessibility, quality]
---

## Quick Answer

Accessibility is treated as a requirement of the build, not an afterthought: the atlas is **keyboard-navigable**, uses **semantic landmarks** for screen readers, meets **AA-level contrast in both light and dark themes**, and works **without JavaScript** for core reading. The goal is conformance with **WCAG 2.1 Level AA**; the atlas has not yet been through a formal third-party audit, so this statement describes what is built and where the known gaps are.

## Built-in features

{K} The following are part of the shipped file:

- **Keyboard navigation** — a visible **skip link** jumps to the main content; the search box, command palette, index, and every page link are reachable and operable by keyboard, with keyboard shortcuts for search (`/`), the command palette (`Ctrl/Cmd-K`), and page-to-page movement.
- **Screen-reader structure** — semantic HTML landmarks (banner, navigation, main), heading hierarchy, and `aria-label`s on controls so assistive technology can navigate the document meaningfully.
- **Contrast** — text and interactive states meet AA contrast in both themes; the dark theme's colours were checked by measuring computed contrast ratios rather than by eye.
- **Works without JavaScript** — the home content renders and is readable with scripting disabled, and a notice points to the interactive features that need it.
- **Scalable text** — the layout uses relative units and reflows with browser zoom and increased default font size.

## Dismissing and operating dialogs

{H} Every overlay — the A–Z index, command palette, study mode, and help — can be closed by the **Escape key**, by its **× button**, and by **clicking outside** it, so a keyboard or screen-reader user is never trapped in a modal.

## Known limitations

{D} A few areas are honest gaps we are working toward: the interactive **calculators and charts** have had less assistive-technology testing than the prose, and the atlas has **not** yet undergone a formal WCAG audit or testing across the full range of screen-reader-and-browser combinations. Real patient images are not yet present; when they are added, each will carry descriptive alt text. If any of these blocks you, please tell us — see below.

## Report a barrier

If you encounter an accessibility barrier, write to **[__CONTACT__](mailto:__CONTACT__)** with the page, the assistive technology you were using, and what happened. Reports are prioritized because a reference no one can reach is not a reference.

## Related Pages

- **[Feedback & Corrections](#/feedback-corrections)** — report any issue, accessibility or otherwise.
- **[Privacy & Data](#/privacy)** — what the atlas stores on your device.
- **[About & Methodology](#/about-methodology)** — how the atlas is built.
