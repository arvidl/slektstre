# 🔒 Håndtering av Sensitive Data / Handling Sensitive Data

En omfattende guide for å håndtere private familie-data på en trygg og ansvarlig måte.

A comprehensive guide for handling private family data in a secure and responsible manner.

---

## 🇳🇴 Norsk

### 1. Hvorfor Separate Repositorier?

#### Personvern i Genealogi

Genealogiske data inneholder ofte **svært sensitiv informasjon**:
- Fulle navn, fødselsdatoer og steder
- Familieforhold og slektskap
- Adresser og kontaktinformasjon
- Personlige historier og dokumenter
- Bilder av levende personer

#### Prinsippet: Offentlig Kode vs. Private Data

**Public Repository (slektstre):**
- ✅ All kildekode og funksjoner
- ✅ Dokumentasjon og guider
- ✅ Syntetiske eksempler og tutorials
- ✅ Testing med mock-data
- ❌ INGEN reelle familie-data

**Private Repository (slektstre-privat):**
- ✅ Reelle familie-data
- ✅ Personlige analyser
- ✅ Bilder og dokumenter
- ✅ Research-notater
- ❌ IKKE kildekode (bruk pakke fra public repo)

#### Fordeler med denne Tilnærmingen

1. **Sikkerhet**: Sensitive data eksponeres aldri offentlig
2. **Deling**: Kan dele kode uten å kompromittere personvern
3. **Samarbeid**: Familie kan bidra til private repo sikkert
4. **Fleksibilitet**: Ulike tilgangsnivåer for forskjellige personer
5. **GDPR-compliance**: Lettere å følge personvernlovgivning

---

### 2. Sette Opp Ditt Private Repository

#### Steg 1: Opprett Private Repository på GitHub

1. Gå til GitHub.com og logg inn
2. Klikk på "New repository"
3. Navn: `slektstre-privat` (eller `min-slekt`, `familie-data`)
4. **VIKTIG**: Velg "Private" ❗
5. Ikke initialiser med README (vi bruker template)
6. Klikk "Create repository"

#### Steg 2: Bruk Template-strukturen

```bash
# Kopier template fra public repo
cp -r /path/to/slektstre/templates/private-repo/* /path/to/slektstre-privat/

# Gå til private repo
cd /path/to/slektstre-privat

# Initialiser Git
git init
git add .
git commit -m "Initial commit with template structure"

# Koble til GitHub remote
git remote add origin git@github.com:DITT-BRUKERNAVN/slektstre-privat.git
git branch -M main
git push -u origin main
```

#### Steg 3: Installer Public Pakke

```bash
# I ditt private repo
pip install git+https://github.com/arvidl/slektstre.git

# Eller legg til i requirements.txt og kjør:
pip install -r requirements.txt
```

---

### 3. Datasikkerhet - Best Practices

#### .gitignore Konfigurasjon

**KRITISK**: Sjekk at `.gitignore` inkluderer:

```gitignore
# Sensitive family data
*.yaml
*.json
*.gedcom
data/real_data/
data/familie/
bilder/personer/
dokumenter/
notater/private/

# Backup files
*.backup
*.old
*_backup/

# Personal notes
mine_notater.md
private_research/
```

#### Aldri Commit Sensitive Filer

**Før hver commit**, sjekk hva som blir committet:

```bash
git status
git diff --staged
```

Hvis du ser sensitive data, **STOPP**:

```bash
git reset HEAD sensitive_file.yaml
```

#### Ekstra Sikkerhet: git-crypt (Valgfritt)

For ekstra sikkerhet, krypter sensitive filer:

```bash
# Installer git-crypt
brew install git-crypt  # macOS
apt install git-crypt   # Linux

# Initialiser i repo
cd slektstre-privat
git-crypt init

# Definer hvilke filer som skal krypteres
echo "data/*.yaml filter=git-crypt diff=git-crypt" >> .gitattributes
echo "data/*.json filter=git-crypt diff=git-crypt" >> .gitattributes

git add .gitattributes
git commit -m "Add git-crypt encryption"
```

#### Backup-strategier

**Anbefalt backup-løsning**:

1. **GitHub Private Repo** (primary)
2. **Lokal ekstern disk** (encrypted backup)
3. **Cloud storage** (Google Drive/Dropbox, kryptert)

```bash
# Eksempel: Backup-script
#!/bin/bash
DATE=$(date +%Y%m%d)
tar -czf ~/backups/slektstre-privat-$DATE.tar.gz slektstre-privat/
gpg --encrypt ~/backups/slektstre-privat-$DATE.tar.gz
```

---

### 4. Arbeide med Begge Repositorier

#### Utviklingsworkflow

**Utvikle nye features:**

```bash
# 1. Jobb i public repo
cd ~/slektstre
git checkout -b new-feature

# 2. Skriv kode med syntetiske data
# 3. Test grundig
# 4. Commit og push
git add .
git commit -m "Add new feature"
git push origin new-feature
```

**Bruk med reelle data:**

```bash
# 1. Oppdater public pakke
cd ~/slektstre-privat
pip install --upgrade git+https://github.com/arvidl/slektstre.git

# 2. Kjør analyser med dine data
jupyter notebook notebooks/min_slektsanalyse.ipynb

# 3. Commit analyser (IKKE data)
git add notebooks/min_slektsanalyse.ipynb
git commit -m "Update family analysis"
git push
```

#### Testing med Syntetiske Data

Opprett test-familier i public repo:

```python
# data/eksempel_familie.yaml
personer:
  - id: "p1"
    fornavn: "Ola"
    etternavn: "Nordmann"
    kjønn: "male"
    fødselsdato: "1950-01-01"
  
  - id: "p2"
    fornavn: "Kari"
    etternavn: "Nordmann"
    kjønn: "female"
    fødselsdato: "1955-06-15"
```

#### Dele Anonymiserte Innsikter

Hvis du finner interessante mønstre:

1. **Anonymiser data** fullstendig
2. **Lag generalisert eksempel** i public repo
3. **Skriv tutorial** basert på funnene
4. **Del med community** uten å røpe private data

---

### 5. Anonymisering av Data for Deling

#### Python-script for Datarensing

```python
# scripts/anonymize_data.py
from datetime import date, timedelta
import random
import yaml

def anonymize_person(person):
    """Anonymiser en person for deling."""
    
    # Generer falske navn
    first_names = ["Ola", "Kari", "Per", "Anne", "Lars", "Ingrid"]
    last_names = ["Nordmann", "Hansen", "Olsen", "Berg", "Dahl"]
    
    anonymized = person.copy()
    anonymized['fornavn'] = random.choice(first_names)
    anonymized['etternavn'] = random.choice(last_names)
    
    # Shift datoer tilfeldig (±5 år)
    if 'fødselsdato' in person:
        orig_date = date.fromisoformat(person['fødselsdato'])
        shift_days = random.randint(-1825, 1825)  # ±5 år
        new_date = orig_date + timedelta(days=shift_days)
        anonymized['fødselsdato'] = new_date.isoformat()
    
    # Fjern identifiserende informasjon
    remove_fields = ['fødested', 'adresse', 'telefon', 'epost', 'bilde']
    for field in remove_fields:
        anonymized.pop(field, None)
    
    return anonymized

def anonymize_family_tree(input_file, output_file):
    """Anonymiser hele slektstreet."""
    with open(input_file, 'r') as f:
        data = yaml.safe_load(f)
    
    # Anonymiser personer
    if 'personer' in data:
        data['personer'] = [anonymize_person(p) for p in data['personer']]
    
    # Behold relasjoner (de er ikke identifiserende)
    
    with open(output_file, 'w') as f:
        yaml.dump(data, f, allow_unicode=True)

# Bruk
anonymize_family_tree('data/min_familie.yaml', 'data/eksempel_anonymisert.yaml')
```

#### Retningslinjer for Anonymisering

**Må fjernes:**
- ✅ Fulle navn (erstatt med pseudonymer)
- ✅ Nøyaktige fødselsdatoer (shift eller generaliser)
- ✅ Spesifikke steder (bruk fylke/land i stedet)
- ✅ Adresser og kontaktinfo
- ✅ Bilder av levende personer
- ✅ Unike historier eller hendelser

**Kan beholdes:**
- ✅ Slektskapsmønstre (hvem er relatert til hvem)
- ✅ Generasjonsstrukturer
- ✅ Statistiske mønstre
- ✅ Historiske tidsepoker (århundre)

---

### 6. Samarbeid med Familie

#### Legge til Collaborators

1. Gå til ditt private repo på GitHub
2. Settings → Collaborators
3. Legg til familiemedlemmer via GitHub-brukernavn
4. De får tilgang til private repo

#### Håndtere Forskjellige Tilgangsnivåer

**Strategi 1: Single Private Repo**
- Alle familiemedlemmer har full tilgang
- Enkel å administrere
- Krever tillit og avtaler

**Strategi 2: Personlige Branches**
```bash
# Hver person jobber på sin egen branch
git checkout -b arvid-research
# Commit personlige analyser
# Merge kun avtalt informasjon til main
```

**Strategi 3: Multiple Private Repos**
- Hvert familiemedlem har sitt eget private repo
- Deler kun avtalt informasjon via public repo
- Maksimal kontroll, mer komplekst

#### Samtykke fra Familie

**Viktig**: Få samtykke før du:
- Legger inn data om levende personer
- Deler data med andre
- Publiserer analyser eller innsikter
- Tar backup til cloud-tjenester

**Eksempel på samtykke-skjema**:
```markdown
# Samtykke for Genealogisk Forskning

Jeg, [Navn], samtykker til at følgende informasjon lagres 
i familiens private genealogi-database:

- [ ] Mitt fulle navn
- [ ] Mine fødselsdato og -sted
- [ ] Mitt forhold til andre familiemedlemmer
- [ ] Bilder hvor jeg er med (spesifiser hvilke)
- [ ] [Annen informasjon]

Jeg forstår at:
- Data lagres privat på GitHub
- Kun familiemedlemmer med tilgang kan se data
- Jeg kan trekke samtykke når som helst
- Data vil da bli fjernet

Dato: _________
Signatur: _________
```

---

### 7. Vanlige Fallgruver

#### Problem 1: Utilsiktet Commit av Sensitive Data

**Symptomer**: Du har committet en `.yaml`-fil med reelle data

**Løsning**:
```bash
# Hvis IKKE pushet ennå
git reset HEAD sensitive_file.yaml
git checkout -- sensitive_file.yaml

# Hvis allerede pushet til GitHub
# Se DEVELOPER.md for git-filter-repo instruksjoner
git filter-repo --path sensitive_file.yaml --invert-paths --force
```

#### Problem 2: Synkroniseringsfeil mellom Repos

**Symptomer**: Ny feature i public repo fungerer ikke med dine data

**Løsning**:
```bash
# Oppdater public pakke
pip install --upgrade --force-reinstall git+https://github.com/arvidl/slektstre.git

# Sjekk versjon
python -c "import slektstre; print(slektstre.__version__)"
```

#### Problem 3: .gitignore Fungerer Ikke

**Symptomer**: `.gitignore` ignorerer ikke `.yaml`-filer

**Løsning**:
```bash
# Filer allerede tracked må un-trackes
git rm --cached data/*.yaml

# Commit endringen
git commit -m "Stop tracking yaml files"

# Nå vil .gitignore fungere
```

#### Problem 4: For Stor Repo Størrelse

**Symptomer**: GitHub klager på repo størrelse

**Løsning**:
```bash
# Sjekk størrelse
du -sh .git

# Finn store filer
git rev-list --objects --all | \
  git cat-file --batch-check='%(objecttype) %(objectname) %(objectsize) %(rest)' | \
  awk '/^blob/ {print substr($0,6)}' | sort -k2 -n | tail -10

# Fjern store filer fra historikk (se DEVELOPER.md)
```

---

### 8. GDPR og Juridiske Hensyn

#### Personvernlovgivning

**GDPR (EU/EØS)** gjelder for:
- Levende personer
- Data som kan identifisere enkeltpersoner
- Lagring og deling av persondata

**Dine plikter**:
1. **Samtykke**: Få samtykke fra levende personer
2. **Formål**: Klar formålsbeskrivelse (genealogisk forskning)
3. **Sikkerhet**: Passende sikkerhetstiltak (private repo, kryptering)
4. **Rettigheter**: Personer kan kreve innsyn, retting, sletting
5. **Databehandler**: GitHub er databehandler - sjekk deres GDPR-compliance

#### Levende vs. Historiske Personer

**Levende personer** (GDPR gjelder):
- Krever samtykke
- Har rett til innsyn og sletting
- Spesielt sensitiv: barn under 18 år

**Historiske personer** (mer frihet):
- Døde personer er ikke dekket av GDPR
- 100-års regel: Data over 100 år anses som historisk
- Offentlige arkiver: Kan fritt brukes

#### Best Practices for Compliance

```yaml
# Eksempel: Dataminimering i YAML
personer:
  - id: "p1"
    fornavn: "Ola"
    etternavn: "Nordmann"
    # Lever: true/false flagg
    lever: false
    # Hvis lever=true, begrens data:
    # - Ingen fødselsdato (kun fødselsår)
    # - Ingen adresse
    # - Ingen bilder uten samtykke
```

#### Få Juridisk Råd

Hvis du:
- Deler data kommersielt
- Publiserer analyser offentlig
- Samler data fra mange personer
- Er usikker på reglene

**→ Konsulter en advokat** med erfaring i personvern og GDPR.

---

### 9. Ressurser og Lenker

#### Interne Ressurser

- [DEVELOPER.md](DEVELOPER.md) - Teknisk utviklerdokumentasjon
- [templates/private-repo/](templates/private-repo/) - Template for private repo
- [BOK-REDIGERING.md](BOK-REDIGERING.md) - Bok-redigering og vedlikehold

#### Eksterne Ressurser

**Personvern:**
- [Datatilsynet (Norge)](https://www.datatilsynet.no/)
- [GDPR Portal](https://gdpr.eu/)
- [GitHub Security Best Practices](https://docs.github.com/en/code-security)

**Genealogi:**
- [FamilySearch Privacy Policy](https://www.familysearch.org/en/help/helpcenter/article/privacy-policy)
- [Genealogical Standards](https://www.ngsgenealogy.org/resources/standards/)

**Git Sikkerhet:**
- [git-crypt](https://github.com/AGWA/git-crypt)
- [git-filter-repo](https://github.com/newren/git-filter-repo)
- [GitHub Private Repositories](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/managing-repository-settings/setting-repository-visibility)

---

## 🇬🇧 English

### 1. Why Separate Repositories?

#### Privacy Concerns in Genealogy

Genealogical data often contains **highly sensitive information**:
- Full names, birth dates and places
- Family relationships and lineage
- Addresses and contact information
- Personal stories and documents
- Photos of living individuals

#### The Principle: Public Code vs. Private Data

**Public Repository (slektstre):**
- ✅ All source code and functionality
- ✅ Documentation and guides
- ✅ Synthetic examples and tutorials
- ✅ Testing with mock data
- ❌ NO real family data

**Private Repository (slektstre-privat):**
- ✅ Real family data
- ✅ Personal analyses
- ✅ Photos and documents
- ✅ Research notes
- ❌ NOT source code (use package from public repo)

#### Benefits of This Approach

1. **Security**: Sensitive data never exposed publicly
2. **Sharing**: Can share code without compromising privacy
3. **Collaboration**: Family can contribute to private repo safely
4. **Flexibility**: Different access levels for different people
5. **GDPR Compliance**: Easier to follow privacy regulations

### 2. Setting Up Your Private Repository

[English translation follows same structure as Norwegian section above]

### 3-9. [Remaining sections follow same structure]

---

## 📝 Sjekkliste / Checklist

Før du begynner med reelle familie-data:

- [ ] Opprettet private repository på GitHub
- [ ] Kopiert template-struktur
- [ ] Verifisert `.gitignore` konfigurasjon
- [ ] Installert public pakke
- [ ] Testet med syntetiske data først
- [ ] Fått samtykke fra levende personer
- [ ] Satt opp backup-løsning
- [ ] Lest og forstått GDPR-forpliktelser
- [ ] Avtalt regler med samarbeidspartnere
- [ ] Vet hvordan man anonymiserer data for deling

**Gratulerer! Du er klar til å starte med din genealogiske forskning på en trygg og ansvarlig måte! 🎉**

