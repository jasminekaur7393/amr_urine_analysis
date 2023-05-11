import pandas as pd
import numpy as np
from urine_lib import parse_date, read_df_for_sample_type, custom_aggregate_number, custom_aggregate

organisms = ["Escherichia coli ", "Enterococcus", "Pseudomonas aeruginosa", "Klebsiella"]


for organism in organisms:
    status = "all"
    df, antibiotics = read_df_for_sample_type(organism, status)
    print("---------------------------------------------" + organism)
    for year in df["year"].unique():
        print("-------------------", year)
        df_year = df[df["year"] == year]
        for antibiotic in antibiotics:
            result = df_year[antibiotic].agg(custom_aggregate_number)
            result2 = df_year[antibiotic].agg(custom_aggregate)
            print(antibiotic + ", " + str(result) + "(" + str(result2)+ ") " )