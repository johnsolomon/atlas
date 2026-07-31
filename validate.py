#!/usr/bin/env python3
"""Nuclear Medicine Atlas — validation & health harness.

Codifies the invariants that keep the atlas trustworthy as it grows. Run after
every build:  python3 build_site.py && python3 validate.py

Exits non-zero if any HARD invariant fails (use in CI / pre-commit). Also prints
a HEALTH report (review status, staleness, coverage) so content aging is visible
rather than invisible. Soft warnings do not fail the build.
"""
import os, re, sys, glob, json, subprocess, shutil, datetime
import yaml
import build_site as B

HTML = open(B.OUT, encoding="utf-8").read()
CONTENT = B.BASE
errors, warnings = [], []
def err(m): errors.append(m)
def warn(m): warnings.append(m)

# ---------------------------------------------------------------- frontmatter
def frontmatter(path):
    t = open(path, encoding="utf-8").read()
    m = re.match(r"^---\n(.*?)\n---", t, re.S)
    return (yaml.safe_load(m.group(1)) or {}) if m else {}

md_files = glob.glob(os.path.join(CONTENT, "**", "*.md"), recursive=True)
fm = {os.path.basename(p)[:-3]: frontmatter(p) for p in md_files}

# ---------------------------------------------------------- 1. placement integrity
ids = [p["id"] for p in B.pages]
seen = {}
for i in ids:
    seen[i] = seen.get(i, 0) + 1
dups = [k for k, v in seen.items() if v > 1]
if dups: err(f"Duplicate page placement: {dups}")

dropped = set(B.raw_pages) - set(ids)
if dropped: err(f"Pages built but never placed in a chapter: {sorted(dropped)}")

unassigned = [p for p in B.raw_pages if p not in B.PAGE_CHAPTER and
              p not in {x for lst in B.CH_ORDER.values() for x in lst}]
if unassigned: err(f"Pages with no chapter assignment: {unassigned}")

# CH_ORDER references must exist as files
for ch, lst in B.CH_ORDER.items():
    for pid in lst:
        if pid not in B.raw_pages:
            err(f"CH_ORDER['{ch}'] references missing page: {pid}")

# every rendered page id appears exactly once as an <article>
art_ids = re.findall(r'<article class="page" id="page-([^"]+)"', HTML)
adup = [i for i in set(art_ids) if art_ids.count(i) > 1]
if adup: err(f"Duplicate <article> in HTML: {adup}")

# ---------------------------------------------------------- 2. token leaks
leaks = re.findall(r"\{[KHD]\}", HTML)
if leaks: err(f"Un-rendered yield tokens leaked into HTML: {len(leaks)} (e.g. {leaks[:3]})")

# ---------------------------------------------------------- 3. nav integrity
go_targets = set(re.findall(r"go\('([^']+)'\)", HTML))
page_ids = set(art_ids)
for t in go_targets:
    if t in ("home", "") or t.startswith("ch-"):
        continue
    if "$" in t:  # template literal (dynamic search), skip
        continue
    if t not in page_ids:
        err(f"Navigation go('{t}') resolves to no page")

# ---------------------------------------------------------- 4. per-page content contract
# Clinical pages carry self-checks + graded evidence. Non-clinical chapters (tools,
# and the community/news layers) legitimately do not, so they are exempt from those
# two content warnings — keeping the health signal about clinical pages meaningful.
NONCLINICAL = {"tools", "articles", "contributors", "field-future", "learning-paths"}
# Specific non-clinical pages living inside clinical chapters that legitimately carry
# neither a quiz nor graded evidence (an industry profile; the methodology meta-page).
EXEMPT_PAGES = {"novartis", "about-methodology", "disclaimer-terms", "feedback-corrections",
                "how-to-cite", "editorial-policy", "privacy", "accessibility", "faq",
                "contact", "whats-new"}
NONTOOL = [p for p in B.pages if p["chapter"] != "tools"]
CLINICAL = [p for p in B.pages if p["chapter"] not in NONCLINICAL and p["id"] not in EXEMPT_PAGES]
for p in CLINICAL:
    pid = p["id"]
    art = HTML.split(f'id="page-{pid}"', 1)[1].split("</article>", 1)[0] if f'id="page-{pid}"' in HTML else ""
    if "<details>" not in art:
        warn(f"[{pid}] no self-check quiz")
    has_ev = pid in B.EVIDENCE or pid in B.EXTRA_EVIDENCE
    if not has_ev:
        warn(f"[{pid}] no graded-evidence entry")

# duplicate titles
titles = {}
for p in B.pages:
    titles.setdefault(p["title"].strip(), []).append(p["id"])
for t, lst in titles.items():
    if len(lst) > 1:
        err(f"Duplicate title '{t}': {lst}")

# required frontmatter fields
REQUIRED = ["title", "subtitle", "review_status", "last_updated"]
for pid, meta in fm.items():
    if pid.startswith("tool-"):
        continue
    missing = [k for k in REQUIRED if not meta.get(k)]
    if missing:
        warn(f"[{pid}] missing frontmatter: {missing}")

# ---------------------------------------------------------- 4b. internal cross-links
# Every in-atlas link [text](#/page-id) must resolve to a real page. Checked against
# rendered hrefs (documentation examples inside code spans are not <a href> and are
# correctly ignored). A broken cross-link would otherwise ship silently.
_valid_ids = {p["id"] for p in B.pages} | {"home"}
_link_ids = set(re.findall(r'href=["\']#/([a-z0-9-]+)["\']', HTML))
_broken_links = sorted(i for i in _link_ids if i not in _valid_ids)
if _broken_links:
    err(f"Internal links to non-existent pages: {_broken_links}")

# ---------------------------------------------------------- 4c. duplicate evidence keys
# Python dict literals silently keep only the last of any duplicated key, so a repeated
# page id in EVIDENCE/EXTRA_EVIDENCE quietly discards citations. Catch it at the source.
import ast as _ast
_tree = _ast.parse(open(os.path.join(B._ROOT, "build_site.py"), encoding="utf-8").read())
for _node in _ast.walk(_tree):
    if isinstance(_node, _ast.Assign) and any(
            getattr(t, "id", "") in ("EVIDENCE", "EXTRA_EVIDENCE") for t in _node.targets):
        _name = _node.targets[0].id
        _keys = [k.value for k in _node.value.keys if isinstance(k, _ast.Constant)]
        _dupe = sorted({k for k in _keys if _keys.count(k) > 1})
        if _dupe:
            err(f"Duplicate keys in {_name} (citations silently dropped): {_dupe}")

# ---------------------------------------------------------- 5. JavaScript syntax
def node_check(js, label):
    if not shutil.which("node"):
        warn("node not available — skipped JS syntax checks")
        return
    tmp = f"/tmp/_val_{label}.js"
    open(tmp, "w").write(js)
    r = subprocess.run(["node", "--check", tmp], capture_output=True, text=True)
    if r.returncode != 0:
        err(f"JS syntax error in {label}: {r.stderr.strip().splitlines()[-1] if r.stderr else '?'}")

# app script (stub out huge JSON literals)
m = re.search(r"<script>\nconst IDX=.*?\}\)\(\);\n</script>", HTML, re.S)
if m:
    js = m.group(0).replace("<script>", "").replace("</script>", "")
    # The const declaration is a single line of injected JSON — stub the whole line
    # (robust to added constants) so node --check validates the code, not the data.
    js = re.sub(r'^const IDX=.*$',
                'const IDX=[],FIRST="home",ORDER=["home"],QUIZ=[],COMPENDIUM=[],DOMAINS=[],GLOSS={};',
                js, count=1, flags=re.M)
    node_check(js, "app")
    # Regex lookbehind throws on Safari / iOS < 16.4 — it broke the whole site on iPhone once.
    if "(?<=" in js or "(?<!" in js:
        err("Regex lookbehind ((?<= / (?<!) in app JS — unsupported on Safari/iOS < 16.4; use a capture-group boundary instead")
else:
    warn("could not locate app script for syntax check")

# each tool IIFE
for tid, src in B.TOOLS.items():
    for sm in re.finditer(r"<script>(.*?)</script>", src, re.S):
        node_check(sm.group(1), tid)

# ---------------------------------------------------------- HEALTH REPORT (soft)
today = datetime.date.today()
def age_days(d):
    try:
        return (today - datetime.date.fromisoformat(str(d))).days
    except Exception:
        return None

status = {}
ages = []
stale = []
for pid, meta in fm.items():
    if pid.startswith("tool-"):
        continue
    s = meta.get("review_status", "unknown")
    status[s] = status.get(s, 0) + 1
    a = age_days(meta.get("last_updated"))
    if a is not None:
        ages.append(a)
        if a > 365:
            stale.append((pid, a))

ev_cov = sum(1 for p in NONTOOL if p["id"] in B.EVIDENCE or p["id"] in B.EXTRA_EVIDENCE)

print("=" * 64)
print("  NUCLEAR MEDICINE ATLAS — VALIDATION & HEALTH")
print("=" * 64)
print(f"  Pages: {len(B.pages)}  |  Chapters: {len({p['chapter'] for p in B.pages})}  |  HTML: {len(HTML):,} bytes")
print(f"  Evidence coverage (non-tool): {ev_cov}/{len(NONTOOL)} ({100*ev_cov//max(1,len(NONTOOL))}%)")
print("  Review status:", ", ".join(f"{k}={v}" for k, v in sorted(status.items())))
if ages:
    ages.sort()
    print(f"  Last-updated age (days): min {ages[0]}, median {ages[len(ages)//2]}, max {ages[-1]}")
print(f"  Pages >365d since update: {len(stale)}")
for pid, a in sorted(stale, key=lambda x: -x[1])[:8]:
    print(f"      {a:>4}d  {pid}")

# ---------------------------------------------------------- verdict
print("-" * 64)
if warnings:
    print(f"  ⚠ {len(warnings)} warning(s):")
    for w in warnings[:25]:
        print(f"      {w}")
    if len(warnings) > 25:
        print(f"      … and {len(warnings)-25} more")
if errors:
    print(f"  ✗ {len(errors)} HARD failure(s):")
    for e in errors:
        print(f"      {e}")
    print("=" * 64)
    sys.exit(1)
print("  ✓ All hard invariants pass.")
print("=" * 64)
