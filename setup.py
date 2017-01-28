# 
from setuptools import setup, find_packages



VERSION = '0.2.1'  
AUTHOR_NAME = 'Bryant E. McDonnell (EmNet LLC)'
AUTHOR_EMAIL = 'bemcdonnell@gmail.com'



setup(name='pyswmm',
      version=VERSION,
      description='Python Wrapper for SWMM5 API',
      author=AUTHOR_NAME,
      url='https://github.com/OpenWaterAnalytics/pyswmm/wiki',
      author_email=AUTHOR_EMAIL,

      package_dir = {'':'pyswmm'},
      packages=[''],
      package_data = {'':
                      ['swmmLinkedLibs/Windows/swmm5.dll',\
                       'license.txt']},
      include_package_data=True,
      license="BSD2 License",
      keywords = "swmm5, swmm, hydraulics, hydrology, modeling, collection system",
      classifiers=[
          "Topic :: Scientific/Engineering",
          "Topic :: Documentation :: Sphinx",
          "Operating System :: Microsoft :: Windows",
          "License :: OSI Approved :: BSD License",
          "Programming Language :: Python :: 2.7",
          "Programming Language :: C",
          "Development Status :: 4 - Beta",
      ]
)
