import csv
import random
from random import randint
import time
from datetime import datetime
import os
import psycopg2
from faker import Faker
import datetime

def generate(name, count, alpha):
    name = name + '.csv'
    try:
        csv_out = open('csv_sources/'+ name)
        csv_out.close()
        print(name + " is already generated")
    except:
        with open('csv_sources/'+ name, 'w',newline = '') as csv_out:
            try:
                csv_writer = csv.writer(csv_out, delimiter=',', quotechar="\"", quoting=csv.QUOTE_MINIMAL)

                for i in range(count):
                    new_row = alpha(i)
                    csv_writer.writerow(new_row)
            except:
                csv_out.close()
                os.remove( name)


def main():
    N = 100
    fake = Faker()

    group = lambda x: [x%6 + 1, "ICS", random.choice(["Bachelor", "Master"]), datetime.date.today().year - x//6 - 1]
    theme = lambda x: [str(x+1), random.randint(1, 10), datetime.date.today().year - randint(1, 3)]
    source = lambda x: [str(x+1), random.choice(["Web", "Report", "Book"]), str(x), datetime.date.today().year - randint(5, 20)]
    student = lambda x: [str(x+1), randint(1, N), x%6 + 1, fake.date_of_birth(minimum_age = 18, maximum_age = 27),datetime.date.today().year - x//6]
    project = lambda x: [str(randint(1, N)), str(randint(1,N)), randint(2, 5),  fake.date_between(-6)]
    source_project = lambda x: [randint(1, N), randint(1, N)]
    generate("group", N, group)
    generate("theme", N, theme)
    generate("source", N, source)
    generate("student", N, student)
    generate("project", N, project)
    generate("source_project",N, source_project)

    
    
if __name__ == "__main__":
    main()
