# 📚 Bok-redigering og kapittelhåndtering

Denne guideen forklarer hvordan du kan redigere, oppdatere og administrere PDF-boken for slektstre-prosjektet.

## 🎯 Oversikt

PDF-boken genereres automatisk fra:
- **README.md** - Introduksjonskapittel
- **notebooks/*.ipynb** - Alle Jupyter notebooks som separate kapitler

## 🚀 Rask oppdatering

### Automatisk regenerering av boken

```bash
# Regenerer hele boken
make book

# Eller manuelt
jupyter nbconvert --to webpdf notebooks/*.ipynb --output-dir=book_pdf
python scripts/combine_pdfs.py
```

## 📝 Legge til et nytt kapittel

### Steg 1: Opprett ny notebook

```bash
# Opprett ny notebook i notebooks/ mappen
touch notebooks/06_nytt_kapittel.ipynb

# Eller bruk Jupyter
jupyter notebook notebooks/
```

### Steg 2: Følg notebook-konvensjoner

Sørg for at den nye notebooken følger samme struktur som eksisterende:

```python
# Importer nødvendige biblioteker
import sys
sys.path.append('../src')

from models import Person, Gender
from tree import Slektstre
# ... andre imports

print("✅ Biblioteker importert!")
```

### Steg 3: Legg til i bok-struktur

Oppdater `scripts/combine_pdfs.py` for å inkludere det nye kapitlet:

```python
# I combine_pdfs.py, legg til i pdf_files listen:
pdf_files = [
    "book_pdf/README.pdf",
    "book_pdf/00_slektstraer_og_grafer.pdf",
    "book_pdf/01_introduksjon.pdf", 
    "book_pdf/02_bygg_tre_manuelt.pdf",
    "book_pdf/03_importer_data.pdf",
    "book_pdf/04_visualisering.pdf",
    "book_pdf/05_eksterne_databaser.pdf",
    "book_pdf/06_nytt_kapittel.pdf"  # ← Nytt kapittel
]
```

### Steg 4: Regenerer boken

```bash
make book
```

## 🔄 Automatisk oppdatering ved endringer

### Metode 1: File watcher (anbefalt)

Opprett et script som overvåker endringer:

```bash
# Installer file watcher
pip install watchdog

# Kjør overvåkingsscript
python scripts/watch_and_rebuild.py
```

### Metode 2: Git hooks

Opprett en pre-commit hook som regenererer boken:

```bash
# .git/hooks/pre-commit
#!/bin/bash
echo "🔄 Regenererer PDF-bok..."
make book
git add book_pdf/
```

### Metode 3: CI/CD pipeline

For automatisk oppdatering på GitHub:

```yaml
# .github/workflows/update-book.yml
name: Update Book
on:
  push:
    paths:
      - 'notebooks/**'
      - 'README.md'
jobs:
  update-book:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Setup Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.12'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Generate book
        run: make book
      - name: Commit changes
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add book_pdf/
          git commit -m "Auto-update book" || exit 0
          git push
```

## 🛠️ Avanserte redigeringsoperasjoner

### Endre kapitelrekkefølge

Rediger `scripts/combine_pdfs.py` og endre rekkefølgen i `pdf_files` listen:

```python
pdf_files = [
    "book_pdf/README.pdf",
    "book_pdf/00_slektstraer_og_grafer.pdf",
    "book_pdf/02_bygg_tre_manuelt.pdf",  # Flyttet opp
    "book_pdf/01_introduksjon.pdf",      # Flyttet ned
    # ... resten
]
```

### Fjerne et kapittel

1. Fjern notebook-filen: `rm notebooks/kapittel.ipynb`
2. Fjern fra `combine_pdfs.py`
3. Regenerer: `make book`

### Splitte et kapittel

1. Kopier eksisterende notebook: `cp notebooks/01_introduksjon.ipynb notebooks/01a_del1.ipynb`
2. Rediger begge filer
3. Oppdater `combine_pdfs.py`
4. Regenerer boken

### Legge til metadata

For bedre bok-organisering, legg til metadata i notebook-celler:

```python
# I første celle av notebook
{
 "cell_type": "markdown",
 "metadata": {
  "book_title": "Kapittel 6: Avansert analyse",
  "book_author": "Ditt navn",
  "book_date": "2024-01-01"
 },
 "source": ["# Kapittel 6: Avansert analyse"]
}
```

## 📊 Kvalitetskontroll

### Automatisk validering

Opprett et valideringsscript:

```python
# scripts/validate_book.py
import os
from pathlib import Path

def validate_notebooks():
    """Valider at alle notebooks er gyldige."""
    notebook_dir = Path("notebooks")
    
    for notebook in notebook_dir.glob("*.ipynb"):
        print(f"Validerer {notebook.name}...")
        # Kjør notebook validering
        os.system(f"jupyter nbconvert --to notebook --execute {notebook} --output /dev/null")
        print(f"✅ {notebook.name} er gyldig")

def check_pdf_sizes():
    """Sjekk at alle PDF-er er generert og har rimelig størrelse."""
    book_dir = Path("book_pdf")
    
    for pdf in book_dir.glob("*.pdf"):
        size_mb = pdf.stat().st_size / (1024 * 1024)
        if size_mb < 0.1:  # Mindre enn 100KB
            print(f"⚠️  {pdf.name} er for liten ({size_mb:.1f}MB)")
        else:
            print(f"✅ {pdf.name} er OK ({size_mb:.1f}MB)")

if __name__ == "__main__":
    validate_notebooks()
    check_pdf_sizes()
```

### Kjør validering

```bash
python scripts/validate_book.py
```

## 🔧 Feilsøking

### Vanlige problemer

#### 1. Notebook kjører ikke
```bash
# Sjekk at alle imports fungerer
python -c "import sys; sys.path.append('src'); from models import Person"

# Kjør notebook manuelt
jupyter nbconvert --to notebook --execute notebooks/problem.ipynb
```

#### 2. PDF genereres ikke
```bash
# Sjekk Playwright
playwright install

# Test nbconvert
jupyter nbconvert --to webpdf notebooks/00_slektstraer_og_grafer.ipynb
```

#### 3. Større PDF-filer
```bash
# Komprimer eksisterende PDF-er
gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/ebook -o compressed.pdf input.pdf
```

#### 4. Manglende avhengigheter
```bash
# Reinstaller alt
pip install -r requirements.txt
playwright install
```

## 📈 Optimalisering

### Redusere PDF-størrelse

1. **Komprimer bilder** i notebooks
2. **Fjern unødvendige output** fra celler
3. **Bruk mindre font-størrelser** i visualiseringer

### Raskere generering

1. **Parallell konvertering**:
```python
# scripts/parallel_convert.py
import concurrent.futures
import subprocess

def convert_notebook(notebook):
    subprocess.run([
        "jupyter", "nbconvert", "--to", "webpdf", 
        f"notebooks/{notebook}", "--output-dir=book_pdf"
    ])

with concurrent.futures.ThreadPoolExecutor() as executor:
    notebooks = ["00_slektstraer_og_grafer.ipynb", "01_introduksjon.ipynb", ...]
    executor.map(convert_notebook, notebooks)
```

2. **Caching** av konverterte filer
3. **Inkrementell oppdatering** (kun endrede filer)

## 🎨 Tilpasning

### Endre bok-stil

Rediger `_config.yml`:

```yaml
# Tilpass bok-utseende
html:
  theme:
    primary: "blue"
    accent: "light-blue"
  favicon: "assets/favicon.ico"
  logo: "assets/logo.png"

# PDF-spesifikke innstillinger
sphinx:
  config:
    latex_elements:
      fontpkg: "\\usepackage{libertinus}"
      geometry: "\\geometry{letterpaper,margin=1in}"
```

### Legge til forside

Opprett `book_pdf/forside.pdf` og inkluder den først i `combine_pdfs.py`.

### Tilpasse kapiteloverskrifter

Rediger notebook-celler for å inkludere kapitelnummer:

```markdown
# Kapittel 6: Avansert slektsanalyse

Dette kapittelet dekker...
```

## 📋 Vedlikeholdsrutiner

### Daglig
- Sjekk at `make book` fungerer
- Valider nye notebooks

### Ukentlig  
- Oppdater avhengigheter
- Test på forskjellige plattformer

### Månedlig
- Gjennomgå bok-struktur
- Optimaliser PDF-størrelser
- Oppdater dokumentasjon

## 🆘 Hjelp og støtte

### Debugging
```bash
# Aktiver debug-modus
export JUPYTER_LOG_LEVEL=DEBUG
make book

# Sjekk loggfiler
tail -f ~/.jupyter/jupyter.log
```

### Backup
```bash
# Lag backup av genererte bøker
tar -czf book_backup_$(date +%Y%m%d).tar.gz book_pdf/
```

### Gjenoppretting
```bash
# Gjenopprett fra backup
tar -xzf book_backup_20240101.tar.gz
```

---

## 📞 Kontakt

For spørsmål om bok-redigering, opprett en issue på GitHub eller kontakt prosjektet vedlikeholder.

**Husk**: Alltid test endringer lokalt før du pusher til hovedrepository!
