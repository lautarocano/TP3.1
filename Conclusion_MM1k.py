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

 
#Parameters
q_limit = 10
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

avgReport = []
for i in range(2):
    avgReport.append([])
    for j in range(24):
        avgReport[i].append(0)

while (mean_interarrival>=0.7):
    print("Procesando (", index,"/ 23 )...")
    for i in (range(iteraciones)):
        initialize()
         
        while (num_custs_delayed < num_delays_required):
            timing()
            if (next_event_type == 0):
                arrive()
            elif (next_event_type == 1):
                depart()
               
        avgReport[0][index] += num_custs_delayed/(num_custs_delayed+q_overflows)/iteraciones
        avgReport[1][index] += q_overflows/(num_custs_delayed+q_overflows)/iteraciones

    count += paso
    mean_interarrival = 1/count
    index += 1

x  = arange(0.25, 1.41, 0.05)

plt.plot(x,avgReport[0], color = 'g', label="Atendidos")
plt.plot(x,avgReport[1], color = 'r', label="Rechazados")
plt.title("Proporción de clientes atendidos y rechazados")
plt.legend(loc="upper right")
plt.ylabel('Porcentaje de clientes')
plt.xlabel('Rho')
plt.show()from random import random
from math import log
import matplotlib.pyplot as plt
from numpy import arange
 
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

 
#Parameters
q_limit = 10
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

avgReport = []
for i in range(2):
    avgReport.append([])
    for j in range(24):
        avgReport[i].append(0)

while (mean_interarrival>=0.7):
    print("Procesando (", index,"/ 23 )...")
    for i in (range(iteraciones)):
        initialize()
         
        while (num_custs_delayed < num_delays_required):
            timing()
            if (next_event_type == 0):
                arrive()
            elif (next_event_type == 1):
                depart()
               
        avgReport[0][index] += num_custs_delayed/(num_custs_delayed+q_overflows)/iteraciones
        avgReport[1][index] += q_overflows/(num_custs_delayed+q_overflows)/iteraciones

    count += paso
    mean_interarrival = 1/count
    index += 1

x  = arange(0.25, 1.41, 0.05)

plt.plot(x,avgReport[0], color = 'g', label="Atendidos")
plt.plot(x,avgReport[1], color = 'r', label="Rechazados")
plt.title("Proporción de clientes atendidos y rechazados")
plt.legend(loc="upper right")
plt.ylabel('Porcentaje de clientes')
plt.xlabel('Rho')
plt.show()