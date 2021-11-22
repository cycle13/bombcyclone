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
import mymatlib


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


class SnowData:

    def __init__(self, file_: str, prefecture: str):
        self.csv_file = file_
        self.prefecture = prefecture
        self.header = None

    def get_city_name(self) -> list:
        city_df = pd.read_csv(
                self.csv_file,
                skiprows=2,
                header=None,
                nrows=1,
                encoding='s-jis'
                ).astype(str)
        city_list = list(set(city_df.loc[0]))
        city_list.remove("nan")
        return city_list

    def _get_csv_header(self) -> list:
        header_parts = pd.read_csv(
            self.csv_file,
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


    def read_csv(self) -> pd.DataFrame:
        header = self._get_csv_header()
        self.df = pd.read_csv(self.csv_file,
            skiprows=6, usecols=tuple(range(len(header))),
            names=tuple(header),
            index_col=0,
            encoding='s-jis')
        return self.df


    def ave_prefecture(self, index: str, city_list: list) -> pd.DataFrame:
        self.df[("all_city"+index)] = 0
        for city in city_list:
            self.df[("all_city"+index)] += self.df[(city+index)].fillna(0)

        self.df[("all_city"+index)] = self.df[("all_city"+index)] / len(city_list)
        return self.df


def ave_hokuriku(ins_dict: dict, index: str):
    ins_dict["hukui"].df["ave_hokuriku"] = 0
    sum_hokuriku = ins_dict["hukui"].df["ave_hokuriku"]
    for prefecture, snow_data in ins_dict.items():
        sum_hokuriku += snow_data.df[("all_city" + index)]
    return sum_hokuriku / len(ins_dict)



def main():
    prefecture_list, file_list = mk_file_list(abspath("snow_data_long"))
    ins_list = []
    for i, file_ in enumerate(file_list):
        snow_data = SnowData(file_, prefecture_list[i])
        city_list = snow_data.get_city_name()
        df = snow_data.read_csv()

        df = snow_data.ave_prefecture("降雪量合計", city_list)
        df = snow_data.ave_prefecture("降雪量合計平年値", city_list)
        df = snow_data.ave_prefecture("降雪量合計過去10年平均", city_list)

        ins_list.append(snow_data)

    ins_dict = dict(zip(prefecture_list, ins_list))

    hokuriku_snow_ave = ave_hokuriku(ins_dict, "降雪量合計")
    hokuriku_snow_heinen_ave = ave_hokuriku(ins_dict, "降雪量合計平年値")
    hokuriku_snow_10year_ave = ave_hokuriku(ins_dict, "降雪量合計過去10年平均")
    #plt_set = mymatlib.PltSet()
    x = ins_dict["hukui"].df.index

    #plt_set.plot(x, hokuriku_snow_ave, "date", "snowfall (cm/day)", xisDate=True)
    #plt_set.ave_line(x, hokuriku_snow_heinen_ave, color="green")
    #plt_set.ave_line(x, hokuriku_snow_10year_ave, color="red")
    #plt_set.save_fig("snow")

    plt_set_2 = mymatlib.PltSet()
    plt_set_2.plot(x, hokuriku_snow_ave.cumsum(), "date", "snowfall integration (cm)", xisDate=True)
    plt_set_2.plot(x, hokuriku_snow_heinen_ave.cumsum(), "date", "snowfall heinen integration (cm)", xisDate=True)
    plt_set_2.plot(x, hokuriku_snow_10year_ave.cumsum(), "date", "snowfall 10year_ave integration (cm)", xisDate=True)
    plt_set_2.save_fig("snow_integration")

    print(hokuriku_snow_ave.mean())
    print(hokuriku_snow_heinen_ave.std())


if __name__ == "__main__":
    main()
