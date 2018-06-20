#coding:utf-8
#查找算法, wrote by tzf, 2018/5/10

class SearchAlgorithm:
    def __init__(self):
        pass

    """
    函数说明:二分法查找算法, 算法复杂度O(log2n),
    注意：二分查找的前提必须待查找的序列有序。

    Parameters:
        array - 待查找的数组
        t - 目标元素
    Returns:
        (0/1,mid) - (是否找到目标元素, 目标元素的位置)
    """
    def binary_search(array,t):
        low = 0
        height = len(array)-1
        while low < height:
            mid = (low+height)//2                         #The // indicates floor division in Python 3.x.
            if array[mid] < t:
                low = mid + 1

            elif array[mid] > t:
                height = mid - 1

            else:
                #return array[mid]
                return (1,mid)

        return (0,0)

    #for test
    res1 = binary_search([1,2,3,34,56,57,78,87],57)
    print('use the binary search to find the target and position: ', res1)

