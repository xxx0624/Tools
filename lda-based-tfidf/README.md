# LDA based on TF-IDF

1. 准备语料 <br>
    eg:localfile/allhtmlcontent

2. 分词(based on jieba)<br>
    python word_segment.py file1 file2 file3 fil4<br>
    file1: 待分词文件(required)<br>
    file2：分词结果(required)<br>
    file3：过滤词典<br>
    file4：过滤后的文件<br>
    file5：分词自定义词典<br>
    file6：停用词词典<br>

    eg:python word_segment.py localfile/allhtmlcontent.txt localfile/wordallhtmlcontent.txt 

3. TF-IDF(based on sklearn) (NOT_necessary)<br>
    python tf-idf.py file4 result_file tf_idf_min_value<br>
    file4：同2中file4(required)<br>
    result_file：tfidf计算结果文件地址(required)<br>
    tf_idf_min_value：在tf-idf矩阵中过滤低于该值的column(required)<br>

    eg:python tf-idf.py localfile/wordallfilterhtmlcontent.txt localfile/x_array.txt 5

4. LDA<br>
    python lda-based-tfidf.py (argv[] in main)<br>
    filter_file_path：同2中的file4(required)<br>
    show_topic_word_num：console中的展示结果，每个topic的word数目<br>
    n_topics random_state n_iter 分别是lda参数<br>

    ps:files in localfile/finalResult/ are 'UTF-8'

    eg:python lda_tfidf.py <br>