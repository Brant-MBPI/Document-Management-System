import re


def normalize(lot_no: str) -> str:
    if not lot_no:
        return ""

    # Remove "LOT #" prefixes everywhere
    lot_no = re.sub(r"LOT\s*#\s*", "", lot_no)

    # Clean line breaks and extra spaces
    lot_no = lot_no.replace("\n", " ").strip()

    # Split on separators ; , or multiple spaces
    parts = re.split(r"[;,]\s*|\s{2,}", lot_no)

    normalized_parts = []
    for part in parts:
        part = part.strip()
        if not part:
            continue

        # Expand inline comma short form (e.g. 95-7737Q,7738Q,7739Q → 95-7737Q, 95-7738Q, 95-7739Q)
        if "," in part and re.match(r"^[0-9]{2}-\d+[A-Z]", part):
            prefix_match = re.match(r"^(\d{2}-)(\d+)([A-Z]+)", part)
            if prefix_match:
                prefix = prefix_match.group(1)
                suffix = prefix_match.group(3)

                # Split all numbers and letters after first full code
                codes = part.split(",")
                expanded = []
                for i, code in enumerate(codes):
                    code = code.strip()
                    if i == 0:
                        expanded.append(code)  # full first code
                    else:
                        expanded.append(prefix + code)  # prefix + rest
                normalized_parts.extend(expanded)
                continue

        # Expand inline comma short form with MB prefix (e.g. MB-08-4608H,4609H)
        if "," in part and part.startswith("MB-"):
            prefix_match = re.match(r"(MB-\d{2}-)(\d+)([A-Z]*)", part)
            if prefix_match:
                prefix = prefix_match.group(1)
                suffix = prefix_match.group(3)

                codes = part.split(",")
                expanded = []
                for i, code in enumerate(codes):
                    code = code.strip()
                    if i == 0:
                        expanded.append(code)  # first one is full
                    else:
                        expanded.append(prefix + code)  # prefix + number
                normalized_parts.extend(expanded)
                continue

        # Expand ranges (works for both MB and numeric lots)
        range_match = re.match(r"(.+?)(\d+[A-Z]*?)-(\d+[A-Z]*)$", part)
        if range_match:
            base_prefix = range_match.group(1)
            start = range_match.group(2)
            end = range_match.group(3)
            normalized_parts.append(f"{base_prefix}{start} to {base_prefix}{end}")
            continue

        # Otherwise, keep as-is
        normalized_parts.append(part)

    # Join with comma + space
    return ", ".join(normalized_parts)
