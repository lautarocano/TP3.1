from random import random
from math import log
import matplotlib.pyplot as plt
from numpy import arange
 
IDLE = 0
BUSY = 1
 
def initialize():
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
    
    #se inicializan array individual de la corrida n
    time_arrival = []
    for i in range(num_delays_required):
        time_arrival.append(0)
 
    #Se inicializa el reloj de simulación
    time = 0.0
    #Se inicializan las variables de estado
    server_status = IDLE
    num_in_q = 0
    time_last_event = 0.0
    #Se inicializan los contadores estadísticos
    num_custs_delayed = 0
    total_of_delays = 0.0
    total_of_delays_in_system = 0.0
    area_num_in_q = 0.0
    area_num_in_system = 0.0
    area_server_status = 0.0
 
    time_next_event = [0,0]
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
    global time_last_event
    global area_num_in_q
    global area_num_in_system
    global area_server_status
 
    time_since_last_event = time - time_last_event
    time_last_event = time
    area_num_in_q += num_in_q*time_since_last_event
    if server_status == BUSY:
        area_num_in_system += (num_in_q+1)*time_since_last_event
    else:
        area_num_in_system += num_in_q*time_since_last_event
    area_server_status += server_status*time_since_last_event
 
def expon(mean):
    u = random()
    r = -mean*log(u)
    return r
 
def getReport():
    report = []
    #Promedio de retardo en cola
    report.append(total_of_delays / num_custs_delayed)
    #Promedio de retardo en el sistema
    report.append(total_of_delays_in_system / num_custs_delayed)
    #Promedio de clientes en cola
    report.append(area_num_in_q / time)
    #Promedio de clientes en el sistema
    report.append(area_num_in_system / time)
    #Promedio de utilizacion del servidor
    report.append(area_server_status / time)
    #Tiempo total de simulacion
    report.append(time)

    return report

 
#Parameters
num_events = 2
mean_service = 1
num_delays_required = 1000
 
iteraciones = 20
paso = 0.05
count = 0.25
index = 0
mean_interarrival = mean_service/count

print("Single-server queueing system")
print("Mean service time", mean_service," minutes")
print("Number of customers: ", num_delays_required)

avgReport = []
for i in range(6):
    avgReport.append([])
    for j in range(24):
        avgReport[i].append(0)

while (mean_interarrival>=0.7):
    print(index)
    for i in (range(iteraciones)):
        initialize()
         
        while (num_custs_delayed < num_delays_required):
            timing()
            update_time_avg_stats()
            if (next_event_type == 0):
                arrive()
            elif (next_event_type == 1):
                depart()
               
        report = getReport()
        for j in range(6):
            avgReport[j][index] += report[j]/iteraciones

    count += paso
    mean_interarrival = 1/count
    index += 1

x  = arange(0.25, 1.41, 0.05)

plt.plot(x,avgReport[0])
plt.title("Promedios de Retardo en cola")
plt.ylabel('Retardo')
plt.xlabel('Rho')
plt.show()

plt.plot(x,avgReport[1])
plt.title("Promedios de Retardo en el Sistema")
plt.ylabel('Retardo')
plt.xlabel('Rho')
plt.show()

plt.plot(x,avgReport[2])
plt.title("Promedios de clientes en cola")
plt.ylabel('Número de clientes')
plt.xlabel('Rho')
plt.show()

plt.plot(x,avgReport[3])
plt.title("Promedios de clientes en el Sistema")
plt.ylabel('Número de clientes')
plt.xlabel('Rho')
plt.show()

plt.plot(x,avgReport[4])
plt.title("Promedio de utilizacion del servidor")
plt.ylabel('Utilización')
plt.xlabel('Rho')
plt.show()

plt.plot(x,avgReport[5])
plt.title("Promedios de tiempo de simulacion")
plt.ylabel('Tiempo')
plt.xlabel('Rho')
plt.show()