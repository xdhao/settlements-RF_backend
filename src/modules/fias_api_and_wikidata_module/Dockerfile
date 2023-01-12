# 
FROM python:3.10

# 
WORKDIR ./src

# 
COPY ./requirements.txt requirements.txt

#
RUN pip install --no-cache-dir --upgrade -r requirements.txt

#
COPY ./ .

# 
CMD ["uvicorn", "modules.fias_api_and_wikidata_module.main:app", "--reload", "--host", "0.0.0.0", "--port", "80", "--proxy-headers"]