#! /usr/bin/env python

import sqlite3
from random import randint, uniform

from faker import Faker


class RandomPeopleGenerator:
    people_data = None

    def __init__(self, number):
        self.number = number

    def generate_data(self):
        """
        Generates random people/products data.
        """

        faker = Faker()

        people = [
            (
                faker.first_name(),
                faker.last_name(),
                randint(1, 80)
            ) for _ in range(self.number)
        ]

        products = [
            (
                faker.word(),
                '{:.3f}'.format(uniform(13.5, 299.4)),
                randint(100, 990),
                randint(1, 1000)
            ) for _ in range(self.number)
        ]

        return people, products


class ServerDatabase(RandomPeopleGenerator):
    def __init__(self, db_name):
        super(ServerDatabase, self).__init__(number=50)

        self.db_name = db_name

        self.conn, self.cursor = self._init_connection()

        self.persons_data, self.products_data = self.generate_data()

    def _init_connection(self):
        """
        Initialises connection with db.
        """

        conn = sqlite3.connect(
            database=self.db_name,
            timeout=10
        )

        return conn, conn.cursor()

    def _initial_cleanup(self):
        """
        Initial cleanup - tables drop.
        """

        if self.conn is not None:
            self.conn.execute("DROP TABLE IF EXISTS product;")
            self.conn.execute("DROP TABLE IF EXISTS person;")

    def create_db_structure(self):
        """
        Creates tables.
        """

        sql_create_person_table = """
            CREATE TABLE IF NOT EXISTS person (
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                name TEXT NOT NULL,
                surname TEXT NOT NULL,
                age INTEGER NOT NULL
            );
        """

        sql_create_product_table = """
            CREATE TABLE IF NOT EXISTS product (
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                name TEXT NOT NULL,
                price FLOAT NOT NULL,
                quantity INTEGER NOT NULL,
                person_id INTEGER NOT NULL,
                FOREIGN KEY(person_id) REFERENCES person (id)
            );"""

        self.cursor.execute(sql_create_person_table)
        self.cursor.execute(sql_create_product_table)

        self.conn.commit()

    def insert_into_person_table(self):
        """
        Inserts data into person table.
        """

        self.cursor.executemany(
            "INSERT INTO person(name, surname, age) VALUES (?,?,?);",
            self.persons_data
        )

    def insert_data_into_product_table(self):
        """
        Inserts data into product table.
        """

        self.cursor.executemany(
            "INSERT INTO product(name, price, quantity, person_id) VALUES (?,?,?,?);",
            self.products_data
        )

    def run(self):
        """
        Runs the entire pipeline to create database.
        """

        self._initial_cleanup()

        self.create_db_structure()
        self.insert_into_person_table()
        self.insert_data_into_product_table()
        self.conn.commit()


ServerDatabase(db_name='rsi.db').run()
