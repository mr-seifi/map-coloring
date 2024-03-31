import geopandas as gpd
import pandas as pd
from shapely import wkt
import matplotlib.pyplot as plt

def draw_colored_map(solution, gdf, continent):
    selected_continent = gdf[gdf['continent'] == continent]

    selected_continent['color'] = selected_continent['iso_a3'].apply(lambda x: solution.get(x, 'lightgrey'))

    fig, ax = plt.subplots(1, 1, figsize=(12, 12))
    selected_continent.plot(ax=ax, color=selected_continent['color'], edgecolor='black')

    if continent == "Europe":
        ax.set_xlim(-40, 100)
        ax.set_ylim(35, 80)
    else:
        minx, miny, maxx, maxy = selected_continent.total_bounds
        ax.set_xlim(minx - 1, maxx + 1)
        ax.set_ylim(miny - 1, maxy + 1)

    for idx, row in selected_continent.iterrows():
        if row['iso_a3'] in solution:
            plt.text(row.geometry.centroid.x, row.geometry.centroid.y, row['iso_a3'], fontsize=6, ha='center', va='center')
    # plt.text(-5, 60, 'Assignment Number = ', fontsize = 22)
    plt.show()


def draw(continent, solution):
    neighbors_df = pd.read_csv('./countries_dataset.csv')
    neighbors_df['geometry'] = neighbors_df['geometry'].apply(wkt.loads)
    gdf = gpd.GeoDataFrame(neighbors_df, geometry='geometry')

    draw_colored_map(solution, gdf, continent)