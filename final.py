import os
import re
import sympy as sp
import tkinter as tk

from tkinter import filedialog


def process_if(file, line):
	global alg_list
	_if = _else = len(re.split(' y | o ', line))
	flag = True
	line = file.readline()
	alg_list.append(line)
	line = line.lower()
	while not line.startswith('fsi'):
		if line.startswith('sino'):
			flag = False
			line = file.readline()
			alg_list.append(line)
			line = line.lower()
			continue
		if flag:
			_if = _if + 1
		else:
			_else = _else + 1
		line = file.readline()
		alg_list.append(line)
		line = line.lower()
	if _if > _else:
		ans = f'+{_if}'
	else:
		ans = f'+{_else}'
	return ans, file


def process_for(file, line):
	global alg_list
	inter = "("
	for_data = re.split(',|\n', re.split('=', re.split(' ', line)[1])[1])
	
	if for_data[2].startswith('+'):
		li, ls, inc = for_data[0], for_data[1], for_data[2]
	elif for_data[2].startswith('-'):
		li, ls, inc = for_data[1], for_data[0], for_data[2]

	line = file.readline()
	alg_list.append(line)
	line = line.lower()
	limits = f'(({ls}-{li}+1)/{inc[1:]})'
	count = 0

	while not line.startswith('fpara'):
		if line.startswith('para'):
			if count != 0:
				inter += f'+{count}'
			val, file = process_for(file, line)
			inter += val
			count = 0
		elif line.startswith('si'):
			if count != 0:
				inter += f'+{count}'
			val, file = process_if(file, line)
			inter += val
			count = 0
		else:
			count = count + 1
		line = file.readline()
		alg_list.append(line)
		line = line.lower()
	if count != 0:
		inter += f'+{count}'
	inter += ')'
	ans = f'+({limits}*{inter}+2*({limits}+1))'
	return ans, file


def calculate():
	global answer1, answer2, alg_list, text1
	text1.config(state=tk.NORMAL)
	text1.delete('1.0', tk.END)
	file_path = filedialog.askopenfilename()
	ans = ""
	ans_simp = ""
	alg_list = []
	with open(file_path, 'r') as f:
		ans = ""
		line = f.readline()
		alg_list.append(line)
		line = line.lower()
		count = 0
		while not line.startswith('pare'):
			if line.startswith('inicio'):
				line = f.readline()
				alg_list.append(line)
				line = line.lower()
				continue
			elif line.startswith('si'):
				if count != 0:
					ans += f'+{count}'
				val, f = process_if(f, line)
				ans += val
				count = 0
			elif line.startswith('para'):
				if count != 0:
					ans += f'+{count}'
				val, f = process_for(f, line)
				ans += val
				count = 0
			else:
				count = count + 1
			line = f.readline()
			alg_list.append(line)
			line = line.lower()
		if count != 0:
			ans += f'+{count}'
		ans_simp = 'T(n) = ' + str(sp.simplify(ans)).replace('**', '^')
		ans = 'T(n) = ' + ans
		print(ans)
	for alg in alg_list:
		text1.insert(tk.END, alg)
	text1.config(state=tk.DISABLED)
	answer1.set(ans)
	answer2.set(ans_simp)
	

def main():
	global answer1, answer2, alg_list, text1
	root = tk.Tk()
	root.title("Calculo del T(n)")
	root.geometry("600x700")
	root.grid_columnconfigure(0, weight=1)

	sep_text = "---------------------------------------------------------------------------------------------"
	sep_font = ('lato', 12)

	sep0 = tk.Label(root, text=sep_text, font=sep_font)
	sep0.pack()

	titlelabel = tk.Label(root, text="Calculo del T(n)", font=('lato', 14, 'bold'))
	titlelabel.pack()

	sep1 = tk.Label(root, text=sep_text, font=sep_font)
	sep1.pack()

	button1 = tk.Button(root, text="Seleccionar Archivo", command=calculate, font=('lato', 10))
	button1.pack()

	sep2 = tk.Label(root, text=sep_text, font=sep_font)
	sep2.pack()

	answer1 = tk.StringVar()
	answer1.set("")
	answer2 = tk.StringVar()
	answer2.set("")

	nored = tk.Label(root, text='T(n) sin simplificar', font=('lato', 11))
	nored.pack()

	sep3 = tk.Label(root, text=sep_text, font=sep_font)
	sep3.pack()

	label1 = tk.Label(root, textvariable=answer1, font=('consolas', 11), wraplength=550)
	label1.pack()

	sep4 = tk.Label(root, text=sep_text, font=sep_font)
	sep4.pack()

	red = tk.Label(root, text='T(n) simplificado', font=('lato', 11))
	red.pack()

	sep5 = tk.Label(root, text=sep_text, font=sep_font)
	sep5.pack()

	label2 = tk.Label(root, textvariable=answer2, font=('consolas', 11), wraplength=550)
	label2.pack()

	sep6 = tk.Label(root, text=sep_text, font=sep_font)
	sep6.pack()

	alglabel = tk.Label(root, text="Algoritmo", font=('lato', 11))
	alglabel.pack()

	scrollbar1 = tk.Scrollbar(root)
	text1 = tk.Text(root, height=15, font=('consolas', 11))
	scrollbar1.pack(side=tk.RIGHT)
	text1.pack(side=tk.LEFT, fill=tk.X)
	scrollbar1.config(command=text1.yview)
	text1.config(yscrollcommand=scrollbar1.set)
	text1.config(state=tk.DISABLED)

	root.mainloop()


if __name__ == "__main__":
	main()