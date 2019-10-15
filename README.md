# Text Generation

I came accross [this](https://towardsdatascience.com/writing-like-shakespeare-with-machine-learning-in-pytorch-d77f851d910c) article and descided to see if I could replicate it using a varity of different techniques.

# Prerequsits

The following packages need to be installed.
I recomend using [Chocolatey](https://chocolatey.org/install)

* [7-zip](https://www.7-zip.org/)
* [Python](https://www.python.org/downloads/windows/)
* [VS Code](https://code.visualstudio.com/Download) along with the below plugins
  * Python by Microsoft.
    Set the option Python >> Data Science: Send Selection To Interactive Window


```{ps1}
if('Unrestricted' -ne (Get-ExecutionPolicy)) { Set-ExecutionPolicy Bypass -Scope Process -Force }
iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
refreshenv

choco install python3  -y
choco install 7zip.install -y
choco install vscode -y
refreshenv

code --install-extension ms-python.python
```