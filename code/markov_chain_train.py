import json
import pathlib
import progressbar as pb
from argparse import ArgumentParser

def learn_line(model, line, order):
    line = [''] * order + line.strip().split() + ['']
    for i in range(len(line) - order):
        condition = '_'.join(line[i : i + order])
        value =  line[i + order]            
        freq = model.get(condition, {})
        freq[value] = freq.get(value, 0) + 1
        model[condition] = freq

def process_all_files(folder_in, model_out, order):
    folder_in = pathlib.Path(folder_in)
    model_out = pathlib.Path(model_out)

    i = 0
    model = {}

    all_file_names = [p for p in folder_in.iterdir() if p.is_file() and p.suffix == '.txt']
    widgets = [ 'Processing Files: ', pb.Percentage(), ' ', pb.Bar(marker = '.', left = '[', right = ']'), ' ', pb.ETA() ]
    with pb.ProgressBar(widgets = widgets, max_value = len(all_file_names)) as bar:
        for file_name in all_file_names:
            bar.update(i)
            i = i + 1
            with open(file_name, 'r', encoding = 'utf-8') as file_in:
                for line in file_in:
                    learn_line(model, line, order)

    print('Saving model')
    with open(model_out, 'w', encoding = 'utf-8') as model_out:
        json.dump([order, model], model_out)
    
if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-in', '--folder-in', help = 'Folder to import files from', required = True)
    parser.add_argument('-out', '--model-out', help = 'File to use to save the model', required = True)
    parser.add_argument('-o', '--order', help = 'The order of the Markov Chain', required = True)
    args = parser.parse_args()
    print('folder in: ' + args.folder_in)
    print('model out: ' + args.model_out)
    print('order: ' + args.order)
    process_all_files(args.folder_in, args.model_out, int(args.order))
