# OFET
import numpy as np
import matplotlib.pyplot as plt
import os
from tkinter import filedialog
from scipy.optimize import curve_fit

tempo,vds,vgs,ids,vgs,potência,v_inicial,v_final = [None]*8
abs_ids= []
sqrt_ids = []

def colunas_extras(ids):
    global abs_ids,sqrt_ids
    for i in ids:
        abs_ids.append(abs(i))
        sqrt_ids.append(np.sqrt(abs(i)))
    plt.plot(vgs,sqrt_ids)
    plt.xlabel('VGS')
    plt.ylabel('sqrt(IDS)')
    plt.show()

def ler_arquivo_txt(caminho_arquivo):
    global tempo,vds,vgs,ids,igs,vgs,potência, v_inicial,v_final
    nome_arquivo = os.path.splitext(os.path.basename(caminho_arquivo))[0]
    with open(caminho_arquivo, 'r') as arquivo:
        linhas = arquivo.readlines()
        tempo = []
        vds = []
        vgs = []
        ids = []
        igs = []
        #potência = []
        armazenar = False 

        for linha in linhas:
            if not armazenar: 
                if  linha[0].isnumeric() or linha[0] == '-':
                    armazenar = True
            if armazenar:
                if linha[0].isalpha() or linha[0].isspace():
                    break  
                colunas = linha.split()
                tempo.append(float(colunas[0]))
                vds.append (float(colunas[1]))
                vgs.append(float(colunas[2]))
                ids.append(float(colunas[3]))
                igs.append(float(colunas[4]))
                #potência.append(float(colunas[5]))
    colunas_extras(ids)
    v_inicial=int(input("Digite o valor inicial da tensão da parte da curva onde começa a reta"))
    v_final = int(input("Agora, o valor final"))

def salvar_dados():
    with open(caminho_arquivo, 'w') as file:
        file.write("Tempo  VDS VGS  IDS  IGS |IDS| sqrt(|IDS|)\n")
        for i in range(len(tempo)):
            file.write("{:.7e}  {:.7e}  {:.7e}  {:.7e}  {:.7e} {:.7e}  {:.7e}\n".format(tempo[i], vds[i], vgs[i],ids[i],igs[i],abs_ids[i], sqrt_ids[i]))
        print ("Os dados foram salvos com sucesso")

caminho_arquivo = 'C:/Users/Estudante/Desktop/LOEM/Alice/OFET/Disp1/30um medida1 transf -40V.txt'
ler_arquivo_txt(caminho_arquivo)
salvar_dados()

