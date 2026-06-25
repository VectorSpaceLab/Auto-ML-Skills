# Bulk RNA-Seq Differential Expression Analysis

## When To Read

Bulk RNA-seq raw-count differential expression analysis, DESeq2-like Python workflows, count/metadata validation, contrasts, Wald tests, LFC shrinkage, VST, and PyDESeq2 troubleshooting.

## Repo Skill Options

<!-- SKILLQED_SCENARIO:bulk-rna-seq-differential-expression-analysis:START -->
### `pydeseq2`

Role: Use PyDESeq2 as a Python package for bulk RNA-seq differential expression workflows from data validation through fitted models and statistical results.
Read when: User mentions PyDESeq2, pydeseq2, DeseqDataSet, DeseqStats, DESeq2 in Python, bulk RNA-seq counts, count matrix and metadata, formula designs, contrasts, Wald tests, padj, log2FoldChange, lfc_shrink, VST, or Cooks outliers.
Best for: Preparing PyDESeq2 inputs, running DeseqDataSet.deseq2 workflows, computing DeseqStats results, interpreting contrasts and result tables, troubleshooting count/design errors, and inspecting normalization/VST internals.
Avoid when: Use single-cell omics skills for Scanpy/scvi single-cell workflows, general pandas/AnnData skills for non-DEA data wrangling, R/Bioconductor guidance for unsupported DESeq2-only features, and Python repository maintenance for editing PyDESeq2 source code.
Useful entry points: `pydeseq2/SKILL.md`, `pydeseq2/sub-skills/data-io-validation/SKILL.md`, `pydeseq2/sub-skills/dea-workflows/SKILL.md`, `pydeseq2/sub-skills/statistics-and-results/SKILL.md`, `pydeseq2/sub-skills/model-fitting-internals/SKILL.md`.

<!-- SKILLQED_SCENARIO:bulk-rna-seq-differential-expression-analysis:END -->

## How To Choose

Use this scenario for package-specific bulk RNA-seq DEA workflows. Do not route general Scanpy/single-cell tasks here unless the user explicitly asks for PyDESeq2 or bulk count differential expression. Choose `pydeseq2` when the user is using PyDESeq2 or asks for DESeq2-like bulk RNA-seq analysis in Python. Start at the root router, then pick data I/O before model construction, DEA workflows for fitting, statistics/results after fitting, or model-fitting internals for staged normalization/VST/debugging.
