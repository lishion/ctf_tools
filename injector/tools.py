#二分搜索
#start:搜索起点
#end:搜索终点
#filter:接受两个参数，第一个是">,<,="，第二个是当前搜索的中点，返回搜索值与中点的大写关系
def binary_search(start,end,filter):

    start_now = start
    end_now = end
    get_middle = lambda s,e:(s+(e-s)//2)

    if end==start or start>end:
        print("input right that end one must < start one")
        exit(0)

    while True:
        middle = get_middle(start_now,end_now)
        
        if filter(">",middle):
            start_now = middle

        elif filter("<",middle):
            end_now = middle

        elif filter("=",middle):
            return middle

        if (end_now-start_now)<=3:
            for i in range(start_now,end_now+1):
                if filter("=",i):
                    return i
            return -1 

 