import numpy as np
import csv

from create_sqlite import create_connection
from insert_sqlite import get_all_indexes
from collections import defaultdict
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
        size_categories = ['xl']
        if 'uint32' in dataset:
            continue
        elif 'uint64' in dataset:
            if size < XS_SIZE:
                size_categories.append('xs')
            if size < S_SIZE:
                size_categories.append('s')
            if size < M_SIZE:
                size_categories.append('m')
            if size < L_SIZE:
                size_categories.append('l')
        else:
            raise ValueError("Dataset name does not contain data type")

        for size_category in size_categories:
            build_times[name][size_category][dataset][variant] = build_time
            latencies[name][size_category][dataset][variant] = latency
            sizes[name][size_category][dataset][variant] = size
        datasets.add(dataset)
    print(datasets)
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
            if all(build_times[index_name][size_cat].values()) and len(build_times) > 0:
                build_times[index_name][size_cat]["mean"] = mean((val for key, val in build_times[index_name][size_cat].items() if "200M" in key))
            else:
                build_times[index_name][size_cat]["mean"] = None
            if len(latencies) > 0:
                latencies[index_name][size_cat]["mean"] = mean((val for key, val in latencies[index_name][size_cat].items() if "200M" in key))
            else:
                latencies[index_name][size_cat]["mean"] = None
            if all(sizes[index_name][size_cat].values()) and len(sizes) > 0:
                sizes[index_name][size_cat]["mean"] = mean((val for key, val in sizes[index_name][size_cat].items() if "200M" in key))
            else:
                sizes[index_name][size_cat]["mean"] = None

            real_builds = [val for key, val in build_times[index_name][size_cat].items() if "200M" in key and key in REAL_DATASETS_64]
            real_latencies = [val for key, val in latencies[index_name][size_cat].items() if "200M" in key and key in REAL_DATASETS_64]
            real_sizes = [val for key, val in sizes[index_name][size_cat].items() if "200M" in key and key in REAL_DATASETS_64]

            if all(real_builds) and len(real_builds) > 0:
                build_times[index_name][size_cat]["real"] = mean(real_builds)
            else:
                build_times[index_name][size_cat]["real"] = None
            if len(real_latencies) > 0:
                latencies[index_name][size_cat]["real"] = mean(real_latencies)
            else:
                latencies[index_name][size_cat]["real"] = None
            if all(real_sizes) and len(real_sizes) > 0:
                sizes[index_name][size_cat]["real"] = mean(real_sizes)
            else:
                sizes[index_name][size_cat]["real"] = None

            synthetic_builds = [val for key, val in build_times[index_name][size_cat].items() if "200M" in key and key not in REAL_DATASETS_64]
            synthetic_latencies = [val for key, val in latencies[index_name][size_cat].items() if "200M" in key and key not in REAL_DATASETS_64]
            synthetic_sizes = [val for key, val in sizes[index_name][size_cat].items() if "200M" in key and key not in REAL_DATASETS_64]

            if all(synthetic_builds) and len(synthetic_builds) > 0:
                build_times[index_name][size_cat]["synthetic"] = mean(synthetic_builds)
            else:
                build_times[index_name][size_cat]["synthetic"] = None
            if len(synthetic_latencies) > 0:
                latencies[index_name][size_cat]["synthetic"] = mean(synthetic_latencies)
            else:
                latencies[index_name][size_cat]["latencies"] = None
            if all(synthetic_sizes) and len(synthetic_sizes) > 0:
                sizes[index_name][size_cat]["synthetic"] = mean(synthetic_sizes)
            else:
                sizes[index_name][size_cat]["synthetic"] = None

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
        size_categories = ['xl']
        if 'uint64' in dataset:
            continue
        elif 'uint32' in dataset:
            if size < XS_SIZE_32:
                size_categories.append('xs')
            if size < S_SIZE_32:
                size_categories.append('s')
            if size < M_SIZE_32:
                size_categories.append('m')
            if size < L_SIZE_32:
                size_categories.append('l')
        else:
            raise ValueError("Dataset name does not contain data type")

        for size_category in size_categories:
            build_times[name][size_category][dataset][variant] = build_time
            latencies[name][size_category][dataset][variant] = latency
            sizes[name][size_category][dataset][variant] = size
        datasets.add(dataset)
    print(datasets)
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
            if all(build_times[index_name][size_cat].values()) and len(build_times) > 0:
                build_times[index_name][size_cat]["mean"] = mean((val for key, val in build_times[index_name][size_cat].items() if "200M" in key))
            else:
                build_times[index_name][size_cat]["mean"] = None
            if len(latencies) > 0:
                latencies[index_name][size_cat]["mean"] = mean((val for key, val in latencies[index_name][size_cat].items() if "200M" in key))
            else:
                latencies[index_name][size_cat]["mean"] = None
            if all(sizes[index_name][size_cat].values()) and len(sizes) > 0:
                sizes[index_name][size_cat]["mean"] = mean((val for key, val in sizes[index_name][size_cat].items() if "200M" in key))
            else:
                sizes[index_name][size_cat]["mean"] = None

            # real_builds = [val for key, val in build_times[index_name][size_cat].items() if key in REAL_DATASETS_32]
            # real_latencies = [val for key, val in latencies[index_name][size_cat].items() if key in REAL_DATASETS_32]
            # real_sizes = [val for key, val in sizes[index_name][size_cat].items() if key in REAL_DATASETS_32]

            # if all(real_builds):
            #     build_times[index_name][size_cat]["real"] = mean(real_builds)
            # else:
            #     build_times[index_name][size_cat]["real"] = None
            # latencies[index_name][size_cat]["real"] = mean(real_latencies)
            # if all(real_sizes):
            #     sizes[index_name][size_cat]["real"] = mean(real_sizes)
            # else:
            #     sizes[index_name][size_cat]["real"] = None

            synthetic_builds = [val for key, val in build_times[index_name][size_cat].items() if "200M" in key and key not in REAL_DATASETS_32]
            synthetic_latencies = [val for key, val in latencies[index_name][size_cat].items() if "200M" in key and key not in REAL_DATASETS_32]
            synthetic_sizes = [val for key, val in sizes[index_name][size_cat].items() if "200M" in key and key not in REAL_DATASETS_32]

            if all(synthetic_builds) and len(synthetic_builds) > 0:
                build_times[index_name][size_cat]["synthetic"] = mean(synthetic_builds)
            else:
                build_times[index_name][size_cat]["synthetic"] = None
            if len(synthetic_latencies) > 0:
                latencies[index_name][size_cat]["synthetic"] = mean(synthetic_latencies)
            else:
                latencies[index_name][size_cat]["latencies"] = None
            if all(synthetic_sizes) and len(synthetic_sizes) > 0:
                sizes[index_name][size_cat]["synthetic"] = mean(synthetic_sizes)
            else:
                sizes[index_name][size_cat]["synthetic"] = None

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
            try:
                writer.writerow([
                    index,
                    str(round(latencies[index]['xs']["mean"])) + " ns" if 'xs' in latencies[index] and latencies[index]['xs']["mean"] not in [None, defaultdict] else ' ',
                    str(round(latencies[index]['s']["mean"])) + " ns" if 's' in latencies[index] and latencies[index]['s']["mean"] not in [None, defaultdict] else ' ',
                    str(round(latencies[index]['m']["mean"])) + " ns" if 'm' in latencies[index] and latencies[index]['m']["mean"] not in [None, defaultdict] else ' ',
                    str(round(latencies[index]['l']["mean"])) + " ns" if 'l' in latencies[index] and latencies[index]['l']["mean"] not in [None, defaultdict] else ' ',
                    str(round(latencies[index]['xl']["mean"])) + " ns" if 'xl' in latencies[index] and latencies[index]['xl']["mean"] not in [None, defaultdict] else ' ',
                    "all_uint64"
                ])
                writer.writerow([
                    index,
                    str(round(latencies[index]['xs']["real"])) + " ns" if 'xs' in latencies[index] and latencies[index]['xs']["real"] not in [None, defaultdict] else ' ',
                    str(round(latencies[index]['s']["real"])) + " ns" if 's' in latencies[index] and latencies[index]['s']["real"] not in [None, defaultdict] else ' ',
                    str(round(latencies[index]['m']["real"])) + " ns" if 'm' in latencies[index] and latencies[index]['m']["real"] not in [None, defaultdict] else ' ',
                    str(round(latencies[index]['l']["real"])) + " ns" if 'l' in latencies[index] and latencies[index]['l']["real"] not in [None, defaultdict] else ' ',
                    str(round(latencies[index]['xl']["real"])) + " ns" if 'xl' in latencies[index] and latencies[index]['xl']["real"] not in [None, defaultdict] else ' ',
                    "real_uint64"
                ])
                writer.writerow([
                    index,
                    str(round(latencies[index]['xs']["synthetic"])) + " ns" if 'xs' in latencies[index] and latencies[index]['xs']["synthetic"] not in [None, defaultdict] else ' ',
                    str(round(latencies[index]['s']["synthetic"])) + " ns" if 's' in latencies[index] and latencies[index]['s']["synthetic"] not in [None, defaultdict] else ' ',
                    str(round(latencies[index]['m']["synthetic"])) + " ns" if 'm' in latencies[index] and latencies[index]['m']["synthetic"] not in [None, defaultdict] else ' ',
                    str(round(latencies[index]['l']["synthetic"])) + " ns" if 'l' in latencies[index] and latencies[index]['l']["synthetic"] not in [None, defaultdict] else ' ',
                    str(round(latencies[index]['xl']["synthetic"])) + " ns" if 'xl' in latencies[index] and latencies[index]['xl']["synthetic"] not in [None, defaultdict] else ' ',
                    "synthetic_uint64"
                ])
            except Exception as e:
                pass

    with open("./_data/buildtimes.csv", "w") as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow(headers)
        for index in build_times:
            try:
                writer.writerow([
                    index,
                    str(round(build_times[index]['xs']["mean"]/1000)) + " ns" if 'xs' in build_times[index] and build_times[index]['xs']["mean"] not in [None, defaultdict] else ' ',
                    str(round(build_times[index]['s']["mean"]/1000)) + " ns" if 's' in build_times[index] and build_times[index]['s']["mean"] not in [None, defaultdict] else ' ',
                    str(round(build_times[index]['m']["mean"]/1000)) + " ns" if 'm' in build_times[index] and build_times[index]['m']["mean"] not in [None, defaultdict] else ' ',
                    str(round(build_times[index]['l']["mean"]/1000)) + " ns" if 'l' in build_times[index] and build_times[index]['l']["mean"] not in [None, defaultdict] else ' ',
                    str(round(build_times[index]['xl']["mean"]/1000)) + " ns" if 'xl' in build_times[index] and build_times[index]['xl']["mean"] not in [None, defaultdict] else ' ',
                    "all_uint64"
                ])
                writer.writerow([
                    index,
                    str(round(build_times[index]['xs']["real"]/1000)) + " ns" if 'xs' in build_times[index] and build_times[index]['xs']["real"] not in [None, defaultdict] else ' ',
                    str(round(build_times[index]['s']["real"]/1000)) + " ns" if 's' in build_times[index] and build_times[index]['s']["real"] not in [None, defaultdict] else ' ',
                    str(round(build_times[index]['m']["real"]/1000)) + " ns" if 'm' in build_times[index] and build_times[index]['m']["real"] not in [None, defaultdict] else ' ',
                    str(round(build_times[index]['l']["real"]/1000)) + " ns" if 'l' in build_times[index] and build_times[index]['l']["real"] not in [None, defaultdict] else ' ',
                    str(round(build_times[index]['xl']["real"]/1000)) + " ns" if 'xl' in build_times[index] and build_times[index]['xl']["real"] not in [None, defaultdict] else ' ',
                    "real_uint64"
                ])
                writer.writerow([
                    index,
                    str(round(build_times[index]['xs']["synthetic"]/1000)) + " ns" if 'xs' in build_times[index] and build_times[index]['xs']["synthetic"] not in [None, defaultdict] else ' ',
                    str(round(build_times[index]['s']["synthetic"]/1000)) + " ns" if 's' in build_times[index] and build_times[index]['s']["synthetic"] not in [None, defaultdict] else ' ',
                    str(round(build_times[index]['m']["synthetic"]/1000)) + " ns" if 'm' in build_times[index] and build_times[index]['m']["synthetic"] not in [None, defaultdict] else ' ',
                    str(round(build_times[index]['l']["synthetic"]/1000)) + " ns" if 'l' in build_times[index] and build_times[index]['l']["synthetic"] not in [None, defaultdict] else ' ',
                    str(round(build_times[index]['xl']["synthetic"]/1000)) + " ns" if 'xl' in build_times[index] and build_times[index]['xl']["synthetic"] not in [None, defaultdict] else ' ',
                    "synthetic_uint64"
                ])
            except Exception as e:
                pass

    with open("./_data/sizes.csv", "w") as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow(headers)
        for index in sizes:
            try:
                writer.writerow([
                    index,
                    get_size_str(sizes[index]['xs']["mean"]) if 'xs' in sizes[index] and sizes[index]['xs']["mean"] not in [None, defaultdict] else ' ',
                    get_size_str(sizes[index]['s']["mean"]) if 's' in sizes[index] and sizes[index]['s']["mean"] not in [None, defaultdict] else ' ',
                    get_size_str(sizes[index]['m']["mean"]) if 'm' in sizes[index] and sizes[index]['m']["mean"] not in [None, defaultdict] else ' ',
                    get_size_str(sizes[index]['l']["mean"]) if 'l' in sizes[index] and sizes[index]['l']["mean"] not in [None, defaultdict] else ' ',
                    get_size_str(sizes[index]['xl']["mean"]) if 'xl' in sizes[index] and sizes[index]['xl']["mean"] not in [None, defaultdict] else ' ',
                    "all_uint64"
                ])
                writer.writerow([
                    index,
                    get_size_str(sizes[index]['xs']["real"]) if 'xs' in sizes[index] and sizes[index]['xs']["real"] not in [None, defaultdict] else ' ',
                    get_size_str(sizes[index]['s']["real"]) if 's' in sizes[index] and sizes[index]['s']["real"] not in [None, defaultdict] else ' ',
                    get_size_str(sizes[index]['m']["real"]) if 'm' in sizes[index] and sizes[index]['m']["real"] not in [None, defaultdict] else ' ',
                    get_size_str(sizes[index]['l']["real"]) if 'l' in sizes[index] and sizes[index]['l']["real"] not in [None, defaultdict] else ' ',
                    get_size_str(sizes[index]['xl']["real"]) if 'xl' in sizes[index] and sizes[index]['xl']["real"] not in [None, defaultdict] else ' ',
                    "real_uint64"
                ])
                writer.writerow([
                    index,
                    get_size_str(sizes[index]['xs']["synthetic"]) if 'xs' in sizes[index] and sizes[index]['xs']["synthetic"] not in [None, defaultdict] else ' ',
                    get_size_str(sizes[index]['s']["synthetic"]) if 's' in sizes[index] and sizes[index]['s']["synthetic"] not in [None, defaultdict] else ' ',
                    get_size_str(sizes[index]['m']["synthetic"]) if 'm' in sizes[index] and sizes[index]['m']["synthetic"] not in [None, defaultdict] else ' ',
                    get_size_str(sizes[index]['l']["synthetic"]) if 'l' in sizes[index] and sizes[index]['l']["synthetic"] not in [None, defaultdict] else ' ',
                    get_size_str(sizes[index]['xl']["synthetic"]) if 'xl' in sizes[index] and sizes[index]['xl']["synthetic"] not in [None, defaultdict] else ' ',
                    "synthetic_uint64"
                ])
            except Exception as e:
                pass

    for dataset in datasets:
        with open(f"./_data/latency.csv", "a") as f:
            writer = csv.writer(f, delimiter=',')
            for index in latencies:
                try:
                    writer.writerow([
                        index,
                        str(round(latencies[index]['xs'][dataset])) + " ns" if 'xs' in latencies[index] and type(latencies[index]['xs'][dataset]) is not defaultdict else ' ',
                        str(round(latencies[index]['s'][dataset])) + " ns" if 's' in latencies[index] and type(latencies[index]['s'][dataset]) is not defaultdict else ' ',
                        str(round(latencies[index]['m'][dataset])) + " ns" if 'm' in latencies[index] and type(latencies[index]['m'][dataset]) is not defaultdict else ' ',
                        str(round(latencies[index]['l'][dataset])) + " ns" if 'l' in latencies[index] and type(latencies[index]['l'][dataset]) is not defaultdict else ' ',
                        str(round(latencies[index]['xl'][dataset])) + " ns" if 'xl' in latencies[index] and type(latencies[index]['xl'][dataset]) is not defaultdict else ' ',
                        dataset
                    ])
                except Exception as e:
                    pass

        with open(f"./_data/buildtimes.csv", "a") as f:
            writer = csv.writer(f, delimiter=',')
            for index in build_times:
                try:
                    writer.writerow([
                        index,
                        str(round(build_times[index]['xs'][dataset]/1000)) + " ns" if 'xs' in build_times[index] and type(build_times[index]['xs'][dataset]) is not defaultdict else ' ',
                        str(round(build_times[index]['s'][dataset]/1000)) + " ns" if 's' in build_times[index] and type(build_times[index]['s'][dataset]) is not defaultdict else ' ',
                        str(round(build_times[index]['m'][dataset]/1000)) + " ns" if 'm' in build_times[index] and type(build_times[index]['m'][dataset]) is not defaultdict else ' ',
                        str(round(build_times[index]['l'][dataset]/1000)) + " ns" if 'l' in build_times[index] and type(build_times[index]['l'][dataset]) is not defaultdict else ' ',
                        str(round(build_times[index]['xl'][dataset]/1000)) + " ns" if 'xl' in build_times[index] and type(build_times[index]['xl'][dataset]) is not defaultdict else ' ',
                        dataset
                    ])
                except Exception as e:
                    pass

        with open(f"./_data/sizes.csv", "a") as f:
            writer = csv.writer(f, delimiter=',')
            for index in sizes:
                try:
                    writer.writerow([
                        index,
                        get_size_str(sizes[index]['xs'][dataset]) if 'xs' in sizes[index] and type(sizes[index]['xs'][dataset]) is not defaultdict else ' ',
                        get_size_str(sizes[index]['s'][dataset]) if 's' in sizes[index] and type(sizes[index]['s'][dataset]) is not defaultdict else ' ',
                        get_size_str(sizes[index]['m'][dataset]) if 'm' in sizes[index] and type(sizes[index]['m'][dataset]) is not defaultdict else ' ',
                        get_size_str(sizes[index]['l'][dataset]) if 'l' in sizes[index] and type(sizes[index]['l'][dataset]) is not defaultdict else ' ',
                        get_size_str(sizes[index]['xl'][dataset]) if 'xl' in sizes[index] and type(sizes[index]['xl'][dataset]) is not defaultdict else ' ',
                        dataset
                    ])
                except Exception as e:
                    pass

    latencies, build_times, sizes, datasets = get_ranked_indexes_uint32(db)
    with open("./_data/latency.csv", "a") as f:
        writer = csv.writer(f, delimiter=',')
        for index in latencies:
            try:
                writer.writerow([
                    index,
                    str(round(latencies[index]['xs']["mean"])) + " ns" if 'xs' in latencies[index] and latencies[index]['xs']["mean"] not in [None, defaultdict] else ' ',
                    str(round(latencies[index]['s']["mean"])) + " ns" if 's' in latencies[index] and latencies[index]['s']["mean"] not in [None, defaultdict] else ' ',
                    str(round(latencies[index]['m']["mean"])) + " ns" if 'm' in latencies[index] and latencies[index]['m']["mean"] not in [None, defaultdict] else ' ',
                    str(round(latencies[index]['l']["mean"])) + " ns" if 'l' in latencies[index] and latencies[index]['l']["mean"] not in [None, defaultdict] else ' ',
                    str(round(latencies[index]['xl']["mean"])) + " ns" if 'xl' in latencies[index] and latencies[index]['xl']["mean"] not in [None, defaultdict] else ' ',
                    "all_uint32"
                ])
                # writer.writerow([
                #     index,
                #     str(round(latencies[index]['xs']["real"])) + " ns" if 'xs' in latencies[index] and latencies[index]['xs']["real"] not in [None, defaultdict] else ' ',
                #     str(round(latencies[index]['s']["real"])) + " ns" if 's' in latencies[index] and latencies[index]['s']["real"] not in [None, defaultdict] else ' ',
                #     str(round(latencies[index]['m']["real"])) + " ns" if 'm' in latencies[index] and latencies[index]['m']["real"] not in [None, defaultdict] else ' ',
                #     str(round(latencies[index]['l']["real"])) + " ns" if 'l' in latencies[index] and latencies[index]['l']["real"] not in [None, defaultdict] else ' ',
                #     str(round(latencies[index]['xl']["real"])) + " ns" if 'xl' in latencies[index] and latencies[index]['xl']["real"] not in [None, defaultdict] else ' ',
                #     "real_uint32"
                # ])
                writer.writerow([
                    index,
                    str(round(latencies[index]['xs']["synthetic"])) + " ns" if 'xs' in latencies[index] and latencies[index]['xs']["synthetic"] not in [None, defaultdict] else ' ',
                    str(round(latencies[index]['s']["synthetic"])) + " ns" if 's' in latencies[index] and latencies[index]['s']["synthetic"] not in [None, defaultdict] else ' ',
                    str(round(latencies[index]['m']["synthetic"])) + " ns" if 'm' in latencies[index] and latencies[index]['m']["synthetic"] not in [None, defaultdict] else ' ',
                    str(round(latencies[index]['l']["synthetic"])) + " ns" if 'l' in latencies[index] and latencies[index]['l']["synthetic"] not in [None, defaultdict] else ' ',
                    str(round(latencies[index]['xl']["synthetic"])) + " ns" if 'xl' in latencies[index] and latencies[index]['xl']["synthetic"] not in [None, defaultdict] else ' ',
                    "synthetic_uint32"
                ])
            except Exception as e: pass

    with open("./_data/buildtimes.csv", "a") as f:
        writer = csv.writer(f, delimiter=',')
        for index in build_times:
            try:
                writer.writerow([
                    index,
                    str(round(build_times[index]['xs']["mean"]/1000)) + " ns" if 'xs' in build_times[index] and build_times[index]['xs']["mean"] not in [None, defaultdict] else ' ',
                    str(round(build_times[index]['s']["mean"]/1000)) + " ns" if 's' in build_times[index] and build_times[index]['s']["mean"] not in [None, defaultdict] else ' ',
                    str(round(build_times[index]['m']["mean"]/1000)) + " ns" if 'm' in build_times[index] and build_times[index]['m']["mean"] not in [None, defaultdict] else ' ',
                    str(round(build_times[index]['l']["mean"]/1000)) + " ns" if 'l' in build_times[index] and build_times[index]['l']["mean"] not in [None, defaultdict] else ' ',
                    str(round(build_times[index]['xl']["mean"]/1000)) + " ns" if 'xl' in build_times[index] and build_times[index]['xl']["mean"] not in [None, defaultdict] else ' ',
                    "all_uint32"
                ])
                # writer.writerow([
                #     index,
                #     str(round(build_times[index]['xs']["real"]/1000)) + " ns" if 'xs' in build_times[index] and build_times[index]['xs']["real"] not in [None, defaultdict] else ' ',
                #     str(round(build_times[index]['s']["real"]/1000)) + " ns" if 's' in build_times[index] and build_times[index]['s']["real"] not in [None, defaultdict] else ' ',
                #     str(round(build_times[index]['m']["real"]/1000)) + " ns" if 'm' in build_times[index] and build_times[index]['m']["real"] not in [None, defaultdict] else ' ',
                #     str(round(build_times[index]['l']["real"]/1000)) + " ns" if 'l' in build_times[index] and build_times[index]['l']["real"] not in [None, defaultdict] else ' ',
                #     str(round(build_times[index]['xl']["real"]/1000)) + " ns" if 'xl' in build_times[index] and build_times[index]['xl']["real"] not in [None, defaultdict] else ' ',
                #     "real_uint32"
                # ])
                writer.writerow([
                    index,
                    str(round(build_times[index]['xs']["synthetic"]/1000)) + " ns" if 'xs' in build_times[index] and build_times[index]['xs']["synthetic"] not in [None, defaultdict] else ' ',
                    str(round(build_times[index]['s']["synthetic"]/1000)) + " ns" if 's' in build_times[index] and build_times[index]['s']["synthetic"] not in [None, defaultdict] else ' ',
                    str(round(build_times[index]['m']["synthetic"]/1000)) + " ns" if 'm' in build_times[index] and build_times[index]['m']["synthetic"] not in [None, defaultdict] else ' ',
                    str(round(build_times[index]['l']["synthetic"]/1000)) + " ns" if 'l' in build_times[index] and build_times[index]['l']["synthetic"] not in [None, defaultdict] else ' ',
                    str(round(build_times[index]['xl']["synthetic"]/1000)) + " ns" if 'xl' in build_times[index] and build_times[index]['xl']["synthetic"] not in [None, defaultdict] else ' ',
                    "synthetic_uint32"
                ])
            except Exception as e:
                pass

    with open("./_data/sizes.csv", "a") as f:
        writer = csv.writer(f, delimiter=',')
        for index in sizes:
            try:
                writer.writerow([
                    index,
                    get_size_str(sizes[index]['xs']["mean"]) if 'xs' in sizes[index] and sizes[index]['xs']["mean"] not in [None, defaultdict] else ' ',
                    get_size_str(sizes[index]['s']["mean"]) if 's' in sizes[index] and sizes[index]['s']["mean"] not in [None, defaultdict] else ' ',
                    get_size_str(sizes[index]['m']["mean"]) if 'm' in sizes[index] and sizes[index]['m']["mean"] not in [None, defaultdict] else ' ',
                    get_size_str(sizes[index]['l']["mean"]) if 'l' in sizes[index] and sizes[index]['l']["mean"] not in [None, defaultdict] else ' ',
                    get_size_str(sizes[index]['xl']["mean"]) if 'xl' in sizes[index] and sizes[index]['xl']["mean"] not in [None, defaultdict] else ' ',
                    "all_uint32"
                ])
                # writer.writerow([
                #     index,
                #     get_size_str(sizes[index]['xs']["real"]) if 'xs' in sizes[index] and sizes[index]['xs']["real"] not in [None, defaultdict] else ' ',
                #     get_size_str(sizes[index]['s']["real"]) if 's' in sizes[index] and sizes[index]['s']["real"] not in [None, defaultdict] else ' ',
                #     get_size_str(sizes[index]['m']["real"]) if 'm' in sizes[index] and sizes[index]['m']["real"] not in [None, defaultdict] else ' ',
                #     get_size_str(sizes[index]['l']["real"]) if 'l' in sizes[index] and sizes[index]['l']["real"] not in [None, defaultdict] else ' ',
                #     get_size_str(sizes[index]['xl']["real"]) if 'xl' in sizes[index] and sizes[index]['xl']["real"] not in [None, defaultdict] else ' ',
                #     "real_uint32"
                # ])
                writer.writerow([
                    index,
                    get_size_str(sizes[index]['xs']["synthetic"]) if 'xs' in sizes[index] and sizes[index]['xs']["synthetic"] not in [None, defaultdict] else ' ',
                    get_size_str(sizes[index]['s']["synthetic"]) if 's' in sizes[index] and sizes[index]['s']["synthetic"] not in [None, defaultdict] else ' ',
                    get_size_str(sizes[index]['m']["synthetic"]) if 'm' in sizes[index] and sizes[index]['m']["synthetic"] not in [None, defaultdict] else ' ',
                    get_size_str(sizes[index]['l']["synthetic"]) if 'l' in sizes[index] and sizes[index]['l']["synthetic"] not in [None, defaultdict] else ' ',
                    get_size_str(sizes[index]['xl']["synthetic"]) if 'xl' in sizes[index] and sizes[index]['xl']["synthetic"] not in [None, defaultdict] else ' ',
                    "synthetic_uint32"
                ])
            except Exception as e:
                pass

    for dataset in datasets:
        with open(f"./_data/latency.csv", "a") as f:
            writer = csv.writer(f, delimiter=',')
            for index in latencies:
                try:
                    writer.writerow([
                        index,
                        str(round(latencies[index]['xs'][dataset])) + " ns" if 'xs' in latencies[index] and type(latencies[index]['xs'][dataset]) is not defaultdict else ' ',
                        str(round(latencies[index]['s'][dataset])) + " ns" if 's' in latencies[index] and type(latencies[index]['s'][dataset]) is not defaultdict else ' ',
                        str(round(latencies[index]['m'][dataset])) + " ns" if 'm' in latencies[index] and type(latencies[index]['m'][dataset]) is not defaultdict else ' ',
                        str(round(latencies[index]['l'][dataset])) + " ns" if 'l' in latencies[index] and type(latencies[index]['l'][dataset]) is not defaultdict else ' ',
                        str(round(latencies[index]['xl'][dataset])) + " ns" if 'xl' in latencies[index] and type(latencies[index]['xl'][dataset]) is not defaultdict else ' ',
                        dataset
                    ])
                except Exception as e:
                    pass

        with open(f"./_data/buildtimes.csv", "a") as f:
            writer = csv.writer(f, delimiter=',')
            for index in build_times:
                try:
                    writer.writerow([
                        index,
                        str(round(build_times[index]['xs'][dataset]/1000)) + " ns" if 'xs' in build_times[index] and type(build_times[index]['xs'][dataset]) is not defaultdict else ' ',
                        str(round(build_times[index]['s'][dataset]/1000)) + " ns" if 's' in build_times[index] and type(build_times[index]['s'][dataset]) is not defaultdict else ' ',
                        str(round(build_times[index]['m'][dataset]/1000)) + " ns" if 'm' in build_times[index] and type(build_times[index]['m'][dataset]) is not defaultdict else ' ',
                        str(round(build_times[index]['l'][dataset]/1000)) + " ns" if 'l' in build_times[index] and type(build_times[index]['l'][dataset]) is not defaultdict else ' ',
                        str(round(build_times[index]['xl'][dataset]/1000)) + " ns" if 'xl' in build_times[index] and type(build_times[index]['xl'][dataset]) is not defaultdict else ' ',
                        dataset
                    ])
                except Exception as e:
                    pass

        with open(f"./_data/sizes.csv", "a") as f:
            writer = csv.writer(f, delimiter=',')
            for index in sizes:
                try:
                    writer.writerow([
                        index,
                        get_size_str(sizes[index]['xs'][dataset]) if 'xs' in sizes[index] and type(sizes[index]['xs'][dataset]) is not defaultdict else ' ',
                        get_size_str(sizes[index]['s'][dataset]) if 's' in sizes[index] and type(sizes[index]['s'][dataset]) is not defaultdict else ' ',
                        get_size_str(sizes[index]['m'][dataset]) if 'm' in sizes[index] and type(sizes[index]['m'][dataset]) is not defaultdict else ' ',
                        get_size_str(sizes[index]['l'][dataset]) if 'l' in sizes[index] and type(sizes[index]['l'][dataset]) is not defaultdict else ' ',
                        get_size_str(sizes[index]['xl'][dataset]) if 'xl' in sizes[index] and type(sizes[index]['xl'][dataset]) is not defaultdict else ' ',
                        dataset
                    ])
                except Exception as e:
                    pass