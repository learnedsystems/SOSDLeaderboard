import numpy as np
import csv

from sql.create_sqlite import create_connection
from sql.insert_sqlite import get_all_indexes
from collections import defaultdict
from statistics import geometric_mean
from sklearn.metrics import auc

XS_SIZE = 1e5
S_SIZE = 1e6
M_SIZE = 1e7
L_SIZE = 1e8
XL_SIZE = 1e9

def rec_dd():
    """ Recursive nested defaultdict generating function """
    return defaultdict(rec_dd)

def get_ranked_indexes(dbname):
    build_times = rec_dd()
    latencies = rec_dd()
    sizes = rec_dd()
    conn = create_connection(dbname)
    all_indexes = get_all_indexes(conn)

    # Dictionaries have structure name -> size -> dataset -> variant -> time of that variant
    # First we'll process to get the lowest-latency variant on each dataset, then take the geometric
    # mean across datasets which gives us name -> size -> mean latency across datasets
    for name, variant, latency, size, build_time, searcher, dataset in all_indexes:
        # Could have been multiple runs for latency

        size_category = ''
        if size == 0:
            # on-the-fly algorithm, put the latency in medium
            size_category = 'm'
        elif size < XS_SIZE:
            size_category = 'xs'
        elif size < S_SIZE:
            size_category = 's'
        elif size < M_SIZE:
            size_category = 'm'
        elif size < L_SIZE:
            size_category = 'l'
        else:
            size_category = 'xl'
        
        build_times[name][size_category][dataset][variant] = build_time
        latencies[name][size_category][dataset][variant] = latency
        sizes[name][size_category][dataset][variant] = size

    for index_name in build_times:
        for size_cat in build_times[index_name]:
            for dataset_name in build_times[index_name][size_cat]:
                lowest_latency_variant = min(latencies[index_name][size_cat][dataset_name],
                    key = latencies[index_name][size_cat][dataset_name].get)
                build_times[index_name][size_cat][dataset_name] = build_times[index_name][size_cat][dataset_name][lowest_latency_variant]
                latencies[index_name][size_cat][dataset_name] = latencies[index_name][size_cat][dataset_name][lowest_latency_variant]
                sizes[index_name][size_cat][dataset_name] = sizes[index_name][size_cat][dataset_name][lowest_latency_variant]

    for index_name in build_times:
        for size_cat in build_times[index_name]:
            # Possibly filed with zeros
            if all(build_times[index_name][size_cat].values()):
                build_times[index_name][size_cat] = geometric_mean(build_times[index_name][size_cat].values())
            else:
                build_times[index_name][size_cat] = None
            latencies[index_name][size_cat] = geometric_mean(latencies[index_name][size_cat].values())
            if all(sizes[index_name][size_cat].values()):
                sizes[index_name][size_cat] = geometric_mean(sizes[index_name][size_cat].values())
            else:
                sizes[index_name][size_cat] = None
    
    return latencies, build_times, sizes

def compute_improvement(pareto_points, index):
    points = pareto_points[index]
    points.sort()

    x = np.array([point[0] for point in points])
    y = np.array([point[1] for point in points])
    return auc(x, y)

if __name__ == "__main__":
    db = r"./indexes.db"
    
    latencies, build_times, sizes = get_ranked_indexes(db)
    print(latencies)
