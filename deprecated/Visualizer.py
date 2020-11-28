import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd


class MapVisualizer:
    def __init__(self, cases: pd.DataFrame):
        self.voivodeships = gpd.read_file('./data/wojewodztwa.shp', encoding='utf-8')[["JPT_NAZWA_", "geometry"]]
        self.voivodeships = self.voivodeships.rename(columns={'JPT_NAZWA_': 'voivodeship'})
        self.voivodeships = self.voivodeships.join(cases, on='voivodeship')

    def visualize(self):
        ax = self.voivodeships.plot(column='cases', cmap='Reds', alpha=0.7)
        self.voivodeships.apply(lambda x: ax.annotate(text=x.cases, xy=x.geometry.centroid.coords[0], ha='center'), axis=1)
        plt.show()
