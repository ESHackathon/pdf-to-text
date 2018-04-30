#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import re
import os
import json

REGEX_1 = r"[A-Z][a-zA-Z\-\:]{2,} [A-Z\-\:]{1,2}, [A-Z][a-zA-Z\-\:]{2,} [A-Z\-\:]{1,2},"
REGEX_2 = r"[A-Z][a-zA-Z\-\:]{2,}, [A-Z\-\:]{1,2}\., [A-Z][a-zA-Z\-\:]{2,}, [A-Z\-\:]{1,2}\.,"
REGEX_3 = r"[A-Z][a-zA-Z\-\:]{2,}, [A-Z\-\:]{1,2}\.,"
REFERENCES = r"R[eE][fF][eE][rR][eE][nN][Cc][eE][sS]"
SPACING = 35

LINES_SPLIT_REGEXS = [
    (
        r'(\b\[?[0-9]{1,3}\]?\.?\b) ([A-Z][a-zA-Z\-\:]{2,} [A-Z\-\:]{1,2},)',
        r"\n\1\2"
    ),
    (
        r'([0-9]{4};[^\.]*\.)',
        r"\1\n"
    ),
    (
        r'([1,2][0-9]{3}[^\.]*[^ ]*\.) (\[?[0-9]{1,3}\]?\.?\b)',
        r"\1\n\2"
    ),
    (
        r'([1,2][0-9]{3}[^\.]*\.)',
        r"\1\n"
    )
]

def possible_references(line, regexp, index):
    if re.search(REFERENCES, line):
        return index
    for _ in re.finditer(regexp, line):
        return index


def find_start_end(references_lines_index):
    if len(references_lines_index) == 0:
        return []
    groups = [[references_lines_index[0]]]
    for index in references_lines_index[1:]:
        if index - groups[-1][-1] < SPACING:
            groups[-1].append(index)
        else:
            groups.append([index,])
    max_group = []
    for group in reversed(groups):
        if len(group) > len(max_group):
            max_group = group
    if len(max_group) > 1:
        return [max_group[0], max_group[-1]]
    return [max_group[0], -1]

def separate_lines(file_lines, start_end):
    if len(start_end) > 1:
        return file_lines[0:start_end[0]] + file_lines[start_end[1]:], file_lines[start_end[0] - 1:start_end[1] + 1]
    if len(start_end) == 1:
        return file_lines[0:start_end[0]], file_lines[start_end[0] - 1:]
    else:
        return file_lines, []

def split_line_references(lines):
    new_lines = []
    for line in lines:
        found_match = False
        for regex, replacement in LINES_SPLIT_REGEXS:
            matched = re.search(regex, line)
            if matched and len(matched.groups()) > 0:
                lines_splitted = [
                    line for line in re.sub(regex, replacement, line).split("\n")
                    if line
                ]
                if len(lines_splitted) > 1 and len(lines_splitted[0]) / len(lines_splitted[1]) > 5:
                    continue
                new_lines += lines_splitted
                found_match = True
                break
        if not found_match:
            new_lines.append(line)
    return "\n".join([line.strip() for line in new_lines if len(line) < 800])

def main():
    file_path = sys.argv[1]
    base_dir = os.path.dirname(file_path)
    base_name =  os.path.splitext(os.path.basename(file_path))[0]
    file_lines = open(file_path).readlines()
    start_end = None
    references_lines_index = []
    for index, line in enumerate(file_lines):
        for regexp in [REGEX_1, REGEX_2, REGEX_3]:
            match = possible_references(line, regexp, index)
            if match:
                references_lines_index.append(match)
                break
    # print(references_lines_index)
    start_end = find_start_end(references_lines_index)
    # print(start_end)
    lines_no_references, references_lines = separate_lines(file_lines, start_end)

    with open(os.path.join(base_dir, base_name+'.references.txt'), 'w') as file_:
        references_raw = json.dumps({
            "references": split_line_references(references_lines),
            "no_references": "\n".join(file_lines).strip(),
        })
        file_.write(references_raw)
    print("____filename___:"+os.path.join(base_dir, base_name)+'.references.txt')

    # with open(os.path.join(base_dir, base_name+'.references.txt'), 'w') as file_:
    #     file_.write("\n".join(references_lines))
    # with open(os.path.join(base_dir, base_name+'.no_references.txt'), 'w') as file_:
    #     file_.write("\n".join(lines_no_references))

if __name__ == '__main__':
    main()
