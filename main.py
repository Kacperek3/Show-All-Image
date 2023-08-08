from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QListWidget, QPushButton, QMessageBox, QLabel, QLineEdit
import os
from PIL import Image


#//////////////////////////////////////////////////////////////
#funkcje
def wyswietl_zdjecia(sciezka_do_folderu):
    for nazwa_pliku in os.listdir(sciezka_do_folderu):
        sciezka_do_pliku = os.path.join(sciezka_do_folderu, nazwa_pliku)

        if os.path.isdir(sciezka_do_pliku):
            wyswietl_zdjecia(sciezka_do_pliku)

        if os.path.isfile(sciezka_do_pliku) and nazwa_pliku.lower().endswith(('.jpg', '.jpeg')):
            tablica.append(nazwa_pliku)
            scie.append(sciezka_do_pliku)

class ScrollableListWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Przeglądarka zdjęć")
        self.setFixedSize(500, 350)

        self.search_box = QLineEdit()
        self.search_box.setFixedSize(200,25)
        self.search_box.setPlaceholderText("Wyszukaj...")

        # Tworzenie widżetu QListWidget
        self.list_widget = QListWidget()
        self.list_widget.setFixedHeight(200)
        self.list_widget.setFixedWidth(200)

        self.buttonOpen = QPushButton("OTWÓRZ", self)
        self.buttonDelete = QPushButton("USUN", self)

        # Przechowywanie indeksu klikniętego elementu
        self.selected_index = None

        # Dodawanie elementów do listy
        self.list_widget.itemClicked.connect(self.klikniecie)
        for i in range(len(scie)):
            nazwa_pliku = os.path.basename(scie[i])  # Pobieranie tylko nazwy pliku z pełnej ścieżki
            self.list_widget.addItem(nazwa_pliku)



        layout = QGridLayout()
        layout.setSpacing(50)
        layout.setVerticalSpacing(10)  # Zwiększenie odstępu pionowego między wierszami
        layout.addWidget(QLabel(""), 2, 1)
        layout.addWidget(QLabel(""), 3, 1)
        layout.setColumnMinimumWidth(1,50)
        layout.addWidget(self.list_widget, 0,0)
        layout.addWidget(self.buttonOpen,1,0)
        layout.addWidget(self.buttonDelete,2,0)
        layout.addWidget(self.search_box,0,1)
        self.search_box.resize(20,30)
        self.setLayout(layout)

        # Podłączanie przycisku do metody Otwarcie
        self.buttonOpen.clicked.connect(self.Otwarcie)
        self.buttonDelete.clicked.connect(self.Usuniecie)
        self.search_box.textChanged.connect(self.filtrowanie)

    #///////////////////////////////////////////////////////////////////////////////
    #metody
    def klikniecie(self, item):
        self.selected_index = self.list_widget.row(item)

    def Otwarcie(self):
        if self.selected_index is not None:
            sciezka_do_pliku = scie[self.selected_index]
            fota = Image.open(sciezka_do_pliku)
            fota.show()
            self.selected_index = None

    def Usuniecie(self):
        if self.selected_index is not None:
            sciezka_do_pliku = scie[self.selected_index]
            try:
                os.remove(sciezka_do_pliku)
                self.list_widget.takeItem(self.selected_index)
                self.selected_index = None

                message_box_Correct_deletePhoto = QMessageBox()
                message_box_Correct_deletePhoto.setIcon(QMessageBox.Information)
                message_box_Correct_deletePhoto.setText("Pomyslnie usunieto")
                message_box_Correct_deletePhoto.setWindowTitle("Usunięto")
                message_box_Correct_deletePhoto.setStandardButtons(QMessageBox.Ok)
                message_box_Correct_deletePhoto.exec_()

            except OSError as e:
                message_box_error_deletePhoto = QMessageBox()
                message_box_error_deletePhoto.setIcon(QMessageBox.Information)
                message_box_error_deletePhoto.setText("Bład w usunieciu")
                message_box_error_deletePhoto.setWindowTitle("Błąd")
                message_box_error_deletePhoto.setStandardButtons(QMessageBox.Ok)
                message_box_error_deletePhoto.exec_()


    def filtrowanie(self, text):
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            if text.lower() in item.text().lower():
                item.setHidden(False)
            else:
                item.setHidden(True)


    #///////////////////////////////////////////////////////////////////////////////
    #main

tablica = []
scie = []
if __name__ == '__main__':
    sciezka = r"C:\Users\kapis\onedrive"
    wyswietl_zdjecia(sciezka)
    app = QApplication([])
    window = ScrollableListWidget()
    window.show()
    app.exec_()
