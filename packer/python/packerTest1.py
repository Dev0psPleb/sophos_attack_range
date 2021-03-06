from packerlicious import builder, provisioner, Template
template = Template()
template.add_builder(
    builder.vmware-iso(
        
    )
)


{
	"description": "Packer Windows Server 2016 build template file.",
	"_comment": "Template file provides framework for subsequent packer builds.",
	"variables": {
		"os-iso-path": "[nfsdatastore01] os/microsoft/server/2016/windows2016_noprompt.iso"
	},

	"builders": [
		{
			"type": "vsphere-iso",

			"vcenter_server": "{{user `vsphere-server`}}",
			"username": "{{user `vsphere-user`}}",
			"password": "{{user `vsphere-password`}}",
			"datacenter": "{{user `vsphere-datacenter`}}",
			"cluster": "{{user `vsphere-cluster`}}",
			"datastore": "{{user `vsphere-datastore`}}",
			"folder": "{{user `vsphere-folder`}}",
			"insecure_connection": "{{user `insecure-connection`}}",

			"communicator": "winrm",
			"winrm_username": "Administrator",
			"winrm_password": "packer",
			"winrm_timeout": "15m",

			"convert_to_template": "true",	

			"vm_name": "windows2016.gold",
			"guest_os_type": "windows9Server64Guest",
			
			"CPUs": 2,
			"RAM": 4096,
			"RAM_reserve_all": true,
			"firmware": "efi",
			"cdrom_type": "sata",

			"storage": [
				{
					"disk_size": 61440,
					"disk_thin_provisioned": true
				}
			],
			"disk_controller_type": "pvscsi",

			"network_adapters": [
				{
					"network": "{{user `vsphere-network`}}",
					"network_card": "vmxnet3"
				}
			],

			"notes": "{{user `vm-notes`}}",

			"iso_paths": [
				"{{user `os-iso-path`}}",
				"[] /vmimages/tools-isoimages/windows.iso"
			],

			"floppy_files": [
				"server_standard/autounattend.xml",
				"../drivers/pvscsi-win8/pvscsi.cat",
				"../drivers/pvscsi-win8/pvscsi.inf",
				"../drivers/pvscsi-win8/pvscsi.sys",
				"../drivers/pvscsi-win8/txtsetup.oem",
				"../scripts/2016/00-vmtools.ps1",
				"../scripts/2016/01-initialize.ps1",
				"../scripts/2016/03-systemsettings.ps1",
				"../scripts/2016/95-enablerdp.ps1"
			],

			"shutdown_command": "shutdown /f /s /t 10 /d p:4:1 /c \"Packer Complete\""
		}
	],
	"provisioners": [
		{
			"type": "powershell",
			"scripts": [
				"../scripts/2016/03-systemsettings.ps1",
				"../scripts/2016/95-enablerdp.ps1"
			]
		},
		{
			"type": "windows-restart",
			"restart_timeout": "30m"
		},
		{
			"type": "windows-update",
			"search_criteria": "IsInstalled=0",
			"filters": [
				"exclude:$_.Title -like '*Preview*'",
                "include:$true"
			]
		}
	]
}