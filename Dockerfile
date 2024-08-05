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

COPY . /autotest
# 设置工作目录
WORKDIR /autotest

# 设置JAVA_HOME环境变量
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PATH="$JAVA_HOME/bin:$PATH"

# 设置 Allure 版本
ENV ALLURE_VERSION=2.15.0

# 下载并安装 Allure
RUN wget https://github.com/allure-framework/allure2/releases/download/${ALLURE_VERSION}/allure-${ALLURE_VERSION}.tgz && \
    tar -zxvf allure-${ALLURE_VERSION}.tgz -C /opt/ && \
    ln -s /opt/allure-${ALLURE_VERSION}/bin/allure /usr/bin/allure && \
    allure --version

# 设置 Allure 环境变量
ENV PATH="/opt/allure-${ALLURE_VERSION}/bin:${PATH}"

# 清理安装过程中的临时文件
RUN rm -rf allure-${ALLURE_VERSION}.tgz

# 安装Python依赖库

EXPOSE 7010


RUN pip3 install -r /autotest/requirements.txt
#RUN iconv -f GBK -t UTF-8 pytest.ini -o pytest.ini
#RUN pytest -ra -v --alluredir=/autotest/log_report/001 /autotest/test_cases
#RUN allure generate -c -o   /autotest/log_report/allure   /autotest/log_report/001
#RUN allure open  /autotest/log_report/allure

# 运行测试并生成报告
#CMD ["bash", "-c", "pytest -ra -v --alluredir=/app/log_report/001 /app/test_cases && allure generate -c -o /app/log_report/allure /app/log_report/001 && allure open /app/log_report/allure"]

