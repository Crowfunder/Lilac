# -*- coding: UTF-8 -*-
# by Crowfunder
# beta v0.3 HEADLESS (Added matplotlib graph generation, added dates to logs, added logs failsafe in case the logfile is too big)
# WARNING: Compiled on Windows does shit with diacritic marks. (FUCK YOU MICROSOFT FOR NOT USING NORMAL GODDAMN ENCODINGS)
# Copyright my ass.
import random, os, csv
from time import localtime, strftime
from datetime import date
from matplotlib import pyplot as plt
    
def csv_parse(fname):
    try:
        with open(fname) as file:
            words = {str(num):col for num,col in csv.reader(file)}
        return words
    except:
        return {"brak-slownika":"brak-slownika"}
        
def pl_to_en(dictionary, query):
    query = (query.lower()).strip()
    return str(list(dictionary.keys())[list(dictionary.values()).index(query)])

def en_to_pl(dictionary, query):
    query = (query.lower()).strip()
    return str(dictionary[query])
    
def comparator(query, question, dictionary):
    if question in list(dictionary.keys()):  #is in en
        return query == en_to_pl(dictionary, question)
    elif question in list(dictionary.values()):  #is in pl
        return query == pl_to_en(dictionary, question)
    
def get_date():
    hour = localtime()
    hour = strftime("%H:%M:%S")
    return hour
    
# Logs player's scores in csv readable format. Will be used for graph creation.
def logger(score, counter):
    ratio = round(score/counter, 1)
    today = get_date()
    with open("log.log", "a+") as file:
        if os.stat("log.log").st_size == 0:
            file.write("score,max,ratio,date\n")
        file.write(f"{score},{counter},{ratio},{today}\n")
        
def log_failsafe():
    if sum(1 for line in open('log.log')) > 100:
        log_flush()

def graph(logfile):
    with open(logfile, "r") as file:
        x = [row["date"] for row in csv.DictReader(file)]
    with open(logfile, "r") as file:
        y = [row["ratio"] for row in csv.DictReader(file)]
    y = [float(i) for i in y]
    plt.plot(x,y)
    plt.gcf().autofmt_xdate()
    plt.title("Twoje Wyniki")
    plt.xlabel("Czas")
    plt.ylabel("Trafione odpowiedzi/pytania")
    plt.show()
    

def log_flush():
    open('log.log', 'w').close()

def random_en(dictionary, question):
    output = random.choice(list(dictionary.keys()))
    while output == question:
        output = random.choice(list(dictionary.keys()))
    return output
    
def random_pl(dictionary, question):
    output = random.choice(list(dictionary.values()))
    while output == question:
        output = random.choice(list(dictionary.values()))
    return output

# Function strictly for debugging! Gives full CLI experience. It also presents the planned functionality logic.
# Yes, I know this function is a mess, it should be commented out/removed for future releases!
# It's meant to be a single goddamn messy function.
def debug(dictionary):
    maxword = len(dictionary)
    score = 0
    not_used = dictionary
    question = ""
    while 1<2:
        while 1<2:
            try:
                counter = input("""Ile słówek? (Wpisz "wszystkie" by wybrać wszystkie słówka) """)
                if counter == "wszystkie":
                    counter = maxword
                counter = int(counter)
                break
            except ValueError:
                print("Zły wybór! Musi być liczbą!")
        if counter > maxword or counter <= 0:
            print(f"Liczba nie może być większa niż {maxword} i mniejsza lub równa 0!")
        else:
            break
    while 1<2:
        mode = str(input("1) Angielski > Polski\n2) Polski > Angielski\n3) Oba\nWybierz tryb: "))
        if mode in ["1", "2", "3"]:
            break
        else:
            print("Zły wybór!")
    if mode == "1":
        for i in range (0,counter):
            question = random_en(not_used, question)
            query = input(f"\n{question} > ")
            ans = en_to_pl(dictionary, question)
            if comparator(query, question, dictionary) == True:
                score += 1
                not_used.pop(question)
            else:
                print(f"Zła odpowiedź! Powinno być: {ans}")
    if mode == "2":
        for i in range (0,counter):
            question = random_pl(not_used, question)
            query = input(f"\n{question} > ")
            ans = pl_to_en(dictionary, question)
            if comparator(query, question, dictionary) == True:
                score += 1
                not_used.pop(ans)
            else:
                print(f"Zła odpowiedź! Powinno być: {ans}")
    if mode == "3":
        for i in range (0,counter):
            lan = random.choice(["ang", "pl"])
            if lan == "ang":
                question = random_en(not_used, question)
                query = input(f"\n{question} > ")
                ans = en_to_pl(dictionary, question)
                if comparator(query, question, dictionary) == True:
                    score += 1
                    not_used.pop(question)
                else:
                    print(f"Zła odpowiedź! Powinno być: {ans}")
            if lan == "pl":
                question = random_pl(not_used, question)
                query = input(f"\n{question} > ")
                ans = pl_to_en(dictionary, question)
                if comparator(query, question, dictionary) == True:
                    score += 1
                    not_used.pop(ans)
                else:
                    print(f"Zła odpowiedź! Powinno być: {ans}")
    percent = str(round((score/counter)*100, 1)) + "%"
    logger(score, counter)
    print(f"Gratulacje! Masz {score} na {counter} punktów! ({percent})")
    graph("log.log")

def main():
    words = csv_parse("slownik.txt")
    debug(words)
    
if __name__ == '__main__':
    main()
