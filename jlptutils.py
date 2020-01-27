# -*- coding: UTF-8 -*-
# Utils for Japanese JLPT N5
import os
import jaconv

dir_path = os.path.realpath(__file__).replace(os.path.basename(os.path.realpath(__file__)), '')
joinpath = lambda *args: os.path.join(*args)
open_from_data = lambda filename, flag='r', encoding='utf-8', subfolder='': open(joinpath(dir_path, 'data', subfolder, filename), flag, encoding=encoding)

from string import ascii_letters as alphabet, ascii_lowercase
alphabet += 'áéíóú' + 'âêîôû' + 'àèìòù' + 'ÁÉÍÓÚ' + 'ÂÊÎÔÛ' + 'ÀÈÌÒÙ' + 'œ'
katakana_chart = open_from_data('hiragana-chart.txt').read()
hiragana_chart = open_from_data('katakana-chart.txt').read()

text_history = ''

def update_entry(index, entry):
    global text_history
    kana = jaconv.alphabet2kana(text_history) if index == 2 else jaconv.hira2kata(jaconv.alphabet2kana(text_history))
    if kana.endswith('っ') or (kana.endswith('ん') and not text_history.endswith('nn')):
        kana = kana[:-1] + text_history[-1]
    entry.delete(0, 'end')
    entry.insert(0, kana)
    return True

def key_pressed(event, index, entry):
    global text_history
    char = event.char
    keycode = event.keycode
    if char in ascii_lowercase:
        text_history += char
    if keycode == 27:
        text_history = ''
    update_entry(index, entry)

def del_pressed(index, entry):
    global text_history
    entry_text = entry.get()
    if text_history:
        if entry_text.endswith('ん'):
            text_history = text_history[:-2]
        elif entry_text[-1] not in alphabet:
            text_history = text_history[:-len(jaconv.kana2alphabet(entry_text[-1]) if entry_text[-1] in hiragana_chart else jaconv.kana2alphabet(jaconv.kata2hira(entry_text[-1])))]
        else: text_history = text_history[:-1]
    update_entry(index, entry)

def clear_text_history():
    global text_history
    print('called')
    text_history = ''
    return True














#
