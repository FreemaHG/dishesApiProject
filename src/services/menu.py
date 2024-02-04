from typing import List

from fastapi_redis import redis_client
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger

from src.models.menu import Menu
from src.repositories.menu import MenuRepository
from src.schemas.base import BaseInSchema, BaseInOptionalSchema


class MenuService:
    """
    Сервис для вывода списка меню, создания, обновления и удаления меню
    """

    @classmethod
    async def get_menus_list(cls, session: AsyncSession) -> List[Menu]:
        """
        Метод кэширует и возвращает данные об имеющихся меню
        :param session: объект асинхронной сессии
        :return: список с меню
        """
        cache = await redis_client.get("menus_list")

        if cache:
            logger.debug(f"Данные из кэша: {cache}")
            return cache

        logger.debug("Запрос данных из БД")
        menus_list = await MenuRepository.get_list(session=session)

        await redis_client.set("menus_list", [menu.as_dict() for menu in menus_list])
        logger.info("Данные кэшированы")

        return menus_list


    @classmethod
    async def create(cls, new_menu: BaseInSchema, session: AsyncSession) -> Menu:
        """
        Метод создает и возвращает новое меню и очищает кэш со списком меню
        :param new_menu: валидные данные для создания нового меню
        :param session: объект асинхронной сессии
        :return: объект нового меню
        """
        menu_id = await MenuRepository.create(new_menu=new_menu, session=session)
        menu = await MenuRepository.get(menu_id=menu_id, session=session)

        await redis_client.delete("menus_list")

        return menu


    @classmethod
    async def get(cls, menu_id: str, session: AsyncSession) -> Menu | None:
        """
        Метод кэширует данные и возвращает меню по переданному id
        :param menu_id: id меню для поиска
        :param session: объект асинхронной сессии для запросов к БД
        :return: объект меню либо None
        """
        cache = await redis_client.get(f"menu_{menu_id}")

        if cache:
            logger.debug(f"Данные из кэша: {cache}")
            return cache

        logger.debug("Запрос данных из БД")
        menu = await MenuRepository.get(menu_id=menu_id, session=session)

        if menu:
            await redis_client.set(f"menu_{menu_id}", menu.as_dict())
            logger.info("Данные кэшированы")

        return menu


    @classmethod
    async def update(cls, menu_id: str, data: BaseInOptionalSchema, session: AsyncSession) -> Menu | bool:
        """
        Метод обновляет меню по переданному id, очищает кэш списка меню
        :param menu_id: id меню для обновления
        :param data: данные для обновления меню
        :param session: объект асинхронной сессии для запросов к БД
        :return: обновленное меню либо None
        """
        await MenuRepository.update(menu_id=menu_id, data=data, session=session)
        update_menu = await MenuRepository.get(menu_id=menu_id, session=session)

        if update_menu:
            await redis_client.delete("menus_list")
            await redis_client.delete(f"menu_{menu_id}")

            logger.info(f"Меню обновлено")
            return update_menu

        else:
            logger.error("Меню не найдено!")
            return False


    @classmethod
    async def delete(cls, menu_id: str, session: AsyncSession) -> bool:
        """
        Метод удаляет и очищает кэш меню по переданному id
        :param menu_id: id меню для удаления
        :param session: объект асинхронной сессии для запросов к БД
        :return: True - успешное удаление, иначе False
        """
        delete_menu = await MenuRepository.get(menu_id=menu_id, session=session)

        if delete_menu:
            await MenuRepository.delete(delete_menu=delete_menu, session=session)

            await redis_client.delete("menus_list")
            await redis_client.delete(f"menu_{menu_id}")

            # TODO Вызов метода для получения id всех подменю и блюд
            # TODO Вызов метода для очистки кэша для всех подменю и блюд по id!!!

            logger.info(f"Меню удалено")
            return True

        logger.error("Меню не найдено!")
        return False
