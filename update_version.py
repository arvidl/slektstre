#!/usr/bin/env python3
"""
Versjonshåndtering for Slektstre-prosjektet
Automatiserer oppdatering av versjonsnummer og datoer
"""

import re
import datetime
from pathlib import Path

def get_current_version():
    """Hent nåværende versjon fra VERSION.md"""
    version_file = Path("VERSION.md")
    if version_file.exists():
        with open(version_file, 'r', encoding='utf-8') as f:
            content = f.read()
            match = re.search(r'## Versjon (\d+\.\d+(?:\.\d+)?)', content)
            if match:
                return match.group(1)
    return "1.0"

def get_current_date():
    """Hent nåværende dato på norsk format"""
    now = datetime.datetime.now()
    months_norwegian = [
        "januar", "februar", "mars", "april", "mai", "juni",
        "juli", "august", "september", "oktober", "november", "desember"
    ]
    return f"{now.day} {months_norwegian[now.month-1]} {now.year}"

def get_current_date_english():
    """Hent nåværende dato på engelsk format"""
    now = datetime.datetime.now()
    months_english = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]
    return f"{months_english[now.month-1]} {now.day}, {now.year}"

def update_index_html(version, date_norwegian, date_english):
    """Oppdater index.html med ny versjon og dato"""
    index_file = Path("index.html")
    if not index_file.exists():
        print("❌ index.html ikke funnet!")
        return False
    
    with open(index_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Oppdater versjonsinfo
    old_pattern = r'Versjon \d+\.\d+(?:\.\d+)? - \d+ \w+ \d+<br>\s*Version \d+\.\d+(?:\.\d+)? - \w+ \d+, \d+'
    new_version_info = f'Versjon {version} - {date_norwegian}<br>\n            Version {version} - {date_english}'
    
    content = re.sub(old_pattern, new_version_info, content)
    
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Oppdatert index.html med versjon {version}")
    return True

def update_version_file(version, date_norwegian, date_english, changes):
    """Oppdater VERSION.md med ny versjon"""
    version_file = Path("VERSION.md")
    
    # Les eksisterende innhold
    existing_content = ""
    if version_file.exists():
        with open(version_file, 'r', encoding='utf-8') as f:
            existing_content = f.read()
    
    # Lag ny versjonsseksjon
    new_section = f"""## Versjon {version} - {date_norwegian}

### 🎉 Ny funksjonalitet:
{changes}

### 📝 Endringer:
- Oppdatert versjonsnummer til {version}
- Oppdatert dato til {date_norwegian}

---

"""
    
    # Sett inn ny seksjon etter overskriften
    if existing_content.startswith("# Slektstre med NetworkX - Versjonshistorikk"):
        lines = existing_content.split('\n')
        insert_index = 2  # Etter overskrift og tom linje
        lines.insert(insert_index, new_section)
        new_content = '\n'.join(lines)
    else:
        new_content = f"# Slektstre med NetworkX - Versjonshistorikk\n\n{new_section}{existing_content}"
    
    with open(version_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"✅ Oppdatert VERSION.md med versjon {version}")
    return True

def main():
    """Hovedfunksjon for versjonsoppdatering"""
    print("🌳 Slektstre Versjonshåndtering")
    print("=" * 40)
    
    current_version = get_current_version()
    print(f"📋 Nåværende versjon: {current_version}")
    
    # Be om ny versjon
    new_version = input(f"📝 Ny versjon (nåværende: {current_version}): ").strip()
    if not new_version:
        new_version = current_version
        print(f"⚠️  Bruker nåværende versjon: {new_version}")
    
    # Be om endringer
    print("\n📝 Beskriv endringene i denne versjonen:")
    print("   (Skriv 'done' når du er ferdig)")
    changes = []
    while True:
        change = input("   • ").strip()
        if change.lower() == 'done':
            break
        if change:
            changes.append(f"- ✅ {change}")
    
    if not changes:
        changes = ["- ✅ Generell oppdatering"]
    
    changes_text = '\n'.join(changes)
    
    # Hent datoer
    date_norwegian = get_current_date()
    date_english = get_current_date_english()
    
    print(f"\n📅 Dato: {date_norwegian} / {date_english}")
    
    # Bekreft oppdatering
    confirm = input(f"\n🤔 Bekreft oppdatering til versjon {new_version}? (y/N): ").strip().lower()
    if confirm not in ['y', 'yes', 'ja']:
        print("❌ Oppdatering avbrutt")
        return
    
    # Utfør oppdateringer
    print("\n🔄 Oppdaterer filer...")
    
    success = True
    success &= update_version_file(new_version, date_norwegian, date_english, changes_text)
    success &= update_index_html(new_version, date_norwegian, date_english)
    
    if success:
        print(f"\n🎉 Versjon {new_version} oppdatert!")
        print("\n📋 Neste steg:")
        print("   1. git add VERSION.md index.html")
        print(f"   2. git commit -m \"Release v{new_version}: {changes[0][4:] if changes else 'Update version'}\"")
        print(f"   3. git tag v{new_version}")
        print("   4. git push origin main --tags")
    else:
        print("\n❌ Noen oppdateringer feilet!")

if __name__ == "__main__":
    main()
