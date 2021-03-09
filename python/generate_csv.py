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

REAL_DATASETS_64 = ["wiki_ts_200M_uint64", "osm_cellids_200M_uint64", "fb_200M_uint64", "books_200M_uint64"]
REAL_DATASETS_32 = ["wiki_ts_200M_uint32", "osm_cellids_200M_uint32", "fb_200M_uint32", "books_200M_uint32"]

def rec_dd():
    """ Recursive nested defaultdict generating function """
    return defaultdict(rec_dd)

# Get all ranked indexes that are uint64, also calculate the average of uint64 functions
def get_ranked_indexes_uint64(dbname):
    build_times = rec_dd()
    latencies = rec_dd()
    sizes = rec_dd()
    conn = create_connection(dbname)
    all_indexes = get_all_indexes(conn)
    datasets = set()

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
            continue
        else:
            raise ValueError("Dataset name does not contain data type")

        build_times[name][size_category][dataset][variant] = build_time
        latencies[name][size_category][dataset][variant] = latency
        sizes[name][size_category][dataset][variant] = size
        datasets.add(dataset)

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
            
            real_builds = [val for key, val in build_times[index_name][size_cat].items() if key in REAL_DATASETS_64]
            real_latencies = [val for key, val in latencies[index_name][size_cat].items() if key in REAL_DATASETS_64]
            real_sizes = [val for key, val in sizes[index_name][size_cat].items() if key in REAL_DATASETS_64]

            if all(real_builds):
                build_times[index_name][size_cat]["real"] = mean(real_builds)
            else:
                build_times[index_name][size_cat]["real"] = None
            latencies[index_name][size_cat]["real"] = mean(real_latencies)
            if all(real_sizes):
                sizes[index_name][size_cat]["real"] = mean(real_sizes)
            else:
                sizes[index_name][size_cat]["real"] = None

    return latencies, build_times, sizes, datasets

def get_ranked_indexes_uint32(dbname):
    build_times = rec_dd()
    latencies = rec_dd()
    sizes = rec_dd()
    conn = create_connection(dbname)
    all_indexes = get_all_indexes(conn)
    datasets = set()

    # Dictionaries have structure name -> size -> dataset -> variant -> time of that variant
    # First we'll process to get the lowest-latency variant on each dataset, then take the geometric
    # mean across datasets which gives us name -> size -> mean latency across datasets
    for entry_id, name, variant, latency, size, build_time, searcher, dataset in all_indexes:
        # Could have been multiple runs for latency
        size_category = ''
        if 'uint64' in dataset:
            continue
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

        build_times[name][size_category][dataset][variant] = build_time
        latencies[name][size_category][dataset][variant] = latency
        sizes[name][size_category][dataset][variant] = size
        datasets.add(dataset)

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
            
            real_builds = [val for key, val in build_times[index_name][size_cat].items() if key in REAL_DATASETS_32]
            real_latencies = [val for key, val in latencies[index_name][size_cat].items() if key in REAL_DATASETS_32]
            real_sizes = [val for key, val in sizes[index_name][size_cat].items() if key in REAL_DATASETS_32]

            if all(real_builds):
                build_times[index_name][size_cat]["real"] = mean(real_builds)
            else:
                build_times[index_name][size_cat]["real"] = None
            latencies[index_name][size_cat]["real"] = mean(real_latencies)
            if all(real_sizes):
                sizes[index_name][size_cat]["real"] = mean(real_sizes)
            else:
                sizes[index_name][size_cat]["real"] = None
    
    return latencies, build_times, sizes, datasets

def get_size_str(size):
    if size < 1e6:
        return str(round(size/1000, 2)) + " KB"
    elif size < 1e9:
        return str(round(size/1e6, 2)) + " MB"
    else:
        return str(round(size/1e9, 2)) + " GB"

if __name__ == "__main__":
    db = r"./indexes.db"
    
    latencies, build_times, sizes, datasets = get_ranked_indexes_uint64(db)
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
                "all_uint64"
            ])
            writer.writerow([
                index,
                round(latencies[index]['xs']["real"]) if 'xs' in latencies[index] and latencies[index]['xs']["real"] is not None else ' ',
                round(latencies[index]['s']["real"]) if 's' in latencies[index] and latencies[index]['s']["real"] is not None else ' ',
                round(latencies[index]['m']["real"]) if 'm' in latencies[index] and latencies[index]['m']["real"] is not None else ' ',
                round(latencies[index]['l']["real"]) if 'l' in latencies[index] and latencies[index]['l']["real"] is not None else ' ',
                round(latencies[index]['xl']["real"]) if 'xl' in latencies[index] and latencies[index]['xl']["real"] is not None else ' ',
                "real_uint64"
            ])
    
    with open("./_data/buildtimes.csv", "w") as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow(headers)
        for index in build_times:
            writer.writerow([
                index,
                round(build_times[index]['xs']["mean"]/1000, 2) if 'xs' in build_times[index] and build_times[index]['xs']["mean"] is not None else ' ',
                round(build_times[index]['s']["mean"]/1000, 2) if 's' in build_times[index] and build_times[index]['s']["mean"] is not None else ' ',
                round(build_times[index]['m']["mean"]/1000, 2) if 'm' in build_times[index] and build_times[index]['m']["mean"] is not None else ' ',
                round(build_times[index]['l']["mean"]/1000, 2) if 'l' in build_times[index] and build_times[index]['l']["mean"] is not None else ' ',
                round(build_times[index]['xl']["mean"]/1000, 2) if 'xl' in build_times[index] and build_times[index]['xl']["mean"] is not None else ' ',
                "all_uint64"
            ])
            writer.writerow([
                index,
                round(build_times[index]['xs']["real"]/1000, 2) if 'xs' in build_times[index] and build_times[index]['xs']["real"] is not None else ' ',
                round(build_times[index]['s']["real"]/1000, 2) if 's' in build_times[index] and build_times[index]['s']["real"] is not None else ' ',
                round(build_times[index]['m']["real"]/1000, 2) if 'm' in build_times[index] and build_times[index]['m']["real"] is not None else ' ',
                round(build_times[index]['l']["real"]/1000, 2) if 'l' in build_times[index] and build_times[index]['l']["real"] is not None else ' ',
                round(build_times[index]['xl']["real"]/1000, 2) if 'xl' in build_times[index] and build_times[index]['xl']["real"] is not None else ' ',
                "real_uint64"
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
                "all_uint64"
            ])
            writer.writerow([
                index,
                get_size_str(sizes[index]['xs']["real"]) if 'xs' in sizes[index] and sizes[index]['xs']["real"] is not None else ' ',
                get_size_str(sizes[index]['s']["real"]) if 's' in sizes[index] and sizes[index]['s']["real"] is not None else ' ',
                get_size_str(sizes[index]['m']["real"]) if 'm' in sizes[index] and sizes[index]['m']["real"] is not None else ' ',
                get_size_str(sizes[index]['l']["real"]) if 'l' in sizes[index] and sizes[index]['l']["real"] is not None else ' ',
                get_size_str(sizes[index]['xl']["real"]) if 'xl' in sizes[index] and sizes[index]['xl']["real"] is not None else ' ',
                "real_uint64"
            ])
    
    for dataset in datasets:
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
                    round(build_times[index]['xs'][dataset]/1000, 2) if 'xs' in build_times[index] and type(build_times[index]['xs'][dataset]) is not defaultdict else ' ',
                    round(build_times[index]['s'][dataset]/1000, 2) if 's' in build_times[index] and type(build_times[index]['s'][dataset]) is not defaultdict else ' ',
                    round(build_times[index]['m'][dataset]/1000, 2) if 'm' in build_times[index] and type(build_times[index]['m'][dataset]) is not defaultdict else ' ',
                    round(build_times[index]['l'][dataset]/1000, 2) if 'l' in build_times[index] and type(build_times[index]['l'][dataset]) is not defaultdict else ' ',
                    round(build_times[index]['xl'][dataset]/1000, 2) if 'xl' in build_times[index] and type(build_times[index]['xl'][dataset]) is not defaultdict else ' ',
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
    
    latencies, build_times, sizes, datasets = get_ranked_indexes_uint32(db)
    with open("./_data/latency.csv", "a") as f:
        writer = csv.writer(f, delimiter=',')
        for index in latencies:
            writer.writerow([
                index,
                round(latencies[index]['xs']["mean"]) if 'xs' in latencies[index] and latencies[index]['xs']["mean"] is not None else ' ',
                round(latencies[index]['s']["mean"]) if 's' in latencies[index] and latencies[index]['s']["mean"] is not None else ' ',
                round(latencies[index]['m']["mean"]) if 'm' in latencies[index] and latencies[index]['m']["mean"] is not None else ' ',
                round(latencies[index]['l']["mean"]) if 'l' in latencies[index] and latencies[index]['l']["mean"] is not None else ' ',
                round(latencies[index]['xl']["mean"]) if 'xl' in latencies[index] and latencies[index]['xl']["mean"] is not None else ' ',
                "all_uint32"
            ])
            writer.writerow([
                index,
                round(latencies[index]['xs']["real"]) if 'xs' in latencies[index] and latencies[index]['xs']["real"] is not None else ' ',
                round(latencies[index]['s']["real"]) if 's' in latencies[index] and latencies[index]['s']["real"] is not None else ' ',
                round(latencies[index]['m']["real"]) if 'm' in latencies[index] and latencies[index]['m']["real"] is not None else ' ',
                round(latencies[index]['l']["real"]) if 'l' in latencies[index] and latencies[index]['l']["real"] is not None else ' ',
                round(latencies[index]['xl']["real"]) if 'xl' in latencies[index] and latencies[index]['xl']["real"] is not None else ' ',
                "real_uint32"
            ])
    
    with open("./_data/buildtimes.csv", "a") as f:
        writer = csv.writer(f, delimiter=',')
        for index in build_times:
            writer.writerow([
                index,
                round(build_times[index]['xs']["mean"]/1000, 2) if 'xs' in build_times[index] and build_times[index]['xs']["mean"] is not None else ' ',
                round(build_times[index]['s']["mean"]/1000, 2) if 's' in build_times[index] and build_times[index]['s']["mean"] is not None else ' ',
                round(build_times[index]['m']["mean"]/1000, 2) if 'm' in build_times[index] and build_times[index]['m']["mean"] is not None else ' ',
                round(build_times[index]['l']["mean"]/1000, 2) if 'l' in build_times[index] and build_times[index]['l']["mean"] is not None else ' ',
                round(build_times[index]['xl']["mean"]/1000, 2) if 'xl' in build_times[index] and build_times[index]['xl']["mean"] is not None else ' ',
                "all_uint32"
            ])
            writer.writerow([
                index,
                round(build_times[index]['xs']["real"]/1000, 2) if 'xs' in build_times[index] and build_times[index]['xs']["real"] is not None else ' ',
                round(build_times[index]['s']["real"]/1000, 2) if 's' in build_times[index] and build_times[index]['s']["real"] is not None else ' ',
                round(build_times[index]['m']["real"]/1000, 2) if 'm' in build_times[index] and build_times[index]['m']["real"] is not None else ' ',
                round(build_times[index]['l']["real"]/1000, 2) if 'l' in build_times[index] and build_times[index]['l']["real"] is not None else ' ',
                round(build_times[index]['xl']["real"]/1000, 2) if 'xl' in build_times[index] and build_times[index]['xl']["real"] is not None else ' ',
                "real_uint32"
            ])
    
    with open("./_data/sizes.csv", "a") as f:
        writer = csv.writer(f, delimiter=',')
        for index in sizes:
            writer.writerow([
                index,
                get_size_str(sizes[index]['xs']["mean"]) if 'xs' in sizes[index] and sizes[index]['xs']["mean"] is not None else ' ',
                get_size_str(sizes[index]['s']["mean"]) if 's' in sizes[index] and sizes[index]['s']["mean"] is not None else ' ',
                get_size_str(sizes[index]['m']["mean"]) if 'm' in sizes[index] and sizes[index]['m']["mean"] is not None else ' ',
                get_size_str(sizes[index]['l']["mean"]) if 'l' in sizes[index] and sizes[index]['l']["mean"] is not None else ' ',
                get_size_str(sizes[index]['xl']["mean"]) if 'xl' in sizes[index] and sizes[index]['xl']["mean"] is not None else ' ',
                "all_uint32"
            ])
            writer.writerow([
                index,
                get_size_str(sizes[index]['xs']["real"]) if 'xs' in sizes[index] and sizes[index]['xs']["real"] is not None else ' ',
                get_size_str(sizes[index]['s']["real"]) if 's' in sizes[index] and sizes[index]['s']["real"] is not None else ' ',
                get_size_str(sizes[index]['m']["real"]) if 'm' in sizes[index] and sizes[index]['m']["real"] is not None else ' ',
                get_size_str(sizes[index]['l']["real"]) if 'l' in sizes[index] and sizes[index]['l']["real"] is not None else ' ',
                get_size_str(sizes[index]['xl']["real"]) if 'xl' in sizes[index] and sizes[index]['xl']["real"] is not None else ' ',
                "real_uint32"
            ])
    
    for dataset in datasets:
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
                    round(build_times[index]['xs'][dataset]/1000, 2) if 'xs' in build_times[index] and type(build_times[index]['xs'][dataset]) is not defaultdict else ' ',
                    round(build_times[index]['s'][dataset]/1000, 2) if 's' in build_times[index] and type(build_times[index]['s'][dataset]) is not defaultdict else ' ',
                    round(build_times[index]['m'][dataset]/1000, 2) if 'm' in build_times[index] and type(build_times[index]['m'][dataset]) is not defaultdict else ' ',
                    round(build_times[index]['l'][dataset]/1000, 2) if 'l' in build_times[index] and type(build_times[index]['l'][dataset]) is not defaultdict else ' ',
                    round(build_times[index]['xl'][dataset]/1000, 2) if 'xl' in build_times[index] and type(build_times[index]['xl'][dataset]) is not defaultdict else ' ',
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