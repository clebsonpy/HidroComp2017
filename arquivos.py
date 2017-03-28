import os
import calendar as ca
import pandas as pd
import numpy as np

class Arquivos():
    def __init__(self, caminho, fonte):
        self.caminho = caminho
        self.fonte = fonte
        self.tipos = {'ONS':'.xls', 'ANA':'TXT'}
        
    def listaArq():
    listaDir = os.listdir(self.caminho)
    listaArquivo = []
    for arquivo in listaDir:
        if os.path.isfile(os.path.join(self.caminho, arquivo)):
            nome, ext = arquivo.split('.')
            if ext == self.tipos[self.fonte]:
                listaArquivo.append(nome)
    return listaArquivo
    
    def lerTxt(nomeArquivo):
        listaLinhas = []
        with open(os.path.join(caminho, nomeArquivo+".TXT"), encoding="Latin-1") as arquivo:
            for linha in arquivo.readlines():
                if linha[:3] != "// " and linha[:3] != "//-" and linha != "\n" and linha !="//\n":
                    listaLinhas.append(linha.strip("//").split(";"))
        return listaLinhas
    
    
    def multIndex(data, dias, consistencia):
        if data.day == 1:
            dias = dias
        else:
            dias = dias - data.day
        listaData = pd.date_range(data, periods=dias, freq="D")
        listaCons = [int(consistencia)]*dias
        indexMult = list(zip(*[listaData, listaCons]))
        return pd.MultiIndex.from_tuples(indexMult, names=["Data", "Consistencia"])
    
    
    
    def trabaLinhas(caminho, nomeArquivo):
        print('Arquivo: ', nomeArquivo)
        listaLinhas = lerTxt(caminho, nomeArquivo)
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
                index = multIndex(data, dias, consistencia)
                indiceVa = [i for i in range(inicioVa, inicioVa+dias)]
                listaVazao = [np.NaN if linha[i] == "" else float(linha[i].replace(",",".")) for i in indiceVa]
                dadosVazao.append(pd.Series(listaVazao, index=index, name=nomeArquivo))
    
        dadosV = pd.DataFrame(pd.concat(dadosVazao))
        
        return dadosV


if __name__ == "__main__":
    caminho = os.getcwd()
    dados = separaDadosConsisBruto(trabaLinhas(caminho, '49370000'), tipo=2)
#    dadox = pd.DataFrame.add(dados)
#    print(dados)