# About
This repository contains code supporting the paper _Coordinates and Intervals on Offset-based graphs_.
See the section "How to run the gene experiments" for information about how to run the gene experiments.

## Web-tool for visualising genes on GRCh38

For a demo of the interactive web tool, please follow this link:  http://46.101.93.163/gen-graph-coords/

## Requirements
There is one requirement:
* The python package _offsetbasedgraph_. Install it with `pip3 install offsetbasedgraph`.
## Setup
Install the above requirements. Then clone this repo:

```
git clone git@github.com:uio-cels/gen-graph-coords.git
```

# How to run the gene experiments

### Experiment 1: Se relationship between genes on alt loci and main chromosomes on GRCh38
In this experiment, we create a simple graph from GRCh38 by
merging the "flanking regions" of the alternatice loci with the main path.
We then represent refseq genes on this graph, and investigate the relationship between transcripts on the alternative loci and the main chromosomes.
The following steps will reproduce the experiment:

```
# Create grch38 graph with translation object.
python3 gen_graph_coords.py create_graph data/grch38.chrom.sizes data/grch38_alt_loci.txt grch38.graph
# Analyse genes
python3 gen_graph_coords.py check_duplicate_genes grch38.graph data/genes/genes_refseq.txt
```

### Experiment 2: Representing genes by multi-path intervals on GRCh38
In this experiment, we create a more complex graph by merging parts of the alternative loci, using alignments generated by NCBI. We then investigate the relationship between transcripts on the alternative loci and main chromosomes using multi-path intervals.

The following will reproduce the experiment for *fuzzy multi-path intervals*:

```
python3 gen_graph_coords.py analyse_multipath_genes data/grch38.chrom.sizes data/grch38_alt_loci.txt data/alt_alignments/ data/genes/genes_refseq.txt fuzzy
```

Using *critical-interval multi-path intervals* :
```
python3 gen_graph_coords.py analyse_multipath_genes data/grch38.chrom.sizes data/grch38_alt_loci.txt data/alt_alignments/ data/genes/genes_refseq.txt critical
```

