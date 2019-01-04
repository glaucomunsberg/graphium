# Environment MAC OS X 10.14


## Basic Instalation 

$ xcode-select --install

### Brew

$ /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

$ brew install readline xz

$ sudo installer -pkg /Library/Developer/CommandLineTools/Packages/macOS_SDK_headers_for_macOS_10.14.pkg -target /


### PyEnv

$ curl -L https://raw.githubusercontent.com/pyenv/pyenv-installer/master/bin/pyenv-installer | bash
    
$ nano ~/.bashrc
    
Insert the content in bashrc file
    
    export PATH=”~/.pyenv/bin:$PATH”
    eval “$(pyenv init -)”
    eval “$(pyenv virtualenv-init -)”
    
$ source ~/.bashrc
    
$ pyenv install 2.7

$ pyenv local 2.7


### MongoDB

$ brew install mongodb

$ sudo mkdir -p /data/db

To start a service 

$ sudo mongod

## Libraries 

$ pip install pymongo unidecode pillow h5py tensorflow keras mkdocs mkdocs-material pympler

$ pip install osgeo osmread osmapi geopy

#### Installing osgeo library

$ brew install gdal

#### Installing Wand library

$ brew install imagemagick@6

$ pip install wand

$ ln -s /usr/local/Cellar/imagemagick@6/<your specific 6 version>/lib/libMagickWand-6.Q16.dylib /usr/local/lib/libMagickWand.dylib



## Install Ruby on Rails

Read and install [https://gorails.com/setup/osx/10.14-mojave](https://gorails.com/setup/osx/10.14-mojave)