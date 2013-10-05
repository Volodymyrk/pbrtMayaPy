Welcome to pbrtMayaPy
=============

This is a cross-platform exporter Plugin for Maya that renders your Autodesk Maya scenes using PBRT v2. PBRT is a Physically Based Rendering system that is described in a wonderful book by Matt Pharr and Greg Humphreys: "Physically Based Rendering: From Theory To Implementation".

About
------------

The purpose of this plugin is to allow the reader of "Physically Based Rendering: From Theory To Implementation" to work with the system described in the book using Autodesk Maya.

Therefore, pbrtMayaPy is written with three principles in mind:
* **Completeness**. Comprehensive coverage of most features of PBRT
* **The user is technically-savvy**. User is capable to enter PBRT commands, when neccecary.
* **Simplicity**. The system has a simple and modular design. New exporter features should be easy to add by anyone with Python knowledge.

This plugin is based on Python LuxMaya translation by Doug Hammond (https://bitbucket.org/luxrender/luxmaya) , in turn base on translation of the c++ luxmaya exporter, 
in turn based on original maya-pbrt c++ exporter by Mark Colbert (http://graphics.cs.ucf.edu/mayapbrt/index.php).

Features
------------
* Render settings and Film options
  * Samplers
  * Filtering
  * Renderers
  * Integrators
  * Accelerators
* Cameras
  * Perspective
  * Environment
  * Orthographic
* Lights
  * Point
  * Spot
  * Distant
  * Area
  * Other types (using a text object)
* Geometric primitives
  * Polygons only
  * Implicit shapes (using a text object)
* Materials
  * Basic Maya materials
  * Full PBRT Shading graph is accessible using text material


Requirements
------------
* Autodesk Maya for Windows, Mac or Linux.
* PBRT Open-Source renderer

Installation
-------------

1. Get the source by pressing "Download ZIP" on the right (or via git). Unzip to any folder, e.g.: $HOME/youMayaStuff/pbrtMayaPy/ 

2. Download and compile PBRT from http://pbrt.org/downloads.php

3. Set the following Environment variables (you can add the following to your Maya.env):
 * MAYA_PLUG_IN_PATH = $HOME/youMayaStuff/pbrtMayaPy/
 * PBRT_SEARCHPATH = $HOME/youMayaStuff/pbrt-v2/Build/Products/Release/

4. Load the plugin in Maya using Plug-in Manager

5. Press "Export and Render" from the top menu or execute MEL: pbrt_export (python: cmds.pbrt_export)

![screenshot](https://raw.github.com/Volodymyrk/Volodymyrk.github.io/master/pbrtMayaPy.png)




Useful links
-------------

* http://pbrt.org/downloads.php
