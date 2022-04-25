import math
from sre_compile import isstring
from scipy.stats import spearmanr
from scipy.stats import pearsonr
import numpy as np
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3

import matplotlib.pyplot as plt


root = Tk()
root.title(
    'ET3107 - A parametric study of spacecraft electric propulsion systems')
root.geometry("1280x800")


def enableEntry(props):
    thrusterEntry.config(state=props)
    orbitEntry.config(state=props)
    propellantEntry.config(state=props)
    inputPowerEntry.config(state=props)
    specificImpulseEntry.config(state=props)
    thrustEntry.config(state=props)
    massEntry.config(state=props)
    dateEntry.config(state=props)
    countryEntry.config(state=props)
    oidEntry.config(state='readonly')


def enableButton(props):
    updateButton.config(state=props)
    removeManyButton.config(state=props)
    moveUpButton.config(state=props)
    moveDownButton.config(state=props)
    # clearRecordButton.config(state=props)
    addButton.config(state=props)


def connectDatabase():
    #! Create a database or connect to one that exists
    connection = sqlite3.connect('dissertation.db')

    #! Create a cursor instance
    cursor = connection.cursor()

    #! Create a table inside the database
    cursor.execute('''
        CREATE TABLE if not exists ion_engines (
            thruster text, orbit text, propellant text,
            inputPower integer, specificImpulse real,
            thrust real, mass real, date integer, country text
        )
    ''')

    enableEntry('disable')
    enableButton('disable')
    connection.commit()
    connection.close()


def queryDatabase():
    # ? Clears the view everytime before querying
    tree.delete(*tree.get_children())

    connection = sqlite3.connect('dissertation.db')
    cursor = connection.cursor()

    cursor.execute('SELECT rowid, * FROM ion_engines')
    records = cursor.fetchall()

    #! Add data to the screen
    count = 0
    for record in records:
        if count % 2 == 0:
            tree.insert(parent='', index='end', iid=count, text='', values=(
                record[0], record[1], record[2], record[3], record[4], record[5], record[6], record[7], record[8], record[9]), tags=('evenrow',))
        else:
            tree.insert(parent='', index='end', iid=count, text='', values=(
                record[0], record[1], record[2], record[3], record[4], record[5], record[6], record[7], record[8], record[9]), tags=('oddrow',))
        count += 1

    connection.commit()
    connection.close()


#! Add style
style = ttk.Style()
#! Pick a theme
style.theme_use('default')
#! Configure treeview colours
style.configure('Treeview', background="#D3D3D3",
                foreground="black", rowheight=25, fieldbackground='#D3D3D3')
#! Change selected colour
style.map("Treeview", background=[('selected', "#347083")])

#! Create Treeview frame
treeFrame = Frame(root)
treeFrame.pack(pady=10)
#! Create Treeview scrollbar
treeScroll = Scrollbar(treeFrame)
treeScroll.pack(side=RIGHT, fill=Y)

#! Create the Treeview
tree = ttk.Treeview(treeFrame, yscrollcommand=treeScroll.set,
                    selectmode='extended')
tree.pack()

#! Configure the scrollbar
treeScroll.config(command=tree.yview)

#! Define columns and then create array of those columns
tree['columns'] = ('ID', 'Thruster', 'Orbit', 'Propellant',
                   'Input Power', 'Specific Impulse', 'Thrust', 'Mass', 'Date', 'Country')
# ? The below line of code converts the above list to an array
treeColumns = np.array(tree['columns'])

#! Add Menu
myMenu = Menu(root)
root.config(menu=myMenu)

#! Configure the menu
searchMenu = Menu(myMenu, tearoff=0)
myMenu.add_cascade(label="Options", menu=searchMenu)


#! Search records
def searchDatabase(queryToSearch):

    if queryToSearch == 'select a value':
        messagebox.showerror('ERROR', 'Please select a field', icon='warning')
    else:
        lookupRecord = searchEntry.get()
        # ? Close the search box
        search.destroy()

        # ? Deletes everything in the treeview
        tree.delete(*tree.get_children())

        connection = sqlite3.connect('dissertation.db')
        cursor = connection.cursor()

    if queryToSearch == 'thruster':
        cursor.execute(
            'SELECT rowid, * FROM ion_engines WHERE thruster like "%"||?||"%"', (lookupRecord,))
    elif queryToSearch == 'orbit':
        cursor.execute(
            'SELECT rowid, * FROM ion_engines WHERE orbit like "%"||?||"%"', (lookupRecord,))
    elif queryToSearch == 'propellant':
        cursor.execute(
            'SELECT rowid, * FROM ion_engines WHERE propellant like "%"||?||"%"', (lookupRecord,))
    elif queryToSearch == 'input power':
        cursor.execute(
            'SELECT rowid, * FROM ion_engines WHERE inputPower like "%"||?||"%"', (lookupRecord,))
    elif queryToSearch == 'specific impulse':
        cursor.execute(
            'SELECT rowid, * FROM ion_engines WHERE specificImpulse like "%"||?||"%"', (lookupRecord,))
    elif queryToSearch == 'thrust':
        cursor.execute(
            'SELECT rowid, * FROM ion_engines WHERE thrust like "%"||?||"%"', (lookupRecord,))
    elif queryToSearch == 'mass':
        cursor.execute(
            'SELECT rowid, * FROM ion_engines WHERE mass like "%"||?||"%"', (lookupRecord,))
    elif queryToSearch == 'date':
        cursor.execute(
            'SELECT rowid, * FROM ion_engines WHERE date like "%"||?||"%"', (lookupRecord,))
    elif queryToSearch == 'country':
        cursor.execute(
            'SELECT rowid, * FROM ion_engines WHERE country like "%"||?||"%"', (lookupRecord,))
    records = cursor.fetchall()

    #! Add data to the screen
    count = 0
    for record in records:
        if count % 2 == 0:
            tree.insert(parent='', index='end', iid=count, text='', values=(
                record[0], record[1], record[2], record[3], record[4], record[5], record[6], record[7], record[8], record[9]), tags=('evenrow',))
        else:
            tree.insert(parent='', index='end', iid=count, text='', values=(
                record[0], record[1], record[2], record[3], record[4], record[5], record[6], record[7], record[8], record[9]), tags=('oddrow',))
        count += 1

    connection.commit()
    connection.close()


#! Search menu function
def lookupRecords():
    global searchEntry, search
    search = Toplevel(root)
    search.title('Lookup Records')
    search.geometry('400x200')

    # ? Create label frame
    searchFrame = LabelFrame(search, text='Search')
    searchFrame.pack(padx=10, pady=10)

    clicked = StringVar(searchFrame)
    clicked.set('Select a value')
    searchDrop = OptionMenu(searchFrame, clicked, *treeColumns)
    searchDrop.pack()

    # ? Add entry box
    searchEntry = Entry(searchFrame, font=('Helvetica', 18))
    searchEntry.pack(padx=20, pady=20)

    # ? Add button
    searchButton = Button(search, text='Search records',
                          command=lambda: searchDatabase(clicked.get().lower()))
    searchButton.pack(padx=20, pady=20)


#! Drop down menu
searchMenu.add_command(label='Search', command=lookupRecords)
searchMenu.add_command(label='Reset', command=queryDatabase)
searchMenu.add_separator()
searchMenu.add_command(label='Exit', command=root.quit)

#! Format columns
tree.column('#0', width=0, stretch=NO)
tree.column('ID', anchor=CENTER, width=35)
tree.column('Thruster', anchor=CENTER, width=130)
tree.column('Orbit', anchor=CENTER, width=130)
tree.column('Propellant', anchor=CENTER, width=130)
tree.column('Input Power', anchor=CENTER, width=130)
tree.column('Specific Impulse', anchor=CENTER, width=130)
tree.column('Thrust', anchor=CENTER, width=130)
tree.column('Mass', anchor=CENTER, width=100)
tree.column('Date', anchor=CENTER, width=80)
tree.column('Country', anchor=CENTER, width=130)


#! Disable interaction with the table headings
def unclickHeader():
    enableEntry('disable')
    enableButton('disable')
    newRecordButton.config(state='normal')
    tree.focus_set()


#! Graph settings
def graphSettings():
    global plot
    plot = Toplevel(root)
    plot.title('Plot Records')
    plot.geometry('700x350')

    # ? Create label frame
    plotFrame = Label(plot, text='Plot')
    plotFrame.grid(row=0, column=0, padx=10, pady=10)

    clickedX = StringVar(plot)
    clickedX.set('Select X value')
    clickedY = StringVar(plot)
    clickedY.set('Select Y value')
    plotDropXLabel = Label(plot, text='X axis')
    plotDropYLabel = Label(plot, text='Y axis')

    def toggleLog():
        if isChecked.get():
            return True
        else:
            return False

    isChecked = BooleanVar()
    checkbox = Checkbutton(
        plot, text='Log mode', variable=isChecked, command=toggleLog)
    checkbox.grid(row=2, column=3)

    plotDropX = OptionMenu(plot, clickedX, *treeColumns[4:9])
    plotDropY = OptionMenu(plot, clickedY, *treeColumns[4:9])
    plotDropXLabel.grid(row=0, column=1, padx=10, pady=10)
    plotDropX.grid(row=1, column=1, padx=10, pady=10)
    plotDropYLabel.grid(row=0, column=2, padx=10, pady=10)
    plotDropY.grid(row=1, column=2, padx=10, pady=10)
    massNote = Label(plot, text='Not enough data to plot mass.')
    massNote.grid(row=2, column=1)

    # ? Add button
    plotButton = Button(plot, text='Plot records',
                        command=lambda: checkAndPlot(clickedX.get(), clickedY.get(), toggleLog()))
    plotButton.grid(row=1, column=3, padx=20, pady=20)


#! Running few checks before plotting the relevant graph
def checkAndPlot(x, y, isLog):
    thrusterArray = []
    inputPowerArray = []
    specificImpulseArray = []
    thrustArray = []
    massArray = []
    dateArray = []

    if (x == y):
        messagebox.showerror(
            'ERROR', 'You cannot have the same quantity on both axes!')
        return False
    else:
        for line in tree.get_children():
            thrusterPlot = tree.item(line)['values'][1]
            inputPowerPlot = tree.item(line)['values'][4]
            specificImpulsePlot = tree.item(line)['values'][5]
            thrustPlot = tree.item(line)['values'][6]
            massPlot = tree.item(line)['values'][7]
            datePlot = tree.item(line)['values'][8]

            thrusterArray.append(thrusterPlot)
            inputPowerArray.append(inputPowerPlot)
            specificImpulseArray.append(specificImpulsePlot)
            thrustArray.append(thrustPlot)
            massArray.append(massPlot)
            dateArray.append(datePlot)

        inputPowerArray = np.array(inputPowerArray)
        specificImpulseArray = np.array(specificImpulseArray)
        thrustArray = np.array(thrustArray)
        massArray = np.array(massArray)
        dateArray = np.array(dateArray)

        if isLog:
            if (x == 'Input Power'):
                xValue = [math.log(float(item)) for item in inputPowerArray]
            elif (x == 'Specific Impulse'):
                xValue = [math.log(float(item))
                          for item in specificImpulseArray]
            elif (x == 'Thrust'):
                xValue = [math.log(float(item)) for item in thrustArray]
            elif (x == 'Mass'):
                xValue = [math.log(float(item)) for item in massArray]
            elif (x == 'Date'):
                xValue = [math.log(float(item)) for item in dateArray]

            if (y == 'Input Power'):
                yValue = [math.log(float(item)) for item in inputPowerArray]
            elif (y == 'Specific Impulse'):
                yValue = [math.log(float(item))
                          for item in specificImpulseArray]
            elif (y == 'Thrust'):
                yValue = [math.log(float(item)) for item in thrustArray]
            elif (y == 'Mass'):
                yValue = [math.log(float(item)) for item in massArray]
            elif (y == 'Date'):
                yValue = [math.log(float(item)) for item in dateArray]
        else:
            if (x == 'Input Power'):
                xValue = [float(item) for item in inputPowerArray]
            elif (x == 'Specific Impulse'):
                xValue = [float(item) for item in specificImpulseArray]
            elif (x == 'Thrust'):
                xValue = [float(item) for item in thrustArray]
            elif (x == 'Mass'):
                xValue = [float(item) for item in massArray]
            elif (x == 'Date'):
                xValue = [float(item) for item in dateArray]

            if (y == 'Input Power'):
                yValue = [float(item) for item in inputPowerArray]
            elif (y == 'Specific Impulse'):
                yValue = [float(item) for item in specificImpulseArray]
            elif (y == 'Thrust'):
                yValue = [float(item) for item in thrustArray]
            elif (y == 'Mass'):
                yValue = [float(item) for item in massArray]
            elif (y == 'Date'):
                yValue = [float(item) for item in dateArray]

        covariance = np.cov(xValue, yValue)
        print('covariance is: ', covariance)

        pearsonCorr, _ = pearsonr(xValue, yValue)
        print("Pearson's correlation: ", pearsonCorr)

        spearmanCorr, _ = spearmanr(xValue, yValue)
        print("Spearman's correlation: ", spearmanCorr)

        # ? Correlation textboxes
        covarianceLabel = Label(plot, text='Covariance')
        covarianceLabel.grid(row=3, column=0, padx=10, pady=10)
        covarianceEntry1 = Entry(plot, width=15)
        covarianceEntry1.grid(row=3, column=1, padx=10, pady=10)
        covarianceEntry2 = Entry(plot, width=15)
        covarianceEntry2.grid(row=3, column=2, padx=10, pady=10)
        covarianceEntry3 = Entry(plot, width=15)
        covarianceEntry3.grid(row=4, column=1, padx=10, pady=10)
        covarianceEntry4 = Entry(plot, width=15)
        covarianceEntry4.grid(row=4, column=2, padx=10, pady=10)
        pearsonLabel = Label(plot, text='Pearson Correlation')
        pearsonLabel.grid(row=5, column=0, padx=10, pady=10)
        pearsonEntry = Entry(plot, width=15)
        pearsonEntry.grid(row=5, column=1, padx=10, pady=10)
        spearmanLabel = Label(plot, text='Spearman Correlation')
        spearmanLabel.grid(row=6, column=0, padx=10, pady=10)
        spearmanEntry = Entry(plot, width=15)
        spearmanEntry.grid(row=6, column=1, padx=10, pady=10)

        covarianceMatrix1 = IntVar()
        covarianceMatrix1.set(round(covariance[0][0], 4))
        covarianceMatrix2 = IntVar()
        covarianceMatrix2.set(round(covariance[0][1], 4))
        covarianceMatrix3 = IntVar()
        covarianceMatrix3.set(round(covariance[1][0], 4))
        covarianceMatrix4 = IntVar()
        covarianceMatrix4.set(round(covariance[1][1], 4))
        pearsonText = IntVar()
        pearsonText.set(round(pearsonCorr, 4))
        spearmanText = IntVar()
        spearmanText.set(round(spearmanCorr, 4))

        covarianceEntry1.config(
            state='readonly', textvariable=covarianceMatrix1)
        covarianceEntry2.config(
            state='readonly', textvariable=covarianceMatrix2)
        covarianceEntry3.config(
            state='readonly', textvariable=covarianceMatrix3)
        covarianceEntry4.config(
            state='readonly', textvariable=covarianceMatrix4)
        pearsonEntry.config(state='readonly', textvariable=pearsonText)
        spearmanEntry.config(state='readonly', textvariable=spearmanText)

        # ? Creating a tuple of values where the values of the
        # ? two datasets are paired together
        xs, ys = zip(*sorted(zip(xValue, yValue)))

        # ? Creating scatter plot
        plt.scatter(xs, ys)

        plt.title('Log mode: ON' if isLog else 'Log mode: OFF')
        plt.xlabel(x, labelpad=7)
        plt.ylabel(y, labelpad=5)

        # ? Appending labels to graph
        for i, txt in enumerate(thrusterArray):
            plt.annotate(txt, (xValue[i], yValue[i]),
                         textcoords='offset points', xytext=(0, 4), ha='center', fontsize='small')
        plt.show()

        return covariance, pearsonCorr, spearmanCorr


#! Create headings
tree.heading('#0', text='', anchor=W)
tree.heading('ID', text='ID', anchor=CENTER, command=unclickHeader)
tree.heading('Thruster', text='Thruster', anchor=CENTER, command=unclickHeader)
tree.heading('Orbit', text='Orbit', anchor=CENTER, command=unclickHeader)
tree.heading('Propellant', text='Propellant',
             anchor=CENTER, command=unclickHeader)
tree.heading('Input Power', text='Input Power (W)',
             anchor=CENTER, command=unclickHeader)
tree.heading('Specific Impulse', text='Specific Impulse (s)',
             anchor=CENTER, command=unclickHeader)
tree.heading('Thrust', text='Thrust (mN)',
             anchor=CENTER, command=unclickHeader)
tree.heading('Mass', text='Mass (kg)',
             anchor=CENTER, command=unclickHeader)
tree.heading('Date', text='Date (Year)',
             anchor=CENTER, command=unclickHeader)
tree.heading('Country', text='Country', anchor=CENTER, command=unclickHeader)


#! Create striped row tags
tree.tag_configure('oddrow', background='white')
tree.tag_configure('evenrow', background='lightblue')


#! Add record entry boxes
dataFrame = LabelFrame(root, text='Record')
dataFrame.pack(fill='x', expand='yes', padx=20)

thrusterLabel = Label(dataFrame, text='Thruster')
thrusterLabel.grid(row=0, column=0, padx=10, pady=10)
thrusterEntry = Entry(dataFrame, width=15)
thrusterEntry.grid(row=0, column=1, padx=10, pady=10)

orbitLabel = Label(dataFrame, text='Orbit')
orbitLabel.grid(row=0, column=2, padx=10, pady=10)
orbitEntry = Entry(dataFrame, width=15)
orbitEntry.grid(row=0, column=3, padx=10, pady=10)

propellantLabel = Label(dataFrame, text='Propellant')
propellantLabel.grid(row=0, column=4, padx=10, pady=10)
propellantEntry = Entry(dataFrame, width=15)
propellantEntry.grid(row=0, column=5, padx=10, pady=10)

inputPowerLabel = Label(dataFrame, text='Input Power (W)')
inputPowerLabel.grid(row=1, column=0, padx=10, pady=10)
inputPowerEntry = Entry(dataFrame, width=15)
inputPowerEntry.grid(row=1, column=1, padx=10, pady=10)

specificImpulseLabel = Label(dataFrame, text='Specific Impulse (s)')
specificImpulseLabel.grid(row=1, column=2, padx=10, pady=10)
specificImpulseEntry = Entry(dataFrame, width=15)
specificImpulseEntry.grid(row=1, column=3, padx=10, pady=10)

thrustLabel = Label(dataFrame, text='Thrust (mN)')
thrustLabel.grid(row=1, column=4, padx=10, pady=10)
thrustEntry = Entry(dataFrame, width=15)
thrustEntry.grid(row=1, column=5, padx=10, pady=10)

massLabel = Label(dataFrame, text='Mass (kg)')
massLabel.grid(row=2, column=0, padx=10, pady=10)
massEntry = Entry(dataFrame, width=15)
massEntry.grid(row=2, column=1, padx=10, pady=10)

dateLabel = Label(dataFrame, text='Date (Year)')
dateLabel.grid(row=2, column=2, padx=10, pady=10)
dateEntry = Entry(dataFrame, width=15)
dateEntry.grid(row=2, column=3, padx=10, pady=10)

countryLabel = Label(dataFrame, text='Country')
countryLabel.grid(row=2, column=4, padx=10, pady=10)
countryEntry = Entry(dataFrame, width=15)
countryEntry.grid(row=2, column=5, padx=10, pady=10)

oidLabel = Label(dataFrame, text='ID')
oidLabel.grid(row=3, column=2, padx=10, pady=10)
oidEntry = Entry(dataFrame, width=15)
oidEntry.grid(row=3, column=3, padx=10, pady=10)


def deselect():
    tree.selection_set()


#! Move row up
def moveUp():
    rows = tree.selection()
    for row in rows:
        tree.move(row, tree.parent(row), tree.index(row)-1)


#! Move row down
def moveDown():
    rows = tree.selection()
    for row in reversed(rows):
        tree.move(row, tree.parent(row), tree.index(row)+1)


#! Remove selected records
def removeSelected():
    confirmDelete = messagebox.askquestion(
        'Remove record?', 'Are you sure you want to delete this record?', icon='warning')
    if confirmDelete == 'yes':
        x = tree.selection()
        for record in x:
            tree.delete(record)
        connection = sqlite3.connect('dissertation.db')
        cursor = connection.cursor()

        cursor.execute("DELETE from ion_engines WHERE oid =" + oidEntry.get())

        connection.commit()
        connection.close()
    else:
        return
    clearEntries()
    enableEntry('disable')
    enableButton('disable')
    newRecordButton.config(state='normal')


#! Clear entry boxes
def clearEntries():
    # ? Clear entry boxes
    oidEntry.delete(0, END)
    thrusterEntry.delete(0, END)
    orbitEntry.delete(0, END)
    propellantEntry.delete(0, END)
    inputPowerEntry.delete(0, END)
    specificImpulseEntry.delete(0, END)
    thrustEntry.delete(0, END)
    massEntry.delete(0, END)
    dateEntry.delete(0, END)
    countryEntry.delete(0, END)

    enableEntry('disable')
    enableButton('disable')
    newRecordButton.config(state='normal')
    tree.focus_set()


#! Select record
def selectRecord(e):
    clearEntries()

    # ? Grab record number
    selected = tree.focus()
    # ? Grab record values
    values = tree.item(selected, 'values')

    enableEntry('normal')
    enableButton('normal')
    addButton.config(state='disable')
    newRecordButton.config(state='disable')
    idText = IntVar()
    idText.set(values[0])

    # ? Output to entry boxes
    # oidEntry.insert(0, idText)
    oidEntry.config(state='readonly', textvariable=idText)
    thrusterEntry.insert(0, values[1])
    orbitEntry.insert(0, values[2])
    propellantEntry.insert(0, values[3])
    inputPowerEntry.insert(0, values[4])
    specificImpulseEntry.insert(0, values[5])
    thrustEntry.insert(0, values[6])
    massEntry.insert(0, values[7])
    dateEntry.insert(0, values[8])
    countryEntry.insert(0, values[9])

    return thrusterEntry, orbitEntry, propellantEntry, inputPowerEntry, specificImpulseEntry, thrustEntry, massEntry, dateEntry, countryEntry


#! Update records
def updateRecords():
    global selected
    confirmEdit = messagebox.askquestion(
        'Edit record?', 'Are you sure you want to edit this record?', icon='warning')
    if confirmEdit == 'yes':
        selected = tree.focus()
        tree.item(selected, text='', values=(oidEntry.get(), thrusterEntry.get(), orbitEntry.get(), propellantEntry.get(), inputPowerEntry.get(
        ), specificImpulseEntry.get(), thrustEntry.get(), massEntry.get(), dateEntry.get(), countryEntry.get(),))

        # ? Update the database
        connection = sqlite3.connect('dissertation.db')
        cursor = connection.cursor()

        cursor.execute('''
            UPDATE ion_engines SET thruster = :thruster, orbit = :orbit, propellant = :propellant, inputPower = :inputPower, specificImpulse = :specificImpulse, thrust = :thrust, mass = :mass, date = :date, country = :country

            WHERE oid = :oid''',
                       {
                           'thruster': thrusterEntry.get(),
                           'orbit': orbitEntry.get(),
                           'propellant': propellantEntry.get(),
                           'inputPower': inputPowerEntry.get(),
                           'specificImpulse': specificImpulseEntry.get(),
                           'thrust': thrustEntry.get(),
                           'mass': massEntry.get(),
                           'date': dateEntry.get(),
                           'country': countryEntry.get(),
                           'oid': oidEntry.get()
                       })

        connection.commit()
        connection.close()

    clearEntries()
    enableEntry('disable')
    enableButton('disable')
    tree.focus_set()
    deselect()


#! Check if textbox is empty
def isFull():
    if len(thrusterEntry.get()) == 0 or len(orbitEntry.get()) == 0 or len(propellantEntry.get()) == 0 or len(inputPowerEntry.get()) == 0 or len(specificImpulseEntry.get()) == 0 or len(thrustEntry.get()) == 0 or len(massEntry.get()) == 0:
        return True


#! Add new record
def addRecords():
    if isFull() == True:
        messagebox.showerror(
            'ERROR', 'Please input all the values', icon='warning')
        thrusterEntry.focus_set()
    else:
        connection = sqlite3.connect('dissertation.db')
        cursor = connection.cursor()

        cursor.execute('''INSERT INTO ion_engines VALUES (:thruster, :orbit,
        :propellant, :inputPower, :specificImpulse, :thrust, :mass, :date,
         :country)''',
                       {
                           'thruster': thrusterEntry.get(),
                           'orbit': orbitEntry.get(),
                           'propellant': propellantEntry.get(),
                           'inputPower': inputPowerEntry.get(),
                           'specificImpulse': specificImpulseEntry.get(),
                           'thrust': thrustEntry.get(),
                           'mass': massEntry.get(),
                           'date': dateEntry.get(),
                           'country': countryEntry.get(),
                       })

        connection.commit()
        connection.close()
        clearEntries()
        enableEntry('disable')
        enableButton('disable')
        newRecordButton.config(state='normal')
        tree.focus_set()
        deselect()

        # ? Clear the treeview table
        tree.delete(*tree.get_children())
        # ? Query the database again (to make values reappear, this time the table is updated)
        queryDatabase()


#! Add buttons
buttonFrame = LabelFrame(root, text='Commands')
buttonFrame.pack(fill=X, expand=YES, padx=20)

updateButton = Button(buttonFrame, text='Update Record',
                      command=updateRecords, width=16)
updateButton.grid(row=0, column=0, padx=10, pady=10)
addButton = Button(buttonFrame, text='Add Record',
                   command=addRecords, width=16)
addButton.grid(row=0, column=1, padx=10, pady=10)
# removeOneButton = Button(
#     buttonFrame, text='Remove One Selected', command=removeOne)
# removeOneButton.grid(row=0, column=3, padx=10, pady=10)
removeManyButton = Button(
    buttonFrame, text='Remove Selected', command=removeSelected, width=16)
removeManyButton.grid(row=0, column=4, padx=10, pady=10)
moveUpButton = Button(buttonFrame, text='Move Up',
                      command=moveUp, width=16)
moveUpButton.grid(row=0, column=5, padx=10, pady=10)
moveDownButton = Button(buttonFrame, text='Move Down',
                        command=moveDown, width=16)
moveDownButton.grid(row=0, column=6, padx=10, pady=10)
clearRecordButton = Button(
    buttonFrame, text='Clear Entries', command=lambda: [clearEntries(), deselect()], width=16)
clearRecordButton.grid(row=0, column=7, padx=10, pady=10)
newRecordButton = Button(dataFrame, text='New Record',
                         command=lambda: [enableEntry('normal'), addButton.config(state='normal'), newRecordButton.config(state='disabled')], width=16)
newRecordButton.grid(row=0, column=6, padx=10, pady=10)

plotGraphButton = Button(dataFrame, text='Plot Graph',
                         command=graphSettings, width=16)
plotGraphButton.grid(row=1, column=6, padx=10, pady=10)

#! Bind the treeview
tree.bind('<ButtonRelease>', selectRecord)

#! Run to pull data from database on start
connectDatabase()
queryDatabase()

root.mainloop()
