# 🛠️ Utvikler-guide / Developer Guide

Denne guiden er for utviklere som bidrar til slektstre-prosjektet.

This guide is for developers contributing to the slektstre project.

## 🇳🇴 Norsk

### Google Colab Development

Når du legger til nye features:

#### Testing i Colab
1. **Test lokalt først** - Sørg for at koden fungerer i lokal Jupyter
2. **Legg til Colab-kompatibilitet** - Inkluder Colab setup-celle i alle notebooks
3. **Test i faktisk Colab-miljø** - Åpne notebook via Colab-badge og test
4. **Oppdater Colab-badge lenker** - Sørg for at badges i README peker til riktige notebooks

#### Colab Setup-celle Template
```python
# =============================================================================
# GOOGLE COLAB SETUP / GOOGLE COLAB SETUP
# =============================================================================

# Sjekk om vi kjører i Google Colab
try:
    import google.colab
    IN_COLAB = True
    print("🔧 Kjører i Google Colab - installerer avhengigheter...")
    print("🔧 Running in Google Colab - installing dependencies...")
    
    # Installer nødvendige pakker
    %pip install -q networkx matplotlib plotly pydantic pyyaml pandas ipywidgets pillow kaleido
    
    # Klon repository
    %git clone https://github.com/arvidl/slektstre.git
    import sys
    sys.path.append('/content/slektstre/src')
    
except ImportError:
    IN_COLAB = False
    print("💻 Kjører lokalt / Running locally")
    import sys
    sys.path.append('../src')

print(f"📍 Miljø: {'Google Colab' if IN_COLAB else 'Lokal'}")
print(f"📍 Environment: {'Google Colab' if IN_COLAB else 'Local'}")
```

#### Colab Badge Format
```markdown
[![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/arvidl/slektstre/blob/main/notebooks/NOTEBOOK_NAME.ipynb)
```

#### Vanlige Colab-problemer
- **Import-feil**: Sjekk at `sys.path.append()` er korrekt
- **Pakke-installasjon**: Bruk `%pip install` ikke `!pip install`
- **Fil-tilgang**: Colab har `/content/` som root, ikke `../`
- **Visualiseringer**: Test at matplotlib/plotly fungerer i Colab

### Repository-vedlikehold

#### Store filer i Git (>100MB)

Hvis du får feil om store filer som overskrider GitHub's 100MB grense:

```bash
# Installer git-filter-repo
pip install git-filter-repo

# Fjern problematisk fil fra hele Git-historikken
git filter-repo --path problematic_file.ipynb --invert-paths --force

# Legg til origin remote på nytt
git remote add origin git@github.com:arvidl/slektstre.git

# Force push for å overskrive remote historikk
git push origin main --force
```

#### Rydde opp i Jupyter Notebook outputs

Hvis notebook-filer blir for store på grunn av output-data:

```bash
# Rydde opp i enkelt notebook
jupyter nbconvert --clear-output --inplace notebooks/notebook.ipynb

# Rydde opp i alle notebooks
find notebooks/ -name "*.ipynb" -exec jupyter nbconvert --clear-output --inplace {} \;
```

#### .gitignore for store filer

Følgende filtyper er ekskludert fra Git:

```gitignore
# Audio files (too large for Git)
*.mp3
*.m4a
*.wav
*.aac
*.ogg

# Large data files
*.zip
*.tar.gz
*.rar
```

### Utviklingsmiljø

#### Oppsett av utviklingsmiljø

```bash
# Klon repository
git clone https://github.com/arvidl/slektstre.git
cd slektstre

# Opprett conda-miljø
conda env create -f environment.yml
conda activate slektstre

# Installer utviklingsverktøy
pip install git-filter-repo
```

#### Testing

```bash
# Valider notebooks
python scripts/validate_book.py

# Test bok-generering
make book

# Test automatisk overvåkning
make watch
```

### Bidrag til prosjektet

#### Git-workflow

1. **Lag en branch** for din feature
2. **Gjør endringer** og test grundig
3. **Rydd opp** i store filer før commit
4. **Lag pull request** med beskrivelse

#### Kode-standarder

- **Bruk type hints** for alle funksjoner
- **Dokumenter funksjoner** med docstrings
- **Følg PEP 8** for Python-kode
- **Test endringer** før commit

## 🇬🇧 English

### Repository Maintenance

#### Large files in Git (>100MB)

If you get errors about large files exceeding GitHub's 100MB limit:

```bash
# Install git-filter-repo
pip install git-filter-repo

# Remove problematic file from entire Git history
git filter-repo --path problematic_file.ipynb --invert-paths --force

# Re-add origin remote
git remote add origin git@github.com:arvidl/slektstre.git

# Force push to overwrite remote history
git push origin main --force
```

#### Cleaning Jupyter Notebook outputs

If notebook files become too large due to output data:

```bash
# Clean single notebook
jupyter nbconvert --clear-output --inplace notebooks/notebook.ipynb

# Clean all notebooks
find notebooks/ -name "*.ipynb" -exec jupyter nbconvert --clear-output --inplace {} \;
```

#### .gitignore for large files

The following file types are excluded from Git:

```gitignore
# Audio files (too large for Git)
*.mp3
*.m4a
*.wav
*.aac
*.ogg

# Large data files
*.zip
*.tar.gz
*.rar
```

### Development Environment

#### Setting up development environment

```bash
# Clone repository
git clone https://github.com/arvidl/slektstre.git
cd slektstre

# Create conda environment
conda env create -f environment.yml
conda activate slektstre

# Install development tools
pip install git-filter-repo
```

#### Testing

```bash
# Validate notebooks
python scripts/validate_book.py

# Test book generation
make book

# Test automatic monitoring
make watch
```

### Contributing to the project

#### Git workflow

1. **Create a branch** for your feature
2. **Make changes** and test thoroughly
3. **Clean up** large files before commit
4. **Create pull request** with description

#### Code standards

- **Use type hints** for all functions
- **Document functions** with docstrings
- **Follow PEP 8** for Python code
- **Test changes** before commit

## 📚 Relaterte dokumenter / Related Documents

- [README.md](README.md) - Hoveddokumentasjon / Main documentation
- [BOK-REDIGERING.md](BOK-REDIGERING.md) - Bok-redigering / Book editing
- [PODCAST.md](PODCAST.md) - Podcast-instruksjoner / Podcast instructions
