from imagesearch.hashing import convert_hash
from imagesearch.hashing import hamming
from imagesearch.hashing import dhash
from imutils import paths
import pickle
import vptree
import cv2
import argparse
import datetime
import os
import numpy as np

# construct the arg parser
parser = argparse.ArgumentParser()
parser.add_argument('-i','--images',required = True,type = str,help = '图片存储路径,imagepath')
parser.add_argument('-t','--tree',required = True,type = str,help = 'vp树路径,vptreepath')
parser.add_argument('-a','--hashes',required = True,type = str,help = 'hash值存储路径,imagepath')
args = parser.parse_args()

def hash_all_images(imagePaths):
    """hash all the image in the path
    return:
    hashes : dictionary with hash as the key and the path as the value
    """
    hashes = {}
    for (i,imagePath) in enumerate(imagePaths):
        print(f'[INFO] processing image {i + 1}/{len(imagePaths)}')
        
        # cwd = os.getcwd()
        # print(os.path.join(cwd,imagePath))
        image = cv2.imdecode(np.fromfile(imagePath,dtype = np.uint8),-1)
        try:
            h = dhash(image)
            h = convert_hash(h)
        
            # update the hashes dic
            # in case there are similar images with different path
            l = hashes.get(h,[])
            l.append(imagePath)
            hashes[h] = l
        except :
            continue
    return hashes

def build_vptree(hashes):
    """
    build the vptree acoording to hamming distance
    """
    print('[INFO] building VP-Tree...')
    points = list(hashes.keys())
    tree = vptree.VPTree(points,hamming)
    
    return tree

if __name__ == '__main__':

    now = datetime.datetime.now()
    imagePaths = list(paths.list_images(args.images))
    hashes = hash_all_images(imagePaths)
    tree = build_vptree(hashes)
    then = datetime.datetime.now()

    print(f'[INFO] image process and tree building takes {then - now}')

    # serialize the VP_Tree to disk
    print('[INFO] serializing the VP-Tree...')
    with open(args.tree,'wb') as f:
        f.write(pickle.dumps(tree))
    
    # serialize the hashes to dictionary
    print('[INFO] serializing the hash dictionary')
    with open(args.hashes,'wb') as f:
        f.write(pickle.dumps(hashes))