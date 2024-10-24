#--------------------------------------------#
# Alfan F. Wicaksono, Fasilkom UI            #
# Simulasi External Merge Sort               #
#--------------------------------------------#

import contextlib
import heapq

from random import randint

MAX_INT = 10000000

class IntegerFileReader:
    """ iterator untuk sebuah file yang berisi angka-angka """
    def __init__(self, file_name):
        self.file_name = file_name

    def __enter__(self):
        self.file = open(self.file_name, 'r')
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.file.close()

    def __iter__(self):
        return self

    def __next__(self):
        val = self.file.readline()
        if val == '':
            raise StopIteration
        return int(val)

def generate_integer_files(num_files, num_numbers_per_file):
    """ menghasilkan beberapa file yang berisi angka-angka secara acak

        num_files : int , banyaknya files
        num_numbers_per_file : int , banyaknya angka di setiap file
    """
    filenames = []
    for i in range(num_files):
        filename = "intfile" + str(i+1) + ".txt"
        filenames.append(filename)
        with open(filename, "w") as file:
            for _ in range(num_numbers_per_file):
                file.write(str(randint(0, MAX_INT)) + "\n")
    return filenames

def external_merge_sort(merged_file_name, intermediate_file_names):
    """ External Merge Sort

        Konsep Iterator yang ada di Python cocok digunakan dalam masalah ini.
        1. Untuk setiap intermediate files, kita urutkan secara in-memory
           semua angka yang ada. Kemudian, hasil sorting-nya disimpan di file
           yang sama. Asumsi: semua angka di sebuah intermediate file muat di
           memori.
        2. Untuk setiap intermediate file (yang sudah sorted), kita buka Iterator.
           Kemudian, melalui Iterator-Iterator tersebut, kita gabungkan dengan
           bantuan struktur data HEAP.

        Kita butuh library contextlib untuk masalah resource management ketika
        membaca banyak file sekaligus at the same time.

        Kita butuh library heapq untuk implementasi Heap di Python.

    """
    # angka-angka di setiap intermediate_file_names mampu ditampung di memori
    # kita bisa lakukan in-memory sort di setiap intermediate_file
    for file_name in intermediate_file_names:
        values = []
        with IntegerFileReader(file_name) as file:
            for value in file:
                values.append(value)
        values.sort() # in memory sort
        with open(file_name, "w") as file:
            for value in values:
                file.write(str(value) + "\n")

    # external merge sort dengan bantuan iterator di setiap file
    # setiap saat, kita baca satu baris pada sebuah file
    with open(merged_file_name, "w") as merged_file:
        with contextlib.ExitStack() as stack:
            intermediate_files = []
            # Bagian berikut menyimpan iterator dari setiap intermediate file;
            # BUKAN MENYIMPAN ISI DARI DARI SETIAP INTERMEDIATE FILE!
            for file_name in intermediate_file_names:
                intermediate_files.append(stack.enter_context(IntegerFileReader(file_name)))
            # Bagian berikut melakukan sort dari semua iterator tersebut, satu-demi-satu
            # dengan bantuan Struktur Data Heap


            # for file_reader in intermediate_files:
            #     # Read each integer from the file reader
            #     for value in file_reader:
            #         print(value)

            l = 0
            for value in heapq.merge(*intermediate_files):
                # l+=1
                print(value)
                merged_file.write(str(value) + "\n")
            print(l)

if __name__ == '__main__':
    NUM_FILES   = 3
    NUM_NUMBERS = 100000

    filenames = generate_integer_files(NUM_FILES, NUM_NUMBERS)
    external_merge_sort("merged_intfile.txt", filenames)
