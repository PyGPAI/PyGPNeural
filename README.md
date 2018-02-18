# PyGPNeural

Neural computations represented in python and OpenCL.

Currently still in development.

1. [Showcase](#showcase)
    1. [PyGPRetina](#pygpretina)
        1. [Checkerboard Illusion](#checkerboard-illusion)
        2. [Pac Man Illusion](#pac-man-illusion)
2. [Installation Instructions](#installation-instructions)
    1. [Installing on Windows](#installing-on-windows)
    2. [Prerequisites (Windows)](#prerequisites-windows)
    3. [Recommendations (Windows)](#recommendations-windows)
    4. [Installing this Repository (Windows)](#installing-this-repository-windows)
    5. [Quick start (Windows)](#quick-start-windows)

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

### Prerequisites (Windows)

To install this repository for development, first, you mast have the following tools installed:

* [Git](https://git-scm.com/), the repository system needed to download this repository.

* Python. However, I recommend [Anaconda with Python 3.6](https://www.anaconda.com/download/), though you can also use 2.7 if you want, for now

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

### Quick start (Windows)

1. Install [Git](https://git-scm.com/)
2. Install [Anaconda with Python 3.6](https://www.anaconda.com/download/)
3. Run these commands from the terminal:

In the directory where you want this repository to show up, run:

    conda create --name pyneural
    activate pyneural
    conda install pip
    pip install pubsub
    conda install opencv
    conda install pyopencl
    conda install numpy
    conda install pytest

    git clone https://github.com/PyGPAI/PyGPNeural.git PyGPNeural
    cd PyGPNeural`

    pytest pygp_v1