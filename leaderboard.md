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
<select id="select" onchange="changeTable(this.value)">
    <option value="latency-leaderboard">Latency (ns)</option>
    <option value="buildtime-leaderboard">Build time (ns)</option>
    <option value="size-leaderboard">Size (MB)</option>
</select>

Results below are by model.
<div id="latency-leaderboard" class = "group">
<table id="leaderboard" class="sortable">
    <thead>
        <tr>
            <th>Model</th>
            <th>XS</th>
            <th>S</th>
            <th>M</th>
            <th>L</th>
            <th>XL</th>
        </tr>
    </thead>
    <tbody>
    {% for row in site.data.latency %}
        {% if forloop.first %}
            {% continue %}
        {% endif %}

        {% tablerow pair in row %}
        {{ pair[1] }}
        {% endtablerow %}
    {% endfor %}
    </tbody>
</table>
</div>
<div id="buildtime-leaderboard" class = "group">
<table id="leaderboard" class="sortable">
    <thead>
        <tr>
            <th>Model</th>
            <th>XS</th>
            <th>S</th>
            <th>M</th>
            <th>L</th>
            <th>XL</th>
        </tr>
    </thead>
    <tbody>
    {% for row in /data/buildtimes %}
        {% if forloop.first %}
            {% continue %}
        {% endif %}

        {% tablerow pair in row %}
        {{ pair[1] }}
        {% endtablerow %}
    {% endfor %}
    </tbody>
</table>
</div>
<div id="size-leaderboard" class = "group">
<table id="leaderboard" class="sortable">
    <thead>
        <tr>
            <th>Model</th>
            <th>XS</th>
            <th>S</th>
            <th>M</th>
            <th>L</th>
            <th>XL</th>
        </tr>
    </thead>
    <tbody>
    {% for row in site.data.sizes %}
        {% if forloop.first %}
            {% continue %}
        {% endif %}

        {% tablerow pair in row %}
        {{ pair[1] }}
        {% endtablerow %}
    {% endfor %}
    </tbody>
</table>
</div>