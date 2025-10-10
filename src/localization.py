"""
Lokalisering for slektstre-prosjektet
Støtter norsk og engelsk språk
"""

from typing import Dict, Any

# Språkdictionaries
TRANSLATIONS: Dict[str, Dict[str, str]] = {
    'no': {
        # Grunnleggende termer
        'person': 'Person',
        'family': 'Familie',
        'marriage': 'Ekteskap',
        'parent': 'Forelder',
        'child': 'Barn',
        'sibling': 'Søsken',
        'ancestor': 'Forfader',
        'descendant': 'Etterkommer',
        'generation': 'Generasjon',
        
        # Metadata
        'name': 'Navn',
        'first_name': 'Fornavn',
        'middle_name': 'Mellomnavn',
        'last_name': 'Etternavn',
        'birth_date': 'Fødselsdato',
        'death_date': 'Dødsdato',
        'birth_place': 'Fødested',
        'gender': 'Kjønn',
        'male': 'Mann',
        'female': 'Kvinne',
        'other': 'Annet',
        'photo': 'Bilde',
        'notes': 'Notater',
        'stories': 'Historier',
        
        # Relasjoner
        'father': 'Far',
        'mother': 'Mor',
        'son': 'Sønn',
        'daughter': 'Datter',
        'brother': 'Bror',
        'sister': 'Søster',
        'husband': 'Ektemann',
        'wife': 'Ektefelle',
        'partner': 'Partner',
        
        # Statistikk og analyse
        'total_persons': 'Totalt antall personer',
        'generations': 'Generasjoner',
        'oldest_person': 'Eldste person',
        'youngest_person': 'Yngste person',
        'average_age': 'Gjennomsnittsalder',
        'living_persons': 'Levende personer',
        'deceased_persons': 'Avdøde personer',
        'gender_distribution': 'Kjønnsfordeling',
        'age_distribution': 'Aldersfordeling',
        'marriage_status': 'Ekteskapstatus',
        
        # Visualisering
        'family_tree': 'Slektstre',
        'ancestor_chart': 'Forfedre-diagram',
        'descendant_chart': 'Etterkommer-diagram',
        'fan_chart': 'Vifte-diagram',
        'hourglass_view': 'Timeglass-visning',
        'interactive_view': 'Interaktiv visning',
        
        # Feilmeldinger
        'person_not_found': 'Person ikke funnet',
        'invalid_date': 'Ugyldig dato',
        'invalid_relationship': 'Ugyldig slektskap',
        'circular_relationship': 'Sirkulær slektskap',
        'file_not_found': 'Fil ikke funnet',
        'invalid_file_format': 'Ugyldig filformat',
        
        # UI-tekst
        'add_person': 'Legg til person',
        'add_marriage': 'Legg til ekteskap',
        'remove_person': 'Fjern person',
        'edit_person': 'Rediger person',
        'save': 'Lagre',
        'load': 'Last',
        'export': 'Eksporter',
        'import': 'Importer',
        'visualize': 'Visualiser',
        'statistics': 'Statistikk',
    },
    'en': {
        # Basic terms
        'person': 'Person',
        'family': 'Family',
        'marriage': 'Marriage',
        'parent': 'Parent',
        'child': 'Child',
        'sibling': 'Sibling',
        'ancestor': 'Ancestor',
        'descendant': 'Descendant',
        'generation': 'Generation',
        
        # Metadata
        'name': 'Name',
        'first_name': 'First Name',
        'middle_name': 'Middle Name',
        'last_name': 'Last Name',
        'birth_date': 'Birth Date',
        'death_date': 'Death Date',
        'birth_place': 'Birth Place',
        'gender': 'Gender',
        'male': 'Male',
        'female': 'Female',
        'other': 'Other',
        'photo': 'Photo',
        'notes': 'Notes',
        'stories': 'Stories',
        
        # Relationships
        'father': 'Father',
        'mother': 'Mother',
        'son': 'Son',
        'daughter': 'Daughter',
        'brother': 'Brother',
        'sister': 'Sister',
        'husband': 'Husband',
        'wife': 'Wife',
        'partner': 'Partner',
        
        # Statistics and analysis
        'total_persons': 'Total Persons',
        'generations': 'Generations',
        'oldest_person': 'Oldest Person',
        'youngest_person': 'Youngest Person',
        'average_age': 'Average Age',
        'living_persons': 'Living Persons',
        'deceased_persons': 'Deceased Persons',
        'gender_distribution': 'Gender Distribution',
        'age_distribution': 'Age Distribution',
        'marriage_status': 'Marriage Status',
        
        # Visualization
        'family_tree': 'Family Tree',
        'ancestor_chart': 'Ancestor Chart',
        'descendant_chart': 'Descendant Chart',
        'fan_chart': 'Fan Chart',
        'hourglass_view': 'Hourglass View',
        'interactive_view': 'Interactive View',
        
        # Error messages
        'person_not_found': 'Person not found',
        'invalid_date': 'Invalid date',
        'invalid_relationship': 'Invalid relationship',
        'circular_relationship': 'Circular relationship',
        'file_not_found': 'File not found',
        'invalid_file_format': 'Invalid file format',
        
        # UI text
        'add_person': 'Add Person',
        'add_marriage': 'Add Marriage',
        'remove_person': 'Remove Person',
        'edit_person': 'Edit Person',
        'save': 'Save',
        'load': 'Load',
        'export': 'Export',
        'import': 'Import',
        'visualize': 'Visualize',
        'statistics': 'Statistics',
    }
}

def t(key: str, lang: str = 'no') -> str:
    """
    Hent oversettelse for en nøkkel på spesifisert språk.
    
    Args:
        key: Nøkkel for oversettelse
        lang: Språkkode ('no' for norsk, 'en' for engelsk)
    
    Returns:
        Oversatt tekst eller nøkkelen hvis oversettelse ikke finnes
    """
    if lang not in TRANSLATIONS:
        lang = 'no'  # Fallback til norsk
    
    return TRANSLATIONS[lang].get(key, key)

def get_available_languages() -> list:
    """Returner liste over tilgjengelige språk."""
    return list(TRANSLATIONS.keys())

def get_translations(lang: str = 'no') -> Dict[str, str]:
    """Hent alle oversettelser for et språk."""
    return TRANSLATIONS.get(lang, TRANSLATIONS['no'])
