import zipfile, os

def listaArq(caminho):
    listaDir = os.listdir(caminho)
    listaZip = []
    listaTxt = []
    for arquivo in listaDir:
        if os.path.isfile(os.path.join(caminho, arquivo)) and arquivo[-3:].upper() == 'ZIP':
            listaZip.append(arquivo)
        elif os.path.isfile(os.path.join(caminho, arquivo)) and arquivo[-3:].upper() == 'TXT':
            listaTxt.append(arquivo[:-4])
    return listaZip, listaTxt

def renomearTxt(caminho, listaTxt):
    for txt in listaTxt:
        if txt == "CHUVAS":
            with open(os.path.join(caminho, txt+'.TXT'), encoding="Latin-1") as arquivo:
                for linha in arquivo.readlines():
                    if linha.split(":")[0] == "//   Código da Estação":
                        nome = linha.split(":")[1][1:-1]
                        print(nome)
                        os.rename(os.path.join(caminho, txt+'.TXT'),
                                  os.path.join(caminho, nome+".TXT"))

def extraindoZip(caminho, listaZip):
    for zipNome in listaZip:
        with zipfile.ZipFile(os.path.join(caminho,zipNome)) as arquivo:
            arquivo.extractall(caminho)
        renomearTxt(caminho, listaArq(caminho)[1])
        print('Arquivo Extraido!')

if __name__ == "__main__":
    caminho = "/home/clebsonpy/Vazões"
    extraindoZip(caminho, listaArq(caminho)[0])
