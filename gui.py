import tkinter as tk
from tkinter import Scrollbar
import pandas as pd

class GUIApp:
    def __init__(self, df, save_path):
        self.df = df
        self.save_path = save_path
        self.current_page = 0

        self.window = tk.Tk()
        self.window.geometry('600x600')  # GUI 창 크기 설정

        self.labels = df['labels'].apply(eval).tolist()  # str을 리스트로 변환
        self.words = df['words'].apply(eval).tolist()  # str을 리스트로 변환
        self.texts = df['content'].tolist()

        self.page_label = tk.Label(self.window, font=('Arial', 14, 'bold'))  # 현재 페이지 표시 라벨
        self.text_widget = tk.Label(self.window, wraplength=550, font=('Arial', 12))  # 줄바꿈을 위한 너비와 폰트 설정
        self.word_listbox = tk.Listbox(self.window, width=30, font=('Arial', 12))  # word를 표시할 Listbox
        self.label_listbox = tk.Listbox(self.window, width=30, font=('Arial', 12))  # label을 표시할 Listbox

        self.next_button = tk.Button(self.window, text='다음 페이지', command=self.next_page)
        self.prev_button = tk.Button(self.window, text='이전 페이지', command=self.prev_page)

        self.window.bind('<Right>', self.next_page_key)  # 오른쪽 화살표 키 바인딩
        self.window.bind('<Left>', self.prev_page_key)  # 왼쪽 화살표 키 바인딩

        self.show_current_page()

    def show_current_page(self):
        label = self.labels[self.current_page]
        word = self.words[self.current_page]
        text = self.texts[self.current_page]

        self.text_widget.config(text=text)
        self.text_widget.grid(row=0, column=0, columnspan=2, padx=10, pady=10)  # 상단에 위치하고 간격을 주기 위해 padx와 pady 사용

        self.page_label.config(text=f'페이지: {self.current_page + 1}/{len(self.labels)}')
        self.page_label.grid(row=1, column=0, sticky='w', padx=10)  # 아래쪽에 배치

        self.word_listbox.delete(0, tk.END)  # 이전 페이지의 데이터 삭제
        for w in word:
            self.word_listbox.insert(tk.END, w)
        self.word_listbox.grid(row=2, column=0, padx=10)  # 왼쪽에 배치

        self.label_listbox.delete(0, tk.END)  # 이전 페이지의 데이터 삭제
        for l in label:
            self.label_listbox.insert(tk.END, l)
        self.label_listbox.grid(row=2, column=1, padx=10)  # 오른쪽에 배치

        self.next_button.grid(row=3, column=1, sticky='e', padx=10, pady=10)  # 아래쪽에 배치
        self.prev_button.grid(row=3, column=0, sticky='w', padx=10, pady=10)  # 아래쪽에 배치

        # word_listbox 요소 클릭 시 label_listbox 요소 변경
        self.word_listbox.bind('<<ListboxSelect>>', self.update_label)

    def next_page(self, event=None):
        self.save_changes(self.save_path)  # 변경 내용 저장
        self.current_page += 1
        if self.current_page >= len(self.labels):
            self.current_page -= 1
        self.clear_widgets()
        self.show_current_page()

    def prev_page(self, event=None):
        self.save_changes(self.save_path)  # 변경 내용 저장
        self.current_page -= 1
        if self.current_page < 0:
            self.current_page += 1
        self.clear_widgets()
        self.show_current_page()

    def next_page_key(self, event):
        self.next_page()

    def prev_page_key(self, event):
        self.prev_page()

    def clear_widgets(self):
        self.text_widget.grid_forget()
        self.page_label.grid_forget()
        self.word_listbox.grid_forget()
        self.label_listbox.grid_forget()
        self.next_button.grid_forget()
        self.prev_button.grid_forget()

    def update_label(self, event):
        selected_index = self.word_listbox.curselection()
        if selected_index:
            selected_index = selected_index[0]
            if selected_index < len(self.label_listbox.get(0, tk.END)):
                current_label = self.label_listbox.get(selected_index)
                if current_label == "O":
                    self.label_listbox.delete(selected_index)
                    self.label_listbox.insert(selected_index, "B-FW")
                elif current_label == "B-FW":
                    self.label_listbox.delete(selected_index)
                    self.label_listbox.insert(selected_index, "I-FW")
                elif current_label == "I-FW":
                    self.label_listbox.delete(selected_index)
                    self.label_listbox.insert(selected_index, "O")

    def save_changes(self, save_path):
        self.labels[self.current_page] = self.label_listbox.get(0, tk.END)  # 변경된 label 저장
        # 엑셀 파일에 변경된 내용 저장
        self.df.loc[self.current_page, 'labels'] = str(self.labels[self.current_page])
        self.df.to_excel(save_path, index=False)

def read_excel_file(file_path):
    df = pd.read_excel(file_path)
    return df
        
if __name__ == '__main__':
    file_path = input('file path:')
    df = read_excel_file(file_path)

    app = GUIApp(df, save_path='modified.xlsx')
    app.window.mainloop()
