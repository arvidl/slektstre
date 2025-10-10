"""
Visualiseringsfunksjoner for slektstre-prosjektet
Støtter Matplotlib og Plotly med forskjellige layouts
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch
import networkx as nx
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
from typing import List, Dict, Optional, Tuple, Any
from datetime import date
import math

from models import Person, Gender
from tree import Slektstre
from localization import t

# Farger for visualisering
COLORS = {
    'male': '#4A90E2',      # Blå
    'female': '#E24A90',    # Rosa
    'other': '#90E24A',     # Grønn
    'marriage': '#F5A623',  # Oransje
    'default': '#7F7F7F'    # Grå
}

def plot_hierarchical_tree(slektstre: Slektstre, 
                          title: str = None,
                          figsize: Tuple[int, int] = (18, 12),
                          lang: str = 'no') -> plt.Figure:
    """
    Plott hierarkisk slektstre med Matplotlib.
    
    Args:
        slektstre: Slektstre objekt
        title: Tittel på plottet
        figsize: Størrelse på figur
        lang: Språk for tekster
    
    Returns:
        Matplotlib figur
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    # Hent alle personer gruppert etter generasjon
    generations = slektstre.get_persons_by_generation()
    
    if not generations:
        ax.text(0.5, 0.5, t('person_not_found', lang), 
                ha='center', va='center', transform=ax.transAxes)
        return fig
    
    # Beregn posisjoner
    pos = {}
    max_generation = max(generations.keys())
    
    for gen, persons in generations.items():
        y = (max_generation - gen) * 2.0  # Enda mer plass mellom generasjoner
        for i, person in enumerate(persons):
            x = i * 1.5 - len(persons) * 0.75  # Mer plass mellom personer
            pos[person.id] = (x, y)
    
    # Tegn grafen
    G = slektstre.graph
    
    # Tegn kanter med tydelige linjer
    for edge in G.edges():
        if G.nodes[edge[0]].get('type') == 'person' and G.nodes[edge[1]].get('type') == 'person':
            x1, y1 = pos[edge[0]]
            x2, y2 = pos[edge[1]]
            
            # Sjekk om det er forelder-barn relasjon
            edge_data = G.get_edge_data(edge[0], edge[1])
            if edge_data and edge_data.get('relation') == 'parent-child':
                # Forelder-barn: tykkere linje
                ax.plot([x1, x2], [y1, y2], 'k-', alpha=0.7, linewidth=2)
            else:
                # Andre relasjoner: tynnere linje
                ax.plot([x1, x2], [y1, y2], 'k--', alpha=0.5, linewidth=1)
    
    # Tegn ekteskap som horisontale linjer mellom partnere
    for ekteskap in slektstre.familie_data.ekteskap:
        partner1 = slektstre.get_person(ekteskap.partner1_id)
        partner2 = slektstre.get_person(ekteskap.partner2_id)
        
        if partner1 and partner2 and partner1.id in pos and partner2.id in pos:
            x1, y1 = pos[partner1.id]
            x2, y2 = pos[partner2.id]
            
            # Tegn horisontal linje mellom partnere
            ax.plot([x1, x2], [y1, y2], 'r-', alpha=0.8, linewidth=3, label='Ekteskap' if ekteskap == slektstre.familie_data.ekteskap[0] else "")
    
    # Tegn noder (personer)
    for person_id, (x, y) in pos.items():
        person = slektstre.get_person(person_id)
        if person:
            color = COLORS.get(person.kjønn, COLORS['default'])
            
            # Tegn sirkel for person
            circle = plt.Circle((x, y), 0.3, color=color, alpha=0.7)
            ax.add_patch(circle)
            
            # Legg til ID (p-nummer) inne i sirkelen
            ax.text(x, y, person.id, ha='center', va='center', fontsize=6, fontweight='bold', color='white')
            
            # Legg til navn
            ax.text(x, y-0.8, person.fornavn, ha='center', va='top', fontsize=8, fontweight='bold')
            if person.etternavn:
                ax.text(x, y-1.0, person.etternavn, ha='center', va='top', fontsize=7)
            
            # Legg til fødselsår
            if person.fødselsdato:
                ax.text(x, y+0.7, str(person.fødselsdato.year), 
                       ha='center', va='bottom', fontsize=6, fontweight='bold')
    
    # Sett opp akser
    ax.set_xlim(-max(len(persons) for persons in generations.values())//2 - 3,
                max(len(persons) for persons in generations.values())//2 + 3)
    ax.set_ylim(-3, max_generation * 2.0 + 3)
    ax.set_aspect('equal')
    ax.axis('off')
    
    # Legg til tittel
    if title:
        ax.set_title(title, fontsize=14, fontweight='bold')
    else:
        ax.set_title(t('family_tree', lang), fontsize=14, fontweight='bold')
    
    # Legg til fargeforklaring og kantforklaring
    legend_elements = [
        plt.Circle((0, 0), 0.1, color=COLORS['male'], label=t('male', lang)),
        plt.Circle((0, 0), 0.1, color=COLORS['female'], label=t('female', lang)),
        plt.Circle((0, 0), 0.1, color=COLORS['other'], label=t('other', lang)),
        plt.Line2D([0], [0], color='black', linewidth=2, label='Forelder-barn'),
        plt.Line2D([0], [0], color='red', linewidth=3, label='Ekteskap'),
        plt.Line2D([0], [0], color='black', linewidth=1, linestyle='--', label='Andre relasjoner')
    ]
    ax.legend(handles=legend_elements, loc='upper right', fontsize=8)
    
    plt.tight_layout()
    return fig

def plot_fan_chart(slektstre: Slektstre,
                   root_person_id: str,
                   title: str = None,
                   figsize: Tuple[int, int] = (10, 10),
                   lang: str = 'no') -> plt.Figure:
    """
    Plott vifte-diagram (fan chart) med Matplotlib.
    
    Args:
        slektstre: Slektstre objekt
        root_person_id: ID til rotperson
        title: Tittel på plottet
        figsize: Størrelse på figur
        lang: Språk for tekster
    
    Returns:
        Matplotlib figur
    """
    fig, ax = plt.subplots(figsize=figsize, subplot_kw=dict(projection='polar'))
    
    root_person = slektstre.get_person(root_person_id)
    if not root_person:
        ax.text(0.5, 0.5, t('person_not_found', lang), 
                ha='center', va='center', transform=ax.transAxes)
        return fig
    
    # Hent alle forfedre
    ancestors = slektstre.get_ancestors(root_person_id)
    
    if not ancestors:
        ax.text(0, 0, root_person.fornavn, ha='center', va='center', fontsize=12)
        return fig
    
    # Grupper etter generasjon
    generations = {}
    for ancestor in ancestors:
        gen = slektstre.get_generation(ancestor.id)
        if gen not in generations:
            generations[gen] = []
        generations[gen].append(ancestor)
    
    # Tegn vifte
    max_generation = max(generations.keys())
    
    for gen, persons in generations.items():
        radius = 0.2 + (gen / max_generation) * 0.8
        angle_step = 2 * math.pi / len(persons)
        
        for i, person in enumerate(persons):
            angle = i * angle_step
            color = COLORS.get(person.kjønn, COLORS['default'])
            
            # Tegn sektor
            wedge = patches.Wedge((0, 0), radius, 
                                math.degrees(angle), 
                                math.degrees(angle + angle_step),
                                color=color, alpha=0.7)
            ax.add_patch(wedge)
            
            # Legg til ID inne i sektoren
            mid_angle = angle + angle_step / 2
            id_radius = radius * 0.7
            ax.text(mid_angle, id_radius, person.id, 
                   ha='center', va='center', fontsize=6, fontweight='bold', color='white')
            
            # Legg til navn
            label_radius = radius + 0.1
            ax.text(mid_angle, label_radius, person.fornavn, 
                   ha='center', va='center', fontsize=8, rotation=0)
    
    # Tegn rotperson i midten
    center_circle = plt.Circle((0, 0), 0.15, color=COLORS.get(root_person.kjønn, COLORS['default']))
    ax.add_patch(center_circle)
    ax.text(0, 0, root_person.id, ha='center', va='center', fontsize=8, fontweight='bold', color='white')
    ax.text(0, -0.25, root_person.fornavn, ha='center', va='center', fontsize=10, fontweight='bold')
    
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.set_aspect('equal')
    ax.axis('off')
    
    if title:
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
    else:
        ax.set_title(f"{t('ancestor_chart', lang)} - {root_person.fornavn}", 
                    fontsize=14, fontweight='bold', pad=20)
    
    plt.tight_layout()
    return fig

def plot_interactive_tree(slektstre: Slektstre,
                          title: str = None,
                          lang: str = 'no') -> go.Figure:
    """
    Plott interaktivt slektstre med Plotly.
    
    Args:
        slektstre: Slektstre objekt
        title: Tittel på plottet
        lang: Språk for tekster
    
    Returns:
        Plotly figur
    """
    G = slektstre.graph
    
    # Hent posisjoner
    pos = nx.spring_layout(G, k=3, iterations=50)
    
    # Forbered data for Plotly
    edge_x = []
    edge_y = []
    edge_info = []
    
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
        
        # Legg til informasjon om relasjon
        edge_info.append(f"{edge[0]} → {edge[1]}")
    
    # Tegn kanter
    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=2, color='#888'),
        hoverinfo='none',
        mode='lines'
    )
    
    # Forbered node-data
    node_x = []
    node_y = []
    node_text = []
    node_hovertext = []
    node_colors = []
    node_sizes = []
    
    for node_id in G.nodes():
        x, y = pos[node_id]
        node_x.append(x)
        node_y.append(y)
        
        node_data = G.nodes[node_id]
        
        if node_data.get('type') == 'person':
            person = node_data['person']
            node_text.append(person.fornavn)
            
            # Hover-tekst med detaljer
            hover_text = f"<b>{person.fullt_navn}</b><br>"
            if person.fødselsdato:
                hover_text += f"{t('birth_date', lang)}: {person.fødselsdato}<br>"
            if person.dødsdato:
                hover_text += f"{t('death_date', lang)}: {person.dødsdato}<br>"
            if person.fødested:
                hover_text += f"{t('birth_place', lang)}: {person.fødested}<br>"
            hover_text += f"{t('gender', lang)}: {t(person.kjønn, lang)}"
            
            node_hovertext.append(hover_text)
            node_colors.append(COLORS.get(person.kjønn, COLORS['default']))
            node_sizes.append(20)
        else:
            # Ekteskap-node
            ekteskap = node_data['ekteskap']
            node_text.append("💒")
            node_hovertext.append(f"Ekteskap: {ekteskap.partner1_id} & {ekteskap.partner2_id}")
            node_colors.append(COLORS['marriage'])
            node_sizes.append(15)
    
    # Tegn noder
    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        hoverinfo='text',
        text=node_text,
        textposition="middle center",
        hovertext=node_hovertext,
        marker=dict(
            size=node_sizes,
            color=node_colors,
            line=dict(width=2, color='white')
        )
    )
    
    # Opprett figur
    fig = go.Figure(data=[edge_trace, node_trace],
                   layout=go.Layout(
                       title=dict(
                           text=title or t('interactive_view', lang),
                           font=dict(size=16)
                       ),
                       showlegend=False,
                       hovermode='closest',
                       margin=dict(b=20,l=5,r=5,t=40),
                       annotations=[ dict(
                           text="",
                           showarrow=False,
                           xref="paper", yref="paper",
                           x=0.005, y=-0.002,
                           xanchor="left", yanchor="bottom",
                           font=dict(color="black", size=12)
                       )],
                       xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                       yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
                   ))
    
    return fig

def plot_statistics(slektstre: Slektstre,
                   lang: str = 'no') -> go.Figure:
    """
    Plott statistikk om slektstreet.
    
    Args:
        slektstre: Slektstre objekt
        lang: Språk for tekster
    
    Returns:
        Plotly figur med statistikk
    """
    stats = slektstre.get_statistics()
    
    if not stats:
        fig = go.Figure()
        fig.add_annotation(text=t('person_not_found', lang), 
                          xref="paper", yref="paper",
                          x=0.5, y=0.5, showarrow=False)
        return fig
    
    # Opprett subplots
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=[
            t('gender_distribution', lang),
            t('generations', lang),
            t('age_distribution', lang),
            t('marriage_status', lang)
        ],
        specs=[[{"type": "pie"}, {"type": "bar"}],
               [{"type": "histogram"}, {"type": "pie"}]]
    )
    
    # Kjønnsfordeling
    gender_dist = stats.get('gender_distribution', {})
    if gender_dist:
        fig.add_trace(
            go.Pie(labels=[t(gender, lang) for gender in gender_dist.keys()],
                   values=list(gender_dist.values()),
                   name=t('gender_distribution', lang)),
            row=1, col=1
        )
    
    # Generasjonsfordeling
    generations = slektstre.get_persons_by_generation()
    gen_counts = {f"Gen {gen}": len(persons) for gen, persons in generations.items()}
    if gen_counts:
        fig.add_trace(
            go.Bar(x=list(gen_counts.keys()),
                   y=list(gen_counts.values()),
                   name=t('generations', lang)),
            row=1, col=2
        )
    
    # Aldersfordeling
    persons = slektstre.get_all_persons()
    ages = [p.alder for p in persons if p.alder is not None]
    if ages:
        fig.add_trace(
            go.Histogram(x=ages, nbinsx=10, name=t('age_distribution', lang)),
            row=2, col=1
        )
    
    # Ekteskapsstatus
    marriage_stats = {
        t('active_marriages', lang): stats.get('active_marriages', 0),
        t('divorced_marriages', lang): stats.get('total_marriages', 0) - stats.get('active_marriages', 0)
    }
    if any(marriage_stats.values()):
        fig.add_trace(
            go.Pie(labels=list(marriage_stats.keys()),
                   values=list(marriage_stats.values()),
                   name=t('marriage_status', lang)),
            row=2, col=2
        )
    
    fig.update_layout(height=600, showlegend=False,
                     title_text=t('statistics', lang), title_x=0.5)
    
    return fig

def plot_hourglass_view(slektstre: Slektstre,
                       focus_person_id: str,
                       generations_up: int = 3,
                       generations_down: int = 3,
                       title: str = None,
                       figsize: Tuple[int, int] = (12, 8),
                       lang: str = 'no') -> plt.Figure:
    """
    Plott timeglass-visning med fokusperson i midten.
    
    Args:
        slektstre: Slektstre objekt
        focus_person_id: ID til fokusperson
        generations_up: Antall generasjoner oppover
        generations_down: Antall generasjoner nedover
        title: Tittel på plottet
        figsize: Størrelse på figur
        lang: Språk for tekster
    
    Returns:
        Matplotlib figur
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    focus_person = slektstre.get_person(focus_person_id)
    if not focus_person:
        ax.text(0.5, 0.5, t('person_not_found', lang), 
                ha='center', va='center', transform=ax.transAxes)
        return fig
    
    # Hent forfedre og etterkommere
    ancestors = slektstre.get_ancestors(focus_person_id, max_generations=generations_up)
    descendants = slektstre.get_descendants(focus_person_id, max_generations=generations_down)
    
    # Beregn posisjoner
    pos = {}
    
    # Fokusperson i midten
    pos[focus_person_id] = (0, 0)
    
    # Forfedre (øverst)
    for i, ancestor in enumerate(ancestors):
        gen = slektstre.get_generation(ancestor.id)
        y = gen - slektstre.get_generation(focus_person_id)
        x = i - len(ancestors) / 2
        pos[ancestor.id] = (x, y)
    
    # Etterkommere (nederst)
    for i, descendant in enumerate(descendants):
        gen = slektstre.get_generation(descendant.id)
        y = gen - slektstre.get_generation(focus_person_id)
        x = i - len(descendants) / 2
        pos[descendant.id] = (x, y)
    
    # Tegn kanter
    G = slektstre.graph
    for edge in G.edges():
        if edge[0] in pos and edge[1] in pos:
            x1, y1 = pos[edge[0]]
            x2, y2 = pos[edge[1]]
            ax.plot([x1, x2], [y1, y2], 'k-', alpha=0.3, linewidth=1)
    
    # Tegn noder
    for person_id, (x, y) in pos.items():
        person = slektstre.get_person(person_id)
        if person:
            if person_id == focus_person_id:
                # Spesiell styling for fokusperson
                color = COLORS.get(person.kjønn, COLORS['default'])
                circle = plt.Circle((x, y), 0.4, color=color, alpha=0.9, linewidth=3)
                ax.add_patch(circle)
                ax.text(x, y, person.id, ha='center', va='center', 
                       fontsize=8, fontweight='bold', color='white')
                ax.text(x, y-0.6, person.fornavn, ha='center', va='top', 
                       fontsize=10, fontweight='bold')
            else:
                color = COLORS.get(person.kjønn, COLORS['default'])
                circle = plt.Circle((x, y), 0.3, color=color, alpha=0.7)
                ax.add_patch(circle)
                ax.text(x, y, person.id, ha='center', va='center', fontsize=6, fontweight='bold', color='white')
                ax.text(x, y-0.8, person.fornavn, ha='center', va='top', fontsize=8, fontweight='bold')
                if person.etternavn:
                    ax.text(x, y-1.0, person.etternavn, ha='center', va='top', fontsize=7)
                if person.fødselsdato:
                    ax.text(x, y+0.7, str(person.fødselsdato.year), 
                           ha='center', va='bottom', fontsize=6, fontweight='bold')
    
    # Sett opp akser
    all_x = [pos[pid][0] for pid in pos.keys()]
    all_y = [pos[pid][1] for pid in pos.keys()]
    
    ax.set_xlim(min(all_x) - 2, max(all_x) + 2)
    ax.set_ylim(min(all_y) - 2, max(all_y) + 2)
    ax.set_aspect('equal')
    ax.axis('off')
    
    if title:
        ax.set_title(title, fontsize=14, fontweight='bold')
    else:
        ax.set_title(f"{t('hourglass_view', lang)} - {focus_person.fornavn}", 
                    fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    return fig
