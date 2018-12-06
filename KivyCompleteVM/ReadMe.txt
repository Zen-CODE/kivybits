Kivy Complete VM - 0.5
======================

Greetings. This VM is intended to provide a complete Kivy launch and development
environment. It is not intended to be lightweight and minimal, but complete and
flexible.

This document outlines the configuration and use of the VM, so that you can use
and manage the machine optimally.

    Download link: http://kivy.braintrainerplus.com/Kivy_Complete_VM_0.5.ova

    md5 checksum: 3533d0571838f406797ca75a0b636130

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

The Kivy installations are built using the master branch, any buildozer is built
from master in order to support Python3.

Buildozer projects
------------------

The VM contains two sample buildozer spec files that successfully build the
touchtracer APK. These lie here:

    Python2: /home/kivy/Repos/kivy/examples/demo/touchtracer/

    Python3: /home/kivy/Repos/Python3/kivy/examples/demo/touchtracer/ 

Please see the buildozer.spec files in these folder for the appropriate
settings.

The VM comes pre-installed with for:

    android.sdk = 28

    android.api = 19 or android.api = 27

Other versions can be specified, but might result in the downloading and
installation of these packages.

Android SDK
------------

The VM comes with SDK 28 pre-installed. To update or reconfigure it:

    $ cd /home/kivy/Android/android-sdk-28/tools/
    $ ./android

Android Debugging with buildozer
---------------------------------

Please note that in order to attached devices to the VM for debugging,
you first need to give permissions. Un linux hosts, this means running

    $ sudo adduser $USER vboxusers

where user is your identity in the host machine. You should then be able
attach a USB filter that allows the VM to pick up your devices. 

In order to start the adb server:

    $ cd /home/kivy/Android/android-sdk-28/platform-tools/
    $ sudo ./adb start-server
    $ sudo ./adb start-server
    $ ./adb devices

Your devices should be listed with the last command. You can then launch
your app with debug output (when inside you app folder) via

    $ buildozer android debug deploy run logcat

Feedback and support
--------------------

For questions and issues, please post on the google Kivy users group.

    https://groups.google.com/forum/#!forum/kivy-users

Thanks
Zen-CODE