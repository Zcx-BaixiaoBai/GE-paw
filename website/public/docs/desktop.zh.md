# gepaw Desktop ?

>  **Beta **
>
>  Beta 
>
> - ****?
> - ****?
> - ****
> - **?*?
>
> ?

****[GitHub Releases][releases]

 Windows ?macOS  gepaw Desktop ?

[releases]: https://gepaw.agentscope.io/downloads

## 

**10-60?*  Python ?Web ?

## 

- [Windows ](#windows-)
- [macOS ](#macos-)
- [](#?

---

## Windows 

### 

- ****: Windows 10 ?
- ****: x64 (64?

### 

1. **?*
   ?[Release ][releases] `gepaw-Setup-<version>.exe` 

2. ****
    `.exe` ?
   - `C:\Users\<?\AppData\Local\gepaw`
   - ?

### 

****?

#### **gepaw Desktop** ()

- ****: ?
- ****: ?
- ****:  "gepaw Desktop" 
- **?*:  VBScript  Python 

#### **gepaw Desktop (Debug)** ()

- ****: ?
- ****:
  - ?
  - ?
  -  Bug ?
- ****:  "gepaw Desktop (Debug)" 
- ****:
  - 
  - Python 
  - API 
  - ?Ctrl+C 

### 

**Q: ?*

A: ?**Microsoft WebView2**  Windows 10 ?

[Microsoft WebView2](https://developer.microsoft.com/en-us/microsoft-edge/webview2/)
?

**Q: **

A:  "gepaw Desktop (Debug)" 

**Q: ?*

A: ?Windows  ? ? ? "gepaw Desktop" ?

**Q: **

A: ?**Microsoft **?$200-800/Windows Defender SmartScreen ?
?"" ?"" 
?GitHub Actions 

---

## macOS 

### 

- ****: macOS 14 (Sonoma) ?
- ****:
  - ?**Apple Silicon (M1/M2/M3/M4)** - 
  -  Intel  - ?

### 

1. **?*
   ?[Release ][releases] `gepaw-<version>-macOS.zip` 

2. **?*
    `.zip` ?`gepaw.app` 

3. ** (?**
   ?`gepaw.app`  `/Applications` ?

### ?

#### 

gepaw **?Apple Notarization?*macOS Gatekeeper ?

****

-  

**?*

- ?**?*?
-  ****
-  **?*CI/CD?

#### ?

####  1 ()

1. **** Control + `gepaw.app`
2.  **""**
3. ?**""** 
4. ?

####  2?

?

1.  ** ??*
2. 
   _"?'gepaw'?_
3.  **""** ?**""** 
4. ?

####  3?

```bash
# ?
xattr -cr /Applications/gepaw.app
```

 ****: ?

###  

macOS 

- ****
  
  -  **""** ?
  -  **"?** 

### 

#### 

-  `gepaw.app` 
- ?
- `~/.gepaw/desktop.log`

#### 



```bash
# ?
cd /Applications  # ?gepaw.app ?

# 
APP_ENV="$(pwd)/gepaw.app/Contents/Resources/env"
PYTHONNOUSERSITE=1 PYTHONPATH= PYTHONHOME="$APP_ENV" "$APP_ENV/bin/python" -m gepaw desktop
```

****

- ??
- ??Python 
- ??
- ??`--log-level debug` ?

**?*

```bash
# 
tail -f ~/.gepaw/desktop.log
```

### 

**Q: **

A: 

1. ?`~/.gepaw/desktop.log` 
2. ?

**Q: "Apple ??*

A: ""

**Q: ?*

A: ?`gepaw.app`  `~/.gepaw` ?

**Q: Intel Mac ?*
A: ?

**Q: **

A: 

- ?****?GitHub
- ?**CI/CD ?*GitHub Actions ?
- ?****
- ?**?*

---

## ?

- **GitHub Issues**: [](https://github.com/agentscope-ai/gepaw/issues)
- ****: `scripts/pack/README.md` - 
- ****:
  - Windows: Debug  `%USERPROFILE%\.gepaw\` 
  - macOS: `~/.gepaw/desktop.log`

---

## 

### Windows 

- ****: ?
- ****: ?Debug ?

### macOS 

- ****: ""
- ****: 
- ****: 
