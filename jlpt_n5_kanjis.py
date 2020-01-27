# Japonais NLPT N5 Kanjis
from jlptutils import *
import json

def read_kanjis(lang_index):
    lang = ['en', 'fr'][lang_index]
    kanjis = json.loads(open_from_data(f'kanjis-{lang}.json').read())
    return kanjis

def build_kanjis():
    kanjis = open('jlpt-n5-kanjis.txt', 'r', encoding='utf-8').read()
    kanjis = kanjis.split('\n')

    for all_kanji in kanjis:

        # trouver kanji
        kanji = all_kanji[3]

        # trouver lecture-on
        index = 5
        while all_kanji[index] not in hiragana_chart:
            index += 1
        lecture_on = list(filter(None, all_kanji[5:index].replace(',','').split()))

        # trouver lecture-kun
        old_index = index
        while all_kanji[index] not in alphabet:
            index += 1
        lecture_kun = list(filter(None, all_kanji[old_index:index].split()))

        # trouver signification
        signification = list(filter(None, all_kanji[index:].split(', ')))

        # append all to list
        yield [kanji, lecture_on, lecture_kun, signification]

#
