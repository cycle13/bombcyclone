# coding: utf-8
"""
Name: snow_analyze.py

Define heavy snow.

Usage:python3 snow_analyze.py

Author: Ryosuke Tomita
Date: 2021/10/20
"""
from typing import Tuple
import os
from os.path import abspath, join
import pandas as pd


def mk_file_list(dir_: str) -> Tuple[list, list]:
    prefecture_list = [
            file_.replace(".csv", "")
            for file_ in os.listdir(dir_)
    ]
    file_list = [
            join(dir_, file_)
            for file_ in os.listdir(dir_)
    ]
    return prefecture_list, file_list


def get_csv_header(file_: str) -> list:
    header_parts = pd.read_csv(
        file_,
        skiprows=2,
        header=None,
        nrows=4,
        encoding='s-jis'
    ).astype(str)
    header = [
        (header_parts[i][0] + header_parts[i][1].replace("(cm)", "") + header_parts[i][2].replace("(cm)", "")
        + header_parts[i][3]).replace("nan", "")
        for i in range(len(header_parts.columns))
    ]
    return header


def get_city_name(file_: str) -> list:
    city_df = pd.read_csv(
            file_,
            skiprows=2,
            header=None,
            nrows=1,
            encoding='s-jis'
            ).astype(str)
    city_list = list(set(city_df.loc[0]))
    city_list.remove("nan")
    return city_list


def read_csv(file_: str, header: list) -> pd.DataFrame:

    data = pd.read_csv(file_,
        skiprows=6, usecols=tuple(range(len(header))),
        names=tuple(header),
        index_col=0,
        encoding='s-jis')
    return data


def ave_prefecture(df: pd.DataFrame, index: str,city_list: list) -> pd.DataFrame:
    df[("all_city"+index)] = 0
    for city in city_list:
        df[("all_city"+index)] += df[(city+"降雪量合計")]
    df[("all_city"+index)] = df[("all_city"+index)] / len(city_list)
    return df


def ave_hokuriku(df: pd.DataFrame)


def main():
    prefecture_list, file_list = mk_file_list(abspath("snow_data"))

    for i, file_ in enumerate(file_list):
        header = get_csv_header(file_)
        city_list = get_city_name(file_)
        df = read_csv(file_, header)

        df = ave_prefecture(df, "降雪量合計", city_list)
        df = ave_prefecture(df, "降雪量合計平年値", city_list)
        prefecture_list[i]

    #df.to_csv("tmp.csv", encoding="s-jis")

    #city_data = {
    #        city: CityData(city)
    #        for city in city_list
    #    }


if __name__ == "__main__":
    main()
