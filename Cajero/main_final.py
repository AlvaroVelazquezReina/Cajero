import tkinter as tk
import time
from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb
from matplotlib import pyplot as plt
import matplotlib.patches as mpatches

balance_actualizado = 1000

class ArquitecturaGeneral(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.datos_compartidos = {'Balance':tk.IntVar()} ## creamos este diccionario para actualizar el balance segun depositamos o lo otro

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (PaginaInicio, PaginaMenu, PaginaRetirada, PaginaDeposito, PaginaBalance):
            nombre_pagina = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[nombre_pagina] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.ir_a_frame("PaginaInicio") ## en esta funcion, decidimos donde empieza el programa (PaginaInicio, o PageOne o PageTwo)

    def ir_a_frame(self, nombre_pagina):
        ## Enseña el frame de la pagina que diga
        frame = self.frames[nombre_pagina]
        frame.tkraise()


class PaginaInicio(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg = '#ffd633') ## el color viene de la pagina: https://www.w3schools.com/colors/colors_picker.asp
        self.controller = controller

        self.controller.title('Cajero')
        self.controller.attributes('-zoomed', True)
        self.controller.iconphoto(False, tk.PhotoImage(file='/home/propietario/Escritorio/PythonProjects/ATM_tutorial/atm.png')) ## ponemos icono al ATM

        cabecero_label = tk.Label(self,
                                text = 'Cajero',
                                font=('orbitron', 45, 'bold'),
                                foreground = '#ffffff', ## esto es el color del texto abreviatura con 'fg'
                                background = '#ffd633') ## se puede usar la abreviatura bg en vez de 'background'
        cabecero_label.pack(pady=25) ## con 'pady=25' separa del extremo para dejarla mas hueco

        espacio_label = tk.Label(self, height = 4, bg='#ffd633')
        espacio_label.pack()

        contraseña_label = tk.Label(self,
                                text= 'Introduzca su contraseña :',
                                font=('orbitron', 25, 'bold'),
                                bg='#ffd633',
                                fg = 'white') ## o como lo he puesto arriba #ffffff
        contraseña_label.pack(pady = 10) ## esto es para meterle espacios entre los labels
        
        mi_contraseña = tk.StringVar()
        
        contraseña_caja = tk.Entry(self,
                                    textvariable = mi_contraseña,
                                    font=('orbitron',12),
                                    width=22)
        contraseña_caja.focus_set() ## esto es para que aparezca parpadeando en el Entry box
        contraseña_caja.pack(ipady=7) ## ipady para hacer la entrada de texto mas amplia
        def enfoque_cosa(_):
            contraseña_caja.configure(fg='black',show='*')
        contraseña_caja.bind('<FocusIn>', enfoque_cosa)

        def checkear_contraseña():
            if mi_contraseña.get() == '1234':
                mi_contraseña.set('') ## esto es para que cuando vuela del boton exit no me deje la contraseña puesta
                incorrect_contraseña_label['text'] = '' ## y esto es para que cuando vuelva no se quede el mensaje 'incorrect password'
                controller.ir_a_frame('PaginaMenu')
            else:
                incorrect_contraseña_label['text']='Contraseña incorrecta'
        boton_intro = tk.Button(self,
								text= 'Confirmar',
								command = checkear_contraseña,
								relief='raised', ## el timpo de boton que queremos meterle
								borderwidth = 3,
								width=40,
								height = 3)
        boton_intro.pack(pady = 10)

        incorrect_contraseña_label = tk.Label(self,
                                            text='',
                                            font=('orbitron', 13),
                                            fg='white',
                                            bg='#a6a6a6',
                                            anchor = 'n')
        incorrect_contraseña_label.pack(fill='both',expand=True) ## para rellenar el espacio de abajo, probar a quitarlo...

        banco_foto = tk.PhotoImage(file = 'banco.png')
        banco_label = tk.Label(self, image = banco_foto)
        banco_label.place(x=0, y=0)
        banco_label.image = banco_foto
        

        boton_frame = tk.Frame(self, relief='raised', borderwidth=3) ## creamos otro frame para las fotos de las credit cards
        boton_frame.pack(fill='x', side='bottom')

        visa_foto = tk.PhotoImage(file = 'visa.png') ## meter la foto de la visa
        visa_label = tk.Label(boton_frame, image=visa_foto)
        visa_label.pack(side='left')
        visa_label.image = visa_foto

        mastercard_foto = tk.PhotoImage(file = 'mastercard.png')
        mastercard_label = tk.Label(boton_frame, image=mastercard_foto)
        mastercard_label.pack(side='left')
        mastercard_label.image = mastercard_foto

        americanexpress_foto = tk.PhotoImage(file = 'americanexpress.png')
        americanexpress_label = tk.Label(boton_frame, image=americanexpress_foto)
        americanexpress_label.pack(side='left')
        americanexpress_label.image = americanexpress_foto
        ## importante tener las imagenes con los mismos pixeles, sino se pegan cada una con sus pixeles y queda mal

        def tick():
            tiempo_actual = time.strftime('%H:%M:%S') ## toquetear estos parametros para ponerlo en 24h, meterle segundos...
            tiempo_label.config(text=tiempo_actual)
            tiempo_label.after(200,tick)#para updatear el tiempo y que no se quede estanco
        tiempo_label = tk.Label(boton_frame,font=('orbitron',12))
        tiempo_label.pack(side='right')

        tick() ## esto es para que lo ejecute, y que no sea por un boton

class PaginaMenu(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg= '#ffd633')
        self.controller = controller

        cabecero_label = tk.Label(self,
                                text = 'Cajero',
                                font=('orbitron', 45, 'bold'),
                                foreground = '#ffffff',
                                background = '#ffd633') 
        cabecero_label.pack(pady=25) 

        menu_principal_label = tk.Label(self,
                                    text = 'Menu Principal',
                                    font =('orbitron', 25, 'bold'),
                                    fg = '#ffffff',
                                    background = '#ffd633')
        menu_principal_label.pack(pady = 50)

        label_de_seleccion = tk.Label(self,
                                text = 'Seleccione una opción: ',
                                font = ('orbitron', 25, 'bold'),
                                fg = '#ffffff',
                                bg = '#ffd633',
                                anchor = 'w') ## para ponerlo a la derecha, tambien valdria en pack(side = 'left')
        label_de_seleccion.pack(fill = 'x') ## si no le metemos esto, nos hace un hueco grande, no se porque!!!!!!

        ######## metemos los botones, pero antes hacemos una frame especial para ellos ########

        boton_frame = tk.Frame(self, bg = '#a6a6a6') ## entiendo que button frame esta dentro de otra frame (self)
        boton_frame.pack(fill='both', expand = True)

        def withdraw():
            controller.ir_a_frame('PaginaRetirada')
        
        boton_retirada = tk.Button(boton_frame,
                                    text = 'Retirada',
                                    command = withdraw,
                                    relief = 'raised',
                                    borderwidth = 3,
                                    width = 50,
                                    height = 5)
        boton_retirada.grid(row=0, column = 0, pady= 5)

        def deposit():
            controller.ir_a_frame('PaginaDeposito')
        
        boton_deposito = tk.Button(boton_frame,
                                    text = 'Depósito',
                                    command = deposit,
                                    relief = 'raised',
                                    borderwidth = 3,
                                    width = 50,
                                    height = 5)
        boton_deposito.grid(row=1, column = 0, pady= 5)

        def balance():
            controller.ir_a_frame('PaginaBalance')
        
        boton_balance = tk.Button(boton_frame,
                                    text = 'Balance',
                                    command = balance,
                                    relief = 'raised',
                                    borderwidth = 3,
                                    width = 50,
                                    height = 5)
        boton_balance.grid(row=2, column = 0, pady= 5)

        def exit():
            controller.ir_a_frame('PaginaInicio')
        
        boton_salida = tk.Button(boton_frame,
                                    text = 'Salir',
                                    command = exit,
                                    relief = 'raised',
                                    borderwidth = 3,
                                    width = 50,
                                    height = 5)
        boton_salida.grid(row=3, column = 0, pady= 5)

        banco_foto = tk.PhotoImage(file = 'banco.png')
        banco_label = tk.Label(self, image = banco_foto)
        banco_label.place(x=0, y=0)
        banco_label.image = banco_foto

        boton_frame = tk.Frame(self, relief='raised', borderwidth=3) 
        boton_frame.pack(fill='x', side='bottom')

        visa_foto = tk.PhotoImage(file = 'visa.png') 
        visa_label = tk.Label(boton_frame, image=visa_foto)
        visa_label.pack(side='left')
        visa_label.image = visa_foto

        mastercard_foto = tk.PhotoImage(file = 'mastercard.png')
        mastercard_label = tk.Label(boton_frame, image=mastercard_foto)
        mastercard_label.pack(side='left')
        mastercard_label.image = mastercard_foto

        americanexpress_foto = tk.PhotoImage(file = 'americanexpress.png')
        americanexpress_label = tk.Label(boton_frame, image=americanexpress_foto)
        americanexpress_label.pack(side='left')
        americanexpress_label.image = americanexpress_foto
        ## importante tener las imagenes con los mismos pixeles, sino se pegan cada una con sus pixeles y queda mal

        def tick():
            tiempo_actual = time.strftime('%H:%M:%S') ## toquetear estos parametros para ponerlo en 24h, meterle segundos...
            tiempo_label.config(text=tiempo_actual)
            tiempo_label.after(200,tick)#para updatear el tiempo y que no se quede estanco
        tiempo_label = tk.Label(boton_frame,font=('orbitron',12))
        tiempo_label.pack(side='right')

        tick() ## esto es para que lo ejecute, y que no sea por un boton


class PaginaRetirada(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg = '#ffd633')
        self.controller = controller

        cabecero_label = tk.Label(self,
                                    text = 'Cajero',
                                    font=('orbitron', 45, 'bold'),
                                    foreground = '#ffffff',
                                    background = '#ffd633') 
        cabecero_label.pack(pady=25) 

        banco_foto = tk.PhotoImage(file = 'banco.png')
        banco_label = tk.Label(self, image = banco_foto)
        banco_label.place(x=0, y=0)
        banco_label.image = banco_foto

        label_elegir_cantidad = tk.Label(self,
                                    text = 'Introduzca la cantidad a retirar',
                                    font =('orbitron', 25, 'bold'),
                                    fg = '#ffffff',
                                    background = '#ffd633')
        label_elegir_cantidad.pack(pady=25)

        boton_frame = tk.Frame(self, relief='raised', borderwidth=3) 
        boton_frame.pack(fill='x', side='bottom')

        boton_frame = tk.Frame(self, bg = '#a6a6a6')
        boton_frame.pack(fill='both', expand = True)

        def withdraw(amount):
            global balance_actualizado
            balance_actualizado -= amount ## le quitamos al balance el amount que es el parametro que estamos metiendo por cada boton
            controller.datos_compartidos['Balance'].set(balance_actualizado) # esto es para actualizar el balance al diccionario de arriba
            controller.ir_a_frame('PaginaMenu')

        cinco_boton = tk.Button(boton_frame,
                                text = '5€',
                                command = lambda:withdraw(5), ## metemos lambda: porque a la funcion withdraw le estamos metiendo un parametro
                                relief = 'raised',
                                borderwidth = 3,
                                width = 50,
                                height = 5)
        cinco_boton.grid(row = 0, column = 0, pady = 5)

        diez_boton = tk.Button(boton_frame,
                                text = '10€',
                                command = lambda:withdraw(10),
                                relief = 'raised',
                                borderwidth = 3,
                                width = 50,
                                height = 5)
        diez_boton.grid(row = 1, column = 0, pady = 5)

        veinte_boton = tk.Button(boton_frame,
                        text = '20€',
                        command = lambda:withdraw(20),
                        relief = 'raised',
                        borderwidth = 3,
                        width = 50,
                        height = 5)
        veinte_boton.grid(row = 2, column = 0, pady = 5)

        cincuenta_boton = tk.Button(boton_frame,
                        text = '50€',
                        command = lambda:withdraw(50),
                        relief = 'raised',
                        borderwidth = 3,
                        width = 50,
                        height = 5)
        cincuenta_boton.grid(row = 3, column = 0, pady = 5) 

        cien_boton = tk.Button(boton_frame,
                        text = '100€',
                        command = lambda:withdraw(100),
                        relief = 'raised',
                        borderwidth = 3,
                        width = 50,
                        height = 5)
        cien_boton.grid(row = 0, column = 1, pady = 5, padx = 950) ## padx para ajustar la segunda columna al nivel que quiera (no necesito meterselo a todas)

        doscientos_boton = tk.Button(boton_frame,
                        text = '200€',
                        command = lambda:withdraw(200),
                        relief = 'raised',
                        borderwidth = 3,
                        width = 50,
                        height = 5)
        doscientos_boton.grid(row = 1, column = 1, pady = 5)

        quinientos_boton = tk.Button(boton_frame,
                text = '500€',
                command = lambda:withdraw(500),
                relief = 'raised',
                borderwidth = 3,
                width = 50,
                height = 5)
        quinientos_boton.grid(row = 2, column = 1, pady = 5)

        cash = tk.StringVar() ## se puede hacer con StringVar() o FloatVar(), pero al meterle numeros con int me vale

        boton_retirada_intro = tk.Entry(boton_frame,
                                    textvariable = cash,
                                    width=59,
                                    justify = 'right') ## para empezar a escribir desde la derecha
        boton_retirada_intro.focus_set() 
        boton_retirada_intro.grid(row = 3, column = 1, pady = 5, ipady = 30)

        ## boton que lleva a menu
        def menu():
            controller.ir_a_frame('PaginaMenu')

        boton_menu = tk.Button(boton_frame,
                                command = menu,
                                text = 'Menu',
                                relief = 'raised',
                                borderwidth = 3,
                                width = 50,
                                height = 5)
        boton_menu.grid(row=4, column=1)

        def other_amounth(_):
            global balance_actualizado 
            balance_actualizado -= int(cash.get())
            controller.datos_compartidos['Balance'].set(balance_actualizado)
            cash.set('')
            controller.ir_a_frame('PaginaMenu')
        
        boton_retirada_intro.bind('<Return>',other_amounth)
        
        boton_frame = tk.Frame(self, relief='raised', borderwidth=3) 
        boton_frame.pack(fill='x', side='bottom')

        visa_foto = tk.PhotoImage(file = 'visa.png') 
        visa_label = tk.Label(boton_frame, image=visa_foto)
        visa_label.pack(side='left')
        visa_label.image = visa_foto

        mastercard_foto = tk.PhotoImage(file = 'mastercard.png')
        mastercard_label = tk.Label(boton_frame, image=mastercard_foto)
        mastercard_label.pack(side='left')
        mastercard_label.image = mastercard_foto

        americanexpress_foto = tk.PhotoImage(file = 'americanexpress.png')
        americanexpress_label = tk.Label(boton_frame, image=americanexpress_foto)
        americanexpress_label.pack(side='left')
        americanexpress_label.image = americanexpress_foto
        

        def tick():
            tiempo_actual = time.strftime('%H:%M:%S')
            tiempo_label.config(text=tiempo_actual)
            tiempo_label.after(200,tick)
        tiempo_label = tk.Label(boton_frame,font=('orbitron',12))
        tiempo_label.pack(side='right')

        tick()

class PaginaDeposito(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg = '#ffd633')
        self.controller = controller
        cabecero_label = tk.Label(self,
                            text = 'Cajero',
                            font=('orbitron', 45, 'bold'),
                            foreground = '#ffffff',
                            background = '#ffd633')
        cabecero_label.pack(pady=25)

        espacio_label = tk.Label(self, height = 4, bg='#ffd633')
        espacio_label.pack()

        introducir_cantidad_label = tk.Label(self,
                                text= 'Introduzca la cantidad a ingresar',
                                font=('orbitron', 25, 'bold'),
                                bg='#ffd633',
                                fg = 'white')
        introducir_cantidad_label.pack(pady = 10)

        banco_foto = tk.PhotoImage(file = 'banco.png')
        banco_label = tk.Label(self, image = banco_foto)
        banco_label.place(x=0, y=0)
        banco_label.image = banco_foto

        cash = tk.StringVar()
        deposito_introducir = tk.Entry(self,
                                textvariable=cash,
                                font=('orbitron', 12),
                                width = 22)
        deposito_introducir.pack(ipady=7)
        deposito_introducir.focus_set() #### este comando para que parpadee no funciona, antes si lo hacia....

        def deposit_cash():
            global balance_actualizado
            balance_actualizado += int(cash.get())
            controller.datos_compartidos['Balance'].set(balance_actualizado)
            controller.ir_a_frame('PaginaMenu')
            cash.set('')
        boton_intro = tk.Button(self,
                                text='Enter',
                                command = deposit_cash,
                                relief = 'raised',
                                borderwidth=3,
                                width=40,
                                height = 3)
        boton_intro.pack(pady=10)

        ## boton que lleva a menu
        def menu():
            controller.ir_a_frame('PaginaMenu')

        boton_menu = tk.Button(self,
                                command = menu,
                                text = 'Menu',
                                relief = 'raised',
                                borderwidth = 3,
                                width = 40,
                                height = 3)
        boton_menu.pack()

        two_tone_label = tk.Label(self, bg = '#a6a6a6')
        two_tone_label.pack(fill= 'both', expand=True)

        boton_frame = tk.Frame(self, relief='raised', borderwidth=3) 
        boton_frame.pack(fill='x', side='bottom')

        visa_foto = tk.PhotoImage(file = 'visa.png') 
        visa_label = tk.Label(boton_frame, image=visa_foto)
        visa_label.pack(side='left')
        visa_label.image = visa_foto

        mastercard_foto = tk.PhotoImage(file = 'mastercard.png')
        mastercard_label = tk.Label(boton_frame, image=mastercard_foto)
        mastercard_label.pack(side='left')
        mastercard_label.image = mastercard_foto

        americanexpress_foto = tk.PhotoImage(file = 'americanexpress.png')
        americanexpress_label = tk.Label(boton_frame, image=americanexpress_foto)
        americanexpress_label.pack(side='left')
        americanexpress_label.image = americanexpress_foto

        def tick():
            tiempo_actual = time.strftime('%H:%M:%S')
            tiempo_label.config(text=tiempo_actual)
            tiempo_label.after(200,tick)
        tiempo_label = tk.Label(boton_frame,font=('orbitron',12))
        tiempo_label.pack(side='right')

        tick()

class PaginaBalance(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg = '#ffd633' )
        self.controller = controller
        cabecero_label = tk.Label(self,
                        text = 'Cajero',
                        font=('orbitron', 45, 'bold'),
                        foreground = '#ffffff',
                        background = '#ffd633')
        cabecero_label.pack(pady=25)

        banco_foto = tk.PhotoImage(file = 'banco.png')
        banco_label = tk.Label(self, image = banco_foto)
        banco_label.place(x=0, y=0)
        banco_label.image = banco_foto
        
        global balance_actualizado
        controller.datos_compartidos['Balance'].set(balance_actualizado)

        texto_label = tk.Label(self,
                        text = 'Su balance actual es de: ',
                        font=('orbitron', 45, 'bold'),
                        fg = 'white',
                        bg = '#ffd633',
                        anchor = 'w')
        texto_label.pack()

        balance_label = tk.Label(self,
                                textvariable= controller.datos_compartidos['Balance'],
                                font=('orbitron', 45, 'bold'),
                                fg = 'white',
                                bg = '#ffd633',
                                anchor = 'w')
        balance_label.pack()

        boton_frame = tk.Frame(self, bg = '#a6a6a6')
        boton_frame.pack(fill='both', expand = True)
        
        ## boton que lleva a menu
        def menu():
            controller.ir_a_frame('PaginaMenu')

        boton_menu = tk.Button(boton_frame,
                                command = menu,
                                text = 'Menu',
                                relief = 'raised',
                                borderwidth = 3,
                                width = 50,
                                height = 5)
        boton_menu.grid(row=0, column=0, pady=5)

        def exit():
            controller.ir_a_frame('PaginaInicio')
        
        boton_salida = tk.Button(boton_frame,
                                text = 'Salir',
                                command = exit,
                                relief = 'raised',
                                borderwidth = 3,
                                width = 50,
                                height= 5)
        boton_salida.grid(row=1, column=0, pady = 5)

        boton_frame = tk.Frame(self, relief='raised', borderwidth=3) 
        boton_frame.pack(fill='x', side='bottom')

        visa_foto = tk.PhotoImage(file = 'visa.png') 
        visa_label = tk.Label(boton_frame, image=visa_foto)
        visa_label.pack(side='left')
        visa_label.image = visa_foto

        mastercard_foto = tk.PhotoImage(file = 'mastercard.png')
        mastercard_label = tk.Label(boton_frame, image=mastercard_foto)
        mastercard_label.pack(side='left')
        mastercard_label.image = mastercard_foto

        americanexpress_foto = tk.PhotoImage(file = 'americanexpress.png')
        americanexpress_label = tk.Label(boton_frame, image=americanexpress_foto)
        americanexpress_label.pack(side='left')
        americanexpress_label.image = americanexpress_foto

        def tick():
            tiempo_actual = time.strftime('%H:%M:%S')
            tiempo_label.config(text=tiempo_actual)
            tiempo_label.after(200,tick)
        tiempo_label = tk.Label(boton_frame,font=('orbitron',12))
        tiempo_label.pack(side='right')

        tick()


if __name__ == "__main__":
    app = ArquitecturaGeneral()
    app.mainloop()