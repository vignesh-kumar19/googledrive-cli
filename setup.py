from setuptools import setup, find_packages
setup(name='drivecli',
      version='1.0.0',
      description='drivecli, manage google drive in command line. It can perform tasks like search file, download or upload file in user\'s google drive',
      url='https://github.com/vignesh-kumar19/googledrive-cli',
      author='Vignesh Kumar',
      author_email='kvkumar1993@gmail.com',
      python_requires='>=3',
      packages=find_packages(),
      install_requires=[
         'prettytable==0.7.2',
         'google-api-python-client==1.7.3',
         'oauth2client==4.1.2'
         ],
      entry_points={
         'console_scripts':[
            'drivecli=googledrivecli.driverclient:main'
         ]
}
)
