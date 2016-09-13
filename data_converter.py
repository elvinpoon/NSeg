import codecs
import sys

biaodian = {}.fromkeys([line.rstrip() for line in codecs.open('dict/biaodian.utf8', 'r', 'utf-8')])
characters = {}.fromkeys([line.rstrip() for line in codecs.open('dict/char.utf8', 'r', 'utf-8')])
num = {}.fromkeys([line.rstrip() for line in codecs.open('dict/num.utf8', 'r', 'utf-8')])
timing = {}.fromkeys([line.rstrip() for line in codecs.open('dict/time.utf8', 'r', 'utf-8')])


def feature_extraction(input_file, output_file,tagged = True):
    input_data = codecs.open(input_file, 'r', 'utf-8')
    output_data = codecs.open(output_file, 'w', 'utf-8')
    wordss = []
    for line in input_data.readlines():
        word_tag = line.strip()
        if word_tag == '':
            #print wordss
            for ids, charss in enumerate(wordss):
                char, tag = charss.split('\t')
                output_data.write(char + '\t')
                T = 'O'
                if char in biaodian:
                    T = 'P'
                elif char in characters:
                    T = 'A'
                elif char in num:
                    T = 'N'
                elif char in timing:
                    T = 'D'
                output_data.write(T + '\t' + tag + '\n')
            wordss = []
            output_data.write('\n')
        else:
            if '\t' not in word_tag:
                word_tag = ' '+ '\t' + word_tag
            wordss.append(word_tag)

def character_tagging(input_file, output_file):
    input_data = codecs.open(input_file, 'r', 'utf-8')
    output_data = codecs.open(output_file, 'w', 'utf-8')
    for line in input_data.readlines():
        word_list = line.strip().split()
        for word in word_list:
            if len(word) == 1:
                output_data.write(word + "\tS\n")
            else:
                output_data.write(word[0] + "\tB\n")
                for w in word[1:len(word)-1]:
                    output_data.write(w + "\tM\n")
                output_data.write(word[len(word)-1] + "\tE\n")
        output_data.write("\n")
    input_data.close()
    output_data.close()

def character_split(input_file, output_file, extracted = False):
    input_data = codecs.open(input_file, 'r', 'utf-8')
    output_data = codecs.open(output_file, 'w', 'utf-8')
    for line in input_data.readlines():
        for word in line.strip():
            word = word.strip()
            if word and not extracted:
                output_data.write(word + "\tB\n")

        output_data.write("\n")
    input_data.close()
    output_data.close()

def character_2_word(input_file, output_file):
    input_data = codecs.open(input_file, 'r', 'utf-8')
    output_data = codecs.open(output_file, 'w', 'utf-8')
    for line in input_data.readlines():
        if line == "\n":
            output_data.write("\n")
        else:
            char_tag_pair = line.strip().split('\t')
            char = char_tag_pair[0]
            tag = char_tag_pair[2]
            if tag == 'B':
                output_data.write(' ' + char)
            elif tag == 'M':
                output_data.write(char)
            elif tag == 'E':
                output_data.write(char + ' ')
            else: # tag == 'S'
                output_data.write(' ' + char + ' ')
    input_data.close()
    output_data.close()

def gene_word_gold(input_file, output_file):
    input_data = codecs.open(input_file, 'r', 'utf-8')
    output_data = codecs.open(output_file, 'w', 'utf-8')
    word_dict = []
    current_word = ''
    for line in input_data.readlines():
        if line == '\n':
            current_word = ''
        else:
            char_tag_pair = line.strip().split('\t')
            if len(char_tag_pair) != 2:
                continue
            char = char_tag_pair[0]
            tag = char_tag_pair[1]
            if tag == 'B':
                current_word = char
            elif tag == 'M' or tag == 'E':
                current_word += char
                if tag == 'E':
                    word_dict.append(current_word)
                    current_word = ''
            else:
                word_dict.append(char)
                current_word = ''
    for word in word_dict:
        output_data.write(word + '\n')
    input_data.close()
    output_data.close()
def execute():
    inputs = 'trainSeg.txt'
    output = 'seg_result/extracted_weibo.utf8'
    feature_extraction(inputs, output)
if __name__ == '__main__':
    if len(sys.argv) != 3:
        print "pls use: python make_crf_train_data.py input output"
        sys.exit()
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    character_tagging(input_file, output_file)
