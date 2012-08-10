# This is a slimmed-down version of the setup.py file
# written by D. Dale for the praxes project 
# @ http://github.com/praxes/praxes.
# Only the setup() is new.

from distutils.core import setup
from distutils.core import Command
from distutils.command.sdist import sdist as _sdist
from distutils.command.build import build as _build
from distutils.command.bdist_wininst import bdist_wininst as _bdist_wininst
import multiprocessing
import os
import subprocess
import sys


def convert_ui(args, **kwargs):
	subprocess.call(args, **kwargs)


class ui_cvt(Command):

	description = "Convert Qt user interface files to PyQt .py files"

	user_options = []

	boolean_options = []

	def initialize_options(self):
		pass

	def finalize_options(self):
		pass

	def run(self):
		try:
			to_process = []
			for root, dirs, files in os.walk('.'):
				for f in files:
					if f.endswith('.ui'):
						source = os.path.join(root, f)
						dest = os.path.splitext(source)[0] + '.py'
						exe = 'pyuic4'
					else:
						continue

					if not os.path.exists(dest):
						to_process.append([exe, '-o', dest, source])

			if sys.platform.startswith('win'):
				# doing this in parallel on windows will crash your computer
				[convert_ui(args, shell=True) for args in to_process]
			else:
				pool = multiprocessing.Pool()
				pool.map(convert_ui, to_process)
		except EnvironmentError:
			print("""\
				Warning: PyQt4 development utilities (pyuic4) not found
				Unable to install graphical user interface
				""")


class sdist(_sdist):

	def run(self):
		self.run_command('ui_cvt')
		_sdist.run(self)


class build(_build):

	def run(self):
		self.run_command('ui_cvt')
		_build.run(self)


class bdist_wininst(_bdist_wininst):

	def run(self):
		self.run_command('ui_cvt')
		_bdist_wininst.run(self)


packages = []
for dirpath, dirnames, filenames in os.walk('.'):
	if '__init__.py' in filenames:
		packages.append('.'.join(dirpath.split(os.sep)))
	else:
		del(dirnames[:])


setup(name = 'TITAN',
	  author = 'Robin M Baur',
	  author_email = 'rmb62@cornell.edu',
	  cmdclass = {
	  	'bdist_wininst': bdist_wininst,
	  	'build': build,
	  	'sdist': sdist,
	  	'ui_cvt': ui_cvt
	 	 },
	  packages = packages,
	  requires = (
	  	'python (>=2.7)',
	  	'numpy (>=1.6.1)',
	  	'scipy (>=0.10.1)',
	  	'h5py (>=2.0.0)',
	  	'praxes (>=0.5.1)'
	  	),
	  version = '0.1.0'
     )