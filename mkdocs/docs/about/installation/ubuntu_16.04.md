## Environment Linux

### Basic Instalation

````bash
$ sudo apt-get update
$ sudo apt-get install build-essential checkinstall
$ sudo apt-get install libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev
````

#### PyEnv


````bash
$ git clone https://github.com/pyenv/pyenv.git ~/.pyenv
$ echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bash_profile
$ echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bash_profile$ echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n  eval "$(pyenv init -)"\nfi' >> ~/.bash_profile
$ exec "$SHELL"
$ pyenv install 2.7.15
````

#### MongoDB

````bash
$ sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv EA312927
$ echo "deb http://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/3.2 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.2.list
$ sudo apt-get update
$ sudo apt-get install -y mongodb-org
$ sudo systemctl start mongod
$ sudo systemctl enable mongod #The last step is to enable automatically starting MongoDB when the system starts.
````

### Libraries 

````bash
$ pip install pymongo unidecode pillow h5py tensorflow keras mkdocs mkdocs-material pympler
$ pip install osgeo osmread osmapi geopy
````

##### Installing osgeo library

````bash
$ sudo apt-get install gdal-bin python-gdal python3-gdal 
````

##### Installing Wand library

````bash
$ sudo apt-get update
$ sudo apt-get install build-essential checkinstall libx11-dev libxext-dev zlib1g-dev libpng12-dev libjpeg-dev libfreetype6-dev libxml2-dev
$ sudo apt-get build-dep imagemagick

$ pip install wand
````

### Install Ruby on Rails

Read and install [How To Install RoR with rbenv on Ubuntu 16.04](https://www.digitalocean.com/community/tutorials/how-to-install-ruby-on-rails-with-rbenv-on-ubuntu-16-04)