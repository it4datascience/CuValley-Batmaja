FROM python:3.10.2
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
EXPOSE 8080
COPY . ./
CMD gunicorn -b 0.0.0.0:8080 Dash_app.app:server --timeout 3600