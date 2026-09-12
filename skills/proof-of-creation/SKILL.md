---
name: proof-of-creation
description: >
  Sets up intellectual-property protection — a copyright header and a
  SHA-256 proof-of-creation hash, logged locally — on files the user asks
  to protect. Nothing runs automatically just because Claude writes or
  edits a file: base protection itself is on demand, triggered by an
  explicit command (/proof-of-creation, /poc-hash) or an explicit request
  to protect/hash/add copyright to a file or project. Deeper analysis
  (project context detection, license suggestion, jurisdiction-specific
  legal alerts, registration guidance) is a further, separate opt-in on top
  of that — it only runs after the user says yes to the one-time
  per-project prompt, or invokes /poc-license, /poc-countries, or
  /poc-register directly. Every piece of legal guidance is presented with
  its statutory source (e.g. Art. L111-1 CPI, 17 U.S.C. §102) and a
  disclaimer — it is decision support, not legal advice.
  Trigger only on an explicit command or an explicit user request naming
  copyright, license, IP, protection, hashing, or Proof of Creation —
  never as a side effect of a file write.
license: MIT
compatibility:
  claude-code: ">=1.0"
metadata:
  author: "Lubansu Alphonse"
  version: "1.1.0"
  tags: ["copyright", "ip", "license", "legal", "protection", "watermark"]
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
---

# Proof of Creation — Intellectual Property Protection Skill

## Purpose

This skill runs in two layers, both on demand, kept deliberately separate:

1. **Base protection (on demand)** — a copyright header and a SHA-256
   proof-of-creation hash, logged locally. Mechanical and deterministic: no
   legal judgment, no interpretation, nothing to get wrong — but it still
   only runs when asked for, never as a silent side effect of writing a
   file.
2. **Deeper analysis (a further, separate opt-in)** — context detection,
   license suggestion, jurisdiction-specific alerts, registration guidance.
   This layer never runs by itself. It only runs once the user has
   explicitly agreed to it, and every claim it makes is tied back to its
   legal source in [Legal reference by country](#legal-reference-by-country)
   — it is decision support, not legal advice.

---

## Trigger conditions

### Base protection — on demand, not automatic

Do **not** inject a header or compute a hash just because Claude writes or
edits a file. Only do it when:

- The user explicitly invokes `/proof-of-creation` or `/poc-hash [file]`, or
- The user explicitly asks to protect, hash, timestamp, or add copyright to
  a file or the current project.

If neither has happened, write the file normally with no header and no log
entry.

### Deeper analysis — a further opt-in, on top of base protection

Do **not** run context analysis, license suggestion, or legal alerts
automatically, and do not run them just because base protection ran. Only
run them when:

- The user answered "yes" to the one-time per-project prompt (Step 3
  below), or
- The user explicitly invokes `/poc-license`, `/poc-countries`, or
  `/poc-register`, or
- The user directly asks something like "how do I protect this?", "is this
  mine?", "can someone copy this?", or names copyright / license / IP /
  dépôt / INPI / GDPR themselves.

A `package.json`, `pyproject.toml`, or `composer.json` missing a `license`
field is, at most, something to mention if the user has already asked for
base protection or deeper analysis on that project — it is never itself a
reason to activate anything unasked.

---

## Behavior when invoked

Everything below only runs once one of the [Base protection trigger
conditions](#base-protection--on-demand-not-automatic) above has actually
been met — a command or an explicit request. If the user asked to protect
one specific file, apply Steps 1–2 to that file only. If they asked to
protect "this project" or ran `/proof-of-creation`, apply them to the
project's files as agreed with the user (e.g. everything since the last
run, or everything matching a pattern they specify) — don't silently expand
scope to files they didn't ask about.

### Step 1 — Inject copyright header

Add at the top of the file, adapted to the file type:

**For code files (.js, .ts, .py, .php, .java, .go, .rs…)**
```
/**
 * © [YEAR] Lubansu Alphonse — All rights reserved.
 * Created: [ISO DATE]
 * File: [FILENAME]
 * SHA-256: [HASH — filled after write]
 * License: [LICENSE TYPE, or "unset" if the user hasn't chosen one yet]
 * Protected under: [JURISDICTION, or "unset" if not yet discussed]
 */
```

**For HTML files**
```html
<!-- © [YEAR] Lubansu Alphonse — All rights reserved | License: [LICENSE] -->
```

**For Markdown / text files**
```
<!-- proof-of-creation: © [YEAR] Lubansu Alphonse | [ISO DATE] | [LICENSE] -->
```

If the user has not provided their name, ask once and store it for the
session. Do not block on license/jurisdiction — leave them as "unset" until
the user opts into deeper analysis (Step 3).

---

### Step 2 — Compute SHA-256 hash

After protecting the file, compute its SHA-256 hash using:

```bash
sha256sum [FILENAME]
# or on macOS:
shasum -a 256 [FILENAME]
```

Append the result to `.proof-of-creation/hashes.log` in this format:

```
[ISO DATETIME] | [FILENAME] | [SHA256] | [LICENSE] | [JURISDICTION]
```

This file is the local proof-of-creation log. Advise the user to commit it
to Git immediately — the commit timestamp becomes an additional layer of
proof.

---

### Step 3 — Offer deeper analysis (once per project, not per file)

The first time Base protection is invoked in a given project — i.e.
`.proof-of-creation/hashes.log` did not exist before this run — ask, once:

> "Base de protection posée pour ce projet (header + hash SHA-256). Voulez-
> vous une analyse du contexte (licence, alertes commercial/GPL/GDPR, guide
> par juridiction) ? [oui/non]"

- **No, or no answer:** stop here. Don't ask again this session. Base
  protection still only runs the next time the user explicitly asks for it
  or invokes a command — it does not become automatic.
- **Yes:** run [Deeper analysis](#deeper-analysis-opt-in) once. After that,
  don't re-run it automatically — later requests go through
  `/poc-license`, `/poc-countries`, or `/poc-register` instead.

---

## Deeper analysis (opt-in)

Everything in this section only runs per the [Trigger conditions](#trigger-conditions-1)
above — never as a side effect of writing a file.

### Context analysis

Ask or infer from context:

| Question | Inferred from |
|----------|--------------|
| Is this project commercial? | `package.json` name, pricing mentions, "app", "SaaS" |
| Target jurisdiction? | User language, mentions of country, hosting location |
| Open-source or proprietary? | Existing LICENSE file, repo visibility |
| Contains personal data (GDPR)? | Database models, user tables, auth code |
| Dependencies with restrictive licenses? | `node_modules`, `requirements.txt`, `Cargo.toml` |

State inferences as inferences ("this looks commercial because...") and let
the user correct them — don't treat a guess as a fact for the rest of the
analysis.

### License suggestion (referenced, not prescriptive)

Present options with why teams pick them and where the underlying legal
protection comes from — never as a bare imperative like "you should use
MIT":

| Project type | Common choice | Why teams pick it | Legal basis for the underlying protection |
|-------------|-------------------|--------|--------|
| Commercial SaaS | Proprietary / All Rights Reserved | Keeps full control | Automatic on creation — see the user's country in [Legal reference by country](#legal-reference-by-country) |
| Open-source, permissive | MIT | Maximum adoption, no copyleft | OSI-approved license text |
| Open-source, protective | AGPL-3.0 | Forces derivatives to stay open | OSI-approved, network copyleft |
| Library / SDK | Apache-2.0 | Includes an explicit patent grant | OSI-approved license text |
| Creative content | CC BY-NC-ND 4.0 | Blocks commercial reuse | Creative Commons license text |
| Internal tool | Proprietary | No external sharing | N/A |

Always say plainly: *"This is a common pattern for this project type, not a
recommendation tailored to your situation — verify with an attorney before
committing to a license where the commercial stakes are real."* Generate the
`LICENSE` file only after the user confirms which option they actually want.

### Legal alert (contextual, source-cited)

When surfacing an alert, name the legal basis instead of asserting a flat
conclusion:

| Situation | What to say |
|-----------|-------------|
| Commercial project, no registration | "Your protection exists automatically from creation (see your country's entry in Legal reference). Formal registration isn't required for that protection to exist, but several jurisdictions tie it to what you can claim in court — see the specific entry before deciding." |
| GPL dependency in proprietary project | "A GPL-licensed dependency was detected. Depending on the GPL version and how you link/distribute, this can require releasing your own code under GPL too — read the dependency's actual license file, this is not a substitute for that." |
| Personal data in code | "EU user data handling was detected. GDPR may require a documented lawful basis and, depending on scale, a DPO — see the GDPR note under your country's entry." |
| AI-generated content (post Aug 2026) | "This model embeds an EU AI Act watermark on generated content since Aug 2, 2026. It's a provenance mark, not a copyright claim against you — keep a record of your own creative direction (prompts, edits, decisions) regardless." |
| Cross-border distribution | "Distribution across multiple jurisdictions was detected — protection terms differ by country (see Legal reference by country); when in doubt, the strictest applicable jurisdiction is the safer assumption." |

---

## Legal reference by country

### 🇫🇷 France

**Automatic protection:** Yes — from the moment of creation (Code de la Propriété
Intellectuelle, Art. L111-1). No registration required for the right to exist.

**Recommended deposit for proof:**
- **Enveloppe Soleau** (INPI) — €15 — valid 5 years, renewable. Simple, fast,
  recognized by French courts. Best for individuals.
- **Dépôt APP** (Agence pour la Protection des Programmes) — €50–€150 —
  specialized in software, stronger evidentiary value.
- **Notaire** — €100–€300 — maximum legal weight.

**Coverage:** Life of author + 70 years.

**For commercial projects:** Register with INPI at inpi.fr. Mention
"Logiciel" as the creation type.

**GDPR note:** If the app processes EU user data, a CNIL declaration or DPO
appointment may be required regardless of company size.

---

### 🇪🇺 European Union (general)

**Automatic protection:** Yes — EU Directive 2009/24/EC protects software
automatically upon creation across all member states.

**EU AI Act (2026):** Content generated by AI models released after August 2,
2026 carries mandatory machine-readable watermarks. This does not negate your
copyright but adds a provenance layer. Keep your original prompts and iteration
history as proof of creative direction.

**Recommended deposit:** National IP office of your country + optional EUIPO
registration for trademarks (not copyright, which is automatic).

**Coverage:** Life + 70 years across all 27 member states.

---

### 🇺🇸 United States

**Automatic protection:** Yes — from creation (17 U.S.C. § 102). However,
**registration is required to sue for statutory damages and attorney's fees.**

**Recommended deposit:**
- **Copyright.gov** — $65 (single work online) — strongly recommended for any
  commercial project. Processing time: 3–11 months, but protection is retroactive
  to filing date.

**Coverage:** Life + 70 years (individual) / 95 years from publication (corporate).

**Important:** For software sold or licensed in the US, register before or within
3 months of publication to preserve full legal remedies.

**AI-generated content:** As of 2026, the USPTO does not grant copyright to
purely AI-generated content. Human creative input must be documented.

---

### 🇬🇧 United Kingdom

**Automatic protection:** Yes — Copyright, Designs and Patents Act 1988. No
registration system for copyright exists in the UK.

**Recommended approach:**
- Use a **timestamped deposit service** (e.g., UK Copyright Service — free to
  £70/year for full service)
- Keep Git commit history as evidence
- Consider **UK IPO** for trademarks if branding is involved

**Coverage:** Life + 70 years.

**Post-Brexit note:** EU copyright directives no longer apply automatically in the
UK, but the protection level is equivalent.

---

### 🇨🇦 Canada

**Automatic protection:** Yes — Copyright Act (R.S.C., 1985, c. C-42). No
registration required.

**Recommended deposit:**
- **CIPO** (Canadian Intellectual Property Office) — registration is optional but
  creates a public record. Free to file, ~$50 for formal certificate.

**Coverage:** Life + 70 years (since 2022 amendment).

---

### 🌍 Other jurisdictions (summary)

| Country | Auto protection | Registration | Approx. cost |
|---------|----------------|-------------|-------------|
| Germany | Yes | DPMA (optional) | Free–€90 |
| Spain | Yes | OEPM | €17–€100 |
| Belgium | Yes | Optional notarial | €50–€200 |
| Switzerland | Yes | IGE/IPI | CHF 200+ |
| Australia | Yes | IP Australia | AUD 0–200 |
| Japan | Yes | JPO | ¥12,000+ |
| Brazil | Yes | INPI-BR | R$80+ |
| India | Yes | Copyright Office | ₹500–2000 |

---

## Blockchain timestamping (optional, on request)

For maximum cross-border proof, optionally timestamp the SHA-256 hash on a
public blockchain. Only bring this up inside Deeper analysis, or when the
user asks directly — never automatically. Services that provide
legally-recognized timestamps:

| Service | Cost | Jurisdiction recognized | Notes |
|---------|------|------------------------|-------|
| **Bernstein.io** | ~€10/deposit | EU, US, UK | Best for businesses |
| **OriginStamp** | Free tier | Global | Basic but usable |
| **ANSA Protect** | ~€5/deposit | France, EU | French press agency backing |
| **Notarius** | Varies | Canada, US | Notarial weight |

Worth mentioning when, during Deeper analysis, the project turns out to be:
- Commercial
- Distributed internationally
- Run by a freelancer or small studio without a legal department

---

## IP Report generation

When the user asks for a report, or when `/poc-report` is invoked, generate
`IP-REPORT.md` at the project root:

```markdown
# IP Protection Report
Generated: [DATE]
Project: [NAME]

## Protected files
| File | Created | SHA-256 | License |
|------|---------|---------|---------|
| ... | ... | ... | ... |

## Legal status
- Jurisdiction: [DETECTED, or "not analyzed — deeper analysis was declined"]
- Automatic protection: Active since [FIRST COMMIT DATE]
- Formal registration: [DONE / RECOMMENDED / NOT DONE / NOT ANALYZED]

## Recommendations
(Only include this section if Deeper analysis has run for this project.)
- [ ] File Enveloppe Soleau (INPI) — €15
- [ ] Register at Copyright.gov — $65
- [ ] Blockchain timestamp via Bernstein.io
- [ ] Add LICENSE file
- [ ] Add NOTICE file with third-party attributions

## Dependency license audit
(Only include this section if Deeper analysis has run for this project.)
| Package | License | Risk |
|---------|---------|------|
| ... | ... | ... |
```

If Deeper analysis was never run for this project, the report should still
be useful on its own — files, hashes, dates — and should say plainly that
the legal/recommendation sections were skipped because the user hadn't
opted in, with a one-line reminder of how to opt in (`/poc-license` etc.).

---

## Commands

| Command | Action |
|---------|--------|
| `/proof-of-creation` | Run base protection (header + hash) on the current project, and offer to opt into Deeper analysis |
| `/poc-report` | Generate IP-REPORT.md |
| `/poc-hash [file]` | Compute and log SHA-256 for a specific file |
| `/poc-license` | Run the license-suggestion part of Deeper analysis and generate LICENSE |
| `/poc-countries` | Show legal requirements for specified countries (no opt-in needed — pure reference lookup) |
| `/poc-register` | Step-by-step registration guide for detected jurisdiction |
| `/poc-workflow` | Guide through combined watermarks-remover + proof-of-creation workflow |

---

## Integration with watermarks-remover

This skill is designed to work in sequence with
[guillaumemeyer/watermarks-remover](https://github.com/guillaumemeyer/watermarks-remover).

### Recommended combined workflow

When both skills are installed, suggest this sequence — both steps are on
demand, run in this order when the user is ready:

1. **proof-of-creation runs first** (`/proof-of-creation`, on demand) —
   copyright header + SHA-256 hash logged, before any modification
2. **watermarks-remover runs second** (on demand) — strips AI provenance
   marks (Unicode, statistical, C2PA/EXIF) for distribution or publication
3. **ip-report confirms** — verifies final protection status

### `/poc-workflow` command behavior

When the user invokes `/poc-workflow`, check if watermarks-remover is installed:

**If watermarks-remover IS installed:**
```
🛡️ IP Workflow — Lubansu Alphonse

Step 1 ✅ proof-of-creation: base protection applied — copyright headers and SHA-256 hashes now logged for this project.

Step 2: Strip AI provenance marks for distribution?
  Run: /remove-ai-marks
  This cleans Unicode invisible characters and file metadata.
  Note: Layer B (text rewrite) will change wording — skip if voice matters.

Step 3: After cleaning, run /poc-report for your final protection summary.

Step 4: Ready to distribute? Run /poc-register for formal deposit guidance.
```

**If watermarks-remover is NOT installed:**
```
🛡️ IP Workflow — Lubansu Alphonse

Step 1 ✅ proof-of-creation: base protection applied — copyright headers and SHA-256 hashes now logged for this project.

Step 2 (optional): To also strip AI provenance marks before distribution,
  install the complementary skill:
  /plugin marketplace add guillaumemeyer/watermarks-remover
  /plugin install watermarks-remover@watermarks-remover
  See: WORKFLOW.md for the complete combined workflow.

Step 3: Run /poc-report for your protection summary.
Step 4: Run /poc-register for formal deposit guidance.
```

### Why this pairing matters

Since August 2, 2026, Claude models embed mandatory EU AI Act watermarks.
The two skills address opposite but complementary needs:
- **watermarks-remover**: strips AI fingerprints for privacy and hygiene
- **proof-of-creation**: asserts creator ownership for legal protection

Neither alone covers the full creator IP lifecycle.

---

## Important disclaimer

This skill provides general legal information, not legal advice. For projects
with significant commercial value, consult a qualified IP attorney in your
jurisdiction. Laws change — always verify current requirements.
