---
layout: page
title: "Leaderboard"
permalink: /leaderboard/
---
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>

## Leaderboard
Metric to display by:
<script src="/SOSDLeaderboard/scripts/sorttable.js" type="text/javascript"></script>
<select id="select">
    <option value="latency-leaderboard">Latency (ns)</option>
    <option value="buildtime-leaderboard">Build time (μs)</option>
    <option value="size-leaderboard">Size</option>
</select>

Select a subset of indexes to display:
<button id="displayToggle" onclick="changeDisplay()">Show options</button>
<script type="text/javascript">
function changeDisplay() {
    if ($("#display").is(":visible")) {
        document.getElementById("display").style.display = "None";
        document.getElementById("displayToggle").innerHTML = "Show options";
    } else {
        document.getElementById("display").style.display = "Block";
        document.getElementById("displayToggle").innerHTML = "Hide table";
    }
}
</script>

Quick selections:
<button id="displayToggle" onclick="showAllIndexes()">All indexes</button>
<button id="displayToggle" onclick="showReadOnly()">Read-only indexes</button>
<button id="displayToggle" onclick="showUpdatable()">Updatable indexes</button>

Displaying results on datasets:
<select id="dataswitch">
    <option value="" disabled> --- 200M Datasets --- </option>
    <option value="" disabled> -- 64-Bit datasets -- </option>
    <option value="all_uint64">All 64-Bit Datasets</option>
    <option value="" disabled> - Real-world datasets - </option>
    <option value="real_uint64">All real datasets</option>
    <option value="books_200M_uint64" selected>Books</option>
    <option value="fb_200M_uint64">Facebook</option>
    <option value="osm_cellids_200M_uint64">OSM</option>
    <option value="wiki_ts_200M_uint64">Wiki</option>
    <option value="" disabled> - Synthetic datasets - </option>
    <option value="synthetic_uint64">All synthetic datasets</option>
    <option value="lognormal_200M_uint64"> Lognormal </option>
    <option value="normal_200M_uint64"> Normal </option>
    <option value="uniform_dense_200M_uint64"> Uniform dense </option>
    <option value="uniform_sparse_200M_uint64"> Uniform sparse </option>
    <option value="" disabled> -- 32-Bit datasets -- </option>
    <option value="all_uint32">All 32-Bit Datasets</option>
    <option value="" disabled> - Real-world datasets - </option>
    <option value="books_200M_uint32">Books</option>
    <option value="" disabled> - Synthetic datasets - </option>
    <option value="synthetic_uint32">All synthetic datasets</option>
    <option value="lognormal_200M_uint32"> Lognormal </option>
    <option value="normal_200M_uint32"> Normal </option>
    <option value="uniform_dense_200M_uint32"> Uniform dense </option>
    <option value="uniform_sparse_200M_uint32"> Uniform sparse </option>
    <option value="" disabled> --- Larger Datasets --- </option>
    <option value="books_400M_uint64">Books (400M)</option>
    <option value="books_600M_uint64">Books (600M)</option>
    <option value="books_800M_uint64">Books (800M)</option>
    <option value="osm_cellids_400M_uint64">OSM (400M)</option>
    <option value="osm_cellids_600M_uint64">OSM (600M)</option>
    <option value="osm_cellids_800M_uint64">OSM (800M)</option>
</select>

<div id="display" style="height:400px;overflow:auto;display:none;">
<table id="display-boxes">
<tbody>
    {% assign rows = site.data.latency | map: 'Name' | uniq %}
    {% for name in rows %}
    <tr>
        <td>
            <input type='checkbox' name='filter' id={{ name }} value={{ name }} />
            {{ name }}
        </td>
    </tr>
    {% endfor %}
</tbody>
</table>
</div>
<script src="/SOSDLeaderboard/scripts/checkbox.js" type="text/javascript"></script>

Results below are by model. Click on a header to sort by that measure. Click on an index name to open the relevant GitHub repo.

<div id="latency-leaderboard" class = "group" style="width:135%;">
This leaderboard displays the average lookup time for a randomly selected key in a sorted dataset of size 200M.

<p>Learned indexes are marked in <strong>bold.</strong></p>
<table id="latency-table" class="sortable tables">
    <thead>
        <tr>
            <th> </th>
            <th>Index / Index Size</th>
            <th style="text-align:center;"><span style="font-size:15px;">XS</span><br>
            <span style="font-size:10px;">Up to 0.01% of data size</span></th>
            <th style="text-align:center;"><span style="font-size:15px;">S</span><br>
            <span style="font-size:10px;">Up to 0.1% of data size</span></th>
            <th style="text-align:center;" class="startClick"><span style="font-size:15px;">M</span><br>
            <span style="font-size:10px;">Up to 1% of data size</span></th>
            <th style="text-align:center;"><span style="font-size:15px;">L</span><br>
            <span style="font-size:10px;">Up to 10% of data size</span></th>
            <th style="text-align:center;"><span style="font-size:15px;">XL</span><br>
            <span style="font-size:10px;">No limit</span></th>
            <th style="text-align:center;">Dataset</th> 
        </tr>
    </thead>
    <tbody>
    {% for row in site.data.latency %}
            {% tablerow pair in row %}
            {{ pair[1] }}
            {% endtablerow %}
    {% endfor %}
    </tbody>
</table>
Top approach in each column is bold and green. Yellow indicates 2-3x degraded performance. Orange/red indicates > 3x degraded performance.
<script src="/SOSDLeaderboard/scripts/annotate.js" type="text/javascript"></script>
</div>
<div id="buildtime-leaderboard" class = "group" style="width:135%;">
<table id="buildtime-table" class="sortable tables">
    <thead>
        <tr>
            <th> </th>
            <th>Index / Index Size</th>
            <th style="text-align:center;"><span style="font-size:15px;">XS</span><br>
            <span style="font-size:10px;">Up to 0.01% of data size</span></th>
            <th style="text-align:center;"><span style="font-size:15px;">S</span><br>
            <span style="font-size:10px;">Up to 0.1% of data size</span></th>
            <th style="text-align:center;" class="startClick"><span style="font-size:15px;">M</span><br>
            <span style="font-size:10px;">Up to 1% of data size</span></th>
            <th style="text-align:center;"><span style="font-size:15px;">L</span><br>
            <span style="font-size:10px;">Up to 10% of data size</span></th>
            <th style="text-align:center;"><span style="font-size:15px;">XL</span><br>
            <span style="font-size:10px;">No limit</span></th>
        </tr>
    </thead>
    <tbody>
    {% for row in site.data.buildtimes %}
        {% tablerow pair in row %}
        {{ pair[1] }}
        {% endtablerow %}
    {% endfor %}
    </tbody>
</table>
</div>
<div id="size-leaderboard" class = "group" style="width:135%;">
<table id="size-table" class="sortable tables">
    <thead>
        <tr>
            <th> </th>
            <th>Index / Index Size</th>
            <th style="text-align:center;"><span style="font-size:15px;">XS</span><br>
            <span style="font-size:10px;">Up to 0.01% of data size</span></th>
            <th style="text-align:center;"><span style="font-size:15px;">S</span><br>
            <span style="font-size:10px;">Up to 0.1% of data size</span></th>
            <th style="text-align:center;" class="startClick"><span style="font-size:15px;">M</span><br>
            <span style="font-size:10px;">Up to 1% of data size</span></th>
            <th style="text-align:center;"><span style="font-size:15px;">L</span><br>
            <span style="font-size:10px;">Up to 10% of data size</span></th>
            <th style="text-align:center;"><span style="font-size:15px;">XL</span><br>
            <span style="font-size:10px;">No limit</span></th>
        </tr>
    </thead>
    <tbody>
    {% for row in site.data.sizes %}
        {% tablerow pair in row %}
        {{ pair[1] }}
        {% endtablerow %}
    {% endfor %}
    </tbody>
</table>
</div>

## Plots
Here we provide a plot of index size against lookup latency on SOSD data. Indexes can be added and removed from the plot using
the corresponding buttons on the table.

<div hidden>
<select class="chzn-select" multiple="true" id="indexes" style="visibility:none;"  data-placeholder="Select indexes to graph"></select>
</div>
<button id="clear-chosen" onclick="clearChosen()">Clear Plot</button>


<span id="error_display" style="color:red"></span>
<div id="latency_plot">
<canvas id="latencyChart" style="height:500px;width:100%"></canvas>
</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/PapaParse/5.3.0/papaparse.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/chart.js@2.8.0"></script>
<script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/chosen/1.8.7/chosen.jquery.min.js"></script>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/chosen/1.8.7/chosen.css" />
<script type="text/javascript" src="/SOSDLeaderboard/scripts/graphs/graph_latency.js"></script>
<script type="text/javascript" src="/SOSDLeaderboard/scripts/graphs/selector.js"></script>
<script type="text/javascript" src="/SOSDLeaderboard/scripts/onStart.js"></script>
