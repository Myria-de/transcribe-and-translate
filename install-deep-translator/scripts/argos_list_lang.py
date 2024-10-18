#!/home/te/python-trans/bin/python3
import argostranslate.package, argostranslate.translate
argostranslate.package.update_package_index()
available_packages = argostranslate.package.get_available_packages()
for package in available_packages:
    pkg = str(package)
    print(pkg + ' ' + package.from_code +'->' + package.to_code )
