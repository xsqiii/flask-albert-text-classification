FROM ubuntu:20.04

RUN sed -i s@/archive.ubuntu.com/@/mirrors.tuna.tsinghua.edu.cn/@g /etc/apt/sources.list
RUN apt update && apt install -y tzdata
ENV TZ Asia/Shanghai

RUN apt install python3-pip -y

RUN pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple pip -U \
    && pip3 config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple \
    && pip3 config set install.trust-host pypi.tuna.tsinghua.edu.cn

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

CMD ["gunicorn", "server:app", "-c", "./gunicorn.conf"]