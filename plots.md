---
layout: page
title: "Plots"
permalink: /plots/
---
# Plots

Here we provide a plot of index size against lookup latency on SOSD data. 
<select id="select">
    <option value="" disabled> -- 64-Bit datasets -- </option>
    <option value="" disabled> - Real-world datasets - </option>
    <option value="osm_cellids_200M_uint64" selected>OSM</option>
    <option value="fb_200M_uint64">Facebook</option>
    <option value="books_200M_uint64">Books</option>
    <option value="wiki_ts_200M_uint64">Wiki</option>
    <option value="" disabled> - Synthetic datasets - </option>
    <option value="normal_200M_uint64"> Normal </option>
    <option value="lognormal_200M_uint64"> Lognormal </option>
    <option value="uniform_sparse_200M_uint64"> Uniform sparse </option>
    <option value="uniform_dense_200M_uint64"> Uniform dense </option>
    <option value="" disabled> -- 32-Bit datasets -- </option>
    <option value="" disabled> - Real-world datasets - </option>
    <option value="fb_200M_uint32">Facebook</option>
    <option value="books_200M_uint32">Books</option>
    <option value="" disabled> - Synthetic datasets - </option>
    <option value="normal_200M_uint32"> Normal </option>
    <option value="lognormal_200M_uint32"> Lognormal </option>
    <option value="uniform_sparse_200M_uint32"> Uniform sparse </option>
    <option value="uniform_dense_200M_uint32"> Uniform dense </option>
</select>

<select class="chzn-select" multiple="true" id="indexes"></select>

<div id="latency_plot">
<canvas id="latencyChart" style="height:400px;width:600px"></canvas>
</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/PapaParse/5.3.0/papaparse.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/chart.js@2.8.0"></script>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
<script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/chosen/1.8.7/chosen.jquery.min.js"></script>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/chosen/1.8.7/chosen.css" />
<script type="text/javascript" src="/scripts/graphs/graph_latency.js"></script>
<script type="text/javascript" src="/scripts/graphs/selector.js"></script>