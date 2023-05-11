import pandas as pd
from datetime import datetime
from mdr_lib import get_all_result
from urine_lib import read_df_for_sample_type

organisms = ["Escherichia coli ", "Enterococcus", "Pseudomonas aeruginosa", "Klebsiella" ]

antibiotic_group_data = {
    "Escherichia coli ": {
        "cephems": ["Cefazolin", "Cefotaxim"],
        "Beta lactam inhibitor": ["Piperacillin-tazobactam"],
        "Carbapenems": ["Ertapenem", "Imipenem", "Meropenem"],
        "Lipopeptides": ["Colistin"],
        "Aminoglycosides":["Amikacin"],
        "Quinolones/Fluorquinolones": ["Ciprofloxacin", "Levofloxacin"],
        "Folate Pathway Antagonists": ["Trimethoprim-sulfamethoxazole"],
        "Fosfomycins": ["Fosfomycin"],
        "Nitrofurans": ["Nitrofurantoin"]
    },
    "Klebsiella": {
        "cephems": ["Cefazolin", "Cefotaxim", "Cefepime"],
        "Beta lactam inhibitor": ["Piperacillin-tazobactam"],
        "Carbapenems": ["Ertapenem", "Imipenem", "Meropenem"],
        "Lipopeptides": ["Colistin"],
        "Aminoglycosides":["Amikacin"],
        "Quinolones/Fluorquinolones": ["Ciprofloxacin", "Levofloxacin"],
        "Folate Pathway Antagonists": ["Trimethoprim-sulfamethoxazole"],
        "Fosfomycins": ["Fosfomycin"],
        "Nitrofurans": ["Nitrofurantoin"]
    },
    "Pseudomonas aeruginosa": {
        "cephems": ["Ceftazidime", "Cefepime"],
        "Beta lactam inhibitor": ["Piperacillin-tazobactam"],
        "Carbapenems": ["Imipenem", "Meropenem"],
        "Lipopeptides": ["Colistin"],
        "Aminoglycosides": ["Amikacin", "Gentamicin", "Tobramycin"],
        "Quinolones/Fluorquinolones": ["Ciprofloxacin", "Levofloxacin"]
    },
    "Enterococcus": {
        "Penicillins": ["Ampicillin"],
        "Glycopeptides": ["Vancomycin"],
        "Lipoglycopeptides": ["Teicoplanin"],
        "Fluorquinolones": ["Ciprofloxacin"],
        "Nitrofurans": ["Nitrofurantoin"],
        "Aminoglycosides": ["Gentamicin HL"],
        "Fosfomycins": ["Fosfomycin"],
        "Oxazolidinones": ["Linezolid"]
    }
}

for organism in organisms:
    assert organism in antibiotic_group_data

    status = "all"
    df, antibiotics = read_df_for_sample_type(organism, status)

    group_dict = {}

    def process_groups(row):
        assert row["amr_id"] not in group_dict
        ## Check amr id is unique
        group_dict[row["amr_id"]] = True
        # print("\n\n-----------------------------------------------------------------")
        mdr_count = 0
        for group in antibiotic_group_data[organism]:
            for antibiotic in antibiotics:
                if antibiotic in antibiotic_group_data[organism][group] and row[antibiotic] == "R":
                    mdr_count +=1
                    # print(row["amr_id"], organism, antibiotic, row[antibiotic])
                    break

        return mdr_count > 2

    df["mdr"] = df.apply(lambda x: process_groups(x), axis=1)
    print(len(df))
    print(organism, len(df[df["mdr"] == True])/len(df))

    df.to_csv("../data/final/mdr/" + organism + "_mdr.csv")


