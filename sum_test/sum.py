import subprocess
import time
import matplotlib.pyplot as plt
import concurrent.futures


executables_list = [
    {
        "name": "normal",
        "executable": "./sum1.exe",
    },
    {
        "name": "parallel",
        "executable": "./sum2.exe",
    }
]


for n in range(len(executables_list)):
    executable = executables_list[n]["executable"]
    name = executables_list[n]["name"]

    print(f"Running {name}...")
    start = time.perf_counter()
    proc = subprocess.run([executable], text=True, capture_output=True)
    end = time.perf_counter()

    print(f"Tempo de execução do {name}: {end - start:0.4f} segundos")