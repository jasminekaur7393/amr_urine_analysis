# Import libraries
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scikits.bootstrap as boot
from urine_lib import read_df_for_sample_type

organisms = ["Escherichia coli ", "Enterococcus", "Pseudomonas aeruginosa", "Klebsiella"]

for org in organisms:
    print("--------------------------Processing------------------" + org)
    status = "all"
    df, antibiotics = read_df_for_sample_type(org, status)
    # print(df["collection_date"])

    #zones = df_all["zone"].unique()

    #for zone in zones:
        #df = df_all[df_all["zone"] == zone].copy()

    # Parse dates
    def parse_date(date_str):
        dob_obj = None
        date_format_strs = ["%d/%m/%y", "%Y-%m-%d"]
        for date_format_str in date_format_strs:
            # print(date_str)
            try:
                dob_obj = datetime.strptime(date_str, date_format_str)
                break
            except Exception as e:
                print(dob_obj, e)
                pass

        if dob_obj is not None and dob_obj.year > 2023:
            dob_obj = dob_obj.replace(year=(dob_obj.year - 100))

        return dob_obj.strftime("%m-%Y")

    count_ab= {}

    def calculate_count(df):
        global count_ab
        for antibiotic in antibiotics:
            count_ab[antibiotic] = df[antibiotic].count()
        return count_ab

    # Define custom aggregation function to calculate proportion
    def custom_aggregate(series, susceptibility="R"):
        unique_counts = round(series.value_counts(normalize=True) * 100, 2)
        return unique_counts[susceptibility] if susceptibility in unique_counts else np.nan

    def custom_aggregate2(series):
        series = series.ravel()
        series = pd.Series(series)
        return custom_aggregate(series)

    # Sampling function
    def sampling(data, month, year, antibiotic):
        date_str =  str(month) + "-" + str(year)
        try:
            month_year_obj = pd.to_datetime(date_str, format='%m-%Y')
        except:
            print("Exception for date", date_str)
            return

        sampled_df = data[data["collection_date"] == month_year_obj]
        if antibiotic not in sampled_df.columns:
            return  # For antibiotics where values are missing
        else:
            sampled_df = sampled_df[[antibiotic]]
        mean = custom_aggregate(sampled_df[antibiotic])
        if np.isnan(mean):
            return
        # (lower, upper) = boot.ci(sampled_df, custom_aggregate2, n_samples=int(len(sampled_df)))
        (lower, upper) = boot.ci(sampled_df, custom_aggregate2)
        return {'lower': lower, 'mean': mean, 'upper': upper, "collection_date": month_year_obj}

    # Define specific colors for each antibiotic
    ab_color_dict = {"Vancomycin": "blue", "Nitrofurantoin": "grey", "Linezolid": "orange", "Teicoplanin": "red",
                     "Ampicillin": "purple", "Gentamicin HL": "hotpink", "Ciprofloxacin": "green", "Fosfomycin": "lime",
                     "Amikacin": "blue", "Piperacillin-tazobactam": "darkgoldenrod",
                     "Imipenem": "purple", "Meropenem": "maroon", "Trimethoprim-sulfamethoxazole": "olive",
                     "Cefotaxime": "orange", "Ertapenem": "red", "Levofloxacin": "yellow", "Cefazolin": "magenta",
                     "Colistin": "darkturquoise", "Cefepime": "red",
                     "Ceftazidime": "orange", "Gentamicin": "olive", "Tobramycin": "grey"}


    calculate_count(df)

    print(count_ab)

    def custom_color(antibiotic):
        return ab_color_dict[antibiotic]

    # Plot rolling average
    def plot_core(df1, is_rolling, antibiotic_name, ax):
        if is_rolling:
            try:
                df1 = df1.rolling(window=3, center=True, min_periods=1).mean()
                ax.plot(df1.index, df1['mean'], label=antibiotic_name + " : " + str(count_ab[antibiotic_name]), color=custom_color(antibiotic_name))
                ax.fill_between(df1.index, df1["upper"], df1["lower"], facecolor=custom_color(antibiotic_name), alpha=0.2)
            except Exception as e:
                print("Error:", e, antibiotic_name)
                print(df1)
                return
        else:
            ax.plot(df1["collection_date"], df1['mean'], label=antibiotic_name + " : " + str(count_ab[antibiotic_name]), color=custom_color(antibiotic_name))
            try:
                ax.fill_between(df1["collection_date"], df1["upper"], df1["lower"], facecolor=custom_color(antibiotic_name),
                                alpha=0.2)
            except:
                pass


    # Set collection date to correct format
    # print(df["collection_date"])
    df["collection_date"] = df.apply(lambda x: parse_date(x["collection_date"]), axis=1)
    # print(df["collection_date"])
    df["collection_date"] = pd.to_datetime(df["collection_date"], format='%m-%Y')
    # print(df["collection_date"])

    # df.to_csv(org + "_gen.csv")

    # Plot graphs
    fig, ax = plt.subplots(figsize=(18, 10), tight_layout=True)
    for idx, antibiotic_name in enumerate(antibiotics):
        print("\t..... Processing", antibiotic_name)
        df1 = pd.DataFrame(columns=['lower', 'mean', 'upper', 'collection_date'])
        for i in range(2017, 2022):
            for j in range(1, 13):
                    try:
                        new_row = sampling(df, j, i, antibiotic_name)
                    except:
                        continue
                    if new_row == None:
                        continue
                    df1 = df1.append(new_row, ignore_index=True)

        df1.index = df1["collection_date"]
        plot_core(df1, True, antibiotic_name, ax)
        # df1 = df1.rolling(window=3, center=True, min_periods=1).mean()
        # df1.to_csv("../data/" + antibiotic_name + ".csv")

    plt.title("Temporal change in Resistance pattern for " + org)# + "in " + zone + " zone")
    plt.xlabel("Date of sample collection")
    plt.ylabel("Percentage Resistance")
    ax.legend(frameon=True, ncol=4, loc='upper right')
    plt.ylim(0, 100)

    plt.savefig('../figures/with_22/temporal_' + org +'.pdf')# + "_" + zone +'.pdf')
