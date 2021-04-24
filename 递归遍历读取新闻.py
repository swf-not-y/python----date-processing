import os,time

'''
功能描述：遍历目录，对子文件单独处理
'''
# 2 遍历目录文件
def TraversalDir(rootDir):
    # 返回指定目录包含的文件或文件夹的名字的列表
    for i,lists in enumerate(os.listdir(rootDir)):#enumerate是Python的的内置函数，对于可迭代的对象，其可以将其组成一个索引序列，利用它可以获得索引值
        #listdir获取目录中的文件夹，但是不返回文件夹里的子文件，i是文件数
        # 待处理文件夹名字集合
        path = os.path.join(rootDir, lists)
        # 核心算法，对文件具体操作
        if os.path.isfile(path):
            if i%5000 == 0:
                print('{t} *** {i} \t docs has been read'.format(i=i, t=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())))
        # 递归遍历文件目录
        if os.path.isdir(path):
            TraversalDir(path)



if __name__ == '__main__'://main函数入口
    t1=time.time()

    # 根目录文件路径
    rootDir = r"C:\Users\Administrator\Documents\python数据处理\数据预处理源代码\第五章-文本数据清洗\新闻语料库"
    TraversalDir(rootDir)

    t2=time.time()
    print('totally cost %.2f' % (t2-t1)+' s')