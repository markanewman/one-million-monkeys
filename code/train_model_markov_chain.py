import pathlib
import progressbar as pb
from argparse import ArgumentParser


def learn_line(model, line, order)


def process_all_files(data_root):

    data_root = pathlib.Path(data_root)
    folder_in = data_root.joinpath('./raw')
    folder_out = data_root.joinpath('./parsed')
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
    data_root = pathlib.Path(__file__).parent
    process_all_files(data_root)