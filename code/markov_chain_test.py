import json
import pathlib
import numpy as np
import progressbar as pb
from argparse import ArgumentParser
from collections import namedtuple

_next = namedtuple('_next', 'values probalities')

def compile_model(model):
    for key in model.keys():
        freq = [i for i in model[key].items()]
        values = [i[0] for i in freq]
        probalities = np.array([i[1] for i in freq], dtype = 'int')
        probalities = probalities / np.sum(probalities)
        model[key] = _next(values, probalities)
    return model

def generate_line(model, order):

    line = [''] * order
    idx = 0

    while(True):
        curr = '_'.join(line[idx:idx+order])
        if curr not in model:
            break
        possible = model[curr]        
        value = np.random.choice(possible.values, p = possible.probalities)
        if value == '':
            break
        line.append(value)
        idx = idx + 1

    return ' '.join(line[2:])
		
def generate_text(model_in, file_out, count):
    model_in = pathlib.Path(model_in)
    file_out = pathlib.Path(file_out)

    print('Loading model...')
    with open(model_in, 'r', encoding = 'utf-8') as model_in:
        model = json.load(model_in)

    print('Compiling model...')
    order = model[0]
    model =  compile_model(model[1])

    print('Generating text...')
    with open(file_out, 'w', encoding = 'utf-8') as file_out:
        for i in range(count):
            line = generate_line(model, order)
            file_out.writelines([line, '\n'])

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-in', '--model-in', help = 'File containing thwe Markov Chain model', required = True)
    parser.add_argument('-out', '--file-out', help = 'File to use to save the generated text', required = True)
    parser.add_argument('-cnt', '--count', help = 'How many lines to generate', required = True)
    args = parser.parse_args()
    print('model in: ' + args.model_in)
    print('file out: ' + args.file_out)
    print('count: ' + args.count)
    generate_text(args.model_in, args.file_out, args.count)
