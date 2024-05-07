Директории и их назначение

deploy - директория с настройками для деплоя проекта  
src - директория с основной частью проекта  
    application - директория
        common - директория  
            gateways.py - базовый класс для crud  
            usecase.py - ?
        handle_update.py - хэндлер для входящих апдейтов телеграма  
    infra - директория  
        postgres - директория  
            gateways.py - CRUD запросов к Postgre  
            models.py - Описание модели Postgre  
        redis - директория  
            models.py - DTO для redis
        log.py - логер какой то  
    main - директория  
        __main__ - запуск телеграм бота  
        di.py - дишка провайдеры