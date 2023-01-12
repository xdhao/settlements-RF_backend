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
CMD ["uvicorn", "modules.database_filling_submodule.main:app", "--reload", "--host", "0.0.0.0", "--port", "80", "--proxy-headers"]