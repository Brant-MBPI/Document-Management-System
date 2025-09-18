import re

def normalize(lot_no: str) -> str:
    if not lot_no:
        return ""

    # 1. Initial cleanup: Remove "LOT #" prefixes.
    cleaned_input = re.sub(r"LOT\s*#\s*", "", lot_no)
    # Split by newlines or semicolons to get primary chunks
    primary_chunks = re.split(r"[\n;]", cleaned_input)

    all_expanded_parts = []
    # Persistent prefix across all chunks
    last_known_prefix_overall = ""

    for chunk in primary_chunks:
        chunk = chunk.strip()
        if not chunk:
            continue

        # Now, within each chunk, handle further splitting by commas or multiple spaces
        # Split by comma OR by two or more spaces, BUT ensure the space splitting
        # doesn't happen *within* a lot number (e.g. "MB-09-7995H")
        sub_parts = re.split(r",|\s{2,}(?=[A-Z0-9])", chunk)

        # Initialize last_known_prefix for this chunk, potentially from the overall persistent prefix
        last_known_prefix_for_this_chunk = last_known_prefix_overall

        for part_index, part in enumerate(sub_parts):
            part = part.strip()
            if not part:
                continue

            # --- NEW CONDITION: Handle already fully qualified ranges (e.g., MB-09-1270I - 1273I) ---
            # This regex looks for a full lot number, followed by ' - ', followed by another number-letter suffix.
            # Example: (MB-09-1270I) - (1273I)
            fully_qualified_range_match = re.match(r"^(MB-\d{2}-|\d{2}-)(\d+[A-Z]*)\s*-\s*(\d+[A-Z]*)$", part)
            if fully_qualified_range_match:
                prefix = fully_qualified_range_match.group(1)
                start_suffix = fully_qualified_range_match.group(2)
                end_suffix = fully_qualified_range_match.group(3)
                all_expanded_parts.append(f"{prefix}{start_suffix} to {prefix}{end_suffix}")
                last_known_prefix_for_this_chunk = prefix # Update prefix for this chunk
                last_known_prefix_overall = prefix # Update overall persistent prefix
                continue # Skip to next part


            # --- PRE-PROCESS TO ESTABLISH / UPDATE last_known_prefix_for_this_chunk ---
            # Attempt to extract a prefix if the current part is a full lot number (e.g., "MB-09-7995H")
            # This regex captures "MB-XX-" or "XX-"
            current_part_prefix_match = re.match(r"^(MB-\d{2}-|\d{2}-)", part)
            if current_part_prefix_match:
                last_known_prefix_for_this_chunk = current_part_prefix_match.group(1)
                last_known_prefix_overall = current_part_prefix_match.group(1) # Update overall
            # If it's just a number-letter suffix and we have a previous prefix, keep it.
            # This `elif` block ensures that if `part` is a suffix, `last_known_prefix_for_this_chunk`
            # is *not* cleared and remains whatever it was from a previous part or `last_known_prefix_overall`.
            elif re.match(r"^\d+[A-Z]*$", part):
                # Do nothing, last_known_prefix_for_this_chunk is already set (from prior part or overall)
                # Ensure last_known_prefix_overall is also consistent if it was just a suffix extending a known prefix
                pass
            # If it's a new, unrelated part (not a suffix, not a known prefix pattern), clear the chunk-level prefix
            # AND the overall prefix. This handles cases where a completely new, unprefixed item appears.
            else:
                last_known_prefix_for_this_chunk = ""
                last_known_prefix_overall = ""


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
                # Update last_known_prefix for this chunk and overall
                last_known_prefix_for_this_chunk = prefix
                last_known_prefix_overall = prefix
                continue # Skip to next part

            # 2. Handle inline comma short forms (e.g., 3681H where prefix is "MB-08-")
            # This applies if the part is just a number-letter suffix AND we have a valid last_known_prefix_for_this_chunk
            if re.match(r"^\d+[A-Z]*$", part) and last_known_prefix_for_this_chunk:
                all_expanded_parts.append(last_known_prefix_for_this_chunk + part)
                # Keep last_known_prefix_overall the same as last_known_prefix_for_this_chunk
                last_known_prefix_overall = last_known_prefix_for_this_chunk
                continue # Skip to next part

            # 3. If none of the above special cases, add the part as is.
            all_expanded_parts.append(part)
            # This block was for clearing prefix if it was an unrecognized format.
            # With the 'else' in the PRE-PROCESS section, this might be redundant or needs re-evaluation.
            # Let's simplify: the 'last_known_prefix_for_this_chunk' and 'last_known_prefix_overall' should be
            # correctly set or cleared by the PRE-PROCESS steps.
            # If a part is added 'as is' and it *didn't* set a prefix (current_part_prefix_match was None),
            # and it wasn't a suffix, then the 'else' block would have already cleared the prefixes.
            # So, we can remove the previous redundant clearing logic here.
            # We only need to ensure overall prefix is updated if a full lot number was added "as is"
            if re.match(r"^(MB-\d{2}-|\d{2}-)(\d+[A-Z]*)$", part) and not current_part_prefix_match:
                 # This case catches full lot numbers that weren't range-matched or fully qualified ranges.
                 # Example: just "MB-08-3680H" by itself.
                 matched_prefix = re.match(r"^(MB-\d{2}-|\d{2}-)", part).group(1)
                 last_known_prefix_for_this_chunk = matched_prefix
                 last_known_prefix_overall = matched_prefix


    return ", ".join(all_expanded_parts)