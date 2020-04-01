# VCF Adjunct Parser #

Small library for parsing vcf files. Based on [vcf_parser](https://github.com/moonso/vcf_parser)

usage examples:
    
    - Calculate the ploidy of presented individuals
    - Calculate the histogram for distribution of lengths of intervals between heterozygotes


## Installation ##

```bash
>git clone https://github.com/fkbyf14/vcf_adjunct_parser.git
>cd vcf_adjunct_parser
>python setup.py install
```

## Usage ##


After get the file vcf_adjunct_parser/usages/test_task.py:

- output: the number of ploidy (1 for haploidy, 2 for diploidy and so on)
```
>python3 test_task.py --file test_vcf.vcf
```
- output: distribution of lengths of intervals between heterozygotes in dictionary: {distance: number of neighbouring heterozygotes}, matplotlib drawing;
for perform task target output: array H - histogram of lengths distribution is necessary to uncomment code block
after such the comm (# for perform task target output: array H - histogram of lengths distribution)

```
>python3 test_task.py --file test_vcf.vcf --individual father

```
