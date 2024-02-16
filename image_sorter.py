from PIL import Image
from os import listdir, mkdir, rename
from shutil import move
from imagehash import average_hash
from time import time

'''
YOU MUST SPECIFY THE MAIN DIRECTORY AND TWO SUBDIRECTORIES FOR THE PROGRAM TO WORK
'''

path_all = ''  # the main directory, for example C:\\python\\image_sorter
path_end = ''  # the subdirectory where the results of the program are saved, for example C:\\python\\image_sorter\\end_dir\\
path_start = ''  # the subdirectory from where the program takes the source data, for example C:\\python\\image_sorter\\start_dir\\

images = listdir(path_start)
images_end = listdir(path_end)


def difference_images(img1, img2):
    image_1, image_2 = (average_hash(Image.open(f'{path_start}{img1}')),
                        average_hash(Image.open(f'{path_start}{img2}')))
    return True if image_1 == image_2 else False


def sort(images_s):
    unique_images, duplicate_images, count = set(), [], 0
    start_time = time()
    for image in images_s:
        count += 1
        print(f'Progress: {count} of {len(images_s)}')
        print("--- %s seconds ---" % (time() - start_time))
        is_duplicate = any(difference_images(image, unique_image) for unique_image in unique_images)

        duplicate_images.append(image) if is_duplicate else unique_images.add(image)
            
    return list(unique_images), duplicate_images


def renaming_file(path, fix=False):
    images_r = listdir(path)
    if fix:
        for i in images_r:
            if i[-5] == '_':
                rename(path + i, path + f'{i[0:-5]}.jpg')
    else:
        for i in images_r:
            try:
                rename(path + i, path + f'art_{images_r.index(i)}.jpg')
            except FileExistsError:
                rename(path + i, path + f'art_{images_r.index(i)}_.jpg')


def to_del(path, path_start_0, images_to_del):
    try:
        mkdir(path + '\\to_del')  # a subdirectory is created where duplicate images will be moved
    except FileExistsError:
        pass

    if len(images_to_del) == 0:
        print('There is no input data for the recycling program')
        return 0
    else:
        for i in images_to_del:
            move(path_start_0 + i, path + '\\to_del')
            print(f'[+] Файл " {i} " was identified as a copy')
            

def os_manager(path_start_1, path_end_1, img, key=False):
    if key:
        for i in images_end:
            move(path_end_1 + i, path_start_1)
        print('[+] The first part of the program has been completed\n'
              'Run the program again by changing the " key" parameter of the " os_manager" function')
        return True

    clean_list_f = sort(img)[0]

    print(f'[+] The file management function is running ....')

    for i in clean_list_f:
        move(path_start_1 + i, path_end_1)
        print(f'[+] Файл " {i} " was defined as unique')

    renaming_file(path_end_1)
    renaming_file(path_end_1, True)


if __name__ == '__main__':
    try:
        key = False
        os_manager(path_start, path_end, images, key)
        '''
        key=False  if there are no files in the subdirectory where the results of the program are saved (path_end)
        key=True  if there are files in both subdirectories
        '''
        if not key:
            to_del(path_all, path_start, images)
    except IndexError:
        print('Error, there is no input data')
