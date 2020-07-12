import os
import hashlib
import itertools

def getHashContent(path):
    """ Get hash of the content of a file
            :param path (string): the path to the file
            :return (string): the hash (hexadecimal) of the whole content """
    chunk_size = 1024
    with open(path, 'rb') as input_file:  # md5 works with binary encoding ("rb")
        md5 = hashlib.md5()  # md5 is an object that can create a hash
        chunk = input_file.read(chunk_size)
        while len(chunk) > 0:
            md5.update(chunk)  # update the hash object with the string argument
            chunk = input_file.read(chunk_size)  # read next chunk
        return md5.hexdigest()


def getDupsPaths(path):
    """ Get duplicated file paths
            :param path (string): the path to the folder
            :return (dict): {content_hash:[file_path]} """
    duplicates = {}
    for dirName, childDir, files in os.walk(path):  # get a tuple with the path values
        for filename in files:
            file_path = os.path.join(dirName, filename)  # get the full path to the file
            hash_of_content = getHashContent(file_path)
            if hash_of_content in duplicates:
                duplicates[hash_of_content].append(file_path)
            else:
                duplicates[hash_of_content] = [file_path]  # hash - key, file path - value
    return duplicates


def findDupsInFolder(path):
    """ Finds files that have a duplicate in the folder's tree
            :param path (string): the path to the folder
            :return (list): list of duplicated file paths """
    duplicates_dict = getDupsPaths(path)
    dups_list = []
    for key, value in duplicates_dict.items():
        if len(value) > 1:  # if there are duplicates
            dups_list.append(value)  # add the duplicates to the dups list
    if len(dups_list) == 0:
        print("No duplicated files found")
    return list(itertools.chain.from_iterable(dups_list))  # destruct: list of lists of paths -> list of paths


print(findDupsInFolder(r"ContainsDups"))
