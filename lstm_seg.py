#coding=utf-8

import numpy as np, time
import tensorflow as tf
from lstm_utils import CharEmbedding, data_loader, batch_iter_test
import sys
import os
import re
from   optparse import OptionParser
from model_lstm_build import CWSModel,config_

files = 'res.txt'
outs = open(files,'w',encoding='utf-8')

'''
    run session to predict the label of each character
    Args: session - tf.session; 
          data - in the format of each sentence per list;
          model - loaded lstm model
          char_embedding - word2vec embedding class
          output - specify where to output th segmented corpus
    Returns: A new file of segmented corpus
'''
def pred(session, data, model, char_embedding,output=outs):
    vb = True
    starting = time.time()
    for step, (x, length) in enumerate(batch_iter_test(data, model.config.batch_size, char_embedding,
                                    model.config.left_window,model.config.right_window,sort=False)):
        flag = 0
        feed_ = {model.input_data: x, model.length: length}
        delta = time.time()
        # use gpu if available
        with tf.device('/gpu:0'):
            pred = session.run([model.predict], feed_dict=feed_)
        delta = time.time() - delta
        sys.stderr.write(' %d wps\n' % ( np.sum(length) / delta))
        # print each character 
        if vb:
            for xds in range(len(length)):
                sss = length[xds]
                ttts = {0: 'B', 1: 'C'}
                sent = ''
                shift = model.config.left_window
                for j in range(sss):
                    if int(pred[0][xds][j]):
                        sent += index2word[int(x[xds][j][shift])]
                    else:
                        if j != 0:
                            sent += ' '
                        sent += index2word[int(x[xds][j][shift])]
                output.write(sent + '\n')

    delta = time.time() - starting
    print (delta)
    return 0
    
class lstmSeg:
    '''
        lstmSeg: class used for segmentation;have to load word2vec model and lstm model at the same time
        
    '''
    def __init__(self, model_dir='/tmp/models/lstm_model',wvmodel='/tmp/models/wvmodel'):
        self.cmodel = CharEmbedding(wvmodel)
        global index2word
        index2word = self.cmodel.index_2_word()
        self.model_dir = model_dir
    '''
        Args: input_file - location of corpus to be segmented
              output_file - location to place the segemented corpus
              batch_size - how many sentence per batch; will speed up the segment proess if batch size gets large enough, default to 200
    '''
    def seg_file(self,input_file,output_file,batch_size=200):
        test_data = data_loader(input_file,self.cmodel, test=True, per_line=True)
        output_data = open(output_file,'w',encoding='utf-8')
        config = config_()
        config.vocab_size = self.cmodel.vocab_size()
        session_conf = tf.ConfigProto(
          allow_soft_placement=True)
        with tf.Graph().as_default(), tf.Session(config=session_conf) as session:
            self.session = session
            stddd = 0.1
            initializer = tf.truncated_normal_initializer(config.init_scale, stddev=stddd)

            with tf.variable_scope("model", reuse=None, initializer=initializer):
                self.model = CWSModel(is_training=False, config=config)
            self.model.config.batch_size = batch_size


            saver = tf.train.Saver()  # save all variables
            checkpoint_dir = self.model_dir
            ckpt = tf.train.get_checkpoint_state(checkpoint_dir)
            if ckpt and ckpt.model_checkpoint_path:
                saver.restore(self.session, ckpt.model_checkpoint_path)
                sys.stderr.write("model restored from %s\n" % (ckpt.model_checkpoint_path))
            else:
                sys.stderr.write("no checkpoint found" + '\n')
                sys.exit(-1)
            valid_accuracy = pred(self.session, test_data, self.model, self.cmodel, output_data)
        

