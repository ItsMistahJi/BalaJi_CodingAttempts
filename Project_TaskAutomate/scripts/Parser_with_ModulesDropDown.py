import sys
import re
import tarfile
import zipfile
import os
import tempfile
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QTextEdit, QVBoxLayout, QFileDialog, QLabel, QLineEdit, QComboBox
)

class LogParserUI(QWidget):
    def __init__(self):
        super().__init__()
        self.module_log_mapping = {
            "TelcoVoiceManager": ["TELCOVOICEMANAGERLog.txt.0","TELCOVOICEMANAGERLog.txt.1","TELCOVOICEIFACEMGRLog.txt.0","VOICELog.txt","Consolelog.txt.0"],
            "InterDeviceManager": ["InterDeviceManagerLog.txt.0", "InterDeviceManagerLog.txt.1"],
            "Xupnp": ["xdevice.log", "xdiscovery.log", "xupnp.log"],
            "LEDManager": ["RDKLEDMANAGERLog.txt.0","RDKLEDMANAGERLog.txt.1"],
            "WiFiManager": ["wifiAnalytics.txt","wifiApps.txt","wifiBus.txt","wifiConnAdmissionCtrl.txt","wifiCtrl.txt","wifiDMCLI.txt","wifiDb.txt","wifiHal.txt","wifiMgr.txt","wifiMon.txt","wifiOcs.txt","wifiPsm.txt","wifiSM.txt","wifiWebConfig.txt","wifi_vendor_apps.log","wifi_vendor_csi.log","wifi_vendor_hal.log","wifihealth.txt","WiFilog.txt.0","WifiConsole.txt"],
            "WebPA": ["WEBPAlog.txt.0"],
            "WebConfig": ["WEBCONFIGlog.txt.0","Webconfig_default_rfc.txt.0"],
            "MESH": ["MeshAgentLog.txt.0","MeshServiceLog.txt.0","MeshServiceLog.txt.1","MeshBlackbox.log"],
            "GatewayManager": ["GATEWAYMANAGER","GATEWAYLOG.txt"],
            "AdvancedSecurity": ["ADVSEClog.txt.0"],
            "AKER": ["AKERlog.txt.0"],
            "EthernetAgent": ["ETHAGENTLog.txt.0"],
            "WANManager": ["WANMANAGERLog.txt.0"],
            "PPPMANAGER": ["PPPMANAGERLog.txt.0"],
            "VLANManager": ["VLANIFACEMGRLog.txt.0","VLANManagerLog.txt.0"],
            "XDNS": ["XDNSlog.txt.0"],
            "xDSLManager": ["XDSLMANAGERLog.txt.0","XDSLMANAGERLog.txt.1"],
            "JSONHALServerDSL": ["JSONHALSERVERDSLLog.txt.0"],
            "DibblerClient": ["dibbler_client_erouter0.log"],
            "DNSMasq": ["dnsmasq.log"],
            "RoutingDaemon": ["rtrouted.log"],
            "ARMConsole": ["ArmConsolelog.txt.0"],
            "BootTime": ["BootTime.log"],
            "CPUInfo": ["CPUInfo.txt.0"],
            "CrashReport": ["CRlog.txt.0"],
            "CoreDumps": ["core_log.txt"],
            "PerformanceMonitoring": ["perfmonstatus.log"],
            "SystemdProcessRestart": ["systemd_processRestart.log"],
            "PAM": ["PAMlog.txt.0"],
            "Parodus": ["PARODUSlog.txt.0"],
            "PSM": ["PSMlog.txt.0"],
            "SelfHealing": ["SelfHeal.txt.0","SelfHealAggressive.txt"],
            "GeneralAgent": ["agent.txt"],
            "AppArmor": ["apparmor.txt"],
            "BandSteering": ["bandsteering_periodic_status.txt"],
            "BBHM": ["bbhm_cur_cfg_before_psminit.xml"],
            "BridgeUtils": ["bridgeUtils.log"],
            "CAUpdate": ["caupdate.log"],
            "CertificateInfo": ["certinfo.txt"],
            "CurlMTLS": ["Curlmtlslog.txt.0"],
            "DNSInternetCheck": ["DNSInternetCheck.txt.0"],
            "FirewallDebug": ["FirewallDebug.txt"],
            "FirmwareUpgradeManager": ["FwUpgradeManagerLog.txt.0"],
            "Harvester": ["Harvesterlog.txt.0","Harvesterlog.txt.1"],
            "IHC": ["IHCLog.txt.0"],
            "ECFS": ["ecfs.txt"],
            "EthernetTelemetry": ["eth_telemetry.txt"],
            "LibCertifier": ["libcertifier.log"],
            "LighttpdError": ["lighttpderror.log"],
            "SystemMessages": ["messages.txt"],
            "NTP": ["ntpLog.log"],
            "OCSPSupport": ["ocsp-support.log"],
            "OVSMeshDebug": ["ovsMeshDebugLogs.txt"],
            "OVSDB": ["ovsdb.txt"],
            "RDKSSA": ["rdkssa.txt"],
            "RFCScript": ["rfcscript.log"],
            "Telemetry2.0": ["telemetry2_0.txt.0","telemetry2_0.txt.1"],
            "TLSError": ["tlsError.log"],
            "WebUI": ["webui.log","webuiupdate.log"],
            "XConf": ["xconf.txt.0"],
            "XfinityTestAgent": ["xfinityTestAgent.log"]
        }
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Log Parser")
        self.setGeometry(200, 200, 800, 600)

        self.label = QLabel("Select a log file (txt, tar, zip) to analyze:", self)
        self.browse_button = QPushButton("Browse File", self)
        self.search_input = QLineEdit(self)
        self.search_input.setPlaceholderText("Enter search term")
        self.search_button = QPushButton("Search", self)
        self.module_dropdown = QComboBox(self)
        self.module_dropdown.addItems(self.module_log_mapping.keys())
        self.module_search_button = QPushButton("Search by Module", self)
        self.result_area = QTextEdit(self)
        self.result_area.setReadOnly(True)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.browse_button)
        layout.addWidget(self.search_input)
        layout.addWidget(self.search_button)
        layout.addWidget(QLabel("Select Module:", self))
        layout.addWidget(self.module_dropdown)
        layout.addWidget(self.module_search_button)
        layout.addWidget(self.result_area)
        self.setLayout(layout)

        self.browse_button.clicked.connect(self.load_log_file)
        self.search_button.clicked.connect(self.search_logs)
        self.module_search_button.clicked.connect(self.search_by_module)
        
        self.log_content = ""

    def load_log_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Log File", "", "All Files (*);;Text Files (*.txt);;Archives (*.tar *.zip)")
        
        if file_path:
            if file_path.endswith((".tar", ".zip")):
                self.log_content = self.extract_logs_from_archive(file_path)
            else:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                    self.log_content = file.read()
            
            self.result_area.setText("Log file loaded successfully.")

    def extract_logs_from_archive(self, archive_path):
        extracted_text = ""
        temp_dir = tempfile.mkdtemp()
        
        if archive_path.endswith(".zip"):
            with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
        elif archive_path.endswith(".tar"):
            with tarfile.open(archive_path, 'r') as tar_ref:
                tar_ref.extractall(temp_dir)
        
        for root, _, files in os.walk(temp_dir):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        extracted_text += f.read() + "\n"
                except Exception as e:
                    print(f"Skipping file {file_path}: {e}")
        
        return extracted_text

    def parse_logs(self, log_content):
        extracted_logs = []
        pattern = r"(\d{6}-\d{2}:\d{2}:\d{2}\.\d+) \[mod=(.*?), lvl=(ERROR)\] \[tid=(\d+)\] (.*)"
        
        for line in log_content.split("\n"):
            match = re.search(pattern, line)
            if match:
                timestamp, module, level, tid, message = match.groups()
                extracted_logs.append({
                    "timestamp": timestamp,
                    "module": module,
                    "level": level,
                    "tid": tid,
                    "message": message
                })
        
        return extracted_logs

    def search_logs(self):
        search_term = self.search_input.text()
        if search_term and self.log_content:
            matching_lines = "\n".join([line for line in self.log_content.split("\n") if search_term in line])
            self.result_area.setText(matching_lines if matching_lines else "No matches found.")

    def search_by_module(self):
        selected_module = self.module_dropdown.currentText()
        relevant_files = self.module_log_mapping.get(selected_module, [])
        
        matching_lines = "\n".join(
            [line for line in self.log_content.split("\n") if any(log_file in line for log_file in relevant_files)]
        )
        
        parsed_logs = self.parse_logs(matching_lines)
        formatted_logs = "\n".join(
            [f"Timestamp: {log['timestamp']}, Module: {log['module']}, Level: {log['level']}, TID: {log['tid']}, Message: {log['message']}"
             for log in parsed_logs]
        )
        
        self.result_area.setText(formatted_logs if formatted_logs else "No relevant ERROR logs found for the selected module.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LogParserUI()
    window.show()
    sys.exit(app.exec_())