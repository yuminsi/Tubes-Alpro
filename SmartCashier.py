import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox, QTextEdit, QFormLayout, QGroupBox
from functools import partial  # Import functools

def load_data(data_barang):
    data = {}
    try:
        with open(data_barang, 'r') as file:
            for line in file:
                parts = line.strip().split(',')
                if len(parts) == 4:
                    nama_barang, harga, stok, satuanbeli = parts
                    data[nama_barang] = {'harga': int(harga), 'stok': int(stok), 'satuanbeli': str(satuanbeli)}
    except FileNotFoundError:
        with open(data_barang, 'w') as file:
            pass
    return data

def save_data(data_barang, data):
    with open(data_barang, 'w') as file:
        for nama_barang, info in data.items():
            file.write(f"{nama_barang},{info['harga']},{info['stok']},{info['satuanbeli']}\n")

class SmartCashier(QWidget):
    def __init__(self):
        super().__init__()
        self.data_barang = "data_barang.txt"  # Pindahkan inisialisasi data_barang ke sini
        self.initUI()

    def initUI(self):
        self.setWindowTitle('SmartCashier')
        self.setGeometry(100, 100, 800, 600)

        self.layout = QVBoxLayout()

        self.menu_label = QLabel("============ Selamat Datang di SmartCashier ===========\n~~~~~~~~~~~~~~~~~~~~~~~~~~~ Menu ~~~~~~~~~~~~~~~~~~~~~~")
        self.layout.addWidget(self.menu_label)

        self.menu_text = QTextEdit()
        self.menu_text.setReadOnly(True)
        self.layout.addWidget(self.menu_text)

        self.load_menu()

        self.form_group = QGroupBox("Form Pembelian")
        self.form_layout = QFormLayout()

        self.menu_input = QLineEdit()
        self.form_layout.addRow('Pilih Menu:', self.menu_input)

        self.quantity_input = QLineEdit()
        self.form_layout.addRow('Jumlah Pesanan:', self.quantity_input)

        self.form_group.setLayout(self.form_layout)
        self.layout.addWidget(self.form_group)

        self.button_layout = QHBoxLayout()
        self.purchase_button = QPushButton('Beli Barang')
        self.purchase_button.clicked.connect(self.purchase_item)
        self.button_layout.addWidget(self.purchase_button)

        self.finish_button = QPushButton('Selesai')
        self.finish_button.clicked.connect(self.complete_purchase)
        self.button_layout.addWidget(self.finish_button)

        self.layout.addLayout(self.button_layout)

        self.detail_group = QGroupBox("Detail Pembelian")
        self.detail_layout = QVBoxLayout()

        self.detail_label = QLabel("~~~~~~~~~~~~~~~~~~~ Detail Pembelian ~~~~~~~~~~~~~~~~~~")
        self.detail_layout.addWidget(self.detail_label)

        self.detail_text = QTextEdit()
        self.detail_text.setReadOnly(True)
        self.detail_layout.addWidget(self.detail_text)

        self.detail_group.setLayout(self.detail_layout)
        self.layout.addWidget(self.detail_group)

        self.setLayout(self.layout)
        self.total_bayar = 0
        self.pesanan = {}
        self.menu = load_data(self.data_barang)  # Gunakan self.data_barang

    def load_menu(self):
        menu = load_data(self.data_barang)  # Gunakan self.data_barang
        menu_text = ""
        for barang_bangunan in menu:
            menu_text += f"Daftar Menu: {barang_bangunan}\t Harga: Rp. {menu[barang_bangunan]['harga']}\t Stok: {menu[barang_bangunan]['stok']}\t Satuan Beli: {menu[barang_bangunan]['satuanbeli']}\n"
        self.menu_text.setText(menu_text)

    def purchase_item(self):
        menu_item = self.menu_input.text().strip()
        quantity = self.quantity_input.text().strip()

        if menu_item not in self.menu:
            QMessageBox.warning(self, 'Error', 'Menu tidak valid!')
            return

        try:
            quantity = int(quantity)
        except ValueError:
            QMessageBox.warning(self, 'Error', 'Jumlah harus berupa angka!')
            return

        if quantity > self.menu[menu_item]['stok']:
            QMessageBox.warning(self, 'Error', 'Stok tidak mencukupi!')
            return

        if menu_item in self.pesanan:
            self.pesanan[menu_item] += quantity
        else:
            self.pesanan[menu_item] = quantity

        self.menu[menu_item]['stok'] -= quantity
        self.total_bayar += self.menu[menu_item]['harga'] * quantity

        self.menu_input.clear()
        self.quantity_input.clear()

    def complete_purchase(self):
        if not self.pesanan:
            QMessageBox.warning(self, 'Error', 'Silahkan pilih barang terlebih dahulu.')
            return

        detail_text = ""
        for beli, jumlah in self.pesanan.items():
            detail_text += f"Pesanan Menu: {beli}\nJumlah Pesanan: {jumlah}\n"

        if self.total_bayar >= 50000:
            diskon = self.total_bayar * 5 / 100
            total = self.total_bayar - diskon
            detail_text += "\nDapat diskon 5%\n"
            detail_text += f"Total Bayar: Rp. {total}"
        else:
            total = self.total_bayar
            detail_text += f"Total Bayar: Rp. {total}"

        self.detail_text.setText(detail_text)
        self.pesanan.clear()
        self.total_bayar = 0
        save_data(self.data_barang, self.menu)  # Gunakan self.data_barang
        self.load_menu()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    cashier = SmartCashier()
    cashier.show()
    sys.exit(app.exec_())
