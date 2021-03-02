# by Crowfunder
# beta v0.4.2 (Fixed Minor Bugs)
# Copyright my ass but also the MIT License
# Github: https://github.com/Crowfunder/Lilac
import random, os, csv, traceback
import PySimpleGUI as sg
from time import localtime, strftime
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        
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
        
# Checks if the logfile is too big by comparing to the set limiter.
def log_failsafe(limiter):
    if os.path.isfile("log.log"):
        if sum(1 for line in open('log.log')) > int(limiter):
            file_flush('log.log')

def file_flush(fname):
    open(fname, 'w').close()

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

def menu():
    default_settings = {
        "log_limit" : 400,
        "theme" : "DarkPurple4"
    }
    setfile = "Lilac.settings"
    if not os.path.isfile(setfile):
        write_settings(setfile, default_settings)
    elif os.stat(setfile).st_size == 0:
        write_settings(setfile, default_settings)
    settings = csv_parse(setfile)
    sg.theme(settings["theme"])
    words = csv_parse("slownik.txt")
    maxword = len(words)
    log_failsafe(int(settings["log_limit"]))
    layout = [[sg.Text('Witaj w Lilac! \nWybierz Tryb Rozgrywki', 
                       size=(22,2), font=("Fixedsys", 15), justification="center")],
      [sg.Text('_'*30)],
      [sg.Image(filename="assets/Lilac.png")],
      [sg.Text('_'*30)],
      [sg.Button("Angielski na Polski", size=(20,1), font="Fixedsys")],
      [sg.Button("Polski na Angielski", size=(20,1), font="Fixedsys")],
      [sg.Button("Mieszane", size=(20,1), font="Fixedsys")],
      [sg.Text('_'*30)],
      [sg.Button("Statystyki", size=(20,1), font="Fixedsys")],
      [sg.Button("Ustawienia", size=(20,1), font="Fixedsys")],
      [sg.Button("Wyjdź", size=(20,1), button_color=("white", "red"), font="Fixedsys")],
      [sg.Text('_'*30)],
      [sg.Text("Made with love by Crowfunder.\nLogo by Nadia <3\n________________\nv0.4.2 beta", 
               font=["Courier", 8], justification='c')]
    ]
    window = sg.Window('Lilac', layout, element_justification='c').Finalize()
    while True:
        event, values = window.Read()    
        if event in (None, 'Wyjdź'):
            break
        elif event == "Angielski na Polski":
            window.close()
            counter = get_counter(maxword)
            mode_wrapper(words, counter, "ang")
        elif event == "Polski na Angielski":
            window.close()
            counter = get_counter(maxword)
            mode_wrapper(words, counter, "pl")
        elif event == "Mieszane":
            window.close()
            counter = get_counter(maxword)
            mode_wrapper(words, counter, "oba")
        elif event == "Statystyki":
            window.close()
            graph("log.log")
        elif event == "Ustawienia":
            window.close()
            menu_settings(settings, default_settings, setfile)
            
# I have little to no idea what it does, but since it works...
def draw_figure(canvas, figure, loc=(0, 0)):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

# The PySimpleGUI x MatPlotLib part was pulled entirely from the PySimpleGUI examples, it just works, don't touch it. 
def graph(logfile):
    layout = [[sg.Text('Tworzenie wykresu w toku...')],
              [sg.ProgressBar(1, orientation='h', size=(20, 20), key='progress')],
             ]
    if not os.path.isfile(logfile):
        file = open(logfile, "w")
        file.close()
    window = sg.Window('Lilac', layout).Finalize()
    progress_bar = window.FindElement('progress')
    progress_bar.UpdateBar(0, 7)
    with open(logfile, "r") as file:
        x = [row["date"] for row in csv.DictReader(file)]
    progress_bar.UpdateBar(1, 7)
    with open(logfile, "r") as file:
        y = [row["ratio"] for row in csv.DictReader(file)]
    y = [float(i) for i in y]
    progress_bar.UpdateBar(2, 7)
    plt.plot(x,y)
    progress_bar.UpdateBar(3, 7)
    plt.gcf().autofmt_xdate()
    progress_bar.UpdateBar(4, 7)
    plt.title("Twoje Wyniki")
    progress_bar.UpdateBar(5, 7)
    plt.xlabel("Godzina")
    progress_bar.UpdateBar(6, 7)
    plt.ylabel("Trafione odpowiedzi / Liczba Pytań")
    progress_bar.UpdateBar(7, 7)
    window.Close()
    fig = plt.gcf()
    figure_x, figure_y, figure_w, figure_h = fig.bbox.bounds
    layout = [[sg.Canvas(size=(figure_w, figure_h), key='-CANVAS-')],
          [sg.OK(pad=((figure_w / 2, 0), 3), size=(4, 2))]]
    window = sg.Window('Lilac', layout, force_toplevel=True, finalize=True)
    fig_photo = draw_figure(window['-CANVAS-'].TKCanvas, fig)
    event, values = window.read()
    if event == "OK":
        window.close()
        menu()
      
def bad_ans_popup(ans):
    sg.popup(f"Zła Odpowiedź! Powinno być: {ans}", title="Źle!", modal=True, font=("Fixedsys",15))

def good_ans_popup():
    texts = ["Świetna robota!", "Brawo!", "Jestem dumny!", "Dobrze zapamiętane!", "Świetnie!"]
    text = random.choice(texts)
    sg.popup(text, title="Dobrze!", modal=True, font=("Fixedsys",15))

def error_popup(message):
    sg.popup_scrolled(f"Wystąpił błąd który uniemożliwił działanie programu, zgłoś go twórcy!\n------------\n{message}", 
                      title="Błąd!", modal=True)

def get_dict_file(fname):
    fname = sg.PopupGetFile(f"Nie udało się znaleźć pliku {fname}! Wybierz go ręcznie.", 
                            title="Wybór", modal=True, font="Fixedsys")
    path = fname.replace("\\", "\\\\")
    return path

def get_counter(maxword):
    while 1<2:
        while 1<2:
            try:
                counter = sg.PopupGetText("""Ile słówek? (Wpisz "wszystkie" by wybrać wszystkie słówka) """,
                                           font="Fixedsys")
                if counter == "wszystkie":
                    counter = maxword
                counter = int(counter)
                break
            except ValueError:
                sg.popup_error("Zły wybór!  Musi być liczbą!", font="Fixedsys")
            except TypeError:
                quit()
        if counter > maxword or counter <= 0:
            sg.popup_error(f"Liczba nie może być większa niż {maxword} i mniejsza lub równa 0!", font="Fixedsys")
        else:
            break
    return counter

def results_screen(score, counter):
    logger(score, counter)
    layout = [[sg.Text(f"GRATULACJE! MASZ {score} NA {counter} PUNKTÓW!", font=["Fixedsys", 15])],
               [sg.Button("Statystyki", font="Fixedsys"), sg.Button("Wróć do menu", font="Fixedsys"), 
                sg.Button("Wyjdź", button_color=("white", "red"), font="Fixedsys")]]
    window = sg.Window("Lilac", layout, element_justification='c')
    event, values = window.Read()
    if event == "Statystyki":
        window.close()
        graph("log.log")
    elif event == "Wróć do menu":
        window.close()
        menu()
    elif event in (None, "Wyjdź"):
        window.close()
        quit()

def mode_wrapper(dictionary, counter, mode):
    question = ""
    not_used = dictionary
    score = 0
    selected = mode
    for i in range(0, counter):
        if selected == "oba":
            mode = str(random.choice(["ang", "pl"]))
        if mode == "ang":
            question = random_en(not_used, question)
        elif mode == "pl":
            question = random_pl(not_used, question)
        layout = [[sg.Text(f"Pytanie {i+1} z {counter}", font=("Fixedsys", 13))],
                  [sg.Text(f"{question}: ", font=["Fixedsys", 10]), 
                    sg.InputText(size=(20,1)), sg.Button("Wprowadź", font="Fixedsys"), 
                    sg.Button("Wyjdź", button_color=("white", "red"), font="Fixedsys")]]
        window = sg.Window("Lilac", layout)
        event, values = window.read()
        if mode == "ang":
            ans = en_to_pl(dictionary, question)
        elif mode == "pl":
            ans = pl_to_en(dictionary, question)
        else:           # Error fallback just in case something messes up in the future.
            window.close()
            error_popup("""BŁĄD KODU: ZŁY TRYB GRY (mode nie jest w ["ang","pl"])""")
            quit()
        if event == "Wprowadź":
            query = values[0].lower()
        elif event == "Wyjdź":
            window.close()
            break
        if comparator(query, question, dictionary) == True:
            score += 1
            if mode == "ang":
                not_used.pop(question)
            elif mode == "pl":
                not_used.pop(ans)
            good_ans_popup()
        else:
            bad_ans_popup(ans)
        window.close()
    results_screen(score, counter)
                
def write_settings(fname, settings):
    try:
        file_flush(fname)
        with open(fname, "w", newline='') as file:
            writer = csv.writer(file)
            for row in settings.items():
                writer.writerow(row)
    except:
        tb = traceback.format_exc()
        error_popup(tb)
        quit()
            
def menu_settings(settings, default_settings, settings_fname): 
    themes_list = sg.ListOfLookAndFeelValues()
    default_limiter = settings["log_limit"]
    default_theme = settings["theme"]
    layout = [ [sg.Text("USTAWIENIA", justification="c", font=("Fixedsys", 25))],
               [sg.Text('_'*27, justification="c", font=("Helvetica", 15))],
               [sg.Text("Maksymalna liczba logów: ", font=("Fixedsys", 10)), 
                    sg.InputText(default_text=default_limiter, key="logs", size=(12,1))],
               [sg.Text("Schemat Kolorów: ", font=("Fixedsys", 10)), 
                    sg.Combo(themes_list, default_value=default_theme, key="theme")],
               [sg.Button("Zapisz", font=("Fixedsys", 12)), sg.Button("Anuluj", font=("Fixedsys", 12)), 
                    sg.Button("Przywróć do Domyślnych", font=("Fixedsys", 12), button_color=("white", "red"))]
    ]
    window = sg.Window('Lilac', layout).Finalize()
    event, values = window.Read()
    if event == None:
        quit()
    elif event == "Zapisz":
        settings["log_limit"] = values["logs"]
        settings["theme"] = values["theme"]
        write_settings(settings_fname, settings)
        sg.popup("Zapisano!", font=("Fixedsys", 12))
        window.close()
    elif event == "Anuluj":
        window.close()
    elif event == "Przywróć do Domyślnych":
        if sg.popup_yes_no("Na pewno chcesz utracić te ustawienia i\nprzywrócić domyślne?", font=("Fixedsys", 12)) == "Yes":
            sg.popup("Przywrócono Ustawienia domyślne!", font=("Fixedsys", 12))
            write_settings(settings_fname, default_settings)
            window.close()
        else:
            menu_settings(settings, default_settings)
    menu()
              
def csv_parse(fname):
    try:
        with open(fname, encoding="utf-8-sig") as file:
            words = {str(num):col for num,col in csv.reader(file)}
        if words == None:
            csv_parse(get_dict_file())
        return words
    except IOError:
        csv_parse(get_dict_file(fname))
    except:
        tb = traceback.format_exc()
        error_popup(tb)
        quit()
    
def main():
    menu()

if __name__ == '__main__':
    main()

# Function strictly for debugging! Gives full CLI experience. It also presents the planned functionality logic.
# Yes, I know this function is a mess, it should be commented out/removed for future releases!
# It's meant to be a single goddamn messy function.
# def debug(dictionary):
#     maxword = len(dictionary)
#     score = 0
#     not_used = dictionary
#     question = ""
#     while 1<2:
#         while 1<2:
#             try:
#                 counter = input("""Ile słówek? (Wpisz "wszystkie" by wybrać wszystkie słówka) """)
#                 if counter == "wszystkie":
#                     counter = maxword
#                 counter = int(counter)
#                 break
#             except ValueError:
#                 print("Zły wybór! Musi być liczbą!")
#         if counter > maxword or counter <= 0:
#             print(f"Liczba nie może być większa niż {maxword} i mniejsza lub równa 0!")
#         else:
#             break
#     while 1<2:
#         mode = str(input("1) Angielski > Polski\n2) Polski > Angielski\n3) Oba\nWybierz tryb: "))
#         if mode in ["1", "2", "3"]:
#             break
#         else:
#             print("Zły wybór!")
#     if mode == "1":
#         for i in range (0,counter):
#             question = random_en(not_used, question)
#             query = input(f"\n{question} > ")
#             ans = en_to_pl(dictionary, question)
#             if comparator(query, question, dictionary) == True:
#                 score += 1
#                 not_used.pop(question)
#             else:
#                 print(f"Zła odpowiedź! Powinno być: {ans}")
#     if mode == "2":
#         for i in range (0,counter):
#             question = random_pl(not_used, question)
#             query = input(f"\n{question} > ")
#             ans = pl_to_en(dictionary, question)
#             if comparator(query, question, dictionary) == True:
#                 score += 1
#                 not_used.pop(ans)
#             else:
#                 print(f"Zła odpowiedź! Powinno być: {ans}")
#     if mode == "3":
#         for i in range (0,counter):
#             lan = random.choice(["ang", "pl"])
#             if lan == "ang":
#                 question = random_en(not_used, question)
#                 query = input(f"\n{question} > ")
#                 ans = en_to_pl(dictionary, question)
#                 if comparator(query, question, dictionary) == True:
#                     score += 1
#                     not_used.pop(question)
#                 else:
#                     print(f"Zła odpowiedź! Powinno być: {ans}")
#             if lan == "pl":
#                 question = random_pl(not_used, question)
#                 query = input(f"\n{question} > ")
#                 ans = pl_to_en(dictionary, question)
#                 if comparator(query, question, dictionary) == True:
#                     score += 1
#                     not_used.pop(ans)
#                 else:
#                     print(f"Zła odpowiedź! Powinno być: {ans}")
#     percent = str(round((score/counter)*100, 1)) + "%"
#     logger(score, counter)
#     print(f"Gratulacje! Masz {score} na {counter} punktów! ({percent})")
#     graph("log.log")
