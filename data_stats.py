import pandas as pd
from datetime import datetime, timedelta
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

from urine_lib import parse_date
from urine_lib import read_df_for_sample_type

organisms = ["Escherichia coli ", "Enterococcus", "Pseudomonas aeruginosa", "Klebsiella"]

colorarray = [
                    [192/255, 162/255, 192/255, 1],
                    [159/255, 185/255, 170/255, 1],
                    [168/255, 212/255, 231/255, 1],
                    [215/255, 168/255, 163/255, 1],
                    [162/255, 172/255, 209/255, 1]
                ]
cmap = ListedColormap(colorarray)

for organism in organisms:
    status = "all"
    df, antibiotics = read_df_for_sample_type(organism, status)
    df["collection_date"] = df.apply(lambda x: parse_date(x["collection_date"]), axis=1)


    def plot_graph(x,sample_type, stack_by):
        fig, ax = plt.subplots(figsize=(8, 6))
        column_wise_count = df.groupby([x, stack_by])["amr_id"].count().sort_values()

        column_wise_count = column_wise_count.to_frame().reset_index(level=[x, stack_by])

        column_wise_count = column_wise_count.pivot(index=x, columns=stack_by).fillna(0)

        column_wise_count['sum_cols'] = column_wise_count.sum(axis=1)
        column_wise_count = column_wise_count.sort_values('sum_cols')
        column_wise_count = column_wise_count.drop(columns=['sum_cols']).sort_index()
        ax = column_wise_count.plot(kind='bar', stacked=True, colormap=cmap)
        for c in ax.containers:
            labels = [int(v.get_height()) if v.get_height() > 10 else '' for v in c]
            ax.bar_label(c, labels=labels, label_type='center', size=3)
        # plt.legend(["16s rRNA Sequencing", "Biochemical test", "Conventional identification by microscopy/phenotype", "MaldiToff", "Proteomics", "Vitek-2", "Whole Genome Sequencing"])

        # plt.legend(["Enterococcus", "Escherichia coli", "Klebsiella", "Pseudomonas aeruginosa"])
        plt.legend(["ICU", "OPD", "Ward"])
        ax.set_title(x + '-wise number of records from ' + sample_type)
        plt.tight_layout()
        plt.xticks(fontsize=6)
        plt.savefig('../figures/general/' + x + '_' + sample_type +"_" + stack_by +'2.pdf')
        plt.close()

    def plot_state(x,sample_type):
        fig, ax = plt.subplots(figsize=(8, 6))
        column_wise_count = df.groupby(x)["amr_id"].count().sort_values()
        ax = column_wise_count.plot(kind='bar')
        for c in ax.containers:
            labels = [int(v.get_height()) if v.get_height() > 0 else '' for v in c]
            ax.bar_label(c, labels=labels, label_type='edge', size=5)
        # plt.legend(["Enterococcus", "Escherichia coli", "Klebsiella", "Pseudomonas aeruginosa"])
        ax.set_title(x + '-wise number of records from ' + sample_type)
        plt.tight_layout()
        plt.xticks(fontsize=8)
        plt.savefig('../figures/general/' + x + '.pdf')
        plt.close()


    # plot_state("state","Urine")

    # plot_graph("organism","Urine")
    # plot_graph("state", "Urine", "location_type")

    # plot_graph("state","Urine", "organism_name")
    # plot_graph("gender","Urine", "organism_name")
    # plot_graph("infection_type","Urine", "organism_name")
    #plot_graph("collection_date","Urine", "organism_name")

    # plot_graph("state","Urine", "location_type")
    plot_graph("gender","Urine", "location_type")
    # plot_graph("infection_type","Urine", "location_type")
    # plot_graph("collection_date","Urine", "location_type")



    #df.plot(x="amr_id", y=[antibiotics], kind="bar")
    #plot_graph("hospital_department","Urine")




