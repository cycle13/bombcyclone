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


class CityData:


    def __init__(self, city: str):
        self.city = city
        self.sum_snow_this_year = pd.DataFrame()
        self.sum_snow_10ave = pd.DataFrame()
        self.sum_snow_ordinary = pd.DataFrame()

    def add_data(self, snow_this_year, snow_10ave, snow_ordinary):
        if self.sum_snow_this_year.empty:
            self.sum_snow_this_year = snow_this_year
            self.sum_snow_10ave = snow_10ave
            self.sum_snow_ordinary = snow_ordinary
        else:
            self.sum_snow_this_year = pd.concat([self.sum_snow_this_year, snow_this_year], sort=True)
            self.sum_snow_10ave = pd.concat([self.sum_snow_10ave, snow_10ave], sort=True)
            self.sum_snow_ordinary = pd.concat([self.sum_snow_ordinary, snow_ordinary], sort=True)

    def save_data(self):

        tmp_data = pd.concat([self.sum_snow_this_year, self.sum_snow_10ave], axis=1, sort=True)
        all_data = pd.concat([tmp_data, self.sum_snow_ordinary], axis=1, sort=True)
        all_data.to_csv("tmp.csv" )


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
        city_data[city].save_data()


if __name__ == "__main__":
    main()
