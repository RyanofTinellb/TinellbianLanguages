import json
import tkinter.ttk as ttk
import tkinter as Tk
from contextlib import contextmanager


@contextmanager
def ignored(*exceptions):
    try:
        yield
    except exceptions:
        pass


class Wallet(Tk.StringVar):
    def __init__(self):
        super().__init__()


class Type(Tk.StringVar):
    def __init__(self):
        super().__init__()


class WalletBox(ttk.Combobox):
    def __init__(self, *args, **kwargs):
        values = ('Red Covered Wallet',
                  'Big Black Box',
                  'Pink and Light Grey Wallet',
                  'Black Leather Wallet',
                  'Yellow Wallet',
                  'Silver Box',
                  'Dark Blue Wallet',
                  'Brown Leather Wallet',
                  'Silver Wallet',
                  'Brown Box',
                  'Dark Blue Covered Wallet',
                  'Blue and Dark Gray Wallet',
                  'Black Box',
                  'Velcro Tabbed Black Wallet',
                  'Khaki Camoflage Covered Wallet')
        super().__init__(*args, **kwargs, values=values)


class TypeBox(ttk.Combobox):
    def __init__(self, *args, **kwargs):
        values = ('', 'Premiere', 'Start', 'Hiatus', 'Movie',
                  'Alone', 'Film', 'Back', 'End', 'Finale')
        super().__init__(*args, **kwargs, values=values)


class ListEditor(Tk.Frame):
    def __init__(self, filename):
        super().__init__()
        with open(filename, encoding='utf-8') as eplist:
            self.eplist = json.load(eplist, encoding='utf-8')

        def move(num):
            num = self.position.get()
            for index, frame in enumerate(self.frames, start=num):
                try:
                    frame.open_entry(self.eplist[index])
                except IndexError:
                    pass

        def up():
            self.position.set(self.position.get()-7)
            move(None)

        def down(event=None):
            self.position.set(self.position.get()+7)
            move(None)

        def shift(event=None):
            (down if event.delta < 0 else up)()

        def save(event=None, filename=filename):
            for frame in self.frames():
                frame.save_entry()
            with open(filename, 'w', encoding='urf-8') as eplist:
                json.dump(self.eplist, eplist, indent=0)

        self.frames = [EpisodeEditor(self.master) for x in range(7)]
        for row, frame in enumerate(self.frames):
            frame.bind('<MouseWheel>', shift)
            frame.grid(row=row, column=0)
        self.position = Tk.IntVar()
        k = ttk.Scale(self.master, from_=0, to=7000, variable=self.position, command=move,
                      orient='vertical', length=500)
        k.grid(row=0, rowspan=7, column=1)
        k.bind('<MouseWheel>', shift)
        Tk.Button(self.master, text='⬆', command=up).grid(row=2, column=2)
        Tk.Button(self.master, text='⬇', command=down).grid(row=3, column=2)
        Tk.Button(self.master, text='Save', command=save).grid(row=4, column=2)
        move(None)


obj = {Tk.StringVar: Tk.Entry, Tk.IntVar: Tk.Spinbox,
       Wallet: WalletBox, Type: TypeBox}
w = {Tk.StringVar: 20, Tk.IntVar: 5, Wallet: 20, Type: 10}


def clean(text):
    return text.replace('_', '').capitalize()


def pad(number):
    return ('0' if number < 10 else '') + str(number)


class EpisodeEditor(Tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.directory = dict(
            series=dict(meta=Tk.StringVar(),
                        series=Tk.StringVar(), number=Tk.IntVar()),
            season=dict(season=Tk.StringVar(), number=Tk.IntVar()),
            episode=dict(article=Tk.StringVar(),
                         episode=Tk.StringVar(), number=Tk.IntVar()),
            location=dict(disc=Tk.IntVar(), wallet=Wallet()),
            miscellaneous=dict(type_=Type(),
                               parts=Tk.IntVar(), section=Tk.StringVar()),
            date=dict(day=Tk.IntVar(), month=Tk.IntVar(), year=Tk.IntVar())
        )
        self.frames = {n: self.label_frame(n, f)
                       for n, f in self.directory.items()}
        for i, frame in enumerate(self.frames.values()):
            frame.grid(row=0, column=i, sticky='n')

    def label_frame(self, name, shape):
        frame = Tk.LabelFrame(self, text=clean(name))
        frame.bind()
        for row, (name, var) in enumerate(shape.items()):
            Tk.Label(frame, text=clean(name)).grid(
                row=row, column=0, sticky='w')
            obj[type(var)](frame, textvariable=var,
                           width=w[type(var)]).grid(row=row, column=1, sticky='w')
        return frame

    def open_entry(self, entry):
        self.entry = entry
        self.set_var('series', 'meta', entry.get('meta', ''))

        value = entry.get('series')
        with ignored(AttributeError):
            value = value.get('name')
        value = value if isinstance(value, str) else ''
        self.set_var('series', 'series', value)

        value = entry.get('series')
        with ignored(AttributeError):
            value = value.get('number')
        value = value if isinstance(value, int) else 0
        self.set_var('series', 'number', value)

        value = entry.get('season')
        with ignored(AttributeError):
            value = value.get('name')
        value = value if isinstance(value, str) else ''
        self.set_var('season', 'season', value)

        value = entry.get('season')
        with ignored(AttributeError):
            value = value.get('number')
        value = value if isinstance(value, int) else 0
        self.set_var('season', 'number', value)

        try:
            value = entry['ep']['article']
        except:
            value = ''
        self.set_var('episode', 'article', value)

        value = entry.get('ep')
        with ignored(AttributeError):
            value = value.get('name')
        value = value if isinstance(value, str) else ''
        self.set_var('episode', 'episode', value)

        value = entry.get('ep')
        with ignored(AttributeError):
            value = value.get('number')
        value = value if isinstance(value, int) else 0
        self.set_var('episode', 'number', value)

        value = entry.get('location')
        with ignored(AttributeError):
            value = value.get('wallet')
        self.set_var('location', 'wallet', value)

        value = entry.get('location')
        try:
            value = value.get('disc')
        except AttributeError:
            value = 0
        self.set_var('location', 'disc', value)

        value = entry.get('type', '')
        self.set_var('miscellaneous', 'type_', value)

        value = entry.get('multi', None)
        if isinstance(value, int):
            self.set_var('miscellaneous', 'parts', value)
            self.set_var('miscellaneous', 'section', '')
        elif isinstance(value, str):
            self.set_var('miscellaneous', 'parts', 0)
            self.set_var('miscellaneous', 'section', value)
        else:
            self.set_var('miscellaneous', 'parts', 0)
            self.set_var('miscellaneous', 'section', '')

        value = entry['date']
        self.set_var('date', 'day', value[-2:])
        self.set_var('date', 'month', value[4:-2])
        self.set_var('date', 'year', value[:4])

    def set_var(self, lat, long_, value):
        self.directory[lat][long_].set(value)

    def save_entry(self):
        sMeta = self.get_var('series', 'meta')
        sSeries = self.get_var('series', 'series')
        nSeries = self.get_var('series', 'number')
        nSeason = self.get_var('season', 'number')
        sSeason = self.get_var('season', 'season')
        sMulti = self.get_var('miscellaneous', 'section')
        nEp = self.get_var('episode', 'number')
        sEpArt = self.get_var('episode', 'article')
        sEp = self.get_var('episode', 'episode')
        nDisc = self.get_var('location', 'disc')
        nMulti = self.get_var('miscellaneous', 'parts')
        sWallet = self.get_var('location', 'wallet')
        dDate = ''.join([pad(self.get_var('date', x))
                         for x in ('day', 'month', 'year')])
        sType = self.get_var('miscellaneous', 'type_')

        if sMeta == sSeries:
            self.entry.pop('meta')
        else:
            self.entry['meta'] = sMeta

        def SEquals(sSeries, sEp):
            return sSeries == sEp or sSeries == sEp + ' (T)'

        if SEquals(sSeries, sEp):
            if nSeries:
                self.entry['series'] = nSeries
            else:
                self.entry.pop('series', None)
        else:
            if nSeries:
                self.entry['series'] = dict(name=sSeries, number=nSeries)
            else:
                self.entry['series'] = sSeries

        if sSeason:
            self.entry['season'] = dict(number=nSeason, name=sSeason)
        else:
            if nSeason:
                self.entry['season'] = nSeason
            else:
                self.entry.pop('season', None)

        if sMulti:
            self.entry['multi'] = sMulti
        elif nMulti:
            self.entry['multi'] = nMulti
        else:
            self.entry.pop('multi')

        if nEp:
            if sEpArt:
                self.entry['ep'] = dict(number=nEp, article=sEpArt, name=sEp)
            else:
                self.entry['ep'] = dict(number=nEp, name=sEp)
        else:
            if sEpArt:
                self.entry['ep'] = dict(article=sEpArt, name=sEp)
            else:
                self.entry['ep'] = sEp

        if nDisc:
            if sWallet:
                self.entry['location'] = dict(disc=nDisc, wallet=sWallet)
            else:
                self.entry['location'] = nDisc
        else:
            if sWallet:
                self.entry['location'] = sWallet
            else:
                self.entry.pop('location', None)

        if sType:
            self.entry['type'] = sType
        else:
            self.entry.pop('type', None)

        self.entry['date'] = dDate

    def get_var(self, lat, long_):
        return self.directory[lat][long_].get()


f = 'c:/users/ryan/tinellbianlanguages/toplevel/eplist.json'
g = ListEditor(f)
g.mainloop()
