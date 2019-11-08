# gBIG enviroments
FROM dmmcquay/python2.7.10
MAINTAINER  yangyi@tib.cas.cn
RUN apt-get update && apt-get install -y --no-install-recommends vim
RUN mkdir -p /home/webservice/
WORKDIR /home/webservice/

RUN wget --no-check-certificate https://repo.anaconda.com/miniconda/Miniconda2-latest-Linux-x86_64.sh
RUN bash ./Miniconda2-latest-Linux-x86_64.sh -b -p /opt/miniconda3
RUN /opt/miniconda3/bin/conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/ && \
    /opt/miniconda3/bin/conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/r/ && \
    /opt/miniconda3/bin/conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/mro/ && \
    /opt/miniconda3/bin/conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/ && \
    /opt/miniconda3/bin/conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge/ && \
    /opt/miniconda3/bin/conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/bioconda/
RUN /opt/miniconda3/bin/conda install -y cas-offinder
COPY requirement.txt ./requirement.txt
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8
RUN pip install -r requirement.txt
COPY ref/ ./ref
COPY bioeledbtib ./bioeledbtib
COPY outlab ./outlab

WORKDIR /home/webservice/bioeledbtib
RUN python manage.py makemigrations
RUN python manage.py migrate
CMD python manage.py runserver 0.0.0.0:8888
