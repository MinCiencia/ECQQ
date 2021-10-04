FROM tensorflow/tensorflow:latest-gpu-jupyter
RUN mkdir /tf/ecqq
WORKDIR /tf/ecqq
ADD ./requirements.txt /tf/ecqq/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
EXPOSE 8888
EXPOSE 6006
ADD . /tf/ecqq
