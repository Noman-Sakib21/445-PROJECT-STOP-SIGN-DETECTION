param([string]$OutFile)

Add-Type -AssemblyName System.Windows.Forms
$f = New-Object System.Windows.Forms.OpenFileDialog
$f.Title = 'Select an image to test'
$f.Filter = 'Images (*.jpg;*.jpeg;*.png;*.bmp)|*.jpg;*.jpeg;*.png;*.bmp|All files (*.*)|*.*'
$f.InitialDirectory = [Environment]::GetFolderPath('Desktop')
if ($f.ShowDialog() -eq [System.Windows.Forms.DialogResult]::OK) {
    [System.IO.File]::WriteAllText($OutFile, $f.FileName)
}
