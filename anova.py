# -*- coding: utf-8 -*-
"""Enem.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1fSIVA_rbq5vRmYXDlyCpzldJ-eqxiDT4
"""
import sys

import pandas as pd
import pyarrow.parquet as pq
import statsmodels.api as sm
from statsmodels.formula.api import ols

path = 'data'

names = pd.read_excel(path + '/names.xlsx')


def get_filename(year, format_file='xlsx'):
    result = path + '/{}.{}'.format(year, format_file)
    print(result)
    return result


def get_dict_from_year(year):
    result = {}
    for index, row in names.iterrows():
        print(row, year)
        if row[year] == '':
            continue
        result[row[year]] = row['novo']
    return result


class DataSet(dict):
    def __init__(self, local_path):
        super().__init__()
        self.parquet = pq.ParquetFile(local_path)

    def __getitem__(self, key):
        try:
            return self.parquet.read([key]).to_pandas()[key]
        except:
            raise KeyError


arg_year = int(sys.argv[1])
arg_sample = 1

print('Ano de {}, com amostragem de {}%'.format(arg_year, arg_sample * 100))
#
# df = pd.read_excel(get_filename(arg_year))
# df.rename(columns=get_dict_from_year(arg_year), inplace=True)
#
# df = df.sample(int(df.shape[0] * arg_sample))
# df = df.dropna()
#
# df_melt = pd.melt(df, id_vars=['media'], value_vars=['nu_idade', 'tp_cor_raca', 'tp_st_conclusao',
# 'TP_ANO_CONCLUIU', 'tp_dependencia_adm_esc', 'etnia', 'grupo_etario', 'regiao_pais', 'faixa_renda', 'computador',
# 'escolaridade_pai', 'escolaridade_mae', 'rendimento', 'pr', 'pa', 'am', 'in', 'sm_1', 'sm_2', 'sm_2_5', 'sm_5_10',
# 'fem', 'fed', 'est', 'mun', 'tem_comp', 'tem_internet'])

LargeData = DataSet(get_filename(arg_year, 'parquet'))
print(LargeData)

# model_str = 'media ~ C(media) + C(variable) + C(media):C(variable)'
model_str = 'media ~ tp_cor_raca + internet + escolaridade_mae + tp_sexo + ' \
            'rendimento + regiao_pais + tp_dependencia_adm_esc'

model = ols(model_str, data=LargeData).fit()

anova_table = sm.stats.anova_lm(model, typ=2)

print(anova_table)
