import geopandas as gpd
import pandas as pd
from shapely import wkt
import matplotlib.pyplot as plt



def generate_borders_by_continent(df, continent):
    continent_df = df[df['continent'] == continent]

    borders = {}
    for _, row in continent_df.iterrows():
        neighbors = row['neighbors'].split(', ') if isinstance(row['neighbors'], str) else []
        borders[row['iso_a3']] = neighbors

    return borders


def is_valid(node, color, assignment, borders):
    for neighbor in borders.get(node, []):
        if color == assignment.get(neighbor):
            return False
    return True


def select_unassigned_variable(assignment, borders, colors):
    mrv = None
    min_colors = float('inf')
    for node in borders:
        if node not in assignment:
            legal_colors = len([color for color in colors if is_valid(node, color, assignment, borders)])
            if legal_colors < min_colors:
                min_colors = legal_colors
                mrv = node
    return mrv

def order_domain_values(node, assignment, borders, colors):
    def count_conflicts(color):
        conflicts = 0
        for neighbor in borders.get(node, []):
            if not is_valid(neighbor, color, assignment, borders):
                conflicts += 1
        return conflicts
    return sorted(colors, key=count_conflicts)


def backtrack(assignment, borders, colors):
    if len(assignment) == len(borders):
        return assignment

    node = select_unassigned_variable(assignment, borders, colors)

    for color in order_domain_values(node, assignment, borders, colors):
        if is_valid(node, color, assignment, borders):
            assignment[node] = color
            result = backtrack(assignment, borders, colors)
            if result:
                return result
            assignment.pop(node)
    return False

def color_map(borders, colors):
  assignment = {}
  return backtrack(assignment, borders, colors)


def draw_colored_map(solution, gdf, continent, xlim=None, ylim=None):
    selected_continent = gdf[gdf['continent'] == continent]

    selected_continent['color'] = selected_continent['iso_a3'].apply(lambda x: solution.get(x, 'lightgrey'))

    fig, ax = plt.subplots(1, 1, figsize=(12, 12))
    selected_continent.plot(ax=ax, color=selected_continent['color'], edgecolor='black')

    if xlim and ylim:
        ax.set_xlim(xlim)
        ax.set_ylim(ylim)
    else:
        minx, miny, maxx, maxy = selected_continent.total_bounds
        ax.set_xlim(minx - 1, maxx + 1)
        ax.set_ylim(miny - 1, maxy + 1)

    for idx, row in selected_continent.iterrows():
        if row['iso_a3'] in solution:
            plt.text(row.geometry.centroid.x, row.geometry.centroid.y, row['iso_a3'], fontsize=6, ha='center', va='center')

    plt.show()


def draw(continent, solution):
    neighbors_df = pd.read_csv('./countries_dataset.csv')
    neighbors_df['geometry'] = neighbors_df['geometry'].apply(wkt.loads)
    gdf = gpd.GeoDataFrame(neighbors_df, geometry='geometry')

    draw_colored_map(solution, gdf, continent)


def main():
    neighbors_df = pd.read_csv('./countries_dataset.csv')
    neighbors_df['geometry'] = neighbors_df['geometry'].apply(wkt.loads)
    gdf = gpd.GeoDataFrame(neighbors_df, geometry='geometry')

    continent = 'Asia'
    borders = generate_borders_by_continent(neighbors_df, continent)

    colors = ['red', 'green', 'blue', 'yellow']
    solution = color_map(borders, colors)
    print(solution)

    draw_colored_map(solution, gdf, continent)  ## For Europe use following args too: "xlim=(-40, 100), ylim=(35, 80)"


if __name__ == '__main__':
    main()