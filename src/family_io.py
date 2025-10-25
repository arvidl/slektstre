"""
Import/eksport funksjoner for slektstre-prosjektet
Støtter YAML, JSON, CSV og GEDCOM formater
"""

import json
import yaml
import csv
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime, date
import pandas as pd

from models import Person, Ekteskap, FamilieData, Gender
from localization import t

def load_from_yaml(file_path: str) -> FamilieData:
    """
    Last familie-data fra YAML-fil.
    
    Args:
        file_path: Sti til YAML-fil
    
    Returns:
        FamilieData objekt
    """
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(t('file_not_found'))
    
    with open(file_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    
    return _parse_yaml_data(data)

def save_to_yaml(familie_data: FamilieData, file_path: str) -> None:
    """
    Lagre familie-data til YAML-fil.
    
    Args:
        familie_data: FamilieData objekt
        file_path: Sti til YAML-fil
    """
    file_path = Path(file_path)
    
    data = {
        'metadata': {
            'versjon': familie_data.versjon,
            'opprettet': familie_data.opprettet.isoformat(),
            'sist_endret': familie_data.sist_endret.isoformat(),
            'beskrivelse': familie_data.beskrivelse
        },
        'personer': [_person_to_dict(p) for p in familie_data.personer],
        'ekteskap': [_ekteskap_to_dict(e) for e in familie_data.ekteskap]
    }
    
    with open(file_path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

def load_from_json(file_path: str) -> FamilieData:
    """
    Last familie-data fra JSON-fil.
    
    Args:
        file_path: Sti til JSON-fil
    
    Returns:
        FamilieData objekt
    """
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(t('file_not_found'))
    
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    return FamilieData(**data)

def save_to_json(familie_data: FamilieData, file_path: str) -> None:
    """
    Lagre familie-data til JSON-fil.
    
    Args:
        familie_data: FamilieData objekt
        file_path: Sti til JSON-fil
    """
    file_path = Path(file_path)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(familie_data.dict(), f, indent=2, ensure_ascii=False, default=str)

def load_from_csv(file_path: str) -> FamilieData:
    """
    Last familie-data fra CSV-fil.
    
    Args:
        file_path: Sti til CSV-fil
    
    Returns:
        FamilieData objekt
    """
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(t('file_not_found'))
    
    df = pd.read_csv(file_path, encoding='utf-8')
    
    personer = []
    for _, row in df.iterrows():
        # Hjelpefunksjon for å håndtere NaN verdier
        def safe_get(key, default=''):
            value = row.get(key, default)
            return default if pd.isna(value) else value
        
        person = Person(
            id=safe_get('id', ''),
            fornavn=safe_get('fornavn', ''),
            mellomnavn=safe_get('mellomnavn') if safe_get('mellomnavn') else None,
            etternavn=safe_get('etternavn') if safe_get('etternavn') else None,
            kjønn=Gender(safe_get('kjønn', 'other')),
            fødselsdato=_parse_date(safe_get('fødselsdato')),
            dødsdato=_parse_date(safe_get('dødsdato')),
            fødested=safe_get('fødested') if safe_get('fødested') else None,
            dødssted=safe_get('dødssted') if safe_get('dødssted') else None,
            bilde_sti=safe_get('bilde_sti') if safe_get('bilde_sti') else None,
            notater=safe_get('notater') if safe_get('notater') else None,
            historier=_parse_list(safe_get('historier')),
            foreldre=_parse_list(safe_get('foreldre')),
            barn=_parse_list(safe_get('barn')),
            partnere=_parse_list(safe_get('partnere'))
        )
        personer.append(person)
    
    # Prøv å laste ekteskap fra separat fil
    ekteskap = []
    ekteskap_file = file_path.parent / f"{file_path.stem}_ekteskap.csv"
    if ekteskap_file.exists():
        ekteskap_df = pd.read_csv(ekteskap_file, encoding='utf-8')
        for _, row in ekteskap_df.iterrows():
            def safe_get(key, default=''):
                value = row.get(key, default)
                return default if pd.isna(value) else value
            
            ekteskap_obj = Ekteskap(
                id=safe_get('id', ''),
                partner1_id=safe_get('partner1_id', ''),
                partner2_id=safe_get('partner2_id', ''),
                ekteskapsdato=_parse_date(safe_get('ekteskapsdato')),
                ekteskapssted=safe_get('ekteskapssted') if safe_get('ekteskapssted') else None,
                skilsmisse_dato=_parse_date(safe_get('skilsmisse_dato')),
                ekteskapstype=safe_get('ekteskapstype', 'ekteskap'),
                notater=safe_get('notater') if safe_get('notater') else None
            )
            ekteskap.append(ekteskap_obj)
    
    return FamilieData(personer=personer, ekteskap=ekteskap)

def save_to_csv(familie_data: FamilieData, file_path: str) -> None:
    """
    Lagre familie-data til CSV-fil.
    
    Args:
        familie_data: FamilieData objekt
        file_path: Sti til CSV-fil
    """
    file_path = Path(file_path)
    
    # Lagre personer
    rows = []
    for person in familie_data.personer:
        row = {
            'id': person.id,
            'fornavn': person.fornavn,
            'mellomnavn': person.mellomnavn,
            'etternavn': person.etternavn,
            'kjønn': person.kjønn,
            'fødselsdato': person.fødselsdato.isoformat() if person.fødselsdato else '',
            'dødsdato': person.dødsdato.isoformat() if person.dødsdato else '',
            'fødested': person.fødested,
            'dødssted': person.dødssted,
            'bilde_sti': person.bilde_sti,
            'notater': person.notater,
            'historier': '|'.join(person.historier) if person.historier else '',
            'foreldre': '|'.join(person.foreldre) if person.foreldre else '',
            'barn': '|'.join(person.barn) if person.barn else '',
            'partnere': '|'.join(person.partnere) if person.partnere else ''
        }
        rows.append(row)
    
    df = pd.DataFrame(rows)
    df.to_csv(file_path, index=False, encoding='utf-8')
    
    # Lagre ekteskap til separat fil
    if familie_data.ekteskap:
        ekteskap_file = file_path.parent / f"{file_path.stem}_ekteskap.csv"
        ekteskap_rows = []
        for ekteskap in familie_data.ekteskap:
            row = {
                'id': ekteskap.id,
                'partner1_id': ekteskap.partner1_id,
                'partner2_id': ekteskap.partner2_id,
                'ekteskapsdato': ekteskap.ekteskapsdato.isoformat() if ekteskap.ekteskapsdato else '',
                'ekteskapssted': ekteskap.ekteskapssted,
                'skilsmisse_dato': ekteskap.skilsmisse_dato.isoformat() if ekteskap.skilsmisse_dato else '',
                'ekteskapstype': ekteskap.ekteskapstype,
                'notater': ekteskap.notater
            }
            ekteskap_rows.append(row)
        
        ekteskap_df = pd.DataFrame(ekteskap_rows)
        ekteskap_df.to_csv(ekteskap_file, index=False, encoding='utf-8')

def load_from_gedcom(file_path: str) -> FamilieData:
    """
    Last familie-data fra GEDCOM-fil.
    
    Args:
        file_path: Sti til GEDCOM-fil
    
    Returns:
        FamilieData objekt
    """
    try:
        from gedcom.parser import Parser
        from gedcom.element.individual import IndividualElement
        from gedcom.element.family import FamilyElement
    except ImportError:
        raise ImportError(
            "python-gedcom library er ikke installert. "
            "Installer med: pip install python-gedcom"
        )
    
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(t('file_not_found'))
    
    # Parse GEDCOM-filen
    gedcom_parser = Parser()
    gedcom_parser.parse_file(str(file_path))
    
    personer = []
    ekteskap_liste = []
    
    # Behandle alle individer
    for element in gedcom_parser.get_root_child_elements():
        if isinstance(element, IndividualElement):
            person = _gedcom_individual_to_person(element, gedcom_parser)
            personer.append(person)
    
    # Behandle alle familier (ekteskap)
    for element in gedcom_parser.get_root_child_elements():
        if isinstance(element, FamilyElement):
            ekteskap = _gedcom_family_to_ekteskap(element, gedcom_parser)
            if ekteskap:
                ekteskap_liste.append(ekteskap)
    
    return FamilieData(
        personer=personer,
        ekteskap=ekteskap_liste,
        beskrivelse=f"Importert fra GEDCOM: {file_path.name}"
    )

def export_to_gedcom(familie_data: FamilieData, file_path: str) -> None:
    """
    Eksporter familie-data til GEDCOM-format.
    
    Args:
        familie_data: FamilieData objekt
        file_path: Sti til GEDCOM-fil
    """
    file_path = Path(file_path)
    
    gedcom_lines = [
        "0 HEAD",
        "1 SOUR SLEKTSTRE",
        "1 VERS 1.0",
        "1 DATE " + datetime.now().strftime("%d %b %Y"),
        "1 CHAR UTF8",
        "0 @FAM@ FAM",
        ""
    ]
    
    # Legg til personer
    for person in familie_data.personer:
        gedcom_lines.extend(_person_to_gedcom(person))
        gedcom_lines.append("")
    
    # Legg til familier
    for ekteskap in familie_data.ekteskap:
        gedcom_lines.extend(_ekteskap_to_gedcom(ekteskap))
        gedcom_lines.append("")
    
    gedcom_lines.append("0 TRLR")
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(gedcom_lines))

def _parse_yaml_data(data: Dict[str, Any]) -> FamilieData:
    """Parse YAML data til FamilieData objekt."""
    personer = []
    ekteskap = []
    
    # Parse personer
    for person_data in data.get('personer', []):
        person = Person(**person_data)
        personer.append(person)
    
    # Parse ekteskap
    for ekteskap_data in data.get('ekteskap', []):
        ekteskap_obj = Ekteskap(**ekteskap_data)
        ekteskap.append(ekteskap_obj)
    
    # Parse metadata
    metadata = data.get('metadata', {})
    
    return FamilieData(
        personer=personer,
        ekteskap=ekteskap,
        versjon=metadata.get('versjon', '1.0'),
        beskrivelse=metadata.get('beskrivelse'),
        opprettet=_parse_datetime(metadata.get('opprettet')),
        sist_endret=_parse_datetime(metadata.get('sist_endret'))
    )

def _person_to_dict(person: Person) -> Dict[str, Any]:
    """Konverter Person til dictionary."""
    return {
        'id': person.id,
        'fornavn': person.fornavn,
        'mellomnavn': person.mellomnavn,
        'etternavn': person.etternavn,
        'kjønn': person.kjønn,
        'fødselsdato': person.fødselsdato.isoformat() if person.fødselsdato else None,
        'dødsdato': person.dødsdato.isoformat() if person.dødsdato else None,
        'fødested': person.fødested,
        'dødssted': person.dødssted,
        'bilde_sti': person.bilde_sti,
        'notater': person.notater,
        'historier': person.historier,
        'foreldre': person.foreldre,
        'barn': person.barn,
        'partnere': person.partnere,
        'ekstra_data': person.ekstra_data
    }

def _ekteskap_to_dict(ekteskap: Ekteskap) -> Dict[str, Any]:
    """Konverter Ekteskap til dictionary."""
    return {
        'id': ekteskap.id,
        'partner1_id': ekteskap.partner1_id,
        'partner2_id': ekteskap.partner2_id,
        'ekteskapsdato': ekteskap.ekteskapsdato.isoformat() if ekteskap.ekteskapsdato else None,
        'skilsmisse_dato': ekteskap.skilsmisse_dato.isoformat() if ekteskap.skilsmisse_dato else None,
        'ekteskapssted': ekteskap.ekteskapssted,
        'ekteskapstype': ekteskap.ekteskapstype,
        'notater': ekteskap.notater
    }

def _parse_date(date_str: Optional[str]) -> Optional[date]:
    """Parse dato-streng til date objekt."""
    if not date_str or pd.isna(date_str):
        return None
    
    try:
        return datetime.strptime(str(date_str), '%Y-%m-%d').date()
    except ValueError:
        try:
            return datetime.strptime(str(date_str), '%d.%m.%Y').date()
        except ValueError:
            return None

def _parse_datetime(datetime_str: Optional[str]) -> Optional[datetime]:
    """Parse datetime-streng til datetime objekt."""
    if not datetime_str:
        return None
    
    try:
        return datetime.fromisoformat(datetime_str.replace('Z', '+00:00'))
    except ValueError:
        return None

def _parse_list(list_str: Optional[str]) -> List[str]:
    """Parse pipe-separated liste."""
    if not list_str or pd.isna(list_str):
        return []
    
    return [item.strip() for item in str(list_str).split('|') if item.strip()]

def _person_to_gedcom(person: Person) -> List[str]:
    """Konverter Person til GEDCOM format."""
    lines = [f"0 @{person.id}@ INDI"]
    lines.append(f"1 NAME {person.fornavn} /{person.etternavn or ''}/")
    
    if person.kjønn == Gender.MALE:
        lines.append("1 SEX M")
    elif person.kjønn == Gender.FEMALE:
        lines.append("1 SEX F")
    
    if person.fødselsdato:
        lines.append(f"1 BIRT")
        lines.append(f"2 DATE {person.fødselsdato.strftime('%d %b %Y')}")
        if person.fødested:
            lines.append(f"2 PLAC {person.fødested}")
    
    if person.dødsdato:
        lines.append(f"1 DEAT")
        lines.append(f"2 DATE {person.dødsdato.strftime('%d %b %Y')}")
        if person.dødssted:
            lines.append(f"2 PLAC {person.dødssted}")
    
    if person.notater:
        lines.append(f"1 NOTE {person.notater}")
    
    return lines

def _ekteskap_to_gedcom(ekteskap: Ekteskap) -> List[str]:
    """Konverter Ekteskap til GEDCOM format."""
    lines = [f"0 @{ekteskap.id}@ FAM"]
    lines.append(f"1 HUSB @{ekteskap.partner1_id}@")
    lines.append(f"1 WIFE @{ekteskap.partner2_id}@")
    
    if ekteskap.ekteskapsdato:
        lines.append(f"1 MARR")
        lines.append(f"2 DATE {ekteskap.ekteskapsdato.strftime('%d %b %Y')}")
        if ekteskap.ekteskapssted:
            lines.append(f"2 PLAC {ekteskap.ekteskapssted}")
    
    if ekteskap.skilsmisse_dato:
        lines.append(f"1 DIV")
        lines.append(f"2 DATE {ekteskap.skilsmisse_dato.strftime('%d %b %Y')}")
    
    return lines

def _gedcom_individual_to_person(individual, parser) -> Person:
    """Konverter GEDCOM Individual til Person objekt."""
    from dateutil import parser as date_parser
    
    # Hent grunnleggende informasjon
    pointer = individual.get_pointer()
    
    # Parse navn
    name_parts = individual.get_name()
    fornavn = ""
    mellomnavn = None
    etternavn = None
    
    if name_parts:
        # GEDCOM format: "Fornavn Mellomnavn /Etternavn/"
        name_str = name_parts[0] if isinstance(name_parts, tuple) else name_parts
        name_str = str(name_str).strip()
        
        # Fjern / rundt etternavn
        if '/' in name_str:
            before_surname, rest = name_str.split('/', 1)
            surname_part, after_surname = rest.split('/', 1) if '/' in rest else (rest, '')
            etternavn = surname_part.strip() if surname_part.strip() else None
            
            # Parse fornavn og mellomnavn
            given_names = before_surname.strip().split()
            if given_names:
                fornavn = given_names[0]
                if len(given_names) > 1:
                    mellomnavn = ' '.join(given_names[1:])
        else:
            # Ingen etternavn markering
            given_names = name_str.split()
            if given_names:
                fornavn = given_names[0]
                if len(given_names) > 1:
                    mellomnavn = ' '.join(given_names[1:])
    
    if not fornavn:
        fornavn = "Ukjent"
    
    # Hent kjønn
    gender_str = individual.get_gender()
    if gender_str == 'M':
        kjønn = Gender.MALE
    elif gender_str == 'F':
        kjønn = Gender.FEMALE
    else:
        kjønn = Gender.OTHER
    
    # Hent fødselsdato og -sted
    fødselsdato = None
    fødested = None
    
    # Forsøk 1: Bruk get_birth_data hvis tilgjengelig (GEDCOM 5.5)
    try:
        if hasattr(individual, 'get_birth_data'):
            birth_data = individual.get_birth_data()
            if birth_data and len(birth_data) >= 2:
                birth_date_str = birth_data[0]
                fødested = birth_data[1] if len(birth_data) > 1 else None
                
                if birth_date_str:
                    try:
                        fødselsdato = date_parser.parse(birth_date_str, fuzzy=True).date()
                    except:
                        pass
    except:
        pass
    
    # Forsøk 2: Parse BIRT tag direkte (GEDCOM 7.0)
    if fødselsdato is None:
        try:
            for child in individual.get_child_elements():
                if child.get_tag() == "BIRT":
                    for birt_child in child.get_child_elements():
                        if birt_child.get_tag() == "DATE":
                            date_str = birt_child.get_value()
                            if date_str:
                                try:
                                    fødselsdato = date_parser.parse(date_str, fuzzy=True).date()
                                except:
                                    pass
                        elif birt_child.get_tag() == "PLAC":
                            fødested = birt_child.get_value()
                    break
        except:
            pass
    
    # Hent dødsdato og -sted
    dødsdato = None
    dødssted = None
    
    # Forsøk 1: Bruk get_death_data hvis tilgjengelig (GEDCOM 5.5)
    try:
        if hasattr(individual, 'get_death_data'):
            death_data = individual.get_death_data()
            if death_data and len(death_data) >= 2:
                death_date_str = death_data[0]
                dødssted = death_data[1] if len(death_data) > 1 else None
                
                if death_date_str:
                    try:
                        dødsdato = date_parser.parse(death_date_str, fuzzy=True).date()
                    except:
                        pass
    except:
        pass
    
    # Forsøk 2: Parse DEAT tag direkte (GEDCOM 7.0)
    if dødsdato is None:
        try:
            for child in individual.get_child_elements():
                if child.get_tag() == "DEAT":
                    for deat_child in child.get_child_elements():
                        if deat_child.get_tag() == "DATE":
                            date_str = deat_child.get_value()
                            if date_str:
                                try:
                                    dødsdato = date_parser.parse(date_str, fuzzy=True).date()
                                except:
                                    pass
                        elif deat_child.get_tag() == "PLAC":
                            dødssted = deat_child.get_value()
                    break
        except:
            pass
    
    # Hent foreldre (via FAMC - family as child)
    foreldre = []
    try:
        parent_families = parser.get_families(individual, "FAMC")
        for family in parent_families:
            parents = parser.get_family_members(family, "PARENTS")
            for parent in parents:
                foreldre.append(parent.get_pointer())
    except:
        pass
    
    # Hent barn (via FAMS - family as spouse)
    barn = []
    partnere = []
    try:
        spouse_families = parser.get_families(individual, "FAMS")
        for family in spouse_families:
            # Hent barn
            children = parser.get_family_members(family, "CHIL")
            for child in children:
                barn.append(child.get_pointer())
            
            # Hent partnere
            parents = parser.get_family_members(family, "PARENTS")
            for parent in parents:
                if parent.get_pointer() != pointer:
                    partnere.append(parent.get_pointer())
    except:
        pass
    
    return Person(
        id=pointer,
        fornavn=fornavn,
        mellomnavn=mellomnavn,
        etternavn=etternavn,
        kjønn=kjønn,
        fødselsdato=fødselsdato,
        dødsdato=dødsdato,
        fødested=fødested,
        dødssted=dødssted,
        foreldre=foreldre,
        barn=barn,
        partnere=partnere,
        notater=f"Importert fra GEDCOM (ID: {pointer})"
    )

def _gedcom_family_to_ekteskap(family, parser) -> Optional[Ekteskap]:
    """Konverter GEDCOM Family til Ekteskap objekt."""
    from dateutil import parser as date_parser
    
    # Hent ektefeller/foreldre i familien
    try:
        parents = parser.get_family_members(family, "PARENTS")
        if len(parents) < 2:
            return None
        
        partner1_id = parents[0].get_pointer()
        partner2_id = parents[1].get_pointer()
    except:
        return None
    
    # Hent ekteskapsdato - forsøk flere metoder (GEDCOM 5.5 vs 7.0)
    ekteskapsdato = None
    ekteskapssted = None
    
    # Forsøk 1: Bruk get_marriage_data hvis tilgjengelig (GEDCOM 5.5)
    try:
        if hasattr(family, 'get_marriage_data'):
            marriage_data = family.get_marriage_data()
            if marriage_data and len(marriage_data) >= 2:
                marriage_date_str = marriage_data[0]
                ekteskapssted = marriage_data[1] if len(marriage_data) > 1 else None
                
                if marriage_date_str:
                    try:
                        ekteskapsdato = date_parser.parse(marriage_date_str, fuzzy=True).date()
                    except:
                        pass
    except:
        pass
    
    # Forsøk 2: Parse MARR tag direkte fra child elements (GEDCOM 7.0)
    if ekteskapsdato is None:
        try:
            for child in family.get_child_elements():
                if child.get_tag() == "MARR":
                    # Se etter DATE og PLAC under MARR
                    for marr_child in child.get_child_elements():
                        if marr_child.get_tag() == "DATE":
                            date_str = marr_child.get_value()
                            if date_str:
                                try:
                                    ekteskapsdato = date_parser.parse(date_str, fuzzy=True).date()
                                except:
                                    pass
                        elif marr_child.get_tag() == "PLAC":
                            ekteskapssted = marr_child.get_value()
                    break
        except:
            pass
    
    # Opprett ekteskap-ID
    family_pointer = family.get_pointer()
    ekteskap_id = family_pointer if family_pointer else f"e_{partner1_id}_{partner2_id}"
    
    return Ekteskap(
        id=ekteskap_id,
        partner1_id=partner1_id,
        partner2_id=partner2_id,
        ekteskapsdato=ekteskapsdato,
        ekteskapssted=ekteskapssted,
        notater=f"Importert fra GEDCOM (Family ID: {family_pointer})"
    )
