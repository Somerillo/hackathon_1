# here we call the mock tracker and fetch the health data from its dictionary
# we also fetch the weather status at the begining of the session
# fetch the starting time and the ending time
# calculate burnt calories and distance traveled
# feed the data into the user database

# The general idea for this feature is to run a while loop that will stop when the user decides to stop session,
# i know its possible, but it scapes the scope of this project. So we will only run for 60 cycles to emulate an hour training

from config import my_apy_key
from weather_api import Get_Weather
from mock_tracker import MockTracker
from datetime import datetime as dt
import pandas as pd
import time
from matplotlib import pyplot as plt


class SessionManager:
    """
    By default we use MockTracker as a fitness traker, but the idea should be something like say a smartwatch\n
    Because we cant keep the inner loop running until the user stops the counter (word = "exit"), i.e. ends training session\n
    we need to stablish manually a cycle limit (top_cycle_limit), such as a time step of 0.1 seconds to make it faster
    """
    def __init__(self, tracker=MockTracker, top_cycle_limit=60, time_step=60):
        # i know i defined by default time_step at 60, that is for the case of a real session
        # but now we want fast results, so i set time_step to 0.1
        # once we connect this to a real tracker and run a real session the line below should be commented
        self.time_step = 0.01
        # this variable should be able to change while the loop is running
        self.word = ""
        # the mock tracker should be replaced by a real tracker, like say a smartwatch
        self.tracker = tracker
        # top cycles limit
        self.top = top_cycle_limit

    def start_session(self):
        """
        gets all the initial stats for the stats loving nerds
        """
        self.start_time = dt.now()
        self.start_time_readable = dt.now().strftime("%Y-%m-%d %H:%M:%S") # in a format we can actually read like normal people
        self.session_date = dt.now().date()

    def run_session(self):
        """
        calls the tracker and gets its health stats
        """
        self.start_session()

        self.rows = []
        k = 0
        while k < self.top and self.word != "exit":
            time.sleep(self.time_step) # we start registering a time_step after the session started
            data = self.tracker().get_all_data()
            data2 = {"time": self.time_step * (k+1)}
            data2.update(data)
            self.rows.append(data2)
            k += 1

        self.stop_time = dt.now() # registers time after the loop ended
        self.build_df()
        self.plot_stats()

    def build_df(self):
        """
        I know we didnt see yet dataframes, i dont care
        """
        self.df = pd.DataFrame(self.rows)

    def get_stats(self):
        """
        more stats for nerds (yay!)
        """
        stats = {
            "total_steps": self.df["steps"].sum(),
            "avg_hr": round(self.df["heart_rate"].mean()),
            "max_hr": self.df["heart_rate"].max(),
            "min_hr": self.df["heart_rate"].min(),
            "avg_bp_sys": round(self.df["blood_pressure_sys"].mean()),
            "max_bp_sys": self.df["blood_pressure_sys"].max(),
            "min_bp_sys": self.df["blood_pressure_sys"].min(),
            "avg_bp_dia": round(self.df["blood_pressure_dia"].mean()),
            "max_bp_dia": self.df["blood_pressure_dia"].max(),
            "max_ox": self.df["oxygen"].max(),
            "min_bp_dia": self.df["blood_pressure_dia"].min(),
            "avg_ox": round(self.df["oxygen"].mean()),
            "min_ox": self.df["oxygen"].min(),
            "start_time": self.start_time_readable,
            "total_time": (self.stop_time - self.start_time).total_seconds(),
            "session_date": self.session_date
        }
        return stats

    def plot_stats(self):
        fig, axs = plt.subplots(2, 2, figsize=(10, 10))  # 2 rows, 2 columns
        x = self.df["time"]

        axs[0, 0].bar(x, self.df["steps"], width=self.time_step*3/4)
        axs[0, 0].set_title(f"Steps\nTotal: {self.get_stats()["total_steps"]}")
        axs[0, 0].set_ylim(bottom=0)

        axs[0, 1].plot(x, self.df["heart_rate"])
        axs[0, 1].set_title(
            f"Heart Rate [bpm]\n"
            f"Max: {self.get_stats()["max_hr"]}    "
            f"Avg: {self.get_stats()["avg_hr"]}    "
            f"Avg: {self.get_stats()["min_hr"]}"
            )

        axs[0, 1].set_ylim(bottom=30, top=200)
        axs[0, 1].yaxis.grid(True, color="gray", linewidth=0.1)

        axs[1, 0].plot(x, self.df["blood_pressure_sys"], label="systolic")
        axs[1, 0].plot(x, self.df["blood_pressure_dia"], label="diastolic")
        axs[1, 0].set_title(
            f"Blood Pressure [mmHg]\n"
            f"Systolic    ( Max: {self.get_stats()['max_bp_sys']}    Avg: {self.get_stats()['avg_bp_sys']}    Min: {self.get_stats()['min_bp_sys']} )\n"
            f"Diastolic   ( Max: {self.get_stats()['max_bp_dia']}      Avg: {self.get_stats()['avg_bp_dia']}      Min: {self.get_stats()['min_bp_dia']} )"
        )

        axs[1, 0].set_ylim(bottom=30, top=210)
        axs[1, 0].yaxis.grid(True, color="gray", linewidth=0.1)
        axs[1, 0].legend()

        axs[1, 1].plot(x, self.df["oxygen"])
        axs[1, 1].set_title(
            f"% Oxygen in Blood\n"
            f"Max: {self.get_stats()['max_ox']}    "
            f"Avg: {self.get_stats()['avg_ox']}    "
            f"Min: {self.get_stats()['min_ox']}"
            )
        axs[1, 1].yaxis.grid(True, color="gray", linewidth=0.1)
        axs[1, 1].set_ylim(bottom=80, top=110)

        fig.suptitle(
            f"Session date: {self.start_time}                "
            f"Total time: {self.get_stats()["total_time"]/60:.2f} minutes",
            fontsize=18,
            # fontweight="bold",
            # ha="right"
            )

        plt.tight_layout()
        plt.show()




## ----------------------------------------- testing... ----------------------------------------- ##
# test = SessionManager()
# run_test = test.run_session()
# stats = test.get_stats()
# print(stats)