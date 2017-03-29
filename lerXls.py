#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 29 10:37:39 2017

@author: clebson
"""
import os
import pandas as pd
import numpy as np

class LerXls():
    def __init__(self, caminho, nomeArquivo):
        self.caminho = caminho
        self.nomeArquivo = nomeArquivo
        
    def lerXls(self):
        arq = os.path.join(self.caminho, self.nomeArquivo+'.xls')
        dadosV = pd.read_excel(arq, shettname='Total', header=0, skiprows=5, index_col=0)
        dadosV.drop(np.NaN, inplace=True)
        aux = []
        dic = {'jan':'1', 'fev':'2', 'mar':'3', 'abr':'4', 'mai':'5', 'jun':'6', 'jul':'7', 'ago':'8', 'set':'9', 'out':'10', 'nov':'11', 'dez':'12'}
        for i in dadosV.index:
            aux.append(i.replace(i[-8:-5], dic[i[-8:-5]]))
        
        dadosV.index = pd.to_datetime(aux, dayfirst=True)
        codiColuna = [i.split('(')[0] for i in dadosV.axes[1]]
        dadosV.columns = codiColuna
        
        return dadosV.astype(float)