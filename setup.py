from distutils.core import setup
import os
try:
    import py2exe
except ImportError:
    print("Warning: package py2exe is not available.")

css_dir = 'web/css'
css_files = [os.path.join(css_dir, f)
             for f in os.listdir(css_dir) if os.path.splitext(f)[1] == '.css']
js_dir = 'web/js'
js_files = [os.path.join(js_dir, f)
            for f in os.listdir(js_dir) if os.path.splitext(f)[1] == '.js']
smoothness_dir = 'web/css/smoothness'
smoothness_files = [os.path.join(smoothness_dir, f)
                    for f in os.listdir(smoothness_dir) if os.path.splitext(f)[1] == '.css']
images_dir = 'web/css/smoothness/images'
image_files = [os.path.join(images_dir, f)
               for f in os.listdir(images_dir) if os.path.splitext(f)[1] == '.png']

setup(
    name='kwaras',
    version='2.2.1.12',
    install_requires=['openpyxl'],
    packages=['kwaras', 'kwaras.langs', 'kwaras.conf', 'kwaras.formats', 'kwaras.process'],
    package_dir={'kwaras': '',
                 'kwaras.langs': 'src/langs', 'kwaras.conf': 'src/conf',
                 'kwaras.formats': 'src/formats', 'kwaras.process': 'src/process'},
    data_files=[('web', ['web/index_wrapper.html']),
                (css_dir, css_files),
                (js_dir, js_files),
                (smoothness_dir, smoothness_files),
                (images_dir, image_files)],
    url='http://github.com/ucsd-field-lab/kwaras',
    license='MIT-LICENSE',
    author='Lucien Carroll',
    author_email='lucien@discurs.us',
    description='Tools for managing ELAN corpus files',
    console=['gui.py'],
    options={"py2exe": {"bundle_files": 3}}
)
