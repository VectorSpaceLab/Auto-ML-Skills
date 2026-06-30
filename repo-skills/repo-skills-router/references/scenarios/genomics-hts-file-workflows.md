# Genomics HTS File Workflows

## When To Read

SAM/BAM/CRAM alignment files, VCF/BCF variant files, tabix-indexed genomic interval tables, FASTA/FASTQ sequence access, htslib/samtools/bcftools Python wrappers, and high-throughput sequencing file troubleshooting.

## Repo Skill Options

<!-- DISCO_SCENARIO:genomics-hts-file-workflows:START -->
### `pysam`

Role: Guides agents using pysam for Pythonic HTS file I/O, genomic interval indexing, sequence fetching, bundled samtools/bcftools dispatchers, and installation or Cython-extension troubleshooting.
Read when: The request names pysam, htslib, samtools or bcftools Python wrappers, AlignmentFile, AlignedSegment, VariantFile, VariantHeader, VariantRecord, TabixFile, FastaFile, FastxFile, tabix_index, tabix_compress, SAM/BAM/CRAM, VCF/BCF, BED/GTF/GFF tabix files, FASTA/FASTQ, PysamDispatcher, SamtoolsError, catch_stdout, save_stdout, or errors involving genomic coordinate conventions, missing BAM/VCF/tabix/FASTA indexes, source builds, Python.h, external htslib, or lib-prefixed pysam Cython modules.
Best for: Opening, writing, indexing, fetching, and troubleshooting SAM/BAM/CRAM alignments; VCF/BCF variants and headers; tabix-indexed interval files; FASTA/FASTQ sequence access; translating samtools/bcftools shell commands into pysam Python dispatchers; and diagnosing pysam install/build/import/link failures.
Avoid when: Use a downstream genomics analysis package skill when the task is biological interpretation, differential expression, variant annotation pipelines, or workflow management rather than pysam file/API mechanics. Use generic Python packaging guidance only when the problem is unrelated to pysam, htslib, samtools, bcftools, genomic file formats, or Cython extension integration.
Useful entry points: `pysam/SKILL.md`, `pysam/sub-skills/alignment-io/SKILL.md`, `pysam/sub-skills/variant-io/SKILL.md`, `pysam/sub-skills/tabix-fasta/SKILL.md`, `pysam/sub-skills/command-wrappers/SKILL.md`, `pysam/sub-skills/troubleshooting-build/SKILL.md`.

<!-- DISCO_SCENARIO:genomics-hts-file-workflows:END -->

## How To Choose

Choose the repo skill whose package or API surface owns the requested genomics file workflow: pysam for Python htslib/samtools/bcftools bindings, alignment/variant/tabix/FASTA/FASTQ file APIs, and command-wrapper troubleshooting. Choose `pysam` when a task needs Python code or troubleshooting around HTS file formats, genomic interval coordinates and indexes, pysam AlignmentFile/VariantFile/TabixFile/FastaFile/FastxFile APIs, or pysam.samtools/pysam.bcftools command dispatchers. Do not choose `pysam` for high-level biological analysis unless the immediate blocker is file I/O, indexing, command-wrapper translation, or package build/import behavior.
