import psycopg2  # to export to the db
from faker import Faker  # generate names, mail, etc
import random  # won`t explain
from config import HOSTNAME, USERNAME, PASSWORD, DATABASE, PORT

# instantiate Faker
fake = Faker()

# connect to db
conn = psycopg2.connect(database=DATABASE,
                        user=USERNAME,
                        password=PASSWORD,
                        host=HOSTNAME,
                        port=PORT)

cursor = conn.cursor()


# define bmi calculator function
def bmi_calculator(weight, height):
    """
    this function calculates the BMI
    based on wikipedia page:
    \nhttps://en.wikipedia.org/wiki/Body_mass_index
    """
    return round(weight / height**2, 1)


# number of fake users to generate
total_users = int(input("Specify the amount of fake users to insert in the dabase: "))

for _ in range(total_users):
    user_mail = fake.email()
    is_male = random.choice([True, False])
    last_name = fake.last_name()

    # distiguish if male/female for the name
    if is_male:
        first_name = fake.first_name_male()
    else:
        first_name = fake.first_name_female()

    # this should be a normal right skewed distribution, but that goes beyond the scope of this project
    birth_date = fake.date_of_birth(minimum_age=18, maximum_age=99)

    # To get `realistic` height/weight distribution we employ a normal dist for each gender
    # but both variables should be related, so far as how our code is written will get extremelly
    # thin tall people and extremelly obesse short people.
    # To fix this we need to get a normal BMI distriution by gender with any height or weight, and from there the third one;
    # but not as we did below with the BMI at the end.
    # height data:
    # *     https://ourworldindata.org/human-height
    # *     https://www.statology.org/example-of-normal-distribution/
    # *     https://www.elconfidencial.com/tecnologia/ciencia/2024-03-04/altura-media-crecimiento-hombres-mujeres_3842169/
    # weight data:
    # *     https://www.cdc.gov/nchs/data/ad/ad347.pdf
    if is_male:
        height_m = round(random.gauss(1.78, 0.076), 2)
        weight_kg = round(random.gauss(86.18, 13.6), 2)
    else:
        # meters and kilograms
        height_m = round(random.gauss(1.63, 0.063), 2)
        weight_kg = round(random.gauss(73.94, 11.34), 2)

    # now we get the initial BMI
    bmi = bmi_calculator(weight_kg, height_m)

    # define the query
    insert_query = """
    INSERT INTO users (user_mail, first_name, last_name, is_male, birth_date, weight_kg, height_m, bmi)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """

    # execute query
    cursor.execute(insert_query, (user_mail, first_name, last_name, is_male, birth_date, weight_kg, height_m, bmi))


# confirm changes & close connection
conn.commit()
cursor.close()
conn.close()

print(f"{total_users} users have been inserted in the database {DATABASE}")