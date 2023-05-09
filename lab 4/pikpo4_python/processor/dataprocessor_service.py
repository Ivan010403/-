from pandas import DataFrame

import sqlite3
from .dataprocessor_factory import DataProcessorFactory
from repository.connectorfactory import SQLStoreConnectorFactory       # подключаем фабрику коннекторов БД
from repository.sql_api import *                                       # подключаем API для работы с БД

"""
    В данном модуле реализуется класс с основной бизнес-логикой приложения. 
    Обычно такие модули / классы имеют в названии слово "Service".
"""


class DataProcessorService:

    def __init__(self, datasource: str, db_connection_url: str):
        self.datasource = datasource
        self.db_connection_url = db_connection_url
        # Инициализируем в конструкторе фабрику DataProcessor
        self.processor_fabric = DataProcessorFactory()

    """
        ВАЖНО! Обратите внимание, что метод run_service использует только методы базового абстрактного класса DataProcessor
        и, таким образом, будет выполняться для любого типа обработчика данных (CSV или TXT), что позволяет в дальнейшем 
        расширять приложение, просто добавляя другие классы обработчиков, которые, например, работают с базой данных или
        сетевым хранилищем файлов (например, FTP-сервером).
    """

    def run_service(self) -> None:
        """ Метод, который запускает сервис обработки данных  """
        processor = self.processor_fabric.get_processor(self.datasource)        # Инициализируем обработчик
        if processor is not None:
            day = int(input ("Enter a day which you want: "))
            self.get_data_from_db(day)

            day = int(input ("Enter a day which you want change: "))
            self.put_data_into_db(day)

            self.delete_row()
            
        else:
            print('Nothing to run')
        # после завершения обработки, запускаем необходимые методы для работы с БД
        self.save_to_database(processor.result)

    def save_to_database(self, result: DataFrame) -> None:
        """ Сохранение данных в БД """
        db_connector = None
        if result is not None:
            try:
                db_connector = SQLStoreConnectorFactory().get_connector(self.db_connection_url)  # инициализируем соединение
                db_connector.start_transaction()  # начинаем выполнение запросов (открываем транзакцию)
                insert_into_source_files(db_connector, self.datasource)  # сохраняем в БД информацию о новом файле с набором данных
                print(select_all_from_source_files(db_connector))  # вывод списка всех обработанных файлов
                insert_rows_into_processed_data(db_connector, result)  # записываем в БД результат обработки набора данных
            except Exception as e:
                print(e)
            finally:
                if db_connector is not None:
                    db_connector.end_transaction()  # завершаем выполнение запросов (закрываем транзакцию)
                    db_connector.close()            # Завершаем работу с БД


# CRUD functions
    def get_data_from_db(self, day):
        try:
            sqlite_connection = sqlite3.connect('test.db')
            cursor = sqlite_connection.cursor()
            print("Подключен к SQLite")

            sqlite_select_query = """SELECT * from processed_data"""
            cursor.execute(sqlite_select_query)
            records = cursor.fetchall()
            
            counter = 0
            for row in records:
                if counter == day-1:
                    print(row)
                counter = counter + 1
        except Exception as e:
            print(e)

    def put_data_into_db(self, day):
        sqlite_connection = sqlite3.connect('test.db')
        cursor = sqlite_connection.cursor()

        sql_update_query = """Update processed_data set rain = ? where id = ?"""
        data = (input("Enter rain "), day)
        cursor.execute(sql_update_query, data)

        sql_update_query = """Update processed_data set temperature = ? where id = ?"""
        data = (input("Enter temperature "), day)
        cursor.execute(sql_update_query, data)

        sql_update_query = """Update processed_data set wind_speed = ? where id = ?"""
        data = (input("Enter wind_speed "), day)
        cursor.execute(sql_update_query, data)
        
        sqlite_connection.commit()

        self.get_data_from_db(day)
        
    def new_row(self):
        sqlite_connection = sqlite3.connect('test.db')
        cursor = sqlite_connection.cursor()

        sqlite_insert_query = """INSERT INTO processed_data
                            (id, rain, temperature, source_file, wind_speed)
                            VALUES
                            (30, 'no', 0, 0, 0);"""
        count = cursor.execute(sqlite_insert_query)
        sqlite_connection.commit()


    def delete_row(self):
        sqlite_connection = sqlite3.connect('test.db')
        cursor = sqlite_connection.cursor()

        sql_delete_query = """DELETE from processed_data where id = 30"""
        cursor.execute(sql_delete_query)

        sqlite_connection.commit()
        