import PySimpleGUI as sg
from datetime import datetime
from re import match

#     TODOlist is a todo list application that features sections which can be used to organise tasks
#     Copyright (C) 2021  Snaiel
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
#     contact: snaiel.email@gmail.com



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
        'menu_bar': [['&Edit', ['Undo', 'Redo', '---', 'Add', ['Task::ADD', 'Section::ADD', 'List::ADD(MENU)', 'Paste::ADD'], ['Delete', ['List::DELETE'], '---', 'Lists', 'Settings', '---', '&Refresh']]], ['Help', ['About', 'Wiki']]],
        'disabled_menu_bar': [['Edit', ['!Undo', '!Redo', '---', '!Add', ['Task'], ['!Delete', ['List'], '---', 'Lists', 'Settings', '---', '!Refresh']]], ['Help', ['About', 'Wiki']]],
        'task_level_0_and_1': ['Right', ['Move', ['Up::MOVE', 'Down::MOVE'], '---', 'Copy::TASK', 'Cut::TASK', '---', 'Insert', ['Task::INSERT', 'Section::INSERT', 'Paste::INSERT'], 'Rename', 'Delete']],
        'section_level_0_and_1': ['&Right', ['Move', ['Up::MOVE', 'Down::MOVE'], '---', 'Copy::SECTION', 'Cut::SECTION', '---', 'Add', ['Task::ADDTO', 'Section::ADDTO', 'Paste::ADDTO'], '&Insert', ['Task::INSERT', 'Section::INSERT', 'Paste::INSERT'],  'Rename', 'Delete']],
        'task_level_2': ['Right', ['Move', ['Up::MOVE', 'Down::MOVE'], '---', 'Copy::TASK', 'Cut::TASK', '---', 'Insert', ['Task::INSERT', 'Paste::INSERT'], 'Rename', 'Delete']],
        'section_level_2': ['Right', ['Move', ['Up::MOVE', 'Down::MOVE'], '---', 'Copy::SECTION', 'Cut::SECTION', '---', 'Add', ['Task::ADDTO', 'Paste::ADDTO'], 'Rename', 'Delete'], '&Insert', ['Task::INSERT', 'Section::INSERT']]
        }

program_values = {
                'current_list': '',
                'time_to_reset_daily_sections': '',
                'background_colour': '',
                'button_colour': '',
                'text_colour_1': '',
                'text_colour_2': ''
                }

temp_data = {
            'list_index': '',
            'last_time_closed': '',
            'element_keys': [],
            'sections_open': {},
            'combo': [],
            'last_element_right_clicked': '',
            'list_selected_to_edit': '',
            'last_list_on': '',
            'element_copied': ('', None),
            'element_to_move': ('', None),
            'last_scrollbar_position': (0.0, 1.0),
            'previous_settings': {
                'time_to_reset_daily_sections': '',
                'background_colour': '',
                'button_colour': '',
                'text_colour_1': '',
                'text_colour_2': ''
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

def read_data_file():
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
        task_data = file[(file.index('Data:') + 1):]

        previous_line = None

        todolist_data = []
        list_data = []
        section = []
        subsection = []

        for i in settings:
            i = i.split()
    
            if i[0] == 'time_to_reset_daily_sections:':
                program_values['time_to_reset_daily_sections'] = i[1]
            if i[0] == 'background_colour:':
                program_values['background_colour'] = i[1]
                continue
            if i[0] == 'button_colour:':
                program_values['button_colour'] = i[1]
                continue
            if i[0] == 'text_colour_1:':
                program_values['text_colour_1'] = i[1]
                continue
            if i[0] == 'text_colour_2:':
                program_values['text_colour_2'] = i[1]
                continue

        for i in task_data:
            i = i.split()

            if i[0] == 'last_time_closed:':
                temp_data['last_time_closed'] = ' '.join(i[1:3])
                

            if previous_line != None and previous_line[0] == '---' and i[0] != '---':
                if i[0] == '----':
                    subsection.append({' '.join(i[1:-1]): booleans[i[-1]]})
                elif len(section) != 0:
                    list_data.append(section.copy())
                    section.clear() 

            if previous_line != None and previous_line[0] == '----' and i[0] != '----':
                if len(subsection) != 0:
                    section.append(subsection.copy())
                    subsection.clear() 

            if i[0] == '----' and previous_line[0] == '----':
                subsection.append({' '.join(i[1:-1]): booleans[i[-1]]})

            if i[0] == '---':

                if i[-1] not in tasks and previous_line[0] == '---' and previous_line[-1] not in tasks:
                    section.append(subsection.copy())
                    subsection.clear() 

                if i[-1] in tasks:
                    section.append({' '.join(i[1:-1]): booleans[i[-1]]})
                else:
                    subsection.append({' '.join(i[1:-1]): booleans[i[-1]]})

            if i[0] == '--':

                if i[-1] not in tasks and previous_line[0] == '--' and previous_line[-1] not in tasks:
                    list_data.append(section.copy())
                    section.clear() 

                if i[-1] in tasks:
                    list_data.append({' '.join(i[1:-1]): booleans[i[-1]]})
                else:
                    section.append({' '.join(i[1:-1]): booleans[i[-1]]})

            if i[0] == '-':
                if len(list_data) != 0:
                    todolist_data.append(list_data.copy())
                    list_data.clear()

                if i[-1] == '!':
                    list_data.append(' '.join(i[1:-1]))
                    program_values['current_list'] = ' '.join(i[1:-1])
                else:
                    list_data.append(' '.join(i[1:]))

            previous_line = i


        if len(subsection) != 0:
            section.append(subsection.copy())
            subsection.clear()
        if len(section) != 0:
            list_data.append(section.copy())
            section.clear()
        if len(list_data) != 0:
            todolist_data.append(list_data.copy())
            list_data.clear()

        global data
        data = todolist_data

def write_data_file():
    with open('data.txt', 'w') as f:

        lines = ['Settings:' ,'Data:']
        file_settings = [
                            f"    time_to_reset_daily_sections: {program_values['time_to_reset_daily_sections']}", 
                            f"    background_colour: {program_values['background_colour']}", 
                            f"    button_colour: {program_values['button_colour']}",
                            f"    text_colour_1: {program_values['text_colour_1']}",
                            f"    text_colour_2: {program_values['text_colour_2']}"
                        ]
        file_data = [
            f"    last_time_closed: {temp_data['last_time_closed']}"
        ]

        for todolist in data:
            for content in todolist:
                if todolist.index(content) == 0:
                    file_data.append(f"- {content}{' !' if program_values['current_list'] == content else ''}")

                if type(content) is dict:
                    for key, value in content.items():
                        file_data.append(f"-- {key} {'(T)' if value == True else '(F)'}")

                if type(content) is list:

                    header = None
                    opened = None

                    for key, value in content[0].items():
                        header = key
                        opened = value

                    file_data.append(f"-- {header} {'(O)' if opened == True else '(C)'}")

                    for content_in_section in content:
                        if type(content_in_section) is dict and content.index(content_in_section) != 0:
                            for key, value in content_in_section.items():
                                file_data.append(f"--- {key} {'(T)' if value == True else '(F)'}")

                        if type(content_in_section) is list:

                            subheader = None
                            subheader_opened = None

                            for key, value in content_in_section[0].items():
                                subheader = key
                                subheader_opened = value

                            file_data.append(f"--- {subheader} {'(O)' if subheader_opened == True else '(C)'}")

                            for content_in_subsection in content_in_section:
                                if type(content_in_subsection) is dict and content_in_section.index(content_in_subsection) != 0:
                                    for key, value in content_in_subsection.items():
                                        file_data.append(f"---- {key} {'(T)' if value == True else '(F)'}")

        lines[1:1] = file_settings
        lines.extend(file_data)

        f.write('\n'.join(lines))

def reset_tasks_in_daily_section():
    for todolist in data:
        for content in todolist:
            if type(content) is list and 'Daily' in content[0]:
                for content_in_section in content:
                    if content.index(content_in_section) == 0:
                        continue

                    if type(content_in_section) is dict:
                        for key in content_in_section:
                            content_in_section[key] = False

                    if type(content_in_section) is list:
                        for sub_task in content_in_section:
                            if content_in_section.index(sub_task) == 0:
                                continue

                            if type(sub_task) is dict:
                                for key in sub_task:
                                    sub_task[key] = False

def colours():
    background_colour = program_values['background_colour']
    button_colour = program_values['button_colour']
    text_colour_1 = program_values['text_colour_1']
    text_colour_2 = program_values['text_colour_2']

    sg.theme_background_color(background_colour)
    sg.theme_element_background_color(background_colour)
    sg.theme_text_element_background_color(background_colour)
    sg.theme_button_color((text_colour_2, button_colour))
    sg.theme_text_color(text_colour_1)
    sg.theme_input_text_color(text_colour_2)

def collapse(layout, key, is_visible):
    """
    Helper function that creates a Column that can be later made hidden, thus appearing "collapsed"
    :param layout: The layout for the section
    :param key: Key used to make this seciton visible / invisible
    :return: A pinned column that can be placed directly into your layout
    :rtype: sg.pin
    """
    return sg.pin(sg.Column(layout, key=key, visible=is_visible, pad=(15,0)))

def symbol(opened):
    if opened is True:
        return SYMBOL_DOWN
    else:
        return SYMBOL_RIGHT

def create_combo():
    temp_data['combo'].clear()
    combo = temp_data['combo']
    for i in data:
        combo.append(i[0])

def create_task(name, checked, list_name, hierarchy_index, section_id):
    for i in data:
        if i[0] == list_name:
            list_index = str(data.index(i)).zfill(2)
            hierarchy_index = str(hierarchy_index).zfill(2)
            section_id = str(section_id).zfill(2)
            element_indexes = f"{list_index} {hierarchy_index} {section_id}"

            checkbox_key = f"{element_indexes} TASK CHECKBOX {name}"
            checkbox_text_key = f"{element_indexes} TASK TEXT {name}"

            right_click_menu = menus['task_level_0_and_1']
            if hierarchy_index == '02':
                right_click_menu = menus['task_level_2']

            if len(name) > 30:
                tooltip = name
            else:
                tooltip = None

            temp_data['element_keys'].append(f"{element_indexes} TASK {name}")
            return [sg.Checkbox('', default=checked, enable_events=True, key=checkbox_key, pad=((10, 0),(3,3))), sg.T(name, right_click_menu=right_click_menu, pad=(0,0), key=checkbox_text_key, enable_events=True, tooltip=tooltip)]

def create_section(header, opened, content, list_name, hierarchy_index, section_id):
    temp_data['sections_open'][f'{header}'] = opened
    for i in data:
        if i[0] == list_name:
            list_index = str(data.index(i)).zfill(2)
            hierarchy_index = str(hierarchy_index).zfill(2)
            section_id = str(section_id).zfill(2)
            element_indexes = f"{list_index} {hierarchy_index} {section_id}"

            sectionArrowKey = f'{element_indexes} SECTION ARROW {header}'
            sectionTextKey = f'{element_indexes} SECTION TEXT {header}'
            section_contentKey = f'{element_indexes} SECTION CONTENT {header}'

            right_click_menu = menus['section_level_0_and_1']
            if hierarchy_index == '01':
                right_click_menu = menus['section_level_2']

            if len(header) > 30:
                tooltip = header
            else:
                tooltip = None

            temp_data['element_keys'].append(f"{element_indexes} SECTION {header}")
            return [[sg.T(symbol(opened), enable_events=True, k=sectionArrowKey, pad=((10, 0),(3,3))), sg.T(header, enable_events=True, k=sectionTextKey, right_click_menu=right_click_menu, tooltip=tooltip)], [collapse(content, section_contentKey, opened)]]

def create_list_layout(list_to_create):
    created_list_layout = []

    section_id = 0

    for i in data:
        if i[0] is list_to_create:
            contents = i
            for content in contents:
                if type(content) is dict:
                    for key, value in content.items():
                        created_list_layout.append(create_task(key, value, list_to_create, 0, 0))

                if type(content) is list:
                    section_id += 1

                    id_of_section = section_id

                    header = None
                    opened = None

                    for key, value in content[0].items():
                            header = key
                            opened = value

                    section_content = []

                    for content_in_section in content:
                        if type(content_in_section) is dict and content.index(content_in_section) != 0:
                            for key, value in content_in_section.items():
                                section_content.append(create_task(key, value, list_to_create, 1, id_of_section))

                        if type(content_in_section) is list:

                            section_id += 1

                            subheader = None
                            subheader_opened = None
                            
                            for key, value in content_in_section[0].items():
                                    subheader = key
                                    subheader_opened = value

                            subsection_content = []

                            for content_in_subsection in content_in_section:

                                if type(content_in_subsection) is dict and content_in_section.index(content_in_subsection) != 0:
                                    for key, value in content_in_subsection.items():
                                        subsection_content.append(create_task(key, value, list_to_create, 2, section_id))

                            for i in create_section(subheader, subheader_opened, subsection_content, list_to_create, 1, id_of_section):
                                section_content.append(i)

                    for i in create_section(header, opened, section_content, list_to_create, 0, 0):
                        created_list_layout.append(i)    
    return created_list_layout

def create_row_of_columns(list_to_create):
    list_of_columns = []
    for i in data:
        list_layout = create_list_layout(i[0])
        list_of_columns.append(sg.Column(layout=list_layout, visible=i[0] == list_to_create, size=(300,390), key=f'COL{data.index(i)}', scrollable=True, vertical_scroll_only=True, pad=((0,5),(10,10))))
    
    list_editor_layout = [
        [sg.Listbox(key='LISTS LISTBOX', values=tuple(temp_data['combo']), size=(32,10), pad=(16,10), enable_events=True)],
        [sg.B('NONE', focus=True, visible=False)],
        [sg.B('Add', k='List::ADD(BUTTON)', size=(28,2), pad=(22, 8), border_width=0)],
        [sg.B('Rename', k='List::RENAME', size=(13, 2), pad=((22, 5), (0, 0)), border_width=0), sg.B('Delete', k='List::DELETE', size=(13, 2), border_width=0)],
        [sg.B('Move up', k='List::MOVEUP', size=(13, 2), pad=((22, 5), (6, 0)), border_width=0), sg.B('Move down', k='List::MOVEDOWN', size=(13, 2), pad=((5, 0), (6, 0)), border_width=0)],
        [sg.B('Undo', k='List::UNDO', size=(13, 2), pad=((22, 5), (8, 0)), border_width=0), sg.B('Redo', k='List::REDO', size=(13, 2), pad=((5, 0), (8, 0)), border_width=0)]
    ]

    frame_layout = [
        [sg.CB('', pad=((10, 0),(3,3))), sg.T('Colour                                   ', pad=(0,0))],
        [sg.T(symbol(True), pad=((10, 0),(3,3))), sg.T('Settings')], [collapse([[sg.CB('', pad=((10, 0),(3,3))), sg.T('Apply', pad=(0,0))]], None, True)]
    ]

    settings_layout = [
        [sg.Text('Reset Daily at', pad=(6, 20)), sg.Input(default_text=program_values['time_to_reset_daily_sections'], key='-TIME_TO_RESET_DAILY_SECTIONS-', size=(18,1), pad=((31,5),(0,0)))],
        [sg.Text('Background Colour', pad=(6,0)), sg.Input(default_text=program_values['background_colour'], key='-BACKGROUND_COLOUR-', size=(9,1), pad=((3,5),(0,0))), sg.ColorChooserButton('Colour...', target=(sg.ThisRow, -1), border_width=0)],
        [sg.Text('Button Colour', pad=(6,0)), sg.Input(default_text=program_values['button_colour'], key='-BUTTON_COLOUR-', size=(9,1), pad=((34,5),(0,0))), sg.ColorChooserButton('Colour...', target=(sg.ThisRow, -1), border_width=0, pad=(5,5))],
        [sg.Text('Text Colour 1', pad=(6,0)), sg.Input(default_text=program_values['text_colour_1'], key='-TEXT_COLOUR_1-', size=(9,1), pad=((36,5),(0,0))), sg.ColorChooserButton('Colour...', target=(sg.ThisRow, -1), border_width=0, pad=(5,5))],
        [sg.Text('Text Colour 2', pad=(6,0)), sg.Input(default_text=program_values['text_colour_2'], key='-TEXT_COLOUR_2-', size=(9,1), pad=((36,5),(0,0))), sg.ColorChooserButton('Colour...', target=(sg.ThisRow, -1), border_width=0, pad=(5,5))],
        [sg.Frame('Result', frame_layout, pad=(25,50), title_color=program_values['text_colour_1'])]
    ]

    list_of_columns.append(sg.Column(layout=list_editor_layout, visible=True if program_values['current_list'] == 'LIST EDITOR' else False, size=(300,400), key=f'COL LIST EDITOR', scrollable=False, pad=((0,5),(10,10))))
    list_of_columns.append(sg.Column(layout=settings_layout, visible=True if program_values['current_list'] == 'SETTINGS' else False, size=(300,390), key=f'COL SETTINGS', scrollable=False, pad=((0,5),(10,10))))
    return(list_of_columns)

def create_layout(list_to_create):
    if list_to_create is None:
        list_to_create = program_values['current_list']

    if list_to_create in ('LIST EDITOR', 'SETTINGS'):
        add_buttons_visible = False
        if list_to_create == 'LIST EDITOR':
            default_value_of_combo_box = 'List Editor'
        else:
            default_value_of_combo_box = 'Settings'
    else:
        add_buttons_visible = True
        default_value_of_combo_box = temp_data['combo'][temp_data['combo'].index(program_values['current_list'] if program_values['current_list'] != 'LIST EDITOR' else temp_data['combo'][0])]

    add_buttons_column = [
        [sg.pin(sg.Button('Add Task', size=(15,2), key='Task::ADD(BUTTON)', pad=((0,0),(2,0)), border_width=0)), sg.pin(sg.Button('Add Section', size=(15,2), key='Section::ADD(BUTTON)', pad=((18,0),(2,0)), border_width=0))]
    ]

    apply_revert_buttons_columns = [
        [sg.B('Apply', size=(15,2), border_width=0, pad=((0,0),(2,0))), sg.B('Revert', size=(15, 2), border_width=0, pad=((18,0),(2,0)))]
    ]

    return [
            [sg.Menu(menus['menu_bar'], key='-MENU BAR-')],
            [sg.Combo(temp_data['combo'],default_value=default_value_of_combo_box , size=(100, 1), key='-COMBO-', readonly=True, enable_events=True)],
            create_row_of_columns(list_to_create),
            [sg.Col(add_buttons_column, k='COL ADD BUTTONS', visible=add_buttons_visible), sg.Col(apply_revert_buttons_columns, k='COL APPLY REVERT BUTTONS', visible=True if program_values['current_list'] == 'SETTINGS' else False)]
        ]
        
def update_data(element_type, event):
    if element_type == 'Task':
        if 'TEXT' in event:
                name = event[19:]
                element_indexes = event[:8]
                checked =  window[f"{element_indexes} TASK CHECKBOX {name}"].Get()
                window[f"{element_indexes} TASK CHECKBOX {name}"].update(value=not checked)
        else:
            name = event[23:]
    else:
        element_indexes = event[:8]

        if 'ARROW' in event:
            name = event[23:]
        else:
            name = event[22:]

        temp_data['sections_open'][name] = not temp_data['sections_open'][name]
        window[f"{element_indexes} SECTION ARROW {name}"].update(SYMBOL_DOWN if temp_data['sections_open'][name] else SYMBOL_RIGHT)
        window[f"{element_indexes} SECTION CONTENT {name}"].update(visible=temp_data['sections_open'][name]) 

    for todolist in data:
            if todolist[0] == program_values['current_list']:
                for content in todolist:
                    if element_type == 'Section':
                        if type(content) is list:
                            if name in content[0]:
                                content[0][name] = temp_data['sections_open'][name]
                                return

                            for content_in_section in content:
                                if type(content_in_section) is list:
                                    if name in content_in_section[0]:
                                        content_in_section[0][name] = temp_data['sections_open'][name]
                                        return

                    if element_type == 'Task':
                        if type(content) is dict:
                            if name in content:
                                content[name] = not content[name]
                                return
                            
                        if type(content) is list:
                            for content_in_section in content:
                                if type(content_in_section) is dict:
                                    if name in content_in_section:
                                        content_in_section[name] = not content_in_section[name]
                                        return
                                if type(content_in_section) is list:
                                    for content_in_subsection in content_in_section:
                                        if name in content_in_subsection:
                                            content_in_subsection[name] = not content_in_subsection[name]
                                            return

def bindings():
    for i in temp_data['element_keys']:
        element_key = i.split(' ')
        element_key.insert(4, 'TEXT')
        window[' '.join(element_key)].bind('<Button-3>', ' +RIGHT CLICK+')
    window['LISTS LISTBOX'].bind('<Double-Button-1>', ' +DOUBLE CLICK+')

def add_or_insert_element_calculations():
    section_name_to_add_to = None
    hierarchy_index = '00'
    section_id = '00'

    if 'ADD' in event:
        if 'BUTTON' in event:
            element_type = event[:-13]
        else:
            element_type = event[:-5]
    else:
        element_type = event[:-8]
        section_id = temp_data['last_element_right_clicked'][6:8]

    if 'ADDTO' in event:
        section_name_to_add_to = temp_data['last_element_right_clicked'][22:]
        hierarchy_index = temp_data['last_element_right_clicked'][3:5]
        hierarchy_index = str((int(hierarchy_index) + 1)).zfill(2)
        section_id = str((int(temp_data['last_element_right_clicked'][6:8]) + 1)).zfill(2)
        element_type = event[:-7]

    if 'Paste' in event and temp_data['element_copied'][1] is not None:
        element_type = 'Task' if type(temp_data['element_copied'][1]) is bool else 'Section'
        if element_type == 'Task':
            element_name = temp_data['element_copied'][0][19:]
        else:
            element_name = list(temp_data['element_copied'][0][0].keys())[0]

        if element_type[0] == 'T':
            element_to_add = {element_name: temp_data['element_copied'][1]}
        else:
            if int(hierarchy_index) == 2:
                current_location = window.CurrentLocation()
                sg.popup('Cannot support more subsections\nPasting tasks within copied section...', title='Error', location=(current_location[0] + 25, current_location[1] + 100), icon='icon.ico')
                element_to_add = tuple(x for x in temp_data['element_copied'][0][1:] if type(x) is dict)
            elif int(hierarchy_index) > 0 and temp_data['element_copied'][1] == 2:
                element_to_add = [x for x in temp_data['element_copied'][0] if type(x) is dict]
                current_location = window.CurrentLocation()
                sg.popup('Cannot support more subsections\nPasting without subsections...', title='Error', location=(current_location[0] + 30, current_location[1] + 100), icon='icon.ico')
            else:
                element_to_add = temp_data['element_copied'][0]
    elif 'Paste' not in event:
        element_name = get_text(f'{element_type} Name:')
        if element_type[0] == 'T':
            element_to_add = {element_name: False}
        else:
            element_to_add = [{element_name: False}]
    else:
        element_name = None
        element_to_add = None

    if check_if_element_exists(temp_data['list_index'], hierarchy_index, section_id, element_type, element_name) == False:
        if element_name not in ('', None):
            temp_data['last_scrollbar_position'] = window[f"COL{temp_data['combo'].index(program_values['current_list'])}"].Widget.vscrollbar.get()
            if 'ADD' in event:
                add_element(element_to_add, section_name_to_add_to, hierarchy_index)
            else:
                if temp_data['last_element_right_clicked'][9:10] == 'T':
                    element_name_of_insert_position = temp_data['last_element_right_clicked'][19:]
                else:
                    element_name_of_insert_position = temp_data['last_element_right_clicked'][22:]
                
                insert_element(element_to_add, element_name_of_insert_position, hierarchy_index, section_id)
    else:
        current_location = window.CurrentLocation()
        sg.popup(f'Element already exists within current area/ section', title='Error', location=(current_location[0] - 14, current_location[1] + 100), icon='icon.ico')

def add_element(element_to_add, section_name_to_add_to, hierarchy_index):
    if element_to_add is None:
        return
    for todolist in data:
        current_list = program_values['current_list']
        if todolist[0] == current_list:
            if hierarchy_index == '00':
                todolist.append(element_to_add)
                return create_new_window()
            elif hierarchy_index == '01':
                for content in todolist:
                    if type(content) is list and section_name_to_add_to in content[0]:
                        content.append(element_to_add)
                        return create_new_window()
            elif hierarchy_index == '02':
                for content in todolist:
                    if type(content) is list:
                        for content_in_section in content:
                            if type(content_in_section) is list and section_name_to_add_to in content_in_section[0]:
                                if type(element_to_add) is tuple:
                                    for task in element_to_add:
                                        content_in_section.append(task)
                                else:
                                    content_in_section.append(element_to_add)
                                return create_new_window()

def insert_element(element_to_insert, element_name_of_insert_position, hierarchy_index, section_id):
    if element_to_insert is None:
        return
    local_section_id = 0

    for todolist in data:
        if todolist[0] == program_values['current_list']:
            for task in [task for task in todolist if type(task) is dict]:
                if element_name_of_insert_position in task and hierarchy_index == '00':
                    todolist.insert(todolist.index(task), element_to_insert)
                    return create_new_window()
            for section in [section for section in todolist if type(section) is list]:
                if element_name_of_insert_position in section[0] and hierarchy_index == '00':
                    todolist.insert(todolist.index(section), element_to_insert)
                    return create_new_window()
                local_section_id += 1
                for task in [task for task in section if type(task) is dict]:
                    if element_name_of_insert_position in task and int(section_id) == local_section_id:
                        section.insert(section.index(task), element_to_insert)
                        return create_new_window()
                for subsection in [subsection for subsection in section if type(subsection) is list]:
                    if element_name_of_insert_position in subsection[0] and int(section_id) == local_section_id:
                        section.insert(section.index(subsection), element_to_insert)
                        return create_new_window()
                else:
                    for subsection in [subsection for subsection in section if type(subsection) is list]:
                        local_section_id += 1
                        for task in [task for task in subsection if type(task) is dict]:
                            if element_name_of_insert_position in task and int(section_id) == local_section_id:
                                if type(element_to_insert) is tuple:
                                    for taskToInsert in element_to_insert:
                                        subsection.insert(subsection.index(task), taskToInsert)
                                else:
                                    subsection.insert(subsection.index(task), element_to_insert)
                                return create_new_window()

def rename_element():
    element = temp_data['last_element_right_clicked']
    new_name = get_text('Rename to:')

    hierarchy_index = element[3:5]
    section_id = element[6:8]

    if 'TASK' in element:
        element_type = 'Task'
        old_name = element[19:]
    else:
        element_type = 'Section'
        old_name = element[22:]

    if check_if_element_exists(temp_data['list_index'], hierarchy_index, section_id, element_type, new_name) == False:
        if new_name not in ('', None):
            local_section_id = 0

            for todolist in data:
                if todolist[0] == program_values['current_list']:
                    for task in [task for task in todolist if type(task) is dict]:
                        if element_type == 'Task' and  old_name in task and hierarchy_index == '00':
                            task[new_name] = task.pop(old_name)
                            return create_new_window()
                    for section in [section for section in todolist if type(section) is list]:
                        if element_type == 'Section' and old_name in section[0] and hierarchy_index == '00':
                            section[0][new_name] = section[0].pop(old_name)
                            return create_new_window()
                        local_section_id += 1
                        for task in [task for task in section if type(task) is dict]:
                            if element_type == 'Task' and  old_name in task and int(section_id) == local_section_id:
                                task[new_name] = task.pop(old_name)
                                return create_new_window()
                        for subsection in [subsection for subsection in section if type(subsection) is list]:
                            if element_type == 'Section' and old_name in subsection[0] and int(section_id) == local_section_id:
                                subsection[0][new_name] = subsection[0].pop(old_name)
                                return create_new_window()
                        else:
                            for subsection in [subsection for subsection in section if type(subsection) is list]:
                                local_section_id += 1
                                for task in [task for task in subsection if type(task) is dict]:
                                    if element_type == 'Task' and old_name in task and int(section_id) == local_section_id:
                                        task[new_name] = task.pop(old_name)
                                        return create_new_window()
    else:
        current_location = window.CurrentLocation()
        sg.popup(f'Element already exists within current area/ section', title='Error', location=(current_location[0] - 14, current_location[1] + 100), icon='icon.ico')

def delete_element():

    element = temp_data['last_element_right_clicked']
    if 'TASK' in element:
        element_name = element[19:]
        element_type = 'Task'
    else:
        element_name = element[22:]
        element_type = 'Section'

    hierarchy_index = element[3:5]
    section_id = element[6:8]
    
    local_section_id = 0

    for todolist in data:
        if todolist[0] == program_values['current_list']:
            for task in [task for task in todolist if type(task) is dict]:
                if element_type == 'Task' and  element_name in task and hierarchy_index == '00':
                    todolist.remove(task)
                    return create_new_window()
            for section in [section for section in todolist if type(section) is list]:
                if element_type == 'Section' and element_name in section[0] and hierarchy_index == '00':
                    todolist.remove(section)
                    return create_new_window()
                local_section_id += 1
                for task in [task for task in section if type(task) is dict]:
                    if element_type == 'Task' and  element_name in task and int(section_id) == local_section_id:
                        section.remove(task)
                        return create_new_window()
                for subsection in [subsection for subsection in section if type(subsection) is list]:
                    if element_type == 'Section' and element_name in subsection[0] and int(section_id) == local_section_id:
                        section.remove(subsection)
                        return create_new_window()
                else:
                    for subsection in [subsection for subsection in section if type(subsection) is list]:
                        local_section_id += 1
                        for task in [task for task in subsection if type(task) is dict]:
                            if element_type == 'Task' and element_name in task and int(section_id) == local_section_id:
                                subsection.remove(task)
                                return create_new_window()

def rename_list():
    print(len(values['LISTS LISTBOX']))
    if len(values['LISTS LISTBOX']) != 0:
        new_list_name = get_text('Rename to:')
        if new_list_name not in temp_data['combo'] and new_list_name not in ('', None):
            list_to_rename = values['LISTS LISTBOX'][0]
            for i in data:
                if i[0] is list_to_rename:
                    i[0] = new_list_name
                    break
            for list_name_in_combo in temp_data['combo']:
                if list_name_in_combo is list_to_rename:
                    list_name_in_combo = new_list_name
                    break
        elif new_list_name in temp_data['combo']:
            current_location = window.CurrentLocation()
            location = (current_location[0] + 80, current_location[1] + 100)
            sg.popup('List already exists', title='Error', location=location, icon='icon.ico')
    elif len(values['LISTS LISTBOX']) == 0:
        current_location = window.CurrentLocation()
        location = (current_location[0] + 80, current_location[1] + 100)
        sg.popup('Select a list first', title='Error', location=location, icon='icon.ico')

    create_combo()
    window['-COMBO-'].update(values=temp_data['combo'])
    window['LISTS LISTBOX'].update(values=tuple(temp_data['combo']))

def delete_list():
    if window[f'COL LIST EDITOR'].visible == True:
        list_to_delete = values['LISTS LISTBOX'][0]
    else:
        list_to_delete = program_values['current_list']
        
    for i in data:
        if i[0] == list_to_delete:
            data.remove(i)
            temp_data['combo'].remove(list_to_delete)
            for list_name in temp_data['combo']:
                if list_name is not list_to_delete:
                    if window[f'COL LIST EDITOR'].visible == True:
                        program_values['current_list'] = 'LIST EDITOR'
                    else:
                        program_values['current_list'] = list_name
                    break
            return create_new_window()

def move_list():
    combo = temp_data['combo']
    list_name = ''

    if values['LISTS LISTBOX'] != []:
        list_name = values['LISTS LISTBOX'][0]
    elif values['LISTS LISTBOX'] == [] and temp_data['list_selected_to_edit'] != '':
        list_name = temp_data['list_selected_to_edit']
    else:
        current_location = window.CurrentLocation()
        location = (current_location[0] + 80, current_location[1] + 100)
        sg.popup('Select a list first', title='Error', location=location, icon='icon.ico')
        return

    for todolist in data:
        if todolist[0] is list_name:
            if 'UP' in event:
                a, b = data.index(todolist), data.index(todolist) - 1
                if a == 0:
                    return
            else:
                a, b = data.index(todolist), data.index(todolist) + 1   
                if len(data) == b:
                    return
            data[b], data[a] = data[a], data[b]
            break

    create_combo()
    create_new_window()

def copy_section(element_name, hierarchy_index, section_id):
    local_section_id = 0
    for todolist in data:
        if todolist[0] == program_values['current_list']:
            for section in [section for section in todolist if type(section) is list]:
                if element_name in section[0] and hierarchy_index == '00':
                    hierarchy_levels = 1
                    if len([x for x in section if type(x) is list]) != 0:
                        hierarchy_levels = 2
                    return(section, hierarchy_levels)
                local_section_id += 1
                for subsection in [subsection for subsection in section if type(subsection) is list]:
                    if element_name in subsection[0] and int(section_id) == local_section_id:
                        return(subsection, 2)

def copy_element():
    element_key = temp_data['last_element_right_clicked']

    if 'TASK' in event:
        element_key = element_key.split(' ')
        element_key.remove('TEXT')    
        element_key.insert(4, 'CHECKBOX')
        element_key = ' '.join(element_key)
        temp_data['element_copied'] = (temp_data['last_element_right_clicked'], values[element_key])
    else:   # A Section
        element_name = element_key[22:]
        hierarchy_index = temp_data['last_element_right_clicked'][3:5]
        section_id = temp_data['last_element_right_clicked'][6:8]
        temp_data['element_copied'] = copy_section(element_name, hierarchy_index, section_id)

def cut_element():
    element_key = temp_data['last_element_right_clicked']
    element_key = element_key.split(' ')
    element_name = ' '.join(element_key[5:])
    element_type = element_key[3].title()
    hierarchy_index = element_key[1]
    section_id = element_key[2]

    if 'TASK' in event:
        element_key.remove('TEXT')
        element_key.insert(4, 'CHECKBOX')
        element_key = ' '.join(element_key)
        temp_data['element_copied'] = (temp_data['last_element_right_clicked'], values[element_key])

        delete_element(element_name, element_type, hierarchy_index, section_id)
    else:   # A Section
        temp_data['element_copied'] = copy_section(element_name, hierarchy_index, section_id)
        delete_element(element_name, element_type, hierarchy_index, section_id)

def move_element():
    element_key = temp_data['last_element_right_clicked']
    element_key = element_key.split(' ')

    element_to_move = ' '.join(element_key[5:])
    hierarchy_index = element_key[1]
    section_id = element_key[2]

    direction = event[:-6]

    local_section_id = 0

    for todolist in data:
        if todolist[0] == program_values['current_list']:
            for task in [task for task in todolist if type(task) is dict]:
                if element_to_move in task and hierarchy_index == '00':
                    if direction == 'Up':
                        a, b = todolist.index(task), todolist.index(task) - 1
                        if a == 1:
                            return
                    else:
                        a, b = todolist.index(task), todolist.index(task) + 1   
                        if len(todolist) == b:
                            return
                    todolist[b], todolist[a] = todolist[a], todolist[b]
                    return create_new_window()
            for section in [section for section in todolist if type(section) is list]:
                if element_to_move in section[0] and hierarchy_index == '00':
                    if direction == 'Up':
                        a, b = todolist.index(section), todolist.index(section) - 1
                        if a == 1:
                            return
                    else:
                        a, b = todolist.index(section), todolist.index(section) + 1   
                        if len(todolist) == b:
                            return
                    todolist[b], todolist[a] = todolist[a], todolist[b]
                    return create_new_window()
                local_section_id += 1
                for task in [task for task in section if type(task) is dict]:
                    if element_to_move in task and int(section_id) == local_section_id:
                        if direction == 'Up':
                            a, b = section.index(task), section.index(task) - 1
                            if a == 1:
                                return
                        else:
                            a, b = section.index(task), section.index(task) + 1   
                            if len(section) == b:
                                return
                        section[b], section[a] = section[a], section[b]
                        return create_new_window()
                for subsection in [subsection for subsection in section if type(subsection) is list]:
                    if element_to_move in subsection[0] and int(section_id) == local_section_id:
                        if direction == 'Up':
                            a, b = section.index(subsection), section.index(subsection) - 1
                            if a == 1:
                                return
                        else:
                            a, b = section.index(subsection), section.index(subsection) + 1   
                            if len(section) == b:
                                return
                        section[b], section[a] = section[a], section[b]
                        return create_new_window()
                else:
                    for subsection in [subsection for subsection in section if type(subsection) is list]:
                        local_section_id += 1
                        for task in [task for task in subsection if type(task) is dict]:
                            if element_to_move in task and int(section_id) == local_section_id:
                                if direction == 'Up':
                                    a, b = subsection.index(task), subsection.index(task) - 1
                                    if a == 1:
                                        return
                                else:
                                    a, b = subsection.index(task), subsection.index(task) + 1   
                                    if len(subsection) == b:
                                        return
                                subsection[b], subsection[a] = subsection[a], subsection[b]
                                return create_new_window()

def check_if_element_exists(listIndex, hierarchy_index, section_id, element_type, element_name):
    return(f"{listIndex} {hierarchy_index} {section_id} {element_type.upper()} {element_name}" in temp_data['element_keys'])

def get_text(message):
    current_location = window.CurrentLocation()
    location = (current_location[0] - 25, current_location[1] + 100)
    return sg.popup_get_text(message, location=location, icon='icon.ico')

def apply_settings():
    current_location = window.CurrentLocation()

    previous_settings = temp_data['previous_settings']

    if match('^(2[0-3]|[01]{1}[0-9]):([0-5]{1}[0-9]):([0-5]{1}[0-9])$', values['-TIME_TO_RESET_DAILY_SECTIONS-']):
        previous_settings['time_to_reset_daily_sections'] = program_values['time_to_reset_daily_sections']
        program_values['time_to_reset_daily_sections'] = values['-TIME_TO_RESET_DAILY_SECTIONS-']
    else:
        location = (current_location[0] - 5, current_location[1] + 100)
        sg.popup('Please use correct format for time (HH:MM:SS)', title='Error', location=location, icon='icon.ico')
        return

    for colour in (values['-BACKGROUND_COLOUR-'], values['-BUTTON_COLOUR-'], values['-TEXT_COLOUR_1-'], values['-TEXT_COLOUR_2-']):
        if match('^#(?:[0-9a-fA-F]{3}){1,2}$', colour):
            pass
        else:
            location = (current_location[0] - 30, current_location[1] + 100)
            sg.popup(f'Please use correct format for colour (Hex). Wrong: {colour}', location=location, line_width=100, icon='icon.ico')
            return

    previous_settings['background_colour'] = program_values['background_colour']
    previous_settings['button_colour'] = program_values['button_colour']
    previous_settings['text_colour_1'] = program_values['text_colour_1']
    previous_settings['text_colour_2'] = program_values['text_colour_2']

    program_values['background_colour'] = values['-BACKGROUND_COLOUR-']
    program_values['button_colour'] = values['-BUTTON_COLOUR-']
    program_values['text_colour_1'] = values['-TEXT_COLOUR_1-']
    program_values['text_colour_2'] = values['-TEXT_COLOUR_2-']
        
    colours()
    create_new_window()

def revert_settings():
    previous_settings = temp_data['previous_settings']

    program_values['background_colour'] = previous_settings['background_colour']
    program_values['button_colour'] = previous_settings['button_colour']
    program_values['text_colour_1'] = previous_settings['text_colour_1']
    program_values['text_colour_2'] = previous_settings['text_colour_2']

    colours()
    create_new_window()

def startup():
    read_data_file()

    # Check whether to reset the daily section
    when_to_reset = f"{datetime.now().strftime(r'%d/%m/%Y')} {program_values['time_to_reset_daily_sections']}"
    date_and_time_now = datetime.now().strftime(r'%d/%m/%Y %H:%M:%S')

    if temp_data['last_time_closed'] < when_to_reset:
        if date_and_time_now > when_to_reset:
            reset_tasks_in_daily_section()

    # Sets the list index
    for todolist in data:
        if todolist[0] == program_values['current_list']:
            temp_data['list_index'] = str(data.index(todolist)).zfill(2)
            break

    colours()
    create_combo()
    
startup()

window = sg.Window('TODOlist', layout=create_layout(None), size=(300,500), finalize=True, icon='icon.ico')
bindings()

def create_new_window():
    temp_data['element_keys'].clear()
    global window
    window1 = sg.Window('TODOlist', layout=create_layout(None), location=window.CurrentLocation(), size=(300,500), finalize=True, icon='icon.ico')
    if program_values['current_list'] not in ('LIST EDITOR', "SETTINGS"):
        window1[f"COL{temp_data['combo'].index(program_values['current_list'])}"].Widget.canvas.yview_moveto(temp_data['last_scrollbar_position'][0])
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
        temp_data['last_time_closed'] = datetime.now().strftime(r'%d/%m/%Y %H:%M:%S')
        if program_values['current_list'] in ('LIST EDITOR', 'SETTINGS'):
            program_values['current_list'] = temp_data['last_list_on']
        #write_data_file()
        break

    # Checking what element the user right clicked
    if '+RIGHT CLICK+' in event:
        element_key = event[:-14]

        if element_key is not temp_data['last_element_right_clicked']:
            temp_data['last_element_right_clicked'] = element_key
            #print(f"Element right clicked was: {element_key}")

        event = window[element_key].user_bind_event
        window[element_key]._RightClickMenuCallback(event)
        event = element_key

    # Add a to do list
    if 'List::ADD' in event:
        list_name = get_text('List Name:')

        if list_name is not None and list_name not in temp_data['combo']:
            data.append([list_name])
            if 'MENU' in event:
                program_values['current_list'] = list_name
            create_combo()
            temp_data['list_index'] = str(temp_data['combo'].index(list_name)).zfill(2)
            create_new_window()
        elif list_name in temp_data['combo']:
            current_location = window.CurrentLocation()
            location = (current_location[0] + 80, current_location[1] + 100)
            sg.popup('List already exists', title='Error', location=location, icon='icon.ico')

    # Change which list your on
    if event == '-COMBO-':
        program_values['current_list'] = values['-COMBO-']
        temp_data['list_index'] = str(temp_data['combo'].index(values['-COMBO-'])).zfill(2)
        for i in data:
            if i[0] == program_values['current_list']:
                window[f'COL{data.index(i)}'].update(visible=True)
            else:
                window[f'COL{data.index(i)}'].update(visible=False)

        for i in ['LIST EDITOR', 'SETTINGS']:
            if window[f'COL {i}'].visible == True:
                window[f'COL {i}'].update(visible=False)

                window['COL APPLY REVERT BUTTONS'].update(visible=False)

                window['-MENU BAR-'].update(menu_definition=menus['menu_bar'])

        window['COL ADD BUTTONS'].update(visible=True)
        window['COL ADD BUTTONS'].unhide_row()


    # Appending or Inserting an element
    if any(x in event for x in ('ADD', 'INSERT')) and 'List' not in event:
        add_or_insert_element_calculations()

    # Opening and closing sections
    if 'SECTION' in event and not any(x in event for x in ('RIGHT CLICK', 'Copy', 'Cut')):
        update_data('Section', event)


    # Updating the checkbox
    if 'TASK' in event and 'RIGHT CLICK' not in event:
        update_data('Task', event)

    # Move element up or down
    if 'MOVE' in event and 'List' not in event:
        move_element()

    # Copy
    if 'Copy' in event:
        copy_element()

    # Cut
    if 'Cut' in event:
        cut_element()

    # Rename
    if event == 'Rename':
        rename_element()

    # Delete Element
    if event == 'Delete':
        delete_element()


    # Show LIST EDITOR Page
    if event == 'Lists':
        temp_data['last_list_on'] = program_values['current_list']

        for i in temp_data['combo']:
            if i == program_values['current_list']:
                window[f"COL{temp_data['combo'].index(i)}"].update(visible=False)
                break
        
        if window['COL SETTINGS'].visible == True:
            window['COL SETTINGS'].update(visible=False)

        window['-MENU BAR-'].update(menu_definition=menus['disabled_menu_bar'])

        program_values['current_list'] = 'LIST EDITOR'
        window['COL LIST EDITOR'].update(visible=True)
        window['COL ADD BUTTONS'].hide_row()
        window['-COMBO-'].update(value='List Editor')

    if event == 'LISTS LISTBOX +DOUBLE CLICK+':
        program_values['current_list'] = values['LISTS LISTBOX'][0]
        temp_data['list_index'] = str(temp_data['combo'].index(program_values['current_list'])).zfill(2)
        for i in data:
            if i[0] == program_values['current_list']:
                window[f'COL{data.index(i)}'].update(visible=True)
            else:
                window[f'COL{data.index(i)}'].update(visible=False)

        window['COL LIST EDITOR'].update(visible=False)
        window['COL ADD BUTTONS'].update(visible=True)
        window['COL ADD BUTTONS'].unhide_row()
        window['-MENU BAR-'].update(menu_definition=menus['menu_bar'])
        window['-COMBO-'].update(value=program_values['current_list'])
    
    # Rename List
    if event == 'List::RENAME':
        rename_list()

    # Delete List
    if event == 'List::DELETE':
        current_location = window.CurrentLocation()
        location = (current_location[0] + 4, current_location[1] + 100)
        if sg.popup_ok_cancel("This will delete the list and all of it's contents", title='Delete?', location=location, icon='icon.ico') == 'OK':
            delete_list()

    # Move a list up or down
    if 'List::MOVE' in event:
        move_list()

    # Settings Page
    if event == 'Settings':
        temp_data['last_list_on'] = program_values['current_list']

        for i in temp_data['combo']:
            if i == program_values['current_list']:
                window[f"COL{temp_data['combo'].index(i)}"].update(visible=False)
                break

        if window['COL LIST EDITOR'].visible == True:
            window['COL LIST EDITOR'].update(visible=False)

        window['-MENU BAR-'].update(menu_definition=menus['disabled_menu_bar'])

        program_values['current_list'] = 'SETTINGS'
        window['COL SETTINGS'].update(visible=True)
        window['COL APPLY REVERT BUTTONS'].update(visible=True)
        window['COL APPLY REVERT BUTTONS'].unhide_row()
        window['COL ADD BUTTONS'].update(visible=False)
        window['-COMBO-'].update(value='Settings')
    
    # Applying or Reverting Settings
    if event == 'Apply':
        apply_settings()
    elif event == 'Revert':
        revert_settings()

    if event == 'Refresh':
        create_new_window()
    

window.close()
