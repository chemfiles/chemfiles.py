if ("$env:CXX_PATH" -ne "") {
    $env:PATH += ";$env:CXX_PATH"
}

if ($env:generator -eq "MinGW Makefiles") {
    # Remove sh.exe from git in the PATH for MinGW to work
    $env:PATH = ($env:PATH.Split(';') | Where-Object { $_ -ne 'C:\Program Files\Git\usr\bin' }) -join ';'
}

$env:CMAKE_ARGUMENTS = "-G `"$env:generator`""
$env:CMAKE_ARGUMENTS += " -DCMAKE_BUILD_TYPE=$env:configuration"

if ($env:generator -Match "Visual Studio") {
    $env:BUILD_ARGUMENTS="/verbosity:minimal"
} else {
    $env:BUILD_ARGUMENTS=""
}

if ($env:ARCH -eq "x64") {
    # Use 64-bit python
    $env:PATH = "C:\Python27-x64;C:\Python27-x64\Scripts;" + $env:PATH
}
