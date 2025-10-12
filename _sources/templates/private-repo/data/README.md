# Data Directory / Datamappe

**🔒 PRIVATE**: Denne mappen inneholder sensitive familie-data / This folder contains sensitive family data

---

## 🇳🇴 Norsk

### Plasser dine familie-datafiler her

Disse filene er git-ignored for personvern. De vil **IKKE** bli committet til GitHub.

### Anbefalt struktur:

```
data/
├── familie.yaml              # Hovedslektstre
├── kilder/                   # Kildedokumenter
│   ├── fødselsattester/
│   ├── vigselsattester/
│   ├── dødsattester/
│   └── andre_dokumenter/
├── bilder/                   # Familiebilder
│   ├── portretter/
│   ├── familiebilder/
│   └── hendelser/
└── notater/                  # Forskningsnotater
    ├── personer/
    ├── steder/
    └── kilder/
```

### Filformater

**Hoveddata** (slektstreet):
- `familie.yaml` - YAML-format (anbefalt)
- `familie.json` - JSON-format (alternativ)
- `familie.gedcom` - GEDCOM-format (for deling med andre programmer)

**Kildedokumenter**:
- PDF (scannede dokumenter)
- JPEG/PNG (bilder)
- TXT/MD (notater og transkripsjoner)

### Sikkerhet

✅ **Alle datafiler er git-ignored**:
- `*.yaml`, `*.json`, `*.gedcom` er automatisk ignorert
- Sjekk `.gitignore` for full liste

⚠️ **Før du committer**:
```bash
# Alltid sjekk hva som blir committet
git status
git diff --staged

# Hvis du ser datafiler, STOPP og fjern dem
git reset HEAD data/familie.yaml
```

### Backup

📦 **Ta regelmessige backups**:

```bash
# Lokal backup (kryptert)
tar -czf ~/backups/familie-data-$(date +%Y%m%d).tar.gz data/
gpg --encrypt ~/backups/familie-data-$(date +%Y%m%d).tar.gz

# Eller bruk backup-script
../scripts/backup_data.sh
```

### Eksempeldata

For testing kan du bruke eksempeldata fra public repo:
```bash
# Kopier eksempeldata (IKKE reelle data)
cp /path/to/slektstre/data/eksempel_familie.yaml data/test_familie.yaml
```

---

## 🇬🇧 English

### Place your family data files here

These files are git-ignored for privacy. They will **NOT** be committed to GitHub.

### Recommended structure:

```
data/
├── familie.yaml              # Main family tree
├── kilder/                   # Source documents
│   ├── birth_certificates/
│   ├── marriage_certificates/
│   ├── death_certificates/
│   └── other_documents/
├── bilder/                   # Family photos
│   ├── portraits/
│   ├── family_photos/
│   └── events/
└── notater/                  # Research notes
    ├── persons/
    ├── places/
    └── sources/
```

### File Formats

**Main data** (family tree):
- `familie.yaml` - YAML format (recommended)
- `familie.json` - JSON format (alternative)
- `familie.gedcom` - GEDCOM format (for sharing with other programs)

**Source documents**:
- PDF (scanned documents)
- JPEG/PNG (images)
- TXT/MD (notes and transcriptions)

### Security

✅ **All data files are git-ignored**:
- `*.yaml`, `*.json`, `*.gedcom` are automatically ignored
- Check `.gitignore` for full list

⚠️ **Before committing**:
```bash
# Always check what will be committed
git status
git diff --staged

# If you see data files, STOP and remove them
git reset HEAD data/familie.yaml
```

### Backup

📦 **Take regular backups**:

```bash
# Local backup (encrypted)
tar -czf ~/backups/familie-data-$(date +%Y%m%d).tar.gz data/
gpg --encrypt ~/backups/familie-data-$(date +%Y%m%d).tar.gz

# Or use backup script
../scripts/backup_data.sh
```

### Example Data

For testing, you can use example data from the public repo:
```bash
# Copy example data (NOT real data)
cp /path/to/slektstre/data/eksempel_familie.yaml data/test_familie.yaml
```

---

## ⚠️ VIKTIG / IMPORTANT

- **ALDRI** commit reelle data til Git / **NEVER** commit real data to Git
- **ALLTID** verifiser `.gitignore` / **ALWAYS** verify `.gitignore`
- **TA BACKUP** regelmessig / **TAKE BACKUPS** regularly
- **KRYPTER** sensitive backups / **ENCRYPT** sensitive backups

