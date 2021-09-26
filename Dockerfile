FROM python:3.8-buster

# 阿里云镜像源
#RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories
RUN apt update
RUN apt upgrade -y
RUN pip install -U pip
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip config set install.trusted-host mirrors.aliyun.com

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "api:sentiment", "-c", "./gunicorn.conf"]