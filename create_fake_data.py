import sqlalchemy
import os
import dotenv
from faker import Faker
import numpy as np

def database_connection_url():
    dotenv.load_dotenv()
    DB_USER: str = os.environ.get("POSTGRES_USER")
    DB_PASSWD = os.environ.get("POSTGRES_PASSWORD")
    DB_SERVER: str = os.environ.get("POSTGRES_SERVER")
    DB_PORT: str = os.environ.get("POSTGRES_PORT")
    DB_NAME: str = os.environ.get("POSTGRES_DB")
    return f"postgresql://{DB_USER}:{DB_PASSWD}@{DB_SERVER}:{DB_PORT}/{DB_NAME}"

# Create a new DB engine based on our connection string
engine = sqlalchemy.create_engine(database_connection_url(), use_insertmanyvalues=True)

with engine.begin() as conn:
    conn.execute(sqlalchemy.text("""
    DROP TABLE IF EXISTS public.employees;
    DROP TABLE IF EXISTS public.dept;

    create table
    public.dept(
        dept_id INTEGER GENERATED BY DEFAULT AS IDENTITY, 
        created_at timestamp with time zone not null default now(),
        dept_name TEXT NULL,
        dept_id INTEGER NOT NULL UNIQUE,
        base_pay FLOAT,
        dept_populus INT,
        CONSTRAINT dept_id_pkey PRIMARY KEY (dept_id)
    ) tablespace pg_default;


    create table 
    public.employees(
        employee.id bigint generated by default as identity,
        hire_date timestamp with time zone not null,
        name text null,
        skills text null,
        pay REAL,
        department text null,
        level integer,
        CONSTRAINT employees_pkey PRIMARY KEY (employee_id)
    ) tablespace pg_default;


    create table 
    public.history(
        ledger_id bigint generated by default as identity,
        created_at timestamp with time zone not null default now(),
        emp_name text null,
        days_employed bigint,
        day_wage float,
        in_dept text null,
        emp_id bigint
        
    ) tablespace pg_default;
    """))
    

num_users = 1000000
fake = Faker()
posts_sample_distribution = np.random.default_rng().negative_binomial(0.04, 0.01, num_users)
category_sample_distribution = np.random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                                                 num_users,
                                                p=[0.1, 0.05, 0.1, 0.3, 0.05, 0.05, 0.05, 0.05, 0.15, 0.1])
total_posts = 0

# create fake posters with fake names and birthdays
with engine.begin() as conn:
    print("creating fake data...")
    posts = []
    for i in range(num_users):
        if (i % 10 == 0):
            print(i)
        
        profile = fake.profile()
        username = fake.unique.email()
        device_type = fake.random_element(elements=('Android', 'iOS', 'Web'))


        pay, base_pay, day_wage = fake.pyfloat()
        dept_id, dept_populus, level, id, emp_id, ledger_id = fake.pyint()

        dept = conn.execute(sqlalchemy.text("INSERT INTO dept (dept_name, dept_id, base_pay, dept_populus) VALUES (:dept_name, :dept_id, :base_pay, :dept_populus)"),
        {"dept_name":,"dept_id":dept_id,"base_pay":base_pay,"dept_populus":dept_populus})

        employees = conn.execute(sqlalchemy.text("INSERT INTO employee (id, name, skills, pay, department, level, hire_date) VALUES (:id, :name, :skills, :pay, :department, :level, :hire_date)"),
        {"id":id,"name":,"skills":,"pay":pay,"department":,"level":level,"hire_date":})

        history = conn.execute(sqlalchemy.text("INSERT INTO history (ledger_id, created_at, emp_name, day_wage, in_dept, emp_id) VALUES (:ledger_id, :created_at,:emp_name,:day_wage,:in_dept,:emp_id)"),
        {"ledger_id":ledger_id,"created_at":,"emp_name","day_wage":day_wage,"in_dept":,"emp_id":})


        poster_id = conn.execute(sqlalchemy.text("""
        INSERT INTO users (username, full_name, birthday, device_type) VALUES (:username, :name, :birthday, :device_type) RETURNING id;
        """), {"username": username, "name": profile['name'], "birthday": profile['birthdate'], "device_type": device_type}).scalar_one()

        num_posts = posts_sample_distribution[i]
        likes_sample_distribution = np.random.default_rng().negative_binomial(0.8, 0.0001, num_posts)  
        for j in range(num_posts):
            total_posts += 1
            posts.append({
                "title": fake.sentence(),
                "content": fake.text(),
                "poster_id": poster_id,
                "category_id": category_sample_distribution[i].item(),
                "visible": fake.boolean(75),
                "created_at": fake.date_time_between(start_date='-5y', end_date='now', tzinfo=None),
                "likes": likes_sample_distribution[j].item(),
                "nsfw": fake.boolean(10)
            })

    if posts:
        conn.execute(sqlalchemy.text("""
        INSERT INTO posts (title, content, poster_id, category_id, visible, created_at) 
        VALUES (:title, :content, :poster_id, :category_id, :visible, :created_at);
        """), posts)

    print("total posts: ", total_posts)
    
