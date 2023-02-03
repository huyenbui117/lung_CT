import argparse
from getUID import *
from get_gt import *
from roi2rect import *
from get_data_from_XML import *


def parse_args():
    parser = argparse.ArgumentParser('Annotation Visualization')

    parser.add_argument('--dicom-mode', type=str, default='CT', choices=['CT', 'PET'])
    parser.add_argument('--dicom-path', type=str,
                        help='path to the folder stored dicom files (.DCM)')
    parser.add_argument('--annotation-path', type=str,
                        help='path to the folder stored annotation files (.xml) or a path to a single annotation file')
    parser.add_argument('--classfile', type=str, default='category.txt',
                        help='path to the txt file stored categories')

    return parser.parse_args()


def main():
    args = parse_args()
    class_list = get_category(args.classfile)
    num_classes = len(class_list)
    dict = getUID_path(args.dicom_path)

    if os.path.isdir(args.annotation_path):
        annotations = XML_preprocessor(args.annotation_path, num_classes=num_classes).data
        for k, v in annotations.items():
            # dcm_name = k + '.dcm'
            dcm_path, dcm_name = dict[k[:-4]]
            image_data = v

            if args.dicom_mode == 'CT':
                matrix, frame_num, width, height, ch = loadFile(os.path.join(dcm_path))
                img_bitmap = MatrixToImage(matrix[0], ch)
            elif args.dicom_mode == 'PET':
                img_array, frame_num, width, height, ch = loadFile(dcm_path)
                img_bitmap = PETToImage(img_array, color_reversed=True)

            roi2rect(img_name=dcm_name, img_np=img_bitmap, img_data=image_data, label_list=class_list)

    elif os.path.isfile(args.annotation_path):
        xml_name = args.annotation_path.split('/')[-1]
        # dcm_name = xml_name[:-4] + '.dcm'
        dcm_path, dcm_name = dict[xml_name[:-4]]
        _, image_data = get_gt(os.path.join(args.annotation_path), num_class=num_classes)

        if args.dicom_mode == 'CT':
            matrix, frame_num, width, height, ch = loadFile(os.path.join(dcm_path))
            img_bitmap = MatrixToImage(matrix[0], ch)
        elif args.dicom_mode == 'PET':
            img_array, frame_num, width, height, ch = loadFile(dcm_path)
            img_bitmap = PETToImage(img_array, color_reversed=True)

        roi2rect(img_name=dcm_name, img_np=img_bitmap, img_data=image_data, label_list=class_list)


if __name__ == '__main__':
    main()