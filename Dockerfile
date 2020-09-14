FROM python:3.7
WORKDIR /dockerBuild
ENV FLASK_APP run.py
ENV FLASK_RUN_HOST 0.0.0.0
ENV FLASK_ENVIRONMENT_CONFIG stag
ENV SECRET_KEY mysecretkey
ENV SECURITY_PASSWORD_SALT f1nd1ngn3m0
COPY ./requirements.txt /dockerBuild/requirements.txt
RUN pip install -r requirements.txt
COPY . /dockerBuild
CMD ["flask","run"]