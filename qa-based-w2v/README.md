# sentence similarity based on w2v

## run
ps: <br>
    all files are utf-8.<br>
    allhtmlcontent must one sentence one line.<br>

1. prepare 4 files <br>
    allhtmlcontent.txt: source file<br>
    filterword.txt: used in word segment & filter the result<br>
    mydict.dic: used in jieba<br>
    stopword.dic: userd in jieba<br>

2. python word_segment.py<br>
    we can get files that are segmented<br>

3. python w2v.py<br>
    we can get the model<br>

4. python similarity.py sentence<br>
    calculate the similarity between sentence<br>
    eg: python similarity.py ʲô�Ƿ�Ʊ<br>