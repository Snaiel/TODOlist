import PySimpleGUI as sg
from datetime import datetime





#  /$$    /$$                     /$$           /$$       /$$                    
# | $$   | $$                    |__/          | $$      | $$                    
# | $$   | $$  /$$$$$$   /$$$$$$  /$$  /$$$$$$ | $$$$$$$ | $$  /$$$$$$   /$$$$$$$
# |  $$ / $$/ |____  $$ /$$__  $$| $$ |____  $$| $$__  $$| $$ /$$__  $$ /$$_____/
#  \  $$ $$/   /$$$$$$$| $$  \__/| $$  /$$$$$$$| $$  \ $$| $$| $$$$$$$$|  $$$$$$ 
#   \  $$$/   /$$__  $$| $$      | $$ /$$__  $$| $$  | $$| $$| $$_____/ \____  $$
#    \  $/   |  $$$$$$$| $$      | $$|  $$$$$$$| $$$$$$$/| $$|  $$$$$$$ /$$$$$$$/
#     \_/     \_______/|__/      |__/ \_______/|_______/ |__/ \_______/|_______/   
                                                                                                                                                      
SYMBOL_RIGHT ='►'
SYMBOL_DOWN =  '▼'

menus = {
        'Menu Bar': [['Edit', ['Undo', 'Redo', '---', 'Add', ['Task::ADD', 'Section::ADD', 'List::ADD(MENU)', 'Paste::ADD'], ['Delete', ['List::DELETE'], '---', 'Lists', 'Settings']]], ['Help', ['About', 'Wiki']]],
        'Disabled Menu Bar': [['Edit', ['!Undo', '!Redo', '---', '!Add', ['Task'], ['!Delete', ['List'], '---', 'Lists', 'Settings']]], ['Help', ['About', 'Wiki']]],
        'Task 0 & 1': ['Right', ['Move', ['Up::MOVE', 'Down::MOVE'], '---', 'Copy::TASK', 'Cut::TASK', '---', 'Insert', ['Task::INSERT', 'Section::INSERT', 'Paste::INSERT'], 'Rename', 'Delete']],
        'Section 0 & 1': ['&Right', ['Move', ['Up::MOVE', 'Down::MOVE'], '---', 'Copy::SECTION', 'Cut::SECTION', '---', 'Add', ['Task::ADDTO', 'Section::ADDTO', 'Paste::ADDTO'], '&Insert', ['Task::INSERT', 'Section::INSERT', 'Paste::INSERT'],  'Rename', 'Delete']],
        'Task 2': ['Right', ['Move', ['Up::MOVE', 'Down::MOVE'], '---', 'Copy::TASK', 'Cut::TASK', '---', 'Insert', ['Task::INSERT', 'Paste::INSERT'], 'Rename', 'Delete']],
        'Section 2': ['Right', ['Move', ['Up::MOVE', 'Down::MOVE'], '---', 'Copy::SECTION', 'Cut::SECTION', '---', 'Add', ['Task::ADDTO', 'Paste::ADDTO'], 'Rename', 'Delete'], '&Insert', ['Task::INSERT', 'Section::INSERT']]
        }

programValues = {
                'List': '',
                'TimeToResetDaily': '',
                'BGColour': '',
                'BColour': '',
                'TColour1': '',
                'TColour2': ''
                }

tempData = {
            'ListIndex': '',
            'WhenLastClosed': '',
            'elementKeys': [],
            'sectionsOpen': {},
            'combo': [],
            'latestElementRightClicked': '',
            'listSelectedToEdit': '',
            'lastListOn': '',
            'elementCopied': ('', None),
            'elementMoving': ('', None),
            'previousSettings': {
                'TimeToResetDaily': '',
                'BGColour': '',
                'BColour': '',
                'TColour1': '',
                'TColour2': ''
                }
            }

data = []




















#  /$$$$$$$$                                 /$$     /$$                              
# | $$_____/                                | $$    |__/                              
# | $$       /$$   /$$ /$$$$$$$   /$$$$$$$ /$$$$$$   /$$  /$$$$$$  /$$$$$$$   /$$$$$$$
# | $$$$$   | $$  | $$| $$__  $$ /$$_____/|_  $$_/  | $$ /$$__  $$| $$__  $$ /$$_____/
# | $$__/   | $$  | $$| $$  \ $$| $$        | $$    | $$| $$  \ $$| $$  \ $$|  $$$$$$ 
# | $$      | $$  | $$| $$  | $$| $$        | $$ /$$| $$| $$  | $$| $$  | $$ \____  $$
# | $$      |  $$$$$$/| $$  | $$|  $$$$$$$  |  $$$$/| $$|  $$$$$$/| $$  | $$ /$$$$$$$/
# |__/       \______/ |__/  |__/ \_______/   \___/  |__/ \______/ |__/  |__/|_______/

def readDataFile():
    tasks = ['(T)', '(F)']
    booleans = {
        '(T)': True,
        '(F)': False,
        '(O)': True,
        '(C)': False
    }

    with open('data.txt') as f:
        file = f.read().splitlines()

        settings = file[(file.index('Settings:') + 1):file.index('Data:')]
        taskData = file[(file.index('Data:') + 1):]

        previousLine = None

        todolistData = []
        listData = []
        section = []
        subsection = []

        for i in settings:
            i = i.split()
    
            if i[0] == 'TimeToResetDaily:':
                programValues['TimeToResetDaily'] = i[1]
            if i[0] == 'BGColour:':
                programValues['BGColour'] = i[1]
                continue
            if i[0] == 'BColour:':
                programValues['BColour'] = i[1]
                continue
            if i[0] == 'TColour1:':
                programValues['TColour1'] = i[1]
                continue
            if i[0] == 'TColour2:':
                programValues['TColour2'] = i[1]
                continue

        for i in taskData:
            i = i.split()

            if i[0] == 'WhenLastClosed:':
                tempData['WhenLastClosed'] = ' '.join(i[1:3])
                

            if previousLine != None and previousLine[0] == '---' and i[0] != '---':
                if i[0] == '----':
                    subsection.append({' '.join(i[1:-1]): booleans[i[-1]]})
                elif len(section) != 0:
                    listData.append(section.copy())
                    section.clear() 

            if previousLine != None and previousLine[0] == '----' and i[0] != '----':
                if len(subsection) != 0:
                    section.append(subsection.copy())
                    subsection.clear() 

            if i[0] == '----' and previousLine[0] == '----':
                subsection.append({' '.join(i[1:-1]): booleans[i[-1]]})

            if i[0] == '---':

                if i[-1] not in tasks and previousLine[0] == '---' and previousLine[-1] not in tasks:
                    section.append(subsection.copy())
                    subsection.clear() 

                if i[-1] in tasks:
                    section.append({' '.join(i[1:-1]): booleans[i[-1]]})
                else:
                    subsection.append({' '.join(i[1:-1]): booleans[i[-1]]})

            if i[0] == '--':

                if i[-1] not in tasks and previousLine[0] == '--' and previousLine[-1] not in tasks:
                    listData.append(section.copy())
                    section.clear() 

                if i[-1] in tasks:
                    listData.append({' '.join(i[1:-1]): booleans[i[-1]]})
                else:
                    section.append({' '.join(i[1:-1]): booleans[i[-1]]})

            if i[0] == '-':
                if len(listData) != 0:
                    todolistData.append(listData.copy())
                    listData.clear()

                if i[-1] == '!':
                    listData.append(' '.join(i[1:-1]))
                    programValues['List'] = ' '.join(i[1:-1])
                else:
                    listData.append(' '.join(i[1:]))

            previousLine = i


        if len(subsection) != 0:
            section.append(subsection.copy())
            subsection.clear()
        if len(section) != 0:
            listData.append(section.copy())
            section.clear()
        if len(listData) != 0:
            todolistData.append(listData.copy())
            listData.clear()

        global data
        data = todolistData

def writeDataFile():
    with open('data.txt', 'w') as f:

        lines = ['Settings:' ,'Data:']
        filesettings = [
                            f"    TimeToResetDaily: {programValues['TimeToResetDaily']}", 
                            f"    BGColour: {programValues['BGColour']}", 
                            f"    BColour: {programValues['BColour']}",
                            f"    TColour1: {programValues['TColour1']}",
                            f"    TColour2: {programValues['TColour2']}"
                        ]
        filedata = [
            f"    WhenLastClosed: {tempData['WhenLastClosed']}"
        ]

        for i in data:
            todolist = i
            for content in todolist:
                if todolist.index(content) == 0:
                    filedata.append(f"- {content}{' !' if programValues['List'] == content else ''}")

                if type(content) is dict:
                    for key, value in content.items():
                        filedata.append(f"-- {key} {'(T)' if value == True else '(F)'}")

                if type(content) is list:

                    header = None
                    opened = None

                    for key, value in content[0].items():
                        header = key
                        opened = value

                    filedata.append(f"-- {header} {'(O)' if opened == True else '(C)'}")

                    for contentInSection in content:
                        if type(contentInSection) is dict and content.index(contentInSection) != 0:
                            for key, value in contentInSection.items():
                                filedata.append(f"--- {key} {'(T)' if value == True else '(F)'}")

                        if type(contentInSection) is list:

                            subheader = None
                            subopened = None

                            for key, value in contentInSection[0].items():
                                subheader = key
                                subopened = value

                            filedata.append(f"--- {subheader} {'(O)' if subopened == True else '(C)'}")

                            for contentInSubSection in contentInSection:
                                if type(contentInSubSection) is dict and contentInSection.index(contentInSubSection) != 0:
                                    for key, value in contentInSubSection.items():
                                        filedata.append(f"---- {key} {'(T)' if value == True else '(F)'}")

        lines[1:1] = filesettings
        lines.extend(filedata)

        f.write('\n'.join(lines))

def resetDaily():
    for todolist in data:
        for content in todolist:
            if type(content) is list and 'Daily' in content[0]:
                for contentInSection in content:
                    if content.index(contentInSection) == 0:
                        continue

                    if type(contentInSection) is dict:
                        for key in contentInSection:
                            contentInSection[key] = False

                    if type(contentInSection) is list:
                        for subTask in contentInSection:
                            if contentInSection.index(subTask) == 0:
                                continue

                            if type(subTask) is dict:
                                for key in subTask:
                                    subTask[key] = False

def colours():
    BGColour = programValues['BGColour']
    BColour = programValues['BColour']
    TColour1 = programValues['TColour1']
    TColour2 = programValues['TColour2']

    sg.theme_background_color(BGColour)
    sg.theme_element_background_color(BGColour)
    sg.theme_text_element_background_color(BGColour)
    sg.theme_button_color((TColour2, BColour))
    sg.theme_text_color(TColour1)
    sg.theme_input_text_color(TColour2)

def collapse(layout, key, isVisible):
    """
    Helper function that creates a Column that can be later made hidden, thus appearing "collapsed"
    :param layout: The layout for the section
    :param key: Key used to make this seciton visible / invisible
    :return: A pinned column that can be placed directly into your layout
    :rtype: sg.pin
    """
    return sg.pin(sg.Column(layout, key=key, visible=isVisible, pad=(15,0)))

def symbol(opened):
    if opened is True:
        return SYMBOL_DOWN
    else:
        return SYMBOL_RIGHT

def createCombo():
    tempData['combo'].clear()
    combo = tempData['combo']
    for i in data:
        combo.append(i[0])

def createTask(name, checked, listName, hierarchyIndex, sectionID):
    for i in data:
        if i[0] == listName:
            ListIndex = str(data.index(i)).zfill(2)
            hierarchyIndex = str(hierarchyIndex).zfill(2)
            sectionID = str(sectionID).zfill(2)
            elementIndexes = f"{ListIndex} {hierarchyIndex} {sectionID}"

            checkBoxKey = f"{elementIndexes} TASK CHECKBOX {name}"
            checkBoxTextKey = f"{elementIndexes} TASK TEXT {name}"

            rightClickMenu = menus['Task 0 & 1']
            if hierarchyIndex == '02':
                rightClickMenu = menus['Task 2']

            if len(name) > 30:
                tooltip = name
            else:
                tooltip = None

            tempData['elementKeys'].append(f"{elementIndexes} TASK {name}")
            return [sg.Checkbox('', default=checked, enable_events=True, key=checkBoxKey, pad=((10, 0),(3,3))), sg.T(name, right_click_menu=rightClickMenu, pad=(0,0), key=checkBoxTextKey, enable_events=True, tooltip=tooltip)]

def createSection(header, opened, content, listName, hierarchyIndex, sectionID):
    tempData['sectionsOpen'][f'{header}'] = opened
    for i in data:
        if i[0] == listName:
            ListIndex = str(data.index(i)).zfill(2)
            hierarchyIndex = str(hierarchyIndex).zfill(2)
            sectionID = str(sectionID).zfill(2)
            elementIndexes = f"{ListIndex} {hierarchyIndex} {sectionID}"

            sectionArrowKey = f'{elementIndexes} SECTION ARROW {header}'
            sectionTextKey = f'{elementIndexes} SECTION TEXT {header}'
            sectionContentKey = f'{elementIndexes} SECTION CONTENT {header}'

            rightClickMenu = menus['Section 0 & 1']
            if hierarchyIndex == '01':
                rightClickMenu = menus['Section 2']

            if len(header) > 30:
                tooltip = header
            else:
                tooltip = None

            tempData['elementKeys'].append(f"{elementIndexes} SECTION {header}")
            return [[sg.T(symbol(opened), enable_events=True, k=sectionArrowKey, pad=((10, 0),(3,3))), sg.T(header, enable_events=True, k=sectionTextKey, right_click_menu=rightClickMenu, tooltip=tooltip)], [collapse(content, sectionContentKey, opened)]]

def createListLayout(theList):
    createdListLayout = []

    sectionID = 0

    for i in data:
        if i[0] is theList:
            contents = i
            for content in contents:
                if type(content) is dict:
                    for key, value in content.items():
                        createdListLayout.append(createTask(key, value, theList, 0, 0))

                if type(content) is list:
                    sectionID += 1

                    ID_of_section = sectionID

                    header = None
                    opened = None

                    for key, value in content[0].items():
                            header = key
                            opened = value

                    sectionContent = []

                    for contentInSection in content:
                        if type(contentInSection) is dict and content.index(contentInSection) != 0:
                            for key, value in contentInSection.items():
                                sectionContent.append(createTask(key, value, theList, 1, ID_of_section))

                        if type(contentInSection) is list:

                            sectionID += 1

                            subheader = None
                            subopened = None
                            
                            for key, value in contentInSection[0].items():
                                    subheader = key
                                    subopened = value

                            subsectionContent = []

                            for contentInSubSection in contentInSection:

                                if type(contentInSubSection) is dict and contentInSection.index(contentInSubSection) != 0:
                                    for key, value in contentInSubSection.items():
                                        subsectionContent.append(createTask(key, value, theList, 2, sectionID))

                            for i in createSection(subheader, subopened, subsectionContent, theList, 1, ID_of_section):
                                sectionContent.append(i)

                    for i in createSection(header, opened, sectionContent, theList, 0, 0):
                        createdListLayout.append(i)    
    return createdListLayout

def createRowOfColumns(listFocused):
    listsColumns = []
    for i in data:
        listLayout = createListLayout(i[0])
        listsColumns.append(sg.Column(layout=listLayout, visible=i[0] == listFocused, size=(300,390), key=f'COL{data.index(i)}', scrollable=True, vertical_scroll_only=True, pad=((0,5),(10,10))))
    
    editListsLayout = [
        [sg.Listbox(key='LISTS LISTBOX', values=tuple(tempData['combo']), size=(32,10), pad=(16,10), enable_events=True)],
        [sg.B('NONE', focus=True, visible=False)],
        [sg.B('Add', k='List::ADD(BUTTON)', size=(28,2), pad=(22, 8), border_width=0)],
        [sg.B('Rename', k='List::RENAME', size=(13, 2), pad=((22, 5), (0, 0)), border_width=0), sg.B('Delete', k='List::DELETE', size=(13, 2), border_width=0)],
        [sg.B('Move up', k='List::MOVEUP', size=(13, 2), pad=((22, 5), (6, 0)), border_width=0), sg.B('Move down', k='List::MOVEDOWN', size=(13, 2), pad=((5, 0), (6, 0)), border_width=0)],
        [sg.B('Undo', k='List::UNDO', size=(13, 2), pad=((22, 5), (8, 0)), border_width=0), sg.B('Redo', k='List::REDO', size=(13, 2), pad=((5, 0), (8, 0)), border_width=0)]
    ]

    frameLayout = [
        [sg.CB('', pad=((10, 0),(3,3))), sg.T('Colour                                   ', pad=(0,0))],
        [sg.T(symbol(True), pad=((10, 0),(3,3))), sg.T('Settings')], [collapse([[sg.CB('', pad=((10, 0),(3,3))), sg.T('Apply', pad=(0,0))]], None, True)]
    ]

    settingsLayout = [
        [sg.Text('Reset Daily at', pad=(6, 20)), sg.Input(default_text=programValues['TimeToResetDaily'], key='TimeToResetDaily', size=(18,1), pad=((31,5),(0,0)))],
        [sg.Text('Background Colour', pad=(6,0)), sg.Input(default_text=programValues['BGColour'], key='BGColour', size=(9,1), pad=((3,5),(0,0))), sg.ColorChooserButton('Colour...', target=(sg.ThisRow, -1), border_width=0)],
        [sg.Text('Button Colour', pad=(6,0)), sg.Input(default_text=programValues['BColour'], key='BColour', size=(9,1), pad=((34,5),(0,0))), sg.ColorChooserButton('Colour...', target=(sg.ThisRow, -1), border_width=0, pad=(5,5))],
        [sg.Text('Text Colour 1', pad=(6,0)), sg.Input(default_text=programValues['TColour1'], key='TColour1', size=(9,1), pad=((36,5),(0,0))), sg.ColorChooserButton('Colour...', target=(sg.ThisRow, -1), border_width=0, pad=(5,5))],
        [sg.Text('Text Colour 2', pad=(6,0)), sg.Input(default_text=programValues['TColour2'], key='TColour2', size=(9,1), pad=((36,5),(0,0))), sg.ColorChooserButton('Colour...', target=(sg.ThisRow, -1), border_width=0, pad=(5,5))],
        [sg.Frame('Result', frameLayout, pad=(25,50), title_color=programValues['TColour1'])]
    ]

    listsColumns.append(sg.Column(layout=editListsLayout, visible=True if programValues['List'] == 'LIST EDITOR' else False, size=(300,400), key=f'COL LIST EDITOR', scrollable=False, pad=((0,5),(10,10))))
    listsColumns.append(sg.Column(layout=settingsLayout, visible=True if programValues['List'] == 'SETTINGS' else False, size=(300,390), key=f'COL SETTINGS', scrollable=False, pad=((0,5),(10,10))))
    return(listsColumns)

def createLayout(listFocused):
    if listFocused is None:
        listFocused = programValues['List']

    if listFocused in ('LIST EDITOR', 'SETTINGS'):
        addButtonsVisible = False
        if listFocused == 'LIST EDITOR':
            comboDefaultValue = 'List Editor'
        else:
            comboDefaultValue = 'Settings'
    else:
        addButtonsVisible = True
        comboDefaultValue = tempData['combo'][tempData['combo'].index(programValues['List'] if programValues['List'] != 'LIST EDITOR' else tempData['combo'][0])]

    addButtonsCol = [
        [sg.pin(sg.Button('Add Task', size=(15,2), key='Task::ADD(BUTTON)', pad=((0,0),(2,0)), border_width=0)), sg.pin(sg.Button('Add Section', size=(15,2), key='Section::ADD(BUTTON)', pad=((18,0),(2,0)), border_width=0))]
    ]

    applyRevertButtonsCol = [
        [sg.B('Apply', size=(15,2), border_width=0, pad=((0,0),(2,0))), sg.B('Revert', size=(15, 2), border_width=0, pad=((18,0),(2,0)))]
    ]

    return [
            [sg.Menu(menus['Menu Bar'], key='-MENU BAR-')],
            [sg.Combo(tempData['combo'],default_value=comboDefaultValue , size=(100, 1), key='-COMBO-', readonly=True, enable_events=True)],
            createRowOfColumns(listFocused),
            [sg.Col(addButtonsCol, k='COL ADD BUTTONS', visible=addButtonsVisible), sg.Col(applyRevertButtonsCol, k='COL APPLY REVERT BUTTONS', visible=True if programValues['List'] == 'SETTINGS' else False)]
        ]
        
def updateData(elementType, name):
    for todoList in data:
            if todoList[0] == programValues['List']:
                for content in todoList:
                    if elementType == 'Section':
                        if type(content) is list:
                            if name in content[0]:
                                content[0][name] = tempData['sectionsOpen'][name]
                                return

                            for contentInSection in content:
                                if type(contentInSection) is list:
                                    if name in contentInSection[0]:
                                        contentInSection[0][name] = tempData['sectionsOpen'][name]
                                        return

                    if elementType == 'Task':
                        if type(content) is dict:
                            if name in content:
                                content[name] = not content[name]
                                return
                            
                        if type(content) is list:
                            for contentInSection in content:
                                if type(contentInSection) is dict:
                                    if name in contentInSection:
                                        contentInSection[name] = not contentInSection[name]
                                        return
                                if type(contentInSection) is list:
                                    for contentInSubSection in contentInSection:
                                        if name in contentInSubSection:
                                            contentInSubSection[name] = not contentInSubSection[name]
                                            return

def bindings():
    for i in tempData['elementKeys']:
        elementKey = i.split(' ')
        elementKey.insert(4, 'TEXT')
        window[' '.join(elementKey)].bind('<Button-3>', ' +RIGHT CLICK+')

    
    window['LISTS LISTBOX'].bind('<Double-Button-1>', ' +DOUBLE CLICK+')

def addElement(elementToAdd, sectionNameToAddTo, hierarchyIndex):
    print(elementToAdd)
    if elementToAdd is None:
        return
    for i in data:
        currentList = programValues['List']
        if i[0] == currentList:
            if hierarchyIndex == '00':
                i.append(elementToAdd)
                return createNewWindow()
            elif hierarchyIndex == '01':
                for content in i:
                    if type(content) is list and sectionNameToAddTo in content[0]:
                        content.append(elementToAdd)
                        return createNewWindow()
            elif hierarchyIndex == '02':
                for content in i:
                    if type(content) is list:
                        for contentInSection in content:
                            if type(contentInSection) is list and sectionNameToAddTo in contentInSection[0]:
                                if type(elementToAdd) is tuple:
                                    for task in elementToAdd:
                                        contentInSection.append(task)
                                else:
                                    contentInSection.append(elementToAdd)
                                return createNewWindow()

def insertElement(elementToInsert, elementNameOfInsertPos, hierarchyIndex, sectionID):
    if elementToInsert is None:
        return
    localSectionID = 0

    print(elementToInsert, elementNameOfInsertPos, hierarchyIndex, sectionID)

    for todolist in data:
        if todolist[0] == programValues['List']:
            for task in [task for task in todolist if type(task) is dict]:
                if elementNameOfInsertPos in task and hierarchyIndex == '00':
                    todolist.insert(todolist.index(task), elementToInsert)
                    return createNewWindow()
            for section in [section for section in todolist if type(section) is list]:
                if elementNameOfInsertPos in section[0] and hierarchyIndex == '00':
                    todolist.insert(todolist.index(section), elementToInsert)
                    return createNewWindow()
                localSectionID += 1
                for task in [task for task in section if type(task) is dict]:
                    if elementNameOfInsertPos in task and int(sectionID) == localSectionID:
                        section.insert(section.index(task), elementToInsert)
                        return createNewWindow()
                for subsection in [subsection for subsection in section if type(subsection) is list]:
                    if elementNameOfInsertPos in subsection[0] and int(sectionID) == localSectionID:
                        section.insert(section.index(subsection), elementToInsert)
                        return createNewWindow()
                else:
                    for subsection in [subsection for subsection in section if type(subsection) is list]:
                        localSectionID += 1
                        for task in [task for task in subsection if type(task) is dict]:
                            if elementNameOfInsertPos in task and int(sectionID) == localSectionID:
                                if type(elementToInsert) is tuple:
                                    for taskToInsert in elementToInsert:
                                        print(taskToInsert)
                                        subsection.insert(subsection.index(task), taskToInsert)
                                else:
                                    subsection.insert(subsection.index(task), elementToInsert)
                                return createNewWindow()

def renameElement(newName, elementType, hierarchyIndex, sectionID):
    
    localSectionID = 0

    for todolist in data:
        if todolist[0] == programValues['List']:
            for task in [task for task in todolist if type(task) is dict]:
                if elementType == 'Task' and  oldName in task and hierarchyIndex == '00':
                    task[newName] = task.pop(oldName)
                    return createNewWindow()
            for section in [section for section in todolist if type(section) is list]:
                if elementType == 'Section' and oldName in section[0] and hierarchyIndex == '00':
                    section[0][newName] = section[0].pop(oldName)
                    return createNewWindow()
                localSectionID += 1
                for task in [task for task in section if type(task) is dict]:
                    if elementType == 'Task' and  oldName in task and int(sectionID) == localSectionID:
                        task[newName] = task.pop(oldName)
                        return createNewWindow()
                for subsection in [subsection for subsection in section if type(subsection) is list]:
                    if elementType == 'Section' and oldName in subsection[0] and int(sectionID) == localSectionID:
                        subsection[0][newName] = subsection[0].pop(oldName)
                        return createNewWindow()
                else:
                    for subsection in [subsection for subsection in section if type(subsection) is list]:
                        localSectionID += 1
                        for task in [task for task in subsection if type(task) is dict]:
                            if elementType == 'Task' and oldName in task and int(sectionID) == localSectionID:
                                task[newName] = task.pop(oldName)
                                return createNewWindow()

def delElement(elementName, elementType, hierarchyIndex, sectionID):
    
    localSectionID = 0
    print(elementName, elementType, hierarchyIndex, sectionID)

    for todolist in data:
        if todolist[0] == programValues['List']:
            for task in [task for task in todolist if type(task) is dict]:
                if elementType == 'Task' and  elementName in task and hierarchyIndex == '00':
                    todolist.remove(task)
                    return createNewWindow()
            for section in [section for section in todolist if type(section) is list]:
                if elementType == 'Section' and elementName in section[0] and hierarchyIndex == '00':
                    todolist.remove(section)
                    return createNewWindow()
                localSectionID += 1
                for task in [task for task in section if type(task) is dict]:
                    if elementType == 'Task' and  elementName in task and int(sectionID) == localSectionID:
                        section.remove(task)
                        return createNewWindow()
                for subsection in [subsection for subsection in section if type(subsection) is list]:
                    if elementType == 'Section' and elementName in subsection[0] and int(sectionID) == localSectionID:
                        section.remove(subsection)
                        return createNewWindow()
                else:
                    for subsection in [subsection for subsection in section if type(subsection) is list]:
                        localSectionID += 1
                        for task in [task for task in subsection if type(task) is dict]:
                            if elementType == 'Task' and elementName in task and int(sectionID) == localSectionID:
                                subsection.remove(task)
                                return createNewWindow()
                

def renameList(listName, newListName):
    for i in data:
        if i[0] == listName:
            i[0] = newListName
            break
         
    for listNameInCombo in tempData['combo']:
        if listNameInCombo is listName:
            listNameInCombo = newListName
            break

    createCombo()

    window['-COMBO-'].update(values=tempData['combo'])
    window['LISTS LISTBOX'].update(values=tuple(tempData['combo']))

    print('donee')

def delList():
    if window[f'COL LIST EDITOR'].visible == True:
        theList = values['LISTS LISTBOX'][0]
    else:
        theList = programValues['List']
        
    for i in data:
        if i[0] == theList:
            data.remove(i)
            tempData['combo'].remove(theList)
            for listName in tempData['combo']:
                if listName is not theList:
                    if window[f'COL LIST EDITOR'].visible == True:
                        programValues['List'] = 'LIST EDITOR'
                    else:
                        programValues['List'] = listName
                    break
            return createNewWindow()

def copySection(elementName, hierarchyIndex, sectionID):
    localSectionID = 0
    for todolist in data:
        if todolist[0] == programValues['List']:
            for section in [section for section in todolist if type(section) is list]:
                if elementName in section[0] and hierarchyIndex == '00':
                    hierarchyLevels = 1
                    if len([x for x in section if type(x) is list]) != 0:
                        hierarchyLevels = 2
                    return(section, hierarchyLevels)
                localSectionID += 1
                for subsection in [subsection for subsection in section if type(subsection) is list]:
                    if elementName in subsection[0] and int(sectionID) == localSectionID:
                        return(subsection, 2)

def moveElement(elementToMove, hierarchyIndex, sectionID, direction):
    localSectionID = 0

    for todolist in data:
        if todolist[0] == programValues['List']:
            for task in [task for task in todolist if type(task) is dict]:
                if elementToMove in task and hierarchyIndex == '00':
                    if direction == 'Up':
                        a, b = todolist.index(task), todolist.index(task) - 1
                        if a == 1:
                            return
                    else:
                        a, b = todolist.index(task), todolist.index(task) + 1   
                        if len(todolist) == b:
                            return
                    todolist[b], todolist[a] = todolist[a], todolist[b]
                    return createNewWindow()
            for section in [section for section in todolist if type(section) is list]:
                if elementToMove in section[0] and hierarchyIndex == '00':
                    if direction == 'Up':
                        a, b = todolist.index(section), todolist.index(section) - 1
                        if a == 1:
                            return
                    else:
                        a, b = todolist.index(section), todolist.index(section) + 1   
                        if len(todolist) == b:
                            return
                    todolist[b], todolist[a] = todolist[a], todolist[b]
                    return createNewWindow()
                localSectionID += 1
                for task in [task for task in section if type(task) is dict]:
                    if elementToMove in task and int(sectionID) == localSectionID:
                        if direction == 'Up':
                            a, b = section.index(task), section.index(task) - 1
                            if a == 1:
                                return
                        else:
                            a, b = section.index(task), section.index(task) + 1   
                            if len(section) == b:
                                return
                        section[b], section[a] = section[a], section[b]
                        return createNewWindow()
                for subsection in [subsection for subsection in section if type(subsection) is list]:
                    if elementToMove in subsection[0] and int(sectionID) == localSectionID:
                        if direction == 'Up':
                            a, b = section.index(subsection), section.index(subsection) - 1
                            if a == 1:
                                return
                        else:
                            a, b = section.index(subsection), section.index(subsection) + 1   
                            if len(section) == b:
                                return
                        section[b], section[a] = section[a], section[b]
                        return createNewWindow()
                else:
                    for subsection in [subsection for subsection in section if type(subsection) is list]:
                        localSectionID += 1
                        for task in [task for task in subsection if type(task) is dict]:
                            if elementToMove in task and int(sectionID) == localSectionID:
                                if direction == 'Up':
                                    a, b = subsection.index(task), subsection.index(task) - 1
                                    if a == 1:
                                        return
                                else:
                                    a, b = subsection.index(task), subsection.index(task) + 1   
                                    if len(subsection) == b:
                                        return
                                subsection[b], subsection[a] = subsection[a], subsection[b]
                                return createNewWindow()

def checkElementExist(listIndex, hierarchyIndex, sectionID, elementType, elementName):
    return(f"{listIndex} {hierarchyIndex} {sectionID} {elementType.upper()} {elementName}" in tempData['elementKeys'])

def getTxt(msg):
    currentLoc = window.CurrentLocation()
    loc = (currentLoc[0] - 25, currentLoc[1] + 100)
    return sg.popup_get_text(msg, location=loc)

def applySettings():
    import re

    currentLoc = window.CurrentLocation()

    previousSettings = tempData['previousSettings']

    if re.match('^(2[0-3]|[01]{1}[0-9]):([0-5]{1}[0-9]):([0-5]{1}[0-9])$', values['TimeToResetDaily']):
        previousSettings['TimeToResetDaily'] = programValues['TimeToResetDaily']
        programValues['TimeToResetDaily'] = values['TimeToResetDaily']
    else:
        loc = (currentLoc[0] - 5, currentLoc[1] + 100)
        sg.popup('Please use correct format for time (HH:MM:SS)', title='Error', location=loc)
        return

    for colourString in (values['BGColour'], values['BColour'], values['TColour1'], values['TColour2']):
        if re.match('^#(?:[0-9a-fA-F]{3}){1,2}$', colourString):
            pass
        else:
            loc = (currentLoc[0] - 30, currentLoc[1] + 100)
            sg.popup(f'Please use correct format for colour (Hex). Wrong: {colourString}', location=loc, line_width=100)
            return

    previousSettings['BGColour'] = programValues['BGColour']
    previousSettings['BColour'] = programValues['BColour']
    previousSettings['TColour1'] = programValues['TColour1']
    previousSettings['TColour2'] = programValues['TColour2']

    programValues['BGColour'] = values['BGColour']
    programValues['BColour'] = values['BColour']
    programValues['TColour1'] = values['TColour1']
    programValues['TColour2'] = values['TColour2']
        

    colours()
    createNewWindow()

def revertSettings():
    previousSettings = tempData['previousSettings']

    programValues['BGColour'] = previousSettings['BGColour']
    programValues['BColour'] = previousSettings['BColour']
    programValues['TColour1'] = previousSettings['TColour1']
    programValues['TColour2'] = previousSettings['TColour2']

    colours()
    createNewWindow()

def startup():
    readDataFile()

    # Check whether to reset the daily section
    whenToReset = f"{datetime.now().strftime(r'%d/%m/%Y')} {programValues['TimeToResetDaily']}"
    dateTimeNow = datetime.now().strftime(r'%d/%m/%Y %H:%M:%S')

    if tempData['WhenLastClosed'] < whenToReset:
        if dateTimeNow > whenToReset:
            resetDaily()

    # Sets the list index
    for i in data:
        if i[0] == programValues['List']:
            tempData['ListIndex'] = str(data.index(i)).zfill(2)
            break

    colours()
    createCombo()
    
startup()

window = sg.Window('TODOlist', layout=createLayout(None), size=(300,500), finalize=True, icon='icon.ico')
bindings()


def createNewWindow():
    tempData['elementKeys'].clear()
    global window
    window1 = sg.Window('TODOlist', layout=createLayout(None), location=window.CurrentLocation(), size=(300,500), finalize=True, icon='icon.ico')
    window.Close()
    window = window1
    bindings()



















#  /$$$$$$$$                                  /$$           /$$                                    
# | $$_____/                                 | $$          | $$                                    
# | $$       /$$    /$$  /$$$$$$  /$$$$$$$  /$$$$$$        | $$        /$$$$$$   /$$$$$$   /$$$$$$ 
# | $$$$$   |  $$  /$$/ /$$__  $$| $$__  $$|_  $$_/        | $$       /$$__  $$ /$$__  $$ /$$__  $$
# | $$__/    \  $$/$$/ | $$$$$$$$| $$  \ $$  | $$          | $$      | $$  \ $$| $$  \ $$| $$  \ $$
# | $$        \  $$$/  | $$_____/| $$  | $$  | $$ /$$      | $$      | $$  | $$| $$  | $$| $$  | $$
# | $$$$$$$$   \  $/   |  $$$$$$$| $$  | $$  |  $$$$/      | $$$$$$$$|  $$$$$$/|  $$$$$$/| $$$$$$$/
# |________/    \_/     \_______/|__/  |__/   \___/        |________/ \______/  \______/ | $$____/ 
#                                                                                        | $$      
#                                                                                        | $$      
#                                                                                        |__/      
  
while True:             
    event, values = window.read()
    print(event)

    if event == sg.WIN_CLOSED:
        tempData['WhenLastClosed'] = datetime.now().strftime(r'%d/%m/%Y %H:%M:%S')
        if programValues['List'] in ('LIST EDITOR', 'SETTINGS'):
            programValues['List'] = tempData['lastListOn']
        #writeDataFile()
        break

    # Add a to do list
    if 'List::ADD' in event:
        listName = getTxt('List Name:')

        if listName is not None and listName not in tempData['combo']:
            data.append([listName])
            if 'MENU' in event:
                programValues['List'] = listName
            createCombo()
            tempData['ListIndex'] = str(tempData['combo'].index(listName)).zfill(2)
            createNewWindow()
        elif listName in tempData['combo']:
            currentLoc = window.CurrentLocation()
            loc = (currentLoc[0] + 80, currentLoc[1] + 100)
            sg.popup('List already exists', title='Error', location=loc)

    # Change which list your on
    if event == '-COMBO-':
        programValues['List'] = values['-COMBO-']
        tempData['ListIndex'] = str(tempData['combo'].index(values['-COMBO-'])).zfill(2)
        for i in data:
            if i[0] == programValues['List']:
                window[f'COL{data.index(i)}'].update(visible=True)
            else:
                window[f'COL{data.index(i)}'].update(visible=False)

        for i in ['LIST EDITOR', 'SETTINGS']:
            if window[f'COL {i}'].visible == True:
                print(i)
                window[f'COL {i}'].update(visible=False)

                window['COL APPLY REVERT BUTTONS'].update(visible=False)

                window['-MENU BAR-'].update(menu_definition=menus['Menu Bar'])

        window['COL ADD BUTTONS'].update(visible=True)
        window['COL ADD BUTTONS'].unhide_row()


    # Appending or Inserting an element
    if any(x in event for x in ('ADD', 'INSERT')) and 'List' not in event:

        sectionNameToAddTo = None
        hierarchyIndex = '00'
        sectionID = '00'

        if 'ADD' in event:
            if 'BUTTON' in event:
                elementType = event[:-13]
            else:
                elementType = event[:-5]
        else:
            elementType = event[:-8]
            sectionID = tempData['latestElementRightClicked'][6:8]

        if 'ADDTO' in event:
            sectionNameToAddTo = tempData['latestElementRightClicked'][22:]
            hierarchyIndex = tempData['latestElementRightClicked'][3:5]
            hierarchyIndex = str((int(hierarchyIndex) + 1)).zfill(2)
            sectionID = str((int(tempData['latestElementRightClicked'][6:8]) + 1)).zfill(2)
            elementType = event[:-7]

        if 'Paste' in event and tempData['elementCopied'][1] is not None:
            elementType = 'Task' if type(tempData['elementCopied'][1]) is bool else 'Section'
            if elementType == 'Task':
                elementName = tempData['elementCopied'][0][19:]
            else:
                elementName = list(tempData['elementCopied'][0][0].keys())[0]

            if elementType[0] == 'T':
                elementToAdd = {elementName: tempData['elementCopied'][1]}
            else:
                if int(hierarchyIndex) == 2:
                    currentLoc = window.CurrentLocation()
                    sg.popup('Cannot support more subsections\nPasting tasks within copied section...', title='Error', location=(currentLoc[0] + 25, currentLoc[1] + 100))
                    elementToAdd = tuple(x for x in tempData['elementCopied'][0][1:] if type(x) is dict)
                elif int(hierarchyIndex) > 0 and tempData['elementCopied'][1] == 2:
                    elementToAdd = [x for x in tempData['elementCopied'][0] if type(x) is dict]
                    currentLoc = window.CurrentLocation()
                    sg.popup('Cannot support more subsections\nPasting without subsections...', title='Error', location=(currentLoc[0] + 30, currentLoc[1] + 100))
                else:
                    elementToAdd = tempData['elementCopied'][0]
        elif 'Paste' not in event:
            elementName = getTxt(f'{elementType} Name:')
            if elementType[0] == 'T':
                elementToAdd = {elementName: False}
            else:
                elementToAdd = [{elementName: False}]
        else:
            elementName = None
            elementToAdd = None

        if checkElementExist(tempData['ListIndex'], hierarchyIndex, sectionID, elementType, elementName) == False:
            if elementName not in ('', None):
                if 'ADD' in event:
                    addElement(elementToAdd, sectionNameToAddTo, hierarchyIndex)
                else:
                    if tempData['latestElementRightClicked'][9:10] == 'T':
                        elementNameOfInsertPos = tempData['latestElementRightClicked'][19:]
                    else:
                        elementNameOfInsertPos = tempData['latestElementRightClicked'][22:]
                    
                    insertElement(elementToAdd, elementNameOfInsertPos, hierarchyIndex, sectionID)
        else:
            currentLoc = window.CurrentLocation()
            sg.popup(f'Element already exists within current area/ section', title='Error', location=(currentLoc[0] - 14, currentLoc[1] + 100))

    # Opening and closing sections
    if 'SECTION' in event and not any(x in event for x in ('RIGHT CLICK', 'Copy', 'Cut')):
        elementIndexes = event[:8]

        if 'ARROW' in event:
            eventName = event[23:]
        else:
            eventName = event[22:]

        tempData['sectionsOpen'][eventName] = not tempData['sectionsOpen'][eventName]
        window[f"{elementIndexes} SECTION ARROW {eventName}"].update(SYMBOL_DOWN if tempData['sectionsOpen'][eventName] else SYMBOL_RIGHT)
        window[f"{elementIndexes} SECTION CONTENT {eventName}"].update(visible=tempData['sectionsOpen'][eventName]) 
        updateData('Section', eventName)


    # Updating the checkbox
    if 'TASK' in event and 'RIGHT CLICK' not in event:

        if 'TEXT' in event:
            eventName = event[19:]
            elementKey = event.split(' ')
            elementKey.remove('TEXT')
            elementKey.insert(4, 'CHECKBOX')
            elementKey = ' '.join(elementKey)
            checked =  window[elementKey].Get()
            window[elementKey].Update(value=not checked)
        else:
            eventName = event[23:]
            
        updateData('Task', eventName)
    
    # Checking what element the user right clicked
    if '+RIGHT CLICK+' in event:
        elementKey = event[:-14]

        if elementKey is not tempData['latestElementRightClicked']:
            tempData['latestElementRightClicked'] = elementKey
            #print(f"Element right clicked was: {elementKey}")

        event = window[elementKey].user_bind_event
        window[elementKey]._RightClickMenuCallback(event)
        event = elementKey

    # Move up or down
    if 'MOVE' in event:
        elementKey = tempData['latestElementRightClicked']
        elementKey = elementKey.split(' ')

        elementToMove = ' '.join(elementKey[5:])
        hierarchyIndex = elementKey[1]
        sectionID = elementKey[2]

        direction = event[:-6]

        print(direction)
        moveElement(elementToMove, hierarchyIndex, sectionID, direction)

    # Copy
    if 'Copy' in event:
        elementKey = tempData['latestElementRightClicked']

        if 'TASK' in event:
            elementKey = elementKey.split(' ')
            elementKey.remove('TEXT')    
            elementKey.insert(4, 'CHECKBOX')
            elementKey = ' '.join(elementKey)
            tempData['elementCopied'] = (tempData['latestElementRightClicked'], values[elementKey])
        else:   # A Section
            elementName = elementKey[22:]
            hierarchyIndex = tempData['latestElementRightClicked'][3:5]
            sectionID = tempData['latestElementRightClicked'][6:8]
            tempData['elementCopied'] = copySection(elementName, hierarchyIndex, sectionID)

    # Cut
    if 'Cut' in event:
        elementKey = tempData['latestElementRightClicked']

        elementKey = elementKey.split(' ')

        elementName = ' '.join(elementKey[5:])
        elementType = elementKey[3].title()
        hierarchyIndex = elementKey[1]
        sectionID = elementKey[2]

        if 'TASK' in event:
            elementKey.remove('TEXT')
            elementKey.insert(4, 'CHECKBOX')
            elementKey = ' '.join(elementKey)
            tempData['elementCopied'] = (tempData['latestElementRightClicked'], values[elementKey])

            delElement(elementName, elementType, hierarchyIndex, sectionID)
        else:   # A Section
            tempData['elementCopied'] = copySection(elementName, hierarchyIndex, sectionID)
            delElement(elementName, elementType, hierarchyIndex, sectionID)

    # Rename
    if event == 'Rename':
        element = tempData['latestElementRightClicked']
        newName = getTxt('Rename to:')

        hierarchyIndex = element[3:5]
        sectionID = element[6:8]

        if 'TASK' in element:
            elementType = 'Task'
            oldName = element[19:]
        else:
            elementType = 'Section'
            oldName = element[22:]

        if checkElementExist(tempData['ListIndex'], hierarchyIndex, sectionID, elementType, newName) == False:
            if newName not in ('', None):
                renameElement(newName, elementType, hierarchyIndex, sectionID)
        else:
            currentLoc = window.CurrentLocation()
            sg.popup(f'Element already exists within current area/ section', title='Error', location=(currentLoc[0] - 14, currentLoc[1] + 100))

    # Delete Element
    if event == 'Delete':
        element = tempData['latestElementRightClicked']
        if 'TASK' in element:
            elementName = element[19:]
            elementType = 'Task'
        else:
            elementName = element[22:]
            elementType = 'Section'

        hierarchyIndex = element[3:5]
        sectionID = element[6:8]

        delElement(elementName, elementType, hierarchyIndex, sectionID)

    
    # Rename List
    if event == 'List::RENAME' and len(values['LISTS LISTBOX']) != 0:
        listNameToRename = values['LISTS LISTBOX'][0]
        newListName = getTxt('Rename to:')
        renameList(listNameToRename, newListName)
    elif event == 'List:RENAME' and len(values['LISTS LISTBOX']) == 0:
        currentLoc = window.CurrentLocation()
        loc = (currentLoc[0] + 80, currentLoc[1] + 100)
        sg.popup('Select a list first', title='Error', location=loc)

    # Delete List
    if event == 'List::DELETE':
        currentLoc = window.CurrentLocation()
        loc = (currentLoc[0] + 4, currentLoc[1] + 100)
        if sg.popup_ok_cancel("This will delete the list and all of it's contents", title='Delete?', location=loc) == 'OK':
            delList()

    # Show LIST EDITOR Page
    if event == 'Lists':
        tempData['lastListOn'] = programValues['List']

        for i in tempData['combo']:
            if i == programValues['List']:
                window[f"COL{tempData['combo'].index(i)}"].update(visible=False)
                break
        
        if window['COL SETTINGS'].visible == True:
            window['COL SETTINGS'].update(visible=False)

        window['-MENU BAR-'].Update(menu_definition=menus['Disabled Menu Bar'])

        programValues['List'] = 'LIST EDITOR'
        window['COL LIST EDITOR'].update(visible=True)
        window['COL ADD BUTTONS'].hide_row()
        window['-COMBO-'].update(value='List Editor')

    if event == 'LISTS LISTBOX +DOUBLE CLICK+':
        programValues['List'] = values['LISTS LISTBOX'][0]
        tempData['ListIndex'] = str(tempData['combo'].index(programValues['List'])).zfill(2)
        for i in data:
            if i[0] == programValues['List']:
                window[f'COL{data.index(i)}'].update(visible=True)
            else:
                window[f'COL{data.index(i)}'].update(visible=False)

        window['COL LIST EDITOR'].update(visible=False)
        window['COL ADD BUTTONS'].update(visible=True)
        window['COL ADD BUTTONS'].unhide_row()
        window['-MENU BAR-'].update(menu_definition=menus['Menu Bar'])
        window['-COMBO-'].update(value=programValues['List'])

    # Move a list up or down
    if 'List::MOVE' in event:
        combo = tempData['combo']
        listName = ''

        if values['LISTS LISTBOX'] != []:
            listName = values['LISTS LISTBOX'][0]
        elif values['LISTS LISTBOX'] == [] and tempData['listSelectedToEdit'] != '':
            listName = tempData['listSelectedToEdit']
        else:
            currentLoc = window.CurrentLocation()
            loc = (currentLoc[0] + 80, currentLoc[1] + 100)
            sg.popup('Select a list first', title='Error', location=loc)

        for i in data:
            if i[0] is listName:
                theList = i

                index = data.index(theList)
                data.remove(theList)

                if 'UP' in event:
                    data.insert(index - 1, theList)
                elif 'DOWN' in event:
                    data.insert(index + 1, theList)
                createCombo()
                break

        tempData['listSelectedToEdit'] = listName

        window['-COMBO-'].update(values=tempData['combo'])
        window['LISTS LISTBOX'].update(values=tuple(tempData['combo']))

    # Settings Page
    if event == 'Settings':
        tempData['lastListOn'] = programValues['List']

        for i in tempData['combo']:
            if i == programValues['List']:
                window[f"COL{tempData['combo'].index(i)}"].update(visible=False)
                break

        if window['COL LIST EDITOR'].visible == True:
            window['COL LIST EDITOR'].update(visible=False)

        window['-MENU BAR-'].Update(menu_definition=menus['Disabled Menu Bar'])

        programValues['List'] = 'SETTINGS'
        window['COL SETTINGS'].update(visible=True)
        window['COL APPLY REVERT BUTTONS'].update(visible=True)
        window['COL APPLY REVERT BUTTONS'].unhide_row()
        window['COL ADD BUTTONS'].update(visible=False)
        window['-COMBO-'].update(value='Settings')
    
    # Applying or Reverting Settings
    if event == 'Apply':
        applySettings()
    elif event == 'Revert':
        revertSettings()
    

window.close()
