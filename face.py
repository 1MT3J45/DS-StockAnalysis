from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.app import App
import YP03
import dfgui
import pandas as pd

Builder.load_string('''
<faceTool>:
    num1: num1
    result: result
    orientation: 'vertical'
    BoxLayout:
        orientation: 'horizontal'
        Label:
            id: num1
            text: 'Stock Data Analysis'
        
    BoxLayout:
        orientation: 'horizontal'
        GridLayout:
            cols: 6
            Label:
                id: blank1
            Label:
                id: blank2
            Button:
                text: 'Execute'
                height: 10
                width: 30
                on_press: root.display_fun(self)
            Label:
                text: 'EMPTY SLOT'
                height: 10
                width: 30
                on_press:
            Button:
                text: "Show XLS Sheet"
                height: 10
                width: 30
                on_press: root.graph()
            Button:
                text: "Clear"
                height: 10
                width: 30
                on_press: root.clear_screen()
    BoxLayout:
        orientation: 'horizontal'
        Label:
            id: result
    GridLayout:
        cols: 2
        size_hint_y: None

        Button:
            text: "Clear"
            on_press: root.clear_screen()
            height: 10
            width: 30
        BubbleButton:
            text: 'Exit'
            on_press: root.exit_it()
            height: 10
            width: 30
''')


class face_app(App):
    def build(self):
        return faceTool()


class faceTool(BoxLayout):
    def __init__(self, **kwargs):
        super(faceTool, self).__init__(**kwargs)

    def display_fun(self, instance):
        '''Fuction called when numeric buttons are pressed,
        if the operation button is pressed the numbers after will be
        on the right hand side.
        '''
        DayClusterNames, length = YP03.execute()
        res = ''
        for i in range(len(DayClusterNames)):
            res = str(DayClusterNames[i])+'\n'+res
        self.result.text = str(res)

    def exit_it(self):
        exit(0)

    def graph(self):
        # xls = pd.read_excel('Res.xls')
        # df = pd.DataFrame(xls)
        # dfgui.show(df)
        import main

    def clear_screen(self):
        self.result.text = ''


face_app().run()
