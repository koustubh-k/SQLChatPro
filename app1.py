import psycopg2
from psycopg2 import sql
from psycopg2 import Error

def create_and_populate_students_table(cursor):
    """Creates and populates the 'students' table."""
    create_table_query = sql.SQL("""
        CREATE TABLE IF NOT EXISTS students (
            student_id SERIAL PRIMARY KEY,
            first_name VARCHAR(50) NOT NULL,
            last_name VARCHAR(50) NOT NULL,
            enrollment_date DATE
        );
    """)
    cursor.execute(create_table_query)
    print("Table 'students' created successfully.")

    insert_data_query = sql.SQL("""
        INSERT INTO students (first_name, last_name, enrollment_date)
        VALUES
        ('Alice', 'Johnson', '2022-09-01'),
        ('Bob', 'Williams', '2022-09-01'),
        ('Charlie', 'Brown', '2023-01-15'),
        ('Diana', 'Miller', '2023-01-15'),
        ('Eve', 'Davis', '2022-09-01'),
        ('Frank', 'Wilson', '2024-03-20');
    """)
    cursor.execute(insert_data_query)
    print("Dummy data for 'students' inserted successfully.")

def create_and_populate_courses_table(cursor):
    """Creates and populates the 'courses' table."""
    create_table_query = sql.SQL("""
        CREATE TABLE IF NOT EXISTS courses (
            course_id SERIAL PRIMARY KEY,
            course_name VARCHAR(100) NOT NULL,
            credits INTEGER
        );
    """)
    cursor.execute(create_table_query)
    print("Table 'courses' created successfully.")
    
    insert_data_query = sql.SQL("""
        INSERT INTO courses (course_name, credits)
        VALUES
        ('Database Systems', 3),
        ('Data Structures', 4),
        ('Web Development', 3),
        ('Artificial Intelligence', 4);
    """)
    cursor.execute(insert_data_query)
    print("Dummy data for 'courses' inserted successfully.")

def create_and_populate_enrollments_table(cursor):
    """Creates a junction table to link students and courses."""
    create_table_query = sql.SQL("""
        CREATE TABLE IF NOT EXISTS enrollments (
            enrollment_id SERIAL PRIMARY KEY,
            student_id INTEGER REFERENCES students(student_id),
            course_id INTEGER REFERENCES courses(course_id),
            grade VARCHAR(2)
        );
    """)
    cursor.execute(create_table_query)
    print("Table 'enrollments' created successfully.")

    insert_data_query = sql.SQL("""
        INSERT INTO enrollments (student_id, course_id, grade)
        VALUES
        (1, 1, 'A'), (1, 2, 'B'),
        (2, 3, 'A'), (3, 1, 'C'),
        (4, 4, 'B'), (5, 2, 'A'),
        (6, 1, 'B');
    """)
    cursor.execute(insert_data_query)
    print("Dummy data for 'enrollments' inserted successfully.")

def run_database_setup():
    """Main function to connect and run all table creation."""
    connection = None
    try:
        connection = psycopg2.connect(
            user="postgres",
            password="2809",
            host="localhost",
            port="5432",
            database="demodb"
        )
        cursor = connection.cursor()

        # Run the functions to create and populate the tables
        create_and_populate_students_table(cursor)
        create_and_populate_courses_table(cursor)
        create_and_populate_enrollments_table(cursor)
        
        connection.commit()
        print("All database operations completed successfully.")

    except (Exception, Error) as error:
        print(f"Error while connecting to or interacting with PostgreSQL: {error}")
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed.")

if __name__ == '__main__':
    run_database_setup()