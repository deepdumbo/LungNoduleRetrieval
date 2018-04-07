from glob import glob
import pickle
import numpy as np


class Weights(object):

    def __init__(self, pre):
        self.weightsTemplate = 'output/Weights/w_{}{{}}_{{}}-{{}}-{{}}.h5'.format(pre)

    def read(self, run=None, epoch=None):
        match = self.weightsTemplate.format(run,epoch,'*','*')
        return open(glob(match)[0], 'br')

    def write(self, run=None, epoch=None, loss=None, val_loss=None):
        match = self.weightsTemplate.format(run, epoch, loss, val_loss)
        return open(match, 'bw')

    def name(self, run=None, epoch=None, loss=None, val_loss=None):
        if (run is None) or (epoch is None):
            return None

        name = None
        if (loss is None) or (val_loss is None):
            while (name is None) and (epoch >= 0):
                if isinstance(epoch, str):
                    match = self.weightsTemplate.format(run, epoch, '*', '*')
                    files = glob(match)
                    if len(files):
                        name = files[0]
                    else:
                        assert False
                else:
                    match = self.weightsTemplate.format(run, '{:02d}'.format(epoch), '*', '*')
                    files = glob(match)
                    if len(files):
                        name = files[0]
                    else:
                        epoch -= 1
        else:
            name = self.weightsTemplate.format(run, epoch, loss, val_loss)

        return name

    __call__ = name


class Embed(object):

    def __init__(self, pre):
        self.weightsTemplate = './output/embed/embed_{}{{}}_{{}}.p'.format(pre)

    def read(self, run=None, dset=None):
        match = self.weightsTemplate.format(run, dset)
        filelist = glob(match)
        if len(filelist) == 0:
            print("Failed to find: {}".format(match))
            return None
        return open(filelist[0], 'br')

    def load(self, run=None, dset=None):
        embed, epochs, meta, images, classes, labels, masks = pickle.load(self.read(run=run, dset=dset))
        return embed, epochs, meta, images, classes, labels, masks

    def write(self, run=None, epoch=None, dset=None):
        match = self.weightsTemplate.format(run, epoch, dset)
        return open(match, 'bw')

    def name(self, run=None, epoch=None,  dset=None):
        return self.weightsTemplate.format(run, epoch, dset)

    __call__ = name


class Pred(object):
    def __init__(self, type, pre):
        self.manager = Embed('')
        if type == 'rating':
            self.manager.weightsTemplate = './output/embed/predR_{}{{}}_E{{}}_{{}}.p'.format(pre)
        elif type == 'malig':
            self.manager.weightsTemplate = './output/embed/pred_{}{{}}_E{{}}_{{}}.p'.format(pre)
        else:
            print("{} - illegal pred type".format(type))
            assert(False)

    def read(self, run=None, dset=None):
        return self.manager.read(run, dset)

    def load(self, run=None, dset=None):
        return self.manager.load(run, dset)

    def write(self, run=None, dset=None):
        return self.manager.write(run, dset)

    def name(self, run=None, dset=None):
        return self.manager.name(run, dset)

    __call__ = name