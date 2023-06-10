import csv
import random
from random import randint
import time
from datetime import datetime
import os
import psycopg2
from faker import Faker
import datetime

N = 100

def generate(cnt):
    name = f'csv_sources/test_student{cnt}.csv'
    student = lambda x: [str(x+1), randint(1, N), x%6 + 1, datetime.date.today(),datetime.date.today().year]
    with open(name, 'w',newline = '') as csv_out:
        csv_writer = csv.writer(csv_out, delimiter=',', quotechar="\"", quoting=csv.QUOTE_MINIMAL)
        for i in range(cnt):
            new_row = student(i)
            csv_writer.writerow(new_row)


def main():
    for i in ([5000000, 10000000]):
    # for i in ([100]):
        generate(i)
        print(i, "done")

    
    
if __name__ == "__main__":
    main()
