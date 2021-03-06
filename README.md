# PyGPNeural

Neural computations represented in python and OpenCL.

Currently still in development.

1. [Showcase](#showcase)
    1. [PyGPRetina](#pygpretina)
        1. [Checkerboard Illusion](#checkerboard-illusion)
        2. [Pac Man Illusion](#pac-man-illusion)
2. [Installation Instructions](#installation-instructions)
    1. [Windows](#installing-on-windows)
        1. [Quick start](#quick-start-windows)
        2. [Prerequisites](#prerequisites-windows)
        3. [Recommendations](#recommendations-windows)
        4. [Installing this Repository](#installing-this-repository-windows)
    2. [Linux](#installing-on-linux)
        1. [Quick start](#quick-start-linux)
        2. [Prerequisites](#prerequisites-linux)
        3. [Recommendations](#recommendations-linux)
        4. [Installing this Repository](#installing-this-repository-linux)

# Showcase

## PyGPRetina

The PyGPRetina subtree preforms approximately the same transformations the RGC cells in the human eye do. Effort was made to keep the transforms operating in real time.

### Checkerboard Illusion

Here, we can see the edge detector succumbing to the checkerboard illusion. Despite that connector being the same color, it says it's brighter than its surroundings when outside of the shadow, and darker than its surroundings when inside the shadow.

[![Image of computer succumbing to the checkerboard illusion.](https://thumbs.gfycat.com/MerryVibrantBasilisk-size_restricted.gif)](https://gfycat.com/MerryVibrantBasilisk)

### Pac Man Illusion

Here, the time averaging filter is used in addition to the relative color filter so that the pac man filter works just like it would with any human.

[![Image of computer succumbing to the pac man illusion.](https://thumbs.gfycat.com/WanWastefulBarnswallow-size_restricted.gif)](https://gfycat.com/WanWastefulBarnswallow)

The feed of the 'burned in' image from staring at the screen for so long is next:

![Image of pac man illusion with no dot removed.](https://i.imgur.com/Zdpd6Kj.png)

That took a minute or two to build up, so the video feed looked just like that image.

It was weird. I would check back after a while and see a different image, but I couldn't see it changing at all.

# Installation Instructions

## Installing on Windows

### Quick start (Windows)

1. Install [Git](https://git-scm.com/)
2. Install [Anaconda with Python 3.6](https://www.anaconda.com/download/)
3. Run these commands from the terminal:

In the directory where you want this repository to show up, run:

    conda create --name pyneural
    activate pyneural
    conda install -c conda-forge opencv pyopencl numpy pytest pip
    pip install pubsub pytube

    git clone https://github.com/PyGPAI/PyGPNeural.git PyGPNeural
    cd PyGPNeural`

    pytest pygp_v1

### Prerequisites (Windows)

To install this repository for development, first, you mast have the following tools installed:

* [Git](https://git-scm.com/), the repository system needed to download this repository.

* Python. However, I recommend [Anaconda with Python 3.6](https://www.anaconda.com/download/), though you can also use 2.7 if you want, for now

* OpenCL. You'll need to install an OpenCL driver. If you have AMD, try here: https://support.amd.com/en-us/kb-articles/Pages/OpenCL2-Driver.aspx
    * If you get `from pyopencl._cffi import ffi as _ffi
ImportError: DLL load failed: The specified procedure could not be found.` It's most likely because you don't have an OpenCL driver.
    * If there is no OpenCL driver for your system, use `conda install pocl` to run things off of the CPU.

Once that's installed, you'll want to create an environment which you'll be developing in, and switch to it. (The quotes aren't necessary as long as there aren't spaces in the name)

`conda create --name 'YOUR ENVIRONMENT NAME'`
`activate 'YOUR ENVIRONMENT NAME'`

Then, you need to install all the libraries from your terminal:

* PIP, the python package install. It's a recursive acronym, by the way, "Pip Installs Packages": `conda install pip`

* PubSub, a simple publisher subscriber library within one process, to make code a little cleaner and to work well with ROS: `pip install pubsub`

* cv2, OpenCV's python computer vision library: `conda install opencv`

    * NOTE: For people with 64-bit python (Default for Anaconda, it seems), you might need to install it this way:
        * Go to the page for [unnoficial precompiled python binaries](https://www.lfd.uci.edu/~gohlke/pythonlibs/#opencv) and download opencv 3.4 for Python36, amd64.
        * Move your terminal to the directory where you have the downloaded .whl file, or move the .whl file to the directory.
        * Run `pip install 'THE FILENAME'`

* pyopencl, a library for running OpenCV code from python: `conda install pyopencl`

* numpy, a library for representing matrices in python. `conda install numpy`

* pytest, a python package for finding and running python unittests. `conda install pytest`

### Recommendations (Windows)

These aren't completely necessary for running and developing things, but they make it a lot easier:

1. [Pycharm](https://www.jetbrains.com/pycharm/). It's a pretty good Python IDE.
2. [OpenSCAD](http://www.openscad.org/downloads.html). We have't started developing physical systems yet, but this seems like a fairly good system even when compared with Solidworks.

### Installing this Repository (Windows)

For now, everything is still in development except for cv_pubsubs, which can be installed from pip.

For everything else, you should open your terminal where you want the code, and then from within that directory, run:

`git clone https://github.com/PyGPAI/PyGPNeural.git 'DESIRED FOLDER NAME'`

3. To run this program, run pytest on, or use pycharm to run, any of the interactive tests under any folder named 'tests interactive'. For files still in development (they'll have _dev in their name), simply run the program like normal.

Simply run this from the top level directory:

`pytest 'DESIRED SUB-REPOSITORY'`

## Installing on Linux

### Quick start (Linux)

1. Install [Anaconda with Python 3.6](https://www.anaconda.com/download/)
2. Run these commands from the terminal:

In the directory where you want this repository to show up, run:

    conda create --name pyneural
    conda activate pyneural
    conda install --channel loopbio --channel conda-forge --channel pkgw-forge gtk2 ffmpeg gtk2-feature opencv pyopencl numpy pytest pip
    pip install pubsub pytube

    git clone https://github.com/PyGPAI/PyGPNeural.git PyGPNeural &&\
    cd PyGPNeural

    pytest pygp_v1

### Prerequisites (Linux)

To install this repository for development, first, you mast have the following tools installed:

* Git, the repository system needed to download this repository: run `sudo apt install git`

* Python. However, I recommend [Anaconda with Python 3.6](https://www.anaconda.com/download/), though you can also use 2.7 if you want, for now. If you need help, follow the [installation instructions on the Anaconda site](https://docs.anaconda.com/anaconda/install/linux).

* OpenCL Driver.
    * If you're getting `pyopencl.cffi_cl.LogicError: clGetPlatformIDs failed: <unknown error -1001>`, that means you don't have any OpenCL compatible devices, or that your drivers aren't updated. Try `sudo apt install mesa-opencl-icd`. If that fails, try `conda install pocl` for the CPU version, or see if you can find other drivers.
    * [Here](https://documen.tician.de/pyopencl/misc.html#installation) is a good tutorial for correctly installing PyOpenCL

Once that's installed, you'll want to create an environment which you'll be developing in, and switch to it. (The quotes aren't necessary as long as there aren't spaces in the name)

`conda create --name 'YOUR ENVIRONMENT NAME'`
`source activate 'YOUR ENVIRONMENT NAME'`

Then, you need to install all the libraries from your terminal:

* PIP, the python package install. It's a recursive acronym, by the way, "Pip Installs Packages": `conda install pip`

* PubSub, a simple publisher subscriber library within one process, to make code a little cleaner and to work well with ROS: `pip install pubsub`

* cv2, OpenCV's python computer vision library: `conda install opencv`

    * Note: when installing on ubuntu for windows, I needed to install libsm6, and then some stuff for X11. I recommend actual ubuntu, but there are ways to run graphical ubuntu applications under windows.

* pyopencl, a library for running OpenCV code from python: `conda install pyopencl`

* numpy, a library for representing matrices in python. `conda install numpy`

* pytest, a python package for finding and running python unittests. `conda install pytest`

### Recommendations (Linux)

These aren't completely necessary for running and developing things, but they make it a lot easier:

1. [Pycharm](https://www.jetbrains.com/pycharm/). It's a pretty good Python IDE.
2. [OpenSCAD](http://www.openscad.org/downloads.html). We have't started developing physical systems yet, but this seems like a fairly good system even when compared with Solidworks:

### Installing this Repository (Linux)

For now, everything is still in development except for cv_pubsubs, which can be installed from pip.

For everything else, you should open your terminal where you want the code, and then from within that directory, run:

`git clone https://github.com/PyGPAI/PyGPNeural.git 'DESIRED FOLDER NAME'`

3. To run this program, run pytest on, or use pycharm to run, any of the interactive tests under any folder named 'tests interactive'. For files still in development (they'll have _dev in their name), simply run the program like normal.

Simply run this from the top level directory:

`pytest 'DESIRED SUB-REPOSITORY'`
