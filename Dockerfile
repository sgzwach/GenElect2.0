FROM tiangolo/meinheld-gunicorn-flask:python3.7

WORKDIR /app

RUN apt-get update
RUN apt-get install -y libmariadb-dev
RUN apt-get autoremove
RUN apt-get clean

# fix datetime to chicago
ENV TZ=America/Chicago
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# add script last as it's most common change
ADD requirements.txt .
RUN pip install -r requirements.txt
ADD . . 
