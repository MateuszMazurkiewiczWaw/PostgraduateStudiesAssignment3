Postgraduate studies - Assignment 3

# Exercise 1 - Adding 2 rows to the newly created Experiments table
# Exercise 2 - Adding 10 rows to the newly created DataPoints table (5 of each experiment exp1 and exp2)
# Exercise 3 - Fetching and presenting of all available records
# Exercise 4 - Bulk update of the Experiments table (setting the finished flag = True)
# Exercise 5 - Many-to-Many Relationship Demo (Subject table ↔ Experiments table)
# Exercise 6 - Bulk deletion of all records (including the intermediate table)

# Alembic DB data migration - sample steps
# 1. Delete an old DB - if it already exists after previous run
rm src/assignment_project3/assignment.db
# 2. Temporarily remove the Subject class and experiment_subject table from models.py. Leave only Experiment and DataPoint + the 1-to-many relationship.
# 3. Generate new migration
cd src/assignment_project3
alembic revision --autogenerate -m "Initial with Experiment and DataPoint"
alembic upgrade head
# 4. Add back Subject class + experiment_subject table + M2M relationship in models.py script.
# 5. Generate second migration
alembic revision --autogenerate -m "Add Subject and M2M relation"
alembic upgrade head
alembic current                -> it will provide the ID of the last migration
alembic history --verbose      -> it will all migrations history