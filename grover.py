#! /home/lenuuks/miniconda3/envs/qc/bin/python3.7
import sys
import numpy as np
import matplotlib.pyplot as plt
from qiskit import  QuantumRegister, ClassicalRegister, execute, QuantumCircuit, Aer
from qiskit import IBMQ
from qiskit.providers.ibmq import least_busy

IBMQ.load_accounts()

# index to be 'found'
if len(sys.argv) != 4:
    sys.exit("ERROR: wrong number of arguments.")
x,y = int(sys.argv[2]),int(sys.argv[3])
if not x in range(2) or not y in range(2):
    sys.exit("ERROR: indices out of bounds.")

# Define the Quantum and Classical Registers
q = QuantumRegister(2)
c = ClassicalRegister(2)

# Build the circuits
circ = QuantumCircuit(q, c)
#create superposition
circ.h(q[0])
circ.h(q[1])
circ.barrier()
# construct oracle depending on indices
if x==1 and y==1:
    circ.h(q[1])
    circ.cx(q[0],q[1])
    circ.h(q[1])
elif x==0 and y==1:
    circ.s(q[0])
    circ.barrier()
    circ.h(q[1])
    circ.cx(q[0],q[1])
    circ.h(q[1])
    circ.barrier()
    circ.s(q[0])        
elif x==1 and y==0:
    circ.s(q[1])
    circ.h(q[1])
    circ.cx(q[0],q[1])
    circ.h(q[1])
    circ.s(q[1])
else:
    if sys.argv[1] == "my_version":
        circ.x(q[0])
        circ.x(q[1])
        circ.h(q[1])
        circ.cx(q[0],q[1])
        circ.h(q[1])
        circ.barrier()
        circ.x(q[0])
        circ.x(q[1])
    elif sys.argv[1] == "ibm_version":
        # different oracle for 00
        circ.s(q[0])
        circ.s(q[1])
        circ.h(q[1])
        circ.cx(q[0],q[1])
        circ.h(q[1])
        circ.barrier()
        circ.s(q[0])
        circ.s(q[1])
    else:
        sys.exit("ERROR: first argument has to be either ibm_version or my_version.")

#reflection on superposition state
circ.barrier()
circ.h(q[0])
circ.h(q[1])

#grover operator
if sys.argv[1] == "my_version":
    circ.z(q[0])
    circ.z(q[1])
    circ.h(q[1])
    circ.cx(q[0],q[1])
    circ.h(q[1])
elif sys.argv[1] == "ibm_version":
    circ.x(q[0])
    circ.x(q[1])
    circ.h(q[1])
    circ.cx(q[0],q[1])
    circ.h(q[1])
    circ.barrier()
    circ.x(q[0])
    circ.x(q[1])

circ.barrier()
circ.h(q[0])
circ.h(q[1])
# measurement
circ.barrier()
circ.measure(q[0], c[0])
circ.measure(q[1], c[1])


# Execute the circuits
shots = 256
backend = least_busy(IBMQ.backends(filters=lambda x: not x.configuration().simulator))
print("Backend: ", backend.name())
#backend=Aer.get_backend('qasm_simulator')
job = execute(circ,backend=backend, shots=shots, max_credits=10)
result = job.result()
print(result.get_counts(circ))


# Circuit visualization
from qiskit.tools.visualization import circuit_drawer
circuit_drawer(circ, filename="circ"+str(x)+str(y), plot_barriers=False, output="mpl")
