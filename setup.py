from setuptools import setup

setup(name='poczta_polska_enadawca',
      version='0.8',
      description='Client wrapper for Poczta Polska e-nadawca WSDL API.',
      url='https://github.com/haloween/poczta-polska-e-nadawca-python',
      keywords = "poczta, polska, e-nadawca, enadawca, wsdl, api",
      classifiers=[
          'Development Status :: 4 - Beta',
          'Framework :: Django',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.9',
          'Programming Language :: Python :: 3.10',
          'Programming Language :: Python :: 3.11',
      ],
      author='Tomasz Utracki-Janeta',
      author_email='halgravity+githubrepo@gmail.com',
      license='MIT',
      zip_safe=True,
      packages=['poczta_polska_enadawca'],
      include_package_data=True,
      install_requires=[
          'zeep',
          'requests'
      ]
      )