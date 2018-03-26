#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 22:57:24 2017

@author: clebson
"""
import pandas as pd
import numpy as np
from datetime import date
import calendar as cal

class Caracteristicas():
    def __init__(self, dadosVazao, nPosto=None, dataInicio = None, dataFim = None):
        self.nPosto = nPosto.upper()
        if dataInicio != None and dataFim != None:
            self.dataInicio = pd.to_datetime(dataInicio, dayfirst=True)
            self.dataFim = pd.to_datetime(dataFim, dayfirst=True)
            self.dadosVazao = dadosVazao.loc[self.dataInicio:self.dataFim]
        elif dataInicio != None:
            self.dataInicio = pd.to_datetime(dataInicio, dayfirst=True)
            self.dadosVazao = dadosVazao.loc[self.dataInicio:]
        elif dataFim != None:
            self.dataFim = pd.to_datetime(dataFim, dayfirst=True)
            self.dadosVazao = dadosVazao.loc[:self.dataFim]
        else:
            self.dadosVazao = dadosVazao
        
    #Ano hidrologico
    def mesInicioAnoHidrologico(self):
        mediaMes = [self.dadosVazao[self.nPosto].loc[self.dadosVazao.index.month==i].mean() for i in range(1,13)]
        mesHidro = 1 + mediaMes.index(min(mediaMes))
        mesHidroAbr = cal.month_abbr[mesHidro]
        return mesHidro, mesHidroAbr.upper()

    #Periodos sem falhas
    def periodoSemFalhas(self):
        aux = []
        listaInicio = []
        listaFim = []
        ganttBool = self.dadosVazao.isnull()[self.nPosto]
        for i in ganttBool.index:
            if ~ganttBool.loc[i]:
                aux.append(i)
            elif len(aux) > 2 and ganttBool.loc[i]:
                listaInicio.append(aux[0])
                listaFim.append(aux[-1])
                aux = []
        if len(aux) > 0:
            listaInicio.append(aux[0])
            listaFim.append(aux[-1])
        dic = {'Inicio': listaInicio, 'Fim': listaFim}
        return pd.DataFrame(dic)


    def parcialEventoPercentil(self, quartilLimiar, evento):
        limiar = self.dadosVazao[self.nPosto].quantile(quartilLimiar)
        if evento == 'cheia':
            eventoL = self.dadosVazao[self.nPosto].isin(self.dadosVazao.loc[self.dadosVazao[self.nPosto] >= limiar, self.nPosto])
            return eventoL
        elif evento == 'estiagem':
            eventoL = self.dadosVazao[self.nPosto].isin(self.dadosVazao.loc[self.dadosVazao[self.nPosto] <= limiar, self.nPosto])
            return eventoL
        else:
            return 'Evento erro!'


    def parcialEventoMediaMaxima(self, dfMaxima, tipoEvento):
        limiar = dfMaxima[self.nPosto].mean()
        print(limiar)
        if tipoEvento == 'cheia':
            eventoL = self.dadosVazao[self.nPosto].isin(self.dadosVazao.loc[self.dadosVazao[self.nPosto] >= limiar, self.nPosto])
            return eventoL
        elif tipoEvento == 'estiagem':
            eventoL = self.dadosVazao[self.nPosto].isin(self.dadosVazao.loc[self.dadosVazao[self.nPosto] <= limiar, self.nPosto])
            return eventoL
        else:
            return 'Evento erro!'


    def maxAnual(self):
        gDados = self.dadosVazao.groupby(pd.Grouper(freq='AS-%s' % self.mesInicioAnoHidrologico()[1]))
        maxVazao = gDados[self.nPosto].max().values
        dataVazao = gDados[self.nPosto].idxmax().values
        
#        dic = {'Data': dataVazao, self.nPosto: maxVazao}
        dfMax = pd.DataFrame(maxVazao, index=dataVazao, columns=[self.nPosto])
        return dfMax
        
        
    def daysJulian(self, reducao):
        
        if reducao.title() == "Maxima":
            data = pd.DatetimeIndex(self.dadosVazao.groupby(pd.Grouper(freq='AS-%s' % self.mesInicioAnoHidrologico()[1])).idxmax()[self.nPosto].values)
        elif reducao.title() == "Minima":
            data = pd.DatetimeIndex(self.dadosVazao.groupby(pd.Grouper(freq='AS-%s' % self.mesInicioAnoHidrologico()[1])).idxmin()[self.nPosto].values)
        
        dfDayJulian = pd.DataFrame(list(map(int, data.strftime("%j"))), index = data)
        dayJulianMedia = dfDayJulian.mean()[0]
        dayJulianCv = dfDayJulian.std()[0]/dayJulianMedia
        return dfDayJulian, dayJulianMedia, dayJulianCv
        

    def __criterioMediana(self, dados, index, tipoEvento):
        median = self.dadosVazao[self.nPosto].median()
        if tipoEvento == 'cheia':
            eventos = self.dadosVazao[self.nPosto].isin(self.dadosVazao.loc[self.dadosVazao[self.nPosto] >= median, self.nPosto])
        elif tipoEvento == 'estiagem':
            eventos = self.dadosVazao[self.nPosto].isin(self.dadosVazao.loc[self.dadosVazao[self.nPosto] <= median, self.nPosto])
        
        if len(dados['Vazao']) > 0 and (not eventos.loc[index] or 
                    index == pd.to_datetime("%s0831" % index.year)):
            return True
        else:
            return False
    

    def __criterioMedia(self, dados, index, tipoEvento):
        mean = self.dadosVazao[self.nPosto].mean()
        if tipoEvento == 'cheia':
            eventos = self.dadosVazao[self.nPosto].isin(self.dadosVazao.loc[self.dadosVazao[self.nPosto] >= mean, self.nPosto])
        elif tipoEvento == 'estiagem':
            eventos = self.dadosVazao[self.nPosto].isin(self.dadosVazao.loc[self.dadosVazao[self.nPosto] <= mean, self.nPosto])
        
        if len(dados['Vazao']) > 0 and (not eventos.loc[index] or 
                    index == pd.to_datetime("%s0831" % index.year)):
            return True
        else:
            return False


    def pulsosDuracao(self, quartilLimiar=0.75, tipoEvento='cheia'):
        eventosL = self.parcialEventoMediaMaxima(self.maxAnual(), tipoEvento)
        grupoEventos = eventosL.groupby(pd.Grouper(freq='AS-%s' % self.mesInicioAnoHidrologico()[1]))
        maxEvento = {'Ano': [], 'Vazao':[], 'Inicio':[], 'Fim':[], 'Duracao':[]}
        Data = []
        iAntes = eventosL.index[1]
        lowLimiar = False
        dados = {'Data':[], 'Vazao':[]}
        for key, serie in grupoEventos:            
            for i in serie.index:
                if serie.loc[i]:
                    dados['Vazao'].append(self.dadosVazao.loc[iAntes, self.nPosto])
                    dados['Data'].append(iAntes)
                    lowLimiar = True
                elif lowLimiar:
                    dados['Vazao'].append(self.dadosVazao.loc[iAntes, self.nPosto])
                    dados['Data'].append(iAntes)
                    dados['Vazao'].append(self.dadosVazao.loc[i, self.nPosto])
                    dados['Data'].append(i)                   
                    lowLimiar = False
                elif self.__criterioMedia(dados, i, tipoEvento):
                    maxEvento['Ano'].append(key.year)
                    Data.append(dados['Data'][dados['Vazao'].index(max(dados['Vazao']))])
                    maxEvento['Vazao'].append(max(dados['Vazao']))
                    maxEvento['Inicio'].append(dados['Data'][0])
                    maxEvento['Fim'].append(dados['Data'][-1])
                    maxEvento['Duracao'].append(len(dados['Data']))
                    dados = {'Data':[], 'Vazao':[]}
                    
                iAntes = i
        eventosPicos = pd.DataFrame(maxEvento, index = Data)
        
        dic = {'Ano':[], 'Duracao':[], 'nPulsos':[], }
        for i, serie in grupoEventos:
            dic['Ano'].append(i.year)
            dic['Duracao'].append(eventosPicos.Duracao.loc[eventosPicos.Ano == i.year].mean())
            dic['nPulsos'].append(len(eventosPicos.loc[eventosPicos.Ano == i.year]))
        evento = pd.DataFrame(dic)
        evento.set_value(evento.loc[evento.Duracao.isnull()].index, 'Duracao', 0)
        durMedia = evento.Duracao.mean()
        durCv = evento.Duracao.std()/durMedia
        nPulsoMedio = evento.nPulsos.mean()
        nPulsoCv = evento.nPulsos.std()/nPulsoMedio
        return eventosPicos, evento, durMedia, durCv, nPulsoMedio, nPulsoCv
    
    def ChecksTypeRate(self, value1, value2, typeRate):
        if typeRate == 'rise':
            return value1 < value2
        elif typeRate == 'fall':
            return value1 > value2
    
    def rate(self, tipo, quartilLimiar, evento):
        eventos = self.parcialEvento(quartilLimiar, evento)[0]
        grupoEventos = eventos.groupby(pd.Grouper(freq='AS-%s' % self.mesInicioAnoHidrologico()[1]))
        rate = {'Data1':[], 'Vazao1': [], 'Data2':[], 'Vazao2': [], 'Taxa':[]}
        rise = {'Ano': [], 'Soma': [], 'Media': []}
        boo = False
        for key, serie in grupoEventos:
            d1 = None
            cont = 0
            values = []
            for i in serie.loc[serie.values == True].index:
                if d1 != None:
                    if self.ChecksTypeRate(self.dadosVazao.loc[d1, self.nPosto], 
                                           self.dadosVazao.loc[i, self.nPosto], tipo):
                        boo = True
                        rate['Data1'].append(d1)
                        rate['Data2'].append(i)
                        rate['Vazao1'].append(self.dadosVazao.loc[d1, self.nPosto])
                        rate['Vazao2'].append(self.dadosVazao.loc[i, self.nPosto])
                        rate['Taxa'].append(self.dadosVazao.loc[i, self.nPosto] - self.dadosVazao.loc[d1, self.nPosto])
                        values.append(self.dadosVazao.loc[i, self.nPosto] - self.dadosVazao.loc[d1, self.nPosto])
                    else:
                        if boo:
                            mean = np.mean(values)
                            cont += 1
                            boo = False
            
                d1 = i
            if boo:
                mean = np.mean(values)
                cont += 1
                boo = False
                
            rise['Ano'].append(key.year)
            rise['Soma'].append(cont)
            rise['Media'].append(mean)
        
        ratesDf = pd.DataFrame(rate)
        riseDf = pd.DataFrame(rise)
        riseMed = riseDf.Media.mean()
        riseCv = riseDf.Media.std()/riseMed
        nMedia = riseDf.Soma.mean()
        nCv = riseDf.Soma.std()/nMedia
        return ratesDf, riseDf, riseMed, riseCv, nMedia, nCv
    
    def precipitacao_anual(self):
        dados_anual = self.dadosVazao.groupby(pd.Grouper(freq='A')).sum().to_period()
        return dados_anual
    
    def acharLimiar(self, nPicos):
        pass
