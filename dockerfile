FROM registry.cn-beijing.aliyuncs.com/aliyunfc/runtime-python3.10:build-latest

WORKDIR /code

COPY ./requirements.txt .

RUN mkdir python && \
    pip install --no-cache-dir -r requirements.txt -t python && \
    zip -ry python.zip python

CMD ["bash"]