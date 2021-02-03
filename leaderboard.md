---
layout: page
title: "Leaderboard"
permalink: /leaderboard/
datatable: true
sorttable: true
---

## Results
Benchmark results are presented below. Initial rankings were calculated through 
the average improvement of the index over binary search.

## Leaderboard
Click on a table heading to sort by it.
<script src="{{ base.url | prepend: site.url }}/scripts/sorttable.js" type="text/javascript"></script>
<table id="leaderboard" class="sortable">
    <thead>
        <tr>
            <th>Rank</th>
            <th>Model</th>
            <th>XS</th>
            <th>S</th>
            <th>M</th>
            <th>L</th>
            <th>X</th>
            <th>BS Improvement</th>
            <th>Build (ns)</th>
        </tr>
    </thead>
    <tbody>
        {% for item in indexes %}
        <TR>
            <TD>{{item.rank}}</TD>
            <TD>{{item.name}}</TD>
            <TD>{{item.xsmalltime}}</TD>
            <TD>{{item.smalltime}}</TD>
            <TD>{{item.mediumtime}}</TD>
            <TD>{{item.largetime}}</TD>
            <TD>{{item.xlargetime}}</TD>
            <TD>{{item.improvement}}</TD>
            <TD>{{item.buildtime}}</TD>
        </TR>
        {% endfor %}
        <TR>
            <TD>1</TD>
            <TD>2</TD>
            <TD>3</TD>
            <TD>4</TD>
            <TD>5</TD>
            <TD>6</TD>
            <TD>7</TD>
            <TD>8</TD>
            <TD>9</TD>
        </TR>
        <TR>
            <TD>2</TD>
            <TD>2</TD>
            <TD>3</TD>
            <TD>4</TD>
            <TD>5</TD>
            <TD>6</TD>
            <TD>7</TD>
            <TD>8</TD>
            <TD>9</TD>
        </TR>
    </tbody>
</table>
