# coding: utf-8
"""
Name: snow_analyze.py

Define heavy snow.

Usage:python3 snow_analyze.py

Author: Ryosuke Tomita
Date: 2021/10/20
"""
import os
from os.path import abspath, join
import pandas as pd
import numpy as np
import mymatlib


def mk_file_list(dir_: str) -> list:
    file_list = [
            join(dir_, file_)
            for file_ in sorted(os.listdir(dir_))
            if ".csv" in file_
    ]
    return file_list


def get_csv_header(file_: str) -> list:
    header_parts = pd.read_csv(
        file_,
        skiprows=2,
        header=None,
        nrows=4,
        encoding='s-jis'
    ).astype(str)
    header = [
        (header_parts[i][0] + header_parts[i][1] + header_parts[i][2]
        + header_parts[i][3]).replace("nan", "")
        for i in range(len(header_parts.columns))
    ]
    return header

def read_csv(file_: str, header: list) -> pd.DataFrame:

    data = pd.read_csv(file_,
        skiprows=6, usecols=tuple(range(len(header))),
        names=tuple(header),
        index_col=0,
        encoding='s-jis')
#    print(data.filter(like="氷", axis=1))
    return data


def cut_snow_data(df: pd.DataFrame, city: str, city_ins):
    city_snow_data = df.filter(like=city, axis=1).filter(like="最深積雪", axis=1)
    city_snow_this_year = city_snow_data.filter(items=[(city+"最深積雪(cm)")])
    city_snow_10ave = city_snow_data.filter(items=[(city+"最深積雪(cm)過去10年平均(cm)")])
    city_snow_ordinary = city_snow_data.filter(items=[(city+"最深積雪(cm)平年値(cm)")])

    city_ins.add_data(
        city_snow_this_year,
        city_snow_10ave,
        city_snow_ordinary,
    )


def ave_all_city(city_data: dict):
    cnt = 0
    all_city_data = 0
    for city, city_ins in city_data.items():
        if cnt == 0:
            all_city_data = city_ins.all_data.values
        else:
            all_city_data += city_ins.all_data.values
        cnt += 1
    ave_city_data = all_city_data.T / len(city_data)
    return ave_city_data


class CityData:

    def __init__(self, city: str):
        self.city = city
        self.snow_this_year = pd.DataFrame()
        self.snow_10ave = pd.DataFrame()
        self.snow_ordinary = pd.DataFrame()
        self.snow_ratio = pd.DataFrame()
        self.all_data = pd.DataFrame()

    def add_data(self, snow_this_year: pd.DataFrame, snow_10ave: pd.DataFrame, snow_ordinary: pd.DataFrame):
        if self.snow_this_year.empty:
            self.snow_this_year = snow_this_year
            self.snow_10ave = snow_10ave
            self.snow_ordinary = snow_ordinary
            self.snow_ratio = snow_ordinary

        else:
            self.snow_this_year = pd.concat([self.snow_this_year, snow_this_year], sort=True)
            self.snow_10ave = pd.concat([self.snow_10ave, snow_10ave], sort=True)
            self.snow_ordinary = pd.concat([self.snow_ordinary, snow_ordinary], sort=True)

            ordinary_monthly_mean = float(snow_ordinary.mean())
            if ordinary_monthly_mean == 0:
                snow_ratio = snow_ordinary.copy()
                self.snow_ratio = pd.concat([self.snow_ratio, snow_ratio])
            else:
                snow_ratio = pd.DataFrame((snow_this_year.values / ordinary_monthly_mean), columns=[(self.city + "最深積雪(cm)平年値(cm)")], index=snow_ordinary.index)
                self.snow_ratio = pd.concat([self.snow_ratio, snow_ratio])

    def concat_data(self):
        self.snow_ratio = self.snow_ratio.rename(columns={(self.city + "最深積雪(cm)平年値(cm)"): (self.city + "最深積雪/平年値平均(cm)")})
        self.all_data = pd.concat(
            [
            self.snow_this_year,
            self.snow_10ave,
            self.snow_ordinary,
            self.snow_ratio,
            ], axis=1, sort=True
        )
        self.all_data.to_csv("tmp.csv")


def main():
    dir_ = abspath("./snowdata")
    file_list = mk_file_list(dir_)

    citys = ["氷見", "伏木", "朝日", "魚津", "富山" ]
    city_data = {
            city: CityData(city)
            for city in citys
        }

    header = get_csv_header(file_list[0])

    for file_ in file_list:
        df= read_csv(file_, header)
        for city in citys:
            cut_snow_data(df, city, city_data[city])

    for city in citys:
        city_data[city].concat_data()

    ave_city_data_all = ave_all_city(city_data)
    plt_set = mymatlib.PltSet()
    x = city_data["氷見"].snow_this_year.index

    plt_set.plot(x, ave_city_data_all[0], "date", "snowfall thisyear (cm)", xisDate=True)
    #plt_set.plot(x, ave_city_data_all[1], "date", "snowfall 10year ave (cm)", xisDate=True)
    plt_set.plot(x, ave_city_data_all[2], "date", "snowfall heinen (cm)", xisDate=True)
    #plt_set.plot(x, ave_city_data_all[3], "date", "snowfall thisyear/snowfall heinen", xisDate=True, newYaxis=True)
    plt_set.save_fig("snow")
    print(ave_city_data_all[2].mean())
    print(ave_city_data_all[2].std())

if __name__ == "__main__":
    main()
