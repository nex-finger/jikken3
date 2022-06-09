import sys
import tkinter
import numpy
import scipy
from tkinter import Tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from scipy.io.wavfile import write

# global variable
global tmp1
global filename
global filedata
global editdata
global signal
global wave

# ハミング符号の行列
global HAMLIST
HAMLIST = [[1, 0, 0, 0, 0, 1, 1],
           [0, 1, 0, 0, 1, 0, 1],
           [0, 0, 1, 0, 1, 1, 0],
           [0, 0, 0, 1, 1, 1, 1]]

# バイナリをwavファイルに
def transwave(signal):

    exname = filedialog.asksaveasfilename(title = "Save",
                                          filetypes = [("WaveFile", ".wav")],
                                          defaultextension = "wav")
    print(exname)
    
    bitrate = int(bittxt.get())
    freqency = int(feqtxt1.get())
    times = int(feqtxt2.get())

    wave = []
    length = len(signal)

    for i in range (length):
        print(i)
        if signal[i] == 0:
            tfre = freqency
            ttim = times
        elif signal[i] == 1:
            tfre = int(freqency / 2)
            ttim = int(times + times)
        elif signal[i] == 2:
            tfre = int(freqency + freqency)
            ttim = int(times / 2)

        for j in range (ttim):
            for k in range (tfre):
                wave = wave + [224]
            for l in range (tfre):
                wave = wave + [32]

    print("AAA")
    finwave = numpy.array(wave, dtype = 'uint8')
    print("finwave:\n")
    print(finwave)

    # カキコミ！
    scipy.io.wavfile.write(exname, bitrate, finwave)
    messagebox.showinfo(u"2031133 KCS Binary Decoder", "Output was completed.")
    sys.exit()

# 文字をバイナリに
def outfile():

    bitrate = bittxt.get()
    freqency = feqtxt1.get()
    times = feqtxt2.get()
    
    print('bitrate  ' + bitrate)
    print('freqency ' + freqency)
    print('times    ' + times)
    print("\n")

    init = '00000000111111112222222233333333444444445555555566666666777777778888888899999999AAAAAAAABBBBBBBBCCCCCCCCDDDDDDDDEEEEEEEEFFFFFFFF'
    signal = []

    tmpdata = editdata.replace(' ', '')
    bindata = init + tmpdata
    length = len(bindata)
    incr = -128
    for i in range (length):
        incr += 1
        char = bindata[i]
        sgnllist = [0, 0, 0, 0, 0, 0, 0]
        
        if char == "0":
            datalist1 = [0, 0, 0, 0]
        elif char == "1":
            datalist1 = [0, 0, 0, 1]
        elif char == "2":
            datalist1 = [0, 0, 1, 0]
        elif char == "3":
            datalist1 = [0, 0, 1, 1]
        elif char == "4":
            datalist1 = [0, 1, 0, 0]
        elif char == "5":
            datalist1 = [0, 1, 0, 1]
        elif char == "6":
            datalist1 = [0, 1, 1, 0]
        elif char == "7":
            datalist1 = [0, 1, 1, 1]
        elif char == "8":
            datalist1 = [1, 0, 0, 0]
        elif char == "9":
            datalist1 = [1, 0, 0, 1]
        elif char == "A":
            datalist1 = [1, 0, 1, 0]
        elif char == "B":
            datalist1 = [1, 0, 1, 1]
        elif char == "C":
            datalist1 = [1, 1, 0, 0]
        elif char == "D":
            datalist1 = [1, 1, 0, 1]
        elif char == "E":
            datalist1 = [1, 1, 1, 0]
        elif char == "F":
            datalist1 = [1, 1, 1, 1]

        for j in range (7):
            sgnllist[j] = 0
            for k in range (4):
                sgnllist[j] += datalist1[k] * HAMLIST[k][j]
            sgnllist[j] = sgnllist[j] % 2

        for l in range (7):
            signal = signal + [sgnllist[l]]

        if incr == 2:
            signal = signal + [2]
            incr = 0

        # print(datalist1)
        # print(sgnllist)
        # print("\n")

    print("0xdata:\n", bindata, "\n")
    print("signal:\n", signal, "\n")

    transwave(signal)
    
    return

# ファイルの読み込み
def insrfile():
    
    typ = [('PlaneTextFile','*.txt')] 
    filename = filedialog.askopenfilename(filetypes = typ)
    
    f = open(filename,
             'r',
             encoding='UTF-8')
    filedata = f.read()
    f.close()

    return filename, filedata

# 文字列の改行を削除
def filesplit():

    tmp = filedata.split()
    editdata = " ".join(tmp);
    
    return editdata

#main
tmp1 = insrfile()
filename = tmp1[0]
filedata = tmp1[1]

editdata = filesplit()

#kokokara

# root.mainloop()まではtkinterの処理
root = Tk()

root.title(u"2031133 KCS Binary Decoder")
root.geometry("600x400")

# 書き込むボタン
otbtn = tkinter.Button(root,
                       text = 'Encode wavfile',
                       command = outfile)
otbtn.pack(side = tkinter.BOTTOM,
           fill = "x",
           padx = 10,
           pady = 5)

# 読み込んだディレクトリの表示
dtxt = tkinter.Label(root,
                     text = 'File: ' + filename,
                     width = 50)
dtxt.pack(side = tkinter.TOP,
          padx = 10,
          pady = 5)

# 読み込んだ内容の表示
ftxt = tkinter.Text(root,
                     width = 48,
                     height = 50)
ftxt.insert('1.0', editdata)
ftxt.pack(side = tkinter.LEFT,
          fill = 'y',
          padx = 10,
          pady = 5)

# エンコードの設定
# wavファイルのビットレート
bitlab = tkinter.Label(root,
                       text = 'SamplingRate',
                       anchor = tkinter.W,
                       width = 10)
bitlab.place(x = 400, y = 50)

bittxt = tkinter.Entry(root,
                       justify = tkinter.RIGHT,
                       width = 10)
bittxt.insert(tkinter.END, '40000')
bittxt.place(x = 500, y = 50)

bitexp1 = tkinter.Label(root,
                       text = 'Rate of wavfile(default = 40000)',
                       anchor = tkinter.W,
                       width = 30)
bitexp1.place(x = 400, y = 70)

# 信号の周波数と回数
feqlab = tkinter.Label(root,
                       text = 'period',
                       anchor = tkinter.W,
                       width = 10)
feqlab.place(x = 400, y = 120)

feqtxt1 = tkinter.Entry(root,
                       justify = tkinter.RIGHT,
                       width = 10)
feqtxt1.insert(tkinter.END, '40')
feqtxt1.place(x = 500, y = 120)

feqlab = tkinter.Label(root,
                       text = 'times',
                       anchor = tkinter.W,
                       width = 10)
feqlab.place(x = 400, y = 140)

feqtxt2 = tkinter.Entry(root,
                       justify = tkinter.RIGHT,
                       width = 10)
feqtxt2.insert(tkinter.END, '8')
feqtxt2.place(x = 500, y = 140)

feqexp1 = tkinter.Label(root,
                       text = 'Property of signal0(default = 40 x 8)',
                       anchor = tkinter.W,
                       width = 30)
feqexp1.place(x = 400, y = 160)

feqexp2 = tkinter.Label(root,
                       text = 'signal1 = 0.5*period x 2.0*times',
                       anchor = tkinter.W,
                       width = 30)
feqexp2.place(x = 400, y = 180)

feqexp3 = tkinter.Label(root,
                       text = 'signalINC = 2.0*period x 0.5*times',
                       anchor = tkinter.W,
                       width = 30)
feqexp3.place(x = 400, y = 200)

# 最前面に
root.attributes("-topmost", True)

root.mainloop()

