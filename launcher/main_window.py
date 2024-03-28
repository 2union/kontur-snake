import tkinter as tk
from tkinter import ttk

from .runner import components_toggle
from leaders import leader_board, turncate_tables


class Launcher(ttk.Frame):
    def __init__(self, parent, settings):
        ttk.Frame.__init__(self)

        self.settings = settings

        # Make the app responsive
        for index in [0, 1, 2]:
            self.columnconfigure(index=index, weight=1)
            self.rowconfigure(index=index, weight=1)

        # Create value lists
        self.socket_variants_list = ["", "Unix", "Net4"]
        self.combo_list = ["Combobox", "Editable item 1", "Editable item 2"]
        self.players_count_list = ["2", "4"]

        # Create control variables
        self.var_0 = tk.BooleanVar()
        self.var_1 = tk.BooleanVar(value=True)
        self.var_2 = tk.BooleanVar()
        self.var_3 = tk.IntVar(value=2)
        self.socket_variant = tk.StringVar(value=self.socket_variants_list[1])
        self.var_5 = tk.DoubleVar(value=75.0)

        # Create widgets :)
        self.setup_widgets()

        self.socket_variant.trace('w', self.socket_change)

    def socket_change(self, *args):
        if self.socket_variant.get() == self.socket_variants_list[1]:
            self.ip_socket.destroy()
            self.ip_socket_port.destroy()
            self.set_unix_socket(self.socket_frame)
        else:
            self.unix_socket.destroy()
            self.set_net_socket(self.socket_frame)

    def refresh_data(self):
        for line in self.treeview.get_children():
            self.treeview.delete(line)

        # Define treeview data
        treeview_data = leader_board()

        # Insert treeview data
        for item in treeview_data:
            self.treeview.insert(
                parent=item[0], index=tk.END, iid=item[1], text=item[2], values=item[3]
            )

    def clear_data(self):
        turncate_tables()
        self.refresh_data()

    def setup_widgets(self):
        # Create a Frame for input widgets
        self.widgets_frame = ttk.Frame(self, padding=(0, 0, 0, 10))
        self.widgets_frame.grid(
            row=0, column=0, padx=10, pady=(30, 10), sticky="nsew", rowspan=3
        )
        self.widgets_frame.columnconfigure(index=0, weight=1)

        # Duration
        self.duration_label = ttk.Label(self.widgets_frame, text="Длительность(секунды)")
        self.duration_label.grid(row=0, column=0, padx=(5, 0), pady=(0, 10), sticky="ew")
        self.duration = ttk.Spinbox(self.widgets_frame, from_=40, to=300, increment=1)
        self.duration.insert(0, "120")
        self.duration.grid(row=1, column=0, padx=5, pady=10, sticky="ew")

        # Read-only combobox
        self.players_label = ttk.Label(self.widgets_frame, text="Количество игроков")
        self.players_label.grid(row=2, column=0, padx=(5, 0), pady=(20, 10), sticky="ew")
        self.players_count = ttk.Combobox(
            self.widgets_frame, state="readonly", values=self.players_count_list
        )
        self.players_count.current(0)
        self.players_count.grid(row=3, column=0, padx=5, pady=10, sticky="ew")

        # Separator
        self.separator_one = ttk.Separator(self.widgets_frame)
        self.separator_one.grid(row=4, column=0, padx=(20, 10), pady=10, sticky="ew")

        # Update user data
        self.updete_button = ttk.Button(self.widgets_frame, text="Обновить статистику",
                                        command=self.refresh_data)
        self.updete_button.grid(row=5, column=0, padx=5, pady=10, sticky="nsew")

        # Reset user date
        self.reset_button = ttk.Button(self.widgets_frame, text="Сбросить статистику",
                                       command=self.clear_data)
        self.reset_button.grid(row=6, column=0, padx=5, pady=10, sticky="nsew")

        # Separator
        self.separator_two = ttk.Separator(self.widgets_frame)
        self.separator_two.grid(row=7, column=0, padx=(20, 10), pady=10, sticky="ew")

        # Run game
        self.run = ttk.Checkbutton(
            self.widgets_frame, text="Играть", style="Toggle.TButton",
            command=components_toggle
        )
        self.run.grid(row=8, column=0, padx=5, pady=10, sticky="nsew")

        # Panedwindow
        self.paned = ttk.PanedWindow(self)
        self.paned.grid(row=0, column=2, pady=(25, 5), sticky="nsew", rowspan=3)

        # Pane #1
        self.pane_1 = ttk.Frame(self.paned, padding=5)
        self.paned.add(self.pane_1, weight=1)

        # Scrollbar
        self.scrollbar = ttk.Scrollbar(self.pane_1)
        self.scrollbar.pack(side="right", fill="y")

        # Treeview
        self.treeview = ttk.Treeview(
            self.pane_1,
            selectmode="browse",
            yscrollcommand=self.scrollbar.set,
            columns=("#1",),
            height=10,
        )
        self.treeview.pack(expand=True, fill="both")
        self.scrollbar.config(command=self.treeview.yview)

        # Treeview columns
        self.treeview.column("#0", anchor="w", width=240, stretch=True)
        self.treeview.column("#1", anchor="w", width=120, stretch=False)

        # Treeview headings
        self.treeview.heading("#0", text="Команда", anchor="center")
        self.treeview.heading("#1", text="Счёт", anchor="center")

        # Define treeview data
        treeview_data = leader_board()

        # Insert treeview data
        for item in treeview_data:
            self.treeview.insert(
                parent=item[0], index=tk.END, iid=item[1], text=item[2], values=item[3]
            )

        # Select and scroll
        self.treeview.selection_set(1)
        self.treeview.see(1)

        # Notebook, pane #2
        self.pane_2 = ttk.Frame(self.paned, padding=5)
        self.paned.add(self.pane_2, weight=3)

        # Notebook, pane #2
        self.notebook = ttk.Notebook(self.pane_2)
        self.notebook.pack(fill="both", expand=True)

        # Tab game settings
        self.game_settings = ttk.Frame(self.notebook)
        for index in [0, 1]:
            self.game_settings.columnconfigure(index=index, weight=1)
            self.game_settings.rowconfigure(index=index, weight=1)
        self.notebook.add(self.game_settings, text="Настройки игры")

        self.volume_label = ttk.Label(
            self.game_settings,
            text="Громкость",
            justify="left",
        )
        self.volume_label.grid(row=0, column=0, padx=(20, 0), pady=(10, 0), sticky="ew")

        # Volume
        self.volume = ttk.Scale(
            self.game_settings,
            from_=100,
            to=0,
            variable=self.var_5,
            # command=lambda event: self.var_5.set(self.scale.get()),
        )
        self.volume.grid(row=0, column=1, padx=(0, 10), pady=(10, 0), sticky="ew")

        self.video_frame = ttk.LabelFrame(self.game_settings, text="Экран", padding=(20, 10))
        self.video_frame.grid(row=1, column=0, padx=(20, 10), pady=10, sticky="nsew", columnspan=2)

        self.resolution_label = ttk.Label(
            self.video_frame,
            text="Размер окна",
            justify="left",
        )
        self.resolution_label.grid(row=0, column=0, padx=(6, 10), pady=(10, 0), sticky="ew")

        self.width = ttk.Entry(self.video_frame)
        self.width.insert(0, "640")
        self.width.grid(row=0, column=1, padx=10, pady=(10, 0), sticky="ew")

        self.resolution_label_x = ttk.Label(
            self.video_frame,
            text="x",
            justify="left",
        )
        self.resolution_label_x.grid(row=0, column=2, padx=(6, 10), pady=(10, 0), sticky="ew")

        self.height = ttk.Entry(self.video_frame)
        self.height.insert(0, "480")
        self.height.grid(row=0, column=3, padx=(10, 0), pady=(10, 0), sticky="ew")

        # Full screen
        self.full_screen = ttk.Checkbutton(
            self.video_frame, text="Полный экран", style="Switch.TCheckbutton"
        )
        self.full_screen.grid(row=2, column=0, padx=5, pady=10, sticky="nsew")

        # Tab network settings
        self.network_settings = ttk.Frame(self.notebook)
        for index in [0, 1]:
            self.network_settings.columnconfigure(index=index, weight=1)
            self.network_settings.rowconfigure(index=index, weight=1)
        self.notebook.add(self.network_settings, text="Настройки сети")

        # Socket
        self.socket_label = ttk.Label(
            self.network_settings,
            text="Socket settings",
        )
        self.socket_label.grid(row=0, column=0, padx=20, pady=(10, 0), sticky="ew")

        self.socket_type = ttk.OptionMenu(
            self.network_settings, self.socket_variant, *self.socket_variants_list
        )
        self.socket_type.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        self.socket_frame = ttk.LabelFrame(self.network_settings, text="Socket", padding=(20, 10))
        self.socket_frame.grid(row=2, column=0, padx=(20, 10), pady=10, sticky="nsew", columnspan=2)
        self.set_unix_socket(self.socket_frame)

        # Telegram token
        self.token_label = ttk.Label(
            self.network_settings,
            text="Telegram token",
        )
        self.token_label.grid(row=0, column=1, padx=20, pady=(10, 0), sticky="ew")

        self.token = ttk.Entry(self.network_settings)
        self.token.insert(0, "Telegram Token")
        self.token.config(show="*")
        self.token.grid(row=1, column=1, padx=20, pady=10, sticky="ew")

        # About
        self.about_program = ttk.Frame(self.notebook)
        self.notebook.add(self.about_program, text="О проекте")

        # Label
        self.daniil = ttk.Label(
            self.about_program,
            text="Эту змейку сделал Даня, он крутой!",
            justify="center",
            font=("-size", 15, "-weight", "bold"),
        )
        self.daniil.grid(row=0, column=0, pady=10, columnspan=2)

        # Sizegrip
        self.sizegrip = ttk.Sizegrip(self)
        self.sizegrip.grid(row=100, column=100, padx=(0, 5), pady=(0, 5))

    def set_unix_socket(self, root):
        self.unix_socket = ttk.Entry(root)
        self.unix_socket.insert(0, "/tmp/snake")
        self.unix_socket.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")

    def set_net_socket(self, root):
        self.ip_socket = ttk.Entry(root)
        self.ip_socket.insert(0, "127.0.0.1")
        self.ip_socket.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")

        self.ip_socket_port = ttk.Entry(root)
        self.ip_socket_port.insert(0, "8000")
        self.ip_socket_port.grid(row=0, column=1, padx=(10, 0), pady=0, sticky="nsew")
