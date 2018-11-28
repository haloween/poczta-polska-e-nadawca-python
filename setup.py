from setuptools import setup

setup(name='poczta_polska_enadawca',
      version='0.1',
      description='Client wrapper for Poczta Polska e-nadawca WSDL API. ',
      url='https://github.com/haloween/poczta-polska-e-nadawca-python',
      keywords = "poczta, polska, e-nadawca, enadawca, wsdl, api",
      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Web Environment',
          'Framework :: Django',
          'Intended Audience :: Developers',
          'License :: MIT License',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
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
