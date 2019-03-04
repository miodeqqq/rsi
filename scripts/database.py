#! /usr/bin/env python

import sqlite3


class ServerDatabase:
    persons_data = [
        ('Maciej', 'Januszewski', 27),
        ('John', 'Travolta', 40),
        ('Elton', 'John', 80)
    ]

    products_data = [
        ('product1', 200.5, 200, 1),
        ('product2', 160.4, 500, 2),
        ('product3', 120.85, 900, 3),
    ]

    def __init__(self, db_name):
        self.db_name = db_name
        self.conn, self.cursor = self._init_connection()

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
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                surname TEXT NOT NULL,
                age INTEGER NOT NULL
            );
        """

        sql_create_product_table = """
            CREATE TABLE IF NOT EXISTS product (
                id INTEGER PRIMARY KEY,
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

    def verify_db_creation(self):
        """
        Verifies if db tables have been created.
        """

        db_tables = [x[0] for x in self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")]

        assert ['person', 'product'] == db_tables

    def run(self):
        """
        Runs the entire pipeline to create database.
        """

        self._initial_cleanup()
        self.create_db_structure()
        self.verify_db_creation()
        self.insert_into_person_table()
        self.insert_data_into_product_table()


ServerDatabase(db_name='rsi.db').run()
