# Complete Creator Workflow
## Remove AI Marks → Protect Your Creation

> **proof-of-creation** + **watermarks-remover** — two complementary skills
> for the complete IP lifecycle of AI-assisted creative work.

---

## The problem these two skills solve together

Since August 2, 2026, Claude models embed mandatory EU AI Act watermarks in
generated content. As a creator, you face two distinct needs:

1. **Privacy / hygiene** — strip provenance marks from content you own,
   so it doesn't carry an AI fingerprint when you publish or distribute it
2. **Ownership** — assert *your* copyright over the creative work you directed,
   so it's legally documented as yours

Neither skill alone covers both needs. Together, they form a complete workflow.

---

## The two skills

| Skill | Repository | Stars | What it does |
|-------|-----------|-------|-------------|
| **watermarks-remover** | [guillaumemeyer/watermarks-remover](https://github.com/guillaumemeyer/watermarks-remover) | ⭐ 21k+ | Strips AI provenance marks (Unicode, statistical, C2PA/EXIF metadata) from text and files |
| **proof-of-creation** | [Lubansu/proof-of-creation](https://github.com/Lubansu/proof-of-creation) | This project | Protects your IP with copyright headers, SHA-256 hashes, and multi-jurisdiction legal guidance |

---

## Recommended sequential workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                    YOUR CREATIVE SESSION                        │
│                                                                 │
│  1. Create with Claude Code                                     │
│     Claude writes files → proof-of-creation auto-injects copyright      │
│     headers + logs SHA-256 hash → your ownership is recorded   │
│                          ↓                                      │
│  2. Strip AI provenance marks (optional, for distribution)      │
│     /remove-ai-marks → watermarks-remover cleans Unicode,      │
│     statistical marks, and file metadata                        │
│                          ↓                                      │
│  3. Verify your protection status                               │
│     /poc-report → proof-of-creation generates full IP-REPORT.md          │
│     with files, hashes, legal status, and next steps           │
│                          ↓                                      │
│  4. Register formally (if commercial)                           │
│     /poc-register → step-by-step guide for your jurisdiction    │
│     (INPI Enveloppe Soleau, USPTO, UKIPO, etc.)                │
└─────────────────────────────────────────────────────────────────┘
```

---

## Install both skills

### Step 1 — Install watermarks-remover

```bash
# Via Claude Code plugin marketplace
/plugin marketplace add guillaumemeyer/watermarks-remover
/plugin install watermarks-remover@watermarks-remover

# Start the local service (Python 3.10+ required)
cd watermarks-remover && make serve
```

### Step 2 — Install proof-of-creation

```bash
# Via Claude Code plugin marketplace
/plugin marketplace add Lubansu/proof-of-creation
/plugin install proof-of-creation@proof-of-creation
```

### Step 3 — Verify both are loaded

```
/skills
```

You should see both `proof-of-creation` and `remove-ai-marks` (or `watermarks-remover`)
in the list.

---

## Combined workflow in practice

### Scenario: You built a commercial web app with Claude Code

```bash
# During development — proof-of-creation runs automatically on every file Claude writes
# All files get: copyright header + SHA-256 hash logged

# Before shipping to production:
/remove-ai-marks          # Strip AI provenance from all project files
/poc-report                # Review your full Proof of Creation status
/poc-register              # Get registration guide for your country
```

### Scenario: You wrote content / documentation with Claude

```bash
# After Claude writes the content:
/remove-ai-marks article.md    # Strip statistical text watermarks
/poc-hash article.md            # Log SHA-256 as proof of creation date
/poc-countries FR,US            # Get legal guidance for your target markets
```

### Scenario: You're a freelancer delivering to a client

```bash
# Before delivery:
/remove-ai-marks               # Clean all AI marks from deliverables
/poc-report                     # Generate IP-REPORT.md for your records
# → Keep IP-REPORT.md internally as proof you directed the creative work
# → Deliver clean files to client
```

---

## What each layer removes / protects

### watermarks-remover covers:

| Layer | What | How |
|-------|------|-----|
| A | Invisible Unicode (ZWSP, bidi, tag chars) | Deterministic Python scripts |
| B | Statistical token-sampling watermarks | LLM rewrite (best-effort) |
| Files | C2PA / EXIF / XMP / doc props | Format-specific cleaners |

### proof-of-creation covers:

| Layer | What | How |
|-------|------|-----|
| Headers | Copyright assertion in every file | Automatic injection on write |
| Hashes | SHA-256 proof-of-creation | Logged to `.proof-of-creation/hashes.log` |
| Legal | Jurisdiction-specific guidance | Context analysis + 15+ country DB |
| Alerts | GPL risk, GDPR, commercial flags | Automatic detection |

---

## Important: what watermark removal costs

From the watermarks-remover documentation:

> Text watermarks live in the wording itself. Removal means rewording, not
> restructuring. Any rewrite replaces the original word choices, which flattens
> tone, voice, and precision.

**Recommendation:** For high-quality content where voice matters, skip Layer B
(statistical rewrite) and use only Layer A (Unicode scrub) + file metadata
cleaning. Keep your original prose, protect it with proof-of-creation, and let the
SHA-256 hash document your creation date.

---

## The honest picture on AI copyright (2026)

- **EU**: Copyright is automatic from creation. The AI Act watermark does not
  negate your rights but adds a provenance layer. Document your creative direction.
- **USA**: Copyright requires human authorship. Keep records of your prompts,
  decisions, and iterations. USPTO does not grant copyright to purely AI-generated
  content.
- **UK/Canada/Australia**: Automatic protection, human authorship required.

The combination of both skills — cleaned provenance marks + documented creation
hashes — is your strongest practical position across all jurisdictions.

---

## Ecosystem acknowledgment

`proof-of-creation` is inspired by and complementary to
[guillaumemeyer/watermarks-remover](https://github.com/guillaumemeyer/watermarks-remover).
We encourage users to install both skills for complete coverage of the AI content
provenance lifecycle.

If you maintain a tool that integrates with either skill, open a PR to add it
to this section.

---

*© 2026 Lubansu Alphonse — proof-of-creation is MIT licensed.*
*watermarks-remover is MIT licensed by Guillaume Meyer and contributors.*
