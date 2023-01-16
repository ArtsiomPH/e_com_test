FROM mongo

COPY init.json /init.json
CMD mongoimport --host mongodb --db test-form --collection forms --type json --file /init.json --jsonArray