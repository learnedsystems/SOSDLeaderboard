---
layout: page
title: "Home Page"
permalink: /home/
datatable: true
---
# SOSD
## The Search on Sorted Data benchmark
Search on Sorted Data (SOSD) is a new benchmark that allows researchers
to compare their new (learned) index structures on both synthetic and real-world datasets. It is provided 
as C++ open source code that incurs little overhead (8 instructions and 1 cache miss per lookup), comes 
with diverse synthetic and real-world datasets, and provides efficient baseline implementations. 
Here we provide an interface and leaderboard for index structures on our own hosted SOSD benchmark.

## Leaderboard
```html
<table id="leaderboard" class="display">
    <thead>
        <tr>
            <th>Rank</th>
            <th>Model</th>
            <th>XS</th>
            <th>S</th>
            <th>M</th>
            <th>L</th>
            <th>X</th>
            <th>Improvement from BS</th>
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
    </tbody>
</table>
```