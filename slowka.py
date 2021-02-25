# -*- coding: UTF-8 -*-
# by Crowfunder
# beta v0.1 HEADLESS (Working CLI)
# WARNING: Compiled on Windows does shit with diacritic marks. (FUCK YOU MICROSOFT FOR NOT USING NORMAL GODDAMN ENCODINGS)
# Copyright my ass.
import csv, random
    
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
    
def logger(score, max):
    pass

def random_en(dictionary):
    return random.choice(list(dictionary.keys()))
    
def random_pl(dictionary):
    return random.choice(list(dictionary.values()))

# Function strictly for debugging! Gives full CLI experience. It also presents the planned functionality logic.
# Yes, I know this function is a mess, it should be commented out/removed for releases!
# It's meant to be a single goddamn messy function.
def debug(dictionary):
    maxword = len(dictionary)
    score = 0
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
            print(f"Liczba nie może być większa niż {counter} i mniejsza lub równa 0!")
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
            question = random_en(dictionary)
            query = input(f"\n{question} > ")
            ans = en_to_pl(dictionary, question)
            if comparator(query, question, dictionary) == True:
                score += 1
            else:
                print(f"Zła odpowiedź! Powinno być: {ans}")
    if mode == "2":
        for i in range (0,counter):
            question = random_pl(dictionary)
            query = input(f"\n{question} > ")
            ans = pl_to_en(dictionary, question)
            if comparator(query, question, dictionary) == True:
                score += 1
            else:
                print(f"Zła odpowiedź! Powinno być: {ans}")
    if mode == "3":
        for i in range (0,counter):
            lan = random.choice(["ang", "pl"])
            if lan == "ang":
                question = random_en(dictionary)
                query = input(f"\n{question} > ")
                ans = en_to_pl(dictionary, question)
                if comparator(query, question, dictionary) == True:
                    score += 1
                else:
                    print(f"Zła odpowiedź! Powinno być: {ans}")
            if lan == "pl":
                question = random_pl(dictionary)
                query = input(f"\n{question} > ")
                ans = pl_to_en(dictionary, question)
                if comparator(query, question, dictionary) == True:
                    score += 1
                else:
                    print(f"Zła odpowiedź! Powinno być: {ans}")
    percent = str((score/counter)*100) + "%"
    print(f"Gratulacje! Masz {score} na {counter} punktów! ({percent})")

def main():
    words = csv_parse("slownik.txt")
    debug(words)
    
if __name__ == '__main__':
    main()