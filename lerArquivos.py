#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 29 10:15:34 2017

@author: clebson
"""
import os
import pandas as pd
import numpy as np
import gdal
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
        tipos = {'FLUVIOMÉTRICO': "Vazao01", 'PLUVIOMÉTRICO': "Chuva01"}
        listaLinhas = self.linhas()
        dadosVazao = []
        count = 0
        for linha in listaLinhas:
            count += 1
            if count == 1:
                #indiceCodigo = linha.index("EstacaoCodigo")
                inicioVa = linha.index(tipos[self.tipoDado])
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
#                print(dadosVazao)
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

class LerHdf():
    def __init__(self, caminho, nomeArquivo):
        self.caminho = caminho
        self.nomeArquivo = nomeArquivo
#        self.lon = lon
#        self.lat = lat
    def listaLonLat(self, arq):
        inf = arq.GetMetadata()['Grid_GridHeader'].split(';\n')[3:8]
        resol = float(inf[0].split('=')[1])
        lonLat = list(map(lambda x: round(float(x.split('=')[1]), 1), inf[1:]))
        lat, lon = [lonLat[i*2:2+i*2:] for i in range(2)]
        lat.sort()
        lon.sort()
        lon = [lon[0]+0.05, lon[1]]
        lat = [lat[0]+0.05, lat[1]]
        listaLon = np.arange(lon[0], lon[1], resol)
        listaLat = np.arange(lat[0], lat[1], resol)
        return listaLon, listaLat
    
    def lerHdf(self):
        arq = gdal.Open(os.path.join(self.caminho, self.nomeArquivo+'.HDF5'))
#        3B-HHR-CS-36W7S34W8S.MS.MRG.3IMERG.20160424-S000000-E002959.0001.V04A.HDF5
        dataAux = self.nomeArquivo.split('.')[4].split('-')
        data = pd.to_datetime(dataAux[0]+dataAux[1].replace('S',''))
        subData = arq.GetSubDatasets()
        precip = gdal.Open(subData[5][0])
        df = pd.DataFrame(precip.ReadAsArray())
#        df1 = df.iloc[range(((180+self.lon[0])*4)-1,(180+self.lon[1])*4), range(((50+self.lat[0])*4)-1,(50+self.lat[1])*4)]
        listLon, listLat = self.listaLonLat(arq)
        lista=[]
        index = []
        for i in df:
            for k in df.index:
                lista.append(df[i][k])
                index.append((str(listLat[i]),str(listLon[k])))

        serie = pd.Series(lista, index=index, name=data)
        return serie

class LerSam():
    def __init__(self, caminho, nomeArquivo):
        self.caminho = caminho
        self.nomeArquivo = nomeArquivo
    
    def linhasSam(self):
        listaLinhas = []
        with open(os.path.join(self.caminho, self.nomeArquivo+".sam"), 'r') as arq:
            for linha in arq.readlines():
                listaLinhas.append(linha.split())
        return listaLinhas
    
    def lerSam(self):
        listaLinhas = self.linhasSam()
        dado = []
        index = []
        cont = 0
        for linha in listaLinhas:
            if cont > 0:
                dataHora = pd.to_datetime(self.nomeArquivo)
                dado.append(float(linha[3]))
                index.append((linha[1], linha[2]))
            cont +=1
        serie = pd.Series(dado, index=index, name=dataHora)
        return serie