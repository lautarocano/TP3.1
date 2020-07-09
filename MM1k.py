from random import random
from math import log
import matplotlib.pyplot as plt
 
IDLE = 0
BUSY = 1
 
def initialize():
    global time
    global server_status
    global num_in_q
    global num_custs_delayed
    global time_next_event
    global q_overflows
    global array_service_denial
 
    #Se inicializa el reloj de simulación
    time = 0.0
    #Se inicializan las variables de estado
    server_status = IDLE
    num_in_q = 0
    num_custs_delayed = 0
    time_next_event = [0,0]
    time_next_event[0] = time + expon(mean_interarrival)
    time_next_event[1] = 2147483648
 
    q_overflows = 0
    array_service_denial = []
 
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
        exit(1)
    time = min_time_next_event
 
 
def arrive():
    global time_next_event
    global server_status
    global num_in_q
    global num_custs_delayed
    global q_overflows
 
    time_next_event[0] = time + expon(mean_interarrival)
    if server_status == BUSY:
        num_in_q += 1
        if num_in_q > q_limit:
                q_overflows += 1
                num_in_q -= 1
    else:
        num_custs_delayed += 1
        server_status = BUSY
        time_next_event[1] = time + expon(mean_service)
 
def depart():
    global server_status
    global time_next_event
    global num_in_q
    global num_custs_delayed
   
    if(num_in_q == 0):
        server_status = IDLE
        time_next_event[1] = 2147483648
    else:
        num_in_q -= 1
        time_start = time
        num_custs_delayed += 1
        time_next_event[1]= time + expon(mean_service)
 
def expon(mean):
    u = random()
    r = -mean*log(u)
    return r
 
# def report():
#     print("Tiempo total de simulacion: ", time)
#     print("Probabilidad de denegación de servicio: ", q_overflows/(num_custs_delayed+q_overflows))
#     pdenegacion = q_overflows/(num_custs_delayed+q_overflows)
#     plt.pie([pdenegacion, 1-pdenegacion], labels=["denegacion", "no denegacion"], autopct="%0.1f %%")
#     plt.title("Probabilidad de denegación de servicio")
#     plt.show()
 
def reportavg():
    denial_prom = []
    for i in range(minlen):
        denial_prom.append(0)
    for i in range(iteraciones):
        for j in range(minlen):
            denial_prom[j] += avg_array[i][j]/iteraciones
 
    for i in range(iteraciones):
        plt.plot(avg_array[i], alpha=.5)
    plt.plot(denial_prom, color='black', label='Promedio')
    plt.legend(loc="upper right")
    plt.title(f"Probabilidad de denegación de servicio \n (lambda = {(1/mean_interarrival)*100}%   -   k = {q_limit+1})")
    plt.ylabel('Probabilidad')
    plt.xlabel('Cantidad de eventos')
    plt.show()  
    plt.pie([denial_prom[-1], 1-denial_prom[-1]], labels=["Denegación", "No denegación"], autopct="%0.1f %%")
    plt.title(f"Probabilidad de denegación de servicio \n (lambda = {(1/mean_interarrival)*100}%   -   k = {q_limit+1})")
    plt.show()
 
#Parameters
q_limit = 0
num_events = 2
mean_interarrival = 4/3
mean_service = 1
num_delays_required = 2500
 
iteraciones = 10
avg_array = []
minlen = 2147483648
 
print("Single-server queueing system")
print("Mean interarrival time: ", mean_interarrival, " minutes")
print("Mean service time", mean_service," minutes")
print("Number of customers: ", num_delays_required)
 
for i in range(iteraciones):
    initialize()
    while (num_custs_delayed < num_delays_required):
        timing()
        if (next_event_type == 0):
            arrive()
        elif (next_event_type == 1):
            depart()
        array_service_denial.append(q_overflows/(num_custs_delayed+q_overflows))
    avg_array.append(array_service_denial)
    if len(array_service_denial)<minlen:
        minlen = len(array_service_denial)
 
reportavg()