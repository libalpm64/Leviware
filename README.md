# Leviware
A ransomware coded in python, bypasses all AV's and EDRs except Kaspersky. (If PYArmor is used)


This is a disastrous program. Do not run it on other people's computers (this isn't a joke and is also against the law). Don't even run it on your own computer; run it on a virtual machine.

Features:
- Not detected by AVs (for now)
- Supports a lot of file extensions
- Encrypts all users, not just the current user
- Includes a decryptor for it
- Discord webhook for keys
- Irreversible (meaning it’s impossible to use a tool to decrypt this without obtaining the private key)


Some Q/A:

How do I set this up?
Pack it into an executable with PyArmor.

Why is it named Leviware?
Leviware is based on a character called "Levi Kazama," a ninja with unique stealth capabilities who can evade attackers easily. Combine ransomware with "Levi" (her first name), and you get Leviware.

Is this detected by any antivirus?
Only Kaspersky caught it after it encrypts the downloads. However, it still encrypts everything on the desktop fine, so it is still dangerous. (This is not an advertisement for Kaspersky; it is likely to become detected by every AV as soon as someone tries using it maliciously.)

Why did you make this?
We conducted a lab simulation and did a mock trial to demonstrate how an incident response and forensics team would work together to investigate and convict someone. (I was found not guilty, as the incident response team, forensics, and sysadmin weren’t really experienced in their fields. They are now fully educated on this, I can assure you. Thanks, RJ!)
