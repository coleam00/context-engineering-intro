## Installing Claude Code on Windows (with WSL)

Claude Code only supports Linux and MacOS by default. To use Claude Code with Windows, you can use WSL.

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

# Now reinstall Claude Code in the new location
npm install -g @anthropic-ai/claude-code
```

5. Now within your IDEs you can open a terminal with Ctrl + J (also use this hotkey to toggle it off) and you can click on the down arrow next to the plus to open an Ubuntu (WSL) terminal where you can run the "claude" command to start Claude Code.