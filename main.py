# This is the script that runs everything together


from session_manager import SessionManager
from weather_api import Get_Weather
import psycopg2
from config import HOSTNAME, USERNAME, PASSWORD, DATABASE, PORT, my_apy_key
import random


# we dont have a geolocator module, so we input location manually
cities = ["Ashkelon,IL", "Tel Aviv,IL", "Los Angeles,US", "Tokyo,JP", "Ushuaia,AR",
          "New York,US", "Paris,FR", "Sydney,AU", "Rio de Janeiro,BR", "Buenos Aires,AR"]
city = random.choice(cities)

# user mails from the users table, should delete this after testing
mails = [
    "michaellee@example.com", "xhoward@example.org", "richardrichards@example.net", "jhoward@example.net", "morgan14@example.com",
    "mariaboyd@example.org", "hernandezvanessa@example.net", "caitlinharris@example.org", "amandaestes@example.org", "harrisjohn@example.org",
    "ewingraymond@example.com", "langjason@example.com", "smithkaren@example.org", "pamela69@example.com",
    "obrienisaac@example.org", "charlesscott@example.org", "vzavala@example.com", "wisematthew@example.org",
    "pbenson@example.com", "thomas53@example.com", "mwatson@example.org", "wellsheather@example.com", "mario05@example.net", "david27@example.org",
    "robert91@example.com", "derrickcalhoun@example.net", "whill@example.org", "mtaylor@example.org", "barnesjustin@example.net", "nelsonian@example.com",
    "pgonzalez@example.org", "jeremy92@example.org", "mirandakelsey@example.org", "georgejacqueline@example.org",
    "selena78@example.com", "nathan22@example.com", "susan40@example.org", "david72@example.com",
    "lindsay64@example.org", "troyjones@example.org", "kochdylan@example.org", "coxbernard@example.org",
    "wcarter@example.org", "thardin@example.net", "george55@example.org", "katherineallen@example.net",
    "jason35@example.net", "vjackson@example.org", "daniel65@example.org", "dennis37@example.com",
    "gary45@example.net", "kjones@example.org", "stonedanielle@example.org", "atkinsonbobby@example.com",
    "nmack@example.org", "carl87@example.net", "jbrooks@example.com", "laura65@example.net",
    "kelseyanderson@example.com", "sandrahaas@example.org"
]


# connect to db
conn = psycopg2.connect(database=DATABASE,
                        user=USERNAME,
                        password=PASSWORD,
                        host=HOSTNAME,
                        port=PORT)

cursor = conn.cursor()


class Main:
    """
    one class to run them all
    """

    def __init__(self):
        print(f"\n{"-" * 68}")
        print(ascii_art)
        print(f"\n{"-" * 68}\n\n")
        self.city = city
        self.check_email()

    def check_email(self):
        """
        checks if e-mail in users_table from database if count > 0, redundant because the e-mail is the primary key
        """
        while True:
            self.user_mail = input(
                "input e-mail to start session, input `random` for random user, or `q` to quit: ")

            if self.user_mail.lower() == "q":
                print("exiting...")
                break  # exit the bucle
            elif self.user_mail.lower() == "random":
                self.user_mail = random.choice(mails)

            cursor.execute(
                "SELECT COUNT(*) FROM users WHERE user_mail = %s", (self.user_mail,))
            count = cursor.fetchone()[0]

            if count > 0:
                # after the user is validated we access the rest of the data
                self.get_user_data()

                # weather related stuff
                self.fetch_weather()
                print(
                    f"\n\n\n\n\nHello {self.first_name} {self.last_name}\n"
                    f"\nThe weather status in `{self.city}` is {self.weather_data["description"]} "
                    f"with {self.weather_data["temperature"]} °C "
                    f"and {self.weather_data["humidity"]}% humidity, "
                    f"the current wind speed is {self.weather_data["wind"]["speed"]} m/s.\n"
                )

                # user session related stuff
                input("\ninput any command to start tracking: ")
                print()
                self.instantiate_session()
                self.session_data.run_session()
                self.stats = self.session_data.get_stats()

                # export to the sessions table
                self.export_session()

                break  # exit the bucle
            else:
                print("the e-mail doesnt belong to a user in the database, try again")

    def get_user_data(self):
        cursor.execute("""
            SELECT first_name, last_name, is_male, birth_date, weight_kg, height_m, bmi 
            FROM users 
            WHERE user_mail = %s
        """, (self.user_mail,))  # need tuple for db!!!

        # get all results
        results = cursor.fetchall()

        if results:
            # only 1st row, its a redundancy because the mail doesnt repeat
            # BUT in case its repeated we could have more than one row, and we want only one
            user_data = results[0]

            self.first_name = user_data[0]
            self.last_name = user_data[1]
            self.is_male = user_data[2]
            self.birth_date = user_data[3]
            self.weight_kg = user_data[4]
            self.height_m = user_data[5]
            self.bmi = user_data[6]

        else:
            print(
                "provided email doest exists... this shouldnt be printed because we checked the mail exists")

    def fetch_weather(self):
        self.weather_data = Get_Weather(my_apy_key, self.city).get_all_data()

    def instantiate_session(self):
        self.session_data = SessionManager()

    def export_session(self):
        try:
            cursor.execute("""
                INSERT INTO sessions (
                    user_mail, start_time, total_time_s, total_steps, avg_hr_bpm, max_hr_bpm, min_hr_bpm,
                    avg_bp_sys_mmHg, max_bp_sys_mmHg, min_bp_sys_mmHg, avg_bp_dia_mmHg, max_bp_dia_mmHg, min_bp_dia_mmHg,
                    max_ox, avg_ox, min_ox, temperature_C, city, weather_status
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
            """, (
                self.user_mail,
                self.stats['start_time'],
                self.stats['total_time'],
                int(self.stats['total_steps']),
                int(self.stats['avg_hr']),
                int(self.stats['max_hr']),
                int(self.stats['min_hr']),
                int(self.stats['avg_bp_sys']),
                int(self.stats['max_bp_sys']),
                int(self.stats['min_bp_sys']),
                int(self.stats['avg_bp_dia']),
                int(self.stats['max_bp_dia']),
                int(self.stats['min_bp_dia']),
                int(self.stats['max_ox']),
                int(self.stats['avg_ox']),
                int(self.stats['min_ox']),
                self.weather_data['temperature'],
                self.city,
                self.weather_data['status']
            ))
            conn.commit()
            print("session data exported to database")
        except Exception as e:
            print("fuuuuuuuuuuuuuuuuuuuuuu", str(e))


ascii_art = r"""
   __ _ _                         _                  _             
  / _(_) |                       | |                | |            
 | |_ _| |_ _ __   ___  ___ ___  | |_ _ __ __ _  ___| | _____ _ __ 
 |  _| | __| '_ \ / _ \/ __/ __| | __| '__/ _` |/ __| |/ / _ \ '__|
 | | | | |_| | | |  __/\__ \__ \ | |_| | | (_| | (__|   <  __/ |   
 |_| |_|\__|_| |_|\___||___/___/  \__|_|  \__,_|\___|_|\_\___|_|   
"""


# call the class to execute
Main().get_user_data()

# close conection
cursor.close()
conn.close()
