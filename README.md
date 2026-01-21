GTO Wizard Range Importer

Overview
This repository contains a Python script that parses preflop hand range data exported from GTO Wizard HTML and converts it into action-specific range files compatible with GTO+.

The script extracts raise, call, and fold frequencies for each hand and outputs them in GTO+ range format.

Features
- Parses GTO Wizard HTML with mixed gradient- and legend-based encoding
- Extracts raise, call, and fold percentages per hand
- Handles incomplete or missing legend data
- Outputs sorted, GTO+-compatible range files
- Deterministic hand ordering for consistent imports

Requirements
- Python 3.8 or newer
- No external dependencies (standard library only)

Input
- gtowiz.txt
  A UTF-8 encoded file containing the relevant GTO Wizard HTML source.

Output
The script generates three files:
- raise_range.txt
- call_range.txt
- fold_range.txt

Each file contains hands formatted as:
[percentage]HAND[/percentage]

and ordered in standard poker rank order.

Usage
1. Place the GTO Wizard HTML into a file named gtowiz.txt in the project directory.
2. Run the script:
   python importer.py
3. Import the generated range files into GTO+.

Notes
- Percentages are rounded to one decimal place.
- Fold percentage is calculated as the remainder when not explicitly provided.
- RGB values used for action detection match GTO Wizard’s default color scheme.

License
MIT License
