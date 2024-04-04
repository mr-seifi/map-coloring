import pandas as pd
from shapely import wkt
from typing import Dict, List

def generate_borders_by_continent(continent: str, neighbor_threshold: int = 1) -> Dict[str, List[str]]:
    """
    Generates a dictionary mapping each country in the specified continent to a list of its neighboring countries'
    ISO A3 codes. The function loads geographic and neighbor data from a CSV file, filters it by the specified
    continent, and then parses each country's neighbors.

    Args:
        continent (str): The name of the continent for which to generate borders and neighbors.
        neighbor_threshold (int): The threshold for including neighbors of neighbors. Default is 1.

    Returns:
        Dict[str, List[str]]: A dictionary where keys are country ISO A3 codes and values are lists of ISO A3 codes
                               of neighboring countries within the same continent.
    """
    neighbors_df = pd.read_csv('./countries_dataset.csv')
    neighbors_df['geometry'] = neighbors_df['geometry'].apply(wkt.loads)

    continent_df = neighbors_df[neighbors_df['continent'] == continent]

    borders = {}
    for _, row in continent_df.iterrows():
        neighbors = set(row['neighbors'].split(', ')) if isinstance(row['neighbors'], str) else set()
        for k in range(1, neighbor_threshold):
            for neighbor in list(neighbors):
                second_neighbors = continent_df[continent_df['iso_a3'] == neighbor]['neighbors'].values
                if second_neighbors:
                    second_neighbors = second_neighbors[0].split(', ')
                    neighbors.update(second_neighbors)
        neighbors.discard(row['iso_a3'])
        borders[row['iso_a3']] = neighbors


    return borders
