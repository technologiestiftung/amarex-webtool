import geopandas as gpd
import pandas as pd


def read_file():
    """
    Read and print the contents of a DBF file.
    """
    # TODO: Make this path configurable, use relative path
    input_file = "/Users/guadaluperomero/ProjectsTSB/amarex/amarex-webtool/data/abimo_2019_mitstrassen.dbf"

    # Convert DBF file to Pandas dataframe
    df = gpd.read_file(input_file).drop("geometry", axis=1)

    return df


def to_abimo_array(df):
    """

    :param df: Pandas DataFrame, input data to process
    :return abimo_array: list, array of arrays following the AbimoInputRecord format
    :return shape: tuple, containing the number of rows and columns
    """
    # TODO: Move mapping and float_fraction_columns out of this function
    mapping = {
        "NUTZUNG": "usage",                                                 # 0/  int
        "CODE": "code",                                                     # 1/  QString
        "REGENJA": "precipitationYear",                                     # 2/  int
        "REGENSO": "precipitationSummer",                                   # 3/  int
        "FLUR": "depthToWaterTable",                                        # 4/  float
        "TYP": "type",                                                      # 5/  int
        "FELD_30": "fieldCapacity_30",                                      # 6/  int
        "FELD_150": "fieldCapacity_150",                                    # 7/  int
        "BEZIRK": "district",                                               # 8/  int
        "PROBAU": "mainFractionBuiltSealed",                                # 9/  float fraction
        "PROVGU": "mainFractionUnbuiltSealed",                              # 10/ float fraction
        "VGSTRASSE": "roadFractionSealed",                                  # 11/ float fraction
        "KAN_BEB": "builtSealedFractionConnected",                          # 12/ float fraction
        "KAN_VGU": "unbuiltSealedFractionConnected",                        # 13/ float fraction
        "KAN_STR": "roadSealedFractionConnected",                           # 14/ float fraction

        "BELAG1": "BELAG1",                                                 # 15/ float fraction [1]
        "BELAG2": "BELAG2",                                                 # 16/ float fraction [2]
        "BELAG3": "BELAG3",                                                 # 17/ float fraction [3]
        "BELAG4": "BELAG4",                                                 # 18/ float fraction [4]

        "STR_BELAG1": "STR_BELAG1",                                         # 19/ float fraction [1]
        "STR_BELAG2": "STR_BELAG2",                                         # 20/ float fraction [2]
        "STR_BELAG3": "STR_BELAG3",                                         # 21/ float fraction [3]
        "STR_BELAG4": "STR_BELAG4",                                         # 22/ float fraction [4]

        "FLGES": "mainArea",                                                # 23/ float
        "STR_FLGES": "roadArea"                                             # 24/ float
    }

    float_fraction_columns = [
        "PROBAU",
        "PROVGU",
        "VGSTRASSE",
        "KAN_BEB",
        "KAN_VGU",
        "KAN_STR",
        "BELAG1",
        "BELAG2",
        "BELAG3",
        "BELAG4",
        "STR_BELAG1",
        "STR_BELAG2",
        "STR_BELAG3",
        "STR_BELAG4",
    ]

    # Change selected columns to float fractions
    df[float_fraction_columns] = df[float_fraction_columns].applymap(lambda x: to_float_fraction(x))

    # Rename columns
    df_renamed = df.rename(columns=mapping)

    # Delete unnecessary columns
    columns_to_keep = list(mapping.values())
    abimo_df = df_renamed[columns_to_keep]

    # Convert DataFrame to array
    abimo_array = abimo_df.values.tolist()

    # Flatten the array
    abimo_array_flat = [col for row in abimo_array
                            for col in row]

    # Get the number of rows and columns
    shape = abimo_df.shape

    return abimo_array_flat, shape


def to_float_fraction(value):
    """
    Helper function.
    Convert value to float fraction.

    :param value: int or float, value to convert
    :return: float, value as fraction
    """
    return float(value) / 100.0


# TODO: Delete later, just for testing
df = read_file()
abimo_array, shape = to_abimo_array(df)
