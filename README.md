# SOSD Leaderboard
This website serves as an informational site for the SOSD Benchmark.

## Updates
Scripts to update the leaderboard are in the `update` directory. To update the index, just move new result CSV files into the
benchmark_results directory, and run `update/makecsv.sh`. Regardless of whether or not an `indexes.db` file currently exists, the new results (and only the new results) will be overwritten into the site's CSV files, which Jekyll will automatically use to generate the site.
