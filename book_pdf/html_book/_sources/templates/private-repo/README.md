# Min Slektstre (Private) / My Family Tree (Private)

Private repository for family data and personal genealogy research.

**⚠️ VIKTIG / IMPORTANT**: Dette er et privat repository. Del aldri reelle familie-data offentlig! / This is a private repository. Never share real family data publicly!

---

## 🇳🇴 Norsk

### Oppsett

1. **Installer slektstre-pakken**:
   ```bash
   pip install git+https://github.com/arvidl/slektstre.git
   ```

2. **Legg til dine datafiler** i `data/`-mappen

3. **Aldri commit sensitive data** til offentlige repos!

### Datastruktur

```
slektstre-privat/
├── data/
│   ├── familie.yaml          # Hovedfamilie-data
│   ├── historiske_dokumenter/ # Kildedokumenter
│   └── bilder/               # Familiebilder
├── notebooks/
│   └── min_slektsanalyse.ipynb # Dine analyser
├── .gitignore                 # Viktig: beskytter sensitive filer
└── requirements.txt           # Avhengigheter
```

### Datafiler

- **familie.yaml** - Hovedslektstreet i YAML-format
- **historiske_dokumenter/** - Scannede dokumenter, fødselsattester, etc.
- **bilder/** - Familiebilder (organiser per person/hendelse)
- **notater/** - Forskningsnotater og kilder

### Viktige Regler

1. ✅ **Bruk private repository** på GitHub
2. ✅ **Verifiser .gitignore** før hver commit
3. ✅ **Ta regelmessige backups** (encrypted)
4. ✅ **Få samtykke** fra levende personer
5. ❌ **Aldri push** til offentlig repository
6. ❌ **Aldri del** linker til raw files

### Sikkerhet

Se [SENSITIVE_DATA_GUIDE.md](../../SENSITIVE_DATA_GUIDE.md) for:
- Detaljerte sikkerhetspraksis
- GDPR-compliance
- Anonymiseringsteknikker
- Backup-strategier

### Arbeidsflyt

#### Daglig Bruk

```bash
# Åpne Jupyter
jupyter notebook notebooks/min_slektsanalyse.ipynb

# Kjør analyser med dine data
# Commit kun notebooks (IKKE data)
git add notebooks/
git commit -m "Update family analysis"
git push
```

#### Oppdatere Kode

```bash
# Hent nyeste versjon av slektstre-pakken
pip install --upgrade git+https://github.com/arvidl/slektstre.git

# Test at alt fungerer
python -c "from slektstre import Slektstre; print('OK')"
```

### Samarbeid med Familie

1. Legg til collaborators på GitHub (Settings → Collaborators)
2. Alle må ha eget samtykke-skjema
3. Avtal hvem som har ansvar for hva
4. Bruk branches for personlige analyser

---

## 🇬🇧 English

### Setup

1. **Install the slektstre package**:
   ```bash
   pip install git+https://github.com/arvidl/slektstre.git
   ```

2. **Add your data files** to the `data/` directory

3. **Never commit sensitive data** to public repos!

### Data Structure

```
slektstre-privat/
├── data/
│   ├── familie.yaml          # Main family data
│   ├── historiske_dokumenter/ # Source documents
│   └── bilder/               # Family photos
├── notebooks/
│   └── min_slektsanalyse.ipynb # Your analyses
├── .gitignore                 # Important: protects sensitive files
└── requirements.txt           # Dependencies
```

### Data Files

- **familie.yaml** - Main family tree in YAML format
- **historiske_dokumenter/** - Scanned documents, birth certificates, etc.
- **bilder/** - Family photos (organize by person/event)
- **notater/** - Research notes and sources

### Important Rules

1. ✅ **Use private repository** on GitHub
2. ✅ **Verify .gitignore** before each commit
3. ✅ **Take regular backups** (encrypted)
4. ✅ **Get consent** from living individuals
5. ❌ **Never push** to public repository
6. ❌ **Never share** links to raw files

### Security

See [SENSITIVE_DATA_GUIDE.md](../../SENSITIVE_DATA_GUIDE.md) for:
- Detailed security practices
- GDPR compliance
- Anonymization techniques
- Backup strategies

### Workflow

#### Daily Use

```bash
# Open Jupyter
jupyter notebook notebooks/min_slektsanalyse.ipynb

# Run analyses with your data
# Commit only notebooks (NOT data)
git add notebooks/
git commit -m "Update family analysis"
git push
```

#### Update Code

```bash
# Get latest version of slektstre package
pip install --upgrade git+https://github.com/arvidl/slektstre.git

# Test that everything works
python -c "from slektstre import Slektstre; print('OK')"
```

### Collaborate with Family

1. Add collaborators on GitHub (Settings → Collaborators)
2. Everyone needs their own consent form
3. Agree on who is responsible for what
4. Use branches for personal analyses

---

## 📚 Ressurser / Resources

- [Public slektstre repo](https://github.com/arvidl/slektstre) - Source code and documentation
- [SENSITIVE_DATA_GUIDE.md](../../SENSITIVE_DATA_GUIDE.md) - Privacy and security guide
- [Notebooks guide](https://github.com/arvidl/slektstre#jupyter-notebooks) - How to use notebooks

## ⚠️ Disclaimer

This template is provided as-is for personal genealogical research. Users are responsible for:
- Compliance with applicable privacy laws (GDPR, etc.)
- Obtaining proper consent from individuals
- Secure storage and handling of sensitive data
- Following best practices for data protection

**Always consult with a legal professional if you're unsure about privacy requirements.**

