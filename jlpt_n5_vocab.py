# Japonais NLPT N5 Vocabulaire
from jlptutils import *
import json

def read_vocab(lang_index):
    lang = ['en', 'fr'][lang_index]
    vocab = json.loads(open_from_data(f'vocab-{lang}.json').read())
    return vocab

def build_vocab():
    vocab = open('jlpt-n5-vocab-2.txt', 'r', encoding='utf-8').read().replace('[一段]', '').replace('[五段]', '').replace('  ', ' ')
    vocab = vocab.split('\n')

    for all_vocab in vocab:

        # trouver kanas
        index = 3
        while all_vocab[index] in hiragana_chart + '・, ' or all_vocab[index] in katakana_chart + '・, ':
            index += 1
        kanas = list(filter(None, all_vocab[3:index].split()))

        # trouver kanjis
        old_index = index
        while all_vocab[index] not in alphabet:
            index += 1
        kanjis = list(filter(None, all_vocab[old_index:index].split()))

        # trouver signification
        while '(' in all_vocab[index:]:
            sub_text = all_vocab[index:all_vocab.index('(', index)] + all_vocab[all_vocab.index(')', index)+1:]
            all_vocab = all_vocab[:index] + sub_text
            all_vocab.replace('  ', ' ')
        signification = list(map(lambda s: ' '.join(list(filter(None, s.split()))), list(filter(None, all_vocab[index:].split(', ')))))

        # append all to list
        yield [kanas, kanjis, signification]








#
