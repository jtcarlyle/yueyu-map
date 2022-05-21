#~/.virtualenvs/common-yue/bin/python
# -*- coding: utf-8 -*-
import pandas as pd
import os


df = pd.read_excel('cy_lex_77.xlsx', sheet_name='data') #encoding='utf-8'
df.gloss_en = df.gloss_en.str.replace(r'\s', '_', regex=True)
df.dialect = df.dialect.str.replace('_P', '_p')

#sanitization tweaks
df.transcription = df.transcription.str.replace(r'e(ŋ|k)', r'i\1', regex=True)
df.transcription = df.transcription.str.replace(r'o(ŋ|k)', r'u\1', regex=True)
df.transcription = df.transcription.str.replace(r'[ʃɕʂ]', r's', regex=True)
df.transcription = df.transcription.str.replace(r'(^|\s)j?i([aɐəeɛɔuyœøɪʏ])', r'\1j\2', regex=True)
df.transcription = df.transcription.str.replace(r'(^|\s)w?u([aɐəeɛɔuyœøɪʏ])', r'\1w\2', regex=True)
df.transcription = df.transcription.str.replace(r'(^|\s)i', r'\1ji', regex=True)
df.transcription = df.transcription.str.replace(r'(^|\s)u', r'\1wu', regex=True)
df.transcription = df.transcription.str.replace(r'(^|\s)ʔ', r'\1', regex=True)
df.transcription = df.transcription.str.replace(r'niɐ', r'ȵɐ', regex=True)
df.transcription = df.transcription.str.replace(r'\s', '.', regex=True)


lex_items = df.groupby('gloss_en')
for gloss, entries in lex_items:
    dialects = entries.groupby('dialect')
    filename = 'sanfon/' + gloss + '.lex'
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w+', encoding='UTF-8') as f:
        f.write('%utf8\n') #not necessary for tokens I think?
        for dialect, forms in dialects:
            f.write(': ' + dialect + '\n')
            for form in forms['transcription'].tolist():
                f.write('- ' + str(form) + '\n')

# # df = pd.read_excel('45Q_lex_dist_v2.xlsx', encoding='utf-8', sheet_name='data')
# # df.gloss_en = df.gloss_en.str.replace(r'\s', '_', regex=True)
# # df.dialect = df.dialect.str.replace('_P', '_p')

lex_items = df.groupby('gloss_en')
for gloss, entries in lex_items:
    dialects = entries.groupby('dialect')
    filename = 'lex/' + gloss + '.lex'
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w+', encoding='UTF-8') as f:
        f.write('%utf8\n')
        for dialect, forms in dialects:
            f.write(': ' + dialect + '\n')
            for form in forms['form'].tolist():
                f.write('- ' + str(form) + '\n')

#above is manual lexification and ipa lex

#this is north wind crud
# df1 = pd.read_excel('nw_lex_data.xlsx', encoding='utf-8', sheet_name='Sheet1')
# df1.CONCEPT = df1.CONCEPT.str.replace(r'\s', '_', regex=True)
# df1.DOCULECT = df1.DOCULECT.str.replace('_P', '_p')

# fon_items = df1.groupby('CONCEPT')
# for gloss, entries in fon_items:
#     dialects = entries.groupby('DOCULECT')
#     filename = 'fon/' + gloss + '.fon'
#     os.makedirs(os.path.dirname(filename), exist_ok=True)
#     with open(filename, 'w+', encoding='UTF-8') as f:
#         for dialect, forms in dialects:
#             f.write(': ' + dialect + '\n')
#             for form in forms['IPA'].tolist():
#                 f.write('- ' + str(form) + '\n')

# #this is the ziyin stuff

# df2 = pd.read_csv('cy_unique_char.csv', encoding='utf-8',dtype=str, keep_default_na=False)

# ziyin_items = df2.groupby('gybh')

# temp = ziyin_items.get_group('1')
# ''.join(temp['graph'].unique().tolist())
# ''.join(temp['tone_class'].unique().tolist())

# for bianhao, entries in ziyin_items:
#     dialects = entries.groupby('dialect')
#     filename = 'ziyin/' + str(bianhao) + '.fon'
#     os.makedirs(os.path.dirname(filename), exist_ok=True)
#     with open(filename, 'w+', encoding='UTF-8') as f:
#         f.write('%utf8\n')
#         chars = [str(i) for i in entries['graph'].unique().tolist()]
#         tones = [str(i) for i in entries['tone_class'].unique().tolist()]
#         f.write('# ' +  str(bianhao) + ' ' + ''.join(chars) + ' ' + ''.join(tones) + '\n')
#         for dialect, forms in dialects:
#             f.write(': ' + dialect + '\n')
#             for form in forms['IPA'].tolist():
#                 f.write('- ' + str(form) + '\n')






