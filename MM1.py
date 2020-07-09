from random import random
from math import log
import matplotlib.pyplot as plt
from numpy import arange
 
IDLE = 0
BUSY = 1
 
def initialize():
    global array_delay_q
    global array_delay_s
    global array_custs_q
    global array_custs_s
    global array_util_server
    global time
    global server_status
    global num_in_q
    global time_last_event
    global num_custs_delayed
    global total_of_delays
    global total_of_delays_in_system
    global area_num_in_q
    global area_num_in_system
    global area_server_status
    global time_next_event
    global time_arrival
    global prob_num_in_q
 
    #se inicializan los arrays individuales de la corrida n
    array_delay_q=[]
    array_delay_s=[]
    array_custs_q=[]
    array_custs_s=[]
    array_util_server=[]
    #Se inicializan variables que estaban en el main    
    time_last_event = 0.0
    time_arrival = []
    prob_num_in_q = [[],[]]
    for i in range(num_delays_required):
        time_arrival.append(0)
    time_next_event = [0,0]
    #Se inicializa el reloj de simulación
    time = 0.0
    #Se inicializan las variables de estado
    server_status = IDLE
    num_in_q = 0
    #Se inicializan los contadores estadísticos
    num_custs_delayed = 0
    total_of_delays = 0.0
    total_of_delays_in_system = 0.0
    area_num_in_q = 0.0
    area_num_in_system = 0.0
    area_server_status = 0.0
 
    time_next_event[0] = time + expon(mean_interarrival)
    time_next_event[1] = 2147483648
 
def timing():
    global next_event_type
    global time
 
    min_time_next_event = 2147483648
    next_event_type = -1
    for i in range(num_events):
        if (time_next_event[i] < min_time_next_event):
            min_time_next_event = time_next_event[i]
            next_event_type = i
    if (next_event_type == -1):
        print("Lista de eventos vacia en el momento: ", time)
        exit(1) #WTF
    time = min_time_next_event
 
 
def arrive():
    global time_next_event
    global server_status
    global num_in_q
    global total_of_delays
    global num_custs_delayed
    global total_of_delays_in_system
    global time_arrival
    global time_start
 
    time_next_event[0] = time + expon(mean_interarrival)
    if server_status == BUSY:
        num_in_q += 1
        time_arrival[num_in_q-1] = time
    else:
        #The following two statements are for program clarity and do not affect the results of the simulation.
        delay = 0.0
        total_of_delays += delay
        num_custs_delayed += 1
        server_status = BUSY
        time_next_event[1] = time + expon(mean_service)
        time_start = time
 
def depart():
    global server_status
    global time_next_event
    global num_in_q
    global time_arrival
    global time_start #Tiempo en el que el cliente ingresa al servidor
    global total_of_delays
    global total_of_delays_in_system
    global num_custs_delayed
   
    total_of_delays_in_system += time - time_start
    if(num_in_q == 0):
        server_status = IDLE
        time_next_event[1] = 2147483648
    else:
        num_in_q -= 1
        time_start = time
        delay = time - time_arrival[0]
        total_of_delays += delay
        total_of_delays_in_system += delay
        num_custs_delayed += 1
        time_next_event[1]= time + expon(mean_service)
        for i in range(num_in_q):
            time_arrival[i] = time_arrival[i+1]
        time_arrival[num_in_q] = 0

 
def update_time_avg_stats():
    global array_custs_q
    global array_custs_s
    global array_util_server
    global time_last_event
    global area_num_in_q
    global area_num_in_system
    global area_server_status
 
    time_since_last_event = time - time_last_event
    prob_num_in_q[1].append(time_since_last_event)
    time_last_event = time    
    area_num_in_q += num_in_q*time_since_last_event
    if server_status == BUSY:
        area_num_in_system += (num_in_q+1)*time_since_last_event
        prob_num_in_q[0].append(num_in_q+1)
    else:
        area_num_in_system += num_in_q*time_since_last_event
        prob_num_in_q[0].append(num_in_q)
    area_server_status += server_status*time_since_last_event
    array_custs_q.append(area_num_in_q / time) #comienza el llenado
    array_custs_s.append(area_num_in_system / time)
    array_util_server.append(area_server_status / time)
 
def expon(mean):
    u = random()
    r = -mean*log(u)
    return r
 
def report():
    print("Promedio de retardo en cola: ", (total_of_delays / num_custs_delayed))    
    print("Promedio de retardo en el sistema: ", (total_of_delays_in_system / num_custs_delayed))
    print("Promedio de clientes en cola: ", (area_num_in_q / time))
    print("Promedio de clientes en el sistema: ", (area_num_in_system / time))
    print("Promedio de utilizacion del servidor: ", (area_server_status / time))
    print("Tiempo total de simulacion: ", time)
    #frec = getFreq(prob_num_in_q)
    #plt.bar(range(len(frec)),height=frec)
    #plt.title("Probabilidad de n clientes en la cola")
    #plt.show()


def reportavg():
    promedios=[]
    for i in range(5):
        promedios.append([])
        for j in range(minlen):
            promedios[i].append(0)

    ncusts_prom=[]
    for i in range(maxlenprob):
        ncusts_prom.append(0)
    for i in range(iteraciones):
        for j in range(minlen):
            promedios[0][j]+=avgdelay_q[i][j]/iteraciones
            promedios[1][j]+=avgdelay_s[i][j]/iteraciones
            promedios[2][j]+=avgcusts_q[i][j]/iteraciones
            promedios[3][j]+=avgcusts_s[i][j]/iteraciones
            promedios[4][j]+=avg_util_server[i][j]/iteraciones
        for k in range(len(avg_probn_in_q[i])):
            ncusts_prom[k]+=avg_probn_in_q[i][k]/iteraciones

    for i in range(iteraciones):
        plt.plot(avgdelay_q[i], alpha=.5)
    plt.plot(promedios[0], color='k', label='Promedio')
    plt.legend(loc="upper right")
    plt.title("Promedios de Retardo en Cola")
    plt.ylabel('Retardo')
    plt.xlabel('Cantidad de eventos')
    plt.show()

    for i in range(iteraciones):
        plt.plot(avgdelay_s[i], alpha=.5)
    plt.plot(promedios[1], color='k', label='Promedio')
    plt.legend(loc="upper right")
    plt.title("Promedios de Retardo en el Sistema")
    plt.ylabel('Retardo')
    plt.xlabel('Cantidad de eventos')
    plt.show()

    for i in range(iteraciones):
        plt.plot(avgcusts_q[i], alpha=.5)
    plt.plot(promedios[2], color='k', label='Promedio')
    plt.legend(loc="upper right")
    plt.title("Promedios de clientes en Cola")
    plt.ylabel('Cantidad de clientes')
    plt.xlabel('Cantidad de eventos')
    plt.show()

    for i in range(iteraciones):
        plt.plot(avgcusts_s[i], alpha=.5)
    plt.plot(promedios[3], color='k', label='Promedio')
    plt.legend(loc="upper right")
    plt.title("Promedios de clientes en Sistema")
    plt.ylabel('Cantidad de clientes')
    plt.xlabel('Cantidad de eventos')
    plt.show()

    for i in range(iteraciones):
        plt.plot(avg_util_server[i], alpha=.5)
    plt.plot(promedios[4], color='k', label='Promedio')
    plt.legend(loc="upper right")
    plt.title("Promedios de utilizacion del Servidor")
    plt.ylabel('Utilizacion')
    plt.xlabel('Cantidad de eventos')
    plt.show()        

    for i in range(iteraciones):
        if mean_interarrival < 1.1:
            plt.bar(range(len(avg_probn_in_q[i])),height=avg_probn_in_q[i],alpha=.5)
        else:
            plt.plot(avg_probn_in_q[i],'o', markersize=3)
    x = range(len(ncusts_prom))        
    plt.bar(x, height=ncusts_prom, color='k',label='Promedio')
    plt.legend(loc="upper right")
    plt.title("Probabilidad de n clientes en el Sistema")
    plt.ylabel('Probabilidad')
    plt.xlabel('n')
    plt.show()

    if (mean_interarrival >= 1.1):
        rho = mean_service/mean_interarrival
        expected_prob = []
        for i in x:
            expected_prob.append((1-rho)*rho**i)
        X = arange(len(ncusts_prom))
        plt.bar(X + 0.00, ncusts_prom, color = "grey", width = 0.25, label='Promedio obtenido')
        plt.bar(X + 0.25, expected_prob, color = "cyan", width = 0.25, label='Valor esperado')
        plt.xticks(X + 0.125, x)
        plt.legend(loc="upper right")
        plt.title("Probabilidad de n clientes en el Sistema")
        plt.ylabel('Probabilidad')
        plt.xlabel('n')
        plt.show()

 
def getFreq(array):
    max = 0
    size = len(array[0])
    for i in range(size):
        if (max < array[0][i]):
            max = array[0][i]
    fr = []
    for i in range(max+1):
        fr.append(0)
    for i in range(size):
        fr[array[0][i]] += array[1][i]/time
    return fr
 
#Parameters
num_events = 2
mean_interarrival = 0.8
mean_service = 1
num_delays_required = 2500
iteraciones=10

avg_probn_in_q=[]
avgdelay_q=[]
avgdelay_s=[]
avgcusts_q=[]
avgcusts_s=[]
avg_util_server=[]
print("Single-server queueing system")
print("Mean interarrival time: ", mean_interarrival, " minutes")
print("Mean service time", mean_service," minutes")
print("Number of customers: ", num_delays_required)

minlen=2147483648
maxlenprob=0
for i in range(iteraciones):
    initialize()
    while (num_custs_delayed < num_delays_required):
        timing()
        update_time_avg_stats()
        if (next_event_type == 0):
            arrive()
        elif (next_event_type == 1):
            depart()
        array_delay_s.append(total_of_delays_in_system / num_custs_delayed) #llenado de arrays
        array_delay_q.append(total_of_delays / num_custs_delayed)
    if len(array_delay_s)<minlen:
        minlen=len(array_delay_s)
    frecs=getFreq(prob_num_in_q)
    if len(frecs)>maxlenprob:
        maxlenprob=len(frecs)
    avgdelay_q.append(array_delay_q)
    avgdelay_s.append(array_delay_s)
    avgcusts_q.append(array_custs_q)
    avgcusts_s.append(array_custs_s)
    avg_util_server.append(array_util_server)      
    avg_probn_in_q.append(frecs)
report()
reportavg()