import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import seaborn as sns
import matplotlib.pyplot as plt
import os

def create_cluster_frequency_table(cluster_file_path, proteomes_dir=None, genomes_dir=None):
    """
    Creates a frequency table from mmseqs2 cluster output showing how often each cluster appears in each genome.
    
    Args:
        cluster_file_path (str): path to the mmseqs2 cluster output file
        proteomes_dir (str, optional): dir containing proteome .faa files
        genomes_dir (str, optional): dir containing complete genome fasta files
        
    Returns:
        pd.DataFrame: Frequency table with genomes as rows and clusters as columns
    """
    import os

    clusters = []
    genomes = set()
    current_cluster = None
    
    # First pass - collect all unique genomes and clusters
    with open(cluster_file_path) as f:
        for line in f:
            line = line.strip()
            if line.startswith('Cluster#'):
                current_cluster = line.split('\t')[1]
            elif line.startswith('>'):
                # Extract genome name from sequence header
                header = line[1:]  # Remove '>' character
                genome = header.split('|')[0]  # Get genome ID (e.g., 'pa8')
                clusters.append((genome, f"cluster_{current_cluster}"))
                genomes.add(genome)
            # Skip other lines (sequence data and stats)

    df = pd.DataFrame(clusters, columns=['genome', 'cluster'])
    
    # create frequency table
    freq_table = pd.crosstab(df['genome'], df['cluster'], normalize=True)
    
    # if proteome directory provided, verify all genomes are present
    if proteomes_dir:
        proteome_files = {os.path.splitext(f)[0] for f in os.listdir(proteomes_dir) if f.endswith('.faa')}
        missing = genomes - proteome_files
        if missing:
            print(f"Warning: The following genomes from clusters are missing proteome files: {missing}")
    
    # if genomes directory provided, verify all genomes are present
    if genomes_dir:
        genome_files = {os.path.splitext(f)[0] for f in os.listdir(genomes_dir) if f.endswith('.fasta')}
        missing = genomes - genome_files
        if missing:
            print(f"Warning: The following genomes from clusters are missing genome files: {missing}")
            
    return freq_table

def perform_pca_and_plot(freq_table, output_path='pca_plot.svg'):
    """
    Performs PCA on the frequency table and creates scatter plot
    
    Args:
        freq_table (pd.DataFrame): frequency table with genomes as rows and clusters as columns
        output_path (str): path where the output SVG should be saved
    """
    # perform PCA
    pca = PCA(n_components=2)
    pca_result = pca.fit_transform(freq_table)
    
    # create DataFrame with PCA results
    pca_df = pd.DataFrame(data=pca_result, columns=['PC1', 'PC2'], index=freq_table.index)
    # same order as the indices in the freq table
    pca_df.index = ['50071', 'HMGUpa1', 'Pa13', 'Pa3', 'Pa4', 'Pa8']
    
    # calculate explained variance ratio
    explained_var = pca.explained_variance_ratio_ * 100
    
    # create the plot
    plt.figure(figsize=(6, 6))
    
    # get colorblind-friendly palette with enough colors for all genomes
    colors = sns.color_palette('colorblind', n_colors=len(pca_df))
    
    # create scatter plot with different colors for each genome
    for i, (idx, row) in enumerate(pca_df.iterrows()):
        plt.scatter(row['PC1'], row['PC2'], c=[colors[i]], label=idx)
    
    # add labels for each point
    for idx, row in pca_df[:-1].iterrows():
        plt.annotate(idx, (row['PC1'], row['PC2']), 
                    xytext=(5, 5), textcoords='offset points',
                    fontsize=12)

    # one separate annotation for better readability
    plt.annotate('Pa8', (pca_df[-1:]['PC1'] * 0.3, pca_df[-1:]['PC2'] * 1.1),
                 xytext=(5, 5), textcoords='offset points',
                 fontsize=12)

    # customize the plot
    plt.xlabel(f'PC1 ({explained_var[0]:.1f}%)', fontsize=12)
    plt.ylabel(f'PC2 ({explained_var[1]:.1f}%)', fontsize=12)
    plt.legend(title='Genome', loc='upper left', fontsize=12, title_fontsize=12)
    plt.tight_layout()
    plt.savefig(output_path, bbox_inches='tight', dpi=1200)
    plt.close()
    
    print(f"PCA plot saved to {output_path}")
    print(f"Total variance explained by first two components: {sum(explained_var):.1f}%")


if __name__ == "__main__":
    # perform_pca_and_plot(csv_file_path='/Users/torben.sanders/Desktop/PhD/Corinna_project/AAI.csv')
    cluster_file_path = '/Users/torben.sanders/Desktop/PhD/Corinna_project/ref_genomes/proteins/clusters.out'
    proteomes_dir = '/Users/torben.sanders/Desktop/PhD/Corinna_project/ref_genomes/proteins'
    genomes_dir = '/Users/torben.sanders/Desktop/PhD/Corinna_project/ref_genomes'
    freq_table = create_cluster_frequency_table(cluster_file_path, proteomes_dir, genomes_dir)
    print(freq_table)
    perform_pca_and_plot(freq_table, output_path='/Users/torben.sanders/Desktop/PhD/Corinna_project/pca_plot.svg')
