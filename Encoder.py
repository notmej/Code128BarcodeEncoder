"""Code 128 encoder based on the supplied pseudocode.
Install Pillow first: pip install pillow
"""
from PIL import Image, ImageDraw

# virt env: source .venv/bin/activate, deactivate to leave
# Maps Code 128 symbol values (0–106) to bar/space widths in modules.
BAR_LOOK_TBL = {
    0: [2, 1, 2, 2, 2, 2],
    1: [2, 2, 2, 1, 2, 2],
    2: [2, 2, 2, 2, 2, 1],
    3: [1, 2, 1, 2, 2, 3],
    4: [1, 2, 1, 3, 2, 2],
    5: [1, 3, 1, 2, 2, 2],
    6: [1, 2, 2, 2, 1, 3],
    7: [1, 2, 2, 3, 1, 2],
    8: [1, 3, 2, 2, 1, 2],
    9: [2, 2, 1, 2, 1, 3],
    10: [2, 2, 1, 3, 1, 2],
    11: [2, 3, 1, 2, 1, 2],
    12: [1, 1, 2, 2, 3, 2],
    13: [1, 2, 2, 1, 3, 2],
    14: [1, 2, 2, 2, 3, 1],
    15: [1, 1, 3, 2, 2, 2],
    16: [1, 2, 3, 1, 2, 2],
    17: [1, 2, 3, 2, 2, 1],
    18: [2, 2, 3, 2, 1, 1],
    19: [2, 2, 1, 1, 3, 2],
    20: [2, 2, 1, 2, 3, 1],
    21: [2, 1, 3, 2, 1, 2],
    22: [2, 2, 3, 1, 1, 2],
    23: [3, 1, 2, 1, 3, 1],
    24: [3, 1, 1, 2, 2, 2],
    25: [3, 2, 1, 1, 2, 2],
    26: [3, 2, 1, 2, 2, 1],
    27: [3, 1, 2, 2, 1, 2],
    28: [3, 2, 2, 1, 1, 2],
    29: [3, 2, 2, 2, 1, 1],
    30: [2, 1, 2, 1, 2, 3],
    31: [2, 1, 2, 3, 2, 1],
    32: [2, 3, 2, 1, 2, 1],
    33: [1, 1, 1, 3, 2, 3],
    34: [1, 3, 1, 1, 2, 3],
    35: [1, 3, 1, 3, 2, 1],
    36: [1, 1, 2, 3, 1, 3],
    37: [1, 3, 2, 1, 1, 3],
    38: [1, 3, 2, 3, 1, 1],
    39: [2, 1, 1, 3, 1, 3],
    40: [2, 3, 1, 1, 1, 3],
    41: [2, 3, 1, 3, 1, 1],
    42: [1, 1, 2, 1, 3, 3],
    43: [1, 1, 2, 3, 3, 1],
    44: [1, 3, 2, 1, 3, 1],
    45: [1, 1, 3, 1, 2, 3],
    46: [1, 1, 3, 3, 2, 1],
    47: [1, 3, 3, 1, 2, 1],
    48: [3, 1, 3, 1, 2, 1],
    49: [2, 1, 1, 3, 3, 1],
    50: [2, 3, 1, 1, 3, 1],
    51: [2, 1, 3, 1, 1, 3],
    52: [2, 1, 3, 3, 1, 1],
    53: [2, 1, 3, 1, 3, 1],
    54: [3, 1, 1, 1, 2, 3],
    55: [3, 1, 1, 3, 2, 1],
    56: [3, 3, 1, 1, 2, 1],
    57: [3, 1, 2, 1, 1, 3],
    58: [3, 1, 2, 3, 1, 1],
    59: [3, 3, 2, 1, 1, 1],
    60: [3, 1, 4, 1, 1, 1],
    61: [2, 2, 1, 4, 1, 1],
    62: [4, 3, 1, 1, 1, 1],
    63: [1, 1, 1, 2, 2, 4],
    64: [1, 1, 1, 4, 2, 2],
    65: [1, 2, 1, 1, 2, 4],
    66: [1, 2, 1, 4, 2, 1],
    67: [1, 4, 1, 1, 2, 2],
    68: [1, 4, 1, 2, 2, 1],
    69: [1, 1, 2, 2, 1, 4],
    70: [1, 1, 2, 4, 1, 2],
    71: [1, 2, 2, 1, 1, 4],
    72: [1, 2, 2, 4, 1, 1],
    73: [1, 4, 2, 1, 1, 2],
    74: [1, 4, 2, 2, 1, 1],
    75: [2, 4, 1, 2, 1, 1],
    76: [2, 2, 1, 1, 1, 4],
    77: [4, 1, 3, 1, 1, 1],
    78: [2, 4, 1, 1, 1, 2],
    79: [1, 3, 4, 1, 1, 1],
    80: [1, 1, 1, 2, 4, 2],
    81: [1, 2, 1, 1, 4, 2],
    82: [1, 2, 1, 2, 4, 1],
    83: [1, 1, 4, 2, 1, 2],
    84: [1, 2, 4, 1, 1, 2],
    85: [1, 2, 4, 2, 1, 1],
    86: [4, 1, 1, 2, 1, 2],
    87: [4, 2, 1, 1, 1, 2],
    88: [4, 2, 1, 2, 1, 1],
    89: [2, 1, 2, 1, 4, 1],
    90: [2, 1, 4, 1, 2, 1],
    91: [4, 1, 2, 1, 2, 1],
    92: [1, 1, 1, 1, 4, 3],
    93: [1, 1, 1, 3, 4, 1],
    94: [1, 3, 1, 1, 4, 1],
    95: [1, 1, 4, 1, 1, 3],
    96: [1, 1, 4, 3, 1, 1],
    97: [4, 1, 1, 1, 1, 3],
    98: [4, 1, 1, 3, 1, 1],
    99: [1, 1, 3, 1, 4, 1],
    100: [1, 1, 4, 1, 3, 1],
    101: [3, 1, 1, 1, 4, 1],
    102: [4, 1, 1, 1, 3, 1],
    103: [2, 1, 1, 4, 1, 2],
    104: [2, 1, 1, 2, 1, 4],
    105: [2, 1, 1, 2, 3, 2],
    106: [2, 3, 3, 1, 1, 1, 2],

}


def create_code128(text: str, filename: str = "barcode.png") -> Image.Image:
    # Input validation
    if len(text) == 0 or any(ord(c) > 127 for c in text):
        raise ValueError("Input must contain at least one ASCII character (0–127).")

    symbols = []
    barcode = []
    i = 0
    code = ""

    moduleWidth = 3
    barHeight = 100
    quietZone = 10

    # Select starting code set
    if ord(text[0]) < 32:
        symbols.append(103)  # Start A
        code = "A"
    else:
        symbols.append(104)  # Start B
        code = "B"

    # Encode input characters
    while i < len(text):
        digits = 0

        # Count consecutive digits
        while i + digits < len(text) and "0" <= text[i + digits] <= "9":
            digits += 1

        # Decide whether to use Code C
        if digits >= 6 or (digits >= 4 and i + digits == len(text)):
            # Handle an odd number of digits
            if digits % 2 == 1:
                if code == "C":
                    # Leave the final unpaired digit to the next iteration.
                    digits -= 1
                else:
                    # A and B both encode ASCII digits using ASCII - 32.
                    symbols.append(ord(text[i]) - 32)
                    i += 1
                    digits -= 1

            if code != "C":
                symbols.append(99)  # Switch to Code C
                code = "C"

            while digits >= 2:
                symbols.append(int(text[i:i + 2]))
                i += 2
                digits -= 2
        else:
            if code == "A":
                if 0 <= ord(text[i]) <= 31:
                    symbols.append(ord(text[i]) + 64)
                    i += 1
                elif ord(text[i]) <= 95:
                    symbols.append(ord(text[i]) - 32)
                    i += 1
                else:
                    symbols.append(100)  # Switch to B
                    code = "B"
                    symbols.append(ord(text[i]) - 32)
                    i += 1
            elif code == "B":
                if 32 <= ord(text[i]) <= 127:
                    symbols.append(ord(text[i]) - 32)
                    i += 1
                else:
                    symbols.append(101)  # Switch to A
                    code = "A"
                    symbols.append(ord(text[i]) + 64)
                    i += 1
            else:  # Currently in Code C
                if ord(text[i]) < 32:
                    symbols.append(101)  # Switch to A
                    code = "A"
                    symbols.append(ord(text[i]) + 64)
                    i += 1
                else:
                    symbols.append(100)  # Switch to B
                    code = "B"
                    symbols.append(ord(text[i]) - 32)
                    i += 1

    # Modulo 103 checksum
    wSum = symbols[0]
    for position in range(1, len(symbols)):
        wSum += symbols[position] * position

    chksum = wSum % 103
    symbols.append(chksum)
    symbols.append(106)  # Stop

    # Recalculate checksum to verify the stored value
    check = symbols[-2]
    verifySum = symbols[0]
    for position in range(1, len(symbols) - 2):
        verifySum += symbols[position] * position

    if check != verifySum % 103:
        raise ValueError("Checksum verification failed.")

    # Convert each symbol to its bar/space width pattern
    for value in symbols:
        barcode.extend(BAR_LOOK_TBL[value])

    # Render bitmap, including the quiet zones
    imgWidth = (sum(barcode) + 2 * quietZone) * moduleWidth
    bitmap = Image.new("RGB", (imgWidth, barHeight), "white")
    draw = ImageDraw.Draw(bitmap)
    x = quietZone * moduleWidth

    for i in range(len(barcode)):
        width = barcode[i] * moduleWidth
        if i % 2 == 0:
            draw.rectangle((x, 0, x + width - 1, barHeight - 1), fill="black")
        x += width

    bitmap.save(filename)
    print("Encoded symbols:", symbols)
    print("Checksum:", chksum)
    print("Saved barcode to:", filename)
    return bitmap


if __name__ == "__main__":
    text = input("Enter text to encode: ")
    try:
        create_code128(text)
    except ValueError as error:
        print("Error:", error)
