"""
Slektstre - Et Python-bibliotek for å bygge og visualisere familie-trær med NetworkX
"""

from models import Person, Ekteskap, FamilieData, Gender
from tree import Slektstre
from family_io import (
    load_from_yaml, save_to_yaml,
    load_from_json, save_to_json,
    load_from_csv, save_to_csv,
    export_to_gedcom
)
from visualization import (
    plot_hierarchical_tree,
    plot_fan_chart,
    plot_interactive_tree,
    plot_statistics,
    plot_hourglass_view
)
from localization import t, get_available_languages

__version__ = "1.0.0"
__author__ = "Arvid Lundervold"

__all__ = [
    # Models
    'Person', 'Ekteskap', 'FamilieData', 'Gender',
    
    # Main class
    'Slektstre',
    
    # I/O functions
    'load_from_yaml', 'save_to_yaml',
    'load_from_json', 'save_to_json',
    'load_from_csv', 'save_to_csv',
    'export_to_gedcom',
    
    # Visualization functions
    'plot_hierarchical_tree',
    'plot_fan_chart',
    'plot_interactive_tree',
    'plot_statistics',
    'plot_hourglass_view',
    
    # Localization
    't', 'get_available_languages'
]
