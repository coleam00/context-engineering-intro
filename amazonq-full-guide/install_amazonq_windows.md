## Installing Amazon Q Developer on Windows (with WSL)

Amazon Q Developer CLI works best on Linux and MacOS. To use Amazon Q Developer with Windows, you can use WSL.

1. Go to the Microsoft Store

2. Search for Ubuntu WSL and install

3. Open WSL in a terminal

4. Run the following commands (this follows best security practices):

```bash
# First, save a list of your existing global packages for later migration
npm list -g --depth=0 > ~/npm-global-packages.txt

# Create a directory for your global packages
mkdir -p ~/.npm-global

# Configure npm to use the new directory path
npm config set prefix ~/.npm-global

# Note: Replace ~/.bashrc with ~/.zshrc, ~/.profile, or other appropriate file for your shell
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.bashrc

# Apply the new PATH setting
source ~/.bashrc

# Now install Amazon Q Developer CLI in the new location
npm install -g @aws/amazon-q-developer-cli
```

5. Now within your IDEs you can open a terminal with Ctrl + J (also use this hotkey to toggle it off) and you can click on the down arrow next to the plus to open an Ubuntu (WSL) terminal where you can run the "q" command to start Amazon Q Developer.