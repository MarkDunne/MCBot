FROM python:3.8-slim

RUN apt-get update && apt-get install -y \
  build-essential

# We need wget to set up the PPA and xvfb to have a virtual screen and unzip to install the Chromedriver
RUN apt-get install -y wget xvfb unzip

# Set up the Chrome PPA
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list

# Update the package list and install chrome
RUN apt-get update -y
RUN apt-get install -y google-chrome-stable

# Set up Chromedriver Environment variables
ENV CHROMEDRIVER_VERSION 89.0.4389.23
ENV CHROMEDRIVER_DIR /chromedriver
RUN mkdir $CHROMEDRIVER_DIR

# Download and install Chromedriver
RUN wget -q --continue -P $CHROMEDRIVER_DIR "http://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip"
RUN unzip $CHROMEDRIVER_DIR/chromedriver* -d $CHROMEDRIVER_DIR

# Put Chromedriver into the PATH
ENV PATH $CHROMEDRIVER_DIR:$PATH

ENV POETRY_VERSION=1.1.5
RUN pip install poetry=="${POETRY_VERSION}"

WORKDIR /usr/src/app

#RUN useradd -ms /bin/bash botuser
#RUN chown -R botuser:botuser /usr/src/app
#USER botuser

COPY poetry.lock pyproject.toml poetry.toml ./

RUN poetry install --no-dev

COPY . .

EXPOSE 8000

CMD poetry run supervisord