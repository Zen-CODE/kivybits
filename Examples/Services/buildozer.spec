[app]

# (str) Title of your application
title = ServiceDemo
package.name = zencode.kivy.org
package.domain = service.demo

# (str) Source code where the main.py live
source.dir = ./

# source.include_exts = py,png,jpg,kv,atlas,ini
#source.exclude_exts = spec
#source.exclude_patterns = license,images/*/*.jpg

# (str) Application versioning (method 1)
version = 1.0.0

# (list) Application requirements
requirements = python2,kivy==1.10.0,pyjnius

# (str) Icon of the application
# icon.filename = %(source.dir)sicon.png

# (str) Supported orientation (one of landscape, portrait or all)
# orientation = landscape

# (list) List of service to declare
#services = NAME:ENTRYPOINT_TO_PY,NAME2:ENTRYPOINT2_TO_PY
services = serviceone:service_one/main.py

#
# Android specific
#

fullscreen = 1
# android.permissions = INTERNET

# (int) Android API to use
android.api = 19
android.minapi = 19
android.sdk = 23
# android.sdk = 28

# (str) Android NDK version to use
android.ndk = 16b

android.ndk_path = ~/.buildozer/android/platform/android-ndk-r16b/
# android.sdk_path = ~/.buildozer/android/platform/android-sdk-28/
p4a.source_dir = ~/Repos/python-for-android

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1
