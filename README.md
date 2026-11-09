# Code 128 Barcode Encoder

## Live Demo

Try the Code 128 Barcode Encoder here:

[Code 128 Barcode Encoder](https://zetiee.site/code128/)

# Encoder

A Python implementation of a **Code 128 barcode encoder** based on a pseudocode algorithm. It converts ASCII text into Code 128 symbol values, calculates and verifies a modulo-103 checksum, and draws the resulting barcode as a PNG bitmap.

The implementation uses a **greedy heuristic** to decide when to switch to Code Set C; it does **not** guarantee the shortest possible symbol sequence.

## Requirements

- Python 3
- [Pillow](https://pillow.readthedocs.io/) for image generation

## local Setup

From the project folder, create and activate a virtual environment:

**macOS / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install pillow
```

**Windows (PowerShell):**

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install pillow
```

Using a virtual environment is particularly helpful when a system-managed Python installation prevents global package installation (`externally-managed-environment`).

## Usage

Run the program from the directory containing `code128_encoder.py`:

```bash
python code128_encoder.py
```

When prompted, enter text to encode:

```text
Enter text to encode: CSE370
Encoded symbols: [104, 35, 51, 37, 19, 23, 16, 21, 106]
Checksum: 21
Saved barcode to: barcode.png
```

The resulting **`barcode.png`** is saved in your current working directory. Running the program again with the default filename overwrites the previous image.

You can also use the function from another Python file:

```python
from code128_encoder import create_code128

create_code128("ABC123456", "my_barcode.png")
```

`create_code128(text, filename="barcode.png")` saves the image and returns a Pillow `Image` object.

## How it works

1. **Validate input:** reject empty strings and characters outside the 7-bit ASCII range (0–127).
2. **Select a starting code set:** use Start C (`105`) if there are at least 6 consecutive leading digits, or at least 4 leading digits extending to the end of the input; otherwise, use Start A (`103`) if the first character is an ASCII control character, or Start B (`104`) for other characters.
3. **Encode the text:** traverse the input and count consecutive digits. Switch to Code C (`99`) for runs of at least six digits, or at least four digits at the end; encode pairs of digits as values from `00` to `99`. Switch between Code A (`101`) and Code B (`100`) as needed for other characters.
4. **Calculate the checksum:** add the Start symbol value to the weighted sum of subsequent symbol values, then take the remainder modulo 103.
5. **Append checksum and Stop:** add the checksum symbol and the Stop symbol (`106`). Recalculate the weighted sum to check that the stored checksum matches the encoded symbol sequence.
6. **Build bar/space widths:** look up each symbol in `BAR_LOOK_TBL` (values `0`–`106`) and combine the patterns into one sequence.
7. **Draw the bitmap:** render black bars on a white image, leaving blank quiet zones at both ends; save as PNG.

The Code 128 checksum is:

```text
checksum = (start_value + sum(position * symbol_value)) % 103
```

Positions start at **1** for the first symbol following the Start symbol. The checksum and Stop symbols are excluded from this sum.

## Image settings

The script currently uses these rendering values inside `create_code128()`:

| Parameter | Value | Meaning |
| --- | --- | --- |
| `moduleWidth` | `3` pixels | Width of one module in the output image |
| `barHeight` | `100` pixels | Image/bar height |
| `quietZone` | `10` modules | White margin on **each** side of the barcode |

`moduleWidth` and `barHeight` are illustrative implementation choices. A quiet zone of at least 10 modules on each side follows the Code 128 specification. Image dimensions and print quality may need further adjustment for use with physical scanners.

## Limitations

- Accepts **non-empty ASCII text only**; Unicode characters beyond ASCII are rejected.
- Uses a heuristic, **not** a globally optimal symbol-selection algorithm. For example, it does not begin directly with Start C even when the input starts with a long numeric run.
- Supports the basic Code A/B/C mappings used by the supplied pseudocode, not every Code 128 feature or optimization.
- Generates **bars only**; it does not print human-readable text under the barcode.
- The checksum verification checks consistency with the encoded symbols, not whether encoding preserved the intended input in every case.
- Barcode scannability is not guaranteed without testing at the intended print size and resolution.

## Project files

```text
Code128Encoder/
├── code128_encoder.py   # Encoder and bitmap generation
├── README.md            # Project documentation
└── barcode.png          # Created when the script runs
```

## Reference

**ISO/IEC 15417:2007** — Information technology — Automatic identification and data capture techniques — Code 128 bar code symbology specification.
