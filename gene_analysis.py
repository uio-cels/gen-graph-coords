from __future__ import print_function
from __future__ import absolute_import
from DbWrapper import DbWrapper
from offsetbasedgraph import LinearInterval
from main import get_flanks


def interval_from_gene(gene):
    interval = LinearInterval("hg38",
                              gene["chrom"],
                              gene["txStart"],
                              gene["txEnd"])
    interval.gene_name = gene["name"]
    return interval


def get_flanking_lins():
    db = DbWrapper()
    genes = db.get_alt_genes()
    gene_intervals = map(interval_from_gene,
                         genes)

    alt_loci_infos = db.get_alt_loci_infos(False)
    names = map(lambda x: x["name"], alt_loci_infos)
    partitions = [get_flanks(ali) for ali in alt_loci_infos]
    alt_partitions = [par[1] for par in partitions]
    lin_ref_dict = dict(zip(names, alt_partitions))

    real_alt_genes = [gi for gi in gene_intervals if
                      lin_ref_dict[gi.chromosome][1].intersects(gi)]

    # Find genes that are partly in aligned regions
    intersecting_genes = [gi for gi in real_alt_genes if
                          gi.intersects(lin_ref_dict[gi.chromosome][0]) or
                          gi.intersects(lin_ref_dict[gi.chromosome][2])]

    print(len(intersecting_genes))
    print(len(real_alt_genes))
    print(len(intersecting_genes)/float(len(real_alt_genes)))


def calculate_original_main_spans():
    """
    Find all genes on the main path that intersects both
    with a flanking region and a pure main region.
    """
    db = DbWrapper()
    genes = db.get_main_genes()
    gene_intervals = [interval_from_gene(gene) for gene in genes]
    alt_loci_infos = db.get_alt_loci_infos(False)
    partitions = [get_flanks(ali) for ali in alt_loci_infos]
    main_partitions = [par[0] for par in partitions]

    lin_ref_dict = {}
    for gene in gene_intervals:
        lin_ref_dict[gene.chromosome] = []

    for i, ali in enumerate(alt_loci_infos):
        chrom = ali["chrom"]
        if chrom not in lin_ref_dict:
            lin_ref_dict[chrom] = []
        lin_ref_dict[chrom].append(main_partitions[i])

    intersecting_genes = [gi for gi in gene_intervals if
                          any([(gi.intersects(interval[0]) or
                                gi.intersects(interval[2])) and
                               not gi.intersects(interval[2]) for
                               interval in lin_ref_dict[gi.chromosome]])
                          ]
    crossing_genes = [gi for gi in intersecting_genes if
                      any([(interval[0].intersects(gi) and not interval[0].contains(gi)) and
                           (interval[2].intersects(gi) and not interval[2].contains(gi)) for
                           interval in lin_ref_dict[gi.chromosome]])]

    print(len(gene_intervals))
    print(len(intersecting_genes))
    print(len(crossing_genes))
    for gene in crossing_genes:
        print(gene.gene_name, gene)


def calculate_main_spans():
    """
    Find all genes on main paths that overlaps with real
    alt sequence, and find ratio of those that intersects both
    main and real alt.
    """
    db = DbWrapper()
    genes = db.get_main_genes()
    gene_intervals = [interval_from_gene(gene) for gene in genes]
    alt_loci_infos = db.get_alt_loci_infos(False)
    partitions = [get_flanks(ali) for ali in alt_loci_infos]
    main_partitions = [par[0] for par in partitions]
    lin_ref_dict = {}
    for gene in gene_intervals:
        lin_ref_dict[gene.chromosome] = []

    for i, ali in enumerate(alt_loci_infos):
        chrom = ali["chrom"]
        if chrom not in lin_ref_dict:
            lin_ref_dict[chrom] = []
        lin_ref_dict[chrom].append(main_partitions[i])

    print(len(genes), len(gene_intervals))

    real_alt_genes = [gi for gi in gene_intervals if
                      any([interval[1].intersects(gi) for
                           interval in lin_ref_dict[gi.chromosome]])]

    # Find genes that are partly in aligned regions
    intersecting_genes = [gi for gi in real_alt_genes if
                          any([gi.intersects(interval[0]) +
                               gi.intersects(interval[1]) +
                               gi.intersects(interval[2]) > 1 for
                               interval in lin_ref_dict[gi.chromosome]])
                          ]

    print(len(intersecting_genes))
    print(len(real_alt_genes))
    print(len(intersecting_genes)/float(len(real_alt_genes)))
    print(len(intersecting_genes)/float(len(genes)))

if __name__ == "__main__":

    calculate_original_main_spans()
    # get_flanking_lins()
    # calculate_main_spans()
    exit(0)
