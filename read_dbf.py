import ctypes
import geopandas as gpd


# Define the struct for AbimoInputRecord
class AbimoInputRecord(ctypes.Structure):
    _fields_ = [
        ("usage", ctypes.c_int),
        ("code", ctypes.c_char_p),
        ("precipitationYear", ctypes.c_int),
        ("precipitationSummer", ctypes.c_int),
        ("depthToWaterTable", ctypes.c_float),
        ("type", ctypes.c_int),
        ("fieldCapacity_30", ctypes.c_int),
        ("fieldCapacity_150", ctypes.c_int),
        ("district", ctypes.c_int),
        ("mainFractionBuiltSealed", ctypes.c_float),
        ("mainFractionUnbuiltSealed", ctypes.c_float),
        ("roadFractionSealed", ctypes.c_float),
        ("builtSealedFractionConnected", ctypes.c_float),
        ("unbuiltSealedFractionConnected", ctypes.c_float),
        ("unbuiltSealedFractionConnected", ctypes.c_float),
        ("roadSealedFractionConnected", ctypes.c_float),
        ("BELAG1", ctypes.c_float),
        ("BELAG2", ctypes.c_float),
        ("BELAG3", ctypes.c_float),
        ("BELAG4", ctypes.c_float),
        ("STR_BELAG1", ctypes.c_float),
        ("STR_BELAG2", ctypes.c_float),
        ("STR_BELAG3", ctypes.c_float),
        ("STR_BELAG4", ctypes.c_float),
        ("mainArea", ctypes.c_float),
        ("roadArea", ctypes.c_float),
    ]


# Define the struct for AbimoOutputRecord
class AbimoOutputRecord(ctypes.Structure):
    _fields_ = [
        ("code_CODE", ctypes.c_char_p),
        ("totalRunoff_R", ctypes.c_float),
        ("surfaceRunoff_ROW", ctypes.c_float),
        ("infiltration_RI", ctypes.c_float),
        ("totalRunoffFlow_RVOL", ctypes.c_float),
        ("surfaceRunoffFlow_ROWVOL", ctypes.c_float),
        ("infiltrationFlow_RIVOL", ctypes.c_float),
        ("totalArea_FLAECHE", ctypes.c_float),
        ("evaporation_VERDUNSTUN", ctypes.c_float),
    ]


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

    # Create an array to hold the AbimoInputRecord objects
    records = []

    # Iterate over DataFrame rows and create AbimoInputRecord objects
    for index, row in abimo_df.iterrows():
        record = AbimoInputRecord(
            usage=row["usage"],
            code=row["code"].encode("utf-8"),
            precipitationYear=row["precipitationYear"],
            precipitationSummer=row["precipitationSummer"],
            depthToWaterTable=row["depthToWaterTable"],
            type=row["type"],
            fieldCapacity_30=row["fieldCapacity_30"],
            fieldCapacity_150=row["fieldCapacity_150"],
            district=row["district"],
            mainFractionBuiltSealed=row["mainFractionBuiltSealed"],
            mainFractionUnbuiltSealed=row["mainFractionUnbuiltSealed"],
            roadFractionSealed=row["roadFractionSealed"],
            builtSealedFractionConnected=row["builtSealedFractionConnected"],
            unbuiltSealedFractionConnected=row["unbuiltSealedFractionConnected"],
            roadSealedFractionConnected=row["roadSealedFractionConnected"],
            BELAG1=row["BELAG1"],
            BELAG2=row["BELAG2"],
            BELAG3=row["BELAG3"],
            BELAG4=row["BELAG4"],
            STR_BELAG1=row["STR_BELAG1"],
            STR_BELAG2=row["STR_BELAG2"],
            STR_BELAG3=row["STR_BELAG3"],
            STR_BELAG4=row["STR_BELAG4"],
            mainArea=row["mainArea"],
            roadArea=row["roadArea"],
        )
        records.append(record)

    records_n = abimo_df.shape[0]

    return records, records_n


def to_float_fraction(value):
    """
    Helper function.
    Convert value to float fraction.

    :param value: int or float, value to convert
    :return: float, value as fraction
    """
    return float(value) / 100.0
