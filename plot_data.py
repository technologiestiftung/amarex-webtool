import argparse
import zipfile

import geopandas as gpd
import matplotlib.pyplot as plt


class Plotter:
    def __init__(self, map=None, data=None):
        self.map = map
        self.data = data

    def load_map(self, shp_path):
        """
        Load map in Shapefile format.
        """
        zip_contents = zipfile.ZipFile(shp_path)
        zip_contents.extractall()
        dbf, prj, shp, shx = [f for f in sorted(zip_contents.namelist()) for ending in
                              ['dbf', 'prj', 'shp', 'shx'] if f.endswith(ending)]
        map_shp = gpd.read_file(shp)

        self.map = map_shp

    def load_data(self, data_path):
        """
        Load data in DBF format.
        """
        # Convert DBF file to Pandas dataframe
        data = gpd.read_file(data_path).drop("geometry", axis=1)
        self.data = data

    def plot(self, var):
        """
        Plot choropleth map.
        """
        var_codes = {
            "runoff": "R",
            "infiltration": "RI",
            "evaporation": "VERDUNSTUN"
        }

        merged_df = self.map.set_index("SCHLUESSEL").join(self.data.set_index("CODE"))
        merged_df.plot(column=var_codes[var], legend=True)  # Plot evaporation

        # Style the plot
        plt.title(f"{var}")
        plt.axis("off")

        plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Plot data on a map."
    )

    parser.add_argument("map_path", help="Path to the Shapefile ZIP containing the map")
    parser.add_argument("data_path", help="Path to the DBF file containing the data to plot")
    parser.add_argument("var",
                        choices=["runoff", "infiltration", "evaporation"],
                        help="Variable to plot")

    args = parser.parse_args()

    plotter = Plotter()
    plotter.load_map(args.map_path)
    plotter.load_data(args.data_path)
    plotter.plot(args.var)
