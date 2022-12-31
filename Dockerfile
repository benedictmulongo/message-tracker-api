FROM python:3.9.15

# ARG TEMP_ARG=arg_input

WORKDIR /message-tracker-api
COPY . .
RUN pip install pipenv
RUN pipenv sync
RUN pipenv requirements > requirements.txt
# RUN pip install -r requirements.txt
# pipenv requirements > requirements.txt 
# pipenv run pip freeze > requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt
#RUN pipenv shell

# ENV TEMP_ARG_ENV=${TEMP_ARG}

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host=0.0.0.0" , "--reload" , "--port", "8000"]
