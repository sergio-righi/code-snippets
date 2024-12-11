# Define applications and random words
$typingWords = @("automation", "random", "example", "PowerShell", "task", "text")

Add-Type @"
using System;
using System.Text;
using System.Runtime.InteropServices;

public class User32 {
    [DllImport("user32.dll")]
    public static extern IntPtr GetForegroundWindow();

    [DllImport("user32.dll", CharSet = CharSet.Auto, SetLastError = true)]
    public static extern int GetWindowText(IntPtr hWnd, StringBuilder lpString, int nMaxCount);
    
    [DllImport("user32.dll")]
    public static extern uint GetWindowThreadProcessId(IntPtr hWnd, out uint lpdwProcessId);
}
"@

Add-Type @"
using System;
using System.Runtime.InteropServices;
public class Win32 {
    [DllImport("user32.dll")]
    public static extern bool SetForegroundWindow(IntPtr hWnd);
}
"@

# Function to get the currently focused process
function Get-FocusedProcess {
    $hWnd = [User32]::GetForegroundWindow()
    $title = New-Object Text.StringBuilder 256
    [User32]::GetWindowText($hWnd, $title, $title.Capacity) | Out-Null

    # Initialize localPid to null or zero before passing by reference
    $localPid = 0
    [User32]::GetWindowThreadProcessId($hWnd, [ref]$localPid) | Out-Null

    try {
        $process = Get-Process -Id $localPid
        return [PSCustomObject]@{
            Title       = $title.ToString()
            ProcessName = "$($process.ProcessName).exe"
        }
    }
    catch {
        return [PSCustomObject]@{
            Title       = $title.ToString()
            ProcessName = "Unknown"
        }
    }
}

Function Switch-RandomApp {

  # Define target process names
  $targetProcesses = @("Opera.exe", "Code.exe")
  
  # Loop until the focused process matches one of the target processes
  do {
      # Simulate ALT + TAB
      [System.Windows.Forms.SendKeys]::SendWait("%{TAB}")

      # Delay to allow the target application to activate
      Start-Sleep -Milliseconds 1000

      # Retrieve the focused process
      $focusedProcess = Get-FocusedProcess
      Write-Host "Window Title: $($focusedProcess.Title)"
      Write-Host "Process Name: $($focusedProcess.ProcessName)"

  } while (-not $targetProcesses.Contains($focusedProcess.ProcessName))

  Write-Host "Focused on target process: $($focusedProcess.ProcessName)"
}

Function Open-Or-Focus-Notepad {
  Write-Host "Opening Notepad if not already running..."

  # Check if Notepad is already open
  $notepadProcesses = Get-Process -Name "notepad" -ErrorAction SilentlyContinue
  if ($notepadProcesses -eq $null) {
      # Start Notepad if it's not running
      Start-Process "notepad.exe"
      Start-Sleep -Seconds 2
      $notepadProcesses = Get-Process -Name "notepad" | Where-Object { $_.MainWindowHandle -ne 0 }
  }

  # Select the first Notepad process with a valid window handle
  $notepad = $notepadProcesses | Where-Object { $_.MainWindowHandle -ne 0 } | Select-Object -First 1

  # Bring Notepad to the foreground
  if ($notepad) {
      [Win32]::SetForegroundWindow($notepad.MainWindowHandle)
  }
  else {
      Write-Host "Failed to bring Notepad to the foreground."
  }

  return $notepad
}

Function TypeInNotepad {
  $notepad = Open-Or-Focus-Notepad

  # Ensure Notepad is focused
  if ($notepad) {
        # Simulate more human-like typing with relevant phrases
        $sentencePatterns = @(
            "Writing a GlideAjax call for {0}.",
            "Debugging a {0} issue in ServiceNow.",
            "Refactoring a script include to optimize {0}.",
            "Testing the JavaScript code for {0}.",
            "Implementing a new business rule for {0}.",
            "Analyzing a workflow for {0} improvements.",
            "Creating a UI script for enhanced {0}.",
            "Developing a custom widget for {0} in the Service Portal.",
            "Integrating REST APIs for {0}.",
            "Exploring how to improve {0} performance in ServiceNow."
        )

      $sentence = Get-Random -InputObject $sentencePatterns -Count 1
      $word = Get-Random -InputObject $typingWords
      $typedText = $sentence -f $word

      foreach ($char in $typedText.ToCharArray()) {
          [System.Windows.Forms.SendKeys]::SendWait($char)
          Start-Sleep -Milliseconds (Get-Random -Minimum 50 -Maximum 150) # Simulate typing speed
      }

      [System.Windows.Forms.SendKeys]::SendWait("{ENTER}")
      Write-Host "Typed: $typedText"
  }
}

# Load the SendKeys functionality
Add-Type -AssemblyName System.Windows.Forms

# Main loop
while ($true) {
    $action = Get-Random -Minimum 1 -Maximum 3
    switch ($action) {
        1 { Switch-RandomApp }      # Switch to a random app
        2 { TypeInNotepad }         # Type in Notepad (open it if necessary)
    }
    Start-Sleep -Seconds (Get-Random -Minimum 10 -Maximum 30) # Random delay
}
