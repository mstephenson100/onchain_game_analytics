# Indexer Schema
This is the MySQL schema which indexer writes and reads from. The api also reads from this same schema.
### Loading The Schema
Assuming you have a running MySQL server with root credentials then login to it and create the bios database:
~~
$ mysql -uroot
mysql> create database bios
~~
Navigate to this directory and load the schema:
~~
$ mysql -uroot bios < bios.sql
~~

The end.
