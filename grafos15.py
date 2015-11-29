#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import Queue as pq
import timeit as timeit
import math
import matplotlib.pyplot as plt
#from sklearn import linear_model
import argparse 


#######################################################
# Nombre:
# Funcionalidad:
# Argumentos:
# Salida:
#######################################################
def randMatrPosWGraph(nNodes, sparseFactor, maxWeight=50.):
  
  matriz = np.zeros(shape = (nNodes, nNodes))
  for i in range(nNodes):
    for j in range(nNodes):
      matriz[i][j] = np.inf
  for i in range(nNodes):
    for j in range(nNodes):
      if i != j:  
        if np.random.binomial(1, sparseFactor) == 1:
          weight  = np.random.randint(0, maxWeight)
          neight = np.random.randint(0, nNodes)
          if i != neight:
            matriz[i][neight] = weight
  return matriz



def cuentaRamas(mG):
  count = 0
  for i in range(len(mG)):
    for j in range(len(mG)):
      if mG[i][j] != np.inf:
        count = count + 1
  return count

def fromAdjM2Dict(mG) :
  dic = dict()
  contador = 0
  
  for i in mG: #range(mG.shape[0]):
    dicAux =[]
    #dic.update( {i:[]} )
    for j in range(len(i)): #range(N):
      #if j != i and mG[i,j] != np.inf:
      #  dic[i].append( (j, mG[i,j]) )
      dicAux2 = []

      if contador != j and i[j] != np.inf:
        dicAux2.append(i[j])
        dicAux2.append(j)
        dicAux.append((i[j], j))

    dic.update({contador : dicAux})
    contador += 1
  return dic

def fromDict2AdjM(dG):
  
  nNodes = len(dG.keys())
  matriz = np.zeros(shape = (nNodes, nNodes))
  for i in range(nNodes):
    matriz[i] = np.inf

  #for k in dG:
  # for le in dG[k]:
  #   j = le[0]; w = le[1]
  #   matriz[k, j] = w
  for key, value in dG.iteritems():
    while value:
      lista = value.pop()
      #lista = list(lista)
    
      matriz[key][lista[0]] = lista[1]
  return matriz

def dijkstraM(mG, u):
  v = []
  p = []
  d = []
  for i in range(len(mG)):
    v.append(False)
    p.append(None) 
    d.append(np.inf) 

  q = pq.PriorityQueue()
 
  d[u] = 0
  

  q.put((mG[u][0], u)) 

  while not q.empty():
    w = q.get()
    if v[w[1]] == False:
      v[w[1]] = True
      for k in range(len(mG[w[1]])):
        if d[k] > d[w[1]] + mG[w[1]][k]:
          d[k] = d[w[1]] + mG[w[1]][k]
          p[k] = w[1]
          q.put((mG[k][0], k))


  return p, d

def dijkstraD(dG, u):

  matriz = fromDict2AdjM(dG)
  return dijkstraM(matriz, u)
 

arr = []
k = 0

def timeDijkstraM(nGraphs, nNodesIni, nNodesFin, step, sparseFactor=.25): 
  timeList = []

  for nNodes in range(nNodesIni, nNodesFin, step):
    matriz = randMatrPosWGraph(nNodes, sparseFactor, maxWeight=50.)
    arr.append(matriz)
    
    acum = 0
    for j in range(len(matriz)):
      k = j
      setup = "import __main__ as test"
      
      acum += timeit.timeit("test.dijkstraM(test.arr[len(test.arr)-1], test.k)", setup=setup, number = 1)

    timeList.append(acum/len(matriz))
        
          

  return timeList
  
def n2log(nNodesIni, nNodesFin, step):
  log = []
  for i in range(nNodesIni, nNodesFin, step):
    log.append(i**2 * np.log10(i))
  nlog = np.array(log);
  return nlog

def plotFitDijkstraM(lT, func2fit, nNodesIni, nNodesFin, step):
  n2log = func2fit(nNodesIni, nNodesFin, step);
  print "medidas"
  print l 
  print len(l)
  print n2log
  print len(n2log)
  N = len(l) 

  lr = linear_model.LinearRegression()
  lr.fit(n2log[:, np.newaxis], lT)
  fit = lr.predict(n2log[:, np.newaxis])

  plt.plot(fit)
  plt.plot(lT)
  plt.show()

  return


def dijkstraMAllPairs(mG):
  nNodes = len(mG)
  matriz = np.zeros(shape = (nNodes, nNodes))
  for i in range(nNodes):
    for j in range(nNodes):
      matriz[i][j] = np.inf

  for i in range(len(mG)):
    p,d = dijkstraM(mG,i)
    for j in range(len(mG)):
      matriz[i][j] = d[j]
  return matriz


def floydWarshall(mG):
  nNodes = len(mG)
  matriz = np.zeros(shape = (nNodes, nNodes))
  for i in range(nNodes):
    for j in range(nNodes):
      matriz[i][j] = np.inf

  for k in range(nNodes):
    matriz[k][k] = 0
  for i in range(nNodes):
    for j in range(nNodes):
      if i != j:
        matriz[i][j] = mG[i][j]

  for k in range(nNodes):
    for i in range(nNodes):
      for j  in range(nNodes):
        aux = matriz[i][k] + matriz[k][j]
        if matriz[i][j] > aux:
          matriz[i][j] = aux
  
  return matriz


# FIX mirar donde usar nGraphs
def timeDijkstraMAllPairs(nGraphs, nNodesIni, nNodesFin, step, sparseFactor):
  timeList = []

  for nNodes in range(nNodesIni, nNodesFin, step):
    matriz = randMatrPosWGraph(nNodes, sparseFactor, maxWeight=50.)
    arr.append(matriz)
    # print arr
    acum = 0
    for j in range(len(matriz)):
      k = j
      setup = "import __main__ as test"
      
      acum += timeit.timeit("test.dijkstraMAllPairs(test.arr[len(test.arr)-1])", setup=setup, number = 1)

    timeList.append(acum/len(matriz))
  return timeList




def timeFloydWarshall(nGraphs, nNodesIni, nNodesFin, step, sparseFactor):
  timeList = []

  for nNodes in range(nNodesIni, nNodesFin, step):
    matriz = randMatrPosWGraph(nNodes, sparseFactor, maxWeight=50.)
    arr.append(matriz)
    # print arr
    acum = 0
    for j in range(len(matriz)):
      k = j
      setup = "import __main__ as test"
      
      acum += timeit.timeit("test.floydWarshall(test.arr[len(test.arr)-1])", setup=setup, number = 1)

    timeList.append(acum/len(matriz))
  return timeList


def dG2TGF(dG, fName):
  f = open(fName, "w")
  matriz = fromDict2AdjM(dG)
  for i in range(len(matriz)):
    f.write("%d" % i)
    f.write("\n")
  f.write("#")
  f.write("\n")

  for i in range(len(matriz)):
    for j in range(len(matriz)):
      if matriz[i][j] != np.inf:
        f.write("%d" % i)
        f.write(" ")
        f.write("%d" % j)
        f.write(" ")
        f.write("%s" % matriz[i][j])
        f.write("\n")
  f.close()
  return

def TGF2dG(fName):
  f = open(fName)
  initialize = 0
  nNodes = 0
  for line in f.read().splitlines():
    spl = line.split()
    if len(spl) == 1:
      nNodes = 1 + nNodes
    else:
      initialize = initialize + 1
    if initialize == 1:
      nNodes = nNodes - 1
      matriz = np.zeros(shape = (nNodes, nNodes))

      for i in range(nNodes):
        for j in range(nNodes):
          matriz[i][j] = np.inf
    if initialize > 0:
      matriz[int(spl[0])][int(spl[1])] = spl[2]

  return fromDict2AdjM(matriz)



#plotFitDijkstraM(timeDijkstraM(20, 10, 1000, 10, sparseFactor=.25), n2log, 10, 1000, 10)


# parser = argparse.ArgumentParser(description='Parseo de argumentos')
# parser.add_argument('file')

# args = parser.parse_args()

# mG = TGF2dG(args.file)
# dicc = fromAdjM2Dict(mG)
# print mG
# print fromDict2AdjM(dicc)

# p = dijkstraMAllPairs(mG)
# r = floydWarshall(mG)

# print p[0:8, 0:8]
# print r[0:8, 0:8]

def randMatrUndPosWGraph(nNodes, sparseFactor, maxWeight=50.):

  matriz = np.zeros(shape = (nNodes, nNodes))
  for i in range(nNodes):
    for j in range(nNodes):
      matriz[i][j] = np.inf
  for i in range(nNodes):
    for j in range(nNodes):
      if i != j:
        if np.random.binomial(1, sparseFactor) == 1:
          weight  = np.random.randint(0, maxWeight)
          neight = np.random.randint(0, nNodes)
          if i != neight:
            matriz[i][neight] = weight
            matriz[neight][i] = weight
  return matriz


def checkUndirectedM(mG):
  for i in range(len(mG)):
    for j in range(len(mG)):
      if mG[i][j] != mG[j][i]:
        return False
  return True

def checkUndirectedD(dG):   
  for k in dG:
    for le in dG[k]:
      nodo = le[1]
      peso = le[0]
      count = 0
      for le2 in dG[nodo]:  
        peso2 = le2[0]
        nodo2 = le2[1]
        if k == nodo2:
          if peso == peso2:
            count = 1
      if count == 0:
        return False
  return True

def initCD(N):
  array = np.ones(N)*-1
  return array

def union(rep1, rep2, pS):
  pS[rep2] = rep1 #join second tree to first
  return rep1
  # if pS[rep2] < pS[rep1]: #T_rep2 is taller
  #   print "11"
  #   pS[rep1] = rep2
  #   return rep2
  # elif pS[rep2] > pS[rep1]: #T_rep1 is taller
  #   print "22"
  #   pS[rep2] = rep1
  #   return rep1
  # else: #T_rep1, T_rep2 have the same lenght
  #   pS[rep2] = rep1
  #   pS[rep1] -= 1
  #   print "33"
  #   return rep1
  
def find(ind, pS, flagCC):
  if flagCC == False:
    while pS[ind] != -1:
      ind = pS[ind]
    return ind
  else:
    z = ind
    while pS[z] >= 0:
      z = pS[z]
    while pS[ind] >= 0:
      y = pS[ind]
      pS[ind] = z
      ind = y
    return z

#KRUSKAL

def insertPQ(dG, Q):
  #Recorrer el arbol hallando uniones
  #Q.put((mG[u][0], u)) 
  for k in dG:
    for le in dG[k]:
      nodo = le[1]
      peso = le[0]
      if(k < nodo):
        Q.put((peso,k,nodo)) 
  return 

def formatToDicc(L, N):
  dG = dict()
  for i in range(N):
    dG.update({i : []})
  for i in L:
    dG[i[1]].append((i[0],i[2]))
    dG[i[2]].append((i[0],i[1]))
  return dG

def kruskal(dG, flagCC=True):
  L = [] 
  Q = pq.PriorityQueue()  
  insertPQ(dG, Q)
  S = initCD(len(dG.keys())) 
  while not Q.empty(): 
    w = Q.get() 
    x = find(w[1], S, flagCC)
    y = find(w[2], S, flagCC) 
    if x != y:
      L.append((w[0],w[1],w[2]))
      union(x, y, S) 
  dG = formatToDicc(L,len(dG))
  return dG

udicc = dict()

def timeKruskal(nGraphs, nNodesIni, nNodesFin, step, sparseFactor, flagCC):
  timeList = []
  acum = 0
  i = 0
  for nNodes in range(nNodesIni, nNodesFin, step):
    if i == nGraphs:
      return timeList
    mG = randMatrUndPosWGraph(nNodes, 0.5, maxWeight= 50)
    udicc = fromAdjM2Dict(mG)
    start_time = timeit.default_timer()
      
    #acum += timeit.timeit("test.kruskal(test.udicc)", setup=setup, number = 1)
    kruskal(udicc)
    elapsed = timeit.default_timer() - start_time
    timeList.append(elapsed)
    i = i + 1

  return timeList

def kruskal102(dG, flagCC=True):
  timeList = []
  L = [] 
  Q = pq.PriorityQueue()  
  insertPQ(dG, Q)
  S = initCD(len(dG.keys())) 
  #Timer
  start_time = timeit.default_timer()
  while not Q.empty(): 
    w = Q.get() 
    x = find(w[1], S, flagCC)
    y = find(w[2], S, flagCC) 
    if x != y:
      L.append((w[0],w[1],w[2]))
      union(x, y, S) 
  elapsed = timeit.default_timer() - start_time
  dG = formatToDicc(L,len(dG))
  return dG, elapsed

def timeKruskal102(nGraphs, nNodesIni, nNodesFin, step, sparseFactor, flagCC):
  timeList = []
  acum = 0
  i = 0
  for nNodes in range(nNodesIni, nNodesFin, step):
    if i == nGraphs:
      return timeList
    mG = randMatrUndPosWGraph(nNodes, 0.5, maxWeight= 50)
    udicc = fromAdjM2Dict(mG)
    dG, time = kruskal102(udicc, flagCC)
    i = i + 1
    timeList.append(time)
  return timeList

def plotKruskal(lT, func2fit, nNodesIni, nNodesFin, step):
  n2log = func2fit(nNodesIni, nNodesFin, step);
  print "medidas"
  print lT 
  print len(lT)
  print n2log
  print len(n2log)
  N = len(lT) 

  lr = linear_model.LinearRegression()
  lr.fit(n2log[:, np.newaxis], lT)
  fit = lr.predict(n2log[:, np.newaxis])

  plt.plot(fit)
  plt.plot(lT)
  plt.show()

  return
###############################################################################
# Nombre: incAdy
# Funcionalidad: Devolver la lista de adyacencia e incidencia de un grado dado.
# Argumentos: 
#             -dG: Diccionario de adyacencia de un grafo dirigido.
# Salida: 
#             -Lista de adyacencia de todos los nodos del grafo.
#             -Lista de incidencia de todos los nodos del grafo
###############################################################################
def incAdy(dG):
  lAdy = np.zeros(len(dG))
  lInc = np.zeros(len(dG))

  for k in dG:
    for le in dG[k]:
      lAdy[k] += 1
      lAdy[le[1]] += 1
      lInc[le[1]] += 1
  return lAdy, lInc

###############################################################################
# Nombre: drBP
# Funcionalidad: Función contenedora de la función que desarrolla el algoritmo de 
# busqueda en profundidad en grafos dirigidos.
# Argumentos: 
#             -dG: Diccionario de adyacencia de un grafo dirigido.
# Salida: 
#             -prev: Lista de previos del grafo.
#             -fin: Lista de finalización del grafo
#             -desc: Lista de descubrimiento del grafo.
###############################################################################
def drBP(dG):
  prev = initCD(len(dG))
  fin = initCD(len(dG))
  vist = [False] * len(dG)
  desc = initCD(len(dG))

  for k in dG:
    BP(vist, prev, fin, desc, dG, k)

  return desc, fin, prev

###############################################################################
# Nombre: BP
# Funcionalidad: Función que desarrolla el algoritmo de busqueda en profundidad
# en grafos dirigidos.
# Argumentos: 
#             -dG: Diccionario de adyacencia de un grafo dirigido.
#             -v: Lista de nodos visitados del algoritmo.
#             -p: Lista de previos del grafo.
#             -f: Lista de finalización del grafo
#             -d: Lista de descubrimiento del grafo.
#             
# Salida: 
#             -prev: Lista de previos del grafo.
#             -fin: Lista de finalización del grafo
#             -desc: Lista de descubrimiento del grafo.
###############################################################################
def BP(v, p, f, d, dG, u):
  count = -1
  if v[int(u)] == False:
    v[int(u)] = True
    #Para comprobar el último tiempo(t) usado
    for k in d:
      if k > count:
        count = k   
    for k in f:
      if k > count:
        count = k  
    #Actualización array descubrimiento
    d[u] = count + 1
    for el in dG[u]:
      if v[el[1]] == False:
        p[el[1]] = u
      BP(v, p, f, d, dG, el[1])
    #Para comprobar el último tiempo(t) usado
    for k in d:
      if k > count:
        count = k 
    for k in f:
      if k > count:
        count = k 
    #Actualización array finalización
    f[u] = count + 1
     
  else:
    if u != 0: 
      BP(v, p, f, d, dG, p[int(u)])

  
  return 

def BPasc(v, p, f, d, dG, u, asc):
  count = -1
  if v[int(u)] == False:
    v[int(u)] = True
    #Para comprobar el último tiempo(t) usado
    for k in d:
      if k > count:
        count = k   
    for k in f:
      if k > count:
        count = k  
    #Actualización array descubrimiento
    d[u] = count + 1
    for el in dG[u]:
      if v[el[1]] == False:
        p[el[1]] = u
      #Calculo de ramas ascendentes
      rAscendentes(u, asc, p)

      BPasc(v, p, f, d, dG, int(el[1]), asc)
    #Para comprobar el último tiempo(t) usado
    for k in d:
      if k > count:
        count = k 
    for k in f:
      if k > count:
        count = k    
    #Actualización array finalización
    f[u] = count + 1 
  else:
    rAscendentes(u, asc, p)
    if u != 0: 
      BPasc(v, p, f, d, dG, p[int(u)], asc)
  return 


def rAscendentes(u,asc,p):
  P = u
  cont = 0   
  while P != -1:
    previoAnterior = P
    P = p[P]
    cont += 1
    if cont > 2:
      asc.append((u,int(previoAnterior))) 
  return 

def detectarCiclos(p,dG):
  
  for k in dG:
    for el in dG[k]:
      P = k  
      while P != -1:
        P = p[P]
        if P == el[1]:
          return True
      asc =  P != -1
  return False



def drBPasc(dG):
  prev = initCD(len(dG))
  fin = initCD(len(dG))
  vist = [False] * len(dG)
  desc = initCD(len(dG))
  asc = []

  for k in dG:
    BPasc(vist, prev, fin, desc, dG, k, asc)

  asc = np.unique(asc)
  return asc

def DAG(dG):
  d,f,p = drBP(dG)
  return detectarCiclos(p,dG)
  
def OT(dG):
  OT = []
  q = pq.PriorityQueue()

  #Comprobar si es dirigido
  if checkUndirectedM(dG) == False:
    #Comprobar si tiene ciclos
    if DAG(dG) == False:
      #Realizar ordenacion topologica
      #Comprobar cual es el nodo inicial(menor incidencia)
      ady,inc = incAdy(dG)
      min = np.amin(inc)
      nodo = 0
      for nodo in range(len(inc)):
        if min == inc[nodo]:
          break
      
      #Realizar BP empexando en nodo con menor incidencia
      d,f,p = drBPOT(dG, nodo)

      for k in range(len(f)):
        q.put((f[k], k)) 
      while not q.empty():
        w = q.get()
        OT.append(w)
      OT = OT[::-1]
      for el in range(len(OT)):
        OT[el] = OT[el][1]
      return OT
  return 

def drBPOT(dG, nodo):
  prev = initCD(len(dG))
  fin = initCD(len(dG))
  vist = [False] * len(dG)
  desc = initCD(len(dG))
  
  BP(vist, prev, fin, desc, dG, nodo)
  for n in range(len(vist)):
    if vist[n] == False:
      BP(vist, prev, fin, desc, dG, n)

  return desc, fin, prev

def distMinSingleSourceDAG(dG):
  #Comprobar si es dirigido
  if checkUndirectedM(dG) == False:
    #Comprobar si tiene ciclos
    if DAG(dG) == False:
      #Comprobar si tiene una unica fuente
      d,f,p = drBP(dG)
      count = 0
      for prev in p:
        if prev == -1:
          count += 1
      print "fuentes"
      print count
      if count == 1:
        print "Cumplidas condiciones previas"
        #DAG con una única fuente.
        #Comprobar si hay más de un vértice con incidencia 0
        ady,inc = incAdy(dG)
        count = 0
        print "incidencia"
        print inc
        for l in range(len(inc)):
          if inc[l] == 0:
            count += 1
            if count == 1:
              source = l
        if count > 1:
          print "Existe más de un vértice de incidencia 0"
          print "Se usará el vértice %d como source" % source

        #Cálculo de distancias mínimas.
        #Preparación variables
        d = []
        p = []
        L = []
        for i in range(len(dG)):
          p.append(-1) 
          d.append(np.inf) 
        #Obtener la ordenación topológica.
        L = OT(dG)
        print "ordenacion topológica"
        
        d[L[0]] = 0
        for i in range(len(L)):
          for el in dG[L[i]]:
            if d[el[1]] > d[L[i]] + el[0]:
              d[el[1]] = d[L[i]] + el[0]
              p[el[1]] = L[i]
        return d,p
        #Iterar sobre la ordenación topológica para encontrar caminos mínimos
        
      else:
        print "Mas de un nodo fuente encontrado"
    else:
      print "Grafo con ciclos"
  else:
    print "Grafo no dirigido"

  return

#TEST

# m = np.zeros(shape = (4, 4))
# for i in range (4): m[i] = np.inf

# m[0][1] = 2
# m[1][0] = 3
# m[1][2] = 1
# m[2][1] = 4
# m[2][3] = 2
# m[3][1] = 1

# print m 

# dicc = fromAdjM2Dict(m)
# print dicc

# checkUndirectedD(dicc)

# #Prueba diccionarios no dirigidos

# mG = randMatrUndPosWGraph(4, 0.5, maxWeight= 50)

# udicc = fromAdjM2Dict(mG)
# print udicc
# print checkUndirectedM(mG)
# print checkUndirectedD(udicc)
# print checkUndirectedD(dicc)


#Test Kruskal
# Q = pq.PriorityQueue()
# insertPQ(udicc, Q)
# while not Q.empty():
#   print Q.get()
udicc2 = {0:[(10,1), (12,2), (5,1)], 1:[(10,0),(4,3),(5,0),(6,2)], 2:[(12,0),(6,1),(8,3)], 3:[(4,1),(8,2)]}
udicc3 = {0: [(6.0, 1), (37.0, 2),(15,3)], 1: [(6.0, 0), (40.0, 2), (40.0, 3)], 2: [(37.0, 0), (40.0, 1)], 3: [(40.0, 1),(15,0)]}
dicc3 = {0: [(6.0, 1)], 1: [(40.0, 2), (40.0, 3)], 2: [(37.0, 0)], 3: [(15,0)]}
diccInconexo = {0: [(6.0, 1)], 1: [(40.0, 2), (40.0, 3)], 2: [(37.0, 0)], 3: [(15,0)], 4:[(10,1)]}
diccInconexo2 = {0: [(6, 1)], 1: [(40, 2), (40, 3)], 2: [(37, 0)], 3: [(15,0)], 4:[(12,1)], 5:[(30,0), (25,3)]}
diccAscAciclico = {0: [(3,1), (4,2), (3,4)], 1: [(3,3)], 2: [], 3: [(5,2)], 4:[(9,3)]}
diccAscAciclico2 = {0: [(3,1), (4,2), (3,4)], 1: [(3,3)], 2: [], 3: [(5,2)], 4:[(1,3), (6,5)], 5:[]}
diccAscCiclico = {0: [(3,1), (4,2), (3,4)], 1: [(3,3)], 2: [], 3: [(5,2)], 4:[(9,3), (6,5)], 5:[(3,0)]}
diccAscAciclico3 = {0: [(3,1), (4,2), (3,4)], 1: [(3,3)], 2: [], 3: [(5,2)], 4:[(9,3)], 5:[(5,0)], 6:[(2,0)]}
# print checkUndirectedD(udicc3)
# print udicc2
# print "KRUSKAL"
# print kruskal(udicc2, flagCC=False)

# print "timeKruskal"
# time = timeKruskal(10, 1, 1000, 10, 0.5, True)
# print time
# print timeKruskal102(10, 1, 1000, 10, 0.5, True)

# plotKruskal(time, n2log, 1, 100, 10)

#TEST BP

# a,b = incAdy(dicc3)
# print a
# print b

# d,f,p = drBP(diccAscAciclico2)
# print "previos"
# print p
# print "finalización"
# print f
# print "descubrimiento"
# print d

# a = drBPasc(diccAscAciclico2)

# # print "ascendentes"
# print a

# print DAG(diccAscCiclico)

print "OT"
print OT(diccAscAciclico2)

print distMinSingleSourceDAG(diccAscAciclico2)






