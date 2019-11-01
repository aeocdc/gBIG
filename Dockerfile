# gBIG enviroments
FROM dmmcquay/python2.7.10
MAINTAINER  yangyi@tib.cas.cn
WORKDIR /tmp

COPY requirements.txt ./requirements.txt
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8
RUN pip install -r requirements.txt
COPY ref/ ./ref
COPY bioeledbtib ./bioeledbtib
COPY outlab ./outlab

WORKDIR /tmp/bioeledbtib
CMD python manage.py runserver 0.0.0.0:8888
