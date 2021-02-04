import numpy as np
import csv

from create_sqlite import create_connection
from insert_sqlite import get_all_indexes
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
    for entry_id, name, variant, latency, size, build_time, searcher, dataset in all_indexes:
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
    headers = ["Name", "XS", "S", "M", "L", "XL"]
    with open("./_data/latency.csv", "w") as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow(headers)
        for index in latencies:
            writer.writerow([
                index,
                latencies[index].get('xs', ' '),
                latencies[index].get('s', ' '),
                latencies[index].get('m', ' '),
                latencies[index].get('l', ' '),
                latencies[index].get('xl', ' '),
            ])
    
    with open("./_data/buildtimes.csv", "w") as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow(headers)
        for index in build_times:
            writer.writerow([
                index,
                build_times[index].get('xs', ' '),
                build_times[index].get('s', ' '),
                build_times[index].get('m', ' '),
                build_times[index].get('l', ' '),
                build_times[index].get('xl', ' ')
            ])
    
    with open("./_data/sizes.csv", "w") as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow(headers)
        for index in sizes:
            writer.writerow([
                index,
                sizes[index]['xs']/1000 if 'xs' in sizes[index] and sizes[index]['xs'] is not None else ' ',
                sizes[index]['s']/1000 if 's' in sizes[index] and sizes[index]['s'] is not None else ' ',
                sizes[index]['m']/1000 if 'm' in sizes[index] and sizes[index]['m'] is not None else ' ',
                sizes[index]['l']/1000 if 'l' in sizes[index] and sizes[index]['l'] is not None else ' ',
                sizes[index]['xl']/1000 if 'xl' in sizes[index] and sizes[index]['xl'] is not None else ' '
            ])