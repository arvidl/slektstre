#!/usr/bin/env python3
"""
Script to create front matter for the slektstre book including:
- Cover page
- Table of contents
- Index of terms
"""

import os
import subprocess
from datetime import datetime
from pathlib import Path

def create_cover_page():
    """Create a cover page for the book."""
    cover_html = f"""
<!DOCTYPE html>
<html lang="no">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Slektstre med NetworkX - Komplett Guide</title>
    <style>
        body {{
            font-family: 'Arial', sans-serif;
            margin: 0;
            padding: 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        .cover {{
            text-align: center;
            max-width: 800px;
            padding: 60px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            backdrop-filter: blur(10px);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        }}
        .title {{
            font-size: 3.5em;
            font-weight: bold;
            margin-bottom: 20px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
        }}
        .subtitle {{
            font-size: 1.8em;
            margin-bottom: 30px;
            opacity: 0.9;
        }}
        .description {{
            font-size: 1.2em;
            line-height: 1.6;
            margin-bottom: 40px;
            opacity: 0.8;
        }}
        .author {{
            font-size: 1.4em;
            margin-bottom: 20px;
            font-weight: 600;
        }}
        .date {{
            font-size: 1.1em;
            opacity: 0.7;
        }}
        .version {{
            position: absolute;
            bottom: 20px;
            right: 20px;
            font-size: 0.9em;
            opacity: 0.6;
        }}
        .features {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 40px 0;
        }}
        .feature {{
            background: rgba(255, 255, 255, 0.1);
            padding: 20px;
            border-radius: 10px;
            font-size: 1.1em;
        }}
    </style>
</head>
<body>
    <div class="cover">
        <div class="title">🌳 Slektstre med NetworkX</div>
        <div class="subtitle">En komplett guide til genealogi og grafteori</div>
        
        <div class="description">
            En omfattende lærebok som kombinerer slektstrær (genealogi) og grafteori 
            med praktiske eksempler og øvelser. Perfekt for både nybegynnere og 
            erfarne brukere som vil forstå hvordan NetworkX kan brukes til å bygge 
            og analysere familie-trær.
        </div>
        
        <div class="features">
            <div class="feature">📚 6 omfattende kapitler</div>
            <div class="feature">🇳🇴🇬🇧 Tospråklig</div>
            <div class="feature">💻 Praktiske øvelser</div>
            <div class="feature">📊 Visualiseringer</div>
            <div class="feature">🔍 Slektsanalyse</div>
            <div class="feature">🌐 Eksterne databaser</div>
        </div>
        
        <div class="author">Av Arvid Lundervold</div>
        <div class="date">{datetime.now().strftime('%B %Y')}</div>
        <div class="version">Versjon 1.0</div>
    </div>
</body>
</html>
"""
    
    with open('book_pdf/cover.html', 'w', encoding='utf-8') as f:
        f.write(cover_html)
    
    print("✅ Cover page created: book_pdf/cover.html")

def create_table_of_contents():
    """Create a table of contents for the book."""
    toc_html = f"""
<!DOCTYPE html>
<html lang="no">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Innholdsfortegnelse - Slektstre med NetworkX</title>
    <style>
        body {{
            font-family: 'Arial', sans-serif;
            margin: 0;
            padding: 40px;
            background: #f8f9fa;
            color: #333;
        }}
        .toc-container {{
            max-width: 800px;
            margin: 0 auto;
            background: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }}
        .toc-title {{
            font-size: 2.5em;
            font-weight: bold;
            text-align: center;
            margin-bottom: 40px;
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 20px;
        }}
        .part {{
            margin-bottom: 30px;
        }}
        .part-title {{
            font-size: 1.4em;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 15px;
            padding: 10px;
            background: #ecf0f1;
            border-left: 4px solid #3498db;
        }}
        .chapter {{
            margin-left: 20px;
            margin-bottom: 10px;
        }}
        .chapter-title {{
            font-size: 1.1em;
            color: #34495e;
            margin-bottom: 5px;
        }}
        .chapter-description {{
            font-size: 0.9em;
            color: #7f8c8d;
            margin-left: 20px;
            margin-bottom: 10px;
        }}
        .page-number {{
            float: right;
            font-weight: bold;
            color: #3498db;
        }}
        .clear {{
            clear: both;
        }}
    </style>
</head>
<body>
    <div class="toc-container">
        <div class="toc-title">📚 Innholdsfortegnelse</div>
        
        <div class="part">
            <div class="part-title">Introduksjon</div>
            <div class="chapter">
                <div class="chapter-title">
                    <span class="page-number">1</span>
                    Slektstre med NetworkX - Introduksjon
                </div>
                <div class="chapter-description">
                    Hva er prosjektet, installasjon, hovedfunksjoner og rask start
                </div>
            </div>
        </div>
        
        <div class="part">
            <div class="part-title">Teori og grunnleggende konsepter</div>
            <div class="chapter">
                <div class="chapter-title">
                    <span class="page-number">15</span>
                    Slektstrær og Grafer - En Introduksjon
                </div>
                <div class="chapter-description">
                    Kombinert introduksjon til genealogi og grafteori med praktiske øvelser
                </div>
            </div>
        </div>
        
        <div class="part">
            <div class="part-title">Praktisk bruk</div>
            <div class="chapter">
                <div class="chapter-title">
                    <span class="page-number">45</span>
                    Oversikt og grunnleggende konsepter
                </div>
                <div class="chapter-description">
                    Detaljert oversikt over slektstre-prosjektet og dets komponenter
                </div>
            </div>
            <div class="chapter">
                <div class="chapter-title">
                    <span class="page-number">65</span>
                    Bygge slektstrær programmatisk
                </div>
                <div class="chapter-description">
                    Steg-for-steg guide til å bygge slektstrær med Python
                </div>
            </div>
            <div class="chapter">
                <div class="chapter-title">
                    <span class="page-number">85</span>
                    Import og eksport av data
                </div>
                <div class="chapter-description">
                    Håndtering av forskjellige dataformater (YAML, JSON, CSV, GEDCOM)
                </div>
            </div>
            <div class="chapter">
                <div class="chapter-title">
                    <span class="page-number">105</span>
                    Visualisering av slektstrær
                </div>
                <div class="chapter-description">
                    Alle visualiseringsalternativer og hvordan de brukes
                </div>
            </div>
            <div class="chapter">
                <div class="chapter-title">
                    <span class="page-number">125</span>
                    Integrasjon med eksterne databaser
                </div>
                <div class="chapter-description">
                    Kobling til FamilySearch, Digitalarkivet og andre genealogi-tjenester
                </div>
            </div>
        </div>
        
        <div class="part">
            <div class="part-title">Vedlegg</div>
            <div class="chapter">
                <div class="chapter-title">
                    <span class="page-number">145</span>
                    Stikkordregister
                </div>
                <div class="chapter-description">
                    Alfabetisk oversikt over viktige begreper og deres definisjoner
                </div>
            </div>
            <div class="chapter">
                <div class="chapter-title">
                    <span class="page-number">155</span>
                    Bok-redigering og vedlikehold
                </div>
                <div class="chapter-description">
                    Instruksjoner for å redigere boken og legge til nye kapitler
                </div>
            </div>
        </div>
        
        <div class="clear"></div>
    </div>
</body>
</html>
"""
    
    with open('book_pdf/table_of_contents.html', 'w', encoding='utf-8') as f:
        f.write(toc_html)
    
    print("✅ Table of contents created: book_pdf/table_of_contents.html")

def create_index():
    """Create an index of terms for the book."""
    index_html = f"""
<!DOCTYPE html>
<html lang="no">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Stikkordregister - Slektstre med NetworkX</title>
    <style>
        body {{
            font-family: 'Arial', sans-serif;
            margin: 0;
            padding: 40px;
            background: #f8f9fa;
            color: #333;
        }}
        .index-container {{
            max-width: 800px;
            margin: 0 auto;
            background: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }}
        .index-title {{
            font-size: 2.5em;
            font-weight: bold;
            text-align: center;
            margin-bottom: 40px;
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 20px;
        }}
        .index-section {{
            margin-bottom: 30px;
        }}
        .section-title {{
            font-size: 1.4em;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 15px;
            padding: 10px;
            background: #ecf0f1;
            border-left: 4px solid #3498db;
        }}
        .index-entry {{
            margin-bottom: 8px;
            padding: 5px 0;
            border-bottom: 1px solid #ecf0f1;
        }}
        .term {{
            font-weight: bold;
            color: #2c3e50;
        }}
        .definition {{
            color: #7f8c8d;
            font-size: 0.9em;
            margin-left: 10px;
        }}
        .page-ref {{
            float: right;
            color: #3498db;
            font-weight: bold;
        }}
        .clear {{
            clear: both;
        }}
    </style>
</head>
<body>
    <div class="index-container">
        <div class="index-title">📖 Stikkordregister</div>
        
        <div class="index-section">
            <div class="section-title">A</div>
            <div class="index-entry">
                <span class="term">Ancestor</span>
                <span class="page-ref">15, 45</span>
                <div class="definition">Forfader, person som er i slekt med en annen person gjennom tidligere generasjoner</div>
            </div>
            <div class="index-entry">
                <span class="term">API</span>
                <span class="page-ref">125</span>
                <div class="definition">Application Programming Interface, grensesnitt for å kommunisere med eksterne tjenester</div>
            </div>
        </div>
        
        <div class="index-section">
            <div class="section-title">B</div>
            <div class="index-entry">
                <span class="term">Barn</span>
                <span class="page-ref">15, 65</span>
                <div class="definition">Person som er direkte etterkommer av foreldre</div>
            </div>
            <div class="index-entry">
                <span class="term">Bidirectional edge</span>
                <span class="page-ref">25</span>
                <div class="definition">Kant i en graf som kan traverseres i begge retninger</div>
            </div>
        </div>
        
        <div class="index-section">
            <div class="section-title">C</div>
            <div class="index-entry">
                <span class="term">CSV</span>
                <span class="page-ref">85</span>
                <div class="definition">Comma-Separated Values, tekstformat for tabulære data</div>
            </div>
            <div class="index-entry">
                <span class="term">Cycle</span>
                <span class="page-ref">25, 35</span>
                <div class="definition">Sykel, sti i en graf som returnerer til startnoden</div>
            </div>
        </div>
        
        <div class="index-section">
            <div class="section-title">D</div>
            <div class="index-entry">
                <span class="term">Descendant</span>
                <span class="page-ref">15, 45</span>
                <div class="definition">Etterkommer, person som er i slekt med en annen person gjennom senere generasjoner</div>
            </div>
            <div class="index-entry">
                <span class="term">Directed graph</span>
                <span class="page-ref">25</span>
                <div class="definition">Retnet graf, graf hvor kanter har retning</div>
            </div>
        </div>
        
        <div class="index-section">
            <div class="section-title">E</div>
            <div class="index-entry">
                <span class="term">Edge</span>
                <span class="page-ref">25</span>
                <div class="definition">Kant, linje som kobler to noder i en graf</div>
            </div>
            <div class="index-entry">
                <span class="term">Ekteskap</span>
                <span class="page-ref">15, 65</span>
                <div class="definition">Partnerskap mellom to personer, representert som uretnede kanter</div>
            </div>
        </div>
        
        <div class="index-section">
            <div class="section-title">F</div>
            <div class="index-entry">
                <span class="term">Family tree</span>
                <span class="page-ref">15</span>
                <div class="definition">Slektstre, visuell representasjon av slektskap og familierelasjoner</div>
            </div>
            <div class="index-entry">
                <span class="term">Forelder</span>
                <span class="page-ref">15, 65</span>
                <div class="definition">Person som er direkte forfader til barn</div>
            </div>
        </div>
        
        <div class="index-section">
            <div class="section-title">G</div>
            <div class="index-entry">
                <span class="term">GEDCOM</span>
                <span class="page-ref">85</span>
                <div class="definition">Genealogical Data Communication, standardformat for genealogi-data</div>
            </div>
            <div class="index-entry">
                <span class="term">Generation</span>
                <span class="page-ref">15, 45</span>
                <div class="definition">Generasjon, nivå i slektskapet basert på avstand fra rot</div>
            </div>
            <div class="index-entry">
                <span class="term">Graph theory</span>
                <span class="page-ref">25</span>
                <div class="definition">Grafteori, matematisk studie av grafer og deres egenskaper</div>
            </div>
        </div>
        
        <div class="index-section">
            <div class="section-title">J</div>
            <div class="index-entry">
                <span class="term">JSON</span>
                <span class="page-ref">85</span>
                <div class="definition">JavaScript Object Notation, tekstformat for strukturert data</div>
            </div>
        </div>
        
        <div class="index-section">
            <div class="section-title">K</div>
            <div class="index-entry">
                <span class="term">Kinship</span>
                <span class="page-ref">15, 45</span>
                <div class="definition">Slektskap, relasjon mellom personer basert på familieforhold</div>
            </div>
        </div>
        
        <div class="index-section">
            <div class="section-title">N</div>
            <div class="index-entry">
                <span class="term">NetworkX</span>
                <span class="page-ref">25, 45</span>
                <div class="definition">Python-bibliotek for analyse av komplekse nettverk og grafer</div>
            </div>
            <div class="index-entry">
                <span class="term">Node</span>
                <span class="page-ref">25</span>
                <div class="definition">Node, punkt i en graf som representerer en enhet</div>
            </div>
        </div>
        
        <div class="index-section">
            <div class="section-title">P</div>
            <div class="index-entry">
                <span class="term">Path</span>
                <span class="page-ref">25, 35</span>
                <div class="definition">Sti, sekvens av noder koblet med kanter</div>
            </div>
            <div class="index-entry">
                <span class="term">Pedigree</span>
                <span class="page-ref">15</span>
                <div class="definition">Stamtavle, visuell representasjon av forfedre</div>
            </div>
        </div>
        
        <div class="index-section">
            <div class="section-title">S</div>
            <div class="index-entry">
                <span class="term">Slektstre</span>
                <span class="page-ref">15</span>
                <div class="definition">Family tree, visuell representasjon av slektskap og familierelasjoner</div>
            </div>
            <div class="index-entry">
                <span class="term">Søsken</span>
                <span class="page-ref">15, 45</span>
                <div class="definition">Personer som deler samme foreldre</div>
            </div>
        </div>
        
        <div class="index-section">
            <div class="section-title">T</div>
            <div class="index-entry">
                <span class="term">Tree</span>
                <span class="page-ref">25, 35</span>
                <div class="definition">Tre, spesiell type graf uten sykler og sammenkoblet</div>
            </div>
        </div>
        
        <div class="index-section">
            <div class="section-title">V</div>
            <div class="index-entry">
                <span class="term">Vertex</span>
                <span class="page-ref">25</span>
                <div class="definition">Hjørne, alternativt navn for node i en graf</div>
            </div>
        </div>
        
        <div class="index-section">
            <div class="section-title">Y</div>
            <div class="index-entry">
                <span class="term">YAML</span>
                <span class="page-ref">85</span>
                <div class="definition">YAML Ain't Markup Language, menneskelesbart dataformat</div>
            </div>
        </div>
        
        <div class="clear"></div>
    </div>
</body>
</html>
"""
    
    with open('book_pdf/index.html', 'w', encoding='utf-8') as f:
        f.write(index_html)
    
    print("✅ Index created: book_pdf/index.html")

def convert_html_to_pdf(html_file, pdf_file):
    """Convert HTML file to PDF using Chrome."""
    try:
        subprocess.run([
            '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
            '--headless',
            '--disable-gpu',
            f'--print-to-pdf={pdf_file}',
            '--print-to-pdf-no-header',
            f'file://{os.path.abspath(html_file)}'
        ], check=True)
        return True
    except Exception as e:
        print(f"❌ Error converting {html_file}: {e}")
        return False

def main():
    """Main function to create all front matter."""
    print("📚 Creating book front matter...")
    
    # Create HTML files
    create_cover_page()
    create_table_of_contents()
    create_index()
    
    # Convert to PDF
    print("\n🔄 Converting to PDF...")
    
    # Import subprocess here to avoid issues if not available
    import subprocess
    
    success = True
    success &= convert_html_to_pdf('book_pdf/cover.html', 'book_pdf/cover.pdf')
    success &= convert_html_to_pdf('book_pdf/table_of_contents.html', 'book_pdf/table_of_contents.pdf')
    success &= convert_html_to_pdf('book_pdf/index.html', 'book_pdf/index.pdf')
    
    if success:
        print("✅ All front matter created successfully!")
        print("📄 Files created:")
        print("  - book_pdf/cover.pdf")
        print("  - book_pdf/table_of_contents.pdf")
        print("  - book_pdf/index.pdf")
    else:
        print("❌ Some conversions failed")

if __name__ == "__main__":
    main()
