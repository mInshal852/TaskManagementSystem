# ---------------------------------------------------------
# 1. Import os
# ---------------------------------------------------------

import os

# `os` is Python's built-in module for interacting with
# the operating system.
#
# We will use `os.getenv()` to read values such as:
# DB_USER
# DB_PASSWORD
# DB_HOST
# DB_PORT
# DB_NAME
#
# These values will come from our .env file.


# ---------------------------------------------------------
# 2. Import SQLAlchemy functions
# ---------------------------------------------------------

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# `create_engine()`
# -----------------
# Creates a SQLAlchemy Engine.
#
# The Engine is responsible for communicating with the
# PostgreSQL database.
#
# Argument:
#
# create_engine(DATABASE_URL)
#
# `DATABASE_URL` tells SQLAlchemy:
# - Which database system to use
# - Where the database is
# - Which username to use
# - Which password to use
# - Which database to connect to


# `sessionmaker`
# --------------
# `sessionmaker` creates a factory for creating database
# sessions.
#
# A database session is used when we want to interact
# with PostgreSQL, for example:
#
# - INSERT data
# - SELECT data
# - UPDATE data
# - DELETE data
#
# Think of SessionLocal as a "session creator."


# ---------------------------------------------------------
# 3. Import load_dotenv
# ---------------------------------------------------------

from dotenv import load_dotenv

# `load_dotenv()` reads the variables stored inside our
# `.env` file and loads them into Python's environment.
#
# For example, our .env might contain:
#
# DB_USER=postgres
# DB_PASSWORD=mypassword
# DB_HOST=localhost
# DB_PORT=5432
# DB_NAME=task_management
#
# After calling load_dotenv(), Python can access them
# using os.getenv().


# ---------------------------------------------------------
# 4. Load .env variables
# ---------------------------------------------------------

load_dotenv()

# This function has no required arguments here.
#
# By default, it looks for a `.env` file and loads the
# variables inside it into the environment.


# ---------------------------------------------------------
# 5. Build the PostgreSQL database URL
# ---------------------------------------------------------

DATABASE_URL = (
    f"postgresql+psycopg2://"
    f"{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)
# looks like this: "postgresql+psycopg2://postgres:password@localhost:5432/task_management"

# This creates one string containing all the information
# SQLAlchemy needs to connect to PostgreSQL.
#
# The final result will look approximately like:
#
# postgresql+psycopg2://postgres:mypassword@localhost:5432/task_management
#
#
# Let's break it down:
#
# postgresql
# ----------
# Tells SQLAlchemy that our database is PostgreSQL.
#
#
# +psycopg2
# ---------
# Tells SQLAlchemy to use the psycopg2 Python driver
# to communicate with PostgreSQL.
#
#
# os.getenv('DB_USER')
# --------------------
# Gets the value of DB_USER from the environment.
#
# Example:
#
# DB_USER=postgres
#
# Then:
#
# os.getenv('DB_USER')
#
# returns:
#
# "postgres"
#
#
# os.getenv('DB_PASSWORD')
# ------------------------
# Gets the PostgreSQL password.
#
#
# os.getenv('DB_HOST')
# --------------------
# Gets the location of the PostgreSQL server.
#
# If PostgreSQL is running on our own computer:
#
# localhost
#
#
# os.getenv('DB_PORT')
# --------------------
# Gets the port PostgreSQL is listening on.
#
# PostgreSQL's default port is:
#
# 5432
#
#
# os.getenv('DB_NAME')
# -------------------
# Gets the name of the database we want to use.
#
# Example:
#
# task_management
#
#
# The `f` before each string means this is an f-string.
# It allows us to insert Python expressions using `{}`.


# ---------------------------------------------------------
# 6. Create SQLAlchemy Engine
# ---------------------------------------------------------

engine = create_engine(DATABASE_URL)

# `create_engine()` creates the SQLAlchemy Engine.
#
# Argument:
#
# DATABASE_URL
#
# tells the engine how to connect to PostgreSQL.
#
# The engine is basically SQLAlchemy's main connection
# interface to the database.
#
# It manages communication between:
#
# Python / FastAPI
#        ↓
#    SQLAlchemy
#        ↓
#    PostgreSQL


# ---------------------------------------------------------
# 7. Create a database session factory
# ---------------------------------------------------------

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# `sessionmaker()` creates a factory that can create
# individual database sessions.
#
#
# bind=engine
# ----------
# Connects this session factory to our SQLAlchemy engine.
#
# So when we create:
#
# db = SessionLocal()
#
# that session knows which database it should communicate
# with because it is bound to `engine`.
#
#
# autocommit=False
# ----------------
# Means SQLAlchemy will NOT automatically commit database
# changes.
#
# We will explicitly call:
#
# db.commit()
#
# when we want to permanently save changes.
#
# This gives us more control over transactions.
#
#
# autoflush=False
# ---------------
# Prevents SQLAlchemy from automatically flushing pending
# changes to the database before certain operations.
#
# We can control when changes are flushed/committed.


# ---------------------------------------------------------
# 8. Create a function that provides a database session
# ---------------------------------------------------------


def get_db():

    # Create a new database session using our factory.
    #
    # SessionLocal is the factory.
    # Calling SessionLocal() creates one actual session.
    db = SessionLocal()

    try:

        # `yield` gives the database session to whoever
        # requested it.
        #
        # In FastAPI, this function can be used as a
        # dependency.
        yield db

    finally:

        # `db.close()` closes the database session after
        # the request is finished.
        #
        # This is important because we don't want to leave
        # database sessions open unnecessarily.
        db.close()


# now for testing the connection, with posgres on linux
# from sqlalchemy import text

# # Test the connection to PostgreSQL
# try:
#     with engine.connect() as connection:
#         result = connection.execute(text("SELECT 1"))
#         print("Database response:", result.scalar())
#         print(" PostgreSQL connection successful!")

# except Exception as e:
#     print(" PostgreSQL connection failed!")
#     print("Error:", e)

##
