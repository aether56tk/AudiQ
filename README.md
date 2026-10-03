# AudiQ

**AudiQ is an educational audiometry workflow and learning utility for BASLP students and supervised clinical training.**

## Current workflow

- Manual AC/BC threshold entry
- 3-frequency PTA calculation (500, 1000 and 2000 Hz)
- Audiogram visualization
- Speech-audiometry documentation fields
- Masking decision-support screen
- Audiogram-photo candidate extraction
- Mandatory human verification before analysis/reporting
- Print/save-to-PDF workflow
- Responsive browser interface

## Safety boundary

AudiQ is **not calibrated audiometric equipment and is not an autonomous diagnostic system**.

Photo extraction produces threshold **candidates** that must be reviewed against the original audiogram. Masking output is decision support and must be checked against the transducer, interaural attenuation, occlusion effects, masked bone-conduction information and the protocol used by the supervising clinician.

Do not enter identifiable patient information into the public deployment or repository.

## Engineering status

### Complete software work

- Single production entry point
- Candidate extraction with explicit verification gate
- Clinical calculation/report workflow
- Privacy and safety messaging
- GitHub Pages deployment
- Repository cleanup and documentation

### Validation is the remaining research item

Clinical/research validation of photo extraction and decision-support behavior remains pending.

Before any accuracy or diagnostic-performance claim:

1. Define a governed, de-identified test set.
2. Establish expert reference values.
3. Freeze the software version.
4. Compare extracted thresholds with reference thresholds.
5. Report error distributions and failure cases.
6. Evaluate masking guidance against the applicable institutional/professional procedure.

Software tests alone do not establish clinical validity.

## Technology

- HTML5
- CSS3
- Vanilla JavaScript
- Canvas
- OpenCV.js for experimental image processing
- GitHub Pages
- No application backend

## Project files

- [Security policy](SECURITY.md)
- [Contributing guide](CONTRIBUTING.md)
- [Validation status](VALIDATION_STATUS.md)
- [Citation metadata](CITATION.cff)

## Author

**Adithyan Tk** — BASLP Student | Clinical Technology & HealthTech Projects

## License

MIT
