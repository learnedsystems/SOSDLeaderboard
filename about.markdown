---
layout: page
title: About
permalink: /about/
---

## Search on Sorted Data

Search on Sorted Data (SOSD) is a new benchmark that allows researchers
to compare their new (learned) index structures on both synthetic and real-world datasets. It is provided 
as C++ open source code that incurs little overhead (8 instructions and 1 cache miss per lookup), comes 
with diverse synthetic and real-world datasets, and provides efficient baseline implementations. 

SOSD is a read-only workload and does not measure index performance on inserts.

The original SOSD paper can be found [here](https://arxiv.org/abs/1911.13014), and our detailed findings of learned 
index performance on SOSD datasets can be found [here](https://arxiv.org/abs/2006.12804).

Benchmark datasets are run five times on an AWS m5zn.metal VM for an even playing field, and the median latency of these runs
is taken for each dataset. The average of these latency medians is taken across the eight datasets within SOSD, for which final
results are reported.

To reproduce results, pull the [SOSD repo](https://github.com/learnedsystems/SOSD) and run scripts/reproduce.sh.

References:

[1] Amazon sales rank data for print and kindle books. https://www.kaggle.com/ucffool/
amazon-sales-rank-data-for-print-and-kindle-books.

[2] Intel Memory Latency Checker. https://software.intel.com/en-us/articles/
intelr-memory-latency-checker.

[3] S2 Geometry. https://s2geometry.io/.

[4] Search on Sorted Data Benchmark. https://github.com/learnedsystems/SOSD.

[5] STX B+ Tree. https://panthema.net/2007/stx-btree/.

[6] Wikimedia Downloads. http://dumps.wikimedia.org.

[7] J. Ding, U. F. Minhas, H. Zhang, Y. Li, C. Wang, B. Chandramouli, J. Gehrke, D. Kossmann,
and D. B. Lomet. ALEX: an updatable adaptive learned index. CoRR, abs/1905.08898, 2019.

[8] P. Ferragina and G. Vinciguerra. The PGM-index: A multicriteria, compressed and learned
approach to data indexing. arXiv:1910.06169 [cs], Oct. 2019.

[9] A. Galakatos, M. Markovitch, C. Binnig, R. Fonseca, and T. Kraska. FITing-Tree: A Data-aware
Index Structure. In Proceedings of the 2019 International Conference on Management of Data,
SIGMOD ’19, pages 1189–1206, New York, NY, USA, 2019. ACM.

[10] G. Graefe. B-tree indexes, interpolation search, and skew. In Workshop on Data Management
on New Hardware, DaMoN 2006, Chicago, Illinois, USA, June 25, 2006, page 5, 2006.

[11] C. Kim, J. Chhugani, N. Satish, E. Sedlar, A. D. Nguyen, T. Kaldewey, V. W. Lee, S. A. Brandt,
and P. Dubey. FAST: fast architecture sensitive tree search on modern cpus and gpus. In
Proceedings of the ACM SIGMOD International Conference on Management of Data, SIGMOD
2010, Indianapolis, Indiana, USA, June 6-10, 2010, pages 339–350, 2010.

[12] A. Kipf, T. Kipf, B. Radke, V. Leis, P. Boncz, and A. Kemper. Learned Cardinalities: Estimating
Correlated Joins with Deep Learning. In 9th Biennial Conference on Innovative Data Systems
Research, CIDR ’19, 2019.

[13] T. Kraska, M. Alizadeh, A. Beutel, E. H. Chi, A. Kristo, G. Leclerc, S. Madden, H. Mao, and
V. Nathan. SageDB: A learned database system. In CIDR 2019, 9th Biennial Conference
on Innovative Data Systems Research, Asilomar, CA, USA, January 13-16, 2019, Online
Proceedings, 2019.

[14] T. Kraska, A. Beutel, E. H. Chi, J. Dean, and N. Polyzotis. The case for learned index structures.
In Proceedings of the 2018 International Conference on Management of Data, SIGMOD
Conference 2018, Houston, TX, USA, June 10-15, 2018, pages 489–504, 2018.

[15] V. Leis, A. Kemper, and T. Neumann. The adaptive radix tree: Artful indexing for main-memory
databases. In 29th IEEE International Conference on Data Engineering, ICDE 2013, Brisbane,
Australia, April 8-12, 2013, pages 38–49, 2013.

[16] R. Marcus, P. Negi, H. Mao, C. Zhang, M. Alizadeh, T. Kraska, O. Papaemmanouil, and
N. Tatbul. Neo: A Learned Query Optimizer. PVLDB, 12(11):1705–1718, 2019.

[17] R. Marcus, O. Papaemmanouil, S. Semenova, and S. Garber. NashDB: An Economic Approach
to Fragmentation, Replication and Provisioning for Elastic Databases. In 37th ACM Special
Interest Group in Data Management, SIGMOD ’18, Houston, TX, 2018.

[18] T. Neumann and S. Michel. Smooth interpolating histograms with error guarantees. In Sharing
Data, Information and Knowledge, 25th British National Conference on Databases, BNCOD
25, Cardiff, UK, July 7-10, 2008. Proceedings, pages 126–138, 2008.

[19] V. Pandey, A. Kipf, T. Neumann, and A. Kemper. How good are modern spatial analytics
systems? PVLDB, 11(11):1661–1673, 2018.

[20] P. V. Sandt, Y. Chronis, and J. M. Patel. Efficiently searching in-memory sorted arrays:
Revenge of the interpolation search? In Proceedings of the 2019 International Conference on
Management of Data, SIGMOD Conference 2019, Amsterdam, The Netherlands, June 30 - July
5, 2019., pages 36–53, 2019.

[21] Y. Wu, J. Yu, Y. Tian, R. Sidle, and R. Barber. Designing succinct secondary indexing
mechanism by exploiting column correlations. In Proceedings of the 2019 International
Conference on Management of Data, SIGMOD Conference 2019, Amsterdam, The Netherlands,
June 30 - July 5, 2019., pages 1223–1240, 2019.
