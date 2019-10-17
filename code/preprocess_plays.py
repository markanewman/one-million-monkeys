import pathlib
import progressbar as pb
import string
from argparse import ArgumentParser
from bs4 import BeautifulSoup
from shutil import rmtree

def parse_play_quote(quote):
    lines = [anchor.text for anchor in quote.select('a[NAME]')]
    line = ' '.join(lines)
    return line

def parse_play_html(lines):
    content = ''.join(lines)
    soup = BeautifulSoup(content, features = 'lxml')
    lines = [parse_play_quote(quote) for quote in soup.select('blockquote')]
    lines = [line for line in lines if len(line) > 0]
    return lines

def strip_stage_direction(line):
    line = line.strip()
    if line.startswith('['):
        i = line.index(']')
        line = line[(i+1):].strip()
    return line

def expand_punctuation(line):
    tokens = line.split()
    tokens = [_expand_punctuation(token) for token in tokens]
    tokens = [' '.join(token) for token in tokens]
    return ' '.join(tokens)

def _expand_punctuation(token):
    l = len(token)
    if l < 2:
        return [token]
    elif token[l - 1] in string.punctuation:
        return [token[:l - 1], token[l - 1]]
    else:
        return [token]

def prepare_folder_out(folder_out):
    folder_out = pathlib.Path(folder_out)

    if folder_out.exists():
        for p in folder_out.iterdir():
            if p.is_file():
                p.unlink()
            elif p.is_dir():
                rmtree(folder_out)
    else:
        folder_out.mkdir()

def process_all_files(folder_in, folder_out):

    folder_in = pathlib.Path(folder_in)
    folder_out = pathlib.Path(folder_out)
    prepare_folder_out(folder_out)

    i = 0
    all_file_names = [p for p in folder_in.iterdir() if p.is_file() and p.suffix == '.html']
    widgets = [ 'Processing Files: ', pb.Percentage(), ' ', pb.Bar(marker = '.', left = '[', right = ']'), ' ', pb.ETA() ]
    with pb.ProgressBar(widgets = widgets, max_value = len(all_file_names)) as bar:
        for file_name in all_file_names:
            bar.update(i)
            i = i + 1

            file_in = file_name
            with open(file_in, 'r', encoding = 'utf-8') as file_in:
                lines = file_in.readlines()

            lines = parse_play_html(lines)
            lines = [strip_stage_direction(line) for line in lines]
            lines = [expand_punctuation(line) for line in lines]

            file_out = folder_out.joinpath(file_name.stem + '.txt')
            with file_out.open('w', encoding = 'utf-8') as file_out:
                file_out.writelines(['{}\n'.format(line) for line in lines])

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-in', '--folder-in', help = 'Folder to import files from', required = True)
    parser.add_argument('-out', '--folder-out', help = 'Folder to save results', required = True)
    args = parser.parse_args()
    print('folder in: ' + args.folder_in)
    print('folder out: ' + args.folder_out)
    process_all_files(args.folder_in, args.folder_out)
