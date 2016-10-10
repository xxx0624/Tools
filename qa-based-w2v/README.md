# sentence similarity based on w2v

## run (All files are UTF-8)
1. prepare 4 files <br>
    allhtmlcontent.txt: source file
    filterword.txt: used in word segment & filter the result
    mydict.dic: used in jieba
    stopword.dic: userd in jieba

2. python word_segment.py
    we can get files that are segmented

3. python w2v.py
    we can get the model

4. python similarity.py sentence
    calculate the similarity between sentence
    eg: python similarity.py ʲô�Ƿ�Ʊ