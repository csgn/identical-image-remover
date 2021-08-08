import os
import sys
import shutil
import imagehash

from pathlib import Path
from PIL import Image

colors = {
    "r": '\033[31m',
    "endc": '\033[m',
    "g": '\033[32m',
    "y": '\033[33m',
    "b": '\033[34m'
}


def cprint(text: str, color: str = 'g'):
    if color == 'r':
        status = '🔴 '
    elif color == 'y':
        status = '🟡️ '
    elif color == 'b':
        status = '🔵️ '
    else:
        status = '🟢 '

    print(f"{colors[color]} {status} {text} {colors['endc']}\n")


def cls():
    command = 'cls' if os.name in ('nt', 'dos') else 'clear'
    os.system(command)


def get_images(target_dir):
    try:
        return sorted(list(filter(lambda img: not Path(img).is_dir(), map(
            lambda img: f"{target_dir}/{img}", os.listdir(target_dir)))))
    except:
        cprint(f"{target_dir} was not found.", 'r')
        sys.exit(1)


def to_f(path):
    return path.split('/')[-1]


def to_p(p):
    return Path(p)


def analyze(images, target_dir):
    temp_images_dir = target_dir.joinpath("temp")

    if not os.path.exists(temp_images_dir):
        os.mkdir(temp_images_dir)
        cprint(f"{temp_images_dir} was created.", 'y')

    p_i = 0
    counter = 0

    hashmap = {}

    while p_i < len(images):
        s_i = p_i + 1

        while s_i < len(images):
            p_img = images[p_i]
            s_img = images[s_i]

            cprint(f"'{to_f(p_img)}' is being compared '{to_f(s_img)}'", 'b')

            if to_f(p_img) not in hashmap:
                hashmap[to_f(p_img)] = imagehash.average_hash(
                    Image.open(p_img))

            if to_f(s_img) not in hashmap:
                hashmap[to_f(s_img)] = imagehash.average_hash(
                    Image.open(s_img))

            conv__p_img = hashmap[to_f(p_img)]
            conv__s_img = hashmap[to_f(s_img)]

            if conv__p_img == conv__s_img:
                cprint(f"{to_f(p_img)} and {to_f(s_img)} are the same.", 'y')

                shutil.move(s_img, f"{temp_images_dir}/{to_f(s_img)}")
                cprint(f"{to_f(s_img)} was moved to {temp_images_dir}")
                del images[s_i]
                del hashmap[to_f(s_img)]
                counter += 1
            else:
                cprint(f"{to_f(p_img)} and {to_f(s_img)} are different.", 'y')
                s_i += 1

            print('⊢' + 70*'-' + '⊣', end='\n')
        del images[p_i]

    cprint(f"{counter} images was removed.", 'y')


def main(args):
    cls()

    try:
        TARGET_DIR = Path(args[1])
    except:
        cprint(
            "Please enter target directory.\n\tusage: python3 remover.py <TARGET_DIRECTORY>", 'r')
        sys.exit(1)

    if not TARGET_DIR.exists():
        cprint(f"{TARGET_DIR} was not found.", 'r')
        sys.exit(1)
    else:
        cprint(f"{TARGET_DIR} was found.", 'g')

    images = get_images(TARGET_DIR)
    cprint(f"{len(images)} images was found.", 'g')

    if len(images) == 0:
        cprint(f"{TARGET_DIR} is empty.", 'r')
    else:
        analyze(images, TARGET_DIR)

    return True


if __name__ == '__main__':
    main(sys.argv)
