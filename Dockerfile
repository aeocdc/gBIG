# gBIG enviroments
FROM dmmcquay/python2.7.10
MAINTAINER  yangyi@tib.cas.cn
WORKDIR /tmp

COPY requirement.txt ./requirement.txt
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8
RUN pip install -r requirement.txt
COPY ref/ ./ref
COPY bioeledbtib ./bioeledbtib
COPY outlab ./outlab

WORKDIR /tmp/bioeledbtib
RUN chmod 755 /tmp/bioeledbtib/componenttib/cas-offinder
CMD python manage.py runserver 0.0.0.0:8888
