# NSeg 文档

### 安装依赖

1. 使用crfmodel的依赖：CRFPP
```
安装方法:
1 download CRF++-0.58.tar.gz
2 tar -xvf CRF++-0.58.tar.gz
3 cd CRF
4 ./configure & make & sudo make install
5 cd python
6 python setup build 
7 sudo python setup.py install
```
2. 使用dcrf的依赖：pycrfsuite
```
pip install python-crfsuite
```
3. 使用lstm_seg的依赖：tensorflow,numpy,gensim
```
if use cpu version of tensorflow:
    pip install tensorflow
else:
    see https://www.tensorflow.org/get_started/index.html

1. pip install numpy
2. pip install gensim
```

### 安装说明
```
1 cd  NeuralSegmenter
2 sudo python setup.py install
```
> 执行命令后会将几个python文件安装到python默认包的路径下，会将模型文件安装到/tmp目录下

### API说明
1. crfmodel
```
$ python
Python 2.7.12 (default, Jul  1 2016, 15:12:24)
[GCC 5.4.0 20160609] on linux2
Type "help", "copyright", "credits" or "license" for more information.
$ import crfmodel
$ seg = crfmodel.crfSeg()
$ seg = crfmodel.crfSeg('models/CTB_model')
$ seg.seg('我爱北京天安门')
[u'\u6211', u'\u7231', u'\u5317\u4eac', u'\u5929\u5b89\u95e8']
$ pos = crfmodel.crfPos()
$ pos.seg('我爱北京天安门')
[(u'\u6211', 'PNP'), (u'\u7231', 'VV'), (u'\u5317\u4eac', 'LOC'), (u'\u5929\u5b89\u95e8', 'LOC')]
```
* crfmodel包含两个类,crfSeg和crfPos，分别用于分词和词性标注，crfSeg默认读取/tmp下的模型
* crfSeg有两个功能
  - **seg(sentence)**
    - 输入一个未切分的句子（str类型），返回一个包含所有切分词的list
  - **seg_files(fin,fout)**
    - 输入需要切分的文件的路径，若不指定输出路径，则返回一个二维list，代表文件中每一行的切分结果；若指定输出路径，按照切分后的结果输出


* crfPos有一个功能
  - **seg(sentence)**
    - 输入一个未切分的句子（str类型），返回一个包含所有切分词和其词性的tuple的list
 
2.dcrf
```
$ python
Python 2.7.12 (default, Jul  1 2016, 15:12:24)
[GCC 5.4.0 20160609] on linux2
Type "help", "copyright", "credits" or "license" for more information.
$ import dcrf
$ seg = dcrf.crfdSeg()
$ seg = dcrf.crfdSeg('models/bosonseg_weibo.pycrfsuite')
$ seg.seg('我爱北京天安门')
[u'\u6211', u'\u7231', u'\u5317\u4eac', u'\u5929\u5b89\u95e8']
```
* crfSeg有一个功能
  - **seg(sentence)**
    - 输入一个未切分的句子（str类型），返回一个包含所有切分词的list

3.lstm_seg
```
Python 3.5.2 (default, Jul  5 2016, 12:43:10)
[GCC 5.4.0 20160609] on linux
Type "help", "copyright", "credits" or "license" for more information.
$ import lstm_seg
I tensorflow/stream_executor/dso_loader.cc:108] successfully opened CUDA library libcublas.so.8.0 locally
I tensorflow/stream_executor/dso_loader.cc:108] successfully opened CUDA library libcudnn.so.5.1.5 locally
I tensorflow/stream_executor/dso_loader.cc:108] successfully opened CUDA library libcufft.so.8.0 locally
I tensorflow/stream_executor/dso_loader.cc:108] successfully opened CUDA library libcuda.so.1 locally
I tensorflow/stream_executor/dso_loader.cc:108] successfully opened CUDA library libcurand.so.8.0 locally
$ m = lstm_seg.lstmSeg()
$ m.seg_file('../CWS/icwb2-data/testing/msr_test.utf8','hello.txt')

...load information and processing...

```
* lstmSeg有一个功能
  - **seg_files(fin,fout)**
    - 输入需要切分的文件的路径和指定输出路径，按照切分后的结果输出