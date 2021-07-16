# SOSD Leaderboard
This website serves as an informational site for the SOSD Benchmark.

## Updating new results
To obtain new results, results should be present in a local copy of the original [SOSD repo](https://github.com/learnedsystems/SOSD). Once results are present, move them to `SOSDLeaderboard/benchmark_results`. Once the leaderboard and HTML are updated, submit a pull request to the SOSDLeaderboard repo to update the repo.

## Updating the leaderboard
Scripts to update the leaderboard are in the `update` directory. To update the index, just move new result CSV files into the
benchmark_results directory, and run `update/makecsv.sh`, or run the commands within manually to update the CSV files. Regardless of whether or not an `indexes.db` file currently exists, the new results (and only the new results) will be overwritten into the site's CSV files, which Jekyll will automatically use to generate the site.
