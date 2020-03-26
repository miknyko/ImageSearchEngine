from imagesearch.hashing import convert_hash
from imagesearch.hashing import dhash
from imutils import paths
import argparse
import pickle
import time
import cv2
import numpy as np
import datetime


ap = argparse.ArgumentParser()
ap.add_argument("-t", "--tree", required=False, type=str,
	help="path to pre-constructed VP-Tree")
ap.add_argument("-a", "--hashes", required=False, type=str,
	help="path to hashes dictionary")
ap.add_argument("-q", "--query", required=False, type=str,
	help="path to input query image")
ap.add_argument("-d", "--distance", type=int, default=6,
	help="maximum hamming distance")
ap.add_argument("-cc", "--crosscheck", type = str,default='False',
	help="if cross check the database")
ap.add_argument("-cp", "--crosscheckpath", type=str,default='标书图片\\',
	help="the path to group images")
args = ap.parse_args()

def test():
    print('[INFO] load vp tree and hashes..')
    tree = pickle.loads(open("vptree.pickle",'rb').read())
    hashes = pickle.loads(open("hashes.pickle",'rb').read())

    image = cv2.imdecode(np.fromfile(args.query,dtype = np.uint8),-1)
    cv2.imshow('Query',image)

    queryHash = dhash(image)
    queryHash = convert_hash(queryHash)
    
    print('[INFO] performing search..')
    start = datetime.datetime.now()
    res = tree.get_all_in_range(queryHash,args.distance)
    res = sorted(res)
    end = datetime.datetime.now()
    print(f'[INFO] search took {end - start}')

    for (d,h) in res:
        resultPath = hashes.get(h,[])
        print(f'[INFO] {len(resultPath)} total images with distance : {d},hash : {h}')
        for path in resultPath:
            res = cv2.imdecode(np.fromfile(path,dtype = np.uint8),-1)
            cv2.imshow('result',res)
            cv2.waitKey(0)

def cross_check():
    print('[INFO] load vp tree and hashes..')
    tree = pickle.loads(open("vptree.pickle",'rb').read())
    hashes = pickle.loads(open("hashes.pickle",'rb').read())

    img_list = list(paths.list_images(args.crosscheckpath))
    start = datetime.datetime.now()
    i = 0
    similar_images = {}
    for imgPath in img_list:
        try:
            image = cv2.imdecode(np.fromfile(imgPath,dtype = np.uint8),-1)
            queryHash = dhash(image)
            queryHash = convert_hash(queryHash)
            res = tree.get_all_in_range(queryHash,args.distance)
            res = sorted(res)
            
            for (d,h) in res:
                if d != 0:
                    v = similar_images.get(imgPath,[])
                    v.append((d,hashes.get(h,[])))
                    similar_images[imgPath] = v
            i += 1
            print(f'[INFO] {i}/{len(img_list)} images has been checked')
        except:
            continue
    end = datetime.datetime.now()
    
    print(f'[INFO] it took {end - start} to check {i} images\n')
    print(f'[INFO] {len(img_list) - i} images falied to check\n')
    # print(f'[INFO] {(end - start)/i} per image')

    with open('crosscheck.pickle','wb') as f:
        f.write(pickle.dumps(similar_images))


if __name__ == '__main__':
    cross_check()
        

    # test()

    
    
