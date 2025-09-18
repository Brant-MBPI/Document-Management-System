import re

def normalize(lot_no: str) -> str:
    if not lot_no:
        return ""

    # 1. Initial cleanup: Remove "LOT #" prefixes.
    cleaned_input = re.sub(r"LOT\s*#\s*", "", lot_no)
    # Split by newlines or semicolons to get primary chunks
    primary_chunks = re.split(r"[\n;]", cleaned_input)

    all_expanded_parts = []

    for chunk in primary_chunks:
        chunk = chunk.strip()
        if not chunk:
            continue

        # Now, within each chunk, handle further splitting by commas or multiple spaces
        # Split by comma OR by two or more spaces, BUT ensure the space splitting
        # doesn't happen *within* a lot number (e.g. "MB-09-7995H")
        sub_parts = re.split(r",|\s{2,}(?=[A-Z0-9])", chunk)

        last_known_prefix = ""

        for part_index, part in enumerate(sub_parts):
            part = part.strip()
            if not part:
                continue

            # --- PRE-PROCESS TO ESTABLISH / UPDATE last_known_prefix ---
            # Attempt to extract a prefix if the current part is a full lot number (e.g., "MB-09-7995H")
            # This regex captures "MB-XX-" or "XX-"
            current_part_prefix_match = re.match(r"^(MB-\d{2}-|\d{2}-)", part)
            if current_part_prefix_match:
                last_known_prefix = current_part_prefix_match.group(1)
            # If it's just a number-letter suffix and we have a previous prefix, keep it.
            elif re.match(r"^\d+[A-Z]*$", part) and last_known_prefix:
                # Do nothing, last_known_prefix is already set
                pass
            # If it's a new, unrelated part (not a suffix, not a known prefix pattern), clear the prefix
            elif not re.match(r"^\d+[A-Z]*$", part):
                last_known_prefix = ""

            # --- APPLY TRANSFORMATION RULES ---

            # 1. Handle ranges first (e.g., MB-25-6351AM-6358AM)
            # This regex is made more specific to ensure a hyphen is truly present and
            # it captures the prefix and then the two range numbers/letters.
            # Example: (MB-25-)(6351AM)-(6358AM)
            range_match = re.match(r"^(MB-\d{2}-|\d{2}-)(\d+[A-Z]*)-(\d+[A-Z]*)$", part)

            if range_match:
                prefix = range_match.group(1)
                start_val = range_match.group(2)
                end_val = range_match.group(3)
                all_expanded_parts.append(f"{prefix}{start_val} to {prefix}{end_val}")
                # Update last_known_prefix from this range if it explicitly has one
                last_known_prefix = prefix
                continue # Skip to next part

            # 2. Handle inline comma short forms (e.g., 3681H where prefix is "MB-08-")
            # This applies if the part is just a number-letter suffix AND we have a valid last_known_prefix
            if re.match(r"^\d+[A-Z]*$", part) and last_known_prefix:
                all_expanded_parts.append(last_known_prefix + part)
                continue # Skip to next part

            # 3. If none of the above special cases, add the part as is.
            all_expanded_parts.append(part)
            # If the current part did not establish a clear prefix for the *next* iteration, clear it.
            # This prevents prefix from carrying over to completely unrelated items.
            # The 'if current_part_prefix_match' check earlier correctly sets it if it's a full lot.
            # If it was a suffix (matched by re.match(r"^\d+[A-Z]*$", part)), then last_known_prefix
            # would remain from the prior item.
            # We want to clear prefix if the current part doesn't define it AND wasn't a short-form.
            if not current_part_prefix_match and not re.match(r"^\d+[A-Z]*$", part):
                 last_known_prefix = "" # Clear if it's an unrecognized format
            # Special case: if it was a full lot number (e.g. 95-4569R), ensure its prefix is stored
            elif re.match(r"^(\d{2}-)(\d+[A-Z]*)$", part) and not current_part_prefix_match:
                 last_known_prefix = re.match(r"^(\d{2}-)", part).group(1)

    return ", ".join(all_expanded_parts)