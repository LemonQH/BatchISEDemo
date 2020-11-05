import tkinter as tk
from tkinter import filedialog,messagebox,ttk
from audioandprocess import Audio_model

au_model=Audio_model("",False)
file_dict=[]

def get_file():
    # 获取文本路径
    file = filedialog.askopenfilename(filetypes=[('text files', '.txt')])
    au_model.current_file=file
    text1.delete('1.0',tk.END)
    text1.insert(tk.END, file)
    # 展示文本
    file_content=au_model.get_content(file)
    text2.delete('1.0',tk.END)
    text2.insert(tk.END,file_content)

def set_result_path():
    result_path=filedialog.askdirectory()
    au_model.audio_path=result_path
    text1.insert(tk.END,result_path)

def start_rec():
    lb_Status['text']='Working...'
    au_model.record_and_save()
#
def stop_rec():
    text1.delete('1.0', tk.END)
    text2.delete('1.0', tk.END)
    lb_Status['text']='Ready'
    file_dict.append(au_model.current_file)
    au_model.is_recording=False

def start_score():
    result=au_model.get_score(file_dict)
    for r in result:
        text3.insert(tk.END,r)



root=tk.Tk()
root.title("youdao ise test")
frm = tk.Frame(root)
frm.grid(padx='50', pady='50')

btn_get_file_path=tk.Button(frm,text='选择课文 ：',command=get_file)
btn_get_file_path.grid(row=0,column=0)

text1=tk.Text(frm,width='70', height='2')
text1.grid(row=0,column=1)

text2=tk.Text(frm,width='70', height='5')
text2.grid(row=1,column=1)

btn_start_rec=tk.Button(frm,text='录音',command=start_rec,width=10)
btn_start_rec.grid(row=2,column=0)

lb_Status = tk.Label(frm, text='Ready', anchor='w', fg='green')
lb_Status.grid(row=2,column=1)

btn_stop_rec=tk.Button(frm,text="结束录音",command=stop_rec)
btn_stop_rec.grid(row=2,column=2)



btn_score=tk.Button(frm,text="评分",command=start_score,width=10)
btn_score.grid(row=3,column=0)

text3=tk.Text(frm,width='70', height='10')
text3.grid(row=3,column=1)

root.mainloop()
