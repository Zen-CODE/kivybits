Kivy Complete VM - 0.2
======================

Greetings. This VM is intented to provide a complete Kivy launch and development
environment. It is not intended to be lightweight and minimal, but complete and
flexible.

This document outlines the configuration and use of the VM, so that you can use
and manage the machine optimally.

    Download link: http://www.camiweb.com/zenkey/kivy/Kivy_Complete_VM_0.2.ova
    MD5: http://www.camiweb.com/zenkey/kivy/Kivy_Complete_VM_0.2.md5

    md5 checksum: 18a3d0fccf9a66173ae79ed72db26b7a

Please consult the readme.txt on the VM's desktop for more information.

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
