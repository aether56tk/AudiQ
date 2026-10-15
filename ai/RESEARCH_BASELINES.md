# AudiQ AI — Research Baseline Review

Checked 17 September 2026.

## 1. GreenCUBIC / AudiogramDigitization

Repository: https://github.com/GreenCUBIC/AudiogramDigitization

The repository contains a Python audiogram digitization algorithm using deep convolutional neural networks and an Electron annotation application. Its README describes retraining YOLOv5 object detectors from annotated audiograms and replacing model weights for audiogram, symbol, and axis-label detection. It outputs structured threshold objects containing ear, conduction, masking, frequency and threshold fields.

Repository license: MIT. Dataset rights are a separate question; do not assume the repository license grants rights to every underlying image/data source.

## 2. MAIN2021

Repository: https://github.com/jacklishufan/MAIN2021

The README describes the Open Audiogram Dataset and a multi-stage pipeline with gram, axis and mask detectors. It provides a Dropbox location for dataset/pretrained weights and scripts for training and benchmarking. The reported benchmark includes frequency-label and hearing-loss-label metrics, with different results for scanned and camera images.

Repository license must be checked before reusing code in a commercial AudiQ implementation. Treat the dataset and pretrained weights as separately licensed/access-controlled until their terms are verified.

## 3. AutoAudiogram

Repository: https://github.com/biodatlab/autoaudiogram

The project reports annotation of 200 audiograms containing graphs, tables and eight audiological symbols. It provides training code for graph/table detection and symbol detection and a severity-classification stage. The README states that the 200-image dataset is private and requires a data-access form for research/educational use.

Do not copy that dataset into AudiQ unless access is granted and the terms permit the intended use.

## 4. SyntHH

Repository: https://github.com/evidENT-AI/SyntHH

SyntHH focuses on synthetic audiometric data generation and validation. It is useful later for controlled augmentation, privacy-preserving experiments and edge-case generation, but it is not our first symbol-detection dataset.

## Decision for AudiQ v0.1

We will NOT train a clinical interpretation model first.

First target: robust visual detection of audiogram marks/symbols.

Pipeline:

image -> chart/axis calibration -> symbol detector -> candidate coordinates -> frequency/dB mapping -> confidence -> human verification -> PTA/clinical calculations

The model must never silently turn an uncertain visual detection into a clinical conclusion.

## Data policy

- Use only de-identified or synthetic development data.
- Do not commit patient images to this public repository.
- Keep third-party datasets outside the repository unless their license/access terms explicitly permit redistribution.
- Keep an independent teacher-verified validation set separate from training data.
