# Backend for pet-project [planner-dev.ru](https://planner-dev.ru/)
<img src="https://img.shields.io/github/workflow/status/kuratov-v/planner-backend/Deploy/master?style=plastic"> <img src="https://img.shields.io/github/last-commit/kuratov-v/planner-backend?style=plastic"> <a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg?style=plastic"></a>

Backend is built on DRF, see [frontend repo](https://github.com/kuratov-v/planner-frontend).

## Project features
- [x] use docker-compose
- [x] use vk auth
- [x] tests
- [x] configure ci cd
- [ ] embed microservices
- [ ] embed VK bot

## Project configuration
Create a [vk app](https://vk.com/editapp?act=create) for user auth with the following settings.

```
Адрес сайта: http://localhost:8080/
Базовый домен: localhost
Доверенный редирект URI: http://localhost:8080/auth/vk/success/
```
Then configure `.envs` directory, for example see `.envs_example`.
```
SOCIAL_AUTH_VK_OAUTH2_KEY = "ID приложения"
SOCIAL_AUTH_VK_OAUTH2_SECRET = "Защищённый ключ"
SOCIAL_AUTH_VK_REDIRECT_URI = "Сервисный ключ доступа"
```

## Build and run
```
docker-compose build
docker-compose up 
```

## Tests
```
docker-compose -f test.yml build
docker-compose -f test.yml up --abort-on-container-exit 
```
