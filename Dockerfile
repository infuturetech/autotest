# 使用一个基础镜像，这里我们使用Ubuntu
FROM ubuntu:20.04

# 设置环境变量以避免交互提示
ENV DEBIAN_FRONTEND=noninteractive

#安装JDK Python3.7
RUN apt-get update && apt-get install -y \
    wget \
    software-properties-common \
    openjdk-11-jdk

RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get update && apt install -y python3 python3-pip


# 复制测试用例到工作目录
COPY . /autotest

# 设置工作目录
WORKDIR /autotest

# 设置JAVA_HOME环境变量
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PATH="$JAVA_HOME/bin:$PATH"


# 安装Python依赖库

# RUN pip3 install -r /autotest/requirements.txt


# 运行测试并生成报告
#CMD ["bash", "-c", "pytest -ra -v --alluredir=/app/log_report/001 /app/test_cases && allure generate -c -o /app/log_report/allure /app/log_report/001 && allure open /app/log_report/allure"]

