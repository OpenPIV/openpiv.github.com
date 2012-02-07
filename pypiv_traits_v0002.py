# ver. 0002 - start/stop breaks the loop
# need to add some error handling to the rest of the run subroutine
# plans: add hor/vertical treatment, rectangular windows
# add imshow() of the images before the vectors
# 
#! The imports
#!-------------
#!
#! The MPLFigureEditor is imported from last example.

import glob
import os
import csv

from numpy.fft import fftshift, ifft2, fft2
from numpy import savetxt


from threading import Thread
from time import sleep
from enthought.traits.api import *
from enthought.traits.ui.api import View, Item, Group, \
        HSplit, Handler
from enthought.traits.ui.menu import NoButtons
#from mpl_figure_editor import MPLFigureEditor
from scipy import *
from scipy.misc import imread
from scipy.signal.signaltools import medfilt2d
import wx

import matplotlib
# We want matplotlib to use a wxPython backend
matplotlib.use('WXAgg')
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.backends.backend_wx import NavigationToolbar2Wx

from enthought.traits.ui.wx.editor import Editor
from enthought.traits.ui.wx.basic_editor_factory import BasicEditorFactory

# PIV processing subroutines

def readimdir(dirName):
    """ Returns the number of files and file names of BMP/TIF/JPG images in directory """

    known_extensions = ['*.tif','*.bmp','*.jpg']
    for i in known_extensions:
        filenames = glob.glob(os.path.join(os.path.abspath(dirName),i))
        if len(filenames) == 0:
            continue
        else:
            break
        filenames.sort()
    return (filenames, len(filenames))


def read_pair_of_images(image1,image2, crop_vector, itt, spc):
    """ Returns two matrices of intensity values of a pair of PIV images """    
    import scipy.misc.pilutil as im
    A = im.imread(image1,1)/255.0
    B = im.imread(image2,1)/255.0
    sxa,sya = A.shape
    sxb,syb = B.shape
    sx = min(sxa,sxb)
    sy = min(sya,syb)

    l,t,r,b = crop_vector[:] # left, right, top, bottom Number of lines to crop, each of SPC pixels
    
    A  = A[0+t*itt:spc*(sx/spc)-b*itt,0+l*itt:spc*(sy/spc)-r*itt]
    B  = B[0+t*itt:spc*(sx/spc)-b*itt,0+l*itt:spc*(sy/spc)-r*itt]
        
    return A,B


def cross_correlate(a2,b2,NfftH,NfftV=0):
    """ 
        2D cross correlation, mean removed (normalized) 
    """
    if NfftV == 0:
        NfftV = NfftH
    
    a2 -= a2.ravel().mean()
    b2 -= b2.ravel().mean()
    # c = signal.signaltools.correlate2d(a2,b2)
    return fftshift(ifft2(fft2(a2,s=(NfftH,NfftV))*conj(fft2(b2,s=(NfftH,NfftV)))).real,axes=(0,1))



def sub2ind(row,col,i,j):
    """ Converts i,j indices (a list of indices) into a single index vector for .flat (1d) vector """
    # row,col = c.shape
    ind = []
    if len(i) == len(j):
        for k in xrange(len(i)):
            ind.append(i[k]*col + j[k])
    else:
        for k in xrange(len(i)):
            for m in xrange(len(j)):
                ind.append(i[k]*col + j[m])
                
    
    return ind


def ind2sub(row,col,ind):
    """ Converts row,col indices into one index for .flat """
    i = ind/col
    j = ind - i* row
    return i,j    


def find_2Dpeak(c):
    """ Looks for a 2D peak (a mountain peak) in a correlation map """
    i,j = ind2sub(c.shape[0],c.shape[1],argmax(c.flat))
    return i,j

    
def find_displacement(c,s2nm):
    peak1 = max(c.flat)
    # print peak1
    i,j = find_2Dpeak(c)
    row,col = c.shape

    # Temproraly matrix without the maximum peak
    tmp = where(less(c,peak1),c,0)
    

    
    if i == 0 or i == row or j == col or j == 0: 
        peak2 = peak1 # If the peak is on the border, it's out
    else:
        # Look for the Signal-To-Noise ratio by
        if s2nm == 1:       # First-to-second peak ratio
                            # Remove 3x3 pixels neighbourhood around the peak
            tmp[i-1:i+1,j-1:j+1] = 0
            peak2 = max(tmp.flat) # Look for the second highest peak
            x2,y2 = find_2Dpeak(tmp)
            tmp[x2,y2] = 0
            if x2 > 0 and y2 > 0 and x2 < row and y2 < col: # Only if second peak isn't at the borders
                while peak2 < max(ravel(c[x2-1:x2+1,y2-1:y2+1])):
                    # Look for the clear (global) peak, not for a local maximum
                    peak2 = max(tmp.flat)
                    x2,y2 = find_2Dpeak(tmp)
                    if x2 == 0 or y2 == 0 or x2 == row or y2 == col:
                        peak2 = peak1 # will be outlier
                        break
                    tmp[x2,y2] = 0
            else:    
                peak2 = peak1 # second peak is on the border, means "outlier"
        
        elif s2nm == 2: # PEAK-TO-MEAN VALUE RATIO, DEFAULT
            peak2 = mean(fabs(tmp.flat))

    return peak1,peak2,i,j


def sub_pixel_velocity(c,pixi,pixj,peak1,peak2,s2nl,sclt,itt):
    if max(c.flat) < 1e-3: # if it's an empty interrogation window
        peakx = itt
        peaky = itt
        s2n = inf
        return peakx, peaky, s2n

    if peak2 < 0:
        s2n = inf         # outlier
    else:
        s2n = peak1/peak2 # signal-to-noise ratio

    if s2n < s2nl:
        peakx = itt
        peaky = itt
    else:
        try: # 2D Gaussian
            f0 = log(c[pixi,pixj])
            f1 = log(c[pixi-1,pixj])
            f2 = log(c[pixi+1,pixj])
            peakx = pixi + (f1-f2)/(2*f1-4*f0+2*f2)
            f0 = log(c[pixi, pixj])
            f1 = log(c[pixi, pixj-1])
            f2 = log(c[pixi, pixj+1])
            peaky = pixj + (f1-f2)/(2*f1-4*f0+2*f2)
        except:
            peaky = peakx = itt # outlier
            

    if iscomplex(peakx) or iscomplex(peaky):
        peakx = itt
        peaky = itt

    return peakx, peaky, s2n


#def quiverm(res,a,resRows,resCols,scalearrows=1000.0):
#    ax = self.figure.axes[0]
#    self.imshow(a,cmap=p.cm.gray,alpha=0.7)
#    ax.set_ylim((max(res[:,1])+16,0)) # reverse axis for the image
#    hold(True)
#    quiver(reshape(res[:,0],(resRows,resCols)),\
#           reshape(res[:,1],(resRows,resCols)),\
#           reshape(res[:,2],(resRows,resCols)),\
#           reshape(res[:,3],(resRows,resCols)))#,scale=scalearrows)
##    show()


class _MPLFigureEditor(Editor):

    scrollable  = True

    def init(self, parent):
        self.control = self._create_canvas(parent)
        self.set_tooltip()
        
    def update_editor(self):
        pass

    def _create_canvas(self, parent):
        """ Create the MPL canvas. """
        # The panel lets us add additional controls.
        panel = wx.Panel(parent, -1, style=wx.CLIP_CHILDREN)
        sizer = wx.BoxSizer(wx.VERTICAL)
        panel.SetSizer(sizer)
        # matplotlib commands to create a canvas
        mpl_control = FigureCanvas(panel, -1, self.value)
        sizer.Add(mpl_control, 1, wx.LEFT | wx.TOP | wx.GROW)
        toolbar = NavigationToolbar2Wx(mpl_control)
        sizer.Add(toolbar, 0, wx.EXPAND)
        self.value.canvas.SetMinSize((10,10))
        return panel

class MPLFigureEditor(BasicEditorFactory):

    klass = _MPLFigureEditor

#! User interface objects
#!------------------------
#!
#! These objects store information for the program to interact with the
#! user via traitsUI.

class Experiment(HasTraits):
    """ Object that contains the parameters that control the experiment, 
        modified by the user.
    """
#    width = Float(30, label="Width", desc="width of the cloud")
#    x = Float(50, label="X", desc="X position of the center")
#    y = Float(50, label="Y", desc="Y position of the center")
    dir_name = Directory('C:\Python25\user\pypiv\images4',label="Images path")
    
    ittx = Enum(32,8,16,32,64,128,256,label="ITT x", desc="Interrogation window width in pixels")
    itty = Enum(32,8,16,32,64,128,256,label="ITT y", desc="Interrogation window height in pixels")
    spacing_X = Enum(32,8,16,32,64,128,256,label="Spacing X", desc="shift aside in pixels")
    spacing_Y = Enum(32,8,16,32,64,128,256,label="Spacing Y", desc="shift down in pixels")
    S2N_Type = Enum(1,2,label="S/N type",desc="Signal-to-Noise type: choose 1 for 2nd peak or 2 - peak-to-mean")
    S2N_Value = Int(1,label="S/N value")
    scale = Float(1.0,label="Scaling",desc="pixel/mm x dt/sec")
    Outlier_Filter = Int(100)
    jump = Int(1)
    select_roi = Button("Select Region-of-Interest(ROI)")
    reset_roi = Button("RESET ROI")
    
    def acquire(self):
        self.fNames,self.numOfFiles = readimdir(self.dir_name)
        return self.fNames, self.numOfFiles

    
#! Threads and flow control
#!--------------------------
#!
#! There are three threads in this application:
#! 
#!  * The GUI event loop, the only thread running at the start of the program.
#!
#!  * The acquisition thread, started through the GUI. This thread is an
#!    infinite loop that waits for the camera to be triggered, retrieves the 
#!    images, displays them, and spawns the processing thread for each image
#!    recieved.
#!
#!  * The processing thread, started by the acquisition thread. This thread
#!    is responsible for the numerical intensive work of the application.
#!    it processes the data and displays the results. It dies when it is done.
#!    One processing thread runs per shot acquired on the camera, but to avoid
#!    accumulation of threads in the case that the processing takes longer than
#!    the time lapse between two images, the acquisition thread checks that the
#!    processing thread is done before spawning a new one.
#! 

    def process(image, results_obj):
        """ Function called to do the processing """
        X, Y = indices(image.shape)
        x = sum(X*image)/sum(image)
        y = sum(Y*image)/sum(image)
        width = sqrt(abs(sum(((X-x)**2+(Y-y)**2)*image)/sum(image))) 
        results_obj.x = x
        results_obj.y = y
        results_obj.width = width
        pypiv_process(self.dir_name)
        return

class AcquisitionThread(Thread):
    """ Acquisition loop. This is the worker thread that retrieves images 
        from the camera, displays them, and spawns the processing job.
    """
    wants_abort = False

    def process(self, image):
        """ Spawns the processing job.
        """
        try:
            if self.processing_job.isAlive():
                self.display("Processing to slow")
                return
        except AttributeError:
            pass
        self.processing_job = Thread(target=process, args=(image,
                                                            self.results))
        self.processing_job.start()

    def run(self):
        """ Runs the acquisition loop.
        """
        self.display('Processing started')
        fNames,numOfFiles =self.acquire()
        self.display("%d files are found " % numOfFiles)
        self.display("ittx is %d" % self.experiment.ittx)
        itt = self.experiment.ittx
        spc = self.experiment.spacing_X
        s2nm = self.experiment.S2N_Type
        s2n = self.experiment.S2N_Value
        sclt = self.experiment.scale
        outl = self.experiment.Outlier_Filter
        jump = self.experiment.jump
        
        
#        for fileind in range(0,numOfFiles,2):
        fileind = 0
        while not self.wants_abort and fileind < numOfFiles:
            
            a,b = read_pair_of_images(fNames[fileind],fNames[fileind+1],([0,0,0,0]),itt,spc)
            sx,sy = a.shape
            Nfft = 2*itt
            resRows = (sx-itt)/spc+1
            resCols = (sy-itt)/spc+1
            res = zeros((resRows*resCols,5))
            counter = 0
            k = 0
#            for k in r_[0:sx-itt+1:spc]:
            while not self.wants_abort and k <= (sx-itt+1):
                self.display("\n Working on %d pixel row "  % k)
                for m in r_[0:sy-itt+1:spc]:
#                    self.display(".")
                    a2 = a[k:k+itt,m:m+itt]
                    b2 = b[k:k+itt,m:m+itt]
                    c = cross_correlate(a2,b2,Nfft) 
                    [peak1,peak2,peakx,peaky] = find_displacement(c,s2nm) # find integer displacement
                    s2n = 1
                    [peakx,peaky,s2n] = sub_pixel_velocity(c,peakx,peaky,peak1,peak2,s2n,sclt,itt)
##              Scale the pixel displacement to the velocity
                    u = (itt-peaky)*sclt
                    v = (itt-peakx)*sclt
                    x = m+itt/2
                    y = k+itt/2
                    res[counter][:] = [x,y,u, v, s2n]
                    counter += 1
                k += spc

# Write unfiltered, raw data
            row,col = shape(res)
#            writer = csv.writer(file(fNames[fileind]+'_noflt.txt','w'),dialect='excel',delimiter='\t')
            savetxt(fNames[fileind][:-4]+'_noflt.txt',res,fmt='%4.3f',delimiter=' ')

#            for i in xrange(row):
#                writer.writerow(res[i][:])
                

        # Find outliers
            uMag = (res[:,2]**2 + res[:,3]**2)**0.5
            limit = mean(compress(uMag!=0,uMag))*outl
            filtres = res.copy()
            u = filtres[:,2].copy()
            v = filtres[:,3].copy()
            u = choose(uMag > limit,(u,0))
            v = choose(uMag > limit, (v,0))
        

        # Median filter
            tmpu = fabs(ravel(medfilt2d(reshape(u,(resRows,resCols)),3)))
            tmpv = fabs(ravel(medfilt2d(reshape(v,(resRows,resCols)),3)))
        
            uLimit = mean(take(tmpu,nonzero(tmpu!=0))) + 3*std(take(tmpu,nonzero(tmpu!=0)))
            vLimit = mean(take(tmpv,nonzero(tmpv!=0))) + 3*std(take(tmpv,nonzero(tmpv!=0)))
    
            u = where(greater(tmpu,uLimit),0,u)
            v = where(greater(tmpv,vLimit),0,v)
    
            filtres[:,2] = u.copy()
            filtres[:,3] = v.copy()
            
            savetxt(fNames[fileind][:-4]+'_flt.txt',filtres,fmt='%4.3f',delimiter=' ')
    
            ind = nonzero(logical_and(u == 0,v == 0))
            indLoop = 0
            while size(ind[0]) > 0: # Loop until no more "holes" are found
                indLoop += 1
                self.display("Interpolation loop %d " % indLoop)
                for i in ind[0]: # find a "hole" (zero), fill with an average of 5 x 5 neighbours
                    x2 = i/resCols
                    y2 = i - x2 * resCols
                    k = r_[maximum(2,x2)-2:minimum(resCols-3,x2)+2]
                    m = r_[maximum(2,y2)-2:minimum(resRows-3,y2)+2]
                    region = sub2ind(resRows,resCols,k,m)
                    tmpu = take(u,region)
                    tmpu = take(v,region)
                    u[i] = mean(tmpu)
                    v[i] = mean(tmpv)
    
                ind = nonzero(logical_and(u == 0,v == 0))
            
            filtres[:,2] = u
            filtres[:,3] = v
            
            savetxt(fNames[fileind][:-4]+'.txt',filtres,fmt='%4.3f',delimiter=' ')
    
            self.quiverm(filtres,a,resRows,resCols,scalearrows=50)
            
            fileind += 2

#        n_img = 0
#        while not self.wants_abort:
#            n_img += 1
#            self.display('%d image captured' % n_img)
#            self.image_show(im1)
#            self.process(img)
#            sleep(1)
#        self.display('Camera stopped')

#! The GUI elements
#!------------------
#!
#! The GUI of this application is separated in two (and thus created by a
#! sub-class of *SplitApplicationWindow*).
#!
#! On the left a plotting area, made of an MPL figure, and its editor, displays
#! the images acquired by the camera.
#!
#! On the right a panel hosts the `TraitsUI` representation of a *ControlPanel*
#! object. This object is mainly a container for our other objects, but it also
#! has an *Button* for starting or stopping the acquisition, and a string 
#! (represented by a textbox) to display informations on the acquisition
#! process. The view attribute is tweaked to produce a pleasant and usable
#! dialog. Tabs are used as it help the display to be light and clear.
#!

class ControlPanel(HasTraits):
    """ This object is the core of the traitsUI interface. Its view is
        the right panel of the application, and it hosts the method for
        interaction between the objects and the GUI.
    """
    experiment = Instance(Experiment, ())
#    camera = Instance(Camera, ())
    figure = Instance(Figure)
#    results = Instance(Results, ())
    start_stop_acquisition = Button("Start/Stop acquisition")
    results_string =  String()
    acquisition_thread = Instance(AcquisitionThread)
    view = View(Group(
                Group(
                  Item('start_stop_acquisition', show_label=False ),
                  Item('results_string',show_label=False, 
                                        springy=True, style='custom' ),
                  label="Control", dock='tab',),
                Group(                  
                  Group(
                    Item(name='experiment',style='custom', show_label=False, width=1, resizable=True),
                    label="PIV processing setup",),
#		          Group(
#                    Item(name='results', style='custom', show_label=False),
#                    label="Results",),
                label='Setup', dock="tab"),
#                Item(name='camera', style='custom', show_label=False,
#                                    dock="tab"),
               layout='tabbed'),
               )

    def _start_stop_acquisition_fired(self):
        """ Callback of the "start stop acquisition" button. This starts
            the acquisition thread, or kills it/
        """
        if self.acquisition_thread and self.acquisition_thread.isAlive():
            self.acquisition_thread.wants_abort = True
        else:
            self.acquisition_thread = AcquisitionThread()
            self.acquisition_thread.display = self.add_line
            self.acquisition_thread.quiverm = self.quiverm
            self.acquisition_thread.acquire = self.experiment.acquire
            self.acquisition_thread.experiment = self.experiment
            self.acquisition_thread.image_show = self.image_show
            self.acquisition_thread.figure = self.figure
            self.acquisition_thread.start()
    
    def add_line(self, string):
        """ Adds a line to the textbox display.
        """
        self.results_string = (string + "\n" + self.results_string)[0:1000]

    def image_show(self, image):
        """ Plots an image on the canvas in a thread safe way.
        """
        self.figure.axes[0].images=[]
        self.figure.axes[0].imshow(image, aspect='auto')
        wx.CallAfter(self.figure.canvas.draw)
        
    def quiverm(self,res,a,resRows,resCols,scalearrows=1000.0):
        """ Plots an image on the canvas in a thread safe way.
        """
#        self.figure.axes[0].images=[]
#        self.figure.axes[0].imshow(image, aspect='auto')
        self.figure.axes[0].imshow(a,cmap=matplotlib.cm.gray,alpha=0.7)
        self.figure.axes[0].set_ylim((max(res[:,1])+16,0)) # reverse axis for the image
        self.figure.axes[0].hold(True)
        self.figure.axes[0].quiver(reshape(res[:,0],(resRows,resCols)),\
                                   reshape(res[:,1],(resRows,resCols)),\
                                   reshape(res[:,2],(resRows,resCols)),\
                                   reshape(res[:,3],(resRows,resCols)),\
                                   color='r')
#,scale=scalearrows)
#    show()
        self.figure.axes[0].hold(False)
        wx.CallAfter(self.figure.canvas.draw)

        
class MainWindowHandler(Handler):
    def close(self, info, is_OK):
        if ( info.object.panel.acquisition_thread 
                        and info.object.panel.acquisition_thread.isAlive() ):
            info.object.panel.acquisition_thread.wants_abort = True
            while info.object.panel.acquisition_thread.isAlive():
                sleep(0.1)
            wx.Yield()
        return True


class MainWindow(HasTraits):
    """ The main window, here go the instructions to create and destroy
        the application.
    """
    figure = Instance(Figure)

    panel = Instance(ControlPanel)

    def _figure_default(self):
        figure = Figure()
        figure.add_axes([0.05, 0.04, 0.9, 0.92])
        return figure

    def _panel_default(self):
        return ControlPanel(figure=self.figure)

    view = View(HSplit(  Item('figure',  editor=MPLFigureEditor(),
                                                        dock='vertical',
                                                        width=800,
                                                        height=600,
                                                        resizable=False),
                        Item('panel', style="custom"),
                    show_labels=False, 
                    ),
                resizable=False, 
                height=0.75, width=0.75,
                handler=MainWindowHandler(),
                buttons=NoButtons,
                title='PyPIV_Traits_UI ver 0.001')
                

if __name__ == '__main__':
    MainWindow().configure_traits()
