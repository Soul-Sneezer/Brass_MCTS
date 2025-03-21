import time
import tracemalloc
import matplotlib.pyplot as plt 
from functools import wraps
from typing import Dict, List, Tuple 
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
        recorder.metrics[func_name].append((duration, peak / 1024**2)) # Convert to MB 

        return result 
    return wrapper

def plot_performance():
    plt.figure(figsize=(15,10))

    plt.subplot(2, 2, 1)
    for func_name, metrics in recorder.metrics.items():
        times = [m[0] for m in metrics]
        plt.plot(times, label=func_name, alpha=0.7)
    plt.title("Execution Time per Call")
    plt.ylabel("Seconds")
    plt.legend()

    # Memory usage plot 
    plt.subplot(2, 2, 2)
    for func_name, metrics in recorder.metrics.items():
        mem_usage = [m[1] for m in metrics]
        plt.plot(mem_usage, label=func_name, alpha=0.7)
    plt.title("Peak Memory Usage per Call")
    plt.ylabel("MB")
    plt.legend()

    # Histograms
    plt.subplot(2, 2, 3)
    bins = np.linspace(0, max(m[0] for metrics in recorder.metrics.values() for m in metrics), 20)
    for func_name, metrics in recorder.metrics.items():
        times = [m[0] for m in metrics]
        plt.hist(times, bins=bins, alpha=0.5, label=func_name)
    plt.title("Execution Time Distribution")
    plt.xlabel("Seconds")
    plt.legend()

    # Box plots
    plt.subplot(2, 2, 4)
    data = [[m[0] for m in metrics] for metrics in recorder.metrics.values()]
    plt.boxplot(data, labels=recorder.metrics.keys())
    plt.title("Execution Time Spread")
    plt.ylabel("Seconds")
    
    plt.tight_layout()
    plt.show()

def add_percentiles(ax, data):
    for p in [25, 50, 75]:
        ax.axhline(np.percentile(data, p), color='red', linestyle='--', alpha=0.3)
