# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Rockstar He
# Date: 2021-10-09
# Description:

import os
import glob
import numpy as np
import shutil
import argparse
from cv2 import imdecode
from imagesearch.hashing import convert_hash
from imagesearch.hashing import hamming
from imagesearch.hashing import dhash

parser = argparse.ArgumentParser("Get rid of replica images")
parser.add_argument("--target_dir", type=str)
parser.add_argument("-keep_small", action='store_true')
args = parser.parse_args()

def main():
    hashes = []
    num = 0
    target_dir = args.target_dir
    useless_dir = os.path.join(target_dir, "meiyong")
    count = 0
    if not os.path.exists(useless_dir):
        os.makedirs(useless_dir)
    all_files = glob.glob(os.path.join(target_dir, "**"), recursive=True)
    for filename in all_files:
        if os.path.isdir(filename):
            continue
        name = os.path.split(filename)[1]
        file_id, ext = os.path.splitext(name)
        # 0. get rid of non-image files
        if ext == ".exe":
            continue
        elif ext not in [".jpeg", ".png", ".jpg"]:
            print("非图片>>>>>>>>", filename)
            shutil.move(filename, os.path.join(useless_dir, name))
            num += 1
            continue
        
        # 1.get rid of small size pictures
        size = os.path.getsize(filename)
        # 30 KB
        if not args.keep_small and size < 30 * 1024:
            print("文件过小>>>>>>>>", filename)
            shutil.move(filename, os.path.join(useless_dir, name))
            num += 1
            continue
        # 2.get rid of identical pictures
        print(filename)
        image = imdecode(np.fromfile(filename, dtype=np.uint8), 1)
        query = convert_hash(dhash(image))
        # cross check with previous hashes
        if not hashes:
            hashes.append(query)
        else:
            for h in hashes:
                distance = hamming(query, h)
                if distance <= 10:
                    print("重复图片>>>>>>>>", filename)
                    shutil.move(filename, os.path.join(useless_dir, name))
                    num += 1
                    break
            hashes.append(query)
        count += 1
        if count % 100 == 0:
            print(f"{count}/{len(all_files)}")
            
if __name__ == "__main__":
    main()
