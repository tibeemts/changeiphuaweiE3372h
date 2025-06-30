#!/usr/bin/env python3
"""
Huawei E3372 IP Address Changer
Automates browser to change device IP address using Selenium
"""
import time
import os
import sys
import re

def install_selenium():
    """Install selenium if not present"""
    try:
        import selenium
    except ImportError:
        print("Installing selenium...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "selenium"])

def validate_ip(ip_address):
    """Validate IP address format"""
    pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
    if not re.match(pattern, ip_address):
        return False
    
    # Check each octet is valid (0-255)
    octets = ip_address.split('.')
    for octet in octets:
        if int(octet) > 255:
            return False
    return True

def get_user_input():
    """Get IP addresses from user"""
    print("Huawei E3372 IP Address Changer")
    print("=" * 50)
    print()
    
    # Get current IP
    current_ip = input("Enter current device IP (default: 192.168.8.1): ").strip()
    if not current_ip:
        current_ip = "192.168.8.1"
    
    if not validate_ip(current_ip):
        print("Invalid IP format!")
        return None, None
    
    # Get new IP
    print("\nExamples of new IP: 192.168.18.1, 192.168.100.1, 10.0.0.1")
    new_ip = input("Enter new device IP: ").strip()
    
    if not new_ip:
        print("New IP is required!")
        return None, None
    
    if not validate_ip(new_ip):
        print("Invalid IP format!")
        return None, None
    
    # Confirm changes
    ip_parts = new_ip.split('.')
    network = '.'.join(ip_parts[:3])
    
    print(f"\nConfiguration Summary:")
    print(f"Current IP: {current_ip}")
    print(f"New IP: {new_ip}")
    print(f"DHCP Range: {network}.100 - {network}.200")
    print(f"Subnet Mask: 255.255.255.0")
    
    confirm = input("\nProceed with these settings? (y/n): ").lower()
    if confirm != 'y':
        print("Cancelled.")
        return None, None
    
    return current_ip, new_ip

def main():
    install_selenium()
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import TimeoutException
    
    # Get user input
    current_ip, new_ip = get_user_input()
    if not current_ip or not new_ip:
        return
    
    # Extract network parts for DHCP range
    ip_parts = new_ip.split('.')
    network = '.'.join(ip_parts[:3])
    print("\nStarting browser automation...")
    
    # JavaScript template with placeholders
    js_code = f"""
    // Get session token
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/api/webserver/SesTokInfo', false);
    xhr.send();
    var response = xhr.responseText;
    var sessionId = response.match(/SessionID=([^<]+)/)[1];
    var token = response.match(/TokInfo>([^<]+)/)[1];
    
    // Set session cookie
    document.cookie = 'SessionID=' + sessionId;
    
    // Send IP change request
    var xhr2 = new XMLHttpRequest();
    xhr2.open('POST', '/api/dhcp/settings', false);
    xhr2.setRequestHeader('__RequestVerificationToken', token);
    xhr2.setRequestHeader('Content-Type', 'text/xml');
    
    var data = '<?xml version="1.0" encoding="UTF-8"?>' +
        '<request>' +
        '<DhcpIPAddress>{new_ip}</DhcpIPAddress>' +
        '<DhcpLanNetmask>255.255.255.0</DhcpLanNetmask>' +
        '<DhcpStatus>1</DhcpStatus>' +
        '<DhcpStartIPAddress>{network}.100</DhcpStartIPAddress>' +
        '<DhcpEndIPAddress>{network}.200</DhcpEndIPAddress>' +
        '<DhcpLeaseTime>86400</DhcpLeaseTime>' +
        '<DnsStatus>1</DnsStatus>' +
        '<PrimaryDns>8.8.8.8</PrimaryDns>' +
        '<SecondaryDns>8.8.4.4</SecondaryDns>' +
        '</request>';
    
    xhr2.send(data);
    return xhr2.responseText;
    """
    
    # Try multiple browsers
    browsers = [
        ("Chrome", webdriver.Chrome),
        ("Firefox", webdriver.Firefox),
        ("Edge", webdriver.Edge)
    ]
    
    for browser_name, browser_class in browsers:
        try:
            print(f"\nTrying with {browser_name}...")
            
            # Set up browser options
            if browser_name == "Chrome":
                options = webdriver.ChromeOptions()
                options.add_argument('--disable-blink-features=AutomationControlled')
                options.add_experimental_option("excludeSwitches", ["enable-automation"])
                options.add_experimental_option('useAutomationExtension', False)
                driver = browser_class(options=options)
            else:
                driver = browser_class()
            
            print("Opening device page...")
            driver.get(f"http://{current_ip}")
            
            # Wait for page to load
            time.sleep(3)
            
            # Try to find and click login if needed
            try:
                login_button = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.ID, "login"))
                )
                print("Login page detected - you may need to login manually")
                input("Press Enter after logging in...")
            except TimeoutException:
                pass
            
            print("Injecting JavaScript...")
            result = driver.execute_script(js_code)
            print(f"Result: {result}")
            
            if "error" not in str(result).lower():
                print("\n✓ IP change command sent successfully!")
                print(f"Device will reboot. New address: http://{new_ip}")
                
                # Try alternative injection methods
                print("\nTrying alternative injection methods...")
                
                # Method 2: Direct API manipulation
                driver.execute_script(f"""
                    // Try to access internal functions
                    if (typeof EMUI !== 'undefined' && EMUI.api) {{
                        EMUI.api.dhcp.setSettings({{
                            DhcpIPAddress: '{new_ip}',
                            DhcpLanNetmask: '255.255.255.0'
                        }});
                    }}
                """)
                
                # Method 3: Form manipulation
                driver.execute_script(f"""
                    // Look for hidden forms
                    var forms = document.querySelectorAll('form');
                    forms.forEach(function(form) {{
                        var inputs = form.querySelectorAll('input');
                        inputs.forEach(function(input) {{
                            if (input.name && input.name.includes('ip')) {{
                                input.value = '{new_ip}';
                            }}
                        }});
                    }});
                """)
                
                time.sleep(5)
                driver.quit()
                return True
            else:
                print(f"Error response: {result}")
            
            driver.quit()
            
        except Exception as e:
            print(f"Error with {browser_name}: {e}")
            continue
    
    print("\n❌ All browser automation attempts failed")
    print("\nPossible reasons:")
    print("1. Device firmware doesn't support IP changes")
    print("2. Browser driver not installed (Chrome/Firefox/Edge)")
    print("3. Device requires different authentication")
    
    print("\nManual alternative:")
    print(f"1. Open http://{current_ip} in Chrome")
    print("2. Press F12 for Developer Tools")
    print("3. Go to Console tab")
    print("4. Paste this command:")
    print(f"\nfetch('/api/webserver/SesTokInfo').then(r=>r.text()).then(t=>{{let s=t.match(/SessionID=([^<]+)/)[1],k=t.match(/TokInfo>([^<]+)/)[1];document.cookie='SessionID='+s;fetch('/api/dhcp/settings',{{method:'POST',headers:{{'__RequestVerificationToken':k,'Content-Type':'text/xml'}},body:'<?xml version=\"1.0\" encoding=\"UTF-8\"?><request><DhcpIPAddress>{new_ip}</DhcpIPAddress><DhcpLanNetmask>255.255.255.0</DhcpLanNetmask><DhcpStatus>1</DhcpStatus><DhcpStartIPAddress>{network}.100</DhcpStartIPAddress><DhcpEndIPAddress>{network}.200</DhcpEndIPAddress><DhcpLeaseTime>86400</DhcpLeaseTime></request>'}}).then(r=>alert(r.ok?'Success! Device will reboot to {new_ip}':'Failed'))}})")

if __name__ == "__main__":
    main()