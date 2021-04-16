"""
To fix the yield from the UPTSO preprocessed files
both Schwaller & Lowe versions
Filters all reactions with faulty/no yield
and keeps minimum number of columns

Version: 1.31: 2021-04-16; A.M.
@author: Alexander Minidis (DocMinus)

license: MIT License
Copyright (c) 2021 DocMinus
"""

import pandas as pd
import numpy as np


def deconvolute_yield(row):
    text_yield_data = row["TextMinedYield"]
    calc_yield_data = row["CalculatedYield"]
    my_text_yield = 0
    my_calc_yield = 0

    if 0 < text_yield_data <= 100:
        my_text_yield = text_yield_data
    if 0 < calc_yield_data <= 100:
        my_calc_yield = calc_yield_data

    out_yield = my_text_yield
    if my_calc_yield > my_text_yield:
        out_yield = my_calc_yield

    return out_yield


def main():
    #
    # change these two lines accordingly
    #
    in_file = "/data/uspto/Lowe_processed_and_yield_curated/2001_Sep2016_USPTOapplications_smiles.rsmi"
    out_file = "/data/uspto/Lowe_processed_and_yield_curated/2001_Sep2016_USPTOapplications_smiles_yield_ok_cropped_data.csv"

    print("Reading...")
    # read first line only.
    with open(in_file) as file_in:
        first_line = file_in.readline()

    to_skip = 0  # Lowe data set, contains no initial comments
    if first_line.startswith("# Original"):
        to_skip = 2  # Schwaller data set, contains comments

    data = pd.read_csv(in_file, sep="\t", low_memory=False, skiprows=to_skip)

    # optional: create your own ID; for example good for use in a database
    data["myID"] = np.arange(len(data))
    id_prefix = "ID"  # change as you like
    data["myID"] = data["myID"].apply(lambda x: id_prefix + "{0:0>8}".format(x))
    cols = data.columns.tolist()  # also optional.
    cols = cols[-1:] + cols[:-1]  # I prefer the ID to come first
    data = data[cols]

    print("Massaging...")
    # Remove empty (NaNs) only if both have simultaneous NaNs.
    # If no yield, then of no interest
    data.dropna(subset=["TextMinedYield", "CalculatedYield"], how="all", inplace=True)
    # Optional removal of whole columns:
    """
    Columns in Schwaller dataset: (Lowe dataset marked with *)
    Source                   
    Target                   
    CanonicalizedReaction    
    OriginalReaction (= ReactionSmiles*)         
    PatentNumber*            
    ParagraphNum*             
    Year*                     
    TextMinedYield*           
    CalculatedYield*          
    """
    data.drop(
        ["PatentNumber", "ParagraphNum", "Year"], axis=1, inplace=True,
    )

    # Keep only digits, remove all >, %, etc.
    # Easier (for overview) to replace step-wise, too many exceptions become otherwise converted wrong.
    # Goal is to keep largest yield
    #
    # CalculatedYield is simplest to convert
    data["CalculatedYield"] = data["CalculatedYield"].str.rstrip("%")
    # TextMinedYield has multiple tricky combos (single regex could solve, but wouldn't be readable)
    data["TextMinedYield"] = data["TextMinedYield"].str.lstrip("~")
    data["TextMinedYield"] = data["TextMinedYield"].str.rstrip("%")
    data["TextMinedYield"] = data["TextMinedYield"].str.replace(">=", "", regex=True)
    data["TextMinedYield"] = data["TextMinedYield"].str.replace(">", "", regex=True)
    data["TextMinedYield"] = data["TextMinedYield"].str.replace("<", "", regex=True)
    # How to treat x to y% is a matter of taste; here it becomes last (i.e. highest value)
    data["TextMinedYield"] = data["TextMinedYield"].str.replace(
        "\d{1,2}\sto\s", "", regex=True
    )

    data["TextMinedYield"] = data["TextMinedYield"].replace(np.nan, 0)
    data["CalculatedYield"] = data["CalculatedYield"].replace(np.nan, 0)
    data["TextMinedYield"] = pd.to_numeric(data["TextMinedYield"], errors="coerce")
    data["CalculatedYield"] = pd.to_numeric(data["CalculatedYield"], errors="coerce")

    # correct the input yields and keep only one final yield. Remove 0 since stemming from NaN.
    print("Converting...")
    data["Yield"] = data.apply(deconvolute_yield, axis=1)
    data.drop(["TextMinedYield", "CalculatedYield"], axis=1, inplace=True)
    data = data[data["Yield"] != 0]
    print(data.head())

    # Write to e.g. csv.; use tab separator.
    # sooner or later in chemistry one will encounter "," ";" or " " used in structures or text fields.
    print("Writing...")
    # data.to_csv(out_file, sep="\t")
    print("Done.")

    return None


if __name__ == "__main__":
    main()
