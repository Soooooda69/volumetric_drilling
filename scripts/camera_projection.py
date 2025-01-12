import math
from argparse import ArgumentParser
import numpy as np
import ruamel.yaml

yaml = ruamel.yaml.YAML()
yaml.boolean_representation = [u'false', u'true']


if __name__ == '__main__':

    word_adf = '../ADF/world/world.yaml'
    with open(word_adf, 'r') as f:
            params = yaml.load(f)
            f.close()
    camera = params['main_camera']

    near = camera['clipping plane']['near']
    far = camera['clipping plane']['far']
    width = camera['publish image resolution']['width']
    height = camera['publish image resolution']['height']
    print(width,height)

    # camera intrinsic matrix
    K = np.load('/home/shc/Twin-S/params/zed_M_l.npy')
    print(K)
    # K[0, 2] = 900
    K[0, 2] = 922
    K[0, 0] = 1.02*K[0, 0]
    K = K/3

    depth = far - near
    p_M = np.zeros([4,4])
    p_M[0, 0] = 2*K[0,0]/width
    p_M[0, 2] = (width - 2*K[0,2])/width
    p_M[1, 1] = 2*K[1,1]/height
    p_M[1, 2] = (-height + 2*K[1,2])/height
    p_M[2, 2] = (-far - near)/depth
    p_M[2, 3] = -2*(far*near)/depth
    p_M[3, 2] = -1

    print(p_M)