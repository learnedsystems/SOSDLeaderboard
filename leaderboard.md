---
layout: page
title: "Leaderboard"
permalink: /leaderboard/
datatable: true
sorttable: true
---
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>

## Results
Benchmark results are presented below. Initial rankings were calculated through 
the average improvement of the index over binary search.

## Leaderboard
Metric to display by:
<script src="/scripts/sorttable.js" type="text/javascript"></script>
<select id="select">
    <option value="latency-leaderboard">Latency (ns)</option>
    <option value="buildtime-leaderboard">Build time (ns)</option>
    <option value="size-leaderboard">Size</option>
</select>

To select which indexes to display:
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
<div id="display" style="height:400px;overflow:auto;display:none;">
<table id="display-boxes">
<tbody>
    {% for row in site.data.latency %}
    <tr>
        <td>
            <input type='checkbox' name='filter' id={{ row.Name }} value={{ row.Name }} />
            {{ row.Name }}
        </td>
    </tr>
    {% endfor %}
</tbody>
</table>
</div>
<script src="/scripts/checkbox.js" type="text/javascript"></script>

Results below are by model. Click on a header to sort by that measure. Click on an index name to open the relevant GitHub repo.

<div id="latency-leaderboard" class = "group">
<table id="latency-table" class="sortable">
    <thead>
        <tr>
            <th>Model</th>
            <th style="text-align:center;"><span style="font-size:15px;">XS</span><br>
            <span style="font-size:10px;">0.01% of data size</span></th>
            <th style="text-align:center;"><span style="font-size:15px;">S</span><br>
            <span style="font-size:10px;">0.1% of data size</span></th>
            <th style="text-align:center;"><span style="font-size:15px;">M</span><br>
            <span style="font-size:10px;">1% of data size</span></th>
            <th style="text-align:center;"><span style="font-size:15px;">L</span><br>
            <span style="font-size:10px;">10% of data size</span></th>
            <th style="text-align:center;"><span style="font-size:15px;">XL</span><br>
            <span style="font-size:10px;">No limit</span></th>
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
Top approach in each row is bold and green. Yellow indicates 2-3x degraded performance. Red indicates > 3x degraded performance.
<script src="/scripts/annotate.js" type="text/javascript"></script>
</div>
<div id="buildtime-leaderboard" class = "group">
<table id="buildtime-table" class="sortable">
    <thead>
        <tr>
            <th>Model</th>
            <th style="text-align:center;"><span style="font-size:15px;">XS</span><br>
            <span style="font-size:10px;">0.01% of data size</span></th>
            <th style="text-align:center;"><span style="font-size:15px;">S</span><br>
            <span style="font-size:10px;">0.1% of data size</span></th>
            <th style="text-align:center;"><span style="font-size:15px;">M</span><br>
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
<table id="size-table" class="sortable">
    <thead>
        <tr>
            <th>Model</th>
            <th style="text-align:center;"><span style="font-size:15px;">XS</span><br>
            <span style="font-size:10px;">0.01% of data size</span></th>
            <th style="text-align:center;"><span style="font-size:15px;">S</span><br>
            <span style="font-size:10px;">0.1% of data size</span></th>
            <th style="text-align:center;"><span style="font-size:15px;">M</span><br>
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