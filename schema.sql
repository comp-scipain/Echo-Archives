create table
    public.dept(
        dept_id INTEGER GENERATED BY DEFAULT AS IDENTITY, 
        created_at timestamp with time zone not null default now(),
        dept_name TEXT NULL,
        base_pay FLOAT,
        dept_populus INT,
        CONSTRAINT dept_id_pkey PRIMARY KEY (dept_id)
    ) tablespace pg_default;

create table 
    public.reviews(
        review_id BIGINT generated by default as identity,
        created_at timestamp with time zone not null default now(),
        employee_id bigint,
        performance_score integer, 
        review_text text,        
        reviewer_id bigint,      
        review_date timestamp with time zone
) tablespace pg_default;

create table 
    public.employees(
        employee_id bigint generated by default as identity,
        hire_date timestamp with time zone not null,
        name text null,
        skills text null,
        pay FLOAT,
        department text null,
        level integer,
        CONSTRAINT employees_pkey PRIMARY KEY (employee_id)
    ) tablespace pg_default;


create table 
    public.history(
        ledger_id BIGINT generated by default as identity,
        created_at timestamp with time zone not null default now(),
        emp_name text null,
        days_employed bigint,
        day_wage float,
        in_dept text null,
        emp_id bigint
        
    ) tablespace pg_default;
    """))