from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='dagpy',
      version='0.3',
      description='Data science collaboration tool based on iPython notebooks.',
      long_description=readme(),
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.4',
      ],
      keywords='jupyter ipython collaboration dag datasci',
      url='https://github.com/ibestvina/dagpy',
      author='Ivan Bestvina',
      author_email='ivan.bestvina@gmail.com',
      license='MIT',
      packages=['dagpy'],
      package_data={'dagpy': ['*.txt']},
      install_requires=[
          'dill',
          'networkx',
          'matplotlib'
      ],
      entry_points = {
        'console_scripts': ['dagpy=dagpy.__main__:main']
      },
      include_package_data=True,
      zip_safe=False)