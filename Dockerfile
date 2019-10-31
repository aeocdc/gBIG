# gBIG enviroments
FROM dmmcquay/python2.7.10
MAINTAINER  yangyi@tib.cas.cn
RUN yum update  -y && yum upgrade -y && yum install -y --no-install-recommends \
      bzip2 \
      g++ \
      git \
      graphviz \
      libgl1-mesa-glx \
      libhdf5-dev \
      openmpi-bin \
      wget && \
    rm -rf /tmp/*


WORKDIR /tmp

COPY requirements.txt ./requirements.txt
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8
RUN pip install -r requirements.txt
COPY ref/ ./ref
COPY bioeledbtib ./bioeledbtib
COPY outlab ./outlab

WORKDIR /tmp/bioeledbtib
CMD python manage.py runserver 0.0.0.0:8888
