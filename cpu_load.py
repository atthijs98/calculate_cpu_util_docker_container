import docker
import time
import json


def calculate_utilization(stats):
    cpu_util_list = []
    for s in stats:
        if s["precpu_stats"]["cpu_usage"]["total_usage"] == 0:
            continue
        else:
            cpu_percent = 0.0
            cpu_delta = s["cpu_stats"]["cpu_usage"]["total_usage"] - s["precpu_stats"]["cpu_usage"]["total_usage"]
            system_delta = s["cpu_stats"]["system_cpu_usage"] - s["precpu_stats"]["system_cpu_usage"]

            if system_delta > 0.0 and cpu_delta > 0.0:
                cpu_percent = (cpu_delta / system_delta) * len(s["cpu_stats"]["cpu_usage"]["percpu_usage"]) * 100.0

            cpu_util_list.append(cpu_percent)
    return cpu_util_list


def get_cpu_util_average(util_list):
    average = sum(util_list) / len(util_list)
    return round(average, 2)


if __name__ == '__main__':
    client = docker.from_env()
    container = client.containers.get("28d1637d3b02")
    time_end = time.time() + 60 * 1
    stats_list = []

    for stat in container.stats():
        stat_str = stat.decode('utf-8')
        stat_json = json.loads(stat_str)
        stats_list.append(stat_json)
        if time.time() > time_end:
            break

    cpu_utilization_list = calculate_utilization(stats_list)
    print(cpu_utilization_list)
    cpu_utilization_average = get_cpu_util_average(cpu_utilization_list)
    print("The average over 1 minute = " + str(cpu_utilization_average) + "%")
