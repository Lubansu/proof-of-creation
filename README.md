# proof-of-creation

<div align="center">

```
  ___ ____     ____                     _
 |_ _|  _ \   / ___|_   _  __ _ _ __ __| |
  | || |_) | | |  _| | | |/ _` | '__/ _` |
  | ||  __/  | |_| | |_| | (_| | | | (_| |
 |___|_|      \____|\__,_|\__,_|_|  \__,_|
```

**On-demand intellectual property protection for what you ask Claude to protect.**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-compatible-blueviolet)](https://claude.ai/code)
[![Skill version](https://img.shields.io/badge/skill-v1.0.0-green)]()
[![Jurisdictions](https://img.shields.io/badge/jurisdictions-15%2B-orange)]()

[English](#english) · [Français](#français)

</div>

---

## English

### What is proof-of-creation?

`proof-of-creation` is a Claude Code skill that protects the intellectual
property of files Claude creates or edits in your projects — on demand,
never as a silent side effect of a file write.

It runs in two layers, both on demand, kept deliberately separate:

**Base protection** — triggered by `/proof-of-creation`, `/poc-hash`, or an explicit request to protect a file:
- Injects a **copyright header** with your name, date, and license type
- Computes a **SHA-256 hash** as local proof of creation

**Deeper analysis, a further opt-in** — asked once per project after base protection runs, or triggered by `/poc-license`, `/poc-countries`, `/poc-register`:
- Analyzes the **legal context** of your project (commercial, open-source, cross-border)
- Suggests a **license** for your situation, with its legal source cited
- Alerts you when **formal registration** would be worth considering
- Provides **country-specific guidance** for 15+ jurisdictions
- Generates an **IP Report** summarizing your full protection status

Nothing happens on any file until you ask for it — not even the header and hash.

### Why does this exist?

Since August 2, 2026, Claude models embed mandatory EU AI Act watermarks in
generated content — meaning provenance tracking now works in both directions.
Creators need tools to assert *their* ownership alongside Anthropic's transparency
obligations.

This skill fills that gap: it turns every Claude Code session into a documented,
legally-aware creative act.

### Install

**Via Claude Code plugin marketplace (fastest):**
```
/plugin marketplace add Lubansu/proof-of-creation
/plugin install proof-of-creation@proof-of-creation
```

**Via installer script:**
```bash
# Personal install (all projects)
python3 install_skill.py --skill proof-of-creation --target claude-code

# Project install (commit to repo)
python3 install_skill.py --skill proof-of-creation --target claude-project \
  --project-dir /path/to/your/project
```

**Via Cowork / claude.ai:**
```bash
python3 install_skill.py --skill proof-of-creation --target cowork
# Then upload dist/proof-of-creation.zip under Customize → Skills
```

### Usage

The skill only activates when you ask — via a command, or an explicit request to protect a file or project:

| Command | Action |
|---------|--------|
| `/proof-of-creation` | Full protection check on current project |
| `/poc-report` | Generate `IP-REPORT.md` |
| `/poc-hash [file]` | SHA-256 hash + log for a specific file |
| `/poc-license` | Recommend and generate appropriate `LICENSE` |
| `/poc-countries [FR,US,UK]` | Legal requirements for specific countries |
| `/poc-register` | Step-by-step registration guide |

### Jurisdictions covered

| 🇫🇷 France | 🇪🇺 EU | 🇺🇸 USA | 🇬🇧 UK | 🇨🇦 Canada |
|-----------|-------|---------|--------|-----------|
| 🇩🇪 Germany | 🇧🇪 Belgium | 🇨🇭 Switzerland | 🇪🇸 Spain | 🇦🇺 Australia |
| 🇯🇵 Japan | 🇧🇷 Brazil | 🇮🇳 India | 🇸🇬 Singapore | 🌍 +more |

### What it does NOT do

- It does not file registrations automatically (human action required)
- It does not provide legal advice — consult a qualified IP attorney for
  high-value projects
- It does not guarantee protection in jurisdictions not listed

### Blockchain timestamping

Optional integration with:
- [Bernstein.io](https://bernstein.io) — EU/US/UK recognized, ~€10/deposit
- [OriginStamp](https://originstamp.com) — free tier, global
- [ANSA Protect](https://www.ansa.it) — France/EU focus

### Contributing

Contributions welcome. Priority needs:
- Additional jurisdiction coverage (Middle East, Southeast Asia, Africa)
- Integration with national IP office APIs
- Automated Enveloppe Soleau PDF generation

See [CONTRIBUTING.md](CONTRIBUTING.md).

### License

MIT — free to use, modify, and distribute. See [LICENSE](LICENSE).

### Disclaimer

This skill provides general legal information, not legal advice. Laws change.
Always consult a qualified attorney for projects with significant commercial value.

### Combined workflow with watermarks-remover

`proof-of-creation` is designed to work in sequence with
[guillaumemeyer/watermarks-remover](https://github.com/guillaumemeyer/watermarks-remover)
(⭐ 21k+), the leading skill for stripping AI provenance marks from files.

```
Create with Claude Code
        ↓
proof-of-creation: copyright header + SHA-256 hash (on demand)
        ↓
watermarks-remover: strip AI marks before distribution (on demand)
        ↓
/poc-report: verify full protection status
        ↓
/poc-register: formal deposit if commercial
```

Install both and run `/poc-workflow` for the guided combined experience.
See [WORKFLOW.md](WORKFLOW.md) for full documentation.

---

## Français

### Qu'est-ce que proof-of-creation ?

`proof-of-creation` est un skill Claude Code qui protège la propriété
intellectuelle des fichiers que Claude crée ou modifie dans vos projets —
sur demande, jamais comme effet de bord silencieux d'une écriture de fichier.

Il fonctionne en deux couches, toutes deux sur demande, volontairement séparées :

**Base de protection** — déclenchée par `/proof-of-creation`, `/poc-hash`, ou une demande explicite de protéger un fichier :
- Injecte un **header de copyright** avec votre nom, la date et le type de licence
- Calcule un **hash SHA-256** comme preuve locale de création

**Analyse approfondie, un opt-in supplémentaire** — proposée une fois par projet après la base de protection, ou déclenchée via `/poc-license`, `/poc-countries`, `/poc-register` :
- Analyse le **contexte légal** de votre projet (commercial, open-source, transfrontalier)
- Suggère une **licence** pour votre situation, avec sa base légale citée
- Vous alerte quand un **dépôt formel** mériterait d'être envisagé
- Fournit des **conseils spécifiques** pour plus de 15 juridictions
- Génère un **rapport IP** résumant votre statut de protection complet

Rien ne se déclenche sur aucun fichier tant que vous ne le demandez pas — pas même le header et le hash.

### Pourquoi ce projet existe-t-il ?

Depuis le 2 août 2026, les modèles Claude embarquent des watermarks obligatoires
liés à l'AI Act européen — ce qui signifie que le traçage de provenance fonctionne
désormais dans les deux sens. Les créateurs ont besoin d'outils pour faire valoir
*leur* propriété aux côtés des obligations de transparence d'Anthropic.

Ce skill comble ce manque : il transforme chaque session Claude Code en un acte
créatif documenté et juridiquement conscient.

### Installation

**Via le marketplace de plugins Claude Code :**
```
/plugin marketplace add Lubansu/proof-of-creation
/plugin install proof-of-creation@proof-of-creation
```

**Via le script d'installation :**
```bash
# Installation personnelle (tous vos projets)
python3 install_skill.py --skill proof-of-creation --target claude-code

# Installation projet (à commiter dans le dépôt)
python3 install_skill.py --skill proof-of-creation --target claude-project \
  --project-dir /chemin/vers/votre/projet
```

### Utilisation

Le skill ne s'active que sur demande — via une commande, ou une requête explicite pour protéger un fichier ou un projet :

| Commande | Action |
|----------|--------|
| `/proof-of-creation` | Vérification complète du projet en cours |
| `/poc-report` | Génère `IP-REPORT.md` |
| `/poc-hash [fichier]` | Hash SHA-256 + log pour un fichier spécifique |
| `/poc-license` | Recommande et génère le fichier `LICENSE` adapté |
| `/poc-countries [FR,US,UK]` | Exigences légales pour des pays spécifiques |
| `/poc-register` | Guide pas-à-pas pour l'enregistrement |

### Juridictions couvertes

Voir tableau ci-dessus (section anglaise). Documentation complète dans
[`skills/proof-of-creation/references/legal-by-country.md`](skills/proof-of-creation/references/legal-by-country.md).

### Ce que ce skill ne fait PAS

- Il n'effectue pas les dépôts automatiquement (action humaine requise)
- Il ne fournit pas de conseil juridique — consultez un avocat spécialisé PI
  pour les projets à forte valeur commerciale
- Il ne garantit pas la protection dans les juridictions non listées

### Contribuer

Les contributions sont bienvenues, notamment pour :
- Nouvelles juridictions (Moyen-Orient, Asie du Sud-Est, Afrique)
- Intégration avec les APIs des offices de PI nationaux
- Génération automatique du formulaire Enveloppe Soleau

### Licence

MIT — libre d'utilisation, modification et distribution. Voir [LICENSE](LICENSE).

### Avertissement

Ce skill fournit des informations juridiques générales, pas des conseils
juridiques. Les lois évoluent. Consultez toujours un avocat qualifié pour les
projets à forte valeur commerciale.

### Workflow combiné avec watermarks-remover

`proof-of-creation` est conçu pour fonctionner en séquence avec
[guillaumemeyer/watermarks-remover](https://github.com/guillaumemeyer/watermarks-remover)
(⭐ 21k+). Installez les deux et lancez `/poc-workflow` pour l'expérience guidée.
Voir [WORKFLOW.md](WORKFLOW.md) pour la documentation complète.
