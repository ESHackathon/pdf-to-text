import sys
import re
import os
import json

REGEX_1 = r"[A-Z][a-zA-Z\-\:]{2,} [A-Z\-\:]{1,2}, [A-Z][a-zA-Z\-\:]{2,} [A-Z\-\:]{1,2},"
REGEX_2 = r"[A-Z][a-zA-Z\-\:]{2,}, [A-Z\-\:]{1,2}\., [A-Z][a-zA-Z\-\:]{2,}, [A-Z\-\:]{1,2}\.,"
REFERENCES = r"R[eE][fF][eE][rR][eE][nN][Cc][eE]"
SPACING = 25

LINES_SPLIT_REGEXS = [
    r'([0-9]{4};[^\.]*\.)',
    r'([1,2][0-9]{3}[^\.]*[^ ]*\. \[?[0-9]{1,3}\]?\.?)',
    r'([1,2][0-9]{3}[^\.]*\.)'
]

def find_references(file_lines, regexp):
    pdf_lines = []
    index = 0
    lines_numbers = []
    et_al_lines = []
    lines_length = []
    for line in file_lines:
        index += 1
        found = 0
        matches = []
        if re.search(REFERENCES, line):
            lines_numbers.append(index)
        for match_el in re.finditer(regexp, line):
            lines_numbers.append(index)
            lines_length.append(len(line))
    if len(lines_numbers) > 0:
        return lines_numbers
    # import ipdb; import pprint; ipdb.set_trace(context=10); pass
    # elif len(lines_numbers) == 1 and lines_length[0] > 200:
    #     return lines_numbers
    # else:
    #     return None

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
        return file_lines[0:start_end[0]] + file_lines[start_end[1]:], file_lines[start_end[0] - 1:start_end[1]]
    if len(start_end) == 1:
        return file_lines[0:start_end[0]], file_lines[start_end[0] - 1:]
    else:
        return file_lines, []

def split_line_references(lines):
    new_lines = []
    for line in lines:
        found_match = False
        for regex in LINES_SPLIT_REGEXS:
            matched = re.search(regex, line)
            if matched and len(matched.groups()) > 0:
                lines_splitted = re.sub(regex, "\1\n", line).split("\n")
                if len(lines_splitted[0]) / len(lines_splitted[1]) > 5:
                    continue
                new_lines += lines_splitted
                found_match = True
                break
        if not found_match:
            new_lines.append(line)
    return "\n".join([line.strip() for line in new_lines])



def main():
    file_path = sys.argv[1]
    base_dir = os.path.dirname(file_path)
    base_name =  os.path.splitext(os.path.basename(file_path))[0]
    file_lines = open(file_path).readlines()
    start_end = None
    matches = find_references(file_lines, REGEX_1)
    references_lines_index = []
    if matches:
        references_lines_index = matches
    else:
        matches = find_references(file_lines, REGEX_2)
        if matches:
            references_lines_index = matches
    start_end = find_start_end(references_lines_index)
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
