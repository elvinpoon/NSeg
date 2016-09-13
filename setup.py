from distutils.core import setup
setup(
 name='Segger',  
 version='0.1.0',
 data_files=[('/tmp/models', ['models/PD_model_s','models/bosonseg.pycrfsuite','models/wvmodel',
                              'models/bosonpos.pycrfsuite','models/POS_model']),
             ('/tmp/models/lstm_model',['models/model_T/checkpoint','models/model_T/model_35.ckpt',
                                       'models/model_T/model_35.ckpt.meta']),
             ('/tmp/dict',['dict/biaodian.utf8','dict/char.utf8',
                           'dict/num.utf8','dict/time.utf8',
                           'dict/dictionary.utf8','dict/CoreNatureDictionary.utf8'])],
 platforms='any',
 packages=[''],
 description='python chinese word segmentation tools',
 url=' ',
 author=u'Chenyi Pan',
 author_email='pcy@meitu.com',
 )
