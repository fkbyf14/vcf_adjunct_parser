#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import logging
import random
import matplotlib.pyplot as plt
from vcf_adjunct_parser import VCFAdjunctParser

DEFAULT_VCF_PATH = "test_vcf.vcf"


def get_dataline(vcf_parser):
    for variant in vcf_parser:
        yield variant


def get_ploidy(data_line, individual):
    """get ploidy of abitrary presented individual (suppose it is equal for all of them)"""
    return len(data_line['genotypes'].get(individual).alleles)


def get_distance_distr(heterozygotes_pos):
    """return dict distribution, where key is distances between heterozygotes,
    value - numbers of neighbouring heterozygotes that have distance between them equal to key's value"""
    distribution = dict()
    for i in range(len(heterozygotes_pos)):
        for j in range(i + 1, len(heterozygotes_pos)):
            dist = heterozygotes_pos[j] - heterozygotes_pos[i]
            if not distribution.get(dist):
                distribution[dist] = 2
            else:
                distribution[dist] += 1
    return distribution


def draw_hist(distribution):
    freq = list(distribution.values())
    distances = list(distribution.keys())
    ax = plt.gca()
    ax.bar(distances, freq, 10000, align='center')
    ax.set_xticks(distances)
    plt.show()


def main(vcf_parser, individual):
    logging.basicConfig(format='[%(asctime)s] %(levelname).1s %(message)s', level=logging.INFO)
    ploidy_list = list()
    heterozygotes_pos = list()
    for line in get_dataline(vcf_parser):
        ploidy_list.append(get_ploidy(line, random.choice(list(line['genotypes'].keys()))))

        if individual:
            if line['genotypes'][individual].heterozygote:
                heterozygotes_pos.append(int(line['POS']))

    logging.info("ploidy_list is: {}".format(ploidy_list))

    if heterozygotes_pos:
        lengths_distribution = get_distance_distr(heterozygotes_pos)
        logging.info("lengths distribution is: {}".format(lengths_distribution))
        draw_hist(lengths_distribution)
        logging.info("heterozygotes_pos is: {}".format(heterozygotes_pos))

        # for perform task target output: array H - histogram of lengths distribution
        """
        histogram = list()
        for i in range(min(distribution.keys()), max(distribution.keys()) + 1):
            if distribution.get(i):
                histogram.append(distribution.get(i))
            else:
                histogram.append(0)
        logging.info("histogram of lengths distribution is: {}".format(histogram))
        return histogram
        """
        return lengths_distribution
    return ploidy_list


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', help='VCF file path', nargs='?',
                        default=DEFAULT_VCF_PATH)
    parser.add_argument('--individual', help='name of one of the presented individuals ', nargs='?')

    args = parser.parse_args()

    vcf_parser = VCFAdjunctParser(infile=args.file, split_variants=False, check_info=True)

    try:
        main(vcf_parser, args.individual)
    except:
        logging.exception("Unexpected error")

