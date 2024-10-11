# OFET
#Para o programa atualizado pelo Fred
import numpy as np
import matplotlib.pyplot as plt
import os
from tkinter import filedialog
from scipy.optimize import curve_fit
import glob
import re

vgs_ida,ids_ida,vgs_volta,ids_volta,ciclos = [],[],[],[],[]


def ler_arquivo_txt(caminho_arquivo,L,W,Ci,j):
    global vgs_ida,ids_ida,vgs_volta,ids_volta,ciclos
    with open(caminho_arquivo, 'r') as arquivo:
        linhas = arquivo.readlines()
        vgs_ida = []
        ids_ida = []
        vgs_volta = []
        ids_volta = []
        ciclos = []
        armazenar = False 

        for linha in linhas:
            if not armazenar: 
                if  linha[0].isnumeric() or linha[0] == '-':
                    armazenar = True
            if armazenar:
                if linha[0].isalpha() or linha[0].isspace():
                    break  
                colunas = linha.split()
                vgs_ida.append(float(colunas[0]))
                ids_ida.append (float(colunas[1]))
                vgs_volta.append(float(colunas[2]))
                ids_volta.append(float(colunas[3]))
                ciclos.append(float(colunas[4]))

pasta = 'C:/Users/Estudante/Desktop/LOEM/Alice/OFET/24 10 04 Alice e Harold - disp 1/60um'
nome_pasta= os.path.basename(pasta)
match = re.search(r'\d+',nome_pasta) #para pegar o comprimento do canal a partir do nome da pasta
L = int(match.group())
W = 1000
Ci = 50
arquivos = glob.glob(os.path.join(pasta,"*.txt")) #para ler cada cada arquivo .txt dentro da pasta
for j,caminho_arquivo in enumerate (arquivos):
    nome_arquivo = os.path.basename(caminho_arquivo) 
    ler_arquivo_txt(caminho_arquivo,L,W,Ci,j)

#plotar tudo junto (as 4 curvas)
plt.scatter(ciclos,ids_ida,marker = 'o', color = 'blue',label = "IDA")
plt.scatter(ciclos,ids_volta,marker = 'o', color = 'red', label = "VOLTA" )
plt.legend()
plt.xlabel('Ciclos')
plt.ylabel('IDS')
plt.show()

medida_par_ida = [] #leitura depois de escrito
medida_par_volta = [] 
medida_impar_ida = [] #Leitura depois de apagado
medida_impar_volta = [] 
ciclos_meio = []

for i,el in enumerate (ids_ida):
    if (i%2==0):
        medida_par_ida.append(ids_ida[i])
        medida_par_volta.append(ids_volta[i])
        ciclos_meio.append(ciclos[i])
    else:
        medida_impar_ida.append(ids_ida[i])
        medida_impar_volta.append(ids_volta[i])

plt.scatter(ciclos_meio,medida_par_volta,marker = 'o', color = 'blue',label = "LEITURA ESCRITO")
plt.scatter(ciclos_meio,medida_impar_volta,marker = 'o', color = 'red', label = "LEITURA APAGADO" )
plt.legend()
plt.xlabel('Ciclos')
plt.ylabel('IDS')
plt.title("IDS VOLTA")
plt.show()

plt.scatter(ciclos_meio,medida_par_ida,marker = 'o', color = 'blue',label = "LEITURA ESCRITO")
plt.scatter(ciclos_meio,medida_impar_ida,marker = 'o', color = 'red', label = "LEITURA APAGADO" )
plt.legend()
plt.xlabel('Ciclos')
plt.ylabel('IDS')
plt.title("IDS IDA")
plt.show()