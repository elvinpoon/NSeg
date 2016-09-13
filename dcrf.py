import pycrfsuite
import codecs
'''
        load dictionary to identify types of character: punctuation,character of english,numbers(cn and en), time(cn) and word dict for segmentation.
'''
biaodian = {}.fromkeys([line.rstrip() for line in codecs.open('/tmp/dict/biaodian.utf8', 'r', 'utf-8')])
characters = {}.fromkeys([line.rstrip() for line in codecs.open('/tmp/dict/char.utf8', 'r', 'utf-8')])
numbers = {}.fromkeys([line.rstrip() for line in codecs.open('/tmp/dict/num.utf8', 'r', 'utf-8')])
timing = {}.fromkeys([line.rstrip() for line in codecs.open('/tmp/dict/time.utf8', 'r', 'utf-8')])

word_dict = {}.fromkeys([line.rstrip() for line in codecs.open('/tmp/dict/dictionary.utf8', 'r', 'utf-8')])

def char_type(word):
    '''
        Arg: char in unicode format
        Returns: type of char coded by 'PANDO'
    '''
    t = 'O'
    if word in biaodian:
        t = 'P'
    elif word in characters:
        t = 'A'
    elif word in numbers:
        t = 'N'
    elif word in timing:
        t = 'D'
    return t
def word2features(sent, i,wdict):
    '''
        feature extraction of a certain position in sentence; features are neibourghing char features;char type features;bigram and skipgram;repetition of char;word dictionary existence feature.
        Args: sentence in format of [(word,?),...,(word,?)], position i, word dictionary wdict
        Return: A list of features
    '''
    word = sent[i][0]
    feature = [
        'w=' + word,
        't=' + char_type(word),
    ]
    if i > 0:
        word1 = sent[i-1][0]
        feature.extend([
                '-1:w=' + word1,
                '-1:b=' + word1+word,
                '-1:t=' + char_type(word1),
                'r1=' + str((word1==word))
            ])
        if i < len(sent) -1:
            feature.extend([
                    's=' +word1 +sent[i+1][0]
                ])
    else:
        feature.append('BOS')
    if i > 1:
        word2 = sent[i-2][0]
        feature.extend([
                '-2:w=' + word2,
                '-2:b=' + word2 + sent[i-1][0],
                '-2:t=' + char_type(word2),
                'r2=' + str((word2==word))
            ])
    if i < len(sent) - 1:
        wordp1 = sent[i+1][0]
        feature.extend([
                '+1:w=' + wordp1,
                '+1:b=' + word+wordp1,
                '+1:t=' + char_type(wordp1),
            ])
    else:
        feature.append('EOS')
    if i < len(sent) - 2:
        wordp1 = sent[i+1][0]
        wordp2 = sent[i+2][0]
        feature.extend([
                '+2:w=' + wordp2,
                '+2:b=' + wordp1+wordp2,
                '+2:t=' + char_type(wordp2),
            ])
    phrase = word
    for kend in range(1,7):
        if i + kend >= len(sent):
            break
        else:
            phrase += sent[i+kend][0]
            found = phrase in wdict
            feature.append('+P-' + str(kend) +'=' + str(found))
    suffix = word
    for kend in range(1,7):
        if i - kend < 0:
            break
        else:
            suffix = sent[i-kend][0] + suffix
            found = suffix in wdict
            feature.append('-P-' + str(kend) +'=' + str(found))
    
    return feature

def sent2features(sent,wdict):
    return [word2features(sent, i, wdict) for i in range(len(sent))]

def sent2labels(sent):
    return [label for token, label in sent]

def sent2tokens(sent):
    return [token for token, label in sent]

class crfdSeg:
    '''
        crf model with dictionary features to perform chinese word segmentation task
        default model located at /tmp/models/bosonseg.pycrfsuite & default dict at    
        /tmp/dict/dictionary.utf8.
    '''
    def __init__(self,model='/tmp/models/bosonseg.pycrfsuite',dictionary=word_dict):
        self.tagger = pycrfsuite.Tagger()
        self.tagger.open(model)
        self.wdict = dictionary
    
    def seg(self,sentence):
        '''
            Args:
                sentence: a chinese sentence in the format of str object, default coding is utf-8
            Returns:
                A list of (word,postag) pairs in tuple format
        '''
        sentence = sentence.decode('utf-8')
        x = sent2features(sentence,self.wdict)
        y = self.tagger.tag(x)
        seg_list = []
        current_word = ''
        for i in range(len(sentence)):
            char = sentence[i]
            tag = y[i]
            if tag == 'B':
                current_word = char
            elif tag == 'M':
                current_word += char
            elif tag == 'E':
                current_word += char
                seg_list.append(current_word)
                current_word = ''
            else: # tag == 'S'
                seg_list.append(char)
        return seg_list

