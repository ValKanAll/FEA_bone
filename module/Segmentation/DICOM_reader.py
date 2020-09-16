import pydicom as dicom
import cv2
import matplotlib.pylab as plt
from mpl_toolkits.mplot3d import axes3d, Axes3D

import os, glob
import numpy as np
try:
    import Tkinter as tk
    from Tkinter import ttk
# Fall back to Python 3 if import fails
except ImportError:
    import tkinter as tk
    from tkinter import ttk

from tkinter import filedialog


class IndexTracker(object):
    def __init__(self, ax, X, pos):
        self.ax = ax
        #ax.set_title('Scroll to Navigate through the DICOM Image Slices')

        self.X = X
        self.pos = pos

        if self.pos == 2:
            rows, cols, self.slices = X.shape
            self.ind = self.slices // 2
            self.im = ax.imshow(self.X[:, :, self.ind])
        elif self.pos == 1:
            rows, self.slices, cols = X.shape
            self.ind = self.slices // 2
            self.im = ax.imshow(self.X[:, self.ind, :].T)
        elif self.pos == 0:
            self.slices, rows, cols = X.shape
            self.ind = self.slices // 2
            self.im = ax.imshow(self.X[self.ind, :, :].T)
        else:
            return "pos should be 0, 1 or 2"
        self.update()

    def onscroll(self, event):
        print("%s %s" % (event.button, event.step))
        if event.button == 'up':
            self.ind = (self.ind + 1) % self.slices
        else:
            self.ind = (self.ind - 1) % self.slices
        print('Slice Number: %s' % self.ind)
        self.update()

    def update(self):
        if self.pos == 2:
            self.im.set_data(self.X[:, :, self.ind])
        elif self.pos == 1:
            self.im.set_data(self.X[:, self.ind, :].T)
        elif self.pos == 0:
            self.im.set_data(self.X[self.ind, :, :].T)
        else:
            return "pos should be 0, 1 or 2"

        self.ax.set_ylabel('Slice Number: %s' % self.ind)
        self.im.axes.figure.canvas.draw()


class Dicom:
    def __init__(self, dicom_path='', initial_dir=''):
        self.path = dicom_path
        self.dataset = ''
        if not initial_dir:
            self.initial_dir = os.getcwd()
        else:
            self.initial_dir = initial_dir
        if self.path:
            self.dataset = dicom.dcmread(self.path)
            self.pixel_array = self.dataset.pixel_array

    def dataset(self):
        return self.dataset

    def find_path(self):
        self.path = filedialog.askopenfilename(initialdir=self.initial_dir, title="Select file",
                                               filetypes=(("DICOM", "*.dcm"), ("all files", "*.*")))
        self.dataset = dicom.dcmread(self.path)
        self.pixel_array = self.dataset.pixel_array

    def quick_show(self):
        plt.imshow(self.pixel_array)

    def save_as(self, format='.png', new_path=''):
        if not new_path:
            image_format = format
            image_path = self.path.replace('.dcm', image_format)
        if new_path:
            image_path=new_path
        cv2.imwrite(image_path, self.pixel_array)

    def show(self):
        fig, ax = plt.subplots(1, 1)

        plots = []
        slices = []
        skipcount = 0

        folder_path = self.path[:-len(self.path.split("/")[-1])]
        dcm_path = folder_path + '*.dcm'

        os.chdir(folder_path)
        for file in glob.glob(dcm_path):
            filename = file.split("/")[-1]
            dataset = dicom.dcmread(filename)
            pix = dataset.pixel_array
            #pix = pix*1+(-1024)
            plots.append(pix)
            # skip files with no SliceLocation (eg scout views)
            if hasattr(dataset, 'SliceLocation'):
                slices.append(dataset)
            else:
                skipcount = skipcount + 1

        # ensure they are in the correct order
        slices = sorted(slices, key=lambda s: s.SliceLocation)

        # pixel aspects, assuming all slices are the same
        ps = slices[0].PixelSpacing
        ss = slices[0].SliceThickness
        ax_aspect = ps[1] / ps[0]
        sag_aspect = ps[1] / ss
        cor_aspect = ss / ps[0]

        # rescale values to HU
        RI = float(self.dataset.RescaleIntercept)
        RS = float(self.dataset.RescaleSlope)

        # create 3D array
        img_shape = list(slices[0].pixel_array.shape)
        img_shape.append(len(slices))
        img3d = np.zeros(img_shape)
        img3d_thresh_x = []
        img3d_thresh_y = []
        img3d_thresh_z = []
        thresh = 1000

        # fill 3D array with the images from the files
        for i, s in enumerate(slices):
            img2d = s.pixel_array*RS+RI
            for j in range(img_shape[0]):
                for k in range(img_shape[1]):
                    value = img2d[j, k]
                    if value >= thresh:
                        img3d_thresh_x.append(cor_aspect*j)
                        img3d_thresh_y.append(sag_aspect*k)
                        img3d_thresh_z.append(ax_aspect*i)
            img3d[:, :, i] = img2d

        # locate images
        ax_img = img_shape[2]//2
        sag_img = img_shape[1]//2
        cor_img = img_shape[0]//2

        fig1 = plt.figure(1)

        # plot 3 orthogonal slices
        a1 = plt.subplot2grid((2, 2), (1, 1))
        plt.imshow(img3d[:, :, ax_img])
        a1.set_aspect(ax_aspect)

        a2 = plt.subplot2grid((2, 2), (1, 0))
        plt.imshow(img3d[:, sag_img, :].T)
        a2.set_aspect(sag_aspect)

        a3 = plt.subplot2grid((2, 2), (0, 1))
        plt.imshow(img3d[cor_img, :, :].T)
        a3.set_aspect(cor_aspect)

        plt.subplots_adjust(left=0, bottom=0.05, right=1, top=0.95,
                     wspace=0, hspace=0.2)

        # plot 3D volume
        a0 = fig.add_subplot(2, 2, 1, projection='3d')
        a0.scatter3D(img3d_thresh_x, img3d_thresh_y, img3d_thresh_z, s=1)

        # Scrolling through slices
        tracker1 = IndexTracker(a1, img3d, 2)
        fig1.canvas.mpl_connect('scroll_event', tracker1.onscroll)
        tracker2 = IndexTracker(a2, img3d, 1)
        fig.canvas.mpl_connect('scroll_event', tracker2.onscroll)
        tracker3 = IndexTracker(a3, img3d, 0)
        fig1.canvas.mpl_connect('scroll_event', tracker3.onscroll)

        plt.show()

        '''y = np.dstack(plots)

        tracker = IndexTracker(ax, y)

        fig.canvas.mpl_connect('scroll_event', tracker.onscroll)
        plt.show()'''


if __name__ == "__main__":
    path="/Users/valentinallard/FEA_bone/module/Segmentation/series-00000/image-00000.dcm"
    d=Dicom(path)
    dataset = d.dataset
    print(dataset)
    print(dataset.pixel_array.size)
    #d.find_path()
    d.show()