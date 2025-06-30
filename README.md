# Huawei E3372 IP Address Changer

A Python script that uses browser automation to change the LAN IP address of Huawei E3372 4G LTE devices.

## ⚠️ Important Compatibility Notice

**Tested and Working On:**
- Model: **Huawei E3372h-607**
- Hardware Version: CL2E3372HM
- Software Version: 22.200.05.00.00
- Web UI Version: 17.100.11.00.03

**May Also Work On:**
- Other E3372h variants (E3372h-153, E3372h-320, etc.)
- Similar Huawei HiLink devices with web interface

**Will NOT Work On:**
- E3372s models (different hardware architecture)
- Devices in Stick/Modem mode (firmware 21.x)
- Devices with locked or restricted firmware

## ⚠️ Warning

**PLEASE READ BEFORE USING:**
1. **Device Access**: After IP change, your device will ONLY be accessible at the new IP address
2. **Connection Loss**: You will temporarily lose connection during the reboot
3. **Note Your Settings**: Write down the new IP address before proceeding
4. **Recovery**: If something goes wrong, you may need to factory reset your device
5. **Firmware Dependent**: Some firmware versions may not support IP changes via API

## Problem Solved
The Huawei E3372 web interface doesn't provide a direct option to change the device's LAN IP address through the UI. This script automates the process using Selenium WebDriver.

## Features
- Interactive prompt for custom IP configuration
- IP address validation
- Automatic browser control (Chrome/Firefox/Edge)
- JavaScript injection to modify device settings
- Fallback manual instructions if automation fails

## Requirements
```bash
pip install selenium
```

**Note**: Chrome, Firefox, or Edge browser must be installed on your system.

## Installation
```bash
git clone https://github.com/tibeemts/changeiphuaweiE3372h.git
cd huawei-e3372-ip-changer
pip install selenium
```

## Usage
```bash
python huawei_ip_changer.py
```

The script will:
1. Ask for your current device IP (default: 192.168.8.1)
2. Ask for your desired new IP address
3. Show configuration summary and ask for confirmation
4. Open browser and automatically change the IP
5. Device will reboot with the new IP address

## Example
```
Huawei E3372 IP Address Changer
==================================================

Enter current device IP (default: 192.168.8.1): 192.168.8.1

Examples of new IP: 192.168.18.1, 192.168.100.1, 10.0.0.1
Enter new device IP: 192.168.100.1

Configuration Summary:
Current IP: 192.168.8.1
New IP: 192.168.100.1
DHCP Range: 192.168.100.100 - 192.168.100.200
Subnet Mask: 255.255.255.0

Proceed with these settings? (y/n): y

Starting browser automation...
Opening device page...
Injecting JavaScript...
Result: <?xml version="1.0" encoding="UTF-8"?>
<response>OK</response>

✓ IP change command sent successfully!
Device will reboot. New address: http://192.168.100.1
```

## How It Works
1. Uses Selenium WebDriver to control a web browser
2. Navigates to the device's web interface
3. Injects JavaScript to obtain session tokens
4. Sends authenticated API request to change DHCP settings
5. Device automatically reboots with new IP

## Manual Method (If Automation Fails)
If the script doesn't work, you can try manually:

1. Open your device's web interface (http://192.168.8.1)
2. Press F12 to open Developer Tools
3. Go to the Console tab
4. Copy and paste the JavaScript command provided by the script
5. Press Enter

## Troubleshooting

### Script Fails to Run
- Make sure Chrome/Firefox/Edge is installed
- Install/update Selenium: `pip install --upgrade selenium`
- Run as administrator if needed

### IP Change Fails
- Check if you need to login to the device first
- Some firmware versions may not support IP changes
- Try the manual JavaScript method
- Device may be in Stick mode instead of HiLink mode

### Cannot Access Device After Change
- Make sure you're using the new IP address
- Check your network adapter settings
- Wait 60-90 seconds for full reboot
- Factory reset may be required (hold reset button 10+ seconds)

## Contributing
If you've tested this on other Huawei models, please open an issue or PR to update the compatibility list!

## License
MIT License - Use at your own risk

## Disclaimer
**USE AT YOUR OWN RISK**. This script modifies critical network settings on your device. The author is not responsible for any damage, data loss, or connectivity issues that may occur. Always ensure you have physical access to your device for recovery purposes.

## Credits
Created by [Your Name] - Tested on Huawei E3372h-607 in Laos 🇱🇦