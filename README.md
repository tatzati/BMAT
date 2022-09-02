# BMAT


## Execute with docker compose

```
$ docker compose up -d
```

### Part 1
You can run this command to import the csv data to the database.
The csv file is already at the appropriate location: /import/works_metadata.csv
```
docker-compose run web python3 manage.py ingest
```

You can run tests with this command:
```
docker-compose run web python3 manage.py test
```

### Part 2

After the service is running, hit ```http://0.0.0.0:8000/works/enrich/```
from some agent (postman, other service) with a body of
```json
{
  "iswc" : ["ISWC1", "ISWC2", "etc"] 
}
```
it will filter the list and return the works.

If you want to use django Admin page :
```
docker-compose run web python3 manage.py createsuperuser 
```
After filling the data accordingly, you can access the admin page at ```localhost:8000/admin```
with the credentials you configured early.
