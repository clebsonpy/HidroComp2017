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
        print('Arquivo: ', self.nomeArquivo)
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
        

    
    