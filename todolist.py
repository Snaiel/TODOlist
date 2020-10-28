import PySimpleGUI as sg

# test thing yknow

SYMBOL_RIGHT ='►'
SYMBOL_DOWN =  '▼'


opened1, opened2 = True, False

menu = [['Add', ['Task', 'Section']],      
        ['Lists', ['View', 'Add']
     ]]

section_right_click = ['&Right', [['&Add', ['Task', 'Section', ]], 'Rename', 'Delete']]
task_right_click = ['&Right', [['&Rename', 'Delete']]]

programValues = {'List': 'Daily'}

elementKeys = []

SectionsOpen = {}


# data is pretty much everything from the to do lists, sections and tasks
# it is a list of lists that shows each To do list
# The first element of the to do lists is the name of the to do list
# Dictionaries are checkboxes that say whether they are ticked or not.
# lists are sections that contain dicitonaries
# The first dictionary under in a list is the name of the section and whether it is closed or not

data = [
    ['Daily', {'Methods homework': False, 'Physics': True}, [{'Section 1': True}, {'Learn python': False, 'Buy Furniture': True}], [{'Section 2': False}, {'Workout': False}]],
    ['Project 1', {'Workout': False}]
]

def collapse(layout, key, isVisible):
    """
    Helper function that creates a Column that can be later made hidden, thus appearing "collapsed"
    :param layout: The layout for the section
    :param key: Key used to make this seciton visible / invisible
    :return: A pinned column that can be placed directly into your layout
    :rtype: sg.pin
    """
    return sg.pin(sg.Column(layout, key=key, visible=isVisible))

def symbol(opened):
    if opened is True:
        return SYMBOL_DOWN
    else:
        return SYMBOL_RIGHT




combo = []

def createCombo():
    for i in data:
        combo.append(i[0])
    combo.append('                         Add List')
    #print(combo)

def createCheckBox(name, checked):
    return [sg.Checkbox(name, default=checked)]

def createSection(header, opened, content):
    listLayout.append([sg.T(symbol(opened), enable_events=True, k=f'{header} ARROW'), sg.T(header, enable_events=True, k=f'{header}', right_click_menu=section_right_click)])
    listLayout.append([collapse(content, f'{header} CONTENT', opened)])
    elementKeys.append(f'{header}')
    SectionsOpen[f'{header}'] = opened



def createListLayout(theList):
    for i in data:
        if i[0] is theList:
            contents = i
            for content in contents:
                if type(content) is dict:
                    for key, value in content.items():
                        listLayout.append(createCheckBox(key, value))

                if type(content) is list:
                    for key, value in content[0].items():
                            header = key
                            opened = value

                    for contentInSection in content:
                        sectionContent = []

                        if type(contentInSection) is dict and content.index(contentInSection) != 0:
                            for key, value in contentInSection.items():
                                sectionContent.append(createCheckBox(key, value))

                    #print(sectionContent)
                    createSection(header, opened, sectionContent)
                    #print(listLayout)
                    #print(dw)
                    



section1 =  [
                [sg.Checkbox('Learn python')],
                [sg.Checkbox('Buy Furniture')]
            ]

section2 = [[sg.Checkbox('Workout')]
            ]

# The layout that has all the sections and tasks
listLayout = []

# REFERENCE LAYOUT
dw = [
            [sg.Checkbox('Methods homework')],
            #### Section 1 part ####
            [sg.T(symbol(opened1), enable_events=True, k='-OPEN SEC1-'), sg.T('Section 1', enable_events=True, k='-OPEN SEC1-TEXT', right_click_menu=section_right_click)],
            [collapse(section1, '-SEC1-', opened1)],
            #### Section 2 part ####
            [sg.T(symbol(opened2), enable_events=True, k='-OPEN SEC2-'), sg.T('Section 2', enable_events=True, k='-OPEN SEC2-TEXT', right_click_menu=section_right_click)],
            [collapse(section2, '-SEC2-', opened2)]
]

createListLayout(programValues['List'])
createCombo()

layout =   [
            [sg.Menu(menu)],
            [sg.Combo(combo,default_value=combo[0] , size=(100, 1), key='-COMBO-', readonly=True)],
            [sg.Column(listLayout,size=(300,400), key='-LB-', scrollable=True, vertical_scroll_only=True, pad=((0,5),(10,10)))],
            [sg.Button('Add Task', image_size=(130,40), pad=((5,0),(0,10)), image_filename='white.png', border_width=0, button_color=('black', 'black')), sg.Button('Add Section', image_size=(130,40), pad=((5,0),(0,10)), image_filename='white.png', border_width=0, button_color=('black', 'black'))]
            ]

window = sg.Window('To Do List', layout, size=(300,500))
print(elementKeys)

while True:             # Event Loop
    event, values = window.read()
    print(event, values)
    if event == sg.WIN_CLOSED or event == 'Exit':
        break

    if 'ARROW' in event:
        eventName = event.replace(' ARROW', '')
        SectionsOpen[eventName] = not SectionsOpen[eventName]
        window[f'{event}'].update(SYMBOL_DOWN if SectionsOpen[eventName] else SYMBOL_RIGHT)
        window[f'{eventName} CONTENT'].update(visible=SectionsOpen[eventName])

    if event in elementKeys:
        SectionsOpen[event] = not SectionsOpen[event]
        window[f'{event} ARROW'].update(SYMBOL_DOWN if SectionsOpen[event] else SYMBOL_RIGHT)
        window[f'{event} CONTENT'].update(visible=SectionsOpen[event])

    if event.startswith('-OPEN SEC1-'):
        opened1 = not opened1
        window['-OPEN SEC1-'].update(SYMBOL_DOWN if opened1 else SYMBOL_RIGHT)
        window['-SEC1-'].update(visible=opened1)

    if event.startswith('-OPEN SEC2-'):
        opened2 = not opened2
        window['-OPEN SEC2-'].update(SYMBOL_DOWN if opened2 else SYMBOL_RIGHT)
        window['-SEC2-'].update(visible=opened2)

    

window.close()
