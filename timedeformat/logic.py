from datetime import datetime
import re
from copy import deepcopy

DIRECTIVE_TYPES = [
    ["%a", "%A", "%w"],
    ["%d"],
    ["%b", "%B", "%m", "%-m"],
    ["%y", "%Y"],
    ["%H", "%-H", "%I", "%-I"],
    ["%p"],
    ["%M", "%-M"],
    ["%S", "%-S"],
    ["%f"],
    ["%z", "%Z"],
    ["%j", "%-j"],
    ["%U"],
    ["%W"],
    # ["%c"],
    # ["%x"],
    # ["%X"],
]


def find_matching_directive(directives, dt, desired_output):
    for directive in directives:
        if dt.strftime(directive) == desired_output:
            return directive


def build_time_format(input_dt: datetime, desired_output: str):
    # we're going to remove directives when they've successfully matched a segment of
    # the output. (The assumption here is that a single directive isn't repeated.)
    # That's why we deepcopy - we want to delete indices but also keep the original
    possible_directive_groups = deepcopy(DIRECTIVE_TYPES)
    pattern = ""
    while desired_output:
        # identify a segment of the output (digits next to eachother, months, AM/PM)
        segment = re.match("(\d+)|([A-Z][a-z]+)|(A|PM)", desired_output)
        if not segment:
            # if no segment found, added the text directly to the pattern
            extracted_len = 1
            append_to_pattern = desired_output[0]
        else:
            # if a segment is found, search for a directive that will output that
            # the same text as the segment
            segment_text = segment[0]
            extracted_len = len(segment_text)
            for i, directives in enumerate(possible_directive_groups):
                matched_directive = find_matching_directive(
                    directives, input_dt, segment_text
                )
                if matched_directive:
                    # if a valid directive is found, delete all directives of the same
                    # type (at the same index) from possible directives. So an hour
                    # can't be present twice, in different formats, in a single pattern.
                    append_to_pattern = matched_directive
                    del possible_directive_groups[i]
                    break
            else:
                # if no derivative gives the desired output, assume the text is just
                # part of how the user wants the text to be formatted
                append_to_pattern = segment_text
        # desired output is shortened to what is left
        desired_output = desired_output[extracted_len:]
        pattern += append_to_pattern
    return pattern


if __name__ == "__main__":
    print(
        build_time_format(
            input_dt=datetime(2021, 1, 10, 14, 23, 40, 273316),
            desired_output="Jan, 10, 2PM",
        )
    )
