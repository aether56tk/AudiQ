# AudiQ Validation Protocol

## Purpose
Validate photo-based threshold extraction and masking decision-support separately from the manual calculation workflow.

## Dataset
Create a governed, de-identified benchmark of audiogram images covering:
- different layouts and image qualities
- handwritten and printed examples where permitted
- AC and BC symbols
- masked/unmasked examples
- common annotation/scan variations

Maintain expert reference thresholds from the original source.

## Extraction evaluation
For every candidate point, record:
- correct extraction
- missed point
- false point
- frequency error
- threshold error
- unreadable/failed case

Report error distributions and failure rates. Human verification remains mandatory.

## Masking decision-support evaluation
Create predefined cases with expert-reviewed reference decisions. Evaluate:
- recommendation agreement
- missing required inputs
- inappropriate recommendations
- handling of insufficient information

Do not treat the tool as a substitute for the supervising clinician or the applicable protocol.

## Reproducibility
Record:
- Git commit SHA
- browser/OS
- OpenCV.js version
- image-set version
- extraction configuration
- masking-rule version

## Boundary
Software tests and a small demonstration set do not establish clinical validity. Do not publish diagnostic-performance claims until the governed validation is completed.
