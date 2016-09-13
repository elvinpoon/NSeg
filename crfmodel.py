#coding: utf-8
import CRFPP
import codecs

    
class crfSeg:
    '''
        crfSeg: a class to operate chinese word segmentation task on sentences or files
                default model is installed under /tmp/models/CTB_models
    '''
    def __init__(self,model='/tmp/models/PD_model_s'):
        self.tagger = CRFPP.Tagger("-m " + model)
    
    def seg_files(self,input_file,output_file=None,encoding='utf-8'):
        '''
            Args:
                input_file: the path of file to open,must be in the format of one sentence per line
                output_file: the file to write segmented corpus;if not specified, will return a list of
                    segmented sentences
                encoding: the encoding of files, default to utf-8
            Returns:
                A list of segmented sentences(in the structrue of list) if output_file not specified;
                or True if the output_file is specified
        '''
        input_data = codecs.open(input_file, 'r', encoding)
        if output_file is None:
            word_list = []
            for line in input_data:
                self.tagger.clear()
                for word in line.strip():
                    word = word.strip()
                    if word:
                        self.tagger.add((word + '\tB\n').encode('utf-8'))
                self.tagger.parse()
                size = self.tagger.size()
                xsize = self.tagger.xsize()
                current_word = ''
                seg_list = []
                for i in range(0, size):
                    char = self.tagger.x(i, 0).decode('utf-8')
                    tag = self.tagger.y2(i)
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
                word_list.append(seg_list)
            input_data.close()
            return word_list
        else:
            output_data = codecs.open(output_file, 'w', 'utf-8')
            for line in input_data:
                self.tagger.clear()
                for word in line.strip():
                    word = word.strip()
                    self.tagger.add((word+'\tB\n').encode('utf-8'))
                self.tagger.parse()
                size = self.tagger.size()
                xsize = self.tagger.xsize()
                current_word = ''
                for i in range(0, size):
                    char = self.tagger.x(i, 0).decode('utf-8')
                    #print char
                    tag = self.tagger.y2(i)
            
                    if tag == 'B':
                        current_word = char
                    elif tag == 'M':
                        current_word += char
                    elif tag == 'E':
                        current_word += char
                        output_data.write(current_word)
                        output_data.write(' ')
                        current_word = ''
                    else: # tag == 'S'
                        output_data.write(char)
                        output_data.write(' ')
                output_data.write('\n')
            input_data.close()
            output_data.close()
            return True
    
    def seg(self,sentence):
        '''
            Args:
                sentence: a chinese sentence in the format of str object, default coding is utf-8
            Returns:
                A list of words
        '''
        self.tagger.clear()
        for word in sentence.strip().decode('utf-8'):
            word = word.strip()
            if word:
                self.tagger.add((word + '\tB\n').encode('utf-8'))
        self.tagger.parse()
        size = self.tagger.size()
        xsize = self.tagger.xsize()
        current_word = ''
        seg_list = []
        for i in range(0, size):
            char = self.tagger.x(i, 0).decode('utf-8')
            tag = self.tagger.y2(i)
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

class crfPos:
    '''
        crfSeg: a class to operate joint chinese word segmentation and pos tagging task on sentences or files
                default model is installed under /tmp/models/POS_model
    '''
    def __init__(self,model='/tmp/models/POS_model'):
        self.tagger = CRFPP.Tagger("-m " + model)
    
    def seg(self,sentence):
        '''
            Args:
                sentence: a chinese sentence in the format of str object, default coding is utf-8
            Returns:
                A list of (word,postag) pairs in tuple format
        '''
        self.tagger.clear()
        for word in sentence.strip().decode('utf-8'):
            word = word.strip()
            if word:
                self.tagger.add((word + '\tB\n').encode('utf-8'))
        self.tagger.parse()
        size = self.tagger.size()
        xsize = self.tagger.xsize()
        current_word = ''
        seg_list = []
        for i in range(0, size):
            char = self.tagger.x(i, 0).decode('utf-8')
            tag = self.tagger.y2(i)
            if tag[0] == 'B':
                current_word = char
            elif tag[0] == 'M':
                current_word += char
            elif tag[0] == 'E':
                current_word += char
                seg_list.append((current_word,tag.split('-')[1]))
                current_word = ''
            else: # tag == 'S'
                seg_list.append((char,tag.split('-')[1]))
        return seg_list