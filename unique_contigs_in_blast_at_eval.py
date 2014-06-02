#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os, collections

def parse_fasta_to_dict(fasta_file):
	assembly_dict = {}
	with open(fasta_file) as fh:
		header = ''
		seq = ''
		for line in fh:
			line = line.rstrip("\n")
			if line.startswith(">"):
				if (header):
					assembly_dict[header] = seq
				seq = ''
				header = line.split(' ')[0][1:]
			else:
				seq += line
		assembly_dict[header] = seq
	return assembly_dict

def parse_blast_to_dict(blast_file):
	blast_dict = collections.defaultdict(dict) 
	with open(blast_file) as fh:
		for line in fh:
			temp = line.rstrip("\n").rsplit("\t")
			query, subject, evalue = str(temp[0]), str(temp[1]), float(temp[10])
			if query in blast_dict:
				if subject in blast_dict[query]:
					if evalue >= blast_dict[query][subject]:
						continue
					else:
						blast_dict[query][subject] = evalue
				else:
					blast_dict[query][subject] = evalue
			else:
				blast_dict[query][subject] = evalue
	return blast_dict

def print_unique_contigs_at_cutoffs(blast_dict, evalue_cutoffs):
	sys.stdout.write(blast_file)
	for cutoff in evalue_cutoffs:
		unique_contigs_at_cutoff = 0
		contig_span_at_cutoff = 0
		for query in blast_dict:
			for subject in blast_dict[query]:
				if blast_dict[query][subject] <= cutoff:
					unique_contigs_at_cutoff += 1
					contig_span_at_cutoff += len(assembly_dict[query])
					break # breaks out of 'for' loop when one sybject below cutoff is found
		#sys.stdout.write("\t" + str(unique_contigs_at_cutoff))
		sys.stdout.write("\t" + str(contig_span_at_cutoff))
	sys.stdout.write("\n")

if __name__ == "__main__":
	fasta_file = sys.argv[1]
	assembly_dict = parse_fasta_to_dict(fasta_file)
	evalue_cutoffs = [ 1e-5, 1e-10, 1e-15, 1e-20, 1e-25, 1e-30, 1e-35, 1e-40, 1e-45, 1e-50 ]
	print "dataset" + "\t" + "\t".join(map(str, evalue_cutoffs))
	blast_files = sys.argv[2:]
	for blast_file in blast_files: 
		blast_dict = parse_blast_to_dict(blast_file)
		print_unique_contigs_at_cutoffs(blast_dict, evalue_cutoffs)

