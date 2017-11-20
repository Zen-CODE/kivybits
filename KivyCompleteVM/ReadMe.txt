Kivy Complete VM - 0.1
======================

Greetings. This VM is intented to provide a complete Kivy launch and development
environment. It is not intended to be lightweight and minimal, but complete and
flexible.

This document outlines the configuration and use of the VM, so that you can use
and manage the machine optimally.

Download link: https://mega.nz/#!YuIymALI!AT7scnLjlX9uqjhHEQc49TwVTyYnbB0IFPPCEFU2kOs

md5 chceksum: ebf7f6b7e985c7d64db54450f20b0ba8

Checkouts
---------

Kivy and Buildozer have both been built from source. They are checked out in
the ~/Repos folder. For Python 3, they are checkout out in ~/Repos/Python3.
Kivy is built in these folders, using a symlinks below.

  /usr/local/lib/python2.7/distpackages/kivy -> /home/kivy/Repos/kivy/kivy

  /usr/local/lib/python3.5/distpackages/kivy -> /home/kivy/Repos/Python3/kivy/kivy

This means that in order to build and run a new/old version, you can simply
checkout the tag (or master for latest) you wish to use, recompile and it's
ready to use.

The Kivy installations are built using the 1.10.0 tag, but buildozer is built
from master in order to support Python3 (pythoncrystax).

Buildozer projects
------------------

THe VM contains two sample buildozer spec file that successfully build the
touchtracer APK. These lie here:

    Python2: /home/kivy/Repos/kivy/examples/demo/touchtracer/

    Python3: /home/kivy/Repos/Python3/kivy/examples/demo/touchtracer/ 

TODO: The Python3 building is a WIP and not yet functional.

The VM comes with pre-installed with support (specified in your
buildozer.spec file) support for:

    android.sdk = 23

    android.api = 19

Other versions can be specified, but will result in the downloading and
installation of these packages.

Android SDK
------------

The VM comes with SDK 23 pre-installed. To update or reconfigure it:

    $ cd /home/kivy/.buildozer/android/platform/android-sdk-23/tools/
    $ ./android

Feedback and support
--------------------

For questions and issues, please post on the google Kivy users group.

    https://groups.google.com/forum/#!forum/kivy-users

Thanks
Zen-CODE