"""
Pydantic-modeller for slektstre-prosjektet
"""

from datetime import date, datetime
from typing import Optional, List, Dict, Any
from enum import Enum
from pydantic import BaseModel, Field, validator
import uuid

class Gender(str, Enum):
    """Kjønn enum."""
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"

class Person(BaseModel):
    """Modell for en person i slektstreet."""
    
    # Unik identifikator
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    
    # Navn
    fornavn: str = Field(..., min_length=1, description="Fornavn")
    mellomnavn: Optional[str] = Field(None, description="Mellomnavn")
    etternavn: Optional[str] = Field(None, description="Etternavn")
    
    # Metadata
    kjønn: Gender = Field(..., description="Kjønn")
    fødselsdato: Optional[date] = Field(None, description="Fødselsdato")
    dødsdato: Optional[date] = Field(None, description="Dødsdato")
    fødested: Optional[str] = Field(None, description="Fødested")
    dødssted: Optional[str] = Field(None, description="Dødssted")
    
    # Media og notater
    bilde_sti: Optional[str] = Field(None, description="Sti til bilde")
    notater: Optional[str] = Field(None, description="Generelle notater")
    historier: Optional[List[str]] = Field(default_factory=list, description="Historier og anekdoter")
    
    # Relasjoner (referanser til andre person-IDer)
    foreldre: List[str] = Field(default_factory=list, description="IDer til foreldre")
    barn: List[str] = Field(default_factory=list, description="IDer til barn")
    partnere: List[str] = Field(default_factory=list, description="IDer til partnere/ektefeller")
    
    # Ekstra metadata
    ekstra_data: Dict[str, Any] = Field(default_factory=dict, description="Ekstra metadata")
    
    @validator('dødsdato')
    def validate_death_date(cls, v, values):
        """Valider at dødsdato er etter fødselsdato."""
        if v and 'fødselsdato' in values and values['fødselsdato']:
            if v <= values['fødselsdato']:
                raise ValueError('Dødsdato må være etter fødselsdato')
        return v
    
    @property
    def fullt_navn(self) -> str:
        """Returner fullt navn."""
        navn_deler = [self.fornavn]
        if self.mellomnavn:
            navn_deler.append(self.mellomnavn)
        if self.etternavn:
            navn_deler.append(self.etternavn)
        return ' '.join(navn_deler)
    
    @property
    def alder(self) -> Optional[int]:
        """Beregn alder basert på fødselsdato."""
        if not self.fødselsdato:
            return None
        
        sluttdato = self.dødsdato or date.today()
        return (sluttdato - self.fødselsdato).days // 365
    
    @property
    def er_levende(self) -> bool:
        """Sjekk om personen er levende."""
        return self.dødsdato is None
    
    class Config:
        """Pydantic konfigurasjon."""
        use_enum_values = True
        json_encoders = {
            date: lambda v: v.isoformat(),
            datetime: lambda v: v.isoformat()
        }

class Ekteskap(BaseModel):
    """Modell for ekteskap eller partnerskap."""
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    partner1_id: str = Field(..., description="ID til første partner")
    partner2_id: str = Field(..., description="ID til andre partner")
    
    # Ekteskapsdatoer
    ekteskapsdato: Optional[date] = Field(None, description="Dato for ekteskap/partnerskap")
    skilsmisse_dato: Optional[date] = Field(None, description="Dato for skilsmisse")
    
    # Metadata
    ekteskapssted: Optional[str] = Field(None, description="Sted for ekteskap")
    ekteskapstype: str = Field(default="ekteskap", description="Type partnerskap")
    notater: Optional[str] = Field(None, description="Notater om ekteskapet")
    
    @validator('skilsmisse_dato')
    def validate_divorce_date(cls, v, values):
        """Valider at skilsmisse er etter ekteskap."""
        if v and 'ekteskapsdato' in values and values['ekteskapsdato']:
            if v <= values['ekteskapsdato']:
                raise ValueError('Skilsmisse må være etter ekteskapsdato')
        return v
    
    @property
    def varighet(self) -> Optional[int]:
        """Beregn ekteskapets varighet i år."""
        if not self.ekteskapsdato:
            return None
        
        sluttdato = self.skilsmisse_dato or date.today()
        return (sluttdato - self.ekteskapsdato).days // 365
    
    @property
    def er_aktivt(self) -> bool:
        """Sjekk om ekteskapet er aktivt."""
        return self.skilsmisse_dato is None
    
    class Config:
        """Pydantic konfigurasjon."""
        json_encoders = {
            date: lambda v: v.isoformat(),
            datetime: lambda v: v.isoformat()
        }

class FamilieData(BaseModel):
    """Container for all familie-data."""
    
    personer: List[Person] = Field(default_factory=list, description="Liste over personer")
    ekteskap: List[Ekteskap] = Field(default_factory=list, description="Liste over ekteskap")
    
    # Metadata
    opprettet: datetime = Field(default_factory=datetime.now, description="Når dataene ble opprettet")
    sist_endret: datetime = Field(default_factory=datetime.now, description="Når dataene sist ble endret")
    versjon: str = Field(default="1.0", description="Versjon av dataformatet")
    beskrivelse: Optional[str] = Field(None, description="Beskrivelse av familien")
    
    def get_person_by_id(self, person_id: str) -> Optional[Person]:
        """Hent person basert på ID."""
        for person in self.personer:
            if person.id == person_id:
                return person
        return None
    
    def get_ekteskap_by_id(self, ekteskap_id: str) -> Optional[Ekteskap]:
        """Hent ekteskap basert på ID."""
        for ekteskap in self.ekteskap:
            if ekteskap.id == ekteskap_id:
                return ekteskap
        return None
    
    def add_person(self, person: Person) -> None:
        """Legg til person."""
        if not any(p.id == person.id for p in self.personer):
            self.personer.append(person)
            self.sist_endret = datetime.now()
    
    def add_ekteskap(self, ekteskap: Ekteskap) -> None:
        """Legg til ekteskap."""
        if not any(e.id == ekteskap.id for e in self.ekteskap):
            self.ekteskap.append(ekteskap)
            self.sist_endret = datetime.now()
    
    class Config:
        """Pydantic konfigurasjon."""
        json_encoders = {
            date: lambda v: v.isoformat(),
            datetime: lambda v: v.isoformat()
        }
