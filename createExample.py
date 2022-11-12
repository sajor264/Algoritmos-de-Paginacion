import random

procesos = 30
sizes = ["128", "256", "512", "1024", "2048", "4096", "8192", "16384"]
ptr = 0

file = open("procesos.txt", "w")
file.write("PID, Ptr, Size\n")
for procesos in range(1, procesos):
    for i in range(random.randint(2,10)):
        ptr += 1
        ptrStr = str(ptr)
        while len(ptrStr) < 3:
            ptrStr = "0" + ptrStr
        size = random.choice(sizes)
        line = str(procesos) + ",   " + ptrStr + ", " + str(size) + "\n" 
        file.write(line)
file.close()