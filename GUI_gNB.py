
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import os
import pty
import subprocess
import threading
import signal


class TerminalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("gNB command")
        self.root.geometry("1200x1100")  # Dimensione della finestra per adattarsi al contenuto
        self.root.resizable(False, True)

        # Creazione di un Canvas con scrollbar verticale
        self.canvas = tk.Canvas(root)
        self.scrollbar = tk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Posizionamento della scrollbar e del canvas
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Creazione di un frame interno al canvas
        self.inner_frame = tk.Frame(self.canvas)
        self.inner_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # Aggiungi il frame al canvas come una finestra
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")

        # Configurazione delle dimensioni di default per le colonne
        for col in range(6):
            root.columnconfigure(col, weight=1)

        # Titolo della sezione generale
        label_title_gnb = tk.Label(self.inner_frame, text="Informazioni gNB:", font=("Courier", 16, "bold"))
        label_title_gnb.grid(row=0, column=0, columnspan=6, pady=10, padx=10, sticky="w")

        # Frame per l'input del gnb_id e ran_node_name
        label_gnb_id = tk.Label(self.inner_frame, text="gnb_id:", font=("Courier", 12))
        label_gnb_id.grid(row=1, column=0, sticky="e")
        
        self.gnb_id_entry = tk.Entry(self.inner_frame, width=20, font=("Courier", 12))
        self.gnb_id_entry.grid(row=1, column=1, sticky="we")
        self.gnb_id_entry.insert(0, "411")

        label_ran_node_name = tk.Label(self.inner_frame, text="ran_node_name:", font=("Courier", 12))
        label_ran_node_name.grid(row=1, column=2, sticky="e")
        
        self.ran_node_name_entry = tk.Entry(self.inner_frame, width=20, font=("Courier", 12))
        self.ran_node_name_entry.grid(row=1, column=3, sticky="we")
        self.ran_node_name_entry.insert(0, "srsgnb01")

        label_COTSUE = tk.Label(self.inner_frame, text="COTS UE:", font=("Courier", 12))
        label_COTSUE.grid(row=1, column=4, sticky="e")

        self.COTSUE_var = tk.IntVar(value=0)  # Impostato su 0, che è equivalente a False
        self.COTSUE_button = tk.Checkbutton(self.inner_frame, text='', variable=self.COTSUE_var, onvalue=1, offvalue=0, font=("Courier", 12))
        self.COTSUE_button.grid(row=1, column=5, sticky="we")



        # Titolo della sezione AMF
        label_title_amf = tk.Label(self.inner_frame, text="AMF-RETE:", font=("Courier", 16, "bold"))
        label_title_amf.grid(row=2, column=0, columnspan=6, pady=10, padx=10, sticky="w")

        # Campi AMF
        label_bind_address = tk.Label(self.inner_frame, text="Bind address:", font=("Courier", 12))
        label_bind_address.grid(row=3, column=0, sticky="e")
        
        self.bind_address_entry = tk.Entry(self.inner_frame, width=20, font=("Courier", 12))
        self.bind_address_entry.grid(row=3, column=1, sticky="we")
        self.bind_address_entry.insert(0, "10.53.1.1")

        label_amf_address = tk.Label(self.inner_frame, text="AMF address:", font=("Courier", 12))
        label_amf_address.grid(row=3, column=2, sticky="e")
        
        self.amf_address_entry = tk.Entry(self.inner_frame, width=20, font=("Courier", 12))
        self.amf_address_entry.grid(row=3, column=3, sticky="we")
        self.amf_address_entry.insert(0, "10.53.1.2")

        label_port = tk.Label(self.inner_frame, text="Port:", font=("Courier", 12))
        label_port.grid(row=3, column=4, sticky="e")
        
        self.port_entry = tk.Entry(self.inner_frame, width=20, font=("Courier", 12))  # Uniformiamo la larghezza
        self.port_entry.grid(row=3, column=5, sticky="we")
        self.port_entry.insert(0, 38412)

        # Ulteriori campi AMF
        label_tac = tk.Label(self.inner_frame, text="Tac:", font=("Courier", 12))
        label_tac.grid(row=4, column=0, sticky="e")
        
        self.tac_entry = tk.Entry(self.inner_frame, width=20, font=("Courier", 12))  # Uniformiamo la larghezza
        self.tac_entry.grid(row=4, column=1, sticky="we")
        self.tac_entry.insert(0, 7)

        label_plmn = tk.Label(self.inner_frame, text="Plmn:", font=("Courier", 12))
        label_plmn.grid(row=4, column=2, sticky="e")
        
        self.plmn_entry = tk.Entry(self.inner_frame, width=20, font=("Courier", 12))
        self.plmn_entry.grid(row=4, column=3, sticky="we")
        self.plmn_entry.insert(0, "00101")

        label_sst = tk.Label(self.inner_frame, text="sst:", font=("Courier", 12))
        label_sst.grid(row=4, column=4, sticky="e")
        
        self.sst_entry = tk.Entry(self.inner_frame, width=20, font=("Courier", 12))  # Uniformiamo la larghezza
        self.sst_entry.grid(row=4, column=5, sticky="we")
        self.sst_entry.insert(0, 1)

        label_cell_config = tk.Label(self.inner_frame, text="Cell config:", font=("Courier", 16, "bold"))
        label_cell_config.grid(row=5, column=0, columnspan=6, pady=10, padx=10, sticky="w")

        label_pci = tk.Label(self.inner_frame, text="pci:", font=("Courier", 12))
        label_pci.grid(row=6, column=0, sticky="e")

        self.pci_entry = tk.Entry(self.inner_frame, width=20, font=("Courier", 12))
        self.pci_entry.grid(row=6, column=1, sticky="we")
        self.pci_entry.insert(0, 1)
        
        label_dl_arfcn = tk.Label(self.inner_frame, text="dl_arfcn:", font=("Courier", 12))
        label_dl_arfcn.grid(row=6, column=2, sticky="e")

        self.dl_arfcn_entry = tk.Entry(self.inner_frame, width=20, font=("Courier", 12))
        self.dl_arfcn_entry.grid(row=6, column=3, sticky="we")
        self.dl_arfcn_entry.insert(0, 368500)

        label_band = tk.Label(self.inner_frame, text="band:", font=("Courier", 12))
        label_band.grid(row=6, column=4, sticky="e")

        self.band_entry = tk.Entry(self.inner_frame, width=20, font=("Courier", 12))
        self.band_entry.grid(row=6, column=5, sticky="we")
        self.band_entry.insert(0, 3)

        label_common_scs = tk.Label(self.inner_frame, text="common_scs:", font=("Courier", 12))
        label_common_scs.grid(row=7, column=0, sticky="e")

        self.common_scs_entry = tk.Entry(self.inner_frame, width=20, font=("Courier", 12))
        self.common_scs_entry.grid(row=7, column=1, sticky="we")
        self.common_scs_entry.insert(0, 15)

        label_channel_bandwidth_MHz = tk.Label(self.inner_frame, text="BW_MHz:", font=("Courier", 12))
        label_channel_bandwidth_MHz.grid(row=7, column=2, sticky="e")

        self.channel_bandwidth_MHz_entry = tk.Entry(self.inner_frame, width=20, font=("Courier", 12))
        self.channel_bandwidth_MHz_entry.grid(row=7, column=3, sticky="we")
        self.channel_bandwidth_MHz_entry.insert(0, 20)

        label_nof_antennas_dl = tk.Label(self.inner_frame, text="antennas_dl:", font=("Courier", 12))
        label_nof_antennas_dl.grid(row=7, column=4, sticky="e")

        self.nof_antennas_dl_entry = tk.Entry(self.inner_frame, width=20, font=("Courier", 12))
        self.nof_antennas_dl_entry.grid(row=7, column=5, sticky="we")
        self.nof_antennas_dl_entry.insert(0, 1)

        label_nof_antennas_ul = tk.Label(self.inner_frame, text="antennas_ul:", font=("Courier", 12))
        label_nof_antennas_ul.grid(row=8, column=0, sticky="e")

        self.nof_antennas_ul_entry = tk.Entry(self.inner_frame, width=20, font=("Courier", 12))
        self.nof_antennas_ul_entry.grid(row=8, column=1, sticky="we")
        self.nof_antennas_ul_entry.insert(0, 1)

        label_tac = tk.Label(self.inner_frame, text="Tac:", font=("Courier", 12))
        label_tac.grid(row=8, column=2, sticky="e")

        self.tac_entry1 = tk.Entry(self.inner_frame, width=20, font=("Courier", 12))
        self.tac_entry1.grid(row=8, column=3, sticky="we")
        self.tac_entry1.insert(0, 7)

        label_plmn1 = tk.Label(self.inner_frame, text="Plmn:", font=("Courier", 12))
        label_plmn1.grid(row=8, column=4, sticky="e")

        self.plmn1_entry = tk.Entry(self.inner_frame, width=20, font=("Courier", 12))
        self.plmn1_entry.grid(row=8, column=5, sticky="we")
        self.plmn1_entry.insert(0, "00101")

        label_title_RV_FRONTEND = tk.Label(self.inner_frame, text="RV_FRONTEND:", font=("Courier", 16, "bold"))
        label_title_RV_FRONTEND.grid(row=9, column=0, columnspan=6, pady=10, padx=10, sticky="w")

        label_device_driver = tk.Label(self.inner_frame, text="device_driver:", font=("Courier", 12))
        label_device_driver.grid(row=10, column=0, sticky="e")

        self.device_driver_entry = tk.Entry(self.inner_frame, width=20, font=("Courier", 12))
        self.device_driver_entry.grid(row=10, column=1, sticky="we")
        self.device_driver_entry.insert(0, "zmq")

        label_device_args = tk.Label(self.inner_frame, text="device_args:", font=("Courier", 12))
        label_device_args.grid(row=10, column=2, sticky="e")

        self.device_args_entry = tk.Entry(self.inner_frame, width=20, font=("Courier", 12))
        self.device_args_entry.grid(row=10, column=3, sticky="we")
        self.device_args_entry.insert(0, "tx_port=tcp://127.0.0.1:2000,rx_port=tcp://127.0.0.1:2001,base_srate=23.04e6")

        label_tx_gain = tk.Label(self.inner_frame, text="tx_gain:", font=("Courier", 12))
        label_tx_gain.grid(row=10, column=4, sticky="e")

        self.tx_gain_entry = tk.Entry(self.inner_frame, width=20, font=("Courier", 12))
        self.tx_gain_entry.grid(row=10, column=5, sticky="we")
        self.tx_gain_entry.insert(0, 50)

        label_rx_gain = tk.Label(self.inner_frame, text="rx_gain:", font=("Courier", 12))
        label_rx_gain.grid(row=11, column=0, sticky="e")

        self.rx_gain_entry = tk.Entry(self.inner_frame, width=20, font=("Courier", 12))
        self.rx_gain_entry.grid(row=11, column=1, sticky="we")
        self.rx_gain_entry.insert(0, 60)

        label_clock = tk.Label(self.inner_frame, text="clock:", font=("Courier", 12))
        label_clock.grid(row=11, column=2, sticky="e")

        self.clock_entry = tk.Entry(self.inner_frame, width=20, font=("Courier", 12))
        self.clock_entry.grid(row=11, column=3, sticky="we")
        self.clock_entry.insert(0, "default")

        label_sync = tk.Label(self.inner_frame, text="sync:", font=("Courier", 12))
        label_sync.grid(row=11, column=4, sticky="e")

        self.sync_entry = tk.Entry(self.inner_frame, width=20, font=("Courier", 12))
        self.sync_entry.grid(row=11, column=5, sticky="we")
        self.sync_entry.insert(0, "default")

        label_otw_format = tk.Label(self.inner_frame, text="otw_format:", font=("Courier", 12))
        label_otw_format.grid(row=12, column=0, sticky="e")

        self.otw_format_entry = tk.Entry(self.inner_frame, width=20, font=("Courier", 12))
        self.otw_format_entry.grid(row=12, column=1, sticky="we")
        self.otw_format_entry.insert(0, "default")

        label_title_PCAP = tk.Label(self.inner_frame, text="PCAP:", font=("Courier", 16, "bold"))
        label_title_PCAP.grid(row=13, column=0, columnspan=6, pady=10, padx=10, sticky="w")

        label_mac_filename = tk.Label(self.inner_frame, text="mac_filname:", font=("Courier", 12))
        label_mac_filename.grid(row=14, column=0, sticky="e")

        self.mac_filename_entry = tk.Entry(self.inner_frame, width=20, font=("Courier", 12))
        self.mac_filename_entry.grid(row=14, column=1, sticky="e")
        self.mac_filename_entry.insert(0, "/tmp/gnb_mac.pcap")

        
        label_mac_enable = tk.Label(self.inner_frame, text="mac_enable:", font=("Courier", 12))
        label_mac_enable.grid(row=14, column=2, sticky="e")

        self.mac_enable_var = tk.IntVar(value=0)  # Impostato su 0, che è equivalente a False
        self.mac_enable_button = tk.Checkbutton(self.inner_frame, text='', variable=self.mac_enable_var, onvalue=1, offvalue=0, font=("Courier", 12))
        self.mac_enable_button.grid(row=14, column=3, sticky="we")

        
        label_ngap_filename = tk.Label(self.inner_frame, text="ngap_filename:", font=("Courier", 12))
        label_ngap_filename.grid(row=14, column=4, sticky="e")

        self.ngap_filename_entry = tk.Entry(self.inner_frame, width=20, font=("Courier", 12))
        self.ngap_filename_entry.grid(row=14, column=5, sticky="we")
        self.ngap_filename_entry.insert(0, "/tmp/gnb_ngap.pcap")

        label_ngap_enable = tk.Label(self.inner_frame, text="ngap_enable:", font=("Courier", 12))
        label_ngap_enable.grid(row=15, column=0, sticky="e")

        # Usa una variabile Tkinter IntVar per tenere traccia dello stato del Checkbutton
        self.ngap_enable_var = tk.IntVar(value=0)  # Impostato su 0, che è equivalente a False
        self.ngap_enable_button = tk.Checkbutton(self.inner_frame, text='', variable=self.ngap_enable_var, onvalue=1, offvalue=0, font=("Courier", 12))
        self.ngap_enable_button.grid(row=15, column=1, sticky="we")

        label_title_Metrics = tk.Label(self.inner_frame, text="Metrics:", font=("Courier", 16, "bold"))
        label_title_Metrics.grid(row=16, column=0, columnspan=6, pady=10, padx=10, sticky="w")

        label_addr1 = tk.Label(self.inner_frame, text="addr:", font=("Courier", 12))
        label_addr1.grid(row=17, column=0, sticky="e")

        self.addr1_entry = tk.Entry(self.inner_frame, width=20, font=("Courier", 12))
        self.addr1_entry.grid(row=17, column=1, sticky="we")
        self.addr1_entry.insert(0, "127.0.0.1")

        label_port1 = tk.Label(self.inner_frame, text="port:", font=("Courier", 12))
        label_port1.grid(row=17, column=2, sticky="e")

        self.port1_entry = tk.Entry(self.inner_frame, width=20, font=("Courier", 12))
        self.port1_entry.grid(row=17, column=3, sticky="we")
        self.port1_entry.insert(0, 55555)

        # Aggiungi campi per cu_cp_statistics_report_period
        label_cu_cp_statistics_report_period = tk.Label(self.inner_frame, text="cu_cp:", font=("Courier", 12))
        label_cu_cp_statistics_report_period.grid(row=17, column=4, sticky="e")

        self.cu_cp_statistics_report_period_entry = tk.Entry(self.inner_frame, width=20, font=("Courier", 12))
        self.cu_cp_statistics_report_period_entry.grid(row=17, column=5, sticky="we")
        self.cu_cp_statistics_report_period_entry.insert(0, 1)

        # Aggiungi campi per cu_up_statistics_report_period
        label_cu_up_statistics_report_period = tk.Label(self.inner_frame, text="cu_up:", font=("Courier", 12))
        label_cu_up_statistics_report_period.grid(row=18, column=0, sticky="e")

        self.cu_up_statistics_report_period_entry = tk.Entry(self.inner_frame, width=20, font=("Courier", 12))
        self.cu_up_statistics_report_period_entry.grid(row=18, column=1, sticky="we")
        self.cu_up_statistics_report_period_entry.insert(0, 1)

        # Aggiungi campi per pdcp_report_period
        label_pdcp_report_period = tk.Label(self.inner_frame, text="pdcp_report_period:", font=("Courier", 12))
        label_pdcp_report_period.grid(row=18, column=2, sticky="e")

        self.pdcp_report_period_entry = tk.Entry(self.inner_frame, width=20, font=("Courier", 12))
        self.pdcp_report_period_entry.grid(row=18, column=3, sticky="e")
        self.pdcp_report_period_entry.insert(0, 0)

        # Aggiungi campi per rlc_report_period
        label_rlc_report_period = tk.Label(self.inner_frame, text="rlc_report_period:", font=("Courier", 12))
        label_rlc_report_period.grid(row=18, column=4, sticky="we")

        self.rlc_report_period_entry = tk.Entry(self.inner_frame, width=20, font=("Courier", 12))
        self.rlc_report_period_entry.grid(row=18, column=5, sticky="we")
        self.rlc_report_period_entry.insert(0, 1000)

        # Aggiungi campi per rlc_json_enable
        label_rlc_json_enable = tk.Label(self.inner_frame, text="rlc_json_enable:", font=("Courier", 12))
        label_rlc_json_enable.grid(row=19, column=0, sticky="e")

        self.rlc_json_enable_var = tk.IntVar(value=0)  # Impostato su 0, che è equivalente a False
        self.rlc_json_enable_button = tk.Checkbutton(self.inner_frame, text='', variable=self.rlc_json_enable_var, onvalue=1, offvalue=0, font=("Courier", 12))
        self.rlc_json_enable_button.grid(row=19, column=1, sticky="we")

        # Aggiungi campi per enable_json_metrics
        label_enable_json_metrics = tk.Label(self.inner_frame, text="enable_json_metrics:", font=("Courier", 12))
        label_enable_json_metrics.grid(row=19, column=2, sticky="e")

        self.enable_json_metrics_var = tk.IntVar(value=0)  # Impostato su 0, che è equivalente a False
        self.enable_json_metrics_button = tk.Checkbutton(self.inner_frame, text='', variable=self.enable_json_metrics_var, onvalue=1, offvalue=0, font=("Courier", 12))
        self.enable_json_metrics_button.grid(row=19, column=3, sticky="we")



        # Frame per i pulsanti Start e Stop, con dimensioni ridotte
        button_frame = tk.Frame(self.inner_frame)
        button_frame.grid(row=20, column=1, columnspan=4, pady=10, padx=10, sticky="ew")

        self.start_button = tk.Button(button_frame, text="Start",  command=self.start_command, font=("Courier", 12), width=15)
        self.start_button.pack(side=tk.LEFT, padx=50, expand=True)  # Spaziatura aumentata

        self.stop_button = tk.Button(button_frame, text="Stop", command=self.stop_command, font=("Courier", 12), width=15)
        self.stop_button.pack(side=tk.LEFT, padx=50, expand=True)  # Spaziatura aumentata

        self.t_button = tk.Button(button_frame, text="T", command=self.send_t, font=("Courier", 12))
        self.t_button.pack(side=tk.RIGHT, padx=10, expand=True)


        # Area di output
        self.output_area = ScrolledText(self.inner_frame, wrap=tk.WORD, height=15, width=70, font=("Courier", 10))
        self.output_area.grid(row=21, column=0, columnspan=6, padx=10, pady=10, sticky="ew")
        self.output_area.config(state=tk.DISABLED)

        


        self.current_directory = os.path.expanduser("~")
        os.chdir(self.current_directory)
        self.process = None
        self.master_fd = None
        self.stopping = False

        self.append_output(f"{self.current_directory}$ ")
        self.read_output_enabled = True

        self.gnb_zmq_path = None
        self.gnb_COTSUE_path = None
        self.gnb_zmq_yaml_path = None
        self.gnb_COTSUE_yaml_path = None

        # Trova i file necessari all'avvio
        self.find_file_paths()

    
    def find_file_paths(self):
        """Trova i percorsi dei file necessari per i comandi."""
        try:
            # Comando per trovare il file gnb_zmq.yaml in tutto il filesystem
            find_gnb_zmq = "find / -name 'gnb_zmq' 2>/dev/null"
            result_gnb_zmq = subprocess.run(find_gnb_zmq, shell=True, stdout=subprocess.PIPE, text=True)
            self.gnb_zmq_path = result_gnb_zmq.stdout.strip()  # Memorizza il percorso trovato

            # Comando per trovare il file gnb_COTSUE.yml in tutto il filesystem
            find_gnb_COTSUE = "find / -name 'gnb_COTSUE' 2>/dev/null"
            result_gnb_COTSUE = subprocess.run(find_gnb_COTSUE, shell=True, stdout=subprocess.PIPE, text=True)
            self.gnb_COTSUE_path = result_gnb_COTSUE.stdout.strip()  # Memorizza il percorso trovato

            find_gnb_zmq_yaml = "find / -name 'gnb_zmq.yaml' 2>/dev/null"
            result_gnb_zmq_yaml = subprocess.run(find_gnb_zmq_yaml, shell=True, stdout=subprocess.PIPE, text=True)
            self.gnb_zmq_yaml_path = result_gnb_zmq_yaml.stdout.strip()

            find_gnb_COTSUE_yaml = "find / -name 'gnb_COTSUE.yaml' 2>/dev/null"
            result_gnb_COTSUE_yaml = subprocess.run(find_gnb_COTSUE_yaml, shell=True, stdout=subprocess.PIPE, text=True)
            self.gnb_COTSUE_yaml_path = result_gnb_COTSUE_yaml.stdout.strip()

            # Debug: mostra i percorsi trovati
            self.append_output(f"\nPercorso gnb_zmq trovato: {self.gnb_zmq_path}\n")
            self.append_output(f"Percorso gnb_COTSUE trovato: {self.gnb_COTSUE_path}\n")
            self.append_output(f"Percorso gnb_zmq.yaml trovato: {self.gnb_zmq_yaml_path}\n")
            self.append_output(f"Percorso gnb_COTSUE.yaml trovato: {self.gnb_COTSUE_yaml_path}\n")

        except Exception as e:
            self.append_output(f"Errore durante la ricerca dei file: {str(e)}\n")

        

    def start_command(self):
        bind_address = self.bind_address_entry.get()
        amf_address = self.amf_address_entry.get()
        gnb_id = self.gnb_id_entry.get()
        ran_node_name = self.ran_node_name_entry.get()
        port = self.port_entry.get()
        tac = self.tac_entry.get()
        plmn = self.plmn_entry.get()
        sst = self.sst_entry.get()
        pci =self.pci_entry.get()
        dl_arfcn = self.dl_arfcn_entry.get()
        band = self.band_entry.get()
        common_scs = self.common_scs_entry.get()
        channel_bandwidth_Mz = self.channel_bandwidth_MHz_entry.get()
        nof_antennas_dl = self.nof_antennas_dl_entry.get()
        nof_antennas_ul = self.nof_antennas_ul_entry.get()
        tac1 = self.tac_entry1.get()
        plmn1 = self.plmn1_entry.get()
        device_driver = self.device_driver_entry.get()
        device_args = self.device_args_entry.get()
        tx_gain = self.tx_gain_entry.get()
        rx_gain = self.rx_gain_entry.get()
        clock = self.clock_entry.get()
        sync = self.sync_entry.get()
        otw_format = self.otw_format_entry.get()
        mac_filename = self.mac_filename_entry.get()
        mac_enable = self.mac_enable_var.get()
        ngap_filename = self.ngap_filename_entry.get()
        ngap_enable = self.ngap_enable_var.get()
        addr1 = self.addr1_entry.get()
        port1 = self.port1_entry.get()
        cu_cp_statistics_report_period = self.cu_cp_statistics_report_period_entry.get()
        cu_up_statistics_report_period = self.cu_up_statistics_report_period_entry.get()
        pdcp_report_period = self.pdcp_report_period_entry.get()
        rlc_json_enable = self.rlc_json_enable_var.get()
        enable_json_metrics = self.enable_json_metrics_var.get()

        self.read_output_enabled = False

        sed_command = f"sed -e 's/TAC/{tac}/g' -e 's/PLMN/\"{plmn}\"/g' -e 's/SST/{sst}/g' {self.gnb_zmq_path} > {self.gnb_zmq_yaml_path}"
        sed_command2 = f"sed -e 's/TAC/{tac}/g' -e 's/PLMN/\"{plmn}\"/g' -e 's/SST/{sst}/g' {self.gnb_COTSUE_path} > {self.gnb_COTSUE_yaml_path}"
        

        self.read_output_enabled = True
        command = f"sudo -S gnb -c {self.gnb_zmq_yaml_path} --gnb_id={gnb_id} --ran_node_name={ran_node_name} cu_cp amf --bind_addr={bind_address} --addr={amf_address} --port={port} cell_cfg --pci={pci} --dl_arfcn={dl_arfcn} --band={band} --common_scs={common_scs} --channel_bandwidth_MHz={channel_bandwidth_Mz} --nof_antennas_dl={nof_antennas_dl} --nof_antennas_ul={nof_antennas_ul} --tac={tac1} --plmn={plmn1} ru_sdr --device_driver={device_driver} --tx_gain={tx_gain} --rx_gain={rx_gain} --clock={clock} --sync={sync} --otw_format={otw_format} --device_args={device_args} pcap --mac_filename={mac_filename} --mac_enable={mac_enable} --ngap_filename= {ngap_filename} --ngap_enable={ngap_enable} metrics --addr={addr1} --port={port1} --cu_cp_statistics_report_period={cu_cp_statistics_report_period} --cu_up_statistics_report_period={cu_up_statistics_report_period} --pdcp_report_period={pdcp_report_period} --rlc_json_enable={rlc_json_enable} --enable_json_metrics={enable_json_metrics}"
        command2 = f"sudo -S gnb -c {self.gnb_COTSUE_yaml_path} --gnb_id={gnb_id} --ran_node_name={ran_node_name} cu_cp amf --bind_addr={bind_address} --addr={amf_address} --port={port} cell_cfg --pci={pci} --dl_arfcn={dl_arfcn} --band={band} --common_scs={common_scs} --channel_bandwidth_MHz={channel_bandwidth_Mz} --nof_antennas_dl={nof_antennas_dl} --nof_antennas_ul={nof_antennas_ul} --tac={tac1} --plmn={plmn1} ru_sdr --device_driver={device_driver} --tx_gain={tx_gain} --rx_gain={rx_gain} --clock={clock} --sync={sync} --otw_format={otw_format} --device_args={device_args} pcap --mac_filename={mac_filename} --mac_enable={mac_enable} --ngap_filename= {ngap_filename} --ngap_enable={ngap_enable} metrics --addr={addr1} --port={port1} --cu_cp_statistics_report_period={cu_cp_statistics_report_period} --cu_up_statistics_report_period={cu_up_statistics_report_period} --pdcp_report_period={pdcp_report_period} --rlc_json_enable={rlc_json_enable} --enable_json_metrics={enable_json_metrics}"
        
        if self.COTSUE_var.get() == 0:  
            self.read_output_enabled = False
            self.run_command(sed_command)
            self.read_output_enabled = True
            self.run_command(command)

        else:  # Se è True (onvalue=1)
            self.read_output_enabled = False
            self.run_command(sed_command2)
            self.read_output_enabled = True
            self.run_command(command2)
            

        self.stopping = False


    def run_command(self, command):
        try:
            self.master_fd, slave_fd = pty.openpty()
            self.process = subprocess.Popen(
                command,
                shell=True,
                cwd=self.current_directory,
                stdin=slave_fd,
                stdout=slave_fd,
                stderr=slave_fd,
                preexec_fn=os.setsid
            )
            os.close(slave_fd)
            threading.Thread(target=self.read_output_from_fd, daemon=True).start()
        except Exception as e:
            self.append_output(f"Errore nell'avvio del processo: {str(e)}\n")
            if self.master_fd:
                os.close(self.master_fd)
            if self.process:
                self.process.terminate()

    def read_output_from_fd(self):
        try:
            while True:
                if not self.read_output_enabled:
                    break
                output = os.read(self.master_fd, 1024).decode("utf-8")
                if "password for" in output:
                    self.request_sudo_password()
                if not output or self.stopping:
                    break
                self.append_output_safe(output)
        except Exception as e:
            self.append_output_safe(f" \n")

    def request_sudo_password(self):
        def on_submit():
            password = password_entry.get()
            password_window.destroy()
            os.write(self.master_fd, f"{password}\n".encode())

        password_window = tk.Toplevel(self.root)
        password_window.title("Password Sudo")
        tk.Label(password_window, text="Inserisci la password per sudo:").pack(pady=5)
        password_entry = tk.Entry(password_window, show="*", font=("Courier", 12))
        password_entry.pack(pady=5, padx=10, fill=tk.X)
        tk.Button(password_window, text="Invia", command=on_submit).pack(pady=10)

    def send_t(self):
        if self.process and self.process.poll() is None:  # Verifica che il processo sia attivo
            try:
                os.write(self.master_fd, b't\n')  # Invia 't' al terminale del processo
            except Exception as e:
                self.append_output_safe(f"Errore durante l'invio di 't': {str(e)}\n")
        else:
            self.append_output_safe("Il processo non è attivo.\n")

    def stop_command(self):
        self.stopping = True
        if self.process is not None and self.process.poll() is None:
            try:
                os.killpg(os.getpgid(self.process.pid), signal.SIGINT)
                self.process.wait()
            except Exception as e:
                self.append_output_safe(f"Errore durante l'arresto: {str(e)}\n")
            finally:
                self.append_output_safe("Processo Terminato.\n")
                if self.master_fd:
                    os.close(self.master_fd)
                self.process = None
                self.master_fd = None

    def append_output(self, text):
        self.output_area.config(state=tk.NORMAL)
        self.output_area.insert(tk.END, text)
        self.output_area.see(tk.END)
        self.output_area.config(state=tk.DISABLED)

    def append_output_safe(self, text):
        if self.root:
            self.root.after(0, lambda: self.append_output(text))

if __name__ == "__main__":
    root = tk.Tk()
    app = TerminalApp(root)
    root.mainloop()