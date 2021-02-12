import numpy as np
import csv

from create_sqlite import create_connection
from insert_sqlite import get_all_indexes
from collections import defaultdict
from statistics import geometric_mean
from statistics import mean

# 64-bit datasets
XS_SIZE = 1.6e5
S_SIZE = 1.6e6
M_SIZE = 1.6e7
L_SIZE = 1.6e8

# 32-bit datasets
XS_SIZE_32 = 8e4
S_SIZE_32 = 8e5
M_SIZE_32 = 8e6
L_SIZE_32 = 8e7

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
        if 'uint64' in dataset:
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
        elif 'uint32' in dataset:
            if size == 0:
                # on-the-fly algorithm, put the latency in medium
                size_category = 'm'
            elif size < XS_SIZE_32:
                size_category = 'xs'
            elif size < S_SIZE_32:
                size_category = 's'
            elif size < M_SIZE_32:
                size_category = 'm'
            elif size < L_SIZE_32:
                size_category = 'l'
            else:
                size_category = 'xl'
        else:
            raise ValueError("Dataset name does not contain data type")
        
        dataset = dataset.split("_")[0] # Get shortened version of dataset, ie "fb" instead of "fb_200M_uint64"

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
                build_times[index_name][size_cat]["mean"] = mean(build_times[index_name][size_cat].values())
            else:
                build_times[index_name][size_cat]["mean"] = None
            latencies[index_name][size_cat]["mean"] = mean(latencies[index_name][size_cat].values())
            if all(sizes[index_name][size_cat].values()):
                sizes[index_name][size_cat]["mean"] = mean(sizes[index_name][size_cat].values())
            else:
                sizes[index_name][size_cat]["mean"] = None
    
    return latencies, build_times, sizes
    
def get_size_str(size):
    if size < 1e6:
        return str(round(size/1000, 2)) + " KB"
    elif size < 1e9:
        return str(round(size/1e6, 2)) + " MB"
    else:
        return str(round(size/1e9, 2)) + " GB"

if __name__ == "__main__":
    db = r"./indexes.db"
    
    latencies, build_times, sizes = get_ranked_indexes(db)
    headers = ["Name", "XS", "S", "M", "L", "XL", "Dataset"]
    with open("./_data/latency.csv", "w") as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow(headers)
        for index in latencies:
            writer.writerow([
                index,
                round(latencies[index]['xs']["mean"]) if 'xs' in latencies[index] and latencies[index]['xs']["mean"] is not None else ' ',
                round(latencies[index]['s']["mean"]) if 's' in latencies[index] and latencies[index]['s']["mean"] is not None else ' ',
                round(latencies[index]['m']["mean"]) if 'm' in latencies[index] and latencies[index]['m']["mean"] is not None else ' ',
                round(latencies[index]['l']["mean"]) if 'l' in latencies[index] and latencies[index]['l']["mean"] is not None else ' ',
                round(latencies[index]['xl']["mean"]) if 'xl' in latencies[index] and latencies[index]['xl']["mean"] is not None else ' ',
                "all"
            ])
    
    with open("./_data/buildtimes.csv", "w") as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow(headers)
        for index in build_times:
            writer.writerow([
                index,
                round(build_times[index]['xs']["mean"]) if 'xs' in build_times[index] and build_times[index]['xs']["mean"] is not None else ' ',
                round(build_times[index]['s']["mean"]) if 's' in build_times[index] and build_times[index]['s']["mean"] is not None else ' ',
                round(build_times[index]['m']["mean"]) if 'm' in build_times[index] and build_times[index]['m']["mean"] is not None else ' ',
                round(build_times[index]['l']["mean"]) if 'l' in build_times[index] and build_times[index]['l']["mean"] is not None else ' ',
                round(build_times[index]['xl']["mean"]) if 'xl' in build_times[index] and build_times[index]['xl']["mean"] is not None else ' ',
                "all"
            ])
    
    with open("./_data/sizes.csv", "w") as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow(headers)
        for index in sizes:
            writer.writerow([
                index,
                get_size_str(sizes[index]['xs']["mean"]) if 'xs' in sizes[index] and sizes[index]['xs']["mean"] is not None else ' ',
                get_size_str(sizes[index]['s']["mean"]) if 's' in sizes[index] and sizes[index]['s']["mean"] is not None else ' ',
                get_size_str(sizes[index]['m']["mean"]) if 'm' in sizes[index] and sizes[index]['m']["mean"] is not None else ' ',
                get_size_str(sizes[index]['l']["mean"]) if 'l' in sizes[index] and sizes[index]['l']["mean"] is not None else ' ',
                get_size_str(sizes[index]['xl']["mean"]) if 'xl' in sizes[index] and sizes[index]['xl']["mean"] is not None else ' ',
                "all"
            ])
    
    for dataset in (("books", "fb", "osm", "wiki")):
        with open(f"./_data/latency.csv", "a") as f:
            writer = csv.writer(f, delimiter=',')
            for index in latencies:
                writer.writerow([
                    index,
                    round(latencies[index]['xs'][dataset]) if 'xs' in latencies[index] and type(latencies[index]['xs'][dataset]) is not defaultdict else ' ',
                    round(latencies[index]['s'][dataset]) if 's' in latencies[index] and type(latencies[index]['s'][dataset]) is not defaultdict else ' ',
                    round(latencies[index]['m'][dataset]) if 'm' in latencies[index] and type(latencies[index]['m'][dataset]) is not defaultdict else ' ',
                    round(latencies[index]['l'][dataset]) if 'l' in latencies[index] and type(latencies[index]['l'][dataset]) is not defaultdict else ' ',
                    round(latencies[index]['xl'][dataset]) if 'xl' in latencies[index] and type(latencies[index]['xl'][dataset]) is not defaultdict else ' ',
                    dataset
                ])
        
        with open(f"./_data/buildtimes.csv", "a") as f:
            writer = csv.writer(f, delimiter=',')
            for index in build_times:
                writer.writerow([
                    index,
                    round(build_times[index]['xs'][dataset]) if 'xs' in build_times[index] and type(build_times[index]['xs'][dataset]) is not defaultdict else ' ',
                    round(build_times[index]['s'][dataset]) if 's' in build_times[index] and type(build_times[index]['s'][dataset]) is not defaultdict else ' ',
                    round(build_times[index]['m'][dataset]) if 'm' in build_times[index] and type(build_times[index]['m'][dataset]) is not defaultdict else ' ',
                    round(build_times[index]['l'][dataset]) if 'l' in build_times[index] and type(build_times[index]['l'][dataset]) is not defaultdict else ' ',
                    round(build_times[index]['xl'][dataset]) if 'xl' in build_times[index] and type(build_times[index]['xl'][dataset]) is not defaultdict else ' ',
                    dataset
                ])
        
        with open(f"./_data/sizes.csv", "a") as f:
            writer = csv.writer(f, delimiter=',')
            for index in sizes:
                writer.writerow([
                    index,
                    get_size_str(sizes[index]['xs'][dataset]) if 'xs' in sizes[index] and type(sizes[index]['xs'][dataset]) is not defaultdict else ' ',
                    get_size_str(sizes[index]['s'][dataset]) if 's' in sizes[index] and type(sizes[index]['s'][dataset]) is not defaultdict else ' ',
                    get_size_str(sizes[index]['m'][dataset]) if 'm' in sizes[index] and type(sizes[index]['m'][dataset]) is not defaultdict else ' ',
                    get_size_str(sizes[index]['l'][dataset]) if 'l' in sizes[index] and type(sizes[index]['l'][dataset]) is not defaultdict else ' ',
                    get_size_str(sizes[index]['xl'][dataset]) if 'xl' in sizes[index] and type(sizes[index]['xl'][dataset]) is not defaultdict else ' ',
                    dataset
                ])