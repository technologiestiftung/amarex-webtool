import argparse
import zipfile

import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class Plotter:
    def load_map(self, map_path):
        """
        Load map in Shapefile format.

        :param map_path: str, path to the Shapefile ZIP containing the map
        :return: GeoDataFrame object, map base to plot the data
        """
        zip_contents = zipfile.ZipFile(map_path)
        zip_contents.extractall()
        dbf, prj, shp, shx = [f for f in sorted(zip_contents.namelist()) for ending in
                              ['dbf', 'prj', 'shp', 'shx'] if f.endswith(ending)]

        map_base = gpd.read_file(shp)

        return map_base

    def load_data(self, data_path):
        """
        Load data in DBF format.

        :param data_path: str, path to the DBF file containing the data to plot
        """
        # Convert DBF file to Pandas dataframe
        data = gpd.read_file(data_path).drop("geometry", axis=1)

        return data

    def calculate_deviation(self, data, data_ref):
        """
        Calculate deviation of water balance of an urban area from the natural conditions
        as a pairwise comparison of evapotranspiration, surface runoff and infiltration.

        :param data: Pandas dataframe, actual urban data.
        :param data_ref: Pandas dataframe, natural reference.
        :return: Pandas dataframe, data with water balance deviation.
        """
        # Add reference values
        precipitation = 1000  # TODO: Hardcoded a random value, where do I get this information?

        data = pd.merge(data, data_ref, on="CODE")
        data["DEV"] = 1/2 * (abs(data["VERDUNSTUN_REF"] - data["VERDUNSTUN"]) +  # TODO: Here we should use evapotranspiration, not evaporation
                             abs(data["RI_REF"] - data["RI"]) +
                             abs(data["ROW_REF"] - data["ROW"])
                             ) * 1/precipitation  # TODO: Check formula, 100% doesn't make sense to me, this is just 1

        return data

    def plot(self, var, map_base, data):
        """
        Plot choropleth map.

        :param var: str, variable to plot.
        """
        var_codes = {
            "surface_runoff": "ROW",
            "infiltration": "RI",
            "evaporation": "VERDUNSTUN",
            "deviation": "DEV"
        }

        merged_df = map_base.set_index("SCHLUESSEL").join(data.set_index("CODE"))
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
    parser.add_argument("data_ref_path", help="Path to the DBF file containing the reference data")
    parser.add_argument("var",
                        choices=["surface_runoff", "infiltration", "evaporation", "deviation"],
                        help="Variable to plot")

    args = parser.parse_args()

    # Load map and data
    plotter = Plotter()
    map_base = plotter.load_map(args.map_path)
    data = plotter.load_data(args.data_path)

    # Create a synthetic dataframe for testing
    data_ref = plotter.load_data(args.data_ref_path)
    # Add and subtract random values
    data_ref["ROW_REF"] = data_ref["ROW"].to_numpy() - np.random.uniform(0.0, 3.0)
    data_ref["RI_REF"] = data_ref["RI"].to_numpy() + np.random.uniform(0.0, 3.0)
    data_ref["VERDUNSTUN_REF"] = data_ref["VERDUNSTUN"].to_numpy() + np.random.uniform(0.0, 3.0)
    # Normalize negative values to zero
    data_ref["ROW_REF"] = data_ref["ROW_REF"].clip(lower=0)
    data_ref["RI_REF"] = data_ref["RI_REF"].clip(lower=0)
    data_ref["VERDUNSTUN"] = data_ref["VERDUNSTUN"].clip(lower=0)
    # Get rid of unnecessary columns
    data_ref = data_ref[["CODE", "ROW_REF", "RI_REF", "VERDUNSTUN_REF"]]

    # Add water balance deviation to the data
    data = plotter.calculate_deviation(data, data_ref)

    # plot
    plotter.plot(args.var, map_base, data)
