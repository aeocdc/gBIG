# gBIG enviroments
FROM dmmcquay/python2.7.10
MAINTAINER  yangyi@tib.cas.cn
RUN mkdir -p /home/webservice/
WORKDIR /home/webservice/

RUN wget --no-check-certificate https://repo.anaconda.com/miniconda/Miniconda2-latest-Linux-x86_64.sh
RUN bash ./Miniconda2-latest-Linux-x86_64.sh -b -p /opt/miniconda3
ENV PATH=/opt/miniconda3/bin:$PATH
RUN conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/ && \
    conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/r/ && \
    conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/mro/ && \
    conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/ && \
    conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge/ && \
    conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/bioconda/
RUN conda install -y cas-offinder
COPY requirement.txt ./requirement.txt
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8
RUN pip install -r requirement.txt
COPY ref/ ./ref
COPY bioeledbtib ./bioeledbtib
COPY outlab ./outlab

WORKDIR /home/webservice/bioeledbtib
CMD python manage.py runserver 0.0.0.0:8888
