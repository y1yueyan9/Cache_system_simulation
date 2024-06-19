import random
import time

from tqdm import tqdm  # 导入tqdm库
from collections import OrderedDict
import matplotlib.pyplot as plt
import numpy as np

hit_time_delay = 0.0001
inhit_time_delay = 0.003
Cache_Capacity = 10
Total_Num = 100
Lower_Bound = 1
Upper_Bound = 30
mean = 15
std_dev = 5

def basic_test(cache_algorithm, data, data_description):
    processed_requests = 0
    start_time = time.time()
    cache = cache_algorithm(Cache_Capacity, data=data)  # 为缓存算法传递数据

    # 顺序访问数据
    for item in tqdm(data, desc=f"Testing {cache_algorithm.__name__} With {data_description} (Sequential Access)", mininterval=0.5, miniters=1):
        cache.access(item)
    hit_rate = cache.hit_rate()
    processed_requests += cache.hits
    print(f"{cache_algorithm.__name__} Cache Hit Rate (Sequential Access): {hit_rate * 100}%")

    # 清空缓存
    cache.clear()
    time.sleep(0.01)

    # 逆序访问数据
    reversed_data = list(reversed(data))
    for item in tqdm(reversed_data, desc=f"Testing {cache_algorithm.__name__} With {data_description} (Reverse Access)", mininterval=0.5, miniters=1):
        cache.access(item)
    hit_rate = cache.hit_rate()
    print(f"{cache_algorithm.__name__} Cache Hit Rate (Reverse Access): {hit_rate * 100}%")

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"{cache_algorithm.__name__} execution time: {execution_time} seconds")
    processed_requests += cache.hits
    throughput = processed_requests / execution_time
    print(f"{cache_algorithm.__name__} Throughput: {throughput} requests/second")

    return cache  # 返回缓存对象


class FIFOCache:
    def __init__(self, capacity, data):
        self.capacity = capacity
        self.cache = []
        self.hits = 0
        self.leng_of_data = len(data)
        self.hit_time_delay = hit_time_delay  # 设置命中时间开销为hit_time_delay秒
        self.inhit_time_delay = inhit_time_delay  # 设置命中时间开销为hit_time_delay秒
    def access(self, item):
        if item not in self.cache:
            if len(self.cache) >= self.capacity:
                self.cache.pop(0)
            self.cache.append(item)
            time.sleep(self.inhit_time_delay)
        else:
            self.hits += 1  # 项目已存在时递增
            time.sleep(self.hit_time_delay)

    def clear(self):
        self.cache = []
        self.hits = 0

    def hit_rate(self):
        if not self.cache:
            return 0
        return self.hits / self.leng_of_data




class LRUCache:
    def __init__(self, capacity, data=None):
        self.capacity = capacity
        self.cache = OrderedDict()
        self.hits = 0
        self.leng_of_data = len(data) if data else 0
        self.hit_time_delay = hit_time_delay  # 设置命中时间开销为hit_time_delay秒
        self.inhit_time_delay = inhit_time_delay  # 设置命中时间开销为hit_time_delay秒
    def access(self, key):
        if key in self.cache:
            # 如果键已存在，移动到字典末尾表示最近使用
            self.cache.move_to_end(key)
            self.hits += 1  # 项目已存在时递增
            time.sleep(self.hit_time_delay)
        else:
            if len(self.cache) >= self.capacity:
                # 如果缓存已满，移除字典开头的键（最少使用的）
                self.cache.popitem(last=False)
            # 插入新键到字典末尾
            self.cache[key] = None
            time.sleep(self.inhit_time_delay)

    def clear(self):
        self.cache.clear()
        self.hits = 0

    def hit_rate(self):
        if not self.cache:
            return 0
        return self.hits / self.leng_of_data

class LFUCache:
    def __init__(self, capacity, data):
        self.capacity = capacity
        self.cache = {}
        self.frequency = {}
        self.hits = 0
        self.leng_of_data = len(data)
        self.hit_time_delay = hit_time_delay  # 设置命中时间开销为hit_time_delay秒
        self.inhit_time_delay = inhit_time_delay  # 设置命中时间开销为hit_time_delay秒
    def access(self, key):
        if key in self.cache:
            # 如果键已存在，更新频率并增加命中次数
            self.frequency[key] += 1
            self.hits += 1
            time.sleep(self.hit_time_delay)
        else:
            if len(self.cache) >= self.capacity:
                # 如果缓存已满，移除最少使用的键
                min_frequency_key = min(self.frequency, key=self.frequency.get)
                del self.cache[min_frequency_key]
                del self.frequency[min_frequency_key]
            time.sleep(self.inhit_time_delay)
            # 插入新键
            self.cache[key] = None
            self.frequency[key] = 1

    def clear(self):
        self.cache = {}
        self.frequency = {}
        self.hits = 0

    def hit_rate(self):
        if not self.cache:
            return 0
        return self.hits / self.leng_of_data

class MRUCache:
    def __init__(self, capacity, data):
        self.capacity = capacity
        self.cache = []
        self.hits = 0
        self.leng_of_data = len(data)
        self.hit_time_delay = hit_time_delay  # 设置命中时间开销为hit_time_delay秒
        self.inhit_time_delay = inhit_time_delay  # 设置命中时间开销为hit_time_delay秒
    def access(self, item):
        if item in self.cache:
            # 如果项目已存在，将其移到列表的末尾
            self.cache.remove(item)
            self.hits += 1  # 递增命中次数
            time.sleep(self.hit_time_delay)
        else:
            if len(self.cache) >= self.capacity:
                # 如果缓存已满，移除最近最少使用的项目（列表末尾）
                self.cache.pop()
            time.sleep(self.inhit_time_delay)
        # 插入或将项目移到列表的末尾
        self.cache.append(item)


    def clear(self):
        self.cache = []
        self.hits = 0

    def hit_rate(self):
        if not self.cache:
            return 0
        return self.hits / self.leng_of_data

class RRCache:
    def __init__(self, capacity, data):
        self.capacity = capacity
        self.cache = []
        self.hits = 0
        self.leng_of_data = len(data)
        self.hit_time_delay = hit_time_delay  # 设置命中时间开销为hit_time_delay秒
        self.inhit_time_delay = inhit_time_delay  # 设置命中时间开销为hit_time_delay秒
    def access(self, item):
        if item not in self.cache:
            if len(self.cache) >= self.capacity:
                # 如果缓存已满，随机选择一个项目进行替换
                index_to_replace = random.randint(0, self.capacity - 1)
                self.cache[index_to_replace] = item
            else:
                # 缓存未满，直接添加项目
                self.cache.append(item)
            time.sleep(self.inhit_time_delay)
        else:
            self.hits += 1  # 递增命中次数
            time.sleep(self.hit_time_delay)

    def clear(self):
        self.cache = []
        self.hits = 0

    def hit_rate(self):
        if not self.cache:
            return 0
        return self.hits / self.leng_of_data

class ARCCache:
    def __init__(self, capacity, data):
        self.capacity = capacity
        self.T1 = []  # 经常使用但最近未使用的项目的队列
        self.T2 = []  # 最近使用的项目的队列
        self.B1 = []  # T1的伪队列
        self.B2 = []  # T2的伪队列
        self.leng_of_data = len(data)
        self.hits = 0
        self.hit_time_delay = hit_time_delay  # 设置命中时间开销为hit_time_delay秒
        self.inhit_time_delay = inhit_time_delay  # 设置命中时间开销为hit_time_delay秒
    def access(self, key):
        if key in self.T1:
            self.T1.remove(key)
            self.T2.insert(0, key)  # Move to T2's head
            self.hits += 1
            time.sleep(self.hit_time_delay)
        elif key in self.T2:
            self.T2.remove(key)
            self.T2.insert(0, key)  # Keep in T2's head
            self.hits += 1
            time.sleep(self.hit_time_delay)
        else:
            if len(self.T1) + len(self.T2) >= self.capacity:
                self.replace()
            if len(self.T1) < self.capacity - len(self.T2):
                self.T1.insert(0, key)
            else:
                self.T2.insert(0, key)
            time.sleep(self.inhit_time_delay)

    def replace(self):
        if len(self.T1) > 0 and ((len(self.T2) == 0) or (len(self.T2) > 0 and len(self.T1) / len(self.T2)) > (
                len(self.B2) / max(1, len(self.B1)))):
            evicted_key = self.T1.pop()
            self.B1.insert(0, evicted_key)
        else:
            evicted_key = self.T2.pop()
            self.B2.insert(0, evicted_key)

    def adjust(self):
        p = min(len(self.B1), self.capacity - len(self.T1))
        self.T1.extend(self.B1[:p])
        del self.B1[:p]

        p = min(len(self.B2), self.capacity - len(self.T2))
        self.T2.extend(self.B2[:p])
        del self.B2[:p]

    def clear(self):
        self.T1 = []  # Queue for frequently used but recently not used items
        self.T2 = []  # Queue for recently used items
        self.B1 = []  # Pseudo-queue for T1 evictions
        self.B2 = []  # Pseudo-queue for T2 evictions
        self.hits = 0
    def hit_rate(self):
        if self.leng_of_data == 0:
            return 0.0
        return self.hits / self.leng_of_data



class ClockCache:
    def __init__(self, capacity, data):
        self.capacity = capacity
        self.cache = {}
        self.access_bits = {}
        self.pointer = 0
        self.hits = 0
        self.leng_of_data = len(data)
        self.hit_time_delay = hit_time_delay  # 设置命中时间开销为hit_time_delay秒
        self.inhit_time_delay = inhit_time_delay  # 设置命中时间开销为hit_time_delay秒
    def access(self, key):
        if key in self.cache:
            # 如果键已存在，设置访问位为1
            self.access_bits[key] = 1
            self.hits += 1
            time.sleep(self.hit_time_delay)
        else:
            # 页面不在缓存中，执行替换策略
            time.sleep(self.inhit_time_delay)
            while True:
                if self.access_bits.get(self.pointer) == 0:
                    # 找到访问位为0的页面，替换之
                    #evict_key = next((k for k, v in self.cache.items() if self.access_bits.get(k) == 0), None)
                    evict_key = None  # 默认值为 None
                    for k, v in self.cache.items():
                        if self.access_bits.get(k) == 0:
                            evict_key = k
                            break
                    if evict_key:
                        del self.cache[evict_key]
                        del self.access_bits[evict_key]

                    self.cache[key] = None
                    self.access_bits[key] = 1
                    self.pointer = (self.pointer + 1) % self.capacity
                    break
                else:
                    # 将访问位设为0，继续扫描
                    self.access_bits[self.pointer] = 0
                    self.pointer = (self.pointer + 1) % self.capacity

    def clear(self):
        self.cache = {}
        self.access_bits = {}
        self.pointer = 0
        self.hits = 0

    def hit_rate(self):
        if not self.cache:
            return 0
        total_hits = sum(self.access_bits.values())
        return self.hits / self.leng_of_data

def visualize_results(algorithms, datas):
    # 设置中文字体
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 或者 ['Microsoft YaHei']
    plt.rcParams['axes.unicode_minus'] = False

    metrics = ['命中率', '运行时间', '吞吐量']
    colors = ['skyblue', 'lightcoral', 'lightgreen', 'orange', 'purple']
    markers = ['o', 's', '^', 'd', 'v']
    linestyles = ['-', '--', ':', '-.', '--']

    for j, metric in enumerate(metrics):
        # 创建图表
        plt.figure(figsize=(10, 6))
        plt.title(f'不同缓存算法在{metric}上的对比')

        for i, data in enumerate(datas):
            metric_values = []

            # 定义计时变量
            start_time = 0
            end_time = 0

            for algorithm in algorithms:
                # 进行基本测试并获取指标值
                if metric == '命中率':
                    cache = basic_test(algorithm, data, f'{["随机", "顺序", "周期", "重复", "高斯"][i]} 数据')
                    metric_value = cache.hit_rate()
                elif metric == '运行时间':
                    start_time = time.time()
                    basic_test(algorithm, data, f'{["随机", "顺序", "周期", "重复", "高斯"][i]} 数据')
                    end_time = time.time()
                    metric_value = end_time - start_time
                elif metric == '吞吐量':
                    start_time = time.time()
                    cache = basic_test(algorithm, data, f'{["随机", "顺序", "周期", "重复", "高斯"][i]} 数据')
                    end_time = time.time()
                    metric_value = cache.hits / (end_time - start_time) if cache.hits > 0 else 0

                metric_values.append(metric_value)

            # 在图表中绘制折线图
            algorithm_names = [algorithm.__name__ for algorithm in algorithms]  # 获取算法的名称
            color = colors[i % len(colors)]  # 使用取余来保证索引不越界
            marker = markers[i % len(markers)]
            linestyle = linestyles[i % len(linestyles)]
            plt.plot(algorithm_names, metric_values, label=f'{["随机", "顺序", "周期", "重复", "高斯"][i]} 数据', color=color, marker=marker, linestyle=linestyle)

        # 添加图例、坐标轴标签
        plt.legend()
        plt.xlabel('缓存算法')
        plt.ylabel(metric)

        # 显示网格线
        plt.grid(True, linestyle='--', alpha=0.7)

        # 调整坐标轴刻度
        plt.xticks(rotation=45)

        # 显示图表
        plt.show()
# 在 main 函数中调用 visualize_results(algorithms, datas)



def main():
    # 测试用例
    data_random = [random.randint(Lower_Bound, Upper_Bound) for _ in range(Total_Num)] #随机数据
    data_shunxu = [i for i in range(Lower_Bound, Total_Num)]  # 顺序生成
    data_zhouqi = [int((Lower_Bound+ Upper_Bound) / 2 + 30 * np.sin(2 * np.pi * i / 100)) for i in range(Total_Num)]  #周期生成
    data_chongfu = [i for i in range(10)] * int(Total_Num / 10)  # 重复模式
    data_gaosi = [int(np.random.normal(mean, std_dev)) for _ in range(Total_Num)] #高斯模式

    algorithms = [FIFOCache, LRUCache, LFUCache, MRUCache, RRCache, ARCCache]
    datas = [data_random, data_shunxu, data_zhouqi, data_chongfu, data_gaosi]

    visualize_results(algorithms, datas)


if __name__ == "__main__":
    main()