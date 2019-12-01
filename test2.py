# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import os
import scipy.stats as st
from math import sqrt

names_R = np.array([])
names_AF = np.array([])
mid_R = np.array([])
var_R = np.array([])
mid_AF = np.array([])
var_AF = np.array([])
int_R = np.array([0., 0.])
int_AF = np.array([0., 0.])
count = 0
F = 1.65 # из таблицы функции Лапласа
chunksize = 100000000
for i,chunk in enumerate(pd.read_csv('/usr/local/data/transactions.txt', chunksize = chunksize, index_col=0, header=None)):
  x = chunk[chunk[3]=='R']
  x.columns = ['name', 'sum', 'type']
  y = chunk[chunk[3]=='AF']
  y.columns = ['name', 'sum', 'type']

  sum_R = np.array(x['sum'].to_list())
  mR = np.mean(sum_R)
  vR = np.var(sum_R)/chunksize
  mid_R = np.append(mid_R, mR)
  var_R = np.append(var_R, vR)
  sum_AF = np.array(y['sum'].to_list())
  mAF = np.mean(sum_AF)
  vAF = np.var(sum_AF)/chunksize
  mid_AF = np.append(mid_AF, mAF)
  var_AF = np.append(var_AF, vAF)

  int_R += np.array(st.t.interval(0.9, len(sum_R)-1, loc=np.mean(sum_R), scale=st.sem(sum_R)))
  int_AF += np.array(st.t.interval(0.9, len(sum_AF)-1, loc=np.mean(sum_AF), scale=st.sem(sum_AF)))
  count += 1



  names_R = np.append(names_R, x['name'].unique())
  names_AF = np.append(names_AF, y['name'].unique())
  names_R = np.unique(names_R)
  names_AF = np.unique(names_AF)

int_R = [round(i/count, 3) for i in int_R]
int_AF = [round(i/count, 3) for i in int_AF]
p = abs(np.mean(mid_AF) - np.mean(mid_R)) / sqrt(np.mean(var_R) + np.mean(var_AF))
print('Количество клиентов для сегмента R = {}, для сегмента AF = {}'.format(len(names_R), len(names_AF)))
print('Средний объем отдельной транзакции для сегмента R = {}, для сегмента AF = {}'.format(round(np.mean(mid_R), 3), round(np.mean(mid_AF), 3)))
print('90% доверительный интервал для среднего объема отдельной транзакции для сегмента R = {}, для сегмента AF = {}'.format(int_R, int_AF))
print('Гипотеза о равенстве средних объемов транзакций между сегментами при уровне значимости 10%:', p<F)
