db_tab_name = 'music_genre_tab'

upsert_col = 'trackid'

db_cols_dict = {
    'trackID': 'trackid',
    'title': 'title',
    'preds': 'genre'
}

float_cols = [
    'loudness', 'tempo',
    'vect_1', 'vect_2', 'vect_3', 'vect_4', 'vect_5', 'vect_6', 'vect_7',
    'vect_8', 'vect_9', 'vect_10', 'vect_11', 'vect_12', 'vect_13',
    'vect_14', 'vect_15', 'vect_16', 'vect_17', 'vect_18', 'vect_19',
    'vect_20', 'vect_21', 'vect_22', 'vect_23', 'vect_24', 'vect_25',
    'vect_26', 'vect_27', 'vect_28', 'vect_29', 'vect_31', 'vect_32',
    'vect_33', 'vect_34', 'vect_35', 'vect_36', 'vect_37', 'vect_38',
    'vect_39', 'vect_40', 'vect_41', 'vect_42', 'vect_54', 'vect_55',
    'vect_56', 'vect_58', 'vect_59', 'vect_60', 'vect_61', 'vect_62',
    'vect_63', 'vect_64', 'vect_65', 'vect_66', 'vect_67', 'vect_68',
    'vect_69', 'vect_71', 'vect_72', 'vect_73', 'vect_74', 'vect_87',
    'vect_88', 'vect_89', 'vect_90', 'vect_91', 'vect_92', 'vect_93',
    'vect_94', 'vect_96', 'vect_97', 'vect_99', 'vect_100', 'vect_101',
    'vect_102', 'vect_104', 'vect_116', 'vect_117', 'vect_118', 'vect_120',
    'vect_122', 'vect_123', 'vect_125', 'vect_126', 'vect_128', 'vect_129',
    'vect_131', 'vect_132', 'vect_134', 'vect_135', 'vect_147']

cat_cols = [
    'time_sig_mt4',
    '00|00', '00|01', '01|00', '01|01', '02|00', '02|01',
    '03|00', '03|01', '04|00', '04|01', '05|00', '05|01',
    '06|00', '06|01', '07|00', '07|01', '08|00', '08|01',
    '09|00', '09|01', '10|00', '10|01', '11|00', '11|01']

stopwords = [
    'i',
    'me',
    'my',
    'myself',
    'we',
    'our',
    'ours',
    'ourselves',
    'you',
    'you re',
    'you ve',
    'you ll',
    'you d',
    'your',
    'yours',
    'yourself',
    'yourselves',
    'he',
    'him',
    'his',
    'himself',
    'she',
    'she s',
    'her',
    'hers',
    'herself',
    'it',
    'it s',
    'its',
    'itself',
    'they',
    'them',
    'their',
    'theirs',
    'themselves',
    'what',
    'which',
    'who',
    'whom',
    'this',
    'that',
    'that ll',
    'these',
    'those',
    'am',
    'is',
    'are',
    'was',
    'were',
    'be',
    'been',
    'being',
    'have',
    'has',
    'had',
    'having',
    'do',
    'does',
    'did',
    'doing',
    'a',
    'an',
    'the',
    'and',
    'but',
    'if',
    'or',
    'because',
    'as',
    'until',
    'while',
    'of',
    'at',
    'by',
    'for',
    'with',
    'about',
    'against',
    'between',
    'into',
    'through',
    'during',
    'before',
    'after',
    'above',
    'below',
    'to',
    'from',
    'up',
    'down',
    'in',
    'out',
    'on',
    'off',
    'over',
    'under',
    'again',
    'further',
    'then',
    'once',
    'here',
    'there',
    'when',
    'where',
    'why',
    'how',
    'all',
    'any',
    'both',
    'each',
    'few',
    'more',
    'most',
    'other',
    'some',
    'such',
    'no',
    'nor',
    'not',
    'only',
    'own',
    'same',
    'so',
    'than',
    'too',
    'very',
    's',
    't',
    'can',
    'will',
    'just',
    'don',
    'don t',
    'should',
    'should ve',
    'now',
    'd',
    'll',
    'm',
    'o',
    're',
    've',
    'y',
    'ain',
    'aren',
    'aren t',
    'couldn',
    'couldn t',
    'didn',
    'didn t',
    'doesn',
    'doesn t',
    'hadn',
    'hadn t',
    'hasn',
    'hasn t',
    'haven',
    'haven t',
    'isn',
    'isn t',
    'ma',
    'mightn',
    'mightn t',
    'mustn',
    'mustn t',
    'needn',
    'needn t',
    'shan',
    'shan t',
    'shouldn',
    'shouldn t',
    'wasn',
    'wasn t',
    'weren',
    'weren t',
    'won',
    'won t',
    'wouldn',
    'wouldn t']
