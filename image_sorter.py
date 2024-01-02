from PIL import Image
from os import listdir, mkdir, rename
from shutil import move
from imagehash import average_hash
from time import time

'''
ВАЖНО УКАЗАТЬ ОСНОВНУЮ ДИРЕКТОРИЮ И ДВЕ ПОДДИРЕКТОРИИ ДЛЯ РАБОТЫ ПРОГРАММЫ
'''
path_all = ''  # основная директория, например C:\\python\\project_F
path_end = ''  # поддиректория куда сохраняются результаты работы программы, например C:\\python\\project_F\\end_F\\
path_start = ''  # поддиректория откуда программа берет исходные данные, например C:\\python\\project_F\\start_F\\

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

        if is_duplicate:
            duplicate_images.append(image)
        else:
            unique_images.add(image)

    return list(unique_images), duplicate_images


def renaming_file(path, fix=False):
    images_r = listdir(path)
    if fix:
        for i in images_r:
            if i[5:6] == '_':
                rename(path_end + i, path_end + f'{i[0:5]}.jpg')
    else:
        for i in images_r:
            try:
                rename(path + i, path + f'art_{images_r.index(i)}.jpg')
            except FileExistsError:
                rename(path + i, path + f'art_{images_r.index(i)}_.jpg')


def to_del(path, path_start_0, images_to_del):
    try:
        mkdir(path + '\\to_del')  # создается поддиректория куда будут перемещены повторяющиеся изображения
    except FileExistsError:
        pass

    if len(images_to_del) == 0:
        print('Для программы утилизации нет данных на входе')
        return 0
    for i in images_to_del:
        try:
            move(path_start_0 + i, path + '\\to_del')
        except:
            rename(path_start_0 + i, path_start_0 + '_' + i)
            move(path_start_0 + '_' + i, path + '\\to_del')
        print(f'[+] Файл " {i} " был определён как копия')


def os_manager(path_start_1, path_end_1, img, key=False):
    if key:
        for i in images_end:
            move(path_end_1 + i, path_start_1)
        print('[+] Завершена первая часть работы программы\n'
              'Запустите программу повторно изменив параметр " key " функции " os_manager "')
        return True

    clean_list_f = sort(img)[0]

    print(f'[+] Выполняется функция менеджмента файлов ....')

    for i in clean_list_f:
        move(path_start_1 + i, path_end_1)
        print(f'[+] Файл " {i} " был определён как уникальный')

    renaming_file(path_end_1)
    renaming_file(path_end_1, True)


if __name__ == '__main__':
    try:
        key = False
        os_manager(path_start, path_end, images, key)
        '''
        key=False если в поддиректории куда сохраняются результаты работы программы (path_end) нет файлов
        key=True если в обеих поддиректориях есть файлы
        '''
        if not key:
            to_del(path_all, path_start, images)
    except IndexError:
        print('Ошибка, нет данных на входе')
