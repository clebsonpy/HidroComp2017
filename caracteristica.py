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
from peakutils import peak


class Caracteristicas():
    def __init__(self, dadosVazao, nPosto=None, dataInicio=None, dataFim=None):
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

    # Ano hidrologico
    def mesInicioAnoHidrologico(self):
        mediaMes = [self.dadosVazao[self.nPosto].loc[self.dadosVazao.index.month == i].mean()
                    for i in range(1, 13)]
        mesHidro = 1 + mediaMes.index(min(mediaMes))
        mesHidroAbr = cal.month_abbr[mesHidro]
        return mesHidro, mesHidroAbr.upper()

    # Periodos sem falhas
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
            eventoL = self.dadosVazao[self.nPosto].isin(
                self.dadosVazao.loc[self.dadosVazao[self.nPosto] >= limiar, self.nPosto])
            return eventoL, limiar
        elif evento == 'estiagem':
            eventoL = self.dadosVazao[self.nPosto].isin(
                self.dadosVazao.loc[self.dadosVazao[self.nPosto] <= limiar, self.nPosto])
            return eventoL, limiar
        else:
            return 'Evento erro!'

    def parcialEventoMediaMaxima(self, tipoEvento):
        limiar = self.maxAnual()[self.nPosto].mean()
        if tipoEvento == 'cheia':
            eventoL = self.dadosVazao[self.nPosto].isin(
                self.dadosVazao.loc[self.dadosVazao[self.nPosto] >= limiar, self.nPosto])
            return eventoL
        elif tipoEvento == 'estiagem':
            eventoL = self.dadosVazao[self.nPosto].isin(
                self.dadosVazao.loc[self.dadosVazao[self.nPosto] <= limiar, self.nPosto])
            return eventoL
        else:
            return 'Evento erro!'

    def parcialEventoPorAno(self, limiar, tipoEvento):
        if tipoEvento == 'cheia':
            eventoL = self.dadosVazao[self.nPosto].isin(
                self.dadosVazao.loc[self.dadosVazao[self.nPosto] >= limiar, self.nPosto])
            return eventoL
        elif tipoEvento == 'estiagem':
            eventoL = self.dadosVazao[self.nPosto].isin(
                self.dadosVazao.loc[self.dadosVazao[self.nPosto] <= limiar, self.nPosto])
            return eventoL
        else:
            return 'Evento erro!'

    def parcialPorAno(self, nEventos, tipoEvento):
        nAnos = self.dadosVazao[self.nPosto].index.year[-1] - \
            self.dadosVazao[self.nPosto].index.year[0]
        l = self.dadosVazao[self.nPosto].quantile(0.7)
        #vazao = -np.sort(-self.dadosVazao.loc[self.dadosVazao[self.nPosto] <= l, self.nPosto])
        q = 0.54
        for i in range(0, 10):
            q -= 0.005
            limiar = self.dadosVazao[self.nPosto].quantile(q)
            print(limiar)
            eventosL = self.parcialEventoPorAno(limiar, tipoEvento)
            picos = self.eventos_picos(eventosL, tipoEvento)
            print(picos)
            if len(picos) >= nEventos * (nAnos):
                return picos, limiar

    def maxAnual(self):
        gDados = self.dadosVazao.groupby(pd.Grouper(
            freq='AS-%s' % self.mesInicioAnoHidrologico()[1]))
        maxVazao = gDados[self.nPosto].max().values
        dataVazao = gDados[self.nPosto].idxmax().values

        dfMax = pd.DataFrame(maxVazao, index=dataVazao, columns=[self.nPosto])
        return dfMax

    def daysJulian(self, reducao):

        if reducao.title() == "Maxima":
            data = pd.DatetimeIndex(self.dadosVazao.groupby(pd.Grouper(
                freq='AS-%s' % self.mesInicioAnoHidrologico()[1])).idxmax()[self.nPosto].values)
        elif reducao.title() == "Minima":
            data = pd.DatetimeIndex(self.dadosVazao.groupby(pd.Grouper(
                freq='AS-%s' % self.mesInicioAnoHidrologico()[1])).idxmin()[self.nPosto].values)

        dfDayJulian = pd.DataFrame(
            list(map(int, data.strftime("%j"))), index=data)
        dayJulianMedia = dfDayJulian.mean()[0]
        dayJulianCv = dfDayJulian.std()[0]/dayJulianMedia
        return dfDayJulian, dayJulianMedia, dayJulianCv

    def __criterioMediana(self, dados, index, tipoEvento):
        median = self.dadosVazao[self.nPosto].median()
        if tipoEvento == 'cheia':
            eventos = self.dadosVazao[self.nPosto].isin(
                self.dadosVazao.loc[self.dadosVazao[self.nPosto] >= median, self.nPosto])
        elif tipoEvento == 'estiagem':
            eventos = self.dadosVazao[self.nPosto].isin(
                self.dadosVazao.loc[self.dadosVazao[self.nPosto] <= median, self.nPosto])

        if len(dados['Vazao']) > 0 and (not eventos.loc[index] or
                                        index == pd.to_datetime("%s0831" % index.year)):
            return True
        else:
            return False

    def __criterioMedia(self, dados, index, tipoEvento):
        mean = self.dadosVazao[self.nPosto].mean()
        if tipoEvento == 'cheia':
            eventos = self.dadosVazao[self.nPosto].isin(
                self.dadosVazao.loc[self.dadosVazao[self.nPosto] >= mean, self.nPosto])
        elif tipoEvento == 'estiagem':
            eventos = self.dadosVazao[self.nPosto].isin(
                self.dadosVazao.loc[self.dadosVazao[self.nPosto] <= mean, self.nPosto])

        if len(dados['Vazao']) > 0 and (not eventos.loc[index] or
                                        index == pd.to_datetime("%s0831" % index.year)):
            return True
        else:
            return False

    def __criterio_autocorrelacao(self, dados, max_evento, dias):

        if len(max_evento['Data']) == 0:
            return True
        elif len(dados['Data']) == 0:
            return False
        else:
            data_max = dados['Data'][dados['Vazao'].index(max(dados['Vazao']))]
            distancia_dias = data_max - max_evento['Data'][-1]
            print(distancia_dias.days)
            if distancia_dias.days < dias:
                return False
            return True

    def eventos_picos(self, eventosL, tipoEvento, dias):
        grupoEventos = eventosL.groupby(pd.Grouper(
            freq='AS-%s' % self.mesInicioAnoHidrologico()[1]))
        max_evento = {'Data': [], 'Ano': [], 'Vazao': [],
                     'Inicio': [], 'Fim': [], 'Duracao': []}
        iAntes = eventosL.index[1]
        lowLimiar = False
        dados = {'Data': [], 'Vazao': []}
        for key, serie in grupoEventos:
            for i in serie.index:
                if serie.loc[i]:
                    dados['Vazao'].append(
                        self.dadosVazao.loc[iAntes, self.nPosto])
                    dados['Data'].append(iAntes)
                    lowLimiar = True
                elif lowLimiar:
                    dados['Vazao'].append(
                        self.dadosVazao.loc[iAntes, self.nPosto])
                    dados['Data'].append(iAntes)
                    dados['Vazao'].append(self.dadosVazao.loc[i, self.nPosto])
                    dados['Data'].append(i)
                    lowLimiar = False

                elif self.__criterio_autocorrelacao(dados, max_evento, dias):
                    max_evento['Ano'].append(key.year)
                    max_evento['Vazao'].append(max(dados['Vazao']))
                    max_evento['Inicio'].append(dados['Data'][0])
                    max_evento['Fim'].append(dados['Data'][-1])
                    max_evento['Duracao'].append(len(dados['Data']))
                    max_evento['Data'].append(dados['Data'][dados['Vazao'].index(max(dados['Vazao']))])
                    dados = {'Data': [], 'Vazao': []}

                elif len(dados['Vazao']) > 0 and max_evento['Vazao'][-1] < max(dados['Vazao']):
                    max_evento['Ano'][-1] = key.year
                    max_evento['Vazao'][-1] = max(dados['Vazao'])
                    max_evento['Fim'][-1] = dados['Data'][-1]
                    max_evento['Duracao'][-1] = len(dados['Data'])
                    max_evento['Data'][-1] = dados['Data'][dados['Vazao'].index(max(dados['Vazao']))]
                    dados = {'Data': [], 'Vazao': []}

                iAntes = i
        return pd.DataFrame(max_evento,
                            columns=['Ano', 'Duracao', 'Inicio', 'Fim', 'Vazao'],
                            index=max_evento['Data'])


    def pulsosDuracao(self, tipoEvento='cheia'):
        eventosL, limiar = self.parcialEventoPercentil(quartilLimiar=0.75, evento=tipoEvento)
        eventosPicos = self.eventos_picos(eventosL, tipoEvento, dias=17)

        x = eventosPicos.index
        y = eventosPicos.Vazao
        serie = pd.Series(y, index=x)
        #acorr = sm.stats.diagnostic.acorr_ljungbox(serie, lags=2)
        #print(acorr)
        print(serie.autocorr(lag=1))
        print(serie.autocorr(lag=2))
        grupoEventos = self.dadosVazao[self.nPosto].groupby(
            pd.Grouper(freq='AS-%s' % self.mesInicioAnoHidrologico()[1]))
        dic = {'Ano': [], 'Duracao': [], 'nPulsos': []}
        for i, serie in grupoEventos:
            dic['Ano'].append(i.year)
            dic['Duracao'].append(
                eventosPicos.Duracao.loc[eventosPicos.Ano == i.year].mean())
            dic['nPulsos'].append(
                len(eventosPicos.loc[eventosPicos.Ano == i.year]))
        evento = pd.DataFrame(dic)
        evento.set_value(
            evento.loc[evento.Duracao.isnull()].index, 'Duracao', 0)
        durMedia = evento.Duracao.mean()
        durCv = evento.Duracao.std()/durMedia
        nPulsoMedio = evento.nPulsos.mean()
        nPulsoCv = evento.nPulsos.std()/nPulsoMedio
        return eventosPicos, evento, durMedia, durCv, nPulsoMedio, nPulsoCv, limiar

    def ChecksTypeRate(self, value1, value2, typeRate):
        if typeRate == 'rise':
            return value1 < value2
        elif typeRate == 'fall':
            return value1 > value2

    def rate(self, tipo, quartilLimiar, evento):
        eventos = self.parcialEvento(quartilLimiar, evento)[0]
        grupoEventos = eventos.groupby(pd.Grouper(
            freq='AS-%s' % self.mesInicioAnoHidrologico()[1]))
        rate = {'Data1': [], 'Vazao1': [],
                'Data2': [], 'Vazao2': [], 'Taxa': []}
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
                        rate['Vazao1'].append(
                            self.dadosVazao.loc[d1, self.nPosto])
                        rate['Vazao2'].append(
                            self.dadosVazao.loc[i, self.nPosto])
                        rate['Taxa'].append(
                            self.dadosVazao.loc[i, self.nPosto] - self.dadosVazao.loc[d1, self.nPosto])
                        values.append(
                            self.dadosVazao.loc[i, self.nPosto] - self.dadosVazao.loc[d1, self.nPosto])
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
        dados_anual = self.dadosVazao.groupby(
            pd.Grouper(freq='A')).sum().to_period()
        return dados_anual
