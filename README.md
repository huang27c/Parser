# Parser

This is a graphml file parser. The parser takes in a graphmil file with directed graph and stores information about nodes and edges in seperate csv files, including a 2d matrix representation.  

## Getting Started

### Prerequisites

* [yEd Graph Editor](https://www.yworks.com/products/yed#yed-support-resources) - The graph editor 

### Installing

Clone the project

## Running 

For example: a graph with two nodes and a directed edge saved as test.graphml

<img width="174" alt="Screen Shot 2019-11-04 at 2 44 01 PM" src="https://user-images.githubusercontent.com/27383828/68154151-e0f39780-ff14-11e9-8bcd-0fb3137c78fb.png">

Run command
```
python parser.py "test.graphml"
```
Example output

1. test_nodes.csv
```
id, label, x, y
n0,L1,28,40
n1,L2,120,40
```

2. test_edges.csv
```
id, source, target, distance
e0,n1,n0,92.0
```
3. test_matrix.csv
```
0.00 0.00
92.00 0.00
```

## Built With

* [Sublime Text](https://www.sublimetext.com) - The text editor for python

## Authors

* **Ching Ching Huang** - *Initial work* 
