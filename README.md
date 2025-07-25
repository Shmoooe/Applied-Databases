# Applied-Databases

This is a project to demonstrate my ability to connect python with MySQL and Neo4j databases.

In this repository you will find:

1. ```Databases```- contains the database files.

2. ```images``` - contains an image used withing this README file.

3. ```.gitignore```

4. ```README.md```

5. ```connect_mysql.py``` - not available publicly as it contains a password for connecting to MySQL

6. ```connect_neo4j.py``` - driver for connecting to neo4j database.

7. ```main.py``` - contains all code and can be run from the command line.


When running main.py, the user will be prompted to make a choice from the menu below:

```
MoviesDB
---------


MENU
====
1 - View Directors & Films
2 - View Actors by Month of Birth
3 - Add New Actor
4 - View Married Actors
5 - Add Actor Marriage
6 - View Studios
x - Exit Application
Choice:
```

To run the project, you will need to have the following programs in your environment:

1. [mysql command line and workbench](https://dev.mysql.com/downloads/installer/) 

2. [neo4j community edition for windows](https://neo4j.com/deployment-center/)

![image](images/neo4j_download.png)

It's important to download the community edition.

3. [java version 21](https://adoptium.net/en-GB/temurin/releases/?os=any&arch=any&version=21)

4. In your python environment:

```pip install pymysql```

```pip install neo4j```

To initiate your local host, you will paste the path of your neo4j bin folder into your command line e.g. 
```
cd C:\Users\joann\Downloads\neo4j-community-2025.05.0\bin
```
and run the command:
```
neo4j. bat console
```


Change the name of the default database to "appdbproj", by opening your neo4j community edition folder and finding the "conf" file.
```#initial.dbms.default_database=appdbproj```


