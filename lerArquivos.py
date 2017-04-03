#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 29 10:15:34 2017

@author: clebson
"""
import os
import pandas as pd
import numpy as np
import calendar as ca


class LerTxt():
    def __init__(self, caminho, nomeArquivo):
        self.caminho = caminho
        self.nomeArquivo = nomeArquivo

    def linhas(self):
        listaLinhas = []
        with open(os.path.join(self.caminho, self.nomeArquivo+".TXT"), encoding="Latin-1") as arquivo:
            for linha in arquivo.readlines():
                if linha[:3] != "// " and linha[:3] != "//-" and linha != "\n" and linha !="//\n":
                    listaLinhas.append(linha.strip("//").split(";"))
        return listaLinhas

    def multIndex(self, data, dias, consistencia):
        if data.day == 1:
            dias = dias
        else:
            dias = dias - data.day
        listaData = pd.date_range(data, periods=dias, freq="D")
        listaCons = [int(consistencia)]*dias
        indexMult = list(zip(*[listaData, listaCons]))
        return pd.MultiIndex.from_tuples(indexMult, names=["Data", "Consistencia"])

    def lerTxt(self):
        listaLinhas = self.linhas()
        dadosVazao = []
        count = 0
        for linha in listaLinhas:
            count += 1
            if count == 1:
                #indiceCodigo = linha.index("EstacaoCodigo")
                inicioVa = linha.index("Vazao01")
                indiceData = linha.index("Data")
                indiceCons = linha.index("NivelConsistencia")
            elif count >= 2:
                #codigoEst = linha[indiceCodigo]
                data = pd.to_datetime(linha[indiceData], dayfirst=True)
                dias = ca.monthrange(data.year, data.month)[1]
                consistencia = linha[indiceCons]
                index = self.multIndex(data, dias, consistencia)
                indiceVa = [i for i in range(inicioVa, inicioVa+dias)]
                listaVazao = [np.NaN if linha[i] == "" else float(linha[i].replace(",",".")) for i in indiceVa]
                dadosVazao.append(pd.Series(listaVazao, index=index, name=self.nomeArquivo))

        dadosV = pd.DataFrame(pd.concat(dadosVazao))
        return dadosV

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
        codiColuna = [i.split(' (')[0] for i in dadosV.axes[1]]
        dadosV.columns = codiColuna

        return dadosV.astype(float)