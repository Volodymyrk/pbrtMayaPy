Welcome to pbrtMayaPy
=============

This is a cross-platform exporter Plugin for Maya that allows you to render your Autodesk Maya scenes using PBRT v2. PBRT is a Physically Based Rendering system that is described in a wonderful book by Matt Pharr and Greg Humphreys: "Physically Based Rendering: From Theory To Implementation".

About
------------
This plugin is based on Python LuxMaya translation by Doug Hammond (https://bitbucket.org/luxrender/luxmaya) , in turn base on translation of the c++ luxmaya exporter, 
in turn based on original maya-pbrt c++ exporter by Mark Colbert (http://graphics.cs.ucf.edu/mayapbrt/index.php).

The purpose of this plugin is to allow the reader of "Physically Based Rendering: From Theory To Implementation" book to work with the system from Maya.

Therefore, pbrtMayaPy is written with three principles in mind:
* Completeness. Comprehensive coverage of most features of PBRT
* The user is technically-savvy. She is capable to enter PBRT commands to access all features of the renderer inside a text box.
* Simplicity. The system has a simple and modular design, so new exporter features should be easy to add by a Python-

Requirements
------------
* Autodesk Maya for Windows, Mac or Linux
* A working copy of PBRT Open-Source renderer

Installation
-------------

1. Get the source by pressing "Download ZIP" on the right (or by cloning
this repository). Unzip in the folder of your choice, e.g.: $HOME/youMayaStuff/pbrtMayaPy/ 

2. Download and compile PBRT from http://pbrt.org/downloads.php

3. Set the following Environment variables (you can add the following to your Maya.env):
* MAYA_PLUG_IN_PATH = $HOME/youMayaStuff/pbrtMayaPy/
* PBRT_SEARCHPATH = $HOME/youMayaStuff/pbrt-v2/Build/Products/Release/

3. Load the plugin in Maya using Plug-in Manager

3. Press "Export and Render" from the top menu or execute MEL: pbrt_export



Useful links
-------------

* http://pbrt.org/downloads.php
