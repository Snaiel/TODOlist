import PySimpleGUI as sg

SYMBOL_RIGHT ='►'
SYMBOL_DOWN =  '▼'

menus = {
        'Menu Bar': ['Add', ['Task::ADD', 'Section::ADD'],['Lists', ['Modify']]],
        'Task 0 & 1': ['Right', ['Insert', ['Task::INSERT', 'Section::INSERT'], 'Rename', 'Delete']],
        'Section 0 & 1': ['&Right', ['&Add', ['Task::ADDTO', 'Section::ADDTO'], '&Insert', ['Task::INSERT', 'Section::INSERT'], 'Rename', 'Delete']],
        'Task 2': ['Right', ['Insert', ['Task'], 'Rename', 'Delete']],
        'Section 2': ['&Right', ['&Add', ['Task::ADDTO'], '&Insert', ['Task::INSERT', 'Section::INSERT'], 'Rename', 'Delete']]
        }

programValues = {
                'List': 'Project 1',
                'ListIndex': '01', 
                'latestElementRightClicked': ''
                }

tempData = {
            'elementKeys': [],
            'sectionsOpen': {},
            'combo': [],
            'latestElementRightClicked': ''
            }
SectionsOpen = {}

# data is pretty much everything from the to do lists, sections and tasks
# it is a list of lists that shows each To do list
# The first element of the to do lists is the name of the to do list
# Dictionaries are checkboxes that say whether they are ticked or not.
# lists are sections that contain dicitonaries
# The first dictionary under in a list is the name of the section and whether it is closed or not

data = [
    ['Today', [{'Daily': True}, {'Cry': False, 'Protein shake': True}], {'Methods homework': False}, {'Physics': True}, [{'Section 1': True}, {'Learn python': False}, {'Buy Furniture': True}], [{'Section 2': False}, {'Workout': False}]],
    ['Project 1', {'Sell stocks': False}, [{'Section 3': False}, {'Lift weights': False}], [{'Tessubcontent': True}, {'Cook': False}, [{'Work': False}, {'Fix bug': False}, {'Play ping pong': True}], {'Feed dog': True}, {'Train dragon': False}]]
]

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
    combo = tempData['combo']
    for i in data:
        combo.append(i[0])
    combo.append('                         Add List')

def createTask(name, checked, listName, hierarchyIndex):
    for i in data:
        if i[0] == listName:
            ListIndex = str(data.index(i)).zfill(2)
            hierarchyIndex = str(hierarchyIndex).zfill(2)
            elementIndexes = f"{ListIndex} {hierarchyIndex}"

            checkBoxKey = f"{elementIndexes} TASK CHECKBOX {name}"
            checkBoxTextKey = f"{elementIndexes} TASK TEXT {name}"

            rightClickMenu = menus['Task 0 & 1']
            if hierarchyIndex == '02':
                rightClickMenu = menus['Task 2']

            tempData['elementKeys'].append(f"{elementIndexes} TASK {name}")
            return [sg.Checkbox('', default=checked, enable_events=True, key=checkBoxKey, pad=((10, 0),(3,3))), sg.T(name, right_click_menu=rightClickMenu, pad=(0,0), key=checkBoxTextKey, enable_events=True)]

def createSection(header, opened, content, listName, hierarchyIndex):
    SectionsOpen[f'{header}'] = opened
    for i in data:
        if i[0] == listName:
            ListIndex = str(data.index(i)).zfill(2)
            hierarchyIndex = str(hierarchyIndex).zfill(2)
            elementIndexes = f"{ListIndex} {hierarchyIndex}"

            sectionArrowKey = f'{elementIndexes} SECTION ARROW {header}'
            sectionTextKey = f'{elementIndexes} SECTION TEXT {header}'
            sectionContentKey = f'{elementIndexes} SECTION CONTENT {header}'

            rightClickMenu = menus['Section 0 & 1']
            if hierarchyIndex == '01':
                rightClickMenu = menus['Section 2']

            tempData['elementKeys'].append(f"{elementIndexes} SECTION {header}")
            return [[sg.T(symbol(opened), enable_events=True, k=sectionArrowKey, pad=((10, 0),(3,3))), sg.T(header, enable_events=True, k=sectionTextKey, right_click_menu=rightClickMenu)], [collapse(content, sectionContentKey, opened)]]

def createListLayout(theList):
    createdListLayout = []
    for i in data:
        if i[0] is theList:
            contents = i
            for content in contents:
                if type(content) is dict:
                    for key, value in content.items():
                        createdListLayout.append(createTask(key, value, theList, 0))

                if type(content) is list:
                    for key, value in content[0].items():
                            header = key
                            opened = value

                    sectionContent = []

                    for contentInSection in content:
                        if type(contentInSection) is dict and content.index(contentInSection) != 0:
                            for key, value in contentInSection.items():
                                sectionContent.append(createTask(key, value, theList, 1))

                        if type(contentInSection) is list:
                            for key, value in contentInSection[0].items():
                                    subheader = key
                                    subopened = value

                            subsectionContent = []

                            for contentInSubSection in contentInSection:

                                if type(contentInSubSection) is dict and contentInSection.index(contentInSubSection) != 0:
                                    for key, value in contentInSubSection.items():
                                        subsectionContent.append(createTask(key, value, theList, 2))

                            for i in createSection(subheader, subopened, subsectionContent, theList, 1):
                                sectionContent.append(i)

                    for i in createSection(header, opened, sectionContent, theList, 0):
                        createdListLayout.append(i)    
    return createdListLayout

def createRowOfColumns(listFocused):
    listsColumns = []
    for i in data:
        listLayout = createListLayout(i[0])
        listsColumns.append(sg.Column(layout=listLayout, visible=i[0] == listFocused, size=(300,400), key=f'COL{data.index(i)}', scrollable=True, vertical_scroll_only=True, pad=((0,5),(10,10))))
    return(listsColumns)

def createLayout(listFocused):
    if listFocused is None:
        listFocused = programValues['List']
    return [
            [sg.Menu(menus['Menu Bar'])],
            [sg.Combo(tempData['combo'],default_value=tempData['combo'][tempData['combo'].index(programValues['List'])] , size=(100, 1), key='-COMBO-', readonly=True, enable_events=True)],
            createRowOfColumns(listFocused),
            [sg.Button('Add Task', image_size=(125,40), key='Task::ADD(BUTTON)', pad=((5,0),(0,10)), image_filename='white.png', border_width=0, button_color=('black', 'black')), sg.Button('Add Section', image_size=(125,40), key='Section::ADD(BUTTON)', pad=((16,0),(0,10)), image_filename='white.png', border_width=0, button_color=('black', 'black'))]
            ]

def addElement(elementType, name, sectionNameToAddTo, hierarchyIndex):

    done = False

    if name == '' or name is None:
        return 'Nevermind'

    if elementType == 'Task':
        elementToAdd = {name: False}
    elif elementType == 'Section':
        elementToAdd = [{name: False}]

    for i in data:
        currentList = programValues['List']
        if i[0] == currentList:
            if hierarchyIndex == '00':
                i.append(elementToAdd)
                done = True
            elif hierarchyIndex == '01':
                for content in i:
                    if type(content) is list and sectionNameToAddTo in content[0]:
                        content.append(elementToAdd)
                        done = True
                        break
            elif hierarchyIndex == '02':
                for content in i:
                    if type(content) is list:
                        for contentInSection in content:
                            if type(contentInSection) is list and sectionNameToAddTo in contentInSection[0]:
                                contentInSection.append(elementToAdd)
                                done = True
                                break
        if done is True:
            break

    createNewWindow()

def updateData(elementType, name):
    for todoList in data:
            if todoList[0] == programValues['List']:
                for content in todoList:
                    if elementType == 'Section':
                        if type(content) is list:
                            if name in content[0]:
                                content[0][name] = SectionsOpen[name]
                                break

                            for contentInSection in content:
                                if type(contentInSection) is list:
                                    if name in contentInSection[0]:
                                        contentInSection[0][name] = SectionsOpen[name]
                                        break

                    if elementType == 'Task':
                        if type(content) is dict:
                            if name in content:
                                content[name] = not content[name]
                                break
                            
                        if type(content) is list:
                            for contentInSection in content:
                                if type(contentInSection) is dict:
                                    if name in contentInSection:
                                        contentInSection[name] = not contentInSection[name]
                                        break
                                if type(contentInSection) is list:
                                    for contentInSubSection in contentInSection:
                                        if name in contentInSubSection:
                                            contentInSubSection[name] = not contentInSubSection[name]

def bindRightClick():
    for i in tempData['elementKeys']:
        elementKey = i.split(' ')
        elementKey.insert(3, 'TEXT')
        window[' '.join(elementKey)].bind('<Button-3>', ' +RIGHT CLICK+')

def renameElement(oldKey, newName):
    if 'TASK' in oldKey:
        oldName = oldKey[16:]
    else:
        oldName = oldKey[19:]

    for i in data:
        if i[0] == programValues['List']:
            for content in i:
                if type(content) is dict and oldName in content:
                    content[newName] = content.pop(oldName)
                    break
                elif type(content) is list:
                    for contentInSection in content:
                        if type(contentInSection) is dict and oldName in contentInSection:
                            contentInSection[newName] = contentInSection.pop(oldName)
                            break
                        elif type(contentInSection) is list:
                            for contentInSubSection in contentInSection:
                                if type(contentInSubSection) is dict and oldName in contentInSubSection:
                                    contentInSubSection[newName] = contentInSubSection.pop(oldName)
                                    break

    tempData['elementKeys'].clear()
    elementKeys = tempData['elementKeys']
    createNewWindow()
    for i in elementKeys:
        if oldKey in i:
            elementKeys.remove(i)
            break

def delElement(elementKey):
    if 'TASK' in elementKey:
        elementName = elementKey[16:]
    else:
        elementName = elementKey[19:]

    print(elementName)

    for i in data:
        if i[0] == programValues['List']:
            for content in i:
                if type(content) is dict and elementName in content:
                    i.remove(content)
                    break
                elif type(content) is list:
                    for contentInSection in content:
                        if type(contentInSection) is dict and content.index(contentInSection) == 0 and elementName in contentInSection:
                            i.remove(content)
                            break
                        elif type(contentInSection) is list:
                            for contentInSubSection in contentInSection:
                                if contentInSection.index(contentInSubSection) == 0 and elementName in contentInSubSection:
                                    content.remove(contentInSection)
                                    break
                                elif elementName in contentInSubSection:
                                    contentInSection.remove(contentInSubSection)
                                    break
                        elif type(contentInSection) is dict and elementName in contentInSection:
                            content.remove(contentInSection)
                            break

    tempData['elementKeys'].clear()
    elementKeys = tempData['elementKeys']
    createNewWindow()
    for i in elementKeys:
        if elementKey is i:
            elementKeys.remove(i)
            break

def getTxt(msg):
    currentLoc = window.CurrentLocation()
    loc = (currentLoc[0] - 25, currentLoc[1] + 100)
    return sg.popup_get_text(msg, location=loc)

createCombo()

window = sg.Window('TODOlist', layout=createLayout(None), size=(300,500), finalize=True, right_click_menu_background_color=None)
print(tempData['elementKeys'])
#print(SectionsOpen)

def createNewWindow():
    global window
    window1 = sg.Window('TODOlist', layout=createLayout(None), location=window.CurrentLocation(), size=(300,500), finalize=True)
    window.Close()
    window = window1
    bindRightClick()

bindRightClick()

while True:             # Event Loop
    event, values = window.read()
    print(event)

    if event == sg.WIN_CLOSED or event == 'Exit':
        break

    if values['-COMBO-'] == '                         Add List':  # Add a to do list
        currentLoc = window.CurrentLocation()
        loc = (currentLoc[0] - 25, currentLoc[1] + 100)
        text = sg.popup_get_text('List Name', location=loc)

    if event == '-COMBO-':  # Change which list your on
        programValues['List'] = values['-COMBO-']
        programValues['ListIndex'] = str(tempData['combo'].index(values['-COMBO-'])).zfill(2)
        for i in data:
            if i[0] == programValues['List']:
                window[f'COL{data.index(i)}'].update(visible=True)
            else:
                window[f'COL{data.index(i)}'].update(visible=False)


                    # ADDING A TASK OR SECTION
    if '::ADD' in event:

        sectionNameToAddTo = None
        hierarchyIndex = '00'
        if 'BUTTON' in event:
            elementType = event[:-13]
        else:
            elementType = event[:-5]

        if 'ADDTO' in event:
            sectionNameToAddTo = programValues['latestElementRightClicked'][19:]
            hierarchyIndex = programValues['latestElementRightClicked'][3:5]
            hierarchyIndex = (str((int(hierarchyIndex) + 1)).zfill(2))
            elementType = event[:-7]

        elementName = getTxt(f'{elementType} Name:')

        if f"{programValues['ListIndex']} {hierarchyIndex} {elementType.upper()} {elementName}" in tempData['elementKeys']:
            currentLoc = window.CurrentLocation()
            sg.popup(f'{elementType} already exists', location=(currentLoc[0] + 70, currentLoc[1] + 100))
        else:
            addElement(elementType, elementName, sectionNameToAddTo, hierarchyIndex)
                

    # Opening and closing sections
    if 'SECTION' in event and 'RIGHT CLICK' not in event:
        elementIndexes = event[:5]

        if 'ARROW' in event:
            eventName = event[20:]
        else:
            eventName = event[19:]

        SectionsOpen[eventName] = not SectionsOpen[eventName]
        window[f"{elementIndexes} SECTION ARROW {eventName}"].update(SYMBOL_DOWN if SectionsOpen[eventName] else SYMBOL_RIGHT)
        window[f"{elementIndexes} SECTION CONTENT {eventName}"].update(visible=SectionsOpen[eventName]) 
        updateData('Section', eventName)


    # Updating the checkbox
    if 'TASK' in event and 'RIGHT CLICK' not in event:

        if 'TEXT' in event:
            eventName = event[16:]
            elementKey = event.split(' ')
            elementKey.remove('TEXT')
            elementKey.insert(3, 'CHECKBOX')
            elementKey = ' '.join(elementKey)
            checked =  window[elementKey].Get()
            window[elementKey].Update(value=not checked)
        else:
            eventName = event[20:]

        updateData('Task', eventName)


                                                    # Right Click Stuff
    # Checking what element the mouse is hovering over
    if '+RIGHT CLICK+' in event:
        elementKey = event[:-14]

        if elementKey is not programValues['latestElementRightClicked']:
            programValues['latestElementRightClicked'] = elementKey
            print(f"Element right clicked was: {elementKey}")

        event = window[elementKey].user_bind_event
        window[elementKey]._RightClickMenuCallback(event)

    
    # Right click functionality
    if event == 'Rename':
        elementKey = programValues['latestElementRightClicked']
        newName = getTxt('Rename to:')
        if newName is not None:
            renameElement(elementKey, newName)

    if event == 'Delete':
        #print(programValues['latestElementRightClicked'])
        delElement(programValues['latestElementRightClicked'])


window.close()
