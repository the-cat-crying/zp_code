from Images_labels_tools.function import public_function
from PIL import Image
import os
import tqdm


# images_format_transform
def mat(m_file):
    for index in tqdm.tqdm(m_file):
        img = Image.open(index)
        if img.mode != 'RGB':
            img = img.convert('RGB')
            # print(img.mode)
        if img.format != 'jpg':
            prefix, suffix = os.path.split(index)
            abs_path_img_ = os.path.join(prefix, suffix.split('.')[0] + '.jpg')
            img.save(abs_path_img_)
        else:
            img.save(index)


if __name__ == '__main__':
    img_file = public_function.Public().picture_operate()
    mat(img_file)
