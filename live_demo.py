#!/usr/bin/env python3
"""
Live Demo for Slektstre med NetworkX
Interactive family tree visualization examples
"""

import networkx as nx
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import json

def create_sample_family():
    """Create a sample family tree for demonstration"""
    # Sample family data
    family_data = {
        "personer": [
            {"id": "p1", "navn": "Erik Hansen", "fødselsår": 1950, "kjønn": "mann"},
            {"id": "p2", "navn": "Anna Larsen", "fødselsår": 1955, "kjønn": "kvinne"},
            {"id": "p3", "navn": "Lars Hansen", "fødselsår": 1980, "kjønn": "mann"},
            {"id": "p4", "navn": "Maria Hansen", "fødselsår": 1982, "kjønn": "kvinne"},
            {"id": "p5", "navn": "Ole Hansen", "fødselsår": 2010, "kjønn": "mann"},
            {"id": "p6", "navn": "Kari Hansen", "fødselsår": 2012, "kjønn": "kvinne"},
        ],
        "ekteskap": [
            {"person1": "p1", "person2": "p2", "år": 1975},
        ],
        "foreldre": [
            {"barn": "p3", "forelder": "p1"},
            {"barn": "p3", "forelder": "p2"},
            {"barn": "p4", "forelder": "p1"},
            {"barn": "p4", "forelder": "p2"},
            {"barn": "p5", "forelder": "p3"},
            {"barn": "p6", "forelder": "p3"},
        ]
    }
    return family_data

def build_networkx_graph(family_data):
    """Build NetworkX graph from family data"""
    G = nx.DiGraph()
    
    # Add nodes (people)
    for person in family_data["personer"]:
        G.add_node(person["id"], 
                  name=person["navn"], 
                  birth_year=person["fødselsår"],
                  gender=person["kjønn"])
    
    # Add edges (relationships)
    for rel in family_data["foreldre"]:
        G.add_edge(rel["forelder"], rel["barn"], relationship="parent-child")
    
    for marriage in family_data["ekteskap"]:
        G.add_edge(marriage["person1"], marriage["person2"], relationship="marriage")
        G.add_edge(marriage["person2"], marriage["person1"], relationship="marriage")
    
    return G

def create_interactive_plot(G):
    """Create interactive Plotly visualization"""
    # Get node positions using hierarchical layout
    pos = nx.spring_layout(G, k=3, iterations=50)
    
    # Prepare node data
    node_x = []
    node_y = []
    node_text = []
    node_colors = []
    
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        
        node_data = G.nodes[node]
        node_text.append(f"{node_data['name']}<br>Født: {node_data['birth_year']}")
        
        # Color by gender
        if node_data['gender'] == 'mann':
            node_colors.append('#3498db')  # Blue
        else:
            node_colors.append('#e74c3c')  # Red
    
    # Prepare edge data
    edge_x = []
    edge_y = []
    
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
    
    # Create the plot
    fig = go.Figure()
    
    # Add edges
    fig.add_trace(go.Scatter(x=edge_x, y=edge_y,
                           line=dict(width=2, color='#888'),
                           hoverinfo='none',
                           mode='lines',
                           name='Relationships'))
    
    # Add nodes
    fig.add_trace(go.Scatter(x=node_x, y=node_y,
                           mode='markers+text',
                           hoverinfo='text',
                           text=[G.nodes[node]['name'] for node in G.nodes()],
                           textposition="middle center",
                           marker=dict(size=30,
                                     color=node_colors,
                                     line=dict(width=2, color='white')),
                           name='Family Members'))
    
    # Update layout
    fig.update_layout(
        title='🌳 Interaktiv Slektstre Demo / Interactive Family Tree Demo',
        titlefont_size=16,
        showlegend=False,
        hovermode='closest',
        margin=dict(b=20,l=5,r=5,t=40),
        annotations=[ dict(
            text="Klikk og dra for å utforske slektstreet!<br>Click and drag to explore the family tree!",
            showarrow=False,
            xref="paper", yref="paper",
            x=0.005, y=-0.002,
            xanchor='left', yanchor='bottom',
            font=dict(color='#666', size=12)
        )],
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        plot_bgcolor='white',
        width=800,
        height=600
    )
    
    return fig

def create_demo_stats(G):
    """Create family statistics"""
    stats = {
        "total_people": G.number_of_nodes(),
        "total_relationships": G.number_of_edges(),
        "generations": len(set([G.nodes[node]['birth_year'] for node in G.nodes()])),
        "oldest": min([G.nodes[node]['birth_year'] for node in G.nodes()]),
        "youngest": max([G.nodes[node]['birth_year'] for node in G.nodes()])
    }
    return stats

def main():
    """Main demo function"""
    print("🌳 Slektstre Live Demo")
    print("=" * 40)
    
    # Create sample family
    family_data = create_sample_family()
    print(f"📊 Opprettet eksempel-familie med {len(family_data['personer'])} personer")
    
    # Build NetworkX graph
    G = build_networkx_graph(family_data)
    print(f"🔗 Bygget NetworkX graf med {G.number_of_nodes()} noder og {G.number_of_edges()} kanter")
    
    # Create interactive plot
    fig = create_interactive_plot(G)
    print("📈 Genererte interaktiv visualisering")
    
    # Show statistics
    stats = create_demo_stats(G)
    print("\n📊 Familie-statistikk:")
    print(f"   • Totalt antall personer: {stats['total_people']}")
    print(f"   • Totalt antall relasjoner: {stats['total_relationships']}")
    print(f"   • Antall generasjoner: {stats['generations']}")
    print(f"   • Eldste person: {stats['oldest']}")
    print(f"   • Yngste person: {stats['youngest']}")
    
    # Show the plot
    fig.show()
    
    return fig

if __name__ == "__main__":
    main()
