FROM tensorflow/tensorflow:latest-gpu-jupyter
RUN mkdir /tf/nemotion
WORKDIR /tf/nemotion
ADD ./requirements.txt /tf/nemotion/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN python -m nltk.downloader stopwords
EXPOSE 8888
EXPOSE 6006
ADD . /tf/nemotion
