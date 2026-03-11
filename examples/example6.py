import threading
import queue
import time
import random
import math
import functools
import json


class LRUCache:
    def __init__(self, capacity=5):
        self.capacity = capacity
        self.cache = {}
        self.order = []

    def get(self, key):
        if key not in self.cache:
            return None
        self.order.remove(key)
        self.order.append(key)
        return self.cache[key]

    def put(self, key, value):
        if key in self.cache:
            self.order.remove(key)
        elif len(self.cache) >= self.capacity:
            oldest = self.order.pop(0)
            del self.cache[oldest]

        self.cache[key] = value
        self.order.append(key)


def memoize_with_lru(capacity=5):
    cache = LRUCache(capacity)

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args):
            cached = cache.get(args)
            if cached is not None:
                return cached
            result = func(*args)
            cache.put(args, result)
            return result
        return wrapper
    return decorator


@memoize_with_lru(capacity=10)
def expensive_computation(x):
    time.sleep(0.05)
    return math.sqrt(x) * math.sin(x) + math.log(x + 1)


class Worker(threading.Thread):
    def __init__(self, task_queue, result_queue, worker_id):
        super().__init__()
        self.task_queue = task_queue
        self.result_queue = result_queue
        self.worker_id = worker_id
        self.daemon = True

    def run(self):
        while True:
            try:
                task = self.task_queue.get(timeout=1)
            except queue.Empty:
                break

            result = expensive_computation(task)
            processed = {
                "worker": self.worker_id,
                "input": task,
                "output": result,
                "timestamp": time.time()
            }

            self.result_queue.put(processed)
            self.task_queue.task_done()


class DataPipeline:
    def __init__(self, num_workers=4):
        self.task_queue = queue.Queue()
        self.result_queue = queue.Queue()
        self.workers = [Worker(self.task_queue, self.result_queue, i) for i in range(num_workers)]

    def add_tasks(self, tasks):
        for t in tasks:
            self.task_queue.put(t)

    def run(self):
        for w in self.workers:
            w.start()

        self.task_queue.join()

        results = []
        while not self.result_queue.empty():
            results.append(self.result_queue.get())

        return results


class ResultAnalyzer:
    def __init__(self, results):
        self.results = results

    def statistics(self):
        outputs = [r["output"] for r in self.results]
        if not outputs:
            return {}

        mean = sum(outputs) / len(outputs)
        variance = sum((x - mean) ** 2 for x in outputs) / len(outputs)

        return {
            "count": len(outputs),
            "mean": mean,
            "variance": variance,
            "max": max(outputs),
            "min": min(outputs)
        }

    def group_by_worker(self):
        grouped = {}
        for r in self.results:
            grouped.setdefault(r["worker"], []).append(r["output"])
        return grouped

    def export_json(self, path):
        with open(path, "w") as f:
            json.dump(self.results, f, indent=4)


def generate_tasks(n=50):
    return [random.randint(1, 1000) for _ in range(n)]


def main():
    tasks = generate_tasks()

    pipeline = DataPipeline(num_workers=6)
    pipeline.add_tasks(tasks)

    results = pipeline.run()

    analyzer = ResultAnalyzer(results)
    stats = analyzer.statistics()

    print("Statistics:")
    for k, v in stats.items():
        print(f"{k}: {v}")

    grouped = analyzer.group_by_worker()
    print("\nWorker Distribution:")
    for worker, outputs in grouped.items():
        print(f"Worker {worker} processed {len(outputs)} tasks")

    analyzer.export_json("results.json")


if __name__ == "__main__":
    main()