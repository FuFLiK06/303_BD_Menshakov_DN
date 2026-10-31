#!/bin/bash
python db_init.py
sqlite3 movies_rating.db < db_init.sql