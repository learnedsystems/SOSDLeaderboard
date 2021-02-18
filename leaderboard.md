---
layout: page
title: "Leaderboard"
permalink: /leaderboard/
datatable: true
sorttable: true
---
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>

## Leaderboard
Metric to display by:
<script src="/scripts/sorttable.js" type="text/javascript"></script>
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

Displaying results on datasets:
<select id="dataswitch">
    <option value="" disabled> -- 64-Bit datasets -- </option>
    <option value="all_uint64" selected>All 64-Bit Datasets</option>
    <option value="" disabled> - Real-world datasets - </option>
    <option value="osm_cellids_200M_uint64">OSM</option>
    <option value="fb_200M_uint64">Facebook</option>
    <option value="wiki_ts_200M_uint64">Wiki</option>
    <option value="books_200M_uint64">Books</option>
    <option value="" disabled> - Synthetic datasets - </option>
    <option value="normal_200M_uint64"> Normal </option>
    <option value="lognormal_200M_uint64"> Lognormal </option>
    <option value="uniform_sparse_200M_uint64"> Uniform sparse </option>
    <option value="uniform_dense_200M_uint64"> Uniform dense </option>
    <option value="" disabled> -- 32-Bit datasets -- </option>
    <option value="all_uint32">All 32-Bit Datasets</option>
    <option value="" disabled> - Real-world datasets - </option>
    <option value="fb_200M_uint32">Facebook</option>
    <option value="books_200M_uint32">Books</option>
    <option value="" disabled> - Synthetic datasets - </option>
    <option value="normal_200M_uint32"> Normal </option>
    <option value="lognormal_200M_uint32"> Lognormal </option>
    <option value="uniform_sparse_200M_uint32"> Uniform sparse </option>
    <option value="uniform_dense_200M_uint32"> Uniform dense </option>
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
<script src="/scripts/checkbox.js" type="text/javascript"></script>

Results below are by model. Click on a header to sort by that measure. Click on an index name to open the relevant GitHub repo.

<div id="latency-leaderboard" class = "group">
<table id="latency-table" class="sortable tables">
    <thead>
        <tr>
            <th>Model</th>
            <th style="text-align:center;"><span style="font-size:15px;">XS</span><br>
            <span style="font-size:10px;">0.01% of data size</span></th>
            <th style="text-align:center;"><span style="font-size:15px;">S</span><br>
            <span style="font-size:10px;">0.1% of data size</span></th>
            <th style="text-align:center;" class="startClick"><span style="font-size:15px;">M</span><br>
            <span style="font-size:10px;">1% of data size</span></th>
            <th style="text-align:center;"><span style="font-size:15px;">L</span><br>
            <span style="font-size:10px;">10% of data size</span></th>
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
Top approach in each column is bold and green. Yellow indicates 2-3x degraded performance. Red indicates > 3x degraded performance.
<script src="/scripts/annotate.js" type="text/javascript"></script>
</div>
<div id="buildtime-leaderboard" class = "group">
<table id="buildtime-table" class="sortable tables">
    <thead>
        <tr>
            <th>Model</th>
            <th style="text-align:center;"><span style="font-size:15px;">XS</span><br>
            <span style="font-size:10px;">0.01% of data size</span></th>
            <th style="text-align:center;"><span style="font-size:15px;">S</span><br>
            <span style="font-size:10px;">0.1% of data size</span></th>
            <th style="text-align:center;" class="startClick"><span style="font-size:15px;">M</span><br>
            <span style="font-size:10px;">1% of data size</span></th>
            <th style="text-align:center;"><span style="font-size:15px;">L</span><br>
            <span style="font-size:10px;">10% of data size</span></th>
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
<div id="size-leaderboard" class = "group">
<table id="size-table" class="sortable tables">
    <thead>
        <tr>
            <th>Model</th>
            <th style="text-align:center;"><span style="font-size:15px;">XS</span><br>
            <span style="font-size:10px;">0.01% of data size</span></th>
            <th style="text-align:center;"><span style="font-size:15px;">S</span><br>
            <span style="font-size:10px;">0.1% of data size</span></th>
            <th style="text-align:center;" class="startClick"><span style="font-size:15px;">M</span><br>
            <span style="font-size:10px;">1% of data size</span></th>
            <th style="text-align:center;"><span style="font-size:15px;">L</span><br>
            <span style="font-size:10px;">10% of data size</span></th>
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
<script src="/scripts/sort.js" type="text/javascript"></script>