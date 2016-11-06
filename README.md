# Ask Slimov

Technopark@mail.ru, 1 semester, Web-technologies project

```
docker-compose up -d # just run
docker-compose run web python ask_slimov/manage.py fake_users # generate some users
docker-compose run web python ask_slimov/manage.py fake_questions # some questions
docker-compose run web python ask_slimov/manage.py fake_answers # some answers
docker-compose run web python ask_slimov/manage.py fake_likes # some likes
docker-compose run web python ask_slimov/manage.py fake_tags # add some tags to all questions
docker-compose run web python ask_slimov/manage.py cache_tags # cache popular tags (right block of popular tags)
docker-compose run web python ask_slimov/manage.py cache_users # cache popular users (right block of popular users)
```

![The screen](https://raw.github.com/nksoff/ask_slimov/master/screen.png)
