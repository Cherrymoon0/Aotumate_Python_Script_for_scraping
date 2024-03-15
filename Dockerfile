FROM python:3.9
WORKDIR /myApp
COPY . .
RUN pip install pandas beautifulsoup4 selenium
CMD ["python3", "./scraping_proccess.py"]
