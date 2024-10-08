# OFET
import numpy as np
import matplotlib.pyplot as plt
import os
from tkinter import filedialog
from scipy.optimize import curve_fit

tempo,vds,vgs,ids,vgs,potência,v_inicial,v_final,x0,a,coef_saturação = [None]*11
abs_ids,sqrt_ids,vgs_intervalo,ids_intervalo = [],[],[],[]

def colunas_extras(ids):
    global abs_ids,sqrt_ids
    for i in ids:
        abs_ids.append(abs(i))
        sqrt_ids.append(np.sqrt(abs(i)))
    plt.plot(vgs,sqrt_ids)
    plt.plot(vds,sqrt_ids, label = 'VDS')
    plt.xlabel('VGS')
    plt.ylabel('sqrt(IDS)')
    plt.show(block=False)

def reta(x,a,b):
    return a * x + b

def ler_arquivo_txt(caminho_arquivo):
    global tempo,vds,vgs,ids,igs,vgs,potência, v_inicial,v_final, vgs_intervalo,ids_intervalo,x0,a, coef_saturação
    nome_arquivo = os.path.splitext(os.path.basename(caminho_arquivo))[0]
    with open(caminho_arquivo, 'r') as arquivo:
        linhas = arquivo.readlines()
        tempo = []
        vds = []
        vgs = []
        ids = []
        igs = []
        potência = []
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
                potência.append(float(colunas[5]))
    colunas_extras(ids)
    # v_inicial=float(input("Digite o valor inicial da tensão da parte da curva onde começa a reta: "))
    # v_final = float(input("Agora, o valor final: "))
    # Ci = float(input("Digite o valor da capacitância específica do dielétrico(μF/m^2): "))*(10**-10)
    # L = float(input("Digite o comprimento do canal(μm): "))
    # W = float(input("Digite a largura do canal(μm): "))
    v_inicial = -30
    v_final = -40
    Ci = 50
    L = 80
    W = 1000
    plt.close()
    for pos,i in enumerate(vgs):
        if pos>0:
            if i>vgs[pos-1]:
                break
            if i<=v_inicial and i>=v_final:
                vgs_intervalo.append(i)
                ids_intervalo.append(sqrt_ids[pos])
    vgs_intervalo = np.array(vgs_intervalo)
    ids_intervalo = np.array(ids_intervalo)
    coef, incerteza = curve_fit(reta, vgs_intervalo, ids_intervalo)
    a, b = coef
    x0 = -b/a
    coef_saturação = (2*L*a*a)/(W*Ci)
    plt.plot(vgs,sqrt_ids)
    #plt.plot(vgs_intervalo, ids_intervalo, 'o', label='Dados experimentais',markersize=5)
    #reta_intervalo = np.linspace(vgs_intervalo[0], x0, 10)
    plt.plot(vgs_intervalo, reta(vgs_intervalo, a, b), 'r-', label=f'Fitting')
    plt.xlabel('VGS', fontsize = 14)
    plt.ylabel('sqrt(|IDS|)', fontsize = 14)
    plt.xticks(fontsize = 10)
    plt.yticks(fontsize = 10)
    plt.legend()
    plt.show()
    print(f'O coeficiente de saturação é {coef_saturação}')
    # print(f'slope {a}')
    print(f'A tensão limiar é {x0}')
    


def salvar_dados():
    with open(caminho_arquivo, 'w') as file:
        file.write("Tempo            VDS              VGS              IDS              IGS         |IDS|         sqrt(|IDS|)    V_limiar    coef_angular  mobilidade\n")
        for i in range(len(tempo)):
            if i == 0:
                file.write("{:.7e}  {:.7e}  {:.7e}  {:.7e}  {:.7e} {:.7e}  {:.7e}    {:.7e}  {:.7e}   {:.7e}\n".format(
                    tempo[i], vds[i], vgs[i], ids[i], igs[i], abs_ids[i], sqrt_ids[i], x0, a, coef_saturação))
            else:
                file.write("{:.7e}  {:.7e}  {:.7e}  {:.7e}  {:.7e} {:.7e}  {:.7e}    \n".format(
                    tempo[i], vds[i], vgs[i], ids[i], igs[i], abs_ids[i], sqrt_ids[i]))

caminho_arquivo = 'C:/Users/Estudante/Desktop/LOEM/Alice/OFET/24 08 12 (férias)/Disp 2/80um/80um 24 08 08 (-40V) perfeito/50 primeiras/Autosave-2024-08-08~15.17.s-000-.txt'
ler_arquivo_txt(caminho_arquivo)
salvar_dados()

