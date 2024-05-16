"""Python 3.11.1"""

import sys
import os
import argparse
import csv
import datetime
# import xml.etree.ElementTree as ET

__VERSION_NUMBER__ = ('0', '1', '0')
__PROGRAM_NAME__ = 'DicConverter'
__USAGE__ = 'Generate markdown from data file.'
parser = argparse.ArgumentParser(prog=__PROGRAM_NAME__, usage=__USAGE__)
parser.add_argument("INPUT_FILE", help="input file")
parser.add_argument('-v',
                    '--version',
                    action='version',
                    version='%(prog)s ver.' + '.'.join(__VERSION_NUMBER__))
parser.add_argument('--verbose', action='store_true', help='Display operation log')
parser.add_argument('--csv', action='store_true', help='Input file in csv format')
parser.add_argument('--yaml', action='store_true', help='Input file in yaml format')
parser.add_argument('--remove', action='store_true', help='Remove files from input file')
parser.add_argument('-t', '--target_dir', default='./../', help='Set output folder')


class DicConverter:
    "Generate markdown files from files."
    _verbose = False
    _target_dir = ''
    _remove = False
    _input_file = ''

    def __init__(self, arguments: argparse.Namespace):
        print(__PROGRAM_NAME__ + ' ver.' + '.'.join(__VERSION_NUMBER__))
        self._input_file = os.path.abspath(arguments.INPUT_FILE.strip())
        print("  file_name: " + self._input_file)
        self._target_dir = os.path.abspath(arguments.target_dir.strip())
        print("  target_dir: " + self._target_dir)
        if arguments.verbose is True:
            print("  log: verbose")
            self._verbose = True
        if arguments.remove is True:
            print("  mode: remove")
            self._remove = True
        if arguments.csv is True:
            print("  file_type: csv")
            self.read_tsv(self._input_file, self._target_dir, self._remove, ',')
        elif arguments.yaml is True:
            print("  file_type: yaml")
            self.read_yml(self._input_file, self._target_dir, self._remove)
        else:
            print("  file_type: tsv")
            self.read_tsv(self._input_file, self._target_dir, self._remove, '\t')
        self.make_chapter(self._target_dir)

    def make_chapter(self, target_dir: str):
        "make chapter"
        for file in self.find_all_files(target_dir):
            if file.endswith('_chapter.md'):
                dirname = os.path.dirname(file)
                sp_dir = file.split(os.sep)
                current_dir = sp_dir[len(sp_dir) - 2]

                with open(file, mode='w', newline='', encoding='utf-8') as f:
                    f.write('## ' + current_dir + '\n\n')
                    for data in self.find_all_files_name(dirname):
                        if data.endswith('_chapter.md') is False:
                            if data.endswith('.md') is True:
                                f.write('@import "' + data + '"\n')

    def find_all_files(self, directory: str):
        "find all files"
        for root, _dirs, files in os.walk(directory):
            for file in files:
                yield os.path.join(root, file)

    def find_all_files_name(self, directory: str):
        "find all files"
        for _root, _dirs, files in os.walk(directory):
            for file in files:
                yield file

    def remove(self, target_dir: str, data: list):
        "remove file"
        if data[0] != '':
            if data[1] != "":
                if data[2] != "":
                    path = os.path.normpath(
                        os.path.join(target_dir,
                                     data[1],
                                     data[2],
                                     data[0] + '.md'))
                    if os.path.exists(path) is True:
                        os.remove(path)
                        if self._verbose is True:
                            print(path)

    def save(self, target_dir: str, data: list, text: str):
        "save file"
        if data[0] != '':
            if data[1] != "":
                if data[2] != "":
                    t_dir = os.path.normpath(
                        os.path.join(target_dir,
                                     data[1],
                                     data[2]))
                    os.makedirs(t_dir, exist_ok=True)
                    path = os.path.normpath(
                        os.path.join(t_dir, data[0] + '.md'))
                    with open(path, mode='w', newline='', encoding='utf-8') as f:
                        f.write(text)
                    if self._verbose is True:
                        print(path)

    def read_yml(self, filename: str, target_dir: str, remove: bool):
        "Read yml file"
        print("[ERROR] Not implemented yet.")

    def read_tsv(self, filename: str, target_dir: str, remove: bool, delimiter_txt: str = '\t'):
        "Read tsv file"
        d_today = datetime.date.today()
        with open(filename, mode='r', newline='', encoding='utf-8') as f:
            tsv_reader = csv.reader(f, delimiter=delimiter_txt)
            for row in tsv_reader:
                if len(row) > 1:
                    if row[0] == '[名前]':
                        continue
                    if remove is True:
                        self.remove(target_dir, row)
                    else:
                        text = self.make_page(row, d_today)
                        self.save(target_dir, row, text)

    def make_page(self, data: list, d_today: datetime.date):
        "make page from data"
        text = ''
        length = len(data)
        if data[0] != '':
            text += '<article id="' + data[0] + '">\n\n### ' + data[0] + '\n\n'
            text += '<p class="st_update_header">' + str(d_today) + '</p>\n'

            if length > 4:
                if data[4] != "":
                    text += '<p class="st_name_header_en">' + data[4] + '</p>\n'
            if length > 5:
                if data[5] != "" and data[5] != '-':
                    add_ruby = False
                    if length > 6:
                        if data[6] != "" and data[6] != '-' and data[6] != data[5]:
                            add_ruby = True
                    if add_ruby is True:
                        text += '<p class="st_name_header_jp">'
                        text += data[5] + '(' + data[6] + ')</p>\n'
                    else:
                        text += '<p class="st_name_header_jp">'
                        text += data[5] + '</p>\n'
            if length > 3:
                if data[3] != "" and data[3] != '-':
                    text += '<p class="st_name_header_abbreviation">'
                    text += data[3] + '</p>\n'
            if length > 8:
                if data[8] != "" and data[8] != '-':
                    text += '<div class="article_explanation">'
                    text += data[8] + '</div>\n'
            if length > 7:
                if data[7] != "" and data[7] != '-':
                    text += '<p class="st_name_header_synonyms">'
                    text += data[7] + '</p>\n'
            text += "</article>\n"
        return text


if __name__ == '__main__':
    args = parser.parse_args(sys.argv[1:])
    DicConverter(args)
