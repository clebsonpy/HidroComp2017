import os
import timeit
import calendar as ca
import pandas as pd
import numpy as np
import prepara

class Arquivos():
    def __init__(self, caminho, fonte):
        self.caminho = caminho
        self.fonte = fonte
        self.tipos = {'ONS':'xls', 'ANA':'TXT'}
        
    def listaArq(self):
        listaDir = os.listdir(self.caminho)
        listaArquivo = []
        for arquivo in listaDir:
            if os.path.isfile(os.path.join(self.caminho, arquivo)):
                nome, ext = arquivo.split('.')
                if ext == self.tipos[self.fonte]:
                    listaArquivo.append(nome)
        if len(listaArquivo) == 1:
            return listaArquivo[0]
        else:
            return listaArquivo
    
    def lerArquivos(self, nomeArquivo=None, consistencia=None):
        if nomeArquivo == None:
            nomeArquivo = self.listaArq()
        
        def lerTxt():
            def linhas():
                print('Arquivo: ', nomeArquivo)
                listaLinhas = []
                with open(os.path.join(self.caminho, nomeArquivo+".TXT"), encoding="Latin-1") as arquivo:
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
                
            def trabaLinhas():
                listaLinhas = linhas()
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
            
            return trabaLinhas()   

    
        def lerXlsx():
            arq = os.path.join(self.caminho, nomeArquivo+'.xls')
            dadosV = pd.read_excel(arq, shettname='Total', header=0, skiprows=5, index_col=0)
            dadosV.drop(np.NaN, inplace=True)
            aux = []
            dic = {'jan':'1', 'fev':'2', 'mar':'3', 'abr':'4', 'mai':'5', 'jun':'6', 'jul':'7', 'ago':'8', 'set':'9', 'out':'10', 'nov':'11', 'dez':'12'}
            for i in dadosV.index:
                aux.append(i.replace(i[-8:-5], dic[i[-8:-5]]))
            
            dadosV.index = pd.to_datetime(aux, dayfirst=True)
            codiColuna = [i.split(' ')[-1][1:-1] for i in dadosV.axes[1]]
            dadosV.columns = codiColuna
            
            return dadosV.astype(float)
        
        
        if type(nomeArquivo) == list:
            dadosVazao = pd.DataFrame()
            pp = prepara.Prepara()
            for nome in nomeArquivo:
                dadosVazao = pp.combinaDateFrame(dadosVazao, self.lerArquivos(nome))
            if consistencia != None:
                dadosVazao = pp.separaDadosConsisBruto(dadosVazao, consistencia)
            return dadosVazao
        else:
            if self.fonte == 'ANA':
                return lerTxt()
            elif self.fonte == 'ONS':
                return lerXlsx()
            
if __name__ == "__main__":
    ini = timeit.default_timer()
    caminho = os.getcwd()
    arq = Arquivos(caminho, fonte='ANA')
    dados = arq.lerArquivos(consistencia=2)
    fim = timeit.default_timer()
    print('Duração: %s' % (fim-ini))
#    dadox = pd.DataFrame.add(dados)
#    print(dados)