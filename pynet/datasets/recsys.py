
import logging
logger = logging.getLogger(__name__)
import os
import numpy as np
import theano
import pandas
from pynet.datasets.dataset import SingleBlock, DataBlocks
from onlinebehavior.dataset import Dataset_by_Session
from pynet.utils.utils import make_one_hot

class RecSys(SingleBlock):
    def __init__(self, **kwargs):
        super(RecSys, self).__init__(X=None, y=None, **kwargs)

        csv_path = '/home/wuzz/ihpc/onlinebehavior/sessions.csv'
        data = Dataset_by_Session(csv_path=csv_path, train_valid_test = self.ratio)
        tbl = data.split(features=data.feature, labels=data.label)
        self.set_train(X=tbl['train_fea'], y=make_one_hot(tbl['train_lbl'], 2))
        self.set_valid(X=tbl['valid_fea'], y=make_one_hot(tbl['valid_lbl'], 2))
        self.set_test(X=tbl['test_fea'], y=make_one_hot(tbl['test_lbl'], 2))


class RecSysPosterior(SingleBlock):
    def __init__(self, **kwargs):
        super(RecSysPosterior, self).__init__(X=None, y=None, **kwargs)

        sav_dir = '/home/wuzz/ihpc/dataset/posteriors'

        with open(sav_dir + '/train_y.npy') as train_y_fin:
            train_X = np.load(train_y_fin)
        with open(sav_dir + '/train_lbl.npy') as train_lbl_fin:
            train_y = np.load(train_lbl_fin)
        with open(sav_dir + '/test_y.npy') as test_y_fin:
            test_X = np.load(test_y_fin)
        with open(sav_dir + '/test_lbl.npy') as test_lbl_fin:
            test_y = np.load(test_lbl_fin)

        self.set_train(X=train_X, y=make_one_hot(train_y, 2))
        self.set_valid(X=test_X, y=make_one_hot(test_y, 2))
        self.set_test(X=test_X, y=make_one_hot(test_y, 2))


class RecSysJitter(SingleBlock):
    def __init__(self, **kwargs):
        super(RecSysJitter, self).__init__(X=None, y=None, **kwargs)
        data_dir = '/home/wuzz/recsys2015/data/jitter_stdr0_1_dup_15'
        train = Dataset_by_Session(sort_by_session=False, csv_path=data_dir + '/train_jitter.csv')
        valid = Dataset_by_Session(sort_by_session=False, csv_path=data_dir + '/valid.csv')
        test = Dataset_by_Session(sort_by_session=False, csv_path=data_dir + '/test.csv')
        self.set_train(X=train.feature, y=make_one_hot(train.label,2))
        self.set_valid(X=valid.feature, y=make_one_hot(valid.label,2))
        self.set_test(X=test.feature, y=make_one_hot(test.label,2))
