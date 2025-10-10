# Slektstre med NetworkX

Et Python-bibliotek for å bygge, administrere og visualisere familie-trær ved hjelp av NetworkX og Jupyter notebooks.

## 🇳🇴 Norsk / 🇬🇧 English

### Norsk (Hovedspråk)

Slektstre-prosjektet lar deg bygge komplekse familie-trær med rike metadata, importere/eksportere data i flere formater, og visualisere slektskap på forskjellige måter. Prosjektet støtter både norsk og engelsk språk.

#### Hovedfunksjoner

- 📊 **Rike metadata**: Fødselsdatoer, steder, bilder, historier og notater
- 🔄 **Fleksibel datainput**: Manuell programmatisk opprettelse og fil-basert import
- 📈 **Avanserte visualiseringer**: Hierarkisk, vifte-diagram, interaktiv og timeglass-visning
- 🌍 **Tospråklig støtte**: Norsk (primær) og engelsk
- 📁 **Flere dataformater**: YAML, JSON, CSV og GEDCOM
- 🔍 **Slektsanalyse**: Beregning av slektskap, generasjonsnivåer og statistikk

#### Installasjon

```bash
# Opprett conda-miljø
conda env create -f environment.yml
conda activate slektstre

# Eller installer pakker direkte
pip install -r requirements.txt
```

#### Rask start

```python
# Importer modulene direkte fra src-mappen
import sys
sys.path.append('src')

from models import Person, Gender
from tree import Slektstre
from datetime import date

# Opprett personer
person = Person(
    fornavn="Arvid",
    etternavn="Lundervold", 
    kjønn=Gender.MALE,
    fødselsdato=date(1985, 12, 10),
    fødested="Bergen"
)

# Opprett slektstre
slektstre = Slektstre()
slektstre.add_person(person)

# Visualiser
from visualization import plot_hierarchical_tree
import matplotlib.pyplot as plt

fig = plot_hierarchical_tree(slektstre)
plt.show()
```

#### Jupyter Notebooks

Prosjektet inkluderer fire omfattende notebooks:

1. **01_introduksjon.ipynb** - Oversikt og grunnleggende konsepter
2. **02_bygg_tre_manuelt.ipynb** - Bygge slektstreet programmatisk
3. **03_importer_data.ipynb** - Import/eksport av data
4. **04_visualisering.ipynb** - Alle visualiseringsalternativer

#### Dataformat

Slektstreet støtter flere formater:

**YAML (anbefalt)**:
```yaml
personer:
  - id: "p1"
    fornavn: "Arvid"
    etternavn: "Lundervold"
    kjønn: "male"
    fødselsdato: "1985-12-10"
    fødested: "Bergen"
ekteskap:
  - partner1_id: "p1"
    partner2_id: "p2"
    ekteskapsdato: "2010-06-18"
```

**JSON, CSV og GEDCOM** støttes også.

#### Visualiseringer

- **Hierarkisk slektstre**: Tradisjonell tre-struktur
- **Vifte-diagram**: Sirkulær visning av forfedre
- **Interaktiv visning**: Plotly-basert med hover-info
- **Timeglass-visning**: Fokusperson i midten
- **Statistikk-diagrammer**: Kjønnsfordeling, aldersfordeling, etc.

### English

The Slektstre project allows you to build complex family trees with rich metadata, import/export data in multiple formats, and visualize relationships in various ways. The project supports both Norwegian and English languages.

#### Key Features

- 📊 **Rich metadata**: Birth dates, places, photos, stories and notes
- 🔄 **Flexible data input**: Manual programmatic creation and file-based import
- 📈 **Advanced visualizations**: Hierarchical, fan chart, interactive and hourglass views
- 🌍 **Bilingual support**: Norwegian (primary) and English
- 📁 **Multiple data formats**: YAML, JSON, CSV and GEDCOM
- 🔍 **Family analysis**: Relationship calculation, generation levels and statistics

#### Installation

```bash
# Create conda environment
conda env create -f environment.yml
conda activate slektstre

# Or install packages directly
pip install -r requirements.txt
```

#### Quick Start

```python
# Import modules directly from src folder
import sys
sys.path.append('src')

from models import Person, Gender
from tree import Slektstre
from datetime import date

# Create person
person = Person(
    fornavn="Arvid",
    etternavn="Lundervold",
    kjønn=Gender.MALE,
    fødselsdato=date(1985, 12, 10),
    fødested="Bergen"
)

# Create family tree
slektstre = Slektstre()
slektstre.add_person(person)

# Visualize
from visualization import plot_hierarchical_tree
import matplotlib.pyplot as plt

fig = plot_hierarchical_tree(slektstre)
plt.show()
```

#### Jupyter Notebooks

The project includes four comprehensive notebooks:

1. **01_introduksjon.ipynb** - Overview and basic concepts
2. **02_bygg_tre_manuelt.ipynb** - Building family trees programmatically
3. **03_importer_data.ipynb** - Data import/export
4. **04_visualisering.ipynb** - All visualization options

#### Data Format

The family tree supports multiple formats:

**YAML (recommended)**:
```yaml
personer:
  - id: "p1"
    fornavn: "Arvid"
    etternavn: "Lundervold"
    kjønn: "male"
    fødselsdato: "1985-12-10"
    fødested: "Bergen"
ekteskap:
  - partner1_id: "p1"
    partner2_id: "p2"
    ekteskapsdato: "2010-06-18"
```

**JSON, CSV and GEDCOM** are also supported.

#### Visualizations

- **Hierarchical family tree**: Traditional tree structure
- **Fan chart**: Circular ancestor view
- **Interactive view**: Plotly-based with hover info
- **Hourglass view**: Focus person in center
- **Statistics charts**: Gender distribution, age distribution, etc.

## Teknisk informasjon / Technical Information

### Avhengigheter / Dependencies

- Python 3.12+
- NetworkX 3.0+
- Matplotlib 3.7+
- Plotly 5.0+
- Pydantic 2.0+
- PyYAML 6.0+
- Pandas 2.0+
- Jupyter 1.0+

### Prosjektstruktur / Project Structure

```
slektstre/
├── src/                    # Kildekode / Source code
│   ├── __init__.py
│   ├── models.py          # Pydantic modeller / Models
│   ├── tree.py            # Slektstre-klasse / Main class
│   ├── family_io.py       # Import/eksport / I/O functions
│   ├── visualization.py   # Visualisering / Visualization
│   └── localization.py    # Lokalisering / Localization
├── notebooks/             # Jupyter notebooks
├── data/                  # Eksempeldata / Sample data
├── assets/                # Bilder og media / Images and media
├── environment.yml         # Conda miljø / Conda environment
├── requirements.txt       # Python pakker / Python packages
└── README.md              # Dokumentasjon / Documentation
```

### Lisens / License

MIT License - se LICENSE fil for detaljer / see LICENSE file for details.

### Bidrag / Contributing

Bidrag er velkommen! Vennligst opprett en issue eller pull request. / Contributions are welcome! Please create an issue or pull request.

### Kontakt / Contact

Arvid Lundervold - [GitHub](https://github.com/arvid)
