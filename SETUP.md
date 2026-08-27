# Setup Guide

## Prerequisites

- Python 3.9+
- pip
- Git

## Local Development

### 1. Clone the repository

```bash
git clone https://github.com/mamadbypass/security-reference.git
cd security-reference
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Serve locally

```bash
mkdocs serve
```

Visit http://127.0.0.1:8000

### 4. Build for production

```bash
mkdocs build --strict
```

Output is written to `site/`.

## Regenerating Topic Pages

Topic pages are generated from `scripts/generate_docs.py`:

```bash
python3 scripts/generate_docs.py
```

Edit the `STRUCTURE` dictionary in that script to add new topics, then regenerate.

## GitHub Pages Deployment

Deployment is automated via `.github/workflows/deploy.yml`:

1. Push to `main`
2. GitHub Actions builds the site with MkDocs Material
3. Site is published to `gh-pages` branch
4. Available at https://mamadbypass.github.io/security-reference/

### Manual deployment

```bash
mkdocs gh-deploy --force
```

## Project Structure

```
security-reference/
├── docs/                    # Markdown content
│   ├── index.md             # Home page
│   ├── MASTER_CHECKLIST.md  # Engagement checklist
│   ├── TOOLS_INDEX.md       # Tools reference
│   ├── bug-bounty/          # Recon and enumeration
│   ├── web/                 # Web vulnerabilities
│   ├── api/                 # API security
│   ├── authentication/      # Auth testing
│   ├── mobile/              # Mobile security
│   ├── network/             # AD and network pentest
│   ├── blue-team/           # Defensive security
│   ├── cloud/               # Cloud security
│   └── ...                  # Additional sections
├── scripts/
│   └── generate_docs.py     # Page generator
├── mkdocs.yml               # MkDocs configuration
├── requirements.txt         # Python dependencies
└── .github/workflows/
    └── deploy.yml           # CI/CD pipeline
```

## Customization

### Theme

Edit `mkdocs.yml` to change colors, features, and navigation. The site uses [MkDocs Material](https://squidfunk.github.io/mkdocs-material/).

### Custom CSS

Add styles to `docs/stylesheets/extra.css`.

### Adding a new section

1. Add entries to `STRUCTURE` in `scripts/generate_docs.py`
2. Run `python3 scripts/generate_docs.py`
3. Add navigation entries to `mkdocs.yml`
4. Run `mkdocs build --strict` to verify

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `mkdocs: command not found` | Run `pip install -r requirements.txt` |
| Build warnings | Run `mkdocs build --strict` to see all issues |
| Missing pages in nav | Add file path to `nav` section in `mkdocs.yml` |
| Search not working | Ensure `plugins: [search]` is in `mkdocs.yml` |
