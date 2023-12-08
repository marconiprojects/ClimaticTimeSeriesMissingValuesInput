from ast import Index
from threading import local
from tkinter import *
from tkinter import ttk
from tkinter import filedialog as dlg
from tkinter import messagebox as msg
import matplotlib.dates as mdates
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk) 
from matplotlib.figure import Figure 
import datetime as dt
from matplotlib.pyplot import text, title
from scipy import stats
from folium.map import Popup
from haversine import haversine, Unit
from math import floor
from sklearn import tree
from sklearn.neural_network import MLPRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR
import matplotlib.pyplot as plt
import numpy as np
from tksheet import Sheet
import os, csv, time, folium, webbrowser, math, pickle,pyscreenshot

fundo = '#4F4F4F' #? Cor de fundo da tela
fun_b = '#3CB371' #? Cor de fundo dos botoes
fun_ap = '#9C444C'
fun_alt = '#C99418'
fun_meta_le = '#191970'


class Tratamento:
    global alvo
    global vizinhaA
    global vizinhaB
    global vizinhaC
    global download
    alvo = vizinhaA = vizinhaB = vizinhaC = download = ''
    def __init__(self):
        self.alvo = alvo
        self.vizinhaA = vizinhaA
        self.vizinhaB = vizinhaB
        self.vizinhaC = vizinhaC
        self.download = download
        
        
    # def __init__(self, alvo, vizinhaA, vizinhaB, vizinhaC, download):
    def procura_colunas(self, a, b):

        est = (str(b).split(' '))[2]
        est = est.strip("]")
        est = est.strip("'")
        

        if est[0] != 'A':
            coluna_prec = 3
            coluna_tmax = 4
            coluna_tmin = 6    
        else:
            coluna_prec = 1
            coluna_tmax = 4
            coluna_tmin = 6
            
        
        return coluna_prec, coluna_tmax, coluna_tmin
    def get_data_trada(self): #! Funçao para retornar os dados tratados
        diretorio = [self.alvo, self.vizinhaA, self.vizinhaB, self.vizinhaC]
       
        temp = [str(self.download) + "/alvo_limpa.txt", str(self.download) + "/vizinhaA_limpa.txt", str(self.download) + "/vizinhaB_limpa.txt", str(self.download) + "/vizinhaC_limpa.txt"]
        
        arq1 = open("end.txt", "w")
        
        arq1.write(str(self.download) + "/alvo_limpa.txt\n" + str(self.download) + "/vizinhaA_limpa.txt\n" + str(self.download) + "/vizinhaB_limpa.txt\n" + str(self.download) + "/vizinhaC_limpa.txt\n" + str(self.download) + '/dadoscomum.csv\n' + str(self.download) + '/buff.txt\n' + str(self.download) + '/Coordenadas.txt\n')
        arq1.close()
        
        '''arq1 = open("end.txt", "w")
        arq1.write(str(self.download) + "/alvo_limpa.txt\n" + str(self.download) + "/vizinhaA_limpa.txt\n" + str(self.download) + "/vizinhaB_limpa.txt\n" + str(self.download) + "/vizinhaC_limpa.txt")
        arq1.close()'''
        cont = 0
        comum_alvo = comum_vizA = comum_vizB = comum_vizC = list()

        for dir in diretorio:
            aux = list()
            with open(dir) as arq: #* Abrindo os arquivos .csv e armazenando numa lista
                reader = csv.reader(arq, delimiter=';')
                for line in reader:
                    aux.append(line)
            del aux[10][len(aux[10])-1]

            cp, ctmax, ctmin = self.procura_colunas(aux[10], aux[1])

            del aux[len(aux)-1]      #? Remove a ultima linha em branco do arquivo, da pra fazer isso manualmente, mas caso o usuario trabalhe com inumeros arquivos, remover a ultima linha de cada arquivo pode ser um trabalho massante 
            del aux[0:11]            #? Remove o cabeçalho do arquivo .csv

            colunas = [cp, ctmax, ctmin]
            
            buff = list()
            
            for i in range(len(aux)):
                buff2 = list()
                buff2.append(aux[i][0])
                for j in colunas:
                    buff2.append(aux[i][j])
                   
                buff.append(buff2)
            
            
                
            final = list()  #* Lista final 

            for i in range(len(buff)): #* Removendo todas as linhas que possuem o valor null em seu parametros
                condicao = 0
                for j in range(1,4):
                    if buff[i][j] == 'null' or buff[i][j] == '':
                        condicao = 1

                if condicao == 0:
                    final.append(buff[i])
                       

            
            for i in range(len(final)): #* Passando a data de AAAA-MM-DD para AAAA, MM, DD
                aux.clear()
                
                for j in range(4):
                    aux.append(final[i][j])
                
                data = aux[0]
                data = str(data).split('-')

                final[i].insert(0, int(data[0]))
                final[i].insert(1, int(data[1]))
                final[i].insert(2, int(data[2]))
        
                del final[i][3]
           
            new_arq = open(temp[cont], 'w')    #TODO: Salvando os dados em arquivos .txt
            teste = list()
            for i in final:
                aux = list()
                for j in range(len(i)):
                    aux.append(str(i[j]).replace(',', '.'))
                teste.append(aux)
            for i in teste:
                if cont == 0:
                    comum_alvo.append(str(i).replace(' ', ''))
                elif cont == 1:
                    comum_vizA.append(str(i).replace(' ', ''))
                elif cont == 2:
                    comum_vizB.append(str(i).replace(' ', ''))
                else:
                    comum_vizC.append(str(i).replace(' ', ''))

                i = str(i).strip("[")
                i = str(i).strip("]")
                i = i.replace(' ', '')
                
                
                new_arq.write(str(i)+"\n")
            new_arq.close()
            cont += 1
        self.get_coordinates()
        
        self.dadosc2()
        
    def dadosc(self):
        #subprocess.call(r'E:\IC\Interface_Grafica\codes\dadosc.py', shell=True)
        cid1, t1 = self.prepara_dadosc(str(self.download) + "/alvo_limpa.txt")
        cid2, t2 = self.prepara_dadosc(str(self.download) + "/vizinhaA_limpa.txt")
        cid3, t3 = self.prepara_dadosc(str(self.download) + "/vizinhaB_limpa.txt")
        cid4, t4 = self.prepara_dadosc(str(self.download) + "/vizinhaC_limpa.txt")
        
        ano_ini = max([cid1[0][0], cid2[0][0], cid3[0][0], cid4[0][0]])
        fim = min(len(cid1), len(cid2), len(cid3), len(cid4))
        
        for i in range(len(cid1)):
            if ano_ini == cid1[i][0]:
                ind1 = i
                break
        for i in range(len(cid2)):
            if ano_ini == cid2[i][0]:
                ind2 = i
                break
        for i in range(len(cid3)):
            if ano_ini == cid3[i][0]:
                ind3 = i
                break
        for i in range(len(cid4)):
            if ano_ini == cid4[i][0]:
                ind4 = i
                break
        
        final = list()
        aux = list()
        '''
        arq1 = open('end.txt', 'a')
        arq1.write('\n' + str(self.download) + '/dadoscomum.csv\n' + str(self.download) + '/buff.txt\n' + '/Coordenadas.txt\n')
        arq1.close()
        '''
        arq = open(str(self.download) + '/dadoscomum.txt', 'w')
        arq_b = open(str(self.download) + '/buff.txt', 'w')
        total = 0
        ind1 = ind2 = ind3 = ind4 = 0
        
        for i in range(fim):
            
            ano1 = int(cid1[ind1+i][0])
            mes1 = int(cid1[ind1+i][1])
            dia1 = int(cid1[ind1+i][2])
            cond1 = 0
            for j in range(fim):
                ano2 = int(cid2[ind2+j][0])
                mes2 = int(cid2[ind2+j][1])
                dia2 = int(cid2[ind2+j][2])
                if (ano1 == ano2) and (mes1 == mes2) and (dia1 == dia2):
                    
                    for k in range(fim):
                        ano3 = int(cid3[ind3+k][0])
                        mes3 = int(cid3[ind3+k][1])
                        dia3 = int(cid3[ind3+k][2]) 
                        
                        if (ano2 == ano3) and (mes2 == mes3) and (dia2 == dia3):
                                
                                
                                for z in range(fim):
                                    ano4 = int(cid4[ind4+z][0])
                                    mes4 = int(cid4[ind4+z][1])
                                    dia4 = int(cid4[ind4+z][2])
                                    
                                    if (ano3 == ano4) and (mes3 == mes4) and (dia3 == dia4):
                                        
                                        aux.clear()
                                        
                                        """  -> Adicionando os dados numa lista <-  """
                                        buff = ''   
                                        buff = str(ano1) + " " + str(mes1) + " " + str(dia1) + " " + cid1[ind1+i][3] + " " + cid1[ind1+i][4] + " " + cid1[ind1+i][5] + " " + cid2[ind2+j][3] + " " + cid2[ind2+j][4] + " " + cid2[ind2+j][5] + " " + cid3[ind3+k][3] + " " + cid3[ind3+k][4] + " " + cid3[ind3+k][5] + " " + cid4[ind4+z][3] + " " + cid4[ind4+z][4] + " " + cid4[ind4+z][5]  
                                        buff = str(buff).split()
                                        final.append(buff)
                                        
                                        """  -> Adicinando os dados num arquivo .csv <-  """
                                        buff = ''
                                        buff = str(ano1) + ";" + str(mes1) + ";" + str(dia1) + ";" + cid1[ind1+i][3] + ";" + cid1[ind1+i][4] + ";" + cid1[ind1+i][5] + ";" + cid2[ind2+j][3] + ";" + cid2[ind2+j][4] + ";" + cid2[ind2+j][5] + ";" + cid3[ind3+k][3] + ";" + cid3[ind3+k][4] + ";" + cid3[ind3+k][5] + ";" + cid4[ind4+z][3] + ";" + cid4[ind4+z][4] + ";" + cid4[ind4+z][5] + ";\n"
                                        
                                        arq.write(buff)
                                        total += 1
                                        cond1 = 1
                                        break
                                    
                                    
                                
                        if (cond1 == 1):
                            break
                
                if(cond1 == 1):
                    break
        arq_b.write(str(total) + " " + str(t1) + " " + str(t2) + " " + str(t3) + " " + str(t4))
        arq.close()
        arq_b.close()
        
    def dadosc2(self):
        alv, t1 = self.prepara_dadosc(str(self.download) + "/alvo_limpa.txt")
        vizA, t2 = self.prepara_dadosc(str(self.download) + "/vizinhaA_limpa.txt")
        vizB, t3 = self.prepara_dadosc(str(self.download) + "/vizinhaB_limpa.txt")
        vizC, t4 = self.prepara_dadosc(str(self.download) + "/vizinhaC_limpa.txt")
        comeca = max(alv[0][0], vizA[0][0], vizB[0][0], vizC[0][0])

        ind1 = ind2 = ind3 = ind4 = 0
        for i in range(len(alv)):
            if int(comeca )== int(alv[i][0]):
                ind1 = i
                break
        for i in range(len(vizA)):
            if int(comeca)== int(vizA[i][0]):
                ind2 = i
                break
        for i in range(len(vizA)):
            if int(comeca)== int(vizB[i][0]):
                ind3 = i
                break
        for i in range(len(vizA)):
            if int(comeca)== int(vizC[i][0]):
                ind4 = i
                break
        arq = open(str(self.download) + '/dadoscomum.csv', 'w')
        arq_b = open(str(self.download) + '/buff.txt', 'w')
        comum =0
        for i in range(ind1, len(alv)):
            try:
                ano1 = alv[i][0]
                mes1 = alv[i][1]
                dia1 = alv[i][2]
                for j in range(ind2, len(vizA)):
                    ano2 = vizA[j][0]
                    mes2 = vizA[j][1]
                    dia2 = vizA[j][2]
                    if (ano1 == ano2) and (mes1 == mes2) and (dia1 == dia2):
                        for k in range(ind3, len(vizB)):
                            ano3 = vizB[k][0]
                            mes3 = vizB[k][1]
                            dia3 = vizB[k][2]
                            if (ano2 == ano3) and (mes2 == mes3) and (dia2 == dia3):
                                for l in range(ind4, len(vizC)):
                                    ano4 = vizC[l][0]
                                    mes4 = vizC[l][1]
                                    dia4 = vizC[l][2]
                                    if (ano3 == ano4) and (mes3 == mes4) and (dia3 == dia4):
                                        t_alv = str(alv[i]).strip('[')
                                        t_alv = t_alv.strip(']')
                                        t_alv = t_alv.replace(' ', '')
                                        
                                        del vizA[j][:3]
                                        t_vizA = str(vizA[j]).strip('[')
                                        t_vizA = t_vizA.strip(']')
                                        t_vizA = t_vizA.replace(' ', '')
                                        
                                        del vizB[k][:3]
                                        t_vizB = str(vizB[k]).strip('[')
                                        t_vizB = t_vizB.strip(']')
                                        t_vizB = t_vizB.replace(' ', '')
                                        
                                        del vizC[l][:3]
                                        t_vizC = str(vizC[l]).strip('[')
                                        t_vizC = t_vizC.strip(']')
                                        t_vizC = t_vizC.replace(' ', '')

                                        texto = t_alv + ',' + t_vizA + ',' + t_vizB + ',' + t_vizC
                                        texto = texto.replace(',', ';')
                                        
                                        #texto  = str(ano1) + ";" + str(mes1) + ";" + str(dia1) + ";" + alv[ind1+i][3] + ";" + alv[ind1+i][4] + ";" + alv[ind1+i][5] + ";" + vizA[ind2+j][3] + ";" + vizA[ind2+j][4] + ";" + vizA[ind2+j][5] + ";" + vizB[ind3+k][3] + ";" + vizB[ind3+k][4] + ";" + vizB[ind3+k][5] + ";" + vizC[ind4+l][3] + ";" + vizC[ind4+l][4] + ";" + vizC[ind4+l][5] + ";\n"                           
                                        
                                        arq.write(texto + ';\n')
                                        comum += 1    
            except IndexError:
                pass
        arq_b.write(str(comum) + " " + str(t1) + " " + str(t2) + " " + str(t3) + " " + str(t4))
        arq.close()
        arq_b.close()

    def prepara_dadosc(self, dir):
        arq = open(dir)
        lista = list()

        t=0
        for i in arq:
            i = i.strip()
            i = i.replace("'",'')
            i = i.replace(" ",'')
            i = i.split(',')    
            lista.append(i)
            
            t += 1
        
        return lista, t


    def retorna_arq(self, op):
        arq = open('end.txt') 
        a = arq.readlines()
        arq.close()
        if op == 'Cidade alvo':
            di = a[0].replace("\n", '')
        elif op == 'Vizinha A':
            di = a[1].replace("\n", '')
        elif op == 'Vizinha B':
            di = a[2].replace("\n", '')
        elif op == 'Vizinha C':
            di = a[3].replace("\n", '')
        elif op == 'Dados comum':
            di = a[4].replace("\n", '')
            
        

        
        lista = list()
        
        arq = open(di)
        
        for i in arq:
            
            i = i.replace('\n', '')
            i = i.strip()
            i = i.replace("'",'')
            i = i.replace(" ",'')
            
            if op == 'Dados comum':
                i = i.split(';')
                del i[len(i)-1]
                
            else:
                i = i.split(',')  
            lista.append(i)
        arq.close()
        
        return lista
    
    def get_range(self, op):
        controle = 0
        arq = open('end.txt') 
        a = arq.readlines()
        arq.close()
        if op == 'Cidade alvo':
            di = a[0].replace("\n", '')
        elif op == 'Vizinha A':
            di = a[1].replace("\n", '')
        elif op == 'Vizinha B':
            di = a[2].replace("\n", '')
        elif op == 'Vizinha C':
            di = a[3].replace("\n", '')
        elif op == 'Dados comum':
            di = a[4].replace("\n", '')
            controle = 1
            
        arq = open(di)
        aux = list()

        for i in arq:
            i = i.strip()
            i = i.replace("'",'')
            i = i.replace(" ",'')
            if controle == 1:
                i = i.split(';')
                del i[len(i)-1]
            else:
                i = i.split(',')
            aux.append(int(i[0]))
        arq.close()
        
        anos = list()
        
        buff = aux[0]
    
        anos.append(buff)
        
        for i in range(1,len(aux)): 
            try:
                if aux[i-1] != aux[i]:
                    buff = aux[i]
                    anos.append(buff)
            except IndexError:
                pass
        return anos

    def get_qtd(self):
        arq = open('end.txt') 
        a = arq.readlines()
        arq = open(a[5].replace("\n", ''))
        
        a = arq.readline()
        a = a.split()
        ut = int(a[0])
        Tar = int(a[1])
        vA = int(a[2])
        vB = int(a[3])
        vC = int(a[4])
        arq.close()
        return ut, Tar,vA, vB, vC

    def normalizar_dados(self, mat):
        max_min = list()
        aux = list()
        t = len(mat[0])
        for i in range(t):
            aux.clear()
            for j in range(len(mat)):
                aux.append(mat[j][i])
            max_min.append(max(aux))
            max_min.append(min(aux))

        dadosn =list()
        
    
        for i in range(len(mat)):
            cont = 0
            buff = list()
            for j in range(t):
                if cont <= 36:
                    maior = max_min[cont]
                    menor = max_min[cont + 1]
                    dado = ((float(mat[i][j]) - float(menor)) / (float(maior) - float(menor))) * 0.6 + 0.2
                    buff.append(dado)
                    cont = cont + 2
            dadosn.append(buff)
        
        
        return dadosn

    def get_coordinates(self): # ? Função para obter as coordenadas de cada cidade
        coordenadas = list()
        aux = list()
        arq1 = open('end.txt') 
        a = arq1.readlines()
        locais = [self.alvo, self.vizinhaA, self.vizinhaB, self.vizinhaC]
        
        for i in locais:
            aux.clear()
            with open(i) as arq:
                reader = csv.reader(arq)
                for j in reader:
                    aux.append(j)
            arq.close()
            del aux[10:]

            estacao = str(aux[0]).split(':')
            estacao = estacao[1].strip(']')
            estacao = (estacao.strip("'")).strip()

            latitude = str(aux[2]).split(':')
            latitude = latitude[1].strip(']')
            latitude = (latitude.strip("'")).strip()

            longitude = str(aux[3]).split(':')
            longitude = longitude[1].strip(']')
            longitude = (longitude.strip("'")).strip()

            altitude = str(aux[4]).split(':')
            altitude = altitude[1].strip(']')
            altitude = (altitude.strip("'")).strip()

            coordenadas.append(estacao)
            coordenadas.append(latitude)
            coordenadas.append(longitude)
            coordenadas.append(altitude)
        
        arq = open(a[6].replace("\n", ''), 'w')
        for i in coordenadas:
            arq.write(i)
            arq.write('\n')
        arq1.close() 
        arq.close()    
    
    def get_local_cord(self):
        arq = open('end.txt') 
        a = arq.readlines()
        aux = a[6].replace("\n", '')
        return aux
    
    def retorna_end(self, op):
        arq = open('end.txt') 
        a = arq.readlines()

        if op == 'Cidade alvo':
            return a[0].replace("\n", '')
        elif op == 'Vizinha A':
            return a[1].replace("\n", '')
        elif op == 'Vizinha B':
            return a[2].replace("\n", '')
        elif op == 'Vizinha C':
            return a[3].replace("\n", '')

class Triangulaction:
    def __init__(self):
        self.coordenadas = list()
        cod_trat = Tratamento()
        local = cod_trat.get_local_cord()
        arq = open(local)
        aux = list()
        for i in arq:
            aux.append(i)
        for i in range(len(aux)):
            aux[i] = str(aux[i]).strip('\n')   
            self.coordenadas.append(aux[i])
        
        dt_alv = list()
        dt_cidA = list()
        dt_cidB = list()
        dt_cidC = list()
        for i in range(0,4):
            dt_alv.append(self.coordenadas[i])
        for i in range(4,8):
            dt_cidA.append(self.coordenadas[i])
        for i in range(8,12):
            dt_cidB.append(self.coordenadas[i])
        for i in range(12,16):
            dt_cidC.append(self.coordenadas[i])

        self.tupla_tg = (float(dt_alv[1]), float(dt_alv[2]))
        self.tupla_cA = (float(dt_cidA[1]), float(dt_cidA[2]))
        self.tupla_cB = (float(dt_cidB[1]), float(dt_cidB[2]))
        self.tupla_cC = (float(dt_cidC[1]), float(dt_cidC[2]))
        self.h = [float(self.coordenadas[3]), float(self.coordenadas[7]), float(self.coordenadas[11]), float(self.coordenadas[15])]
        d1 = round(haversine(self.tupla_tg, self.tupla_cA, Unit.KILOMETERS), 4)
        d2 = round(haversine(self.tupla_tg, self.tupla_cB, Unit.KILOMETERS), 4)
        d3 = round(haversine(self.tupla_tg, self.tupla_cC, Unit.KILOMETERS), 4)
        media = (d1 + d2 + d3) / 3
        self.d = [d1, d2, d3]
    
    def idw(self, foco): # Todo: 1 - Precipitação, 2 - Temperatura Máxima, 3 - Temperatura Miníma
        t = Tratamento()

        distancia = self.d

        self.idw_x = list()
        self.idw_y = list()
        self.idw_alv_y = list()
        if foco == 1:
            ind = 6
            a = 3
            data = t.normalizar_dados(t.retorna_arq('Dados comum'))
        elif foco == 2:
            ind = 7
            a = 4
            data = t.retorna_arq('Dados comum')
        elif foco == 3:
            ind = 8
            a = 5
            data = t.retorna_arq('Dados comum')

        aux = list()
        cont2 = 1


        self.mat_meta_idw = list()
        for i in range(len(data)):
            cont = 0
            soma = 0
            for j in range(ind,15,3):
                soma = soma + (float(data[i][j])/distancia[cont])
                cont += 1
            
            calc_idw = round(soma / (1/distancia[0] + 1/distancia[1] + 1/distancia[2]),4)
            aux = list()
            aux.append(float(data[i][0]))
            aux.append(float(data[i][1]))
            aux.append(float(data[i][2]))
            aux.append(calc_idw)

            self.mat_meta_idw.append(aux) #Matriz para o meta learning
            
            self.idw_x.append(cont2)
            self.idw_y.append(float(calc_idw))
            self.idw_alv_y.append(float(data[i][a]))

            cont2 += 1


        self.idw_erro_abs, self.idw_erro_rel = self.calcula_erros(self.idw_y, self.idw_alv_y)

    def get_idw(self):
        return self.idw_x, self.idw_y, self.idw_alv_y, self.idw_erro_abs, self.idw_erro_rel, self.mat_meta_idw
    
    def aa(self, foco):
        t = Tratamento()


        self.aa_x = list()
        self.aa_y = list()
        self.aa_alv_y = list()

        if foco == 1:
            ind = 6
            a = 3
            data = t.normalizar_dados(t.retorna_arq('Dados comum'))
        elif foco == 2:
            ind = 7
            a = 4
            data = t.retorna_arq('Dados comum')
        elif foco == 3:
            ind = 8
            a = 5
            data = t.retorna_arq('Dados comum')

        cont = 1
        self.mat_meta_aa = list()
        
        for i in range(len(data)): #Resolver depois para mais de 3 estações vizinhas
            soma = 0
            for j in range(ind, 15, 3):
                soma = soma + float(data[i][j])
            
            aa = (1/3) * soma
            aux = list()

            aux.append(float(data[i][0]))
            aux.append(float(data[i][1]))
            aux.append(float(data[i][2]))
            aux.append(aa)
            self.mat_meta_aa.append(aux)

            self.aa_x.append(cont)
            self.aa_y.append(aa)
            self.aa_alv_y.append(float(data[i][a]))

            cont += 1
        
        self.aa_erro_abs, self.aa_erro_rel = self.calcula_erros(self.aa_y, self.aa_alv_y)

    def get_aa(self):
        return self.aa_x, self.aa_y, self.aa_alv_y, self.aa_erro_abs, self.aa_erro_rel, self.mat_meta_aa

    def show_map(self):
        m = folium.Map(location=self.tupla_tg)
        folium.Marker(location=self.tupla_tg, popup=Popup('Target', show=True)).add_to(m)
        folium.Marker(location=self.tupla_cA, popup=Popup('Vizinha A', show=True)).add_to(m)
        folium.Marker(location=self.tupla_cB, popup=Popup('Vizinha B', show=True)).add_to(m)
        folium.Marker(location=self.tupla_cC, popup=Popup('Vizinha C', show=True)).add_to(m)
        m.save('map.html')
    
        webbrowser.open_new_tab('map.html')
    
    def oidw(self, foco):
        qtd_est = 4 #Quantidade de estações utilizadas


        month_a_tar = self.generate_mothly_ave(foco, 'target')
        month_a_vA = self.generate_mothly_ave(foco, 'VizA')
        month_a_vB = self.generate_mothly_ave(foco, 'VizB')
        month_a_vC = self.generate_mothly_ave(foco, 'VizC')

        ma = list()
        for i in range(len(month_a_tar)):
            aux = list()
            aux.append(month_a_tar[i])
            aux.append(month_a_vA[i])
            aux.append(month_a_vB[i])
            aux.append(month_a_vC[i])
            ma.append(aux)
        
        

        if foco == 1:
            ind = 6
        elif foco == 2:
            ind = 7
        elif foco == 3:
            ind = 8

        t = Tratamento()
        data = t.retorna_arq('Dados comum')
        
        final_oidw = list()
        soma_p1 = 0
        soma_p2 = 0
        cont_ma_linha = 0
        cont_ma_coluna = 1
        cont_est = 0
        for i in range(len(data)):
            try:
                if data[i][1] != data[i+1][1]:
                    cont_est = 0
                    cont_ma_coluna = 1
                    for j in range(ind, 15, 3):
                        soma_p1 = soma_p1 + ((float(data[i][j]) * ma[cont_ma_linha][0] * math.log(self.h[0])) / (self.d[cont_est] + ma[cont_ma_linha][cont_ma_coluna] * math.log(self.h[cont_ma_coluna])))
                        soma_p2 = (1/self.d[0] + 1/self.d[1] + 1/self.d[2])
                        cont_est += 1
                        cont_ma_coluna += 1
                    
                    final_oidw.append(soma_p1/soma_p2)
                    soma_p1 = 0
                    soma_p2 = 0
                    cont_ma_linha += 1
                else:
                    cont_est = 0
                    cont_ma_coluna = 1
                    for j in range(ind, 15, 3):
                        soma_p1 = soma_p1 + ((float(data[i][j]) * ma[cont_ma_linha][0] * math.log(self.h[0])) / (self.d[cont_est] + ma[cont_ma_linha][cont_ma_coluna] * math.log(self.h[cont_ma_coluna])))
                        soma_p2 = (1/self.d[0] + 1/self.d[1] + 1/self.d[2])
                        cont_est += 1
                        cont_ma_coluna += 1
            except IndexError:
                pass
        
                
    def rw(self, foco):
        qtd_est = 3
        month_a_tar = self.generate_mothly_ave(foco, 'target')
        month_a_vA = self.generate_mothly_ave(foco, 'VizA')
        month_a_vB = self.generate_mothly_ave(foco, 'VizB')
        month_a_vC = self.generate_mothly_ave(foco, 'VizC')

        if foco == 1:
            ind = 6
        elif foco == 2:
            ind = 7
        elif foco == 3:
            ind = 8
            
        ma = list()
        self.idw_x = list()
        self.idw_y = list()
        self.idw_alv_y = list()
        for i in range(len(month_a_tar)):
            aux = list()
            aux.append(month_a_tar[i])
            aux.append(month_a_vA[i])
            aux.append(month_a_vB[i])
            aux.append(month_a_vC[i])
            ma.append(aux)   

        t = Tratamento()
        data = t.retorna_arq('Dados comum')
        
        cont_indc = 0

        
        soma = 0
        resultado = list()
        linha_ma = 0
        for i in range(len(data)):
            try:
                if i == self.ind_fim[cont_indc]:
                    soma = ((ma[linha_ma][0]/ma[linha_ma][1])*float(data[i][ind]) + (ma[linha_ma][0]/ma[linha_ma][2])*float(data[i][ind+3]) + (ma[linha_ma][0]/ma[linha_ma][3])*float(data[i][ind+6])) * (1/3)
                    resultado.append(soma)
                    soma = 0
                    linha_ma = linha_ma + 1
                    cont_indc += 1
                else:
                    soma = ((ma[linha_ma][0]/ma[linha_ma][1])*float(data[i][ind]) + (ma[linha_ma][0]/ma[linha_ma][2])*float(data[i][ind+3]) + (ma[linha_ma][0]/ma[linha_ma][3])*float(data[i][ind+6])) * (1/3)   
                    resultado.append(soma)
                    soma = 0
            except IndexError:
                soma = ((ma[linha_ma-1][0]/ma[linha_ma-1][1])*float(data[i][ind]) + (ma[linha_ma-1][0]/ma[linha_ma-1][2])*float(data[i][ind+3]) + (ma[linha_ma-1][0]/ma[linha_ma-1][3])*float(data[i][ind+6])) * (1/3)   
                resultado.append(soma)
                soma = 0
 
        self.rw_x = list()
        self.rw_y = list()
        self.rw_alv_y = list()
        self.mat_meta_rw = list()

        
        x = 0
        for i in range(len(data)):
            self.rw_x.append(x)
            self.rw_y.append(resultado[i])
            self.rw_alv_y.append(float(data[i][ind-3]))

            aux = list()
            aux.append(float(data[i][0]))
            aux.append(float(data[i][1]))
            aux.append(float(data[i][2]))
            aux.append(float(resultado[i]))
            self.mat_meta_rw.append(aux)
            

            x += 1
            
        self.rw_erro_abs, self.rw_erro_rel = self.calcula_erros(self.rw_y, self.rw_alv_y)
    
    def get_rw(self):
        return self.rw_x, self.rw_y, self.rw_alv_y, self.rw_erro_abs, self.rw_erro_rel, self.mat_meta_rw

    def generate_mothly_ave(self, foco, cidade):
        t = Tratamento()
        

        mon_ave = list()
        self.ind_fim = list()
        soma = 0
        cont = 2


        if cidade == 'target':
            if foco == 1:
                ind = 3 #precipitação na target
                data = t.normalizar_dados(t.retorna_arq('Dados comum'))
            elif foco == 2:
                ind = 4 #Temperatura maxima na target
                data = t.retorna_arq('Dados comum')
            elif foco == 3:
                ind = 5 #Temperatura minima na target
                data = t.retorna_arq('Dados comum')
        elif cidade == 'VizA':
            if foco == 1:
                ind = 6 
                data = t.normalizar_dados(t.retorna_arq('Dados comum'))
            elif foco == 2:
                ind = 7
                data = t.retorna_arq('Dados comum')
            elif foco == 3:
                ind = 8
                data = t.retorna_arq('Dados comum')
        elif cidade == 'vizB':
            if foco == 1:
                ind = 9
                data = t.normalizar_dados(t.retorna_arq('Dados comum'))
            elif foco == 2:
                ind = 10
                data = t.retorna_arq('Dados comum')
            elif foco == 3:
                ind = 11
                data = t.retorna_arq('Dados comum')
        else:
            if foco == 1:
                ind = 12
                data = t.normalizar_dados(t.retorna_arq('Dados comum'))
            elif foco == 2:
                ind = 13
                data = t.retorna_arq('Dados comum')
            elif foco == 3:
                ind = 14
                data = t.retorna_arq('Dados comum')

        

        #encontar o index da ultima data de cada mes
        for i in range(len(data)):
            try:
                if data[i][1] != data[i+1][1]:
                    self.ind_fim.append(i)
            except IndexError:
                pass
       
        for i in range(len(data)):
            try:
                if data[i][1] != data[i+1][1]:
                    soma = soma + float(data[i][ind])
                    cont = cont + 1
                    mon_ave.append(soma/cont)
                    soma = 0
                    cont = 1
                else:
                    soma = soma + float(data[i][ind])
                    cont = cont + 1

                
            except IndexError:
                pass
        return mon_ave

    def generate_correlation_coef(self, foco):
        t = Tratamento()
        nor = Treinamento()
        t.retorna_arq
        if foco == 1:
            ind = 3 #precipitação na target
            data = nor.normalizar(t.retorna_arq('Dados comum'))
        elif foco == 2:
            ind = 4 #Temperatura maxima na target
            data = t.retorna_arq('Dados comum')
        elif foco == 3:
            ind = 5 #Temperatura minima na target
            data = t.retorna_arq('Dados comum')


        coef_tg_A = list()
        coef_tg_B = list()
        coef_tg_C = list()
        dias = list()
        cont_d = 0 #Contador de dias
        aux1 = list()
        aux2 = list()
        aux3 = list()
        aux4 = list()

        dias_exc = list() #Guardar indicies onde em um mes tem menos de 2 dias de dados
        for i in range(len(data)):
            try:
                if data[i][1] != data[i+1][1]:
                    aux1.append(float(data[i][ind]))
                    aux2.append(float(data[i][ind+3]))
                    aux3.append(float(data[i][ind+6]))
                    aux4.append(float(data[i][ind+9]))
                    cont_d += 1
                    if cont_d >= 2:
                        dias.append(cont_d)
                        cont_d = 0

                        v1 = stats.pearsonr(aux1, aux2)
                        v2 = stats.pearsonr(aux1, aux3)
                        v3 = stats.pearsonr(aux1, aux4)
                        coef_tg_A.append(v1[0])
                        coef_tg_B.append(v2[0])
                        coef_tg_C.append(v3[0])

                        aux1 = list()
                        aux2 = list()
                        aux3 = list()
                        aux4 = list()
                    else:
                        dias_exc.append(i)
                else:
                    aux1.append(float(data[i][ind]))
                    aux2.append(float(data[i][ind+3]))
                    aux3.append(float(data[i][ind+6]))
                    aux4.append(float(data[i][ind+9]))
                    cont_d += 1
            except IndexError:
                aux1.append(float(data[i-1][ind]))
                aux2.append(float(data[i-1][ind+3]))
                aux3.append(float(data[i-1][ind+6]))
                aux4.append(float(data[i-1][ind+9]))
                cont_d += 1

        return  dias, coef_tg_A, coef_tg_B, coef_tg_C

    def onr(self, foco):
        qtd_est = 3

        
        d, cA, cB, cC = self.generate_correlation_coef(foco)

        if foco == 1:
            ind = 6
        elif foco == 2:
            ind = 7
        elif foco == 3:
            ind = 8

        t = Tratamento()
        data = t.retorna_arq('Dados comum')
        
        self.onr_y = list()
        cont_cor = 0
        resultado = list()
        for i in range(len(data)):
            try:
                if data[i][1] != data[i+1][1]:
                    soma1 = math.pow(cA[cont_cor], 2*((d[cont_cor]-2)/(1-cA[cont_cor]))) * float(data[i][ind])
                    soma1 = soma1 + math.pow(cB[cont_cor], 2*((d[cont_cor]-2)/(1-cB[cont_cor]))) * float(data[i][ind+3])
                    soma1 = soma1 + math.pow(cC[cont_cor], 2*((d[cont_cor]-2)/(1-cC[cont_cor]))) * float(data[i][ind+6])

                    soma2 = math.pow(cA[cont_cor], 2*((d[cont_cor]-2)/(1-cA[cont_cor]))) + math.pow(cB[cont_cor], 2*((d[cont_cor]-2)/(1-cB[cont_cor]))) +math.pow(cC[cont_cor], 2*((d[cont_cor]-2)/(1-cC[cont_cor])))
                    resultado.append(soma1/soma2)
                    cont_cor += 1
                    soma1 = 0
                    soma2 = 0
                    
                else:
                
                    soma1 = math.pow(cA[cont_cor], 2*((d[cont_cor]-2)/(1-cA[cont_cor]))) * float(data[i][ind])
                    soma1 = soma1 + math.pow(cB[cont_cor], 2*((d[cont_cor]-2)/(1-cB[cont_cor]))) * float(data[i][ind+3])
                    soma1 = soma1 + math.pow(cC[cont_cor], 2*((d[cont_cor]-2)/(1-cC[cont_cor]))) * float(data[i][ind+6])

                    soma2 = math.pow(cA[cont_cor], 2*((d[cont_cor]-2)/(1-cA[cont_cor]))) + math.pow(cB[cont_cor], 2*((d[cont_cor]-2)/(1-cB[cont_cor]))) +math.pow(cC[cont_cor], 2*((d[cont_cor]-2)/(1-cC[cont_cor])))
                    resultado.append(soma1/soma2)
                    
                    soma1 = 0
                    soma2 = 0

            except IndexError:
                soma1 = math.pow(cA[cont_cor-1], 2*((d[cont_cor-1]-2)/(1-cA[cont_cor-1]))) * float(data[i][ind])
                soma1 = soma1 + math.pow(cB[cont_cor-1], 2*((d[cont_cor-1]-2)/(1-cB[cont_cor-1]))) * float(data[i][ind+3])
                soma1 = soma1 + math.pow(cC[cont_cor-1], 2*((d[cont_cor-1]-2)/(1-cC[cont_cor-1]))) * float(data[i][ind+6])

                soma2 = math.pow(cA[cont_cor-1], 2*((d[cont_cor-1]-2)/(1-cA[cont_cor-1]))) + math.pow(cB[cont_cor-1], 2*((d[cont_cor-1]-2)/(1-cB[cont_cor-1]))) +math.pow(cC[cont_cor-1], 2*((d[cont_cor-1]-2)/(1-cC[cont_cor-1])))
                resultado.append(soma1/soma2)
                soma1 = 0
                soma2 = 0

            except ValueError:
                soma1 = math.pow(cA[cont_cor-1], 2*((d[cont_cor-1]-2)/(1-cA[cont_cor-1]))) * float(data[i][ind])
                soma1 = soma1 + math.pow(cB[cont_cor-1], 2*((d[cont_cor-1]-2)/(1-cB[cont_cor-1]))) * float(data[i][ind+3])
                soma1 = soma1 + math.pow(cC[cont_cor-1], 2*((d[cont_cor-1]-2)/(1-cC[cont_cor-1]))) * float(data[i][ind+6])

                soma2 = math.pow(cA[cont_cor-1], 2*((d[cont_cor-1]-2)/(1-cA[cont_cor-1]))) + math.pow(cB[cont_cor-1], 2*((d[cont_cor-1]-2)/(1-cB[cont_cor-1]))) +math.pow(cC[cont_cor-1], 2*((d[cont_cor-1]-2)/(1-cC[cont_cor-1])))
                resultado.append(soma1/soma2)
                soma1 = 0
                soma2 = 0
                
        self.onr_x = list()
        self.onr_alv_y = list()
        self.mat_meta_onr = list()
        
        x = 0
        for i in range(len(data)):
            self.onr_x.append(i)
            self.onr_alv_y.append(float(data[i][ind-3]))
            self.onr_y.append(resultado[i])

            aux = list()
            aux.append(float(data[i][0]))
            aux.append(float(data[i][1]))
            aux.append(float(data[i][2]))
            aux.append(float(self.onr_y[i]))
            self.mat_meta_onr.append(aux)

            x = i
        self.onr_erro_abs, self.onr_erro_rel = self.calcula_erros(self.onr_y, self.onr_alv_y)
        
    def get_onr(self):
        return self.onr_x, self.onr_y, self.onr_alv_y, self.onr_erro_abs, self.onr_erro_rel, self.mat_meta_onr
 
    def calcula_erros(self, real, aprox):
        t = Treinamento()
        '''
        exato = t.normalizar(real)
        aproximado = t.normalizar(aprox)
        ''' 
        exato = real  
        aproximado = aprox  
        soma_ea = 0
        soma_er = 0
        for i in range(len(exato)):
            ea = abs(exato[i] - aproximado[i])
            er = ea / exato[i]

            soma_ea = soma_ea + ea
            soma_er = soma_er + er
        
        erro_abs = soma_ea / len(exato)
        erro_rela = soma_er / len(exato)

        return erro_abs, erro_rela

class Treinamento:
    def ArvoreDecisao(self, cidade, indic, divisao, cri, spli, max_d, min_s, max_f,  max_l, n_testes, min_sam_spl, min_wei, minim, ccp, save):
        
        tempo_inicial = time.time()
        if indic == 3:
            indicador = 'Precipitação'
        elif indic == 4:
            indicador = 'Temperatura máxima'
        else:
            indicador = 'Temperatura miníma'




        #m_trei, r_trei, m_vali, r_vali = self.prepara_matriz(cidade, divisao, indic, 0)
        m_trei, r_trei, m_vali, r_vali = self.prepara_matriz3(cidade, divisao, indic)
        soma_er_nteste = 0 #* Soma dos erros relativos dos n testes
        soma_ea_nteste = 0 #* Soma dos erros absolutos dos n testes
       
        eixo_y_exato = list()
        eixo_y_predict = list()
        eixo_x = list()
        cont = 1
        cont2 = 1
        for j in range(n_testes):
            aprendiz = tree.DecisionTreeRegressor(criterion=cri, splitter=spli, max_depth=max_d, min_samples_leaf=min_s, max_features=max_f, max_leaf_nodes=max_l, min_samples_split=min_sam_spl, min_weight_fraction_leaf=min_wei, min_impurity_decrease=minim, ccp_alpha=ccp)
            aprendiz = aprendiz.fit(m_trei, r_trei)

            soma_ea = 0 #* Soma dos erros absolutos
            soma_er = 0 #* Soma dos erros relativos

            for i in range(len(m_vali)):
                valor_exato = r_vali[i]
                valor_aprox = aprendiz.predict([m_vali[i]])[0]
                if j != (n_testes):
                    eixo_y_exato.append(valor_exato)
                    eixo_y_predict.append(valor_aprox)
                    eixo_x.append(cont)
                    cont += 1
                
                Erro_absoluto = valor_exato - valor_aprox

                if Erro_absoluto < 0:
                    Erro_absoluto = Erro_absoluto * (-1)
                
                Erro_relativo = (Erro_absoluto/valor_exato)

                soma_ea = soma_ea + Erro_absoluto
                soma_er = soma_er + Erro_relativo
            
            soma_er_nteste = soma_er_nteste + soma_er/len(m_vali)
            soma_ea_nteste = soma_ea_nteste + soma_ea/len(m_vali)
         
            cont2 += 1

        pontuacao = round((((soma_er_nteste/n_testes)*100) - 100)* (-1),2)
        erro = (eixo_y_exato[i] - eixo_y_predict[i])
        if erro < 0:
            erro = erro * (-1)
                

        maior_ea = erro
        exat_maior = eixo_y_exato[0]
        pre_maior = eixo_y_predict[0]

        menor_ea = erro
        exat_menor = eixo_y_exato[0]
        pre_menor = eixo_y_predict[0]

        for i in range(1, len(eixo_x)):
            erro = (eixo_y_exato[i] - eixo_y_predict[i])
            if erro < 0:
                erro = erro * (-1)

            if erro > maior_ea:
                maior_ea = erro
                exat_maior = eixo_y_exato[i]
                pre_maior = eixo_y_predict[i]
            
            if (erro) < menor_ea and (erro) > 0:
                menor_ea = erro
                exat_menor = eixo_y_exato[i]
                pre_menor = eixo_y_predict[i]
        
        media_ea = soma_ea_nteste/n_testes
        media_er = soma_er_nteste/n_testes

        if save == 1:
            pickle.dump(aprendiz, open(r'E:\IC\Interface_Grafica\Dados_verificacao\modelo_ad.sav', 'wb'))

        return pontuacao, media_ea, media_er, maior_ea, exat_maior, pre_maior, menor_ea, exat_menor, pre_menor, eixo_y_exato, eixo_y_predict, eixo_x
          
    def RedeNeural(self, cidade, indic, divisao, n_teste, activ, solv, alp, batc, learnrat, learnratini, powrt, maxiter,shuf, tol_v, verb, warmst, moment, nestr, early, valid, b1, b2, niter, maxf, save):
        tempo_inicial = time.time()
        if indic == 3:
            indicador = 'Precipitação'
        elif indic == 4:
            indicador = 'Temperatura máxima'
        else:
            indicador = 'Temperatura miníma'

            
        
        
        m_trei, r_trei, m_vali, r_vali = self.prepara_matriz3(cidade, divisao, indic)
        soma_er_nteste = 0
        soma_ea_nteste = 0

        eixo_y_exato = list()
        eixo_y_predict = list()
        eixo_x = list()
        cont = 1
        cont2 = 1

        for j in range(n_teste):
            aprendiz = MLPRegressor(activation=activ, solver=solv, alpha=alp, batch_size=batc, learning_rate=learnrat, learning_rate_init=learnratini, power_t=powrt, max_iter=maxiter, shuffle=shuf, tol=tol_v, verbose=verb, warm_start=warmst, momentum=moment, nesterovs_momentum=nestr, early_stopping=early, validation_fraction=valid, beta_1=b1, beta_2=b2,n_iter_no_change=niter,max_fun=maxf)
            aprendiz = aprendiz.fit(m_trei, r_trei)

            soma_ea = 0
            soma_er = 0

            for i in range(len(m_vali)):
                valor_exato = r_vali[i]
                valor_aprox = aprendiz.predict([m_vali[i]])[0]

                if j != (n_teste): #Quando chegar no final, adicionar todos os valores finais em suas respctivas variaveis
                    eixo_y_exato.append(valor_exato)
                    eixo_y_predict.append(valor_aprox)
                    eixo_x.append(cont)
                    cont += 1
            
                Erro_absoluto = abs(valor_exato - valor_aprox)
                Erro_relativo = Erro_absoluto/valor_exato

                soma_ea = soma_ea + Erro_absoluto
                soma_er = soma_er + Erro_relativo

            soma_ea_nteste = soma_ea_nteste + soma_ea/len(m_vali)
            soma_er_nteste = soma_er_nteste + soma_er/len(m_vali)
            
            cont2 += 1
        pontuacao = round((((soma_er_nteste/n_teste)*100) - 100)* (-1),2)
        erro = abs(eixo_y_exato[i] - eixo_y_predict[i])
        

        maior_ea = erro
        exat_maior = eixo_y_exato[0]
        pre_maior = eixo_y_predict[0]

        menor_ea = erro
        exat_menor = eixo_y_exato[0]
        pre_menor = eixo_y_predict[0]

        for i in range(1, len(eixo_x)):
            erro = (eixo_y_exato[i] - eixo_y_predict[i])
            if erro < 0:
                erro = erro * (-1)

            if erro > maior_ea:
                maior_ea = erro
                exat_maior = eixo_y_exato[i]
                pre_maior = eixo_y_predict[i]
                
            if (erro) < menor_ea and (erro) > 0:
                menor_ea = erro
                exat_menor = eixo_y_exato[i]
                pre_menor = eixo_y_predict[i]
            
        media_ea = soma_ea_nteste/n_teste
        media_er = soma_er_nteste/n_teste

        if save == 1:
            pickle.dump(aprendiz, open(r'E:\IC\Interface_Grafica\Dados_verificacao\modelo_rn.sav', 'wb'))

        
        return pontuacao, media_ea, media_er, maior_ea, exat_maior, pre_maior, menor_ea, exat_menor, pre_menor, eixo_y_exato, eixo_y_predict, eixo_x
            
    def KNeighbors(self, cidade, indic, divisao, n_teste, n_nei, algor, leaf_s, p_val, n_jo, save):
            m_trei, r_trei, m_vali, r_vali = self.prepara_matriz3(cidade, divisao, indic)
            soma_er_nteste = 0
            soma_ea_nteste = 0

            eixo_y_exato = list()
            eixo_y_predict = list()
            eixo_x = list()
            cont = 1
            cont2 = 1

            if indic == 3:
                indicador = 'Precipitação'
            elif indic == 4:
                indicador = 'Temperatura máxima'
            else:
                indicador = 'Temperatura miníma'

            
            for j in range(n_teste):
                aprendiz = KNeighborsRegressor(n_neighbors=n_nei, algorithm=algor, leaf_size=leaf_s, p=p_val, n_jobs=n_jo)
                aprendiz = aprendiz.fit(m_trei, r_trei)

                soma_ea = 0
                soma_er = 0

                for i in range(len(m_vali)):
                    valor_exato = r_vali[i]
                    valor_aprox = aprendiz.predict([m_vali[i]])[0]

                    if j != (n_teste): #Quando chegar no final, adicionar todos os valores finais em suas respctivas variaveis
                        eixo_y_exato.append(valor_exato)
                        eixo_y_predict.append(valor_aprox)
                        eixo_x.append(cont)
                        cont += 1
                
                    Erro_absoluto = abs(valor_exato - valor_aprox)
                    Erro_relativo = Erro_absoluto/valor_exato

                    soma_ea = soma_ea + Erro_absoluto
                    soma_er = soma_er + Erro_relativo

                soma_ea_nteste = soma_ea_nteste + soma_ea/len(m_vali)
                soma_er_nteste = soma_er_nteste + soma_er/len(m_vali)

                cont2 += 1

            pontuacao = round((((soma_er_nteste/n_teste)*100) - 100)* (-1),2)
            erro = abs(eixo_y_exato[i] - eixo_y_predict[i])
            

            maior_ea = erro
            exat_maior = eixo_y_exato[0]
            pre_maior = eixo_y_predict[0]

            menor_ea = erro
            exat_menor = eixo_y_exato[0]
            pre_menor = eixo_y_predict[0]

            for i in range(1, len(eixo_x)):
                erro = (eixo_y_exato[i] - eixo_y_predict[i])
                if erro < 0:
                    erro = erro * (-1)

                if erro > maior_ea:
                    maior_ea = erro
                    exat_maior = eixo_y_exato[i]
                    pre_maior = eixo_y_predict[i]
                    
                if (erro) < menor_ea and (erro) > 0:
                    menor_ea = erro
                    exat_menor = eixo_y_exato[i]
                    pre_menor = eixo_y_predict[i]
                
            media_ea = soma_ea_nteste/n_teste
            media_er = soma_er_nteste/n_teste

            if save == 1:
                pickle.dump(aprendiz, open(r'E:\IC\Interface_Grafica\Dados_verificacao\modelo_kn.sav', 'wb'))

            
            return pontuacao, media_ea, media_er, maior_ea, exat_maior, pre_maior, menor_ea, exat_menor, pre_menor, eixo_y_exato, eixo_y_predict, eixo_x

    def SVR(self, cidade, indic, divisao, n_teste, ker, degr, gam, coe, t, c, eps, shr, cache, verb, maxi, save):
                m_trei, r_trei, m_vali, r_vali = self.prepara_matriz3(cidade, divisao, indic)
                soma_er_nteste = 0
                soma_ea_nteste = 0

                eixo_y_exato = list()
                eixo_y_predict = list()
                eixo_x = list()
                cont = 1
                cont2 = 1

                if indic == 3:
                    indicador = 'Precipitação'
                elif indic == 4:
                    indicador = 'Temperatura máxima'
                else:
                    indicador = 'Temperatura miníma'
            


                for j in range(n_teste):
                    aprendiz = SVR(kernel=ker, degree=degr, gamma=gam, coef0=coe, tol=t, C=c, epsilon=eps, shrinking=shr, cache_size=cache, verbose=verb, max_iter=maxi)
                    aprendiz = aprendiz.fit(m_trei, r_trei)

                    soma_ea = 0
                    soma_er = 0

                    for i in range(len(m_vali)):
                        valor_exato = r_vali[i]
                        valor_aprox = aprendiz.predict([m_vali[i]])[0]

                        if j != (n_teste): #Quando chegar no final, adicionar todos os valores finais em suas respctivas variaveis
                            eixo_y_exato.append(valor_exato)
                            eixo_y_predict.append(valor_aprox)
                            eixo_x.append(cont)
                            cont += 1
                    
                        Erro_absoluto = abs(valor_exato - valor_aprox)
                        Erro_relativo = Erro_absoluto/valor_exato

                        soma_ea = soma_ea + Erro_absoluto
                        soma_er = soma_er + Erro_relativo

                    soma_ea_nteste = soma_ea_nteste + soma_ea/len(m_vali)
                    soma_er_nteste = soma_er_nteste + soma_er/len(m_vali)

                    cont2 += 1

                pontuacao = round((((soma_er_nteste/n_teste)*100) - 100)* (-1),2)
                erro = abs(eixo_y_exato[i] - eixo_y_predict[i])
                

                maior_ea = erro
                exat_maior = eixo_y_exato[0]
                pre_maior = eixo_y_predict[0]

                menor_ea = erro
                exat_menor = eixo_y_exato[0]
                pre_menor = eixo_y_predict[0]

                for i in range(1, len(eixo_x)):
                    erro = (eixo_y_exato[i] - eixo_y_predict[i])
                    if erro < 0:
                        erro = erro * (-1)

                    if erro > maior_ea:
                        maior_ea = erro
                        exat_maior = eixo_y_exato[i]
                        pre_maior = eixo_y_predict[i]
                        
                    if (erro) < menor_ea and (erro) > 0:
                        menor_ea = erro
                        exat_menor = eixo_y_exato[i]
                        pre_menor = eixo_y_predict[i]
                    
                media_ea = soma_ea_nteste/n_teste
                media_er = soma_er_nteste/n_teste

                if save == 1:
                    pickle.dump(aprendiz, open(r'E:\IC\Interface_Grafica\Dados_verificacao\modelo_svr.sav', 'wb'))
                
                return pontuacao, media_ea, media_er, maior_ea, exat_maior, pre_maior, menor_ea, exat_menor, pre_menor, eixo_y_exato, eixo_y_predict, eixo_x

    def prepara_matriz(self, local, divi, indicador, qtd_in):
        norm = Tratamento()

        matriz = list()
        aux1 = list()
        resultado = list()
        arq = open(local)
        for i in arq:
            buff = list()
            i = i.strip()
            i = i.replace("'",'')
            i = i.replace(" ",'')
            i = i.split(',') 
            buff.append(int(i[2])) #dia
            buff.append(int(i[1])) #mes
            buff.append(int(i[0])) #ano
            buff.append(float(i[indicador])) #Indicador selecionado pelo usuário
            aux1.append(buff)
        mat_n = norm.normalizar_dados(aux1)


        buff.clear()
        
        for i in range(len(mat_n)):
            buff = list()
            try:
                for j in range(5):
                    buff.append(mat_n[i+j][0])
                    buff.append(mat_n[i+j][1])
                    buff.append(mat_n[i+j][2])
                    buff.append(mat_n[i+j][3])
                if len(buff) == 20:
                    matriz.append(buff[:19])
                    resultado.append(buff[19])
            except IndexError:
                pass
        arq.close()
        tam = floor(len(matriz)*(divi/100))
        matriz_treinamento = list()
        resultado_treinamento = list()
        matriz_validacao = list()
        resultado_validacao = list()

        for i in range(len(matriz)):
            if i <= tam:
                matriz_treinamento.append(matriz[i])
                resultado_treinamento.append(resultado[i])
            else:
                matriz_validacao.append(matriz[i])
                resultado_validacao.append(resultado[i])
        mat_trein_n = list()
        res_tre_n = list()
        mat_val_n = list()
        res_val_n = list()
        '''if indicador == 3:
            mat_trein_n = norm.normalizar_dados(matriz_treinamento)
            res_tre_n = norm.normalizar_dados(resultado_treinamento)
            mat_val_n = norm.normalizar_dados(matriz_validacao)
            res_val_n = norm.normalizar_dados(resultado_validacao)
            return mat_trein_n, res_tre_n, mat_val_n, res_val_n
        else:'''
        return matriz_treinamento, resultado_treinamento, matriz_validacao, resultado_validacao 

    def prepara_matriz3(self, cidade, divi, indicador):
        matriz = list()
        aux1 = list()
        resultado = list()

        
        if cidade == 'Cidade alvo':
            foco = indicador
        elif cidade == 'Vizinha A':
            foco = 3 + indicador
        elif cidade == 'Vizinha B':
            foco = 6 + indicador
        else:
            foco = 9 + indicador
        t = Tratamento()
        data = t.retorna_arq('Dados comum')
        for i in range(len(data)):
            buff = list()
            buff.append(int(data[i][0]))
            buff.append(int(data[i][1]))
            buff.append(int(data[i][2]))
            buff.append(float(data[i][foco]))
            aux1.append(buff)
        
        mat_n = t.normalizar_dados(aux1)
        buff.clear()

        for i in range(len(mat_n)):
            buff = list()
            try:
                for j in range(5):
                    buff.append(mat_n[i+j][0])
                    buff.append(mat_n[i+j][1])
                    buff.append(mat_n[i+j][2])
                    buff.append(mat_n[i+j][3])
                if len(buff) == 20:
                    matriz.append(buff[:19])
                    resultado.append(buff[19])
            except IndexError:
                pass
        tam = floor(len(matriz)*(divi/100))
        matriz_treinamento = list()
        resultado_treinamento = list()
        matriz_validacao = list()
        resultado_validacao = list()

        for i in range(len(matriz)):
            if i <= tam:
                matriz_treinamento.append(matriz[i])
                resultado_treinamento.append(resultado[i])
            else:
                matriz_validacao.append(matriz[i])
                resultado_validacao.append(resultado[i])   
        return matriz_treinamento, resultado_treinamento, matriz_validacao, resultado_validacao 

    def prepara_matriz2(self, local, divisao, indicadores, foco, normalizar): #Indicadores estão em forma de lista (no max 2 de 3) [3(chuva) e/ou 4(tmax) e/ou 5(tmin)]  || O foco vai ser qual indicador que o usuario quer que as máquinas façam o predict

        matriz = list()
        resultado = list()
        arq = open(local)

        for i in arq:
            buff = list()
            i = i.strip()
            i = i.replace("'",'')
            i = i.replace(" ",'')
            i = i.split(',') 
            buff.append(int(i[2])) #dia
            buff.append(int(i[1])) #mes
            buff.append(int(i[0])) #ano
            if indicadores != []:
                for j in indicadores:
                    buff.append(float(i[j]))
            resultado.append(float(i[foco]))
            matriz.append(buff) 
        arq.close()

        tam = floor(len(matriz)*(divisao/100))
        matriz_treinamento = list()
        resultado_treinamento = list()
        matriz_validacao = list()
        resultado_validacao = list()

        if normalizar == 1:
            resultado_n = self.normalizar(resultado)
            matriz_n = self.normalizar(matriz)

            for i in range(len(matriz)):
                if i <= tam:
                    matriz_treinamento.append(matriz_n[i])
                    resultado_treinamento.append(resultado_n[i])
                else:
                    matriz_validacao.append(matriz_n[i])
                    resultado_validacao.append(resultado_n[i])
        else:
            for i in range(len(matriz)):
                if i <= tam:
                    matriz_treinamento.append(matriz[i])
                    resultado_treinamento.append(resultado[i])
                else:
                    matriz_validacao.append(matriz_n[i])
                    resultado_validacao.append(resultado[i])

        return matriz_treinamento, resultado_treinamento, matriz_validacao, resultado_validacao 

            

    def normalizar(self, data):

        try: #Se for uma matriz (mais de uma coluna)
            max_min = list()  #Lista de max e min de cada coluna
            aux = list()
            t = len(data[0])  #Obter a quantidade de colunas da "matriz"

            for i in range(t): #Um laço começa pelas colunas e vai percorrendo as linhas
                aux.clear()
                for j in range(len(data)):
                    aux.append(float(data[j][i]))
                max_min.append(max(aux))  #Coloca o max e depois o min de cada columa
                max_min.append(min(aux))

            dadosn = list()

            for i in range(len(data)):
                cont = 0
                buff = list()
                for j in range(t):
                    maior = max_min[cont]
                    menor = max_min[cont + 1]
                    dado = ((float(data[i][j]) - float(menor)) / (float(maior) - float(menor))) * 0.6 + 0.2
                    buff.append(dado)
                    cont = cont + 2
                dadosn.append(buff)

            
                     
        except TypeError: #Se for so um vetor (uma so coluna/linha)
            dadosn = list()
            maior = max(data)
            menor = min(data)
            for i in range(len(data)):
                dado = ((float(data[i]) - float(menor)) / (float(maior) - float(menor))) * 0.6 + 0.2
                dadosn.append(dado)

        return dadosn

class MetaL:
    def prepara_input(self, indicador, janela):
        if indicador == 1:
            foco = 3
        elif indicador == 2:
            foco = 4
        else: 
            foco = 5

        trat = Tratamento()
        dt = trat.retorna_arq('Dados comum')

        mat = list()
        for i in range(len(dt)): #Vai fazer uma matriz com ano mes dia foco
            aux = list()
            aux.append(float(dt[i][0]))
            aux.append(float(dt[i][1]))
            aux.append(float(dt[i][2]))
            aux.append(float(dt[i][foco]))
            mat.append(aux)

        norma = Treinamento()
        mat_n = norma.normalizar(mat) #Vai normalizar os dados de cada coluna e de cada linha
        if janela == 'Sim':
            matriz_t, matriz_r = self.janela_deslizante(mat_n) #Vai fazer as matrizes para o input no formato de janela deslizante
        else:
            matriz_t, matriz_r = self.input_comum(mat_n)
        m1_40_t = list()
        m1_40_r = list()
        m2_40_t = list() #Para o aprediz lv0 fazer os predicts, que serão um dos inputs do meta
        m2_40_r = list()
        m3_20_t = list()
        m3_20_r = list()

        tamanho = len(matriz_t)
        t1 = floor(tamanho * 0.4)
        t2 = t1 * 2

        for i in range(tamanho): #Vai separa as porções de dados
            if i <= t1:
                m1_40_t.append(matriz_t[i])
                m1_40_r.append(matriz_r[i])
            elif i > t1 and i <=t2:
                m2_40_t.append(matriz_t[i])
                m2_40_r.append(matriz_r[i])
            else:
                m3_20_t.append(matriz_t[i])
                m3_20_r.append(matriz_r[i])
        
        return m1_40_t, m1_40_r, m2_40_t, m2_40_r, m3_20_t, m3_20_r
         
    def janela_deslizante(self, data):
        matriz = list()
        resultado = list()
        buff = list()
        for i in range(len(data)):
            buff = list()
            try:
                for j in range(5):
                    buff.append(data[i+j][0])
                    buff.append(data[i+j][1])
                    buff.append(data[i+j][2])
                    buff.append(data[i+j][3])
                if len(buff) == 20:
                    matriz.append(buff[:19])
                    resultado.append(buff[19])
            except IndexError:
                pass
        return matriz, resultado

    def input_comum(self, data):
        matriz = list()
        resultado = list()
        
        for i in range(len(data)):
            buff = list()
            buff.append(data[i][0])
            buff.append(data[i][1])
            buff.append(data[i][2])
            matriz.append(buff)

            resultado.append(data[i][3])

        return matriz, resultado
    
    def base_learn(self, mach, pre, n_test, mat_in_tr, mat_res_tr, mat_in_valid, mat_res_valid, mat_in_p2, mat_res_p2, janela):
        if pre == 0:
            if mach == 'Decision Trees':
                aprendiz_lv0 = tree.DecisionTreeRegressor()
            elif mach == 'Neural network':
                aprendiz_lv0 = MLPRegressor()
            elif mach == 'Nearest Neighbors':
                aprendiz_lv0 = KNeighborsRegressor()
            elif mach == 'Support Vector':
                aprendiz_lv0 = SVR()

        soma_er_nteste = 0
        soma_ea_nteste = 0
        
        soma_r2 = 0
        for i in range(n_test):
            aprendiz_lv0 = aprendiz_lv0.fit(mat_in_tr, mat_res_tr)
            soma_ea = 0
            soma_er = 0
            soma_r2 = soma_r2 + aprendiz_lv0.score(mat_in_valid, mat_res_valid)
            for j in range(len(mat_in_valid)):
                valor_ex = float(mat_res_valid[j])
                valor_aprox = float(aprendiz_lv0.predict([(mat_in_valid[j])])[0])
                Erro_abs = abs(valor_ex - valor_aprox)
                Erro_rel = Erro_abs / valor_ex

                soma_ea = soma_ea + Erro_abs
                soma_er = soma_er + Erro_rel
            
            soma_ea_nteste = soma_ea_nteste + soma_ea/len(mat_in_valid)
            soma_er_nteste = soma_er_nteste + soma_er/len(mat_in_valid)

        media_ea = soma_ea_nteste / n_test
        media_er = soma_er_nteste / n_test
        porc_erro = media_ea * 100
        r2 = soma_r2 / n_test

        #Preparando os dados do aprendiz lv0 para o aprendiz lv1
        mat_p2 = list()
        if janela == 'Sim':        
            for i in range(len(mat_in_p2)):
                aux = list()
                valor = float(aprendiz_lv0.predict([(mat_in_p2[i])])[0])
                aux.append(mat_in_p2[i][16])
                aux.append(mat_in_p2[i][17])
                aux.append(mat_in_p2[i][18])
                aux.append(valor)
                mat_p2.append(aux)
        else:
            for i in range(len(mat_in_p2)):
                aux = list()
                valor = float(aprendiz_lv0.predict([(mat_in_p2[i])])[0])
                aux.append(mat_in_p2[i][0])
                aux.append(mat_in_p2[i][1])
                aux.append(mat_in_p2[i][2])
                aux.append(valor)
                mat_p2.append(aux)
        return mat_p2, media_ea, media_er, porc_erro, r2


    def triangula(self, metodo, foco):
        t = Triangulaction()
        nor = Treinamento()
        if metodo == 'Inverse Distance Weighted':
            t.idw(foco)
            matriz_triang = nor.normalizar(t.get_idw()[5])
            x,y,alv_y, erro_abs, erro_rel, mat_ext = t.get_idw()
            erro_abs, erro_rel = self.calcula_erro_tri(alv_y, y)
        elif metodo == 'Arithmetic Average':
            t.aa(foco)
            matriz_triang = nor.normalizar(t.get_aa()[5])
            x,y,alv_y, erro_abs, erro_rel, mat_ext = t.get_aa()
            erro_abs, erro_rel = self.calcula_erro_tri(alv_y, y)
        elif metodo == 'Regional Weight':
            t.rw(foco)
            matriz_triang = nor.normalizar(t.get_rw()[5])
            x,y,alv_y, erro_abs, erro_rel, mat_ext = t.get_rw()
            erro_abs, erro_rel = self.calcula_erro_tri(alv_y, y)
        elif metodo == 'Optimized Normal Ratio':
            t.onr(foco)
            matriz_triang = nor.normalizar(t.get_onr()[5])
            x,y,alv_y, erro_abs, erro_rel, mat_ext = t.get_onr()
            erro_abs, erro_rel = self.calcula_erro_tri(alv_y, y)

        tamanho = len(matriz_triang)
        t1 = floor(tamanho * 0.4)
        t2 = t1 * 2

        matriz_final_data = list()
        matriz_final_dado = list()
        
        for i in range(len(matriz_triang)):
            if i > t1 and i <= t2:
                aux = list()
                aux.append(matriz_triang[i][0])
                aux.append(matriz_triang[i][1])
                aux.append(matriz_triang[i][2])
                matriz_final_data.append(aux)
                matriz_final_dado.append(matriz_triang[i][3])
                

        return matriz_final_data, matriz_final_dado, erro_abs, erro_rel
        
        
    def calcula_erro_tri(self, x, y):
        t = Treinamento()
        mat1 = t.normalizar(x)
        mat2 = t.normalizar(y)
        
        soma_ea = 0
        soma_er = 0
        for i in range(len(mat1)):
            ea = abs(float(mat1[i]) - float(mat2[i]))
            er = ea / float(mat1[i])

            soma_ea = soma_ea + ea
            soma_er = soma_er + er

        ea = soma_ea / len(mat1)
        er = soma_er / len(mat2)
        return ea, er


    def meta_learning_personalizado(self, indicador, base_l, metodo_tri, meta_l, pre1, pre2, n_test, janela):
        m1_40_t, m1_40_r, m2_40_t, m2_40_r, m3_20_t, m3_20_r = self.prepara_input(indicador, janela)
        if base_l != 'Nenhum':
            matriz_input, base_ea, base_er, base_porc, base_r2 = self.base_learn(base_l, 0, n_test, m1_40_t, m1_40_r, m3_20_t, m3_20_r, m2_40_t, m2_40_r, janela)
            del matriz_input[:2]
        if metodo_tri != 'Nenhum':
            seila, matriz_trian, tria_ea, tria_er = self.triangula(metodo_tri, indicador)
            
            del matriz_trian[:4]
        
        matriz_datas, a, b, c = self.triangula('Arithmetic Average', indicador)
        del matriz_datas[:4]
        
        
        del m2_40_r[:2]
        
        matriz_f = list()
        result_f = list()
        for i in range(len(matriz_datas)):
            aux = list()
            if base_l == 'Nenhum' :
                aux.append(matriz_datas[i][0])
                aux.append(matriz_datas[i][1])
                aux.append(matriz_datas[i][2])
                aux.append(matriz_trian[i])
            elif metodo_tri == 'Nenhum':
                aux.append(matriz_datas[i][0])
                aux.append(matriz_datas[i][1])
                aux.append(matriz_datas[i][2])
                aux.append(matriz_input[i][3])
            else:
                aux.append(matriz_datas[i][0])
                aux.append(matriz_datas[i][1])
                aux.append(matriz_datas[i][2])
                aux.append(matriz_trian[i])
                aux.append(matriz_input[i][3])
            matriz_f.append(aux)

        if pre2 == 0:
            if meta_l == 'Decision Trees':
                aprendiz_lv1 = tree.DecisionTreeRegressor()
            elif meta_l == 'Neural network':
                aprendiz_lv1 = MLPRegressor()
            elif meta_l == 'Nearest Neighbors':
                aprendiz_lv1 = KNeighborsRegressor()
            elif meta_l == 'Support Vector':
                aprendiz_lv1 = SVR()

        
        t = len(matriz_f)
        divi = t - floor(t*0.2)
        x_apre = list()
        y_apre = list()

        x_test = list()
        y_test = list()
        
        for i in range(t):
            if i <= divi:
                x_apre.append(matriz_f[i])
                y_apre.append(m2_40_r[i])
            else:
                x_test.append(matriz_f[i])
                y_test.append(m2_40_r[i])
        soma = 0
        soma_er_nteste = 0
        soma_ea_nteste = 0
        x_meta = list()
        y_meta = list()
        y_alvo = list()

        x = 0
        for i in range(n_test):
            aprendiz_lv1 = aprendiz_lv1.fit(x_apre, y_apre)
            val = aprendiz_lv1.score(x_test, y_test)
            soma = soma + val #Calcular o R2

            soma_ea = 0
            soma_er = 0
            for j in range(len(x_test)):
                valor_ex = float(y_test[j])
                valor_aprox = float(aprendiz_lv1.predict([(x_test[j])])[0])

                y_meta.append(valor_aprox)
                y_alvo.append(valor_ex)
                x_meta.append(x)
                x += 1

                Erro_abs = abs(valor_ex - valor_aprox)
                Erro_rel = Erro_abs / valor_ex

                soma_ea = soma_ea + Erro_abs
                soma_er = soma_er + Erro_rel
            
            soma_ea_nteste = soma_ea_nteste + soma_ea/len(x_test)
            soma_er_nteste = soma_er_nteste + soma_er/len(x_test)
        meta_ea = soma_ea_nteste / n_test
        meta_er = soma_er_nteste / n_test
        meta_porc_erro = meta_ea * 100
        meta_r2 = soma / n_test
        
        if base_l == 'Nenhum':
            return meta_ea, meta_er, meta_porc_erro, meta_r2, x_meta, y_meta, y_alvo, 0, 0, 0, 0, tria_ea, tria_er
        elif metodo_tri == 'Nenhum':
            return meta_ea, meta_er, meta_porc_erro, meta_r2, x_meta, y_meta, y_alvo, base_ea, base_er, base_porc, base_r2, 0, 0
        else:
            return meta_ea, meta_er, meta_porc_erro, meta_r2, x_meta, y_meta, y_alvo, base_ea, base_er, base_porc, base_r2, tria_ea, tria_er
    
    def meta_learning_combina(self,  foco, pre1, pre2, n_test, janela):
        machine_l = ['Nenhum','Decision Trees', 'Neural network', 'Nearest Neighbors', 'Support Vector']
        triangulacao = ['Nenhum', 'Arithmetic Average', 'Inverse Distance Weighted', 'Regional Weight', 'Optimized Normal Ratio']
        meta_l = ['Decision Trees', 'Neural network', 'Nearest Neighbors', 'Support Vector']
        
        todos_mod = list()
        ranking_mod = list()

        if foco == 'Precipitação':
            indicador = 1
        elif foco == 'Temperatura máxima':
            indicador = 2
        else:
             indicador = 3

        m1_40_t, m1_40_r, m2_40_t, m2_40_r, m3_20_t, m3_20_r = self.prepara_input(indicador, janela)

        arq = open('meta_comb.txt', 'w')
        arq2 = open('meta_res.csv', 'w')
        arq3 = open('meta_best_results.csv', 'w')

        arq2.write("Modelo;Machine Learning;Triangulação;Meta Learning;Erro Absoluto;Erro Relativo;Erro(%);R2;\n")
        arq3.write("Modelo;Erro(%);\n")
        Modelos = dict()
        cont_model = 1
        teste = repr("Modelo").center(8) + ' || ' + repr('Base-Learning').center(30) + ' || ' +  repr('Triangulation').center(30) + ' || ' + repr('Meta-Learning').center(30) + ' || ' +  repr("Erro(%)").center(20)
        
        for i in range(len(machine_l)):
            for j in range(len(triangulacao)):
                for k in range(len(meta_l)):
                    if machine_l[i] == 'Nenhum' and triangulacao[j] == 'Nenhum':
                        k += 1
                    else:
                        if machine_l[i] != 'Nenhum':
                            matriz_input, base_ea, base_er, base_porc, base_r2 = self.base_learn(machine_l[i], 0, n_test, m1_40_t, m1_40_r, m3_20_t, m3_20_r, m2_40_t, m2_40_r, janela)
                            del matriz_input[:2]
                        if triangulacao[j] != 'Nenhum':
                            seila, matriz_trian, tria_ea, tria_er = self.triangula(triangulacao[j], indicador)
                            del matriz_trian[:4]
                        
                        matriz_datas, a, b, c = self.triangula('Arithmetic Average', indicador)
                        del matriz_datas[:4]
                        del m2_40_r[:2]

                        matriz_f = list()
                        result_f = list()
                        for l in range(len(matriz_datas)):
                            aux = list()
                            if machine_l[i] == 'Nenhum' and triangulacao[j] != 'Nenhum':
                                aux.append(matriz_datas[l][0])
                                aux.append(matriz_datas[l][1])
                                aux.append(matriz_datas[l][2])
                                aux.append(matriz_trian[l])
                            if triangulacao[j] == 'Nenhum' and machine_l[i] != 'Nenhum':
                                aux.append(matriz_datas[l][0])
                                aux.append(matriz_datas[l][1])
                                aux.append(matriz_datas[l][2])
                                aux.append(matriz_input[l][3])
                            if triangulacao[j] != 'Nenhum' and machine_l[i] != 'Nenhum':
                                aux.append(matriz_datas[l][0])
                                aux.append(matriz_datas[l][1])
                                aux.append(matriz_datas[l][2])
                                aux.append(matriz_trian[l])
                                aux.append(matriz_input[l][3])
                            matriz_f.append(aux)
                        os.system('cls')
                        print("{} ---".format(matriz_f[0]))
                        if pre2 == 0:
                            if meta_l[k] == 'Decision Trees':
                                aprendiz_lv1 = tree.DecisionTreeRegressor()
                            elif meta_l[k] == 'Neural network':
                                aprendiz_lv1 = MLPRegressor()
                            elif meta_l[k] == 'Nearest Neighbors':
                                aprendiz_lv1 = KNeighborsRegressor()
                            elif meta_l[k] == 'Support Vector':
                                aprendiz_lv1 = SVR()

                        
                        t = len(m2_40_r)
                        divi = t - floor(t*0.2)
                        x_apre = list()
                        y_apre = list()

                        x_test = list()
                        y_test = list()
                        
                        for n in range(t):
                            try:
                                if n <= divi:
                                    x_apre.append(matriz_f[n])
                                    y_apre.append(m2_40_r[n])
                                else:
                                    x_test.append(matriz_f[n])
                                    y_test.append(m2_40_r[n])
                            except IndexError:
                                pass
                        soma = 0
                        soma_er_nteste = 0
                        soma_ea_nteste = 0
                        x_meta = list()
                        y_meta = list()
                        y_alvo = list()

                        x = 0
                        for l in range(n_test):
                            aprendiz_lv1 = aprendiz_lv1.fit(x_apre, y_apre)
                            val = aprendiz_lv1.score(x_test, y_test)
                            soma = soma + val #Calcular o R2

                            soma_ea = 0
                            soma_er = 0
                            for m in range(len(x_test)):
                                valor_ex = float(y_test[m])
                                valor_aprox = float(aprendiz_lv1.predict([(x_test[m])])[0])

                                y_meta.append(valor_aprox)
                                y_alvo.append(valor_ex)
                                x_meta.append(x)
                                x += 1

                                Erro_abs = abs(valor_ex - valor_aprox)
                                Erro_rel = Erro_abs / valor_ex

                                soma_ea = soma_ea + Erro_abs
                                soma_er = soma_er + Erro_rel
                            
                            soma_ea_nteste = soma_ea_nteste + soma_ea/len(x_test)
                            soma_er_nteste = soma_er_nteste + soma_er/len(x_test)
                        meta_ea = soma_ea_nteste / n_test
                        meta_er = soma_er_nteste / n_test
                        meta_porc_erro = meta_ea * 100
                        meta_r2 = soma / n_test

                        texto = str(cont_model) + " -> Machine Learning: " + machine_l[i] + "  ||  Triangulação: " + triangulacao[j] + "  || Meta Learning: " + meta_l[k] + "  |Resultados para " + str(n_test)+ " testes| --> Erro Absoluto: " + str(meta_ea) + "  |  Erro Relativo: " + str(meta_er) + "  |  Erro(%): " + str(meta_porc_erro) + "  |  R2: " + str(meta_r2)
                        arq.write(texto + "\n")
                        
                        teste = repr(cont_model).center(8) + ' || ' + repr(machine_l[i]).center(30) + ' || ' + repr(triangulacao[j]).center(30) + ' || ' + repr(meta_l[k]).center(30) + ' || ' + repr(meta_porc_erro).center(20)
                        #print(teste)
                        
                        
                        texto = str(cont_model) + ";" + machine_l[i] + ";" + triangulacao[j] + ";" + meta_l[k] + ";" + str(meta_ea).replace('.', ',') + ";" + str(meta_er).replace('.', ',') + ";" + str(meta_porc_erro).replace('.', ',') + ";" + str(meta_r2).replace('.', ',') + ";"   
                        arq2.write(texto + "\n")

                        Modelos[str(cont_model)] = meta_porc_erro
                        

                        aux = list()
                        aux.append(cont_model)      #0
                        aux.append(machine_l[i])    #1
                        aux.append(triangulacao[j]) #2
                        aux.append(meta_l[k])       #3
                        aux.append(n_test)          #4
                        aux.append(round(meta_ea, 4)) #5
                        aux.append(round(meta_er, 4)) #6
                        aux.append(round(meta_porc_erro, 4)) #7
                        aux.append(round(meta_r2, 4)) #8
                        todos_mod.append(aux)

                        cont_model += 1
        for z in sorted(Modelos, key=Modelos.get):
            arq3.write(str(z) + ";" + str(Modelos[z]).replace('.', ',') + ";\n")
            aux = list()
            aux.append(str(z))
            aux.append(str(Modelos[z]).replace('.', ','))
            ranking_mod.append(aux)             
        arq.close()
        arq2.close()
        arq3.close()

        return todos_mod, ranking_mod

    def valid_maxf(self, val):
        if val.isdigit() == True:
            val = int(val)
        elif val.isalnum() == True and val.isdigit() == False:
            val = str(val)
        elif val.isalnum() == False and val.isdigit() == False and val.isalpha() == False:
            val = float(val)
        
        return val

    def salvar_paramt(self):
        img = pyscreenshot.grab(bbox=(0,25,1920,1040))
        img.show()
        img.save(r'C:\Users\pablo\Desktop\teste.png')

    def data_prev(self, pts, media_ea, media_er, maior_ea, exat_maior, pre_maior, menor_ea, exat_menor, pre_menor, eixo_y_exato, eixo_y_predict, eixo_x):
        self.laf_res = LabelFrame(self, text='Preview dos resultados', width=1250, height=950, font='Arial 12 bold', fg='white', bg=fundo).place(x=650, y=50)
        Label(self, text='Pontuação (0-100): '+ str(pts) +'pts', font='Arial 12 bold', fg='white', bg=fundo).place(x=680, y=70)
        media_ea = round(media_ea, 4)
        Label(self, text='Média Erro absoluto: '+ str(media_ea), font='Arial 12 bold', fg='white', bg=fundo).place(x=680, y=100)
        media_er = round(media_er, 4)
        Label(self, text='Média Erro relativo: '+ str(media_er), font='Arial 12 bold', fg='white', bg=fundo).place(x=680, y=130)

        Label(self, text='Maior erro absoluto: ' + str(round(maior_ea,4)), font='Arial 12 bold', fg='white', bg=fundo).place(x=680, y=160)
        Label(self, text="Valor exato do maior EA: " + str(round(exat_maior,4)),font='Arial 12 bold', fg='white', bg=fundo).place(x=940, y=160)
        Label(self, text="Predict do maior EA: " + str(round(pre_maior, 4)), font='Arial 12 bold', fg='white', bg=fundo).place(x=1200, y=160)

        Label(self, text='Menor erro absoluto: ' + str(round(menor_ea,4)), font='Arial 12 bold', fg='white', bg=fundo).place(x=680, y=190)
        Label(self, text="Valor exato do menor EA: " + str(round(exat_menor,4)),font='Arial 12 bold', fg='white', bg=fundo).place(x=940, y=190)
        Label(self, text="Predict do menor EA: " + str(round(pre_menor, 4)), font='Arial 12 bold', fg='white', bg=fundo).place(x=1200, y=190)

        figura = Figure(figsize=(12,7.3), dpi=100)
        plot_r = figura.add_subplot(111)
        plot_r.plot(eixo_x, eixo_y_exato,label='Exato', color='green')
        plot_r.plot(eixo_x, eixo_y_predict, label='Predict', color='red')
        plot_r.legend()
        plot_r.grid(True)
        plot_r.set_ylabel("Temperatura(°C)")
        plot_r.set_xlabel("Comparações")

        canvas = FigureCanvasTkAgg(figura, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack()
        canvas.get_tk_widget().place(x=680, y=240)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.place(x=1150, y=10)
        toolbar.update()
    
    def get_end(self, cidade):
        Trat = Tratamento()
        return Trat.retorna_end(cidade)

    def gerar_preview_dt(self):
        prev = Treinamento()
        salvar_m = self.save_model.get()
        


        #cidade = self.get_end(self.data_s.get())
        cidade = self.data_s.get()
        indicador = self.ind_s.get()
        divisao = int(self.por_trei.get())
        criterio = self.criterion_v.get()
        splitter = self.splitter_v.get()
        maxd = int(self.maxd_v.get())             #* Max_depth
        minsams = self.int_float(self.minsam_s_v.get())    #* Min_samples_split
        minsaml = self.int_float(self.minsam_l_v.get())    #* Min_samples_leaf
        minwei = float(self.minweifra_l_v.get())
        maxfe = self.valid_maxf(self.maxfeat_v.get())
        maxleaf = int(self.maxleaf_n.get())
        
        minim = float(self.minimp_dec.get())
        ccp = float(self.ccp_alp_v.get())
        n_tes = int(self.num_teste.get())

        if indicador == 'Precipitação':
            indicador = 3
        elif indicador == 'Temperatura máxima':
            indicador = 4
        elif indicador == 'Temperatura mínima':
            indicador = 5

        pts, media_ea, media_er, maior_ea, exat_maior, pre_maior, menor_ea, exat_menor, pre_menor, eixo_y_exato, eixo_y_predict, eixo_x = prev.ArvoreDecisao(cidade, indicador, divisao, criterio, splitter, maxd, minsaml, maxfe, maxleaf, n_tes, minsams, minwei, minim, ccp, salvar_m)
        self.data_prev(pts, media_ea, media_er, maior_ea, exat_maior, pre_maior, menor_ea, exat_menor, pre_menor, eixo_y_exato, eixo_y_predict, eixo_x)

    def gerar_preview_nn(self):
        prev = Treinamento()
        salvar_m = self.save_model.get()
        
        cidade = self.get_end(self.data_s.get())
        
        indicador = self.ind_s.get()
        if indicador == 'Precipitação':
            indicador = 3
        elif indicador == 'Temperatura máxima':
            indicador = 4
        elif indicador == 'Temperatura mínima':
            indicador = 5
    
        divisao = int(self.por_trei.get())

        activ = self.activation_v.get()
        solv = self.solver_v.get()
        alph = float(self.alpha_v.get())
        batc = self.batch_size_v.get()
        learn_r = self.learning_rate_v.get()
        learn_r_ini = float(self.learning_rate_init_v.get())
        powt = float(self.power_t_v.get())
        maxit = int(self.max_iter_v.get())
        shuf = self.shuffle_v.get()
        tol = float(self.tol_v.get())
        verb = self.verbose_v.get()
        warms = self.warm_start_v.get()
        moment = float(self.momentum_v.get())
        neste = self.nesterovs_momentum_v.get()
        earlyst = self.early_stopping_v.get()
        valid = float(self.validation_fraction_v.get())
        b1 = float(self.beta_1_v.get())
        b2 = float(self.beta_2_v.get())
        niter = int(self.n_iter_no_change_v.get())
        maxfun = int(self.max_fun_v.get())
        n_teste = int(self.num_teste.get())
        pts, media_ea, media_er, maior_ea, exat_maior, pre_maior, menor_ea, exat_menor, pre_menor, eixo_y_exato, eixo_y_predict, eixo_x = prev.RedeNeural(cidade, indicador, divisao, n_teste, activ, solv, alph, batc, learn_r, learn_r_ini, powt, maxit, shuf, tol, verb, warms, moment, neste, earlyst, valid, b1, b2, niter, maxfun, salvar_m)

        self.data_prev(pts, media_ea, media_er, maior_ea, exat_maior, pre_maior, menor_ea, exat_menor, pre_menor, eixo_y_exato, eixo_y_predict, eixo_x)
    
    def gerar_preview_svm(self):
        prev = Treinamento()
        salvar_m = self.save_model.get()
        
        cidade = self.get_end(self.data_s.get())
        
        indicador = self.ind_s.get()
        if indicador == 'Precipitação':
            indicador = 3
        elif indicador == 'Temperatura máxima':
            indicador = 4
        elif indicador == 'Temperatura mínima':
            indicador = 5
    
        divisao = int(self.por_trei.get())
        n_teste = int(self.num_teste.get())
        kern = self.kernel_v.get()
        degre = self.degree_v.get()
        gam = self.gamma_v.get()
        coef = float(self.coef0_v.get())
        t = float(self.tol_v.get())
        c = float(self.c_v.get())
        eps = float(self.epsilon_v.get())
        shr = self.shrinking_v.get()
        cach = float(self.cache_size_v.get())
        verb = self.verbose_v.get()
        maxi = int(self.maxiter_v.get())


        pts, media_ea, media_er, maior_ea, exat_maior, pre_maior, menor_ea, exat_menor, pre_menor, eixo_y_exato, eixo_y_predict, eixo_x = prev.SVR(cidade, indicador, divisao, n_teste, kern, degre, gam, coef, t, c, eps, shr, cach, verb, maxi, salvar_m)

        self.data_prev(pts, media_ea, media_er, maior_ea, exat_maior, pre_maior, menor_ea, exat_menor, pre_menor, eixo_y_exato, eixo_y_predict, eixo_x)
        
    def gerar_preview_Kn(self):
        prev = Treinamento()
        salvar_m = self.save_model.get()

        cidade = self.get_end(self.data_s.get())

        '''if self.data_s.get() == 'Cidade alvo':
            cidade = r'E:\IC\Interface_Grafica\Dados_verificacao\alvo_limpa.txt'
        elif self.data_s.get() == 'Vizinha A':
            cidade = r'E:\IC\Interface_Grafica\Dados_verificacao\vizinhaA_limpa.txt'
        elif self.data_s.get() == 'Vizinha B':
            cidade = r'E:\IC\Interface_Grafica\Dados_verificacao\vizinhaB_limpa.txt'
        elif self.data_s.get() == 'Vizinha C':
            cidade = r'E:\IC\Interface_Grafica\Dados_verificacao\vizinhaC_limpa.txt'''

        n_tes = int(self.num_teste.get())
        divisao = int(self.por_trei.get())
        n_neig = self.n_neighbors_v.get()
        algor = self.algorithm_v.get()
        leaf_s = self.leaf_size_v.get()
        pv = self.p_v.get()
        n_job = self.n_jobs_v.get()

        if n_job.isdigit() == True:
            n_job = int(n_job)
            
        indicador = self.ind_s.get()
        if indicador == 'Precipitação':
            indicador = 3
        elif indicador == 'Temperatura máxima':
            indicador = 4
        elif indicador == 'Temperatura mínima':
            indicador = 5

        pts, media_ea, media_er, maior_ea, exat_maior, pre_maior, menor_ea, exat_menor, pre_menor, eixo_y_exato, eixo_y_predict, eixo_x = prev.KNeighbors(cidade, indicador, divisao, n_tes, n_neig, algor, leaf_s, pv, n_job, salvar_m)
        self.data_prev(pts, media_ea, media_er, maior_ea, exat_maior, pre_maior, menor_ea, exat_menor, pre_menor, eixo_y_exato, eixo_y_predict, eixo_x)

    def gera_param(self):
        opcao = self.ml_selected.get()
        if opcao == 'Decision Trees':
            w = Canvas(self, width=615, height=900, background=fundo, border=0)
            w.place(x=10, y=95)
            self.lbf_p = LabelFrame(self, text='Parâmetros', width=600, height=395, font='Arial 12 bold', fg ='white', bg=fundo).place(x=20, y=100)

            self.criterion_v = StringVar()
            lista_cri = ["squared_error", "friedman_mse", "absolute_error", "poisson"]
            self.criterion_v.set("squared_error")
            Label(self, text='Criterion:', font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=120)
            ttk.Combobox(self, values=lista_cri, textvariable=self.criterion_v, width=25, font='Arial 12', justify=CENTER, state='readonly').place(x=50, y=145)

            self.splitter_v = StringVar()
            lista_spl = ["best", "random"]
            self.splitter_v.set("best")
            Label(self, text='Splitter:', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=120)
            ttk.Combobox(self, values=lista_spl, textvariable=self.splitter_v, width=25, font='Arial 12', justify=CENTER, state='readonly').place(x=340, y=145)
            

            self.maxd_v = StringVar()
            self.maxd_v.set("10")
            Label(self, text="Max_deph (int):", font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=180)
            self.ent_maxd = Entry(self, textvariable=self.maxd_v, width=27, font='Arial 12', justify=CENTER).place(x=50, y=205)

            self.minsam_s_v = IntVar()
            self.minsam_s_v.set(2)
            Label(self, text="Min_samples_split (int/float (.)):", font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=180)
            self.minsam_s = Entry(self, textvariable=self.minsam_s_v, width=27, font='Arial 12', justify=CENTER).place(x=340, y=205)
            
            self.minsam_l_v = IntVar()
            self.minsam_l_v.set(50)
            Label(self, text="Min_samples_leaf (int/float (.)):", font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=240)
            self.ent_minsam_l = Entry(self, textvariable=self.minsam_l_v, width=27, font='Arial 12', justify=CENTER).place(x=50, y=265)

            self.minweifra_l_v = StringVar()
            self.minweifra_l_v.set("0.0")
            Label(self, text="Min_weight_fraction_leaf (float (.)):", font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=240)
            self.ent_minweifra_l = Entry(self, textvariable=self.minweifra_l_v, width=27, font='Arial 12', justify=CENTER).place(x=340, y=265)
            
            self.maxfeat_v = StringVar()
            self.maxfeat_v.set("auto")
            Label(self, text="Max_features :", font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=300)
            Label(self, text="Valores para Max_features:", font='Arial 12 bold', fg=fun_alt, bg=fundo).place(x=340, y=300)
            Label(self, text="int / float / 'auto' / 'sqrt' / 'log2'", font='Arial 12 bold', fg=fun_alt, bg=fundo).place(x=340, y=325)
            self.ent_maxfeat_v = Entry(self, textvariable=self.maxfeat_v, width=27, font='Arial 12', justify=CENTER).place(x=50, y=325)

            self.maxleaf_n = StringVar()
            self.maxleaf_n.set("10")
            Label(self, text="Max_leaf_nodes (int)", font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=360)
            self.ent_maxleaf_n = Entry(self, textvariable=self.maxleaf_n, width=27, font='Arial 12', justify=CENTER).place(x=50, y=385)

            self.minimp_dec = StringVar()
            self.minimp_dec.set("0.0")
            Label(self, text="Min_impurity_decrease (float (.))", font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=360)
            self.ent_minimp_dec = Entry(self, textvariable=self.minimp_dec, width=27, font='Arial 12', justify=CENTER).place(x=340, y=385)

            self.ccp_alp_v = StringVar()
            self.ccp_alp_v.set("0.0")
            Label(self, text="Ccp_alpha (value>0.0 float):", font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=420)
            self.ent_ccp_alp = Entry(self, textvariable=self.ccp_alp_v, width=27, font='Arial 12', justify=CENTER).place(x=50, y=445)

            self.lbf_d = LabelFrame(self, text='Dados', width=600, height=170, font='Arial 12 bold', fg ='white', bg=fundo).place(x=20, y=500)

            self.data_s = StringVar()
            self.data_s.set('Cidade alvo')
            lista_dt = ['Cidade alvo', 'Vizinha A', 'Vizinha B', 'Vizinha C']
            Label(self, text="Dados para treinamento:", font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=520)
            self.combo_c = ttk.Combobox(self, values=lista_dt, textvariable=self.data_s, width=25, font='Arial 12', justify=CENTER, state='readonly').place(x=50, y=545)

            self.ind_s = StringVar()
            self.ind_s.set('Temperatura máxima')
            lista_ind = ['Precipitação', 'Temperatura máxima', 'Temperatura mínima']
            Label(self, text='Indicador:', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=520)
            ttk.Combobox(self, values=lista_ind, textvariable=self.ind_s, width=25, font='Arial 12', justify=CENTER, state='readonly').place(x=340, y=545)

            self.por_trei = IntVar()
            self.por_trei.set(70)
            Label(self, text="Porção para treinamento:", font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=580)
            Scale(self, variable=self.por_trei, orient=HORIZONTAL, length=240).place(x=50, y=605)
        
            self.num_teste = IntVar()
            self.num_teste.set(5)
            Label(self, text="Número de testes (int):", font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=580)
            self.ent_num_teste = Entry(self, textvariable=self.num_teste, width=27, font='Arial 12', justify=CENTER).place(x=340, y=605)

           
            Button(self, text='Preview', font='Arial 11 bold', fg='white', bg=fun_b, width=25, command=self.gerar_preview_dt).place(x=50, y=685)
            #Button(self, text='Salvar Paramt.', font='Arial 11 bold', fg='white', bg=fun_b, width=25, command=self.salvar_paramt).place(x=340, y=685)
            self.save_model = IntVar()
            Checkbutton(self, text='Salvar modelo', variable=self.save_model, bg=fundo, font='Arial 12 bold', activebackground=fundo).place(x=340, y=685)
        elif opcao == 'Neural network':
            w = Canvas(self, width=615, height=900, background=fundo, border=0)
            w.place(x=10, y=95)
            self.lbf_para_nn = LabelFrame(self, text='Parâmetros', width=600, height=625, font='Arial 12 bold', fg='white', bg=fundo).place(x=20, y=100)

            self.activation_v = StringVar()
            lista_act = ['identity', 'logistic', 'tanh', 'relu']
            self.activation_v.set('relu')
            Label(self, text='Activation:', font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=120)
            ttk.Combobox(self, values=lista_act, textvariable=self.activation_v, width=25, font='Arial 12', justify=CENTER, state='readonly').place(x=50, y=145)
            
            self.solver_v = StringVar()
            lista_sol = ['lbfgs', 'sgd', 'adam']
            self.solver_v.set('adam')
            Label(self, text='Solver:', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=120)
            ttk.Combobox(self, values=lista_sol, textvariable=self.solver_v, width=25, font='Arial 12', justify=CENTER, state='readonly').place(x=340, y=145)

            self.alpha_v = StringVar()
            self.alpha_v.set('0.0001')
            Label(self, text='Alpha:', font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=180)
            Entry(self, textvariable=self.alpha_v, width=27, font='Arial 12', justify=CENTER).place(x=50, y=205)

            self.batch_size_v = StringVar()
            self.batch_size_v.set('auto')
            Label(self, text='Batch_size (int / "auto"):', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=180)
            Entry(self, textvariable=self.batch_size_v, width=27, font='Arial 12', justify=CENTER).place(x=340, y=205)

            self.learning_rate_v = StringVar()
            lista_learn = ['constant', 'invscaling', 'adaptive']
            self.learning_rate_v.set('constant')
            Label(self, text="Learning_rate:", font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=240)
            ttk.Combobox(self, values=lista_learn, textvariable=self.learning_rate_v, width=25, font='Arial 12', justify=CENTER, state='readonly').place(x=50, y=265)

            self.learning_rate_init_v = StringVar()
            self.learning_rate_init_v.set('0.001')
            Label(self, text='Learning_rate_init (float):', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=240)
            Entry(self, textvariable=self.learning_rate_init_v, width=27, font='Arial 12', justify=CENTER).place(x=340, y=265)

            self.power_t_v = StringVar()
            self.power_t_v.set('0.5')
            Label(self, text='Power_t (float):', font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=300)
            Entry(self, textvariable=self.power_t_v, width=27, font='Arial 12', justify=CENTER).place(x=50, y=325)

            self.max_iter_v = StringVar()
            self.max_iter_v.set('200')
            Label(self, text='Max_iter (int):', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=300)
            Entry(self, textvariable=self.max_iter_v, width=27, font='Arial 12', justify=CENTER).place(x=340, y=325)


            self.shuffle_v = BooleanVar()
            self.shuffle_v.set(True)
            Label(self, text='Shuffle (bool 1/0):', font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=360)
            Entry(self, textvariable=self.shuffle_v, width=27, font='Arial 12', justify=CENTER).place(x=50, y=385)

            self.tol_v = StringVar()
            self.tol_v.set('0.0001')
            Label(self, text='Tol (float):', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=360)
            Entry(self, textvariable=self.tol_v, width=27, font='Arial 12', justify=CENTER).place(x=340, y=385)

            self.verbose_v = BooleanVar()
            self.verbose_v.set(False)
            Label(self, text='Verbose (bool 1/0):', font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=420)
            Entry(self, textvariable=self.verbose_v, width=27, font='Arial 12', justify=CENTER).place(x=50, y=445)

            self.warm_start_v = BooleanVar()
            self.warm_start_v.set(False)
            Label(self, text='Warm_start (bool 1/0):', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=420)
            Entry(self, textvariable=self.warm_start_v, width=27, font='Arial 12', justify=CENTER).place(x=340, y=445)

            self.momentum_v = StringVar()
            self.momentum_v.set('0.9')
            Label(self, text='Momentum (float):', font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=480)
            Entry(self, textvariable=self.momentum_v, width=27, font='Arial 12', justify=CENTER).place(x=50, y=505)

            self.nesterovs_momentum_v = BooleanVar()
            self.nesterovs_momentum_v.set(True)
            Label(self, text='Nesterovs_momentum:', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=480)
            Entry(self, textvariable=self.nesterovs_momentum_v, width=27, font='Arial 12', justify=CENTER).place(x=340, y=505)

            self.early_stopping_v = BooleanVar()
            self.early_stopping_v.set(False)
            Label(self, text='Early_stopping:', font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=540)
            Entry(self, textvariable=self.early_stopping_v, width=27, font='Arial 12', justify=CENTER).place(x=50, y=565)

            self.validation_fraction_v = StringVar()
            self.validation_fraction_v.set('0.1')
            Label(self, text='Validation_fraction (float):', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=540)
            Entry(self, textvariable=self.validation_fraction_v, width=27, font='Arial 12', justify=CENTER).place(x=340, y=565)

            self.beta_1_v = StringVar()
            self.beta_1_v.set('0.9')
            Label(self, text='Beta_1 (float):', font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=600)
            Entry(self, textvariable=self.beta_1_v, width=27, font='Arial 12', justify=CENTER).place(x=50, y=625)

            self.beta_2_v = StringVar()
            self.beta_2_v.set('0.999')
            Label(self, text='Beta_2 (float):', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=600)
            Entry(self, textvariable=self.beta_2_v, width=27, font='Arial 12', justify=CENTER).place(x=340, y=625)

            self.n_iter_no_change_v = StringVar()
            self.n_iter_no_change_v.set('10')
            Label(self, text='N_iter_no_change (int):', font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=660)
            Entry(self, textvariable=self.n_iter_no_change_v, width=27, font='Arial 12', justify=CENTER).place(x=50, y=685)

            self.max_fun_v = StringVar()
            self.max_fun_v.set('15000')
            Label(self, text='max_fun (int):', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=660)
            Entry(self, textvariable=self.max_fun_v, width=27, font='Arial 12', justify=CENTER).place(x=340, y=685)

            '''   data   '''
            self.lbf_dt_nn = LabelFrame(self, text='Dados', width=600, height=170, font='Arial 12 bold', fg ='white', bg=fundo).place(x=20, y=730)

            self.data_s = StringVar()
            self.data_s.set('Cidade alvo')
            lista_dt = ['Cidade alvo', 'Vizinha A', 'Vizinha B', 'Vizinha C']
            Label(self, text="Dados para treinamento:", font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=750)
            self.combo_c = ttk.Combobox(self, values=lista_dt, textvariable=self.data_s, width=25, font='Arial 12', justify=CENTER, state='readonly').place(x=50, y=775)

            self.ind_s = StringVar()
            self.ind_s.set('Temperatura máxima')
            lista_ind = ['Precipitação', 'Temperatura máxima', 'Temperatura mínima']
            Label(self, text='Indicador:', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=750)
            ttk.Combobox(self, values=lista_ind, textvariable=self.ind_s, width=25, font='Arial 12', justify=CENTER, state='readonly').place(x=340, y=775)

            self.por_trei = IntVar()
            self.por_trei.set(70)
            Label(self, text="Porção para treinamento:", font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=810)
            Scale(self, variable=self.por_trei, orient=HORIZONTAL, length=240).place(x=50, y=835)
        
            self.num_teste = IntVar()
            self.num_teste.set(5)
            Label(self, text="Número de testes (int):", font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=810)
            self.ent_num_teste = Entry(self, textvariable=self.num_teste, width=27, font='Arial 12', justify=CENTER).place(x=340, y=835)

            Button(self, text='Preview', font='Arial 11 bold', fg='white', bg=fun_b, width=25, command=self.gerar_preview_nn).place(x=50, y=915)
            self.save_model = IntVar()
            Checkbutton(self, text='Salvar modelo', variable=self.save_model, bg=fundo, font='Arial 12 bold', activebackground=fundo).place(x=340, y=915)
        elif opcao == 'Nearest Neighbors':

           w = Canvas(self, width=615, height=900, background=fundo, border=0)
           w.place(x=10, y=95)
           

           self.lbf_para_nn = LabelFrame(self, text='Parâmetros', width=600, height=205, font='Arial 12 bold', fg='white', bg=fundo).place(x=20, y=100) 

           self.n_neighbors_v = IntVar()
           self.n_neighbors_v.set(5)
           Label(self, text='N_neighbors (int):', font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=120)
           Entry(self, textvariable=self.n_neighbors_v, width=27, font='Arial 12', justify=CENTER).place(x=50, y=145)

           self.algorithm_v = StringVar()
           lista_alg = ['auto', 'ball_tree', 'kd_tree', 'brute']
           self.algorithm_v.set('auto')
           Label(self, text='Algorithm:', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=120)
           ttk.Combobox(self, values=lista_alg, textvariable=self.algorithm_v, width=25, font='Arial 12', justify=CENTER, state='readonly').place(x=340, y=145)

           self.leaf_size_v = IntVar()
           self.leaf_size_v.set(30)
           Label(self, text='Leaf_size (int):', font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=180)
           Entry(self, textvariable=self.leaf_size_v, width=27, font='Arial 12', justify=CENTER).place(x=50, y=205)

           self.p_v = IntVar()
           self.p_v.set(2)
           Label(self, text='P (int):', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=180)
           Entry(self, textvariable=self.p_v, width=27, font='Arial 12', justify=CENTER).place(x=340, y=205)

           self.n_jobs_v = StringVar()
           self.n_jobs_v.set('5')
           Label(self, text='N_jobs (int / "None"):', font='Aria 12 bold', fg='white', bg=fundo).place(x=50, y=240)
           Entry(self, textvariable=self.n_jobs_v, width=27, font='Arial 12', justify=CENTER).place(x=50, y=265)

           self.lbf_d = LabelFrame(self, text='Dados', width=600, height=170, font='Arial 12 bold', fg ='white', bg=fundo).place(x=20, y=320)

           self.data_s = StringVar()
           self.data_s.set('Cidade alvo')
           lista_dt = ['Cidade alvo', 'Vizinha A', 'Vizinha B', 'Vizinha C']
           Label(self, text="Dados para treinamento:", font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=340)
           self.combo_c = ttk.Combobox(self, values=lista_dt, textvariable=self.data_s, width=25, font='Arial 12', justify=CENTER, state='readonly').place(x=50, y=365)

           self.ind_s = StringVar()
           self.ind_s.set('Temperatura máxima')
           lista_ind = ['Precipitação', 'Temperatura máxima', 'Temperatura mínima']
           Label(self, text='Indicador:', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=340)
           ttk.Combobox(self, values=lista_ind, textvariable=self.ind_s, width=25, font='Arial 12', justify=CENTER, state='readonly').place(x=340, y=365)

           self.por_trei = IntVar()
           self.por_trei.set(70)
           Label(self, text="Porção para treinamento:", font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=400)
           Scale(self, variable=self.por_trei, orient=HORIZONTAL, length=240).place(x=50, y=425)

           self.num_teste = IntVar()
           self.num_teste.set(5)
           Label(self, text="Número de testes (int):", font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=400)
           self.ent_num_teste = Entry(self, textvariable=self.num_teste, width=27, font='Arial 12', justify=CENTER).place(x=340, y=425)

           Button(self, text='Preview', font='Arial 11 bold', fg='white', bg=fun_b, width=25, command=self.gerar_preview_Kn).place(x=50, y=505)
           self.save_model = IntVar()
           Checkbutton(self, text='Salvar modelo', variable=self.save_model, bg=fundo, font='Arial 12 bold', activebackground=fundo).place(x=340, y=505) 
        elif opcao == 'Support Vector':
            w = Canvas(self, width=615, height=900, background=fundo, border=0)
            w.place(x=10, y=95)
            self.lbf_para_nn = LabelFrame(self, text='Parâmetros', width=600, height=385, font='Arial 12 bold', fg='white', bg=fundo).place(x=20, y=100)
            
            self.kernel_v = StringVar()
            lista_ker = ['linear', 'poly', 'rbf', 'sigmoid']
            self.kernel_v.set('rbf')
            Label(self, text='Kernel:', font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=120)
            ttk.Combobox(self, values=lista_ker, textvariable=self.kernel_v, width=25, font='Arial 12', justify=CENTER, state='readonly').place(x=50, y=145)

            self.degree_v = IntVar()
            self.degree_v.set(3)
            Label(self, text='Degree (int):', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=120)
            Entry(self, textvariable=self.degree_v, font='Arial 12', width=27, justify=CENTER).place(x=340, y=145) 

            self.gamma_v = StringVar()
            self.gamma_v.set('scale')
            Label(self, text='Gamma ("scale", "auto", float):', font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=180)
            Entry(self, textvariable=self.gamma_v, font='Arial 12', width=27, justify=CENTER).place(x=50, y=205)

            self.coef0_v = StringVar()
            self.coef0_v.set('0.0')
            Label(self, text='Coef0 (float):', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=180)
            Entry(self, textvariable=self.coef0_v, font='Arial 12', width=27, justify=CENTER).place(x=340, y=205)

            self.tol_v = StringVar()
            self.tol_v.set('0.001')
            Label(self, text='Tol (float):', font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=240)
            Entry(self, textvariable=self.tol_v, font='Arial 12', width=27, justify=CENTER).place(x=50, y=265)

            self.c_v = StringVar()
            self.c_v.set('1.0')
            Label(self, text='C (float):', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=240)
            Entry(self, textvariable=self.c_v, font='Arial 12', width=27, justify=CENTER).place(x=340, y=265)

            self.epsilon_v = StringVar()
            self.epsilon_v.set('0.1')
            Label(self, text='Epsilon (float):', font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=300)
            Entry(self, textvariable=self.epsilon_v, font='Arial 12', width=27, justify=CENTER).place(x=50, y=325)   

            self.shrinking_v = BooleanVar()
            self.shrinking_v.set(True)
            Label(self, text='Shrinking (Bool):', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=300)
            Entry(self, textvariable=self.shrinking_v, font='Arial 12', width=27, justify=CENTER).place(x=340, y=325)

            self.cache_size_v = StringVar()
            self.cache_size_v.set('200')
            Label(self, text='Cache_size (float):', font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=360)
            Entry(self, textvariable=self.cache_size_v, font='Arial 12', width=27, justify=CENTER).place(x=50, y=385)   

            self.verbose_v = BooleanVar()
            self.verbose_v.set(False)
            Label(self, text='Verbose (Bool):', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=360)
            Entry(self, textvariable=self.verbose_v, font='Arial 12', width=27, justify=CENTER).place(x=340, y=385)

            self.maxiter_v = IntVar()
            self.maxiter_v.set(-1)
            Label(self, text='Max_iter (int):', font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=420)
            Entry(self, textvariable=self.maxiter_v, font='Arial 12', width=27, justify=CENTER).place(x=50, y=445)

            self.lbf_dt_nn = LabelFrame(self, text='Dados', width=600, height=170, font='Arial 12 bold', fg ='white', bg=fundo).place(x=20, y=500)

            self.data_s = StringVar()
            self.data_s.set('Cidade alvo')
            lista_dt = ['Cidade alvo', 'Vizinha A', 'Vizinha B', 'Vizinha C']
            Label(self, text="Dados para treinamento:", font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=520)
            self.combo_c = ttk.Combobox(self, values=lista_dt, textvariable=self.data_s, width=25, font='Arial 12', justify=CENTER, state='readonly').place(x=50, y=545)

            self.ind_s = StringVar()
            self.ind_s.set('Temperatura máxima')
            lista_ind = ['Precipitação', 'Temperatura máxima', 'Temperatura mínima']
            Label(self, text='Indicador:', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=520)
            ttk.Combobox(self, values=lista_ind, textvariable=self.ind_s, width=25, font='Arial 12', justify=CENTER, state='readonly').place(x=340, y=545)

            self.por_trei = IntVar()
            self.por_trei.set(70)
            Label(self, text="Porção para treinamento:", font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=580)
            Scale(self, variable=self.por_trei, orient=HORIZONTAL, length=240).place(x=50, y=605)
        
            self.num_teste = IntVar()
            self.num_teste.set(5)
            Label(self, text="Número de testes (int):", font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=580)
            self.ent_num_teste = Entry(self, textvariable=self.num_teste, width=27, font='Arial 12', justify=CENTER).place(x=340, y=605)

            Button(self, text='Preview', font='Arial 11 bold', fg='white', bg=fun_b, width=25, command=self.gerar_preview_svm).place(x=50, y=680)
            self.save_model = IntVar()
            Checkbutton(self, text='Salvar modelo', variable=self.save_model, bg=fundo, font='Arial 12 bold', activebackground=fundo).place(x=340, y=680)
        elif opcao == 'Gaussian Process':
            w = Canvas(self, width=615, height=900, background=fundo, border=0)
            w.place(x=10, y=95)
            self.lbf_para_nn = LabelFrame(self, text='Parâmetros', width=600, height=205, font='Arial 12 bold', fg='white', bg=fundo).place(x=20, y=100)
            
            self.alpha_gp = StringVar()
            self.alpha_gp.set('0.0000000001')
            Label(self, text='Alpha (float): ', font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=120)
            Entry(self, textvariable=self.alpha_gp, font='Arial 12', width=27, justify=CENTER).place(x=50, y=145)
            
            self.n_restarts_op = IntVar()
            self.n_restarts_op.set(0)
            Label(self, text='N_restart_optimizer (int):', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=120)
            Entry(self, textvariable=self.n_restarts_op, font='Arial 12', width=27, justify=CENTER).place(x=340, y=145)

            self.normalize_y_gp = BooleanVar()
            self.normalize_y_gp.set(0)
            Label(self, text='Normalize_y (Bool 1/0):', font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=180)
            Entry(self, textvariable=self.normalize_y_gp, font='Arial 12', width=27, justify=CENTER).place(x=50, y=205)

            self.copy_X_train = BooleanVar()
            self.copy_X_train.set(0)
            Label(self, text='Copy_X_train (Bool 1/0):', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=180)
            Entry(self, textvariable=self.copy_X_train, font='Arial 12', width=27, justify=CENTER).place(x=340, y=205)

            self.rand_state_gp = StringVar()
            self.rand_state_gp.set('None')
            Label(self, text='Random_state ("None" / int):', font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=240)
            Entry(self, textvariable=self.rand_state_gp, font='Arial 12', width=27, justify=CENTER).place(x=50, y=265)
            

            self.lbf_dt_nn = LabelFrame(self, text='Dados', width=600, height=170, font='Arial 12 bold', fg ='white', bg=fundo).place(x=20, y=320)

            self.data_s = StringVar()
            self.data_s.set('Cidade alvo')
            lista_dt = ['Cidade alvo', 'Vizinha A', 'Vizinha B', 'Vizinha C']
            Label(self, text="Dados para treinamento:", font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=340)
            self.combo_c = ttk.Combobox(self, values=lista_dt, textvariable=self.data_s, width=25, font='Arial 12', justify=CENTER, state='readonly').place(x=50, y=365)

            self.ind_s = StringVar()
            self.ind_s.set('Temperatura máxima')
            lista_ind = ['Precipitação', 'Temperatura máxima', 'Temperatura mínima']
            Label(self, text='Indicador:', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=340)
            ttk.Combobox(self, values=lista_ind, textvariable=self.ind_s, width=25, font='Arial 12', justify=CENTER, state='readonly').place(x=340, y=365)

            self.por_trei = IntVar()
            self.por_trei.set(70)
            Label(self, text="Porção para treinamento:", font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=400)
            Scale(self, variable=self.por_trei, orient=HORIZONTAL, length=240).place(x=50, y=425)
        
            self.num_teste = IntVar()
            self.num_teste.set(5)
            Label(self, text="Número de testes (int):", font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=400)
            self.ent_num_teste = Entry(self, textvariable=self.num_teste, width=27, font='Arial 12', justify=CENTER).place(x=340, y=425)

            Button(self, text='Preview', font='Arial 11 bold', fg='white', bg=fun_b, width=25, command=self.gerar_preview_svm).place(x=50, y=505)
            self.save_model = IntVar()
            Checkbutton(self, text='Salvar modelo', variable=self.save_model, bg=fundo, font='Arial 12 bold', activebackground=fundo).place(x=340, y=505)
    '''
    def __init__(self, master=None):
        Toplevel.__init__(self, master=master)
        self.title('Aprendizado de máquina')
        self.geometry('800x800')
        self.configure(background=fundo)

        Label(self, text='APRENDIZADO DE MÁQUINA', font='Arial 14 bold', fg='white', bg=fundo).place(x=200, y=20)

        self.ml_selected = StringVar()
        self.ml_selected.set('Decision Trees')
        lista_ml = ['Decision Trees', 'Neural network', 'Nearest Neighbors', 'Support Vector', 'Gaussian Process']
        ttk.Combobox(self, values=lista_ml, textvariable=self.ml_selected, width=28, font='Arial 12', justify=CENTER, state='readonly').place(x=20, y=60)
        Button(self, text='Escolher Machine Learning', font='Arial 11 bold', fg='white', bg=fun_ap, width=30, command=self.gera_param).place(x=340, y=59)
    '''
class Aprendizado_Marquina(Toplevel):
    def int_float(self, val):
        try:
            return int(val)
        except ValueError:
            return float(val)

    def valid_maxf(self, val):
        if val.isdigit() == True:
            val = int(val)
        elif val.isalnum() == True and val.isdigit() == False:
            val = str(val)
        elif val.isalnum() == False and val.isdigit() == False and val.isalpha() == False:
            val = float(val)
        
        return val

    def salvar_paramt(self):
        img = pyscreenshot.grab(bbox=(0,25,1920,1040))
        img.show()
        img.save(r'C:\Users\pablo\Desktop\teste.png')

    def data_prev(self, pts, media_ea, media_er, maior_ea, exat_maior, pre_maior, menor_ea, exat_menor, pre_menor, eixo_y_exato, eixo_y_predict, eixo_x):
        self.laf_res = LabelFrame(self, text='Preview dos resultados', width=1250, height=950, font='Arial 12 bold', fg='white', bg=fundo).place(x=650, y=50)
        Label(self, text='Pontuação (0-100): '+ str(pts) +'pts', font='Arial 12 bold', fg='white', bg=fundo).place(x=680, y=70)
        media_ea = round(media_ea, 4)
        Label(self, text='Média Erro absoluto: '+ str(media_ea), font='Arial 12 bold', fg='white', bg=fundo).place(x=680, y=100)
        media_er = round(media_er, 4)
        Label(self, text='Média Erro relativo: '+ str(media_er), font='Arial 12 bold', fg='white', bg=fundo).place(x=680, y=130)

        Label(self, text='Maior erro absoluto: ' + str(round(maior_ea,4)), font='Arial 12 bold', fg='white', bg=fundo).place(x=680, y=160)
        Label(self, text="Valor exato do maior EA: " + str(round(exat_maior,4)),font='Arial 12 bold', fg='white', bg=fundo).place(x=940, y=160)
        Label(self, text="Predict do maior EA: " + str(round(pre_maior, 4)), font='Arial 12 bold', fg='white', bg=fundo).place(x=1200, y=160)

        Label(self, text='Menor erro absoluto: ' + str(round(menor_ea,4)), font='Arial 12 bold', fg='white', bg=fundo).place(x=680, y=190)
        Label(self, text="Valor exato do menor EA: " + str(round(exat_menor,4)),font='Arial 12 bold', fg='white', bg=fundo).place(x=940, y=190)
        Label(self, text="Predict do menor EA: " + str(round(pre_menor, 4)), font='Arial 12 bold', fg='white', bg=fundo).place(x=1200, y=190)

        figura = Figure(figsize=(12,7.3), dpi=100)
        plot_r = figura.add_subplot(111)
        plot_r.plot(eixo_x, eixo_y_exato,label='Exato', color='green')
        plot_r.plot(eixo_x, eixo_y_predict, label='Predict', color='red')
        plot_r.legend()
        plot_r.grid(True)
        plot_r.set_ylabel("Temperatura(°C)")
        plot_r.set_xlabel("Comparações")

        canvas = FigureCanvasTkAgg(figura, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack()
        canvas.get_tk_widget().place(x=680, y=240)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.place(x=1150, y=10)
        toolbar.update()
    
    def get_end(self, cidade):
        Trat = Tratamento()
        return Trat.retorna_end(cidade)

    def gerar_preview_dt(self):
        prev = Treinamento()
        salvar_m = self.save_model.get()
        


        #cidade = self.get_end(self.data_s.get())
        cidade = self.data_s.get()
        indicador = self.ind_s.get()
        divisao = int(self.por_trei.get())
        criterio = self.criterion_v.get()
        splitter = self.splitter_v.get()
        maxd = int(self.maxd_v.get())             #* Max_depth
        minsams = self.int_float(self.minsam_s_v.get())    #* Min_samples_split
        minsaml = self.int_float(self.minsam_l_v.get())    #* Min_samples_leaf
        minwei = float(self.minweifra_l_v.get())
        maxfe = self.valid_maxf(self.maxfeat_v.get())
        maxleaf = int(self.maxleaf_n.get())
        
        minim = float(self.minimp_dec.get())
        ccp = float(self.ccp_alp_v.get())
        n_tes = int(self.num_teste.get())

        if indicador == 'Precipitação':
            indicador = 3
        elif indicador == 'Temperatura máxima':
            indicador = 4
        elif indicador == 'Temperatura mínima':
            indicador = 5

        pts, media_ea, media_er, maior_ea, exat_maior, pre_maior, menor_ea, exat_menor, pre_menor, eixo_y_exato, eixo_y_predict, eixo_x = prev.ArvoreDecisao(cidade, indicador, divisao, criterio, splitter, maxd, minsaml, maxfe, maxleaf, n_tes, minsams, minwei, minim, ccp, salvar_m)
        self.data_prev(pts, media_ea, media_er, maior_ea, exat_maior, pre_maior, menor_ea, exat_menor, pre_menor, eixo_y_exato, eixo_y_predict, eixo_x)

    def gerar_preview_nn(self):
        prev = Treinamento()
        salvar_m = self.save_model.get()
        
        cidade = self.get_end(self.data_s.get())
        
        indicador = self.ind_s.get()
        if indicador == 'Precipitação':
            indicador = 3
        elif indicador == 'Temperatura máxima':
            indicador = 4
        elif indicador == 'Temperatura mínima':
            indicador = 5
    
        divisao = int(self.por_trei.get())

        activ = self.activation_v.get()
        solv = self.solver_v.get()
        alph = float(self.alpha_v.get())
        batc = self.batch_size_v.get()
        learn_r = self.learning_rate_v.get()
        learn_r_ini = float(self.learning_rate_init_v.get())
        powt = float(self.power_t_v.get())
        maxit = int(self.max_iter_v.get())
        shuf = self.shuffle_v.get()
        tol = float(self.tol_v.get())
        verb = self.verbose_v.get()
        warms = self.warm_start_v.get()
        moment = float(self.momentum_v.get())
        neste = self.nesterovs_momentum_v.get()
        earlyst = self.early_stopping_v.get()
        valid = float(self.validation_fraction_v.get())
        b1 = float(self.beta_1_v.get())
        b2 = float(self.beta_2_v.get())
        niter = int(self.n_iter_no_change_v.get())
        maxfun = int(self.max_fun_v.get())
        n_teste = int(self.num_teste.get())
        pts, media_ea, media_er, maior_ea, exat_maior, pre_maior, menor_ea, exat_menor, pre_menor, eixo_y_exato, eixo_y_predict, eixo_x = prev.RedeNeural(cidade, indicador, divisao, n_teste, activ, solv, alph, batc, learn_r, learn_r_ini, powt, maxit, shuf, tol, verb, warms, moment, neste, earlyst, valid, b1, b2, niter, maxfun, salvar_m)

        self.data_prev(pts, media_ea, media_er, maior_ea, exat_maior, pre_maior, menor_ea, exat_menor, pre_menor, eixo_y_exato, eixo_y_predict, eixo_x)
    
    def gerar_preview_svm(self):
        prev = Treinamento()
        salvar_m = self.save_model.get()
        
        cidade = self.get_end(self.data_s.get())
        
        indicador = self.ind_s.get()
        if indicador == 'Precipitação':
            indicador = 3
        elif indicador == 'Temperatura máxima':
            indicador = 4
        elif indicador == 'Temperatura mínima':
            indicador = 5
    
        divisao = int(self.por_trei.get())
        n_teste = int(self.num_teste.get())
        kern = self.kernel_v.get()
        degre = self.degree_v.get()
        gam = self.gamma_v.get()
        coef = float(self.coef0_v.get())
        t = float(self.tol_v.get())
        c = float(self.c_v.get())
        eps = float(self.epsilon_v.get())
        shr = self.shrinking_v.get()
        cach = float(self.cache_size_v.get())
        verb = self.verbose_v.get()
        maxi = int(self.maxiter_v.get())


        pts, media_ea, media_er, maior_ea, exat_maior, pre_maior, menor_ea, exat_menor, pre_menor, eixo_y_exato, eixo_y_predict, eixo_x = prev.SVR(cidade, indicador, divisao, n_teste, kern, degre, gam, coef, t, c, eps, shr, cach, verb, maxi, salvar_m)

        self.data_prev(pts, media_ea, media_er, maior_ea, exat_maior, pre_maior, menor_ea, exat_menor, pre_menor, eixo_y_exato, eixo_y_predict, eixo_x)
        
    def gerar_preview_Kn(self):
        prev = Treinamento()
        salvar_m = self.save_model.get()

        cidade = self.get_end(self.data_s.get())

        '''if self.data_s.get() == 'Cidade alvo':
            cidade = r'E:\IC\Interface_Grafica\Dados_verificacao\alvo_limpa.txt'
        elif self.data_s.get() == 'Vizinha A':
            cidade = r'E:\IC\Interface_Grafica\Dados_verificacao\vizinhaA_limpa.txt'
        elif self.data_s.get() == 'Vizinha B':
            cidade = r'E:\IC\Interface_Grafica\Dados_verificacao\vizinhaB_limpa.txt'
        elif self.data_s.get() == 'Vizinha C':
            cidade = r'E:\IC\Interface_Grafica\Dados_verificacao\vizinhaC_limpa.txt'''

        n_tes = int(self.num_teste.get())
        divisao = int(self.por_trei.get())
        n_neig = self.n_neighbors_v.get()
        algor = self.algorithm_v.get()
        leaf_s = self.leaf_size_v.get()
        pv = self.p_v.get()
        n_job = self.n_jobs_v.get()

        if n_job.isdigit() == True:
            n_job = int(n_job)
            
        indicador = self.ind_s.get()
        if indicador == 'Precipitação':
            indicador = 3
        elif indicador == 'Temperatura máxima':
            indicador = 4
        elif indicador == 'Temperatura mínima':
            indicador = 5

        pts, media_ea, media_er, maior_ea, exat_maior, pre_maior, menor_ea, exat_menor, pre_menor, eixo_y_exato, eixo_y_predict, eixo_x = prev.KNeighbors(cidade, indicador, divisao, n_tes, n_neig, algor, leaf_s, pv, n_job, salvar_m)
        self.data_prev(pts, media_ea, media_er, maior_ea, exat_maior, pre_maior, menor_ea, exat_menor, pre_menor, eixo_y_exato, eixo_y_predict, eixo_x)

    def gera_param(self):
        opcao = self.ml_selected.get()
        if opcao == 'Decision Trees':
            w = Canvas(self, width=615, height=900, background=fundo, border=0)
            w.place(x=10, y=95)
            self.lbf_p = LabelFrame(self, text='Parâmetros', width=600, height=395, font='Arial 12 bold', fg ='white', bg=fundo).place(x=20, y=100)

            self.criterion_v = StringVar()
            lista_cri = ["squared_error", "friedman_mse", "absolute_error", "poisson"]
            self.criterion_v.set("squared_error")
            Label(self, text='Criterion:', font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=120)
            ttk.Combobox(self, values=lista_cri, textvariable=self.criterion_v, width=25, font='Arial 12', justify=CENTER, state='readonly').place(x=50, y=145)

            self.splitter_v = StringVar()
            lista_spl = ["best", "random"]
            self.splitter_v.set("best")
            Label(self, text='Splitter:', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=120)
            ttk.Combobox(self, values=lista_spl, textvariable=self.splitter_v, width=25, font='Arial 12', justify=CENTER, state='readonly').place(x=340, y=145)
            

            self.maxd_v = StringVar()
            self.maxd_v.set("10")
            Label(self, text="Max_deph (int):", font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=180)
            self.ent_maxd = Entry(self, textvariable=self.maxd_v, width=27, font='Arial 12', justify=CENTER).place(x=50, y=205)

            self.minsam_s_v = IntVar()
            self.minsam_s_v.set(2)
            Label(self, text="Min_samples_split (int/float (.)):", font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=180)
            self.minsam_s = Entry(self, textvariable=self.minsam_s_v, width=27, font='Arial 12', justify=CENTER).place(x=340, y=205)
            
            self.minsam_l_v = IntVar()
            self.minsam_l_v.set(50)
            Label(self, text="Min_samples_leaf (int/float (.)):", font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=240)
            self.ent_minsam_l = Entry(self, textvariable=self.minsam_l_v, width=27, font='Arial 12', justify=CENTER).place(x=50, y=265)

            self.minweifra_l_v = StringVar()
            self.minweifra_l_v.set("0.0")
            Label(self, text="Min_weight_fraction_leaf (float (.)):", font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=240)
            self.ent_minweifra_l = Entry(self, textvariable=self.minweifra_l_v, width=27, font='Arial 12', justify=CENTER).place(x=340, y=265)
            
            self.maxfeat_v = StringVar()
            self.maxfeat_v.set("auto")
            Label(self, text="Max_features :", font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=300)
            Label(self, text="Valores para Max_features:", font='Arial 12 bold', fg=fun_alt, bg=fundo).place(x=340, y=300)
            Label(self, text="int / float / 'auto' / 'sqrt' / 'log2'", font='Arial 12 bold', fg=fun_alt, bg=fundo).place(x=340, y=325)
            self.ent_maxfeat_v = Entry(self, textvariable=self.maxfeat_v, width=27, font='Arial 12', justify=CENTER).place(x=50, y=325)

            self.maxleaf_n = StringVar()
            self.maxleaf_n.set("10")
            Label(self, text="Max_leaf_nodes (int)", font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=360)
            self.ent_maxleaf_n = Entry(self, textvariable=self.maxleaf_n, width=27, font='Arial 12', justify=CENTER).place(x=50, y=385)

            self.minimp_dec = StringVar()
            self.minimp_dec.set("0.0")
            Label(self, text="Min_impurity_decrease (float (.))", font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=360)
            self.ent_minimp_dec = Entry(self, textvariable=self.minimp_dec, width=27, font='Arial 12', justify=CENTER).place(x=340, y=385)

            self.ccp_alp_v = StringVar()
            self.ccp_alp_v.set("0.0")
            Label(self, text="Ccp_alpha (value>0.0 float):", font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=420)
            self.ent_ccp_alp = Entry(self, textvariable=self.ccp_alp_v, width=27, font='Arial 12', justify=CENTER).place(x=50, y=445)

            self.lbf_d = LabelFrame(self, text='Dados', width=600, height=170, font='Arial 12 bold', fg ='white', bg=fundo).place(x=20, y=500)

            self.data_s = StringVar()
            self.data_s.set('Cidade alvo')
            lista_dt = ['Cidade alvo', 'Vizinha A', 'Vizinha B', 'Vizinha C']
            Label(self, text="Dados para treinamento:", font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=520)
            self.combo_c = ttk.Combobox(self, values=lista_dt, textvariable=self.data_s, width=25, font='Arial 12', justify=CENTER, state='readonly').place(x=50, y=545)

            self.ind_s = StringVar()
            self.ind_s.set('Temperatura máxima')
            lista_ind = ['Precipitação', 'Temperatura máxima', 'Temperatura mínima']
            Label(self, text='Indicador:', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=520)
            ttk.Combobox(self, values=lista_ind, textvariable=self.ind_s, width=25, font='Arial 12', justify=CENTER, state='readonly').place(x=340, y=545)

            self.por_trei = IntVar()
            self.por_trei.set(70)
            Label(self, text="Porção para treinamento:", font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=580)
            Scale(self, variable=self.por_trei, orient=HORIZONTAL, length=240).place(x=50, y=605)
        
            self.num_teste = IntVar()
            self.num_teste.set(5)
            Label(self, text="Número de testes (int):", font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=580)
            self.ent_num_teste = Entry(self, textvariable=self.num_teste, width=27, font='Arial 12', justify=CENTER).place(x=340, y=605)

           
            Button(self, text='Preview', font='Arial 11 bold', fg='white', bg=fun_b, width=25, command=self.gerar_preview_dt).place(x=50, y=685)
            #Button(self, text='Salvar Paramt.', font='Arial 11 bold', fg='white', bg=fun_b, width=25, command=self.salvar_paramt).place(x=340, y=685)
            self.save_model = IntVar()
            Checkbutton(self, text='Salvar modelo', variable=self.save_model, bg=fundo, font='Arial 12 bold', activebackground=fundo).place(x=340, y=685)
        elif opcao == 'Neural network':
            w = Canvas(self, width=615, height=900, background=fundo, border=0)
            w.place(x=10, y=95)
            self.lbf_para_nn = LabelFrame(self, text='Parâmetros', width=600, height=625, font='Arial 12 bold', fg='white', bg=fundo).place(x=20, y=100)

            self.activation_v = StringVar()
            lista_act = ['identity', 'logistic', 'tanh', 'relu']
            self.activation_v.set('relu')
            Label(self, text='Activation:', font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=120)
            ttk.Combobox(self, values=lista_act, textvariable=self.activation_v, width=25, font='Arial 12', justify=CENTER, state='readonly').place(x=50, y=145)
            
            self.solver_v = StringVar()
            lista_sol = ['lbfgs', 'sgd', 'adam']
            self.solver_v.set('adam')
            Label(self, text='Solver:', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=120)
            ttk.Combobox(self, values=lista_sol, textvariable=self.solver_v, width=25, font='Arial 12', justify=CENTER, state='readonly').place(x=340, y=145)

            self.alpha_v = StringVar()
            self.alpha_v.set('0.0001')
            Label(self, text='Alpha:', font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=180)
            Entry(self, textvariable=self.alpha_v, width=27, font='Arial 12', justify=CENTER).place(x=50, y=205)

            self.batch_size_v = StringVar()
            self.batch_size_v.set('auto')
            Label(self, text='Batch_size (int / "auto"):', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=180)
            Entry(self, textvariable=self.batch_size_v, width=27, font='Arial 12', justify=CENTER).place(x=340, y=205)

            self.learning_rate_v = StringVar()
            lista_learn = ['constant', 'invscaling', 'adaptive']
            self.learning_rate_v.set('constant')
            Label(self, text="Learning_rate:", font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=240)
            ttk.Combobox(self, values=lista_learn, textvariable=self.learning_rate_v, width=25, font='Arial 12', justify=CENTER, state='readonly').place(x=50, y=265)

            self.learning_rate_init_v = StringVar()
            self.learning_rate_init_v.set('0.001')
            Label(self, text='Learning_rate_init (float):', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=240)
            Entry(self, textvariable=self.learning_rate_init_v, width=27, font='Arial 12', justify=CENTER).place(x=340, y=265)

            self.power_t_v = StringVar()
            self.power_t_v.set('0.5')
            Label(self, text='Power_t (float):', font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=300)
            Entry(self, textvariable=self.power_t_v, width=27, font='Arial 12', justify=CENTER).place(x=50, y=325)

            self.max_iter_v = StringVar()
            self.max_iter_v.set('200')
            Label(self, text='Max_iter (int):', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=300)
            Entry(self, textvariable=self.max_iter_v, width=27, font='Arial 12', justify=CENTER).place(x=340, y=325)


            self.shuffle_v = BooleanVar()
            self.shuffle_v.set(True)
            Label(self, text='Shuffle (bool 1/0):', font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=360)
            Entry(self, textvariable=self.shuffle_v, width=27, font='Arial 12', justify=CENTER).place(x=50, y=385)

            self.tol_v = StringVar()
            self.tol_v.set('0.0001')
            Label(self, text='Tol (float):', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=360)
            Entry(self, textvariable=self.tol_v, width=27, font='Arial 12', justify=CENTER).place(x=340, y=385)

            self.verbose_v = BooleanVar()
            self.verbose_v.set(False)
            Label(self, text='Verbose (bool 1/0):', font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=420)
            Entry(self, textvariable=self.verbose_v, width=27, font='Arial 12', justify=CENTER).place(x=50, y=445)

            self.warm_start_v = BooleanVar()
            self.warm_start_v.set(False)
            Label(self, text='Warm_start (bool 1/0):', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=420)
            Entry(self, textvariable=self.warm_start_v, width=27, font='Arial 12', justify=CENTER).place(x=340, y=445)

            self.momentum_v = StringVar()
            self.momentum_v.set('0.9')
            Label(self, text='Momentum (float):', font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=480)
            Entry(self, textvariable=self.momentum_v, width=27, font='Arial 12', justify=CENTER).place(x=50, y=505)

            self.nesterovs_momentum_v = BooleanVar()
            self.nesterovs_momentum_v.set(True)
            Label(self, text='Nesterovs_momentum:', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=480)
            Entry(self, textvariable=self.nesterovs_momentum_v, width=27, font='Arial 12', justify=CENTER).place(x=340, y=505)

            self.early_stopping_v = BooleanVar()
            self.early_stopping_v.set(False)
            Label(self, text='Early_stopping:', font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=540)
            Entry(self, textvariable=self.early_stopping_v, width=27, font='Arial 12', justify=CENTER).place(x=50, y=565)

            self.validation_fraction_v = StringVar()
            self.validation_fraction_v.set('0.1')
            Label(self, text='Validation_fraction (float):', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=540)
            Entry(self, textvariable=self.validation_fraction_v, width=27, font='Arial 12', justify=CENTER).place(x=340, y=565)

            self.beta_1_v = StringVar()
            self.beta_1_v.set('0.9')
            Label(self, text='Beta_1 (float):', font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=600)
            Entry(self, textvariable=self.beta_1_v, width=27, font='Arial 12', justify=CENTER).place(x=50, y=625)

            self.beta_2_v = StringVar()
            self.beta_2_v.set('0.999')
            Label(self, text='Beta_2 (float):', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=600)
            Entry(self, textvariable=self.beta_2_v, width=27, font='Arial 12', justify=CENTER).place(x=340, y=625)

            self.n_iter_no_change_v = StringVar()
            self.n_iter_no_change_v.set('10')
            Label(self, text='N_iter_no_change (int):', font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=660)
            Entry(self, textvariable=self.n_iter_no_change_v, width=27, font='Arial 12', justify=CENTER).place(x=50, y=685)

            self.max_fun_v = StringVar()
            self.max_fun_v.set('15000')
            Label(self, text='max_fun (int):', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=660)
            Entry(self, textvariable=self.max_fun_v, width=27, font='Arial 12', justify=CENTER).place(x=340, y=685)

            '''   data   '''
            self.lbf_dt_nn = LabelFrame(self, text='Dados', width=600, height=170, font='Arial 12 bold', fg ='white', bg=fundo).place(x=20, y=730)

            self.data_s = StringVar()
            self.data_s.set('Cidade alvo')
            lista_dt = ['Cidade alvo', 'Vizinha A', 'Vizinha B', 'Vizinha C']
            Label(self, text="Dados para treinamento:", font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=750)
            self.combo_c = ttk.Combobox(self, values=lista_dt, textvariable=self.data_s, width=25, font='Arial 12', justify=CENTER, state='readonly').place(x=50, y=775)

            self.ind_s = StringVar()
            self.ind_s.set('Temperatura máxima')
            lista_ind = ['Precipitação', 'Temperatura máxima', 'Temperatura mínima']
            Label(self, text='Indicador:', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=750)
            ttk.Combobox(self, values=lista_ind, textvariable=self.ind_s, width=25, font='Arial 12', justify=CENTER, state='readonly').place(x=340, y=775)

            self.por_trei = IntVar()
            self.por_trei.set(70)
            Label(self, text="Porção para treinamento:", font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=810)
            Scale(self, variable=self.por_trei, orient=HORIZONTAL, length=240).place(x=50, y=835)
        
            self.num_teste = IntVar()
            self.num_teste.set(5)
            Label(self, text="Número de testes (int):", font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=810)
            self.ent_num_teste = Entry(self, textvariable=self.num_teste, width=27, font='Arial 12', justify=CENTER).place(x=340, y=835)

            Button(self, text='Preview', font='Arial 11 bold', fg='white', bg=fun_b, width=25, command=self.gerar_preview_nn).place(x=50, y=915)
            self.save_model = IntVar()
            Checkbutton(self, text='Salvar modelo', variable=self.save_model, bg=fundo, font='Arial 12 bold', activebackground=fundo).place(x=340, y=915)
        elif opcao == 'Nearest Neighbors':

           w = Canvas(self, width=615, height=900, background=fundo, border=0)
           w.place(x=10, y=95)
           

           self.lbf_para_nn = LabelFrame(self, text='Parâmetros', width=600, height=205, font='Arial 12 bold', fg='white', bg=fundo).place(x=20, y=100) 

           self.n_neighbors_v = IntVar()
           self.n_neighbors_v.set(5)
           Label(self, text='N_neighbors (int):', font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=120)
           Entry(self, textvariable=self.n_neighbors_v, width=27, font='Arial 12', justify=CENTER).place(x=50, y=145)

           self.algorithm_v = StringVar()
           lista_alg = ['auto', 'ball_tree', 'kd_tree', 'brute']
           self.algorithm_v.set('auto')
           Label(self, text='Algorithm:', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=120)
           ttk.Combobox(self, values=lista_alg, textvariable=self.algorithm_v, width=25, font='Arial 12', justify=CENTER, state='readonly').place(x=340, y=145)

           self.leaf_size_v = IntVar()
           self.leaf_size_v.set(30)
           Label(self, text='Leaf_size (int):', font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=180)
           Entry(self, textvariable=self.leaf_size_v, width=27, font='Arial 12', justify=CENTER).place(x=50, y=205)

           self.p_v = IntVar()
           self.p_v.set(2)
           Label(self, text='P (int):', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=180)
           Entry(self, textvariable=self.p_v, width=27, font='Arial 12', justify=CENTER).place(x=340, y=205)

           self.n_jobs_v = StringVar()
           self.n_jobs_v.set('5')
           Label(self, text='N_jobs (int / "None"):', font='Aria 12 bold', fg='white', bg=fundo).place(x=50, y=240)
           Entry(self, textvariable=self.n_jobs_v, width=27, font='Arial 12', justify=CENTER).place(x=50, y=265)

           self.lbf_d = LabelFrame(self, text='Dados', width=600, height=170, font='Arial 12 bold', fg ='white', bg=fundo).place(x=20, y=320)

           self.data_s = StringVar()
           self.data_s.set('Cidade alvo')
           lista_dt = ['Cidade alvo', 'Vizinha A', 'Vizinha B', 'Vizinha C']
           Label(self, text="Dados para treinamento:", font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=340)
           self.combo_c = ttk.Combobox(self, values=lista_dt, textvariable=self.data_s, width=25, font='Arial 12', justify=CENTER, state='readonly').place(x=50, y=365)

           self.ind_s = StringVar()
           self.ind_s.set('Temperatura máxima')
           lista_ind = ['Precipitação', 'Temperatura máxima', 'Temperatura mínima']
           Label(self, text='Indicador:', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=340)
           ttk.Combobox(self, values=lista_ind, textvariable=self.ind_s, width=25, font='Arial 12', justify=CENTER, state='readonly').place(x=340, y=365)

           self.por_trei = IntVar()
           self.por_trei.set(70)
           Label(self, text="Porção para treinamento:", font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=400)
           Scale(self, variable=self.por_trei, orient=HORIZONTAL, length=240).place(x=50, y=425)

           self.num_teste = IntVar()
           self.num_teste.set(5)
           Label(self, text="Número de testes (int):", font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=400)
           self.ent_num_teste = Entry(self, textvariable=self.num_teste, width=27, font='Arial 12', justify=CENTER).place(x=340, y=425)

           Button(self, text='Preview', font='Arial 11 bold', fg='white', bg=fun_b, width=25, command=self.gerar_preview_Kn).place(x=50, y=505)
           self.save_model = IntVar()
           Checkbutton(self, text='Salvar modelo', variable=self.save_model, bg=fundo, font='Arial 12 bold', activebackground=fundo).place(x=340, y=505) 
        elif opcao == 'Support Vector':
            w = Canvas(self, width=615, height=900, background=fundo, border=0)
            w.place(x=10, y=95)
            self.lbf_para_nn = LabelFrame(self, text='Parâmetros', width=600, height=385, font='Arial 12 bold', fg='white', bg=fundo).place(x=20, y=100)
            
            self.kernel_v = StringVar()
            lista_ker = ['linear', 'poly', 'rbf', 'sigmoid']
            self.kernel_v.set('rbf')
            Label(self, text='Kernel:', font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=120)
            ttk.Combobox(self, values=lista_ker, textvariable=self.kernel_v, width=25, font='Arial 12', justify=CENTER, state='readonly').place(x=50, y=145)

            self.degree_v = IntVar()
            self.degree_v.set(3)
            Label(self, text='Degree (int):', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=120)
            Entry(self, textvariable=self.degree_v, font='Arial 12', width=27, justify=CENTER).place(x=340, y=145) 

            self.gamma_v = StringVar()
            self.gamma_v.set('scale')
            Label(self, text='Gamma ("scale", "auto", float):', font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=180)
            Entry(self, textvariable=self.gamma_v, font='Arial 12', width=27, justify=CENTER).place(x=50, y=205)

            self.coef0_v = StringVar()
            self.coef0_v.set('0.0')
            Label(self, text='Coef0 (float):', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=180)
            Entry(self, textvariable=self.coef0_v, font='Arial 12', width=27, justify=CENTER).place(x=340, y=205)

            self.tol_v = StringVar()
            self.tol_v.set('0.001')
            Label(self, text='Tol (float):', font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=240)
            Entry(self, textvariable=self.tol_v, font='Arial 12', width=27, justify=CENTER).place(x=50, y=265)

            self.c_v = StringVar()
            self.c_v.set('1.0')
            Label(self, text='C (float):', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=240)
            Entry(self, textvariable=self.c_v, font='Arial 12', width=27, justify=CENTER).place(x=340, y=265)

            self.epsilon_v = StringVar()
            self.epsilon_v.set('0.1')
            Label(self, text='Epsilon (float):', font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=300)
            Entry(self, textvariable=self.epsilon_v, font='Arial 12', width=27, justify=CENTER).place(x=50, y=325)   

            self.shrinking_v = BooleanVar()
            self.shrinking_v.set(True)
            Label(self, text='Shrinking (Bool):', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=300)
            Entry(self, textvariable=self.shrinking_v, font='Arial 12', width=27, justify=CENTER).place(x=340, y=325)

            self.cache_size_v = StringVar()
            self.cache_size_v.set('200')
            Label(self, text='Cache_size (float):', font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=360)
            Entry(self, textvariable=self.cache_size_v, font='Arial 12', width=27, justify=CENTER).place(x=50, y=385)   

            self.verbose_v = BooleanVar()
            self.verbose_v.set(False)
            Label(self, text='Verbose (Bool):', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=360)
            Entry(self, textvariable=self.verbose_v, font='Arial 12', width=27, justify=CENTER).place(x=340, y=385)

            self.maxiter_v = IntVar()
            self.maxiter_v.set(-1)
            Label(self, text='Max_iter (int):', font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=420)
            Entry(self, textvariable=self.maxiter_v, font='Arial 12', width=27, justify=CENTER).place(x=50, y=445)

            self.lbf_dt_nn = LabelFrame(self, text='Dados', width=600, height=170, font='Arial 12 bold', fg ='white', bg=fundo).place(x=20, y=500)

            self.data_s = StringVar()
            self.data_s.set('Cidade alvo')
            lista_dt = ['Cidade alvo', 'Vizinha A', 'Vizinha B', 'Vizinha C']
            Label(self, text="Dados para treinamento:", font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=520)
            self.combo_c = ttk.Combobox(self, values=lista_dt, textvariable=self.data_s, width=25, font='Arial 12', justify=CENTER, state='readonly').place(x=50, y=545)

            self.ind_s = StringVar()
            self.ind_s.set('Temperatura máxima')
            lista_ind = ['Precipitação', 'Temperatura máxima', 'Temperatura mínima']
            Label(self, text='Indicador:', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=520)
            ttk.Combobox(self, values=lista_ind, textvariable=self.ind_s, width=25, font='Arial 12', justify=CENTER, state='readonly').place(x=340, y=545)

            self.por_trei = IntVar()
            self.por_trei.set(70)
            Label(self, text="Porção para treinamento:", font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=580)
            Scale(self, variable=self.por_trei, orient=HORIZONTAL, length=240).place(x=50, y=605)
        
            self.num_teste = IntVar()
            self.num_teste.set(5)
            Label(self, text="Número de testes (int):", font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=580)
            self.ent_num_teste = Entry(self, textvariable=self.num_teste, width=27, font='Arial 12', justify=CENTER).place(x=340, y=605)

            Button(self, text='Preview', font='Arial 11 bold', fg='white', bg=fun_b, width=25, command=self.gerar_preview_svm).place(x=50, y=680)
            self.save_model = IntVar()
            Checkbutton(self, text='Salvar modelo', variable=self.save_model, bg=fundo, font='Arial 12 bold', activebackground=fundo).place(x=340, y=680)
        elif opcao == 'Gaussian Process':
            w = Canvas(self, width=615, height=900, background=fundo, border=0)
            w.place(x=10, y=95)
            self.lbf_para_nn = LabelFrame(self, text='Parâmetros', width=600, height=205, font='Arial 12 bold', fg='white', bg=fundo).place(x=20, y=100)
            
            self.alpha_gp = StringVar()
            self.alpha_gp.set('0.0000000001')
            Label(self, text='Alpha (float): ', font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=120)
            Entry(self, textvariable=self.alpha_gp, font='Arial 12', width=27, justify=CENTER).place(x=50, y=145)
            
            self.n_restarts_op = IntVar()
            self.n_restarts_op.set(0)
            Label(self, text='N_restart_optimizer (int):', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=120)
            Entry(self, textvariable=self.n_restarts_op, font='Arial 12', width=27, justify=CENTER).place(x=340, y=145)

            self.normalize_y_gp = BooleanVar()
            self.normalize_y_gp.set(0)
            Label(self, text='Normalize_y (Bool 1/0):', font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=180)
            Entry(self, textvariable=self.normalize_y_gp, font='Arial 12', width=27, justify=CENTER).place(x=50, y=205)

            self.copy_X_train = BooleanVar()
            self.copy_X_train.set(0)
            Label(self, text='Copy_X_train (Bool 1/0):', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=180)
            Entry(self, textvariable=self.copy_X_train, font='Arial 12', width=27, justify=CENTER).place(x=340, y=205)

            self.rand_state_gp = StringVar()
            self.rand_state_gp.set('None')
            Label(self, text='Random_state ("None" / int):', font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=240)
            Entry(self, textvariable=self.rand_state_gp, font='Arial 12', width=27, justify=CENTER).place(x=50, y=265)
            

            self.lbf_dt_nn = LabelFrame(self, text='Dados', width=600, height=170, font='Arial 12 bold', fg ='white', bg=fundo).place(x=20, y=320)

            self.data_s = StringVar()
            self.data_s.set('Cidade alvo')
            lista_dt = ['Cidade alvo', 'Vizinha A', 'Vizinha B', 'Vizinha C']
            Label(self, text="Dados para treinamento:", font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=340)
            self.combo_c = ttk.Combobox(self, values=lista_dt, textvariable=self.data_s, width=25, font='Arial 12', justify=CENTER, state='readonly').place(x=50, y=365)

            self.ind_s = StringVar()
            self.ind_s.set('Temperatura máxima')
            lista_ind = ['Precipitação', 'Temperatura máxima', 'Temperatura mínima']
            Label(self, text='Indicador:', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=340)
            ttk.Combobox(self, values=lista_ind, textvariable=self.ind_s, width=25, font='Arial 12', justify=CENTER, state='readonly').place(x=340, y=365)

            self.por_trei = IntVar()
            self.por_trei.set(70)
            Label(self, text="Porção para treinamento:", font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=400)
            Scale(self, variable=self.por_trei, orient=HORIZONTAL, length=240).place(x=50, y=425)
        
            self.num_teste = IntVar()
            self.num_teste.set(5)
            Label(self, text="Número de testes (int):", font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=400)
            self.ent_num_teste = Entry(self, textvariable=self.num_teste, width=27, font='Arial 12', justify=CENTER).place(x=340, y=425)

            Button(self, text='Preview', font='Arial 11 bold', fg='white', bg=fun_b, width=25, command=self.gerar_preview_svm).place(x=50, y=505)
            self.save_model = IntVar()
            Checkbutton(self, text='Salvar modelo', variable=self.save_model, bg=fundo, font='Arial 12 bold', activebackground=fundo).place(x=340, y=505)

    def __init__(self, master=None):
        Toplevel.__init__(self, master=master)
        self.title('Aprendizado de máquina')
        self.geometry('800x800')
        self.configure(background=fundo)

        Label(self, text='APRENDIZADO DE MÁQUINA', font='Arial 14 bold', fg='white', bg=fundo).place(x=200, y=20)

        self.ml_selected = StringVar()
        self.ml_selected.set('Decision Trees')
        lista_ml = ['Decision Trees', 'Neural network', 'Nearest Neighbors', 'Support Vector', 'Gaussian Process']
        ttk.Combobox(self, values=lista_ml, textvariable=self.ml_selected, width=28, font='Arial 12', justify=CENTER, state='readonly').place(x=20, y=60)
        Button(self, text='Escolher Machine Learning', font='Arial 11 bold', fg='white', bg=fun_ap, width=30, command=self.gera_param).place(x=340, y=59)

class MetaLearning(Toplevel):
    def gerar_teste_perso(self):
        base = self.ml_lv0_p.get()
        tria = self.ml_tr0_p.get()
        meta = self.ml_lv1.get()
        ind = self.ind_meta_perso.get()
        n_teste = int(self.num_teste_mtp.get())
        pre0 = int(self.pre_para_lv0.get())
        pre1 = int(self.pre_para_lv1.get())
        janela = self.type_input.get()
        if ind == 'Precipitação':
            foco = 1
        elif ind == 'Temperatura máxima':
            foco = 2
        elif ind == 'Temperatura mínima':
            foco = 3
        mp = MetaL()
        meta_ea, meta_er, meta_porc_erro, meta_r2, x_meta, y_meta, y_alvo, base_ea, base_er, base_porc, base_r2, tria_ea, tria_er = mp.meta_learning_personalizado(foco, base, tria, meta, 0, 0, n_teste, janela)
        
        
        LabelFrame(self, text='PREVIEW DOS RESULTADOS:', width=1250, height=950, font='Arial 12 bold', fg='white', bg=fundo).place(x=640, y=60)

        texto = "ERRO ABSOLUTO:    Machine Learning: " + str(round(base_ea, 4)) + "   ||   Triangulação: " + str(round(tria_ea,4)) + "   ||   Meta Learning: " + str(round(meta_ea,4))
        Label(self, text=texto, font='Arial 12 bold', fg='white', bg=fundo).place(x=660, y=90)
        
        texto = "ERRO RELATIVO:      Machine Learning: " + str(round(base_er, 4)) + "   ||   Triangulação: " + str(round(tria_er,4)) + "   ||   Meta Learning: " + str(round(meta_er,4))
        Label(self, text=texto, font='Arial 12 bold', fg='white', bg=fundo).place(x=660, y=130)
        
        texto = "ERRO(%):                     Machine Learning: " + str(round(base_porc, 4)) + "   ||   Triangulação: " + str(round(tria_ea*100,4)) +  "   ||   Meta Learning: " + str(round(meta_porc_erro,4))
        Label(self, text=texto, font='Arial 12 bold', fg='white', bg=fundo).place(x=660, y=170)
        
        texto = "R2:                                  Machine Learning: " + str(round(base_r2, 4)) +  "   ||   Meta Learning: " + str(round(meta_r2,4))
        Label(self, text=texto, font='Arial 12 bold', fg='white', bg=fundo).place(x=660, y=210)

        figura = Figure(figsize=(12.3, 7.5), dpi=100)
        plot1 = figura.add_subplot(2,2,1)
        x_ea = ["MacL", 'Trian', 'Meta']
        y_ea = [base_ea, tria_ea, meta_ea]
        plot1.bar(x_ea, y_ea)
        plot1.set_ylabel("Erro Absoluto")
        
        plot2 = figura.add_subplot(2,2,2)
        x_er = ["MacL", 'Trian', 'Meta']
        y_er = [base_er, tria_er, meta_er]
        plot2.bar(x_er, y_er)
        plot2.set_ylabel("Erro Relativo")

        plot3 = figura.add_subplot(2,2,3)
        x_por = ["MacL", 'Trian','Meta']
        y_por = [base_porc, tria_ea*100,meta_porc_erro]
        plot3.bar(x_por, y_por)
        plot3.set_ylabel("Erro (%)")

        plot4 = figura.add_subplot(2,2,4)
        x_r2 = ["MacL", 'Meta']
        y_r2 = [base_r2, meta_r2]
        plot4.bar(x_r2, y_r2)
        plot4.set_ylabel("R2")

        canvas = FigureCanvasTkAgg(figura, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack()
        canvas.get_tk_widget().place(x=650, y=250)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.place(x=1150, y=10)
        toolbar.update()

    def gerar_teste_global(self):
      
        foco = self.ind_meta_comb.get()
        num_t = int(self.num_teste_mtc.get())
        janela = 'Sim'
        
        mc = MetaL()
        
        todos, ranking = mc.meta_learning_combina(foco, 0, 0, num_t, janela)
        
        
        LabelFrame(self, text='RESULTADOS:', width=1260, height=950, font='Arial 12 bold', fg='white', bg=fundo).place(x=640,y=60)

        Label(self, text='Modelos gerados:', font='Arial 12 bold', fg='white', bg=fundo).place(x=660, y=90)
                
        dados_todos = list()
        for i in range(len(todos)):
            buff = list()
            buff.append(todos[i][0])
            buff.append(todos[i][1])
            buff.append(todos[i][2])
            buff.append(todos[i][3])
            buff.append(todos[i][5])
            buff.append(todos[i][6])
            buff.append(todos[i][7])
            dados_todos.append(buff)

        self.tabela_todos = Sheet(self, data=dados_todos, headers=['Modelo','Base Learning', 'Triangulation', 'Meta Learning', 'Erro Absoluto', 'Erro Relativo', 'Erro(%)'], width=890, height=500)
        self.tabela_todos.enable_bindings()
        self.tabela_todos.place(x=660, y=120)
        

        Label(self, text='Ranking dos modelos:', font='Arial 12 bold', fg='white', bg=fundo).place(x=1580, y=90)

        dados_ranking = list()
        x = list()
        y = list()
        for i in range(len(ranking)):
            buff = list()
            buff.append(ranking[i][0])
            buff.append(round(float(ranking[i][1].replace(',', '.')), 4))  
            dados_ranking.append(buff)

            if i <= 15:
                x.append(str(ranking[i][0]))
                y.append(float(ranking[i][1].replace(',', '.')))

        
        self.tabela_ranking = Sheet(self, data=dados_ranking, headers=['Modelo', 'Erro'], width=270, height=500, column_width=115)
        self.tabela_ranking.enable_bindings()
        self.tabela_ranking.place(x=1580, y=120)   

        figura = Figure(figsize=(12, 3.3), dpi=100)
        plot = figura.add_subplot(1,1,1)

        plot.bar(x, y)
        plot.set_ylabel('Erro(%)')
        plot.set_xlabel("Modelos")
        plot.grid(True)
        
        canvas = FigureCanvasTkAgg(figura, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack()
        canvas.get_tk_widget().place(x=660, y=650)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.place(x=1150, y=10)
        toolbar.update()
     
    def __init__(self, master=None):
        Toplevel.__init__(self, master=master)
        self.title('Meta Learning')
        self.geometry("800x800")

        self.configure(background=fundo)

        Label(self, text='META-LEARNING', font='Arial 14 bold', fg='white', bg=fundo).place(x=240, y=20)

        LabelFrame(self, text='TESTE PERSONALIZADO:', width=600, height=450, font='Arial 12 bold', fg='white', bg=fundo).place(x=20, y=60)

        Label(self, text='Base-Learning (Level 0):', font='Arial 12 bold', fg='white', bg=fundo).place(x=40, y=90)
        self.ml_lv0_p = StringVar()
        self.ml_lv0_p.set('Decision Trees')
        lista_ml0 =  ['Nenhum','Decision Trees', 'Neural network', 'Nearest Neighbors', 'Support Vector', 'Gaussian Process']
        ttk.Combobox(self, values=lista_ml0, textvariable=self.ml_lv0_p, width=30, font='Arial 11', justify=CENTER, state='readonly').place(x=40, y=120)

        Label(self, text='Triangulation (Level 0):', font='Arial 12 bold', fg='white', bg=fundo).place(x=40, y=190)
        self.ml_tr0_p = StringVar()
        self.ml_tr0_p.set('Arithmetic Average')
        lista_tr0 =  ['Nenhum', 'Arithmetic Average', 'Inverse Distance Weighted', 'Regional Weight', 'Optimized Normal Ratio']
        ttk.Combobox(self, values=lista_tr0, textvariable=self.ml_tr0_p, width=30, font='Arial 11', justify=CENTER, state='readonly').place(x=40, y=220)

        Label(self, text='Meta-Learning (Level 1):', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=145)
        self.ml_lv1 = StringVar()
        self.ml_lv1.set('Decision Trees')
        lista_ml1 =  ['Decision Trees', 'Neural network', 'Nearest Neighbors', 'Support Vector', 'Gaussian Process']
        ttk.Combobox(self, values=lista_ml1, textvariable=self.ml_lv1, width=30, font='Arial 11', justify=CENTER, state='readonly').place(x=340, y=175)

        Label(self, text='Indicador climático:', font='Arial 12 bold', fg='white', bg=fundo).place(x=40, y=270)
        self.ind_meta_perso = StringVar()
        self.ind_meta_perso.set('Temperatura máxima')
        lista_ind_meta_p = ['Precipitação', 'Temperatura máxima', 'Temperatura mínima']
        ttk.Combobox(self, values=lista_ind_meta_p, textvariable=self.ind_meta_perso, width=30, font='Arial 11', justify=CENTER, state='readonly').place(x=40, y=300)

        self.num_teste_mtp = IntVar()
        self.num_teste_mtp.set(1)
        Label(self, text="Número de testes (int):", font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=270)
        self.ent_num_teste = Entry(self, textvariable=self.num_teste_mtp, width=29, font='Arial 12', justify=CENTER).place(x=340, y=300)

        Label(self, text='Deseja usar alguma ML pré-parametrizada?', font='Arial 12 bold', fg='white', bg=fundo).place(x=40, y=340)
        self.pre_para_lv0 = IntVar()
        self.pre_para_lv1 = IntVar()
        Checkbutton(self, text='Level 0', variable=self.pre_para_lv0, bg=fundo, font='Arial 12 bold', activebackground=fundo).place(x=40, y=360)
        Checkbutton(self, text='Level 1', variable=self.pre_para_lv1, bg=fundo, font='Arial 12 bold', activebackground=fundo).place(x=180, y=360)
        
        Label(self, text='Deseja utilizar a janela deslizante?', font='Arial 12 bold', fg='White', bg=fundo).place(x=40, y=400)
        self.type_input = StringVar()
        self.type_input.set('Sim')
        lista_type_input = ['Sim', 'Não']
        ttk.Combobox(self, values=lista_type_input, textvariable=self.type_input, width=30, font='Arial 11', justify=CENTER, state='readonly').place(x=40, y=430)
        
        Button(self, text='Gerar Preview', font='Arial 11 bold', bg=fun_meta_le, fg='white', width=62, command=self.gerar_teste_perso).place(x=40, y=470)

        '''Teste global'''
        LabelFrame(self, text='TESTE GLOBAL:', width=600, height=210, font='Arial 12 bold', fg='white', bg=fundo).place(x=20, y=520)
        
        Label(self, text='Quais MLs você deseja utilizar?', font='Arial 12 bold', fg='white', bg=fundo).place(x=40, y=550)

        self.pre_nn_comb = IntVar()
        self.pre_dt_comb = IntVar()
        self.pre_nneig_comb = IntVar()
        self.pre_sv_comb = IntVar()
        self.pre_gp_comb = IntVar()
        Checkbutton(self, text='NN', variable=self.pre_nn_comb, bg=fundo, font='Arial 12 bold', activebackground=fundo).place(x=40, y=580)
        Checkbutton(self, text='DT', variable=self.pre_dt_comb, bg=fundo, font='Arial 12 bold', activebackground=fundo).place(x=140, y=580)
        Checkbutton(self, text='NNeig.', variable=self.pre_nneig_comb, bg=fundo, font='Arial 12 bold', activebackground=fundo).place(x=240, y=580)
        Checkbutton(self, text='SV', variable=self.pre_sv_comb, bg=fundo, font='Arial 12 bold', activebackground=fundo).place(x=340, y=580)
        Checkbutton(self, text='GP', variable=self.pre_gp_comb, bg=fundo, font='Arial 12 bold', activebackground=fundo).place(x=440, y=580)
        
        Label(self, text='Indicador climático:', font='Arial 12 bold', fg='white', bg=fundo).place(x=40, y=620)
        self.ind_meta_comb = StringVar()
        self.ind_meta_comb.set('Temperatura máxima')
        lista_ind_meta_p = ['Precipitação', 'Temperatura máxima', 'Temperatura mínima']
        ttk.Combobox(self, values=lista_ind_meta_p, textvariable=self.ind_meta_comb, width=30, font='Arial 11', justify=CENTER, state='readonly').place(x=40, y=650)

        self.num_teste_mtc = IntVar()
        self.num_teste_mtc.set(1)
        Label(self, text="Número de testes (int):", font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=620)
        self.ent_num_teste = Entry(self, textvariable=self.num_teste_mtc, width=29, font='Arial 12', justify=CENTER).place(x=340, y=650)
        
        Button(self, text='Gerar Preview TG', font='Arial 11 bold', bg=fun_meta_le, fg='white', width=62, command=self.gerar_teste_global).place(x=40, y=690)

        #Aviso
        LabelFrame(self, text='ATENÇÃO:', width=600, height=120, font='Arial 12 bold', fg='white', bg=fundo).place(x=20, y=740)
        Label(self, text='Dependendo da combinação feita no "Teste Personalizado" ou no "TESTE ', font='Arial 12 bold', fg='#FF8C00', bg=fundo).place(x=40, y=770)
        Label(self, text='GLOBAL", pode demorar alguns minutos, devido ao processamento.', font='Arial 12 bold', fg='#FF8C00', bg=fundo).place(x=40, y=790)
        Label(self, text='Fique à vontade para utilizar seu computador para fazer outras coisas.', font='Arial 12 bold', fg='#FF8C00', bg=fundo).place(x=40, y=820)


class Principal(Frame):
    def get_info(self,diretorio):       #Função que abre a pasta, onde se encontra todos os arquivos .csv e retorna dados importantes
        arq = open(diretorio, 'r')
        dados_brutos = list()
        
        for i in arq:
            texto = i.replace('\n', '')
            dados_brutos.append(texto)
        del dados_brutos[len(dados_brutos)-1]

        arq.close()

        nome = dados_brutos[0][6:]
        lat = float(dados_brutos[2][10:])
        lon = float(dados_brutos[3][10:])
        alt = float(dados_brutos[4][10:])
        endereco = diretorio
        return nome, lat, lon, alt, endereco

    def listar_cidades(self):
        local_bd = dlg.askdirectory()
        
        lista_nome_arq = os.listdir(local_bd) #O usuário vai selecionar o local onde está os dados
        lista_end_arq = list()

        for i in lista_nome_arq:
            lista_end_arq.append(local_bd + '/' +i)

        self.lista_todas_est = list()
        self.list_end = list()         #Lista com o nome das cidades e o diretorio
        for i in lista_end_arq:
            nome, lat, lon, alt, endereco = self.get_info(i)
            self.lista_todas_est.append(nome)
            self.list_end.append([nome, endereco])

        self.lista_todas_est.sort()
        self.cidade_alvo = StringVar()
        Label(self, text='Cidade Alvo:', font='Arial 11 bold', bg=fundo, fg='white').place(x=20, y=65)
        self.comb_alvo = ttk.Combobox(self, values=self.lista_todas_est, textvariable=self.cidade_alvo, width=20, font='Arial 11', justify=CENTER, state='normal').place(x=20, y=85)

        self.cidade_va = StringVar()
        Label(self, text='Vizinha A:', font='Arial 11 bold', bg=fundo, fg='white').place(x=220, y=65)
        self.comb_va = ttk.Combobox(self, values=self.lista_todas_est, textvariable=self.cidade_va, width=20, font='Arial 11', justify=CENTER, state='readonly').place(x=224, y=85)

        self.cidade_vb = StringVar()
        Label(self, text='Vizinha B:', font='Arial 11 bold', bg=fundo, fg='white').place(x=20, y=115)
        self.comb_vb = ttk.Combobox(self, values=self.lista_todas_est, textvariable=self.cidade_vb, width=20, font='Arial 11', justify=CENTER, state='readonly').place(x=20, y=135)

        self.cidade_vc = StringVar()
        Label(self, text='Vizinha C:', font='Arial 11 bold', bg=fundo, fg='white').place(x=220, y=115)
        self.comb_vc = ttk.Combobox(self, values=self.lista_todas_est, textvariable=self.cidade_vc, width=20, font='Arial 11', justify=CENTER, state='readonly').place(x=224, y=135)

        Button(self, text='Confirmar Grupo', font='Arial 12 bold', fg='white', bg=fun_b, width=38, command=self.tratar).place(x=20, y=170)

    def tratar(self):
        if self.cidade_alvo.get() == '' or self.cidade_va.get() == '' or self.cidade_vb.get() == '' or self.cidade_vc.get() == '':
            msg.showerror(title='Dados Incompletos', message="Alguma(s) cidade(s) não foi(foram) selecionada(s)")
            return

        self.hist_cididade = [self.cidade_alvo.get(), self.cidade_va.get(),self.cidade_vb.get(), self.cidade_vc.get()]
        self.cid_hist = StringVar()
        

        ind_tg = ''
        for i in self.list_end:
            if i[0] == self.cidade_alvo.get():
                ind_tg = i[1]
                break

        ind_va = ''
        for i in self.list_end:
            if i[0] == self.cidade_va.get():
                ind_va = i[1]
                break

        ind_vb = ''
        for i in self.list_end:
            if i[0] == self.cidade_vb.get():
                ind_vb = i[1]
                break

        ind_vc = ''
        for i in self.list_end:
            if i[0] == self.cidade_vc.get():
                ind_vc = i[1]
                break
      
        datat = Tratamento()
        #save = dlg.askdirectory()
        datat.alvo = ind_tg
        datat.vizinhaA = ind_va
        datat.vizinhaB = ind_vb
        datat.vizinhaC = ind_vc
        #datat.download = save
        datat.download = os.getcwd()
        self.local_save = os.getcwd()
        datat.get_data_trada()
        msg.showinfo(title="Sucesso!", message="Arquivos Selecionados com sucesso!")
    
    def get_col(self):
        if self.parameter.get() == "Precipitação":
            y_name = "Precipitação (mm)"
            col = 3
        elif self.parameter.get() == "Temperatura máxima":
            col = 4
            y_name = "Temperatura (°C)"
        elif self.parameter.get() == "Temperatura mínima":
            y_name = "Temperatura (°C)"
            col = 5
        return y_name, col

    def graficos_comum(self):
        my_data = Tratamento()
        data_ana = my_data.retorna_arq(self.type_data.get())
        
        self.gera_range()

        nome_y, col = self.get_col()

        eixo_x = list()
        if self.type_data.get() == 'Dados comum':
            eixo_y1 = list()
            eixo_y2 = list()
            eixo_y3 = list()
            eixo_y4 = list()
            util, tar,t_va, t_vb, t_vc = my_data.get_qtd()
            eixo_y_bar = [util, tar,t_va, t_vb, t_vc]
            eixo_x_bar = ['Comum', 'Alvo','Total vA', 'Total vB', 'Total vC']
        else:
            eixo_y = list()

    
        dados_lb = list()
        for i in data_ana:
            dados_lb.append(i)

            ano = str(i[0])
            mes = str(i[1])
            dia = str(i[2])
            text_data = mes + '/' + dia + '/' + ano
            

            if self.type_data.get() == 'Dados comum':
                try:
                    
                    eixo_y1.append(float(i[col].replace(',', '.')))
                    eixo_y2.append(float(i[col+3].replace(',', '.')))
                    eixo_y3.append(float(i[col+6].replace(',', '.')))
                    eixo_y4.append(float(i[col+9].replace(',', '.')))
                    eixo_x.append(dt.datetime.strptime(text_data,"%m/%d/%Y").date())
                except ValueError:
                    pass
                
            else:
                try:
                    eixo_y.append(float(i[col]))
                    eixo_x.append(dt.datetime.strptime(text_data,"%m/%d/%Y").date())
                except ValueError:
                    pass
        
        #self.caixad_var.set(dados_lb)

        fig = Figure(figsize=(14.5,9.5), dpi=100)
        fig.subplots_adjust(left=0.05, bottom=0.08, right=0.98, top=0.93)

        if self.type_data.get() == 'Dados comum':
            plot1 = fig.add_subplot(321)
            plot2 = fig.add_subplot(322)
            plot3 = fig.add_subplot(323)
            plot4 = fig.add_subplot(324)
            plot5 = fig.add_subplot(325)
            plot6 = fig.add_subplot(326)
            plot1.plot(eixo_x, eixo_y1, label="Alvo")
            plot2.plot(eixo_x, eixo_y2, label="Viz A", color="red")
            plot3.plot(eixo_x, eixo_y3, label="Viz B", color='green')
            plot4.plot(eixo_x, eixo_y4, label="Viz C", color='orange')
            plot5.scatter(eixo_x, eixo_y1, s=2, alpha=1, color='blue')
            plot5.scatter(eixo_x, eixo_y2, s=2, alpha=1, color='red')
            plot5.scatter(eixo_x, eixo_y3, s=2, alpha=1, color='green')
            plot5.scatter(eixo_x, eixo_y4, s=2, alpha=1, color='orange')
            plot6.bar(eixo_x_bar, eixo_y_bar)
            plot1.set_xticklabels(eixo_x, rotation=15, ha='right')
            plot2.set_xticklabels(eixo_x, rotation=15, ha='right')
            plot3.set_xticklabels(eixo_x, rotation=15, ha='right')
            plot4.set_xticklabels(eixo_x, rotation=15, ha='right')
            plot5.set_xticklabels(eixo_x, rotation=15, ha='right')
            plot1.legend()
            plot2.legend()
            plot3.legend()
            plot4.legend()
            plot1.xaxis.set_major_formatter(mdates.DateFormatter("%m/%y")) 
            plot2.xaxis.set_major_formatter(mdates.DateFormatter("%m/%y")) 
            plot3.xaxis.set_major_formatter(mdates.DateFormatter("%m/%y")) 
            plot4.xaxis.set_major_formatter(mdates.DateFormatter("%m/%y")) 
            plot5.xaxis.set_major_formatter(mdates.DateFormatter("%m/%y")) 
            plot1.grid(True)
            plot2.grid(True)
            plot3.grid(True)
            plot4.grid(True)
            plot5.grid(True)
            plot1.set_ylabel(nome_y)
            plot2.set_ylabel(nome_y)
            plot3.set_ylabel(nome_y)
            plot4.set_ylabel(nome_y)
            plot5.set_ylabel(nome_y)
            plot6.set_ylabel('Qtd. de dados')
            
        else:
            plot1 = fig.add_subplot(111)
            plot1.plot(eixo_x, eixo_y)
            plot1.set_xticklabels(eixo_x, rotation=15, ha='right')
            plot1.xaxis.set_major_formatter(mdates.DateFormatter("%m/%y")) 
                
            plot1.grid(True)       
            plot1.set_ylabel(nome_y)
            plot1.set_title(self.parameter.get())
            
        canvas = FigureCanvasTkAgg(fig, master=self.master)
            
        canvas.draw()
        canvas.get_tk_widget().pack()
        canvas.get_tk_widget().place(x=450, y=57)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.place(x=1150, y=10)
        toolbar.update()

    def graficos_range(self):
        my_data = Tratamento()
        data_ana = my_data.retorna_arq(self.type_data.get())
        
        nome_y, col = self.get_col()

        ano_inicio = int(self.var_ini.get())
        ano_final = int(self.var_fim.get())
        if ano_final < ano_inicio:
            msg.showerror(title='Invalid', message='O range inserido é inválido')
            return
        if self.parameter.get() == 'Dados comum':
            self.grafico_dc(ano_inicio,ano_final)
            return
        
        eixo_x = list()
        if self.type_data.get() == 'Dados comum':
            eixo_y1 = list()
            eixo_y2 = list()
            eixo_y3 = list()
            eixo_y4 = list()
            util, tar,t_va, t_vb, t_vc = my_data.get_qtd()
            eixo_y_bar = [util, tar,t_va, t_vb, t_vc]
            eixo_x_bar = ['Comum', 'Alvo','Total vA', 'Total vB', 'Total vC']
        else:
            eixo_y = list()

        dados_lb = list()

        for i in data_ana:
            if int(i[0]) >= ano_inicio and int(i[0]) <= ano_final:
                dados_lb.append(i)

                ano = str(i[0])
                
                mes = str(i[1])
                dia = str(i[2])
                text_data = mes + '/' + dia + '/' + ano
                eixo_x.append(dt.datetime.strptime(text_data,"%m/%d/%Y").date())

                if self.type_data.get() == 'Dados comum':
                    eixo_y1.append(float(i[col]))
                    eixo_y2.append(float(i[col+3]))
                    eixo_y3.append(float(i[col+6]))
                    eixo_y4.append(float(i[col+9]))
                else:
                    eixo_y.append(float(i[col]))
        
        
        fig = Figure(figsize=(14.5,9.5), dpi=100)
        fig.subplots_adjust(left=0.05, bottom=0.08, right=0.98, top=0.93)

        if self.type_data.get() == 'Dados comum':
            plot1 = fig.add_subplot(321)
            plot2 = fig.add_subplot(322)
            plot3 = fig.add_subplot(323)
            plot4 = fig.add_subplot(324)
            plot5 = fig.add_subplot(325)
            plot6 = fig.add_subplot(326)
            plot1.plot(eixo_x, eixo_y1, label="Alvo")
            plot2.plot(eixo_x, eixo_y2, label="Viz A", color="red")
            plot3.plot(eixo_x, eixo_y3, label="Viz B", color='green')
            plot4.plot(eixo_x, eixo_y4, label="Viz C", color='orange')
            plot5.scatter(eixo_x, eixo_y1, s=2, alpha=1, color='blue')
            plot5.scatter(eixo_x, eixo_y2, s=2, alpha=0.6, color='red')
            plot5.scatter(eixo_x, eixo_y3, s=2, alpha=0.6, color='green')
            plot5.scatter(eixo_x, eixo_y4, s=2, alpha=0.6, color='orange')
            plot6.bar(eixo_x_bar, eixo_y_bar)
            plot1.set_xticklabels(eixo_x, rotation=15, ha='right')
            plot2.set_xticklabels(eixo_x, rotation=15, ha='right')
            plot3.set_xticklabels(eixo_x, rotation=15, ha='right')
            plot4.set_xticklabels(eixo_x, rotation=15, ha='right')
            plot5.set_xticklabels(eixo_x, rotation=15, ha='right')
            plot1.legend()
            plot2.legend()
            plot3.legend()
            plot4.legend()
            plot1.xaxis.set_major_formatter(mdates.DateFormatter("%m/%y")) 
            plot2.xaxis.set_major_formatter(mdates.DateFormatter("%m/%y")) 
            plot3.xaxis.set_major_formatter(mdates.DateFormatter("%m/%y")) 
            plot4.xaxis.set_major_formatter(mdates.DateFormatter("%m/%y")) 
            plot5.xaxis.set_major_formatter(mdates.DateFormatter("%m/%y")) 
            plot1.grid(True)
            plot2.grid(True)
            plot3.grid(True)
            plot4.grid(True)
            plot5.grid(True)
            plot1.set_ylabel(nome_y)
            plot2.set_ylabel(nome_y)
            plot3.set_ylabel(nome_y)
            plot4.set_ylabel(nome_y)
            plot5.set_ylabel(nome_y)
            plot6.set_ylabel('Qtd. de dados')
            
        else:
            plot1 = fig.add_subplot(111)
            plot1.plot(eixo_x, eixo_y)
            plot1.set_xticklabels(eixo_x, rotation=15, ha='right')   
            plot1.xaxis.set_major_formatter(mdates.DateFormatter("%m/%y"))   
                
            plot1.grid(True)
            plot1.set_ylabel(nome_y)
            plot1.set_title(self.parameter.get())
        canvas = FigureCanvasTkAgg(fig, master=self.master)
            
        canvas.draw()
        canvas.get_tk_widget().pack()
        canvas.get_tk_widget().place(x=450, y=57)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.place(x=1150, y=10)
        toolbar.update()
    
    def show_map(self):
        triang = Triangulaction()
        triang.show_map()

    def gera_range(self):
        teste = Tratamento()
        self.var_ini = StringVar()
        self.anos = teste.get_range(self.type_data.get())
        Label(self, text='Início:', font='Arial 12 bold', fg='white', bg=fundo).place(x=20, y=290)
        self.com_ini = ttk.Combobox(self, values=self.anos, textvariable=self.var_ini, font='Arial 12', justify=CENTER, state='readonly', width=12).place(x=20, y=310)

        self.var_fim = StringVar()
        Label(self, text='Final:', font='Arial 12 bold', fg='white', bg=fundo).place(x=165, y=290)
        self.com_fim = ttk.Combobox(self, values=self.anos, textvariable=self.var_fim, font='Arial 12', justify=CENTER, state='readonly', width=12).place(x=165, y=310)
        
        Button(self, text='Def. Range', font='Arial 11 bold', fg='white', bg=fun_b, width=10, command=self.graficos_range).place(x=310, y=305)

    def triangulacao(self):
        met = self.metodo.get()

        canvas = Canvas(self, height=200, width=200, bg=fundo, border=0).place(x=450, y=200)
      
        trian = Triangulaction()

        ind = self.paramt_tri.get()
        if ind == 'Precipitação':
            foco = 1
            y_label = "Precipitação (mm)"
        elif ind == 'Temperatura máxima':
            foco = 2
            y_label = "Temperatura(°C)"
        else:
            foco = 3
            y_label = "Temperatura(°C)"


        metodo_list = ['Arithmetic Averange', 'Inverse Distance Weighted', 'Regional Weight', 'Optimized Normal Ratio']  

        if met == 'Arithmetic Averange':
            trian.aa(foco)
            eixo_x, eixo_y_tri, eixo_y_exato, media_ea, media_er, lixo = trian.get_aa()
        elif met == 'Inverse Distance Weighted':
            trian.idw(foco)
            eixo_x, eixo_y_tri, eixo_y_exato, media_ea, media_er, lixo = trian.get_idw()
        elif met == 'Regional Weight':
            trian.rw(foco)
            eixo_x, eixo_y_tri, eixo_y_exato, media_ea, media_er, lixo = trian.get_rw()
        else:
            trian.onr(foco)
            eixo_x, eixo_y_tri, eixo_y_exato, media_ea, media_er, lixo = trian.get_onr()

        

        
       
        media_ea = round(media_ea, 4)
        media_er = round(media_er, 4)
        texto = 'Média Erro absoluto: '+ str(media_ea) + ' | Média Erro relativo: '+ str(media_er)
        figura = Figure(figsize=(14.5,9.5), dpi=100)
        figura.subplots_adjust(left=0.05, bottom=0.08, right=0.98, top=0.93)
        plot_r = figura.add_subplot(111)
        plot_r.plot(eixo_x, eixo_y_exato,label='Exato', color='green')
        plot_r.plot(eixo_x, eixo_y_tri, label='IDW', color='red')
        plot_r.legend()
        plot_r.grid(True)
        plot_r.set_ylabel(y_label)
        plot_r.set_xlabel("Comparações")
        plot_r.set_title(texto)
        

        
        canvas = FigureCanvasTkAgg(figura, master=self.master)
        
        canvas.draw()
        canvas.get_tk_widget().pack()
        canvas.get_tk_widget().place(x=450, y=57)
        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.place(x=1150, y=10)

        toolbar.update()

    def preparar_eixos(self, mat, foco):
        x = list()
        y = list()

        for i in range(len(mat)):
            y.append(mat[i][foco])
            text = str(mat[i][1]) + '/' + str(mat[i][2]) + '/' + str(mat[i][0])
            x.append(dt.datetime.strptime(text,"%m/%d/%Y").date())
    
        return x, y

    def prepara_mat(self, dados, foco):
        mat = list()
        for i in range(len(dados)):
            mat.append([int(dados[i][0]), int(dados[i][1]), int(dados[i][2]), float(dados[i][foco])])
        return mat
    
    def separa_estacao(self, dados, est):
        if est == 1:
            mes1 = 12
            mes2 = 1
            mes3 = 2

        sazonal = list()
        aux = list()
        flag = 0
        for i in range(len(dados)):
            try:
                if mes1 == dados[i][1] or mes2 == dados[i][1] or mes3 == dados[i][1]:
                    aux.append(dados[i])
                    flag = 0
                elif dados[i+1][1] == mes3 + 1 and flag == 0:
                    sazonal.append(aux)
                    aux = list()
                    flag = 1
                
            except IndexError:
                sazonal.append(aux)
                aux = list()
        return sazonal

    def histograma(self):
        t = Tratamento()
        dados = t.retorna_arq(self.data_hist.get())
        if self.paramt_hist.get() == "Precipitação":
            col = 3
        elif self.paramt_hist.get() == "Temperatura máxima":
            col = 4
        elif self.paramt_hist.get() == "Temperatura mínima":
            col = 5

        mat = self.prepara_mat(dados, col)
        
        saz = self.separa_estacao(mat,1)
        del saz[0]
        
        ultimo = len(saz) - 2
        
        x1, y1 = self.preparar_eixos(saz[ultimo-9], 3)
        x2, y2 = self.preparar_eixos(saz[ultimo-8], 3)
        x3, y3 = self.preparar_eixos(saz[ultimo-7], 3)
        x4, y4 = self.preparar_eixos(saz[ultimo-6], 3)
        x5, y5 = self.preparar_eixos(saz[ultimo-5], 3)
        x6, y6 = self.preparar_eixos(saz[ultimo-4], 3)
        x7, y7 = self.preparar_eixos(saz[ultimo-3], 3)
        x8, y8 = self.preparar_eixos(saz[ultimo-2], 3)
        x9, y9 = self.preparar_eixos(saz[ultimo-1], 3)
        x10, y10 = self.preparar_eixos(saz[ultimo], 3)

        
        x = list()
        cont = 17
        
        for i in range(17, 50):
            x.append(cont)
            cont += 0.5
        max_lim = max(max(y1), max(y2), max(y3), max(y4), max(y5), max(y6), max(y7), max(y8), max(y9), max(y10)) +0.5
        min_lim = min(min(y1), min(y2), min(y3), min(y4), min(y5), min(y6), min(y7), min(y8), min(y9), min(y10)) -0.5

        
        y1 = np.array(y1)
        y2 = np.array(y2)
        y3 = np.array(y3)
        y4 = np.array(y4)
        y5 = np.array(y5)
        y6 = np.array(y6)
        y7 = np.array(y7)
        y8 = np.array(y8)
        y9 = np.array(y9)
        y10 = np.array(y10)


        fig = Figure(figsize=(14.5,9.5), dpi=100)
        fig.subplots_adjust(left=0.05, bottom=0.08, right=0.98, top=0.93)
        plot1 = fig.add_subplot(2,5,1)
        plot1.set_title(saz[ultimo-9][len(saz[ultimo-9])-1][0])
        plot1.hist(y1, bins=40, linewidth=0.5, edgecolor="white")
        plot1.set_xlim((min_lim, max_lim))
        plot1.axvline(y1.mean(), color='red')
        

        plot2 = fig.add_subplot(2,5,2)
        plot2.set_title(saz[ultimo-8][len(saz[ultimo-8])-1][0])
        plot2.hist(y2, bins=40, linewidth=0.5, edgecolor="white")
        plot2.set_xlim((min_lim, max_lim))
        plot2.axvline(y2.mean(), color='red')

        plot3 = fig.add_subplot(2,5,3)
        plot3.set_title(saz[ultimo-7][len(saz[ultimo-7])-1][0])
        plot3.hist(y3, bins=40, linewidth=0.5, edgecolor="white")
        plot3.set_xlim((min_lim, max_lim))
        plot3.axvline(y3.mean(), color='red')


        plot4 = fig.add_subplot(2,5,4)
        plot4.set_title(saz[ultimo-6][len(saz[ultimo-6])-1][0])
        plot4.hist(y4, bins=40, linewidth=0.5, edgecolor="white")
        plot4.set_xlim((min_lim, max_lim))
        plot4.axvline(y4.mean(), color='red')


        plot5 = fig.add_subplot(2,5,5)
        plot5.set_title(saz[ultimo-5][len(saz[ultimo-5])-1][0])
        plot5.hist(y5, bins=40, linewidth=0.5, edgecolor="white")
        plot5.set_xlim((min_lim, max_lim))
        plot5.axvline(y5.mean(), color='red')


        plot6 = fig.add_subplot(2,5,6)
        plot6.set_title(saz[ultimo-4][len(saz[ultimo-4])-1][0])
        plot6.hist(y6, bins=40, linewidth=0.5, edgecolor="white")
        plot6.set_xlim((min_lim, max_lim))
        plot6.axvline(y6.mean(), color='red')


        plot7 = fig.add_subplot(2,5,7)
        plot7.set_title(saz[ultimo-3][len(saz[ultimo-3])-1][0])
        plot7.hist(y7, bins=40, linewidth=0.5, edgecolor="white")
        plot7.set_xlim((min_lim, max_lim))
        plot7.axvline(y7.mean(), color='red')


        plot8 = fig.add_subplot(2,5,8)
        plot8.set_title(saz[ultimo-2][len(saz[ultimo-2])-1][0])
        plot8.hist(y8, bins=40, linewidth=0.5, edgecolor="white")
        plot8.set_xlim((min_lim, max_lim))
        plot8.axvline(y8.mean(), color='red')


        plot9 = fig.add_subplot(2,5,9)
        plot9.set_title(saz[ultimo-1][len(saz[ultimo-1])-1][0])
        plot9.hist(y9, bins=40, linewidth=0.5, edgecolor="white")
        plot9.set_xlim((min_lim, max_lim))
        plot9.axvline(y9.mean(), color='red')


        plot10 = fig.add_subplot(2,5,10)
        plot10.set_title(saz[ultimo][len(saz[ultimo])-1][0])
        plot10.hist(y10, bins=40, linewidth=0.5, edgecolor="white")
        plot10.set_xlim((min_lim, max_lim))
        plot10.axvline(y10.mean(), color='red')


        canvas = FigureCanvasTkAgg(fig, master=self.master)
        
        canvas.draw()
        canvas.get_tk_widget().pack()
        canvas.get_tk_widget().place(x=450, y=57)
        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.place(x=1150, y=10)
        toolbar.update()

    def boxplot_grafico(self):
        t = Tratamento()
        dados = t.retorna_arq(self.data_hist.get())
        if self.paramt_hist.get() == "Precipitação":
            col = 3
        elif self.paramt_hist.get() == "Temperatura máxima":
            col = 4
        elif self.paramt_hist.get() == "Temperatura mínima":
            col = 5

        mat = self.prepara_mat(dados, col)
        
        saz = self.separa_estacao(mat,1)
        del saz[0]
        
        ultimo = len(saz) - 2
        
        x1, y1 = self.preparar_eixos(saz[ultimo-9], 3)
        x2, y2 = self.preparar_eixos(saz[ultimo-8], 3)
        x3, y3 = self.preparar_eixos(saz[ultimo-7], 3)
        x4, y4 = self.preparar_eixos(saz[ultimo-6], 3)
        x5, y5 = self.preparar_eixos(saz[ultimo-5], 3)
        x6, y6 = self.preparar_eixos(saz[ultimo-4], 3)
        x7, y7 = self.preparar_eixos(saz[ultimo-3], 3)
        x8, y8 = self.preparar_eixos(saz[ultimo-2], 3)
        x9, y9 = self.preparar_eixos(saz[ultimo-1], 3)
        x10, y10 = self.preparar_eixos(saz[ultimo], 3)

        
        x = list()
        cont = 17
        
        for i in range(17, 50):
            x.append(cont)
            cont += 0.5
        max_lim = max(max(y1), max(y2), max(y3), max(y4), max(y5), max(y6), max(y7), max(y8), max(y9), max(y10)) +0.5
        min_lim = min(min(y1), min(y2), min(y3), min(y4), min(y5), min(y6), min(y7), min(y8), min(y9), min(y10)) -0.5

        boxplot = list()
        boxplot.append(y1)
        boxplot.append(y2)
        boxplot.append(y3)
        boxplot.append(y4)
        boxplot.append(y5)
        boxplot.append(y6)
        boxplot.append(y7)
        boxplot.append(y8)
        boxplot.append(y9)
        boxplot.append(y10)


        fig = Figure(figsize=(14.5,9.5), dpi=100)
        fig.subplots_adjust(left=0.05, bottom=0.08, right=0.98, top=0.93)
     
        plot1 = fig.add_subplot(1,1,1)
        plot1.set_title("Boxplot para Temperatura máxima [10 Anos]")
        plot1.boxplot(boxplot)
        plot1.set_xlabel('Ano')
        plot1.set_ylabel(self.data_hist.get())
        

        canvas = FigureCanvasTkAgg(fig, master=self.master)
        
        canvas.draw()
        canvas.get_tk_widget().pack()
        canvas.get_tk_widget().place(x=450, y=57)
        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.place(x=1150, y=10)
        toolbar.update()
    
    def open_machine(self):
        window = Aprendizado_Marquina()
        window.mainloop()

    def open_meta(self):
        window = MetaLearning()
        window.mainloop()

    def __init__(self, *args, **kwargs):
        Frame.__init__(self, master=None, bg=fundo) #Configurando a janela da ferramenta
        self.master.title("IC_FAPEMGIG - V1.0") #Colocando o titulo na aba da ferramenta
        self.master.geometry('800x800') #Definindo o tamanho inicial da tela (podendo expandir)

        Button(self, text='Selecionar Banco de Dados', font='Arial 12 bold', fg='white', bg=fun_ap, width=38, command=self.listar_cidades).place(x=20, y=20) #Botão para os usuários selecionar a pasta que tem todos os arquivos.csv
        self.pack(fill='both', expand=True)

        Label(self, text='Cidade Alvo:', font='Arial 11 bold', bg=fundo, fg='white', state=DISABLED).place(x=20, y=65)
        self.comb_alvo = ttk.Combobox(self, width=20, font='Arial 11', justify=CENTER, state=DISABLED).place(x=20, y=85)
        Label(self, text='Vizinha A:', font='Arial 11 bold', bg=fundo, fg='white', state=DISABLED).place(x=220, y=65)
        self.comb_va = ttk.Combobox(self, width=20, font='Arial 11', justify=CENTER, state=DISABLED).place(x=224, y=85)
        Label(self, text='Vizinha B:', font='Arial 11 bold', bg=fundo, fg='white', state=DISABLED).place(x=20, y=115)
        self.comb_vb = ttk.Combobox(self, width=20, font='Arial 11', justify=CENTER, state=DISABLED).place(x=20, y=135)
        Label(self, text='Vizinha C:', font='Arial 11 bold', bg=fundo, fg='white', state=DISABLED).place(x=220, y=115)
        self.comb_vc = ttk.Combobox(self, width=20, font='Arial 11', justify=CENTER, state=DISABLED).place(x=224, y=135)

        Button(self, text='Confirmar Grupo', font='Arial 12 bold', fg='white', bg=fun_b, width=38, command=self.tratar, state=DISABLED).place(x=20, y=170)


        Label(self, text='Visualizar Dados', font='Arial 14 bold', fg='white', bg=fundo).place(x=140, y=210)
        Label(self, text='Dado:', font='Arial 12 bold', fg='white', bg=fundo).place(x=20, y=240)
        self.type_data = StringVar()
        data_list = ['Cidade alvo', 'Vizinha A', 'Vizinha B', 'Vizinha C', 'Dados comum']
        self.comb_type_data = ttk.Combobox(self, values=data_list, textvariable=self.type_data, width=12, font='Arial 12', justify=CENTER, state='readonly').place(x=20, y=260)
        
        Label(self, text='Parâmetro:', font='Arial 12 bold', fg='white', bg=fundo).place(x=165, y=240)
        self.parameter = StringVar()
        para_list = ['Precipitação', 'Temperatura máxima', 'Temperatura mínima']
        self.comb_parameter = ttk.Combobox(self, values=para_list, textvariable=self.parameter, width=12, font='Arial 12', justify=CENTER, state='readonly').place(x=165, y=260)
        Button(self, text='Selecionar', font='Arial 11 bold', fg='white', bg=fun_b, width=10, command=self.graficos_comum).place(x=310, y=255)

       
        Label(self, text='Início:', font='Arial 12 bold', fg='white', bg=fundo, state=DISABLED).place(x=20, y=290)
        self.com_ini = ttk.Combobox(self, font='Arial 12', justify=CENTER, state=DISABLED, width=12).place(x=20, y=310)
        Label(self, text='Final:', font='Arial 12 bold', fg='white', bg=fundo, state=DISABLED).place(x=165, y=290)
        self.com_fim = ttk.Combobox(self, font='Arial 12', justify=CENTER, state=DISABLED, width=12).place(x=165, y=310)
        
        Button(self, text='Def. Range', font='Arial 11 bold', fg='white', bg=fun_b, width=10, command=self.graficos_range, state=DISABLED).place(x=310, y=305)


        Label(self, text='Dado', font='Arial 11 bold', fg='white', bg=fundo).place(x=20, y=340)    
        self.data_hist = StringVar()
        datahist_list = ['Cidade alvo', 'Vizinha A', 'Vizinha B', 'Vizinha C']  
        ttk.Combobox(self, values=datahist_list, textvariable=self.data_hist, width=18, font='Arial 12', justify=CENTER, state='readonly').place(x=20, y=360)
        Label(self, text='Parâmetro', font='Arial 11 bold', fg='white', bg=fundo).place(x=20, y=390)    
        self.paramt_hist = StringVar()
        ttk.Combobox(self, values=para_list, textvariable=self.paramt_hist, width=18, font='Arial 12', justify=CENTER, state='readonly').place(x=20, y=410)
        Button(self, text='Histograma, últimos 10y', font='Arial 11 bold', fg='white', bg=fun_meta_le, width=20, command=self.histograma).place(x=220, y=355) 
        
        Button(self, text='Boxplot, últimos 10y', font='Arial 11 bold', fg='white', bg=fun_meta_le, width=20, command=self.boxplot_grafico).place(x=220, y=405) 

        Label(self, text='Técnicas', font='Arial 14 bold', fg='white', bg=fundo).place(x=170, y=460)
        Button(self, text='Machine Learning', font='Arial 11 bold', fg='white', bg=fun_ap, width=42, command=self.open_machine).place(x=20, y=495)

        Label(self, text='Método', font='Arial 11 bold', fg='white', bg=fundo).place(x=20, y=530)    
        self.metodo = StringVar()
        metodo_list = ['Arithmetic Averange', 'Inverse Distance Weighted', 'Regional Weight', 'Optimized Normal Ratio']  
        self.comb_metodo = ttk.Combobox(self, values=metodo_list, textvariable=self.metodo, width=18, font='Arial 12', justify=CENTER, state='readonly').place(x=20, y=550)
        self.teste = Label(self, text='Parâmetro', font='Arial 11 bold', fg='white', bg=fundo).place(x=20, y=580)    
        self.paramt_tri = StringVar()
        self.comb_para_tro = ttk.Combobox(self, values=para_list, textvariable=self.paramt_tri, width=18, font='Arial 12', justify=CENTER, state='readonly').place(x=20, y=600)
        Button(self, text='Triangulação', font='Arial 11 bold', fg='white', bg=fun_alt, width=20, height=4, command=self.triangulacao).place(x=220, y=540) 
        
        Button(self, text='Mostrar Localização', font='Arial 11 bold', fg='white', bg=fun_alt, width=42, command=self.show_map).place(x=20, y=640) 

        Button(self, text='Meta Learning', font='Arial 11 bold', fg='white', bg=fun_b, width=42, command=self.open_meta).place(x=20, y=680)
       
if __name__ == '__main__':
    mainwindow = Principal()
    mainwindow.mainloop()
