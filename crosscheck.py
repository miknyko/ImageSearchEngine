import pickle


if __name__ == '__main__':
    hashes = pickle.loads(open("hashes.pickle",'rb').read())

    for imagepath in hashes.values():
        if len(imagepath) >1:
            print(imagepath)
    