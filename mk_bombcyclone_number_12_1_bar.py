# coding: utf-8
"""
Name: mk_bombcyclone_number_bar.py

make bar graph of cyclone data.

Usage: python3 mk_bombcyclone_number_bar.py -i <csv>

Author: Ryosuke Tomita
Date: 2021/09/21
"""
import argparse
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def parse_args():
    """set csv_file from stdin."""
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--file", help="set csv_file.", type=str)
    p = parser.parse_args()
    args = {"file": p.file}
    return args


def read_csv(csv_file):
    """read csv data using pandas."""
    df = pd.read_csv(csv_file, header=0)
    return df


def concat_str(word_1, word_2):
    """concat two word to get same winter"""
    return (word_1 + "/" + word_2)


def sum_this_winter_data(df):
    """sum same winter data. This function define same winter as previous year 11,12 + this year 1,2,3th."""
    year_list = df['year'].drop_duplicates().tolist()
    year_list_str = list(map(str, year_list))
    df_columns = [concat_str(year_list_str[i], year_list_str[i+1]) \
                  for i in range(len(year_list_str) - 1)]

    same_winter_data = pd.DataFrame(
        index=["all_bomb_cyclone", "oj_all", "oj_strong", "oj_ordinary"],
        columns=df_columns)  # empty DataFrame

    for i, year in enumerate(year_list):
        if year == 2021:
            break

        previous_year_data = df[(df['year'] == year) & (df['month'] == 12)]
        this_year_data = df[(df['year'] == year + 1) & (df['month'] == 1)]
        this_winter_data = pd.concat([previous_year_data, this_year_data]).sum(axis=0)
        same_winter_data[df_columns[i]] = [this_winter_data['number'], this_winter_data['oj_strong'] + this_winter_data['oj_ordinary'],
                                           this_winter_data['oj_strong'], this_winter_data['oj_ordinary']]
    return same_winter_data.T # transpose


def cal_ratio(all_bomb_cyclone, oj_all):
    """Calcurate ratio of oj type bomb cyclone to all cyclone."""
    return (100 * oj_all / all_bomb_cyclone).values


def add_label(graph, oj_ratio):
    for i, rect in enumerate(graph):
        height = rect.get_height() # bar graph height
        plt.rcParams["font.size"] = 40
        if oj_ratio[i] == 0:
            continue
        plt.annotate('{:.1f}'.format(oj_ratio[i]),
                    xy=(rect.get_x() + rect.get_width() / 2, height), # label location settings(x, y)
                    xytext=(0, 3), # distance of bar
                    textcoords="offset points",
                    ha='center',
                    va='bottom',
                    )


def mk_bar(df):
    """make bar graph."""
    fig = plt.figure(figsize=(30, 19))
    ax = fig.add_subplot(111)

    index_num_array = np.array(range(len(df.index)))
    width = 0.2

    for column in df.columns:
        graph = ax.bar(index_num_array, df[column], width=width, label=column)

        if column == "oj_all":
            oj_ratio = cal_ratio(df["all_bomb_cyclone"], df[column])
            add_label(graph, oj_ratio)

        index_num_array = index_num_array + width #avoid overlap bar.

    ax.set_xticks(np.array(range(len(df.index) + 2)))
    ax.set_xticklabels(df.index)
    ax.set_ylabel("The number of bomb cyclone", fontsize=30)
    ax.legend(fontsize=30)
    fig.savefig('test')


def main():
    """
    1. Set csv file from stdin.
    2. Read csv file using pandas.
    3. Define same_winter data as
       previous year December + this year january.
    4. Print basic statistics. using describe().
    5. make bar graph.
    """
    args = parse_args()

    df = read_csv(args["file"])

    same_winter_data = sum_this_winter_data(df)

    print(same_winter_data.describe().round(1))

    mk_bar(same_winter_data)


if __name__ == "__main__":
    main()
