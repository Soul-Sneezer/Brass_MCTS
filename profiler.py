import time
import tracemalloc
from functools import wraps
from typing import Dict, List, Tuple
import matplotlib.pyplot as plt
import numpy as np

class PerformanceRecorder:
    def __init__(self):
        self.metrics: Dict[str, List[Tuple[float, float]]] = {}

    def clear(self):
        self.metrics.clear()

recorder = PerformanceRecorder()
plt.style.use('seaborn-v0_8-dark-palette')

def record_performance(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        tracemalloc.start()
        start_time = time.perf_counter()
        result = func(self, *args, **kwargs)

        duration = time.perf_counter() - start_time
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        func_name = func.__name__
        if func_name not in recorder.metrics:
            recorder.metrics[func_name] = []

        recorder.metrics[func_name].append((duration, peak / 1024**2))  # duration, memory in MB

        return result
    return wrapper

def plot_performance():
    plt.figure(figsize=(8, 6))
    func_names = []
    total_times = []

    # Peak Memory Usage per Call
    plt.subplot(2, 2, 1)
    for func_name, metrics in recorder.metrics.items():
        mem_usage = [m[1] for m in metrics]
        plt.plot(mem_usage, label=func_name, alpha=0.7)
    plt.title("Peak Memory Usage per Call")
    plt.ylabel("MB")
    plt.xlabel("Call Index")
    plt.legend()

    # Boxplot for Execution Times
    plt.subplot(2, 2, 2)
    for func_name, metrics in recorder.metrics.items():
        total_time = sum(duration for duration, _ in recorder.metrics[func_name])
        func_names.append(func_name)
        total_times.append(total_time)

    plt.bar(func_names, total_times, color='skyblue')
    plt.title("Total Time Spent Per Function")
    plt.ylabel("Total Execution Time")
    plt.xticks(rotation=45)

    #data = [[m[0] for m in metrics] for metrics in recorder.metrics.values()]
    #plt.boxplot(data, labels=recorder.metrics.keys())
    #plt.title("Execution Time Spread")
    #plt.ylabel("Seconds")

    for func_name, metrics in recorder.metrics.items():
        total_time = sum(duration for duration, _ in recorder.metrics[func_name])
        print(f"Total time spent in function {func_name}: {total_time:.4f} seconds")

    plt.tight_layout()
    plt.show()

def add_percentiles(ax, data):
    for p in [25, 50, 75]:
        ax.axhline(np.percentile(data, p), color='red', linestyle='--', alpha=0.3)
