FROM resin/rpi-raspbian
LABEL maintainer="Drew Gonzales <drew.gonzales@ucla.edu>"

# Install dependencies
RUN sudo apt-get update && \
  sudo apt-get install -y \
    build-essential \
    tk-dev \
    libncurses5-dev \
    libncursesw5-dev \
    libreadline6-dev \
    libdb5.3-dev \
    libgdbm-dev \
    libsqlite3-dev \
    libssl-dev \
    libbz2-dev \
    libexpat1-dev \
    liblzma-dev zlib1g-dev \
    python3-pip

RUN curl https://www.python.org/ftp/python/3.5.2/Python-3.5.2.tgz  -o /tmp/Python-3.5.2.tgz && \
  tar zxvf /tmp/Python-3.5.2.tgz -C /tmp && \
  cd /tmp/Python-3.5.2 && \
  ./configure --prefix=/usr/local/opt/python-3.5.2 && \
  make && \
  sudo make install

RUN ln -s $(which python3) /usr/bin/python && \
  ln -s $(which pip3) /usr/bin/pip

RUN pip install virtualenv

RUN rm /tmp/*

CMD ['bash']
