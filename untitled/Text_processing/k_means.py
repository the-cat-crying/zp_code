# coding=utf-8
import random
import numpy as np
import os
import sys


# 通过k-means ++ 算法获取YOLOv2需要的anchors的尺寸
# 定义Box类，描述bounding box的坐标
class Box:
    def __init__(self, x_c, y_c, w_w, h_w):
        self.x = x_c
        self.y = y_c
        self.w = w_w
        self.h = h_w


# 计算两个box在某个轴上的重叠部分
# x1是box1的中心在该轴上的坐标
# len1是box1在该轴上的长度
# x2是box2的中心在该轴上的坐标
# len2是box2在该轴上的长度
# 返回值是该轴上重叠的长度
def overlap(x1, len1, x2, len2):
    len1_half = len1 / 2
    len2_half = len2 / 2
    # 计算交集面积的w和h
    difference_max = max(x1 - len1_half, x2 - len2_half)
    difference_min = min(x1 + len1_half, x2 + len2_half)
    return difference_min - difference_max


# a和b都是Box类型实例
def box_iou(a, b):
    #
    w = overlap(a.x, a.w, b.x, b.w)
    h = overlap(a.y, a.h, b.y, b.h)
    if w < 0 or h < 0:
        return 0
    else:
        # 返回值area是box a 和box b 的交集面积
        area = w * h
    # 计算 box a 和 box b 的并集面积
    u = a.w * a.h + b.w * b.h - area
    # 返回值是box a 和box b 的iou
    return area / u


# 进行 k-means 计算新的centroids
# boxes是所有bounding boxes的Box对象列表
# n_anchors是k-means的k值
# 返回值loss是所有box距离所属的最近的centroid的距离的和
def do_k_means(n_anchors, boxes, centroids):
    loss = 0
    # 返回值groups是n_anchors个簇包含的boxes的列表,就是属于每一个中心类别的boxes的集合
    groups = []
    # 返回值new_centroids是计算出的新簇中心
    new_centroids = []
    for x in range(n_anchors):
        # 创建了一个有n个元素的空的groups和一个空的new_centroids
        groups.append([])
        new_centroids.append(Box(0, 0, 0, 0))
    for box in boxes:
        # 完全重合时，距离是0；完全不重合时，距离是1（此时为距离最远）
        min_distance = 1
        group_index = 0
        # enumerate函数用于将一个可遍历的数据对象(如列表、元组或字符串)组合为一个索引序列，同时列出数据和数据下标，一般用在 for 循环当中
        # 给第i个“box”分类,每个bounding box分别与anchor做iou并与1做差值，并找出最小距离并把该box分给该簇
        for centroid_index, centroid in enumerate(centroids):
            distance = (1 - box_iou(box, centroid))
            if distance <= min_distance:    # 当距离小于1时表示两个box有重合,'='两个框重合的时候
                min_distance = distance
                group_index = centroid_index
            else:
                pass
        groups[group_index].append(box)    # 找到box所属的类，然后把这个box放到group中
        loss += min_distance     # 每分类一个box，就叠加一次loss
        new_centroids[group_index].w += box.w
        # 每分类一次box，就将他的宽度叠加到这个类别的box的宽度上，最后得到一个属于此类别的宽度的总和，以便求均值
        new_centroids[group_index].h += box.h
        # 每分类一次box，就将他的高度叠加到这个类别的box的高度上，最后得到一个属于此类别的高度的总和，以便求均值
    for i in range(n_anchors):
        # 以均值形成新的类别box
        if new_centroids[i].w == 0 or new_centroids[i].h == 0:
            continue
        else:
            new_centroids[i].w /= len(groups[i])
            new_centroids[i].h /= len(groups[i])
    return new_centroids, groups, loss


# 计算给定bounding boxes的n_anchors数量的centroids(簇中心)
def compute_centroids(label_path, n_anchors, loss_convergence, grid_size, iterations_num):
    boxes = []
    # 得到我的boxes
    for line in label_path:
        temp = line.strip().split(" ")
        if len(temp) > 1:
            # 将所有的box中心都设置在原点,这一步之后就得到了box中心都设置在原点boxes集合
            boxes.append(Box(0, 0, float(temp[2]), float(temp[3])))
        else:
            pass
    # 在len长度的数字上随机抽取n个不重复的数，返回的是列表
    centroid_indices = random.sample(range(0, len(boxes)), n_anchors)
    # centroids是所有簇的中心
    centroids = []
    for centroid_index in centroid_indices:
        centroids.append(boxes[centroid_index])
    # iterate k-means
    # 第一次聚类为了算出新的centroids(簇心)
    centroids_s, groups, old_loss = do_k_means(n_anchors, boxes, centroids)
    iterations = 1
    i = 0
    while True:
        i = i+1
        # 使用同一变量centroids(簇心)为了使保持每次聚类随时更新(簇心)带入计算
        # 循环是为了使centroids(簇心)不在变化
        centroids_s, groups_s, loss = do_k_means(n_anchors, boxes, centroids_s)
        iterations = iterations + 1
        # print("number:", i, "--------loss = %f" % abs(old_loss-loss))
        if abs(old_loss - loss) < loss_convergence or iterations > iterations_num:
            break
        else:
            # loss值更新
            old_loss = loss
    # 打印最终anchor数据以及排序
    list_c = []
    for centroid in centroids_s:
        list_c.append([centroid.w, centroid.h])
    list_cc = []
    for i_c in list_c:
        list_cc.append(i_c[0]*i_c[1])
    # np.argsort函数返回排后元素的索引，如:[2,3,1]排后[1,2,3]返回索引[2,0,1]
    for np_arg in np.argsort(list_cc):
        # 从小到大排序后的anchor
        print("k-means:", int(list_c[np_arg][0]*grid_size), int(list_c[np_arg][1]*grid_size))


def list_txt(path):
    list_all = []
    for w in path:
        with open(os.path.join(argv_1, w), 'r') as f:
            list_all.append(f.readline())
    return list_all


if __name__ == '__main__':
    # label_path = "/home/zhoup/test/labels/air4.txt" // label_path是训练集列表文件地址
    # n_anchors = 5  // 是anchors的初始数量
    # loss_convergence = 1e-6  // 是允许的loss的最小变化值  阈值：结束迭代的判断标准
    # grid_size = 1  // grid_size * grid_size 是栅格数量,网格是几成几的网格？
    # iterations_num = 100 // 最大迭代次数
    # plus = 0 // plus = 1时启用k means ++ 初始化centroids
    print('**************Start**************')
    argv_1 = sys.argv[1]
    path_all = list_txt(path=os.listdir(argv_1))
    compute_centroids(label_path=path_all, n_anchors=5, loss_convergence=1e-6, grid_size=416, iterations_num=100)
    print('*********Already Finish*********')
