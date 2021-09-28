import os
import hashlib
import cv2
import shutil
import tqdm


if __name__ == '__main__':
    c = '/home/gy/mount_sdc/python_code/zp_code/request/456'
    c_ = os.listdir(c)
    c_.sort()

    md5_dict = {}
    for i in tqdm.tqdm(c_):
        abs_path = os.path.join(c, i)
        p = hashlib.md5(cv2.imread(abs_path))
        md5_dict[p] = abs_path
    for j in md5_dict:
        shutil.move(md5_dict[j], '/home/gy/mount_sdc/python_code/zp_code/request/123')
