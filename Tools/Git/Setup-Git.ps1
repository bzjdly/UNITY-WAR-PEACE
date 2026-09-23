$ErrorActionPreference = "Stop"

$repoRoot = Resolve-Path (Join-Path $PSScriptRoot "..\..")
Push-Location $repoRoot

try {
    if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
        throw "Git is not installed or is not available on PATH."
    }

    git lfs install --local

    $mergeTool = $env:UNITY_YAML_MERGE
    if ([string]::IsNullOrWhiteSpace($mergeTool)) {
        $installRoots = @()
        $projectVersionPath = Join-Path $repoRoot "ProjectSettings\ProjectVersion.txt"

        if (Test-Path -LiteralPath $projectVersionPath) {
            $projectVersionLine = Get-Content $projectVersionPath |
                Where-Object { $_ -match "^m_EditorVersion:\s*(.+)$" } |
                Select-Object -First 1

            if ($projectVersionLine -match "^m_EditorVersion:\s*(.+)$") {
                $projectVersion = $Matches[1].Trim()
                $projectRegistryPath = "HKLM:\SOFTWARE\Unity Technologies\Installer\Unity $projectVersion"
                if (Test-Path $projectRegistryPath) {
                    $installRoots += (Get-ItemProperty $projectRegistryPath)."Location x64"
                }
            }
        }

        $installRoots += Get-ChildItem "HKLM:\SOFTWARE\Unity Technologies\Installer" `
            -ErrorAction SilentlyContinue |
            ForEach-Object {
                (Get-ItemProperty $_.PSPath -ErrorAction SilentlyContinue)."Location x64"
            }
        $installRoots = $installRoots |
            Where-Object { -not [string]::IsNullOrWhiteSpace($_) } |
            Select-Object -Unique

        foreach ($installRoot in $installRoots) {
            $candidate = Join-Path $installRoot "Editor\Data\Tools\UnityYAMLMerge.exe"
            if (Test-Path -LiteralPath $candidate) {
                $mergeTool = $candidate
                break
            }
        }
    }

    if ([string]::IsNullOrWhiteSpace($mergeTool) -or -not (Test-Path -LiteralPath $mergeTool)) {
        Write-Warning "UnityYAMLMerge.exe was not found. Git LFS is configured, but Unity SmartMerge is not."
        Write-Warning "Set UNITY_YAML_MERGE to the full UnityYAMLMerge.exe path and run this script again."
        exit 0
    }

    $mergeTool = (Resolve-Path -LiteralPath $mergeTool).Path.Replace("\", "/")
    $driverTemplate = '"{0}" merge -p %O %B %A %A'
    $driver = $driverTemplate.Replace("{0}", $mergeTool)

    git config merge.unityyamlmerge.name "Unity SmartMerge"
    git config merge.unityyamlmerge.driver $driver
    git config merge.unityyamlmerge.recursive binary

    Write-Host "Git LFS and Unity SmartMerge are configured."
    Write-Host "UnityYAMLMerge: $mergeTool"
}
finally {
    Pop-Location
}
