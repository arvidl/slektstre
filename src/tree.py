"""
Slektstre-klasse med NetworkX som backend
"""

import networkx as nx
from typing import List, Dict, Optional, Set, Tuple, Any
from datetime import date
import statistics
from collections import defaultdict, Counter

from models import Person, Ekteskap, FamilieData, Gender
from localization import t

class Slektstre:
    """Hovedklasse for slektstre med NetworkX som backend."""
    
    def __init__(self, familie_data: Optional[FamilieData] = None):
        """
        Initialiser slektstre.
        
        Args:
            familie_data: Eksisterende familie-data, eller None for tomt tre
        """
        self.graph = nx.DiGraph()
        self.familie_data = familie_data or FamilieData()
        self._build_graph()
    
    def _build_graph(self) -> None:
        """Bygg NetworkX-graf fra familie-data."""
        self.graph.clear()
        
        # Legg til alle personer som noder
        for person in self.familie_data.personer:
            self.graph.add_node(
                person.id,
                person=person,
                type='person'
            )
        
        # Legg til alle ekteskap som noder
        for ekteskap in self.familie_data.ekteskap:
            self.graph.add_node(
                ekteskap.id,
                ekteskap=ekteskap,
                type='marriage'
            )
            
            # Koble partnere til ekteskapet
            if ekteskap.partner1_id in self.graph:
                self.graph.add_edge(ekteskap.partner1_id, ekteskap.id, relation='partner')
                self.graph.add_edge(ekteskap.id, ekteskap.partner1_id, relation='partner')
            
            if ekteskap.partner2_id in self.graph:
                self.graph.add_edge(ekteskap.partner2_id, ekteskap.id, relation='partner')
                self.graph.add_edge(ekteskap.id, ekteskap.partner2_id, relation='partner')
        
        # Legg til forelder-barn relasjoner
        for person in self.familie_data.personer:
            for forelder_id in person.foreldre:
                if forelder_id in self.graph:
                    self.graph.add_edge(forelder_id, person.id, relation='parent-child')
            
            for barn_id in person.barn:
                if barn_id in self.graph:
                    self.graph.add_edge(person.id, barn_id, relation='parent-child')
    
    def add_person(self, person: Person) -> None:
        """Legg til person i slektstreet."""
        self.familie_data.add_person(person)
        self._build_graph()
    
    def add_ekteskap(self, ekteskap: Ekteskap) -> None:
        """Legg til ekteskap i slektstreet."""
        self.familie_data.add_ekteskap(ekteskap)
        self._build_graph()
    
    def add_child(self, forelder_id: str, barn: Person) -> None:
        """Legg til barn til forelder."""
        forelder = self.get_person(forelder_id)
        if not forelder:
            raise ValueError(f"Forelder med ID {forelder_id} ikke funnet")
        
        # Legg til barn
        self.add_person(barn)
        
        # Oppdater relasjoner
        barn.foreldre.append(forelder_id)
        forelder.barn.append(barn.id)
        
        # Rebuild graph
        self._build_graph()
    
    def add_marriage(self, partner1_id: str, partner2_id: str, 
                    ekteskapsdato: Optional[date] = None,
                    ekteskapssted: Optional[str] = None) -> Ekteskap:
        """Legg til ekteskap mellom to partnere."""
        partner1 = self.get_person(partner1_id)
        partner2 = self.get_person(partner2_id)
        
        if not partner1 or not partner2:
            raise ValueError("En eller begge partnere ikke funnet")
        
        ekteskap = Ekteskap(
            partner1_id=partner1_id,
            partner2_id=partner2_id,
            ekteskapsdato=ekteskapsdato,
            ekteskapssted=ekteskapssted
        )
        
        self.add_ekteskap(ekteskap)
        
        # Oppdater partnere-lister
        partner1.partnere.append(partner2_id)
        partner2.partnere.append(partner1_id)
        
        return ekteskap
    
    def get_person(self, person_id: str) -> Optional[Person]:
        """Hent person basert på ID."""
        return self.familie_data.get_person_by_id(person_id)
    
    def get_all_persons(self) -> List[Person]:
        """Hent alle personer."""
        return self.familie_data.personer.copy()
    
    def get_ancestors(self, person_id: str, max_generations: Optional[int] = None) -> List[Person]:
        """Hent alle forfedre til en person."""
        ancestors = []
        visited = set()
        
        def _get_ancestors_recursive(current_id: str, generation: int = 0):
            if max_generations and generation >= max_generations:
                return
            
            if current_id in visited:
                return
            
            visited.add(current_id)
            person = self.get_person(current_id)
            if person:
                ancestors.append(person)
                
                for forelder_id in person.foreldre:
                    _get_ancestors_recursive(forelder_id, generation + 1)
        
        _get_ancestors_recursive(person_id)
        return ancestors[1:]  # Exclude the person themselves
    
    def get_descendants(self, person_id: str, max_generations: Optional[int] = None) -> List[Person]:
        """Hent alle etterkommere til en person."""
        descendants = []
        visited = set()
        
        def _get_descendants_recursive(current_id: str, generation: int = 0):
            if max_generations and generation >= max_generations:
                return
            
            if current_id in visited:
                return
            
            visited.add(current_id)
            person = self.get_person(current_id)
            if person:
                descendants.append(person)
                
                for barn_id in person.barn:
                    _get_descendants_recursive(barn_id, generation + 1)
        
        _get_descendants_recursive(person_id)
        return descendants[1:]  # Exclude the person themselves
    
    def get_siblings(self, person_id: str) -> List[Person]:
        """Hent søsken til en person."""
        person = self.get_person(person_id)
        if not person:
            return []
        
        siblings = []
        for forelder_id in person.foreldre:
            forelder = self.get_person(forelder_id)
            if forelder:
                for barn_id in forelder.barn:
                    if barn_id != person_id:
                        barn = self.get_person(barn_id)
                        if barn and barn not in siblings:
                            siblings.append(barn)
        
        return siblings
    
    def get_generation(self, person_id: str) -> int:
        """Beregn generasjonsnivå for en person."""
        # Finn roten (personer uten foreldre)
        roots = [p.id for p in self.get_all_persons() if not p.foreldre]
        
        if not roots:
            return 0
        
        # Bruk korteste avstand til en rot
        min_distance = float('inf')
        for root in roots:
            try:
                distance = nx.shortest_path_length(self.graph, root, person_id)
                min_distance = min(min_distance, distance)
            except nx.NetworkXNoPath:
                continue
        
        return min_distance if min_distance != float('inf') else 0
    
    def find_relation(self, person1_id: str, person2_id: str) -> Optional[str]:
        """Finn slektskap mellom to personer."""
        person1 = self.get_person(person1_id)
        person2 = self.get_person(person2_id)
        
        if not person1 or not person2:
            return None
        
        # Sjekk direkte relasjoner
        if person2_id in person1.foreldre:
            return "forelder"
        if person1_id in person2.foreldre:
            return "barn"
        if person2_id in person1.barn:
            return "barn"
        if person1_id in person2.barn:
            return "forelder"
        if person2_id in person1.partnere:
            return "partner"
        if person1_id in person2.partnere:
            return "partner"
        
        # Sjekk søsken
        siblings1 = {s.id for s in self.get_siblings(person1_id)}
        if person2_id in siblings1:
            return "søsken"
        
        # Sjekk mer komplekse relasjoner
        ancestors1 = {a.id for a in self.get_ancestors(person1_id)}
        ancestors2 = {a.id for a in self.get_ancestors(person2_id)}
        
        common_ancestors = ancestors1.intersection(ancestors2)
        if common_ancestors:
            return "slektning"
        
        return None
    
    def get_statistics(self) -> Dict[str, Any]:
        """Hent statistikk om slektstreet."""
        persons = self.get_all_persons()
        
        if not persons:
            return {}
        
        # Grunnleggende statistikk
        total_persons = len(persons)
        living_persons = len([p for p in persons if p.er_levende])
        deceased_persons = total_persons - living_persons
        
        # Kjønnsfordeling
        gender_dist = Counter(p.kjønn for p in persons)
        
        # Aldersstatistikk
        ages = [p.alder for p in persons if p.alder is not None]
        avg_age = statistics.mean(ages) if ages else None
        
        # Generasjonsstatistikk
        generations = [self.get_generation(p.id) for p in persons]
        max_generation = max(generations) if generations else 0
        
        # Ekteskapsstatistikk
        total_marriages = len(self.familie_data.ekteskap)
        active_marriages = len([e for e in self.familie_data.ekteskap if e.er_aktivt])
        
        return {
            'total_persons': total_persons,
            'living_persons': living_persons,
            'deceased_persons': deceased_persons,
            'gender_distribution': dict(gender_dist),
            'average_age': round(avg_age, 1) if avg_age else None,
            'max_generation': max_generation,
            'total_marriages': total_marriages,
            'active_marriages': active_marriages,
            'oldest_person': max(persons, key=lambda p: p.alder or 0) if ages else None,
            'youngest_person': min(persons, key=lambda p: p.alder or float('inf')) if ages else None
        }
    
    def get_persons_by_generation(self) -> Dict[int, List[Person]]:
        """Grupper personer etter generasjon."""
        generations = defaultdict(list)
        
        for person in self.get_all_persons():
            generation = self.get_generation(person.id)
            generations[generation].append(person)
        
        return dict(generations)
    
    def export_to_familie_data(self) -> FamilieData:
        """Eksporter til FamilieData-format."""
        return self.familie_data
    
    def validate_tree(self) -> List[str]:
        """Valider slektstreet og returner liste over problemer."""
        problems = []
        
        # Sjekk for sirkulære relasjoner
        try:
            cycles = list(nx.simple_cycles(self.graph))
            if cycles:
                problems.append("Sirkulære slektskap funnet")
        except:
            pass
        
        # Sjekk for foreldre som er yngre enn sine barn
        for person in self.get_all_persons():
            if person.fødselsdato:
                for forelder_id in person.foreldre:
                    forelder = self.get_person(forelder_id)
                    if forelder and forelder.fødselsdato:
                        if forelder.fødselsdato >= person.fødselsdato:
                            problems.append(f"Forelder {forelder.fullt_navn} er ikke eldre enn barn {person.fullt_navn}")
        
        return problems
