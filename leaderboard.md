---
layout: page
title: "Leaderboard"
permalink: /leaderboard/
datatable: true
sorttable: true
---
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
<script type="text/javascript">
$(document).ready(function () {
  $('.group').hide();
  $('#latency-leaderboard').show();
  $('#select').change(function () {
    $('.group').hide();
    $('#'+$(this).val()).show();
  })
});
</script>

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

Results below are by model. Click on a header to sort by that measure. 

The smallest model size is constrained to 0.01% dataset size. Each successive category represents a 10x increase in size.
<div id="latency-leaderboard" class = "group">
Top approach in each row is bold and green. Yellow indicates 2-3x degraded performance. Red indicates > 3x degraded performance.
<table id="latency-table" class="sortable">
    <thead>
        <tr>
            <th>Model</th>
            <th style="text-align:center;"><span style="font-size:15px;">XS</span><br>
            <span style="font-size:12px;">0.01% of data size</span></th>
            <th style="text-align:center;"><span style="font-size:15px;">S</span><br>
            <span style="font-size:12px;">0.1% of data size</span></th>
            <th style="text-align:center;"><span style="font-size:15px;">S</span><br>
            <span style="font-size:12px;">1% of data size</span></th>
            <th style="text-align:center;"><span style="font-size:15px;">L</span><br>
            <span style="font-size:12px;">10% of data size</span></th>
            <th style="text-align:center;"><span style="font-size:15px;">XL</span><br>
            <span style="font-size:12px;">No limit</span></th>
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
<script src="/scripts/annotate.js" type="text/javascript"></script>
</div>
<div id="buildtime-leaderboard" class = "group">
<table id="buildtime-table" class="sortable">
    <thead>
        <tr>
            <th>Model</th>
            <th style="text-align:center;"><span style="font-size:15px;">XS</span><br>
            <span style="font-size:12px;">0.01% of data size</span></th>
            <th style="text-align:center;"><span style="font-size:15px;">S</span><br>
            <span style="font-size:12px;">0.1% of data size</span></th>
            <th style="text-align:center;"><span style="font-size:15px;">S</span><br>
            <span style="font-size:12px;">1% of data size</span></th>
            <th style="text-align:center;"><span style="font-size:15px;">L</span><br>
            <span style="font-size:12px;">10% of data size</span></th>
            <th style="text-align:center;"><span style="font-size:15px;">XL</span><br>
            <span style="font-size:12px;">No limit</span></th>
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
            <span style="font-size:12px;">0.01% of data size</span></th>
            <th style="text-align:center;"><span style="font-size:15px;">S</span><br>
            <span style="font-size:12px;">0.1% of data size</span></th>
            <th style="text-align:center;"><span style="font-size:15px;">S</span><br>
            <span style="font-size:12px;">1% of data size</span></th>
            <th style="text-align:center;"><span style="font-size:15px;">L</span><br>
            <span style="font-size:12px;">10% of data size</span></th>
            <th style="text-align:center;"><span style="font-size:15px;">XL</span><br>
            <span style="font-size:12px;">No limit</span></th>
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