import pandas as pd
import networkx as nx
import seaborn as sns
from chord_v2 import Chord


def plot_ppi_network_as_chord_plot(ppi_csv: str, save_path: str):
    """

    Args:
        ppi_csv:
        save_path:

    Returns:

    """
    ppi_df = pd.read_csv(filepath_or_buffer=ppi_csv, sep=',')
    ppi_df['bac_prot_names'] = [element.split('-')[0].split('_')[1] for count, element in enumerate(ppi_df['ID'])]
    ppi_df['phage_prot_names'] = [element.split('-')[1] for count, element in enumerate(ppi_df['ID'])]

    # G = nx.from_pandas_edgelist(ppi_df, source='bac_prot_names', target='phage_prot_names', edge_attr='num_contacts')
    G = nx.Graph(name='Protein Interaction Graph')
    for row in ppi_df.iterrows():
        a = row[1]['bac_prot_names']  # protein a node
        b = row[1]['phage_prot_names']  # protein b node
        w = row[1]['num_contacts']  # score as weighted edge where high scores = low weight
        G.add_weighted_edges_from([(a, b, w)])  # add weighted edge to graph
    # Get unique nodes
    nodes = list(G.nodes())

    # Create a matrix of interactions
    matrix = nx.to_numpy_array(G, nodelist=nodes)

    fig = Chord(data=matrix, labels=nodes, cmap_name='n_contacts')
    fig.font_size=14
    fig.padding=100
    fig.colormap=list(sns.color_palette(palette='Blues', n_colors=10).as_hex())
    fig.save_svg(save_path)

if __name__ == "__main__":
    plot_ppi_network_as_chord_plot(ppi_csv='../PPI/pa13/ppis_filtered_pa13.csv',
                                   save_path='../PPI/pa13/pa13_ppi_network_chord.svg')