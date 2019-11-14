FROM ma-imagesrepo.maezia.dev:9443/library/python:3.6

ADD ./requirements.txt ./
RUN pip install -r requirements.txt

COPY ./ ./app/

WORKDIR app

EXPOSE 5000 
CMD ["python3", "app.py"]
