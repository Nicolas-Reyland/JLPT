# -*- coding: UTF-8 -*-
# Japanese-Language Proficiency Test N5
from jlptutils import *
from jlpt_n5_kanjis import build_kanjis
from jlpt_n5_vocab import build_vocab
from random import shuffle
import tkinter as tk
from tkinter.messagebox import showerror
from argparse import ArgumentParser
from fuzzywuzzy import fuzz

# https://clips.twitch.tv/TolerantHeartlessMetalTBCheesePull

title = 'お勉強'
parser = ArgumentParser(description='Learn Kanjis and Vocabulary for JLPT N5')
parser.add_argument('-m',
                    '--module',
                    metavar='module',
                    help='Name of module you want to train on. [kanjis, vocab]')
parser.add_argument('-c',
                    '--console',
                    action='store_true',
                    help='Use console mode')
parser.add_argument('-f',
                    '--from',
                    metavar='from_',
                    help='From {} to {}. (df: kanjis)')
parser.add_argument('-t',
                    '--to',
                    metavar='to',
                    help='From {} to {}. (df: meaning)')
parser.add_argument('-r',
                    '--review',
                    metavar='review',
                    help='Do the reviews of those that got failed (df: true)')
parser.add_argument('-l',
                    '--language',
                    metavar='language',
                    help='The language you want the meanings to be in (might also vary the Vocabulary and kanjis a bit). [(fr, francais, français), (en, english)] (df: en)')

args = vars(parser.parse_args())
get_arg = lambda arg, default: args[arg] if args[arg] else default

module = get_arg('module', 'vocab')
console = args['console']
from_ = get_arg('from', 'kanjis' if module == 'vocab' else 'kanji')
to = get_arg('to', 'meaning')
review = args['review'].lower() in ['1', 'true', 'yes', 'enable'] if args['review'] else True
language = args['language']
if language is not None:
    if language.lower() in ['en', 'english']:
        language = 0
    elif language.lower() in ['fr', 'francais', 'français']:
        language = 1
    else:
        raise NotImplementedError(f'Not supported language: "{language.lower()}"')
else:
    language = 0 # English

def learn_kanjis_gui(from_, to, review=True):
    global next_var
    kanjis = list(build_kanjis())[:10]
    shuffle(kanjis)

    d = {'kanji': 0, 'lecture-on': 1, 'kun-lecture': 2, 'meaning': 3}

    root = tk.Tk()
    root.title(title)
    root.protocol('WM_DELETE_WINDOW', lambda : restart(root))

    next_var = tk.BooleanVar()
    root.bind('<Return>', lambda *args: clear_text_history() and (next_var.set(True) if reponse.get() else '') )
    tk.Canvas(root, width=300, height=250).pack()

    question = tk.Label(root, font='Helvetica 50')
    question.place(x=0,y=0,relwidth=1,relheight=.8) # grid(row=0, column=0)
    reponse = tk.Entry(root)
    if to != 'meaning':
        entry_text_var = tk.StringVar()
        entry_text_var.trace_add('write', lambda *args: update_entry(d[to], reponse))
        reponse.configure(textvariable=entry_text_var, validatecommand=lambda : myIMEinput(d[to], reponse))
        root.bind('<BackSpace>', lambda *args: del_pressed(d[to], reponse))
        root.bind('<Key>', lambda entry: key_pressed(entry, d[to], reponse))

    reponse.place(x=0,rely=.8,relwidth=1,relheight=.2) # grid(row=1,column=0)
    reponse.focus_set()

    reussites = 0
    fautes = []

    for kanji in kanjis:
        next_var.set(False)
        question.configure(text=kanji[d[from_]])
        root.wait_variable(next_var)

        if reponse.get() in list(map(lambda s: s.lower(), kanji[d[to]])):
            reussites += 1
        else:
            showerror('Erreur', 'ma réponse: {0}\nréponse{s} correcte{s}:{1}'.format(reponse.get(), '\n - ' + '\n - '.join(kanji[d[to]]) if len(kanji[d[to]]) > 1 else ' ' + kanji[d[to]][0], s='s' if len(kanji[d[to]]) > 1 else ''))
            fautes.append([reponse.get(), kanji])

        reponse.delete(0, 'end')

    print('réussis: {}/{}'.format(reussites, len(kanjis)))

    if review:
        reussites = 0

        for faute in fautes:
            faute = faute[1]
            next_var.set(False)
            question.configure(text=faute[d[from_]])
            root.wait_variable(next_var)

            if reponse.get() in list(map(lambda s: s.lower(), faute[d[to]])) or any([fuzz.ratio(reponse.get().lower(), solution.lower())/100 > .7 for solution in kanji[d[to]]]):
                reussites += 1
            else:
                showerror('Erreur', 'ma réponse: {0}\nréponse{s} correcte{s}:{1}'.format(reponse.get(), '\n - ' + '\n - '.join(kanji[d[to]]) if len(kanji[d[to]]) > 1 else ' ' + kanji[d[to]][0], s='s' if len(kanji[d[to]]) > 1 else ''))
                print('2eme faute: {}'.format(faute))

            reponse.delete(0, 'end')

    return fautes

###########################################################################################################################################################################################################################################################################

def learn_vocab_gui(from_, to, review=True):
    global next_var
    vocab = list(build_vocab())
    shuffle(vocab)

    d = {'kanas': 0, 'kanjis': 1, 'meaning': 2}

    root = tk.Tk()
    root.title(title)
    root.protocol('WM_DELETE_WINDOW', lambda : restart(root))

    next_var = tk.BooleanVar()
    root.bind('<Return>', lambda *args: next_var.set(True) if reponse.get() else '')
    tk.Canvas(root, width=900, height=400).pack()

    question = tk.Label(root, font='Helvetica 75')
    question.place(x=0,y=0,relwidth=1,relheight=.8) # grid(row=0, column=0)
    reponse = tk.Entry(root)
    reponse.place(x=0,rely=.8,relwidth=1,relheight=.2) # grid(row=1,column=0)
    reponse.focus_set()

    reussites = 0
    fautes = []

    for voc in vocab:
        question_list = voc[d[from_]]
        if question_list.__len__() == 0:
            l = [0,1,2]
            l.remove(d[from_])
            l.remove(d[to])
            question_list = voc[l[0]]
        next_var.set(False)
        question.configure(text=question_list)
        root.wait_variable(next_var)

        if reponse.get() in list(map(lambda s: s.lower(), voc[d[to]])) or any([fuzz.ratio(reponse.get().lower(), solution.lower())/100 > .7 for solution in voc[d[to]]]):
            reussites += 1
        else:
            showerror('Erreur', 'ma réponse: {0}\nréponse{s} correcte{s}:{1}'.format(reponse.get(), '\n - ' + '\n - '.join(voc[d[to]]) if len(voc[d[to]]) > 1 else ' ' + voc[d[to]][0], s='s' if len(voc[d[to]]) > 1 else ''))
            fautes.append([reponse.get(), voc])

        reponse.delete(0, 'end')

    print('réussis: {}/{}'.format(reussites, len(vocab)))

    if review:
        reussites = 0

        for faute in fautes:
            question_list = faute[d[from_]]
            if question_list.__len__() == 0:
                l = [0,1,2]
                l.remove(d[from_])
                l.remove(d[to])
                question_list = faute[l[0]]
            faute = faute[1]
            next_var.set(False)
            question.configure(text=question_list)
            root.wait_variable(next_var)

            if reponse.get() in list(map(lambda s: s.lower(), faute[d[to]])) or any([fuzz.ratio(reponse.get().lower(), solution.lower())/100 > .7 for solution in voc[d[to]]]):
                reussites += 1
            else:
                showerror('Erreur', 'ma réponse: {0}\nréponse{s} correcte{s}:{1}'.format(reponse.get(), '\n - ' + '\n - '.join(voc[d[to]]) if len(voc[d[to]]) > 1 else ' ' + voc[d[to]][0], s='s' if len(voc[d[to]]) > 1 else ''))
                print('2eme faute: {}'.format(faute))

            reponse.delete(0, 'end')

    return fautes




def restart(root):
    global next_var
    next_var.set(True)
    root.destroy()
    tk._exit()

if __name__ == '__main__':
    if not console:
        {'kanjis': learn_kanjis_gui, 'vocab': learn_vocab_gui}[module](from_, to, review)
    else:
        raise NotImplementedError('Console mode not implemented yet.')


#
