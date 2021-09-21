# coding: utf-8
"""
Name: mk_bombcycloen_number_bar.py

make bar graph of cycloen data.

Usage:

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
        index=["all_cyclone", "oj_strong", "oj_ordinary", "oj_all"],
        columns=df_columns)  # empty DataFrame

    for i, year in enumerate(year_list):
        if year == 2020:
            break

        previous_year_data = df[(df['year'] == year) & (df['month'] >= 11)]
        this_year_data = df[(df['year'] == year + 1) & (df['month'] <= 3)]
        this_winter_data = pd.concat([previous_year_data, this_year_data]).sum(axis=0)
        same_winter_data[df_columns[i]] = [this_winter_data['number'], this_winter_data['oj_strong'], this_winter_data['oj_ordinary'], this_winter_data['oj_strong'] + this_winter_data['oj_ordinary']]
    return same_winter_data


def mk_bar(df):
    fig = plt.figure(figsize=(15, 6))
    ax = fig.add_subplot(111)

    columns_num_array = np.array(range(len(df.columns)))
    width = 0.1

    for index in df.index:
        ax.bar(columns_num_array, df.loc[index], width=width, label=index)
        columns_num_array = columns_num_array + width #avoid overlap bar.

    ax.set_xticks(np.array(range(len(df.columns) + 2)))
    ax.set_xticklabels(df.columns)
    ax.set_ylabel("The number of bomb cycloen")
    ax.legend()
    fig.savefig('test')


def main():
    args = parse_args()

    df = read_csv(args["file"])

    same_winter_data = sum_this_winter_data(df)
    print(same_winter_data.describe())

    mk_bar(same_winter_data)


if __name__ == "__main__":
    main()
