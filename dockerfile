FROM ubuntu:18.04
MAINTAINER "jingq"<guoqun.jin@hotmail.com>
RUN apt-get update -y && \
    apt-get install -y locales && \
    apt-get upgrade -y && \
    localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8 && \
    apt-get install -y \
        git \
        python3 \
        python3-dev \
        python3-setuptools \
        python3-pip \
        nano \
        nginx && \
    pip3 install --upgrade setuptools pip && \
    pip install -i https://pypi.tuna.tsinghua.edu.cn/simple uwsgi==2.0.18
ENV TZ=Asia/Shanghai
RUN set -eux; \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime; \
    echo $TZ > /etc/timezone
ENV LANG en_US.utf8
ENV PYTHONUNBUFFERED 1
ENV PYTHONIOENCODING UTF-8
COPY requirements.txt /opt/requirements.txt
WORKDIR /opt
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
COPY tb_nginx.conf /etc/nginx/sites-available/default
EXPOSE 80
