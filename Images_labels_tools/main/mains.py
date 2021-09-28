# -*- coding:utf-8 -*-
# 作者:周鹏
from Images_labels_tools.function import public_function
from Images_labels_tools.config import setting
from Images_labels_tools.function import images_cover
from Images_labels_tools.function import images_labels_rename
from Images_labels_tools.function import images_rename
from Images_labels_tools.video_operate import video_copy_padding
from Images_labels_tools.function import labels_operate
from Images_labels_tools.function import images_test_filter
from Images_labels_tools.data_enhancement import mosaic
from Images_labels_tools.data_enhancement import cutout
from Images_labels_tools.data_enhancement import cutmix
from Images_labels_tools.function import labels_classes_split
from Images_labels_tools.function import labels_file_replace


# def dict_list():
#     list_dict = {
#         '1_图片重命名': images_rename,
#         '2_标签去重': labels_deduplication,
#         '3_标签类别统计': labels_category_statistics,
#         '4_标注框是否超出图片边界检验': labels_testing,
#         '5_图片和标签对照重命名': images_labels_rename,
#         '6_图片和标签对照删除': images_labels_delete,
#         '7_遮盖，需要输入类别': images_cover
#     }
#     return list_dict


@public_function.run_func_time
def run():
    if setting.dict_rename['images_renames']:
        images_rename.start_images_rename()
    if setting.labels_operate['labels_operate']:
        labels_operate.start()
    if setting.labels_split['labels_classes_split']:
        labels_classes_split.start()
    if setting.labels_replace['labels_file_replace']:
        labels_file_replace.start()
    if setting.dict_renames['images_labels_renames']:
        images_labels_rename.images_labels_rename_start()
    if setting.dict_cover['images_covers']:
        images_cover.start_main()
    if setting.images_test['images_test_filter']:
        images_test_filter.start()
    if setting.video_copy_padding['video_copy_padding']:
        video_copy_padding.start()
    if setting.mosaic['mosaic']:
        mosaic.start()
    if setting.cutout['cutout']:
        cutout.start()
    if setting.cut_mix['cut_mix']:
        cutmix.start()
