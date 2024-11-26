# API IN FLASK

## Migrate database

Create the database: 

```bash
$ flask db init
```

Migrate the tables:

```bash
$ flask db migrate -m "Create book model"
```

Apply the migration

```bash
$ flask db upgrade
```

Execute the seeder

```bash
$ python seeds/seed.py
```

Run the application:

```bash
$ flask run
```
