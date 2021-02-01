import numpy as np

from jinja2 import Environment, FileSystemLoader
from create_sqlite import create_connection
from insert_sqlite import get_all_indexes
from collections import defaultdict
from statistics import median
from sklearn.metrics import auc

def get_ranked_indexes(dbname):
    build_times = defaultdict(dict)
    latencies = defaultdict(dict)
    sizes = defaultdict(dict)
    conn = create_connection(dbname)
    all_indexes = get_all_indexes(conn)
    pareto_points = defaultdict(list)

    # Get the median latency, build time, and size for each index for each size
    for name, variant, size, *latency, build_time, searcher in all_indexes:
        pareto_points[name].append((size, latency))

        size_category = ''
        if size == 0:
            # on-the-fly algorithm, put the latency in medium
            size_category = 'm'
        elif size < 100:
            size_category = 'xs'
        elif size < 500:
            size_category = 's'
        elif size < 1000:
            size_category = 'm'
        elif size < 5000:
            size_category = 'l'
        else:
            size_category = 'xl'
        if name in latencies:
            if size_category in latencies[name]:
                latencies[name][size_category].append(latency)
                build_times[name][size_category].append(build_time)
                sizes[name][size_category].append(size)
            else:
                latencies[name][size_category] = [latency]
                build_times[name][size_category] = [build_time]
                sizes[name][size_category] = [size]

        for index in latencies:
            for size_category in latencies[index]:
                latencies[index][size_category] = median(latencies[name][size_category])
                build_times[index][size_category] = median(build_times[name][size_category])
                sizes[name][size_category] = median(sizes[name][size_category])
        
        result = []
        for index in latencies:
            result.append(dict(name=index, 
                            xsmalltime=latencies[index]['xs'] or ' ',
                            smalltime=latencies[index]['s'] or ' ',
                            mediumtime=latencies[index]['m'] or ' ',
                            largetime=latencies[index]['l'] or ' ',
                            xlargetime=latencies[index]['xl'] or ' ',
                            improvement=compute_improvement(pareto_points, index)))
        
        result.sort(key=lambda x: x["improvement"], reverse=True)
        for idx, d in enumerate(result):
            d["rank"] = idx + 1
        return result

def compute_improvement(pareto_points, index):
    points = pareto_points[index]
    points.sort()

    x = np.array([point[0] for point in points])
    y = np.array([point[1] for point in points])
    return auc(x, y)

if __name__ == "__main__":
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('template.html')

    dbname = r"./sqlite/indexes.db"
    indexes = get_ranked_indexes(dbname)

    output_from_parsed_template = template.render(indexes=indexes)
    with open("index.html", "w") as filetowrite:
        filetowrite.write(output_from_parsed_template)