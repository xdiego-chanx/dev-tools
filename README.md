# DevTools CLI  

**DevTools** is a simple CLI tool that generates pre-configured module structures (folders with template files) for various frameworks. Designed for personal use, it helps speed up project setup by automating repetitive scaffolding tasks.  

## 🚀 Features  
- 📂 Quickly generate framework-specific module structures  
- 📝 Pre-filled template files for consistency  
- ⚡ Fast and easy to use via CLI  

## 📌 Installation  
Using Python:  
```sh
pip install --editable .
```

## 🛠️ Usage  
Run the CLI and specify the framework/module you want to generate:  
```sh
devtools <framework> new module <module-name> <path> <...options>
```
Example:  
```sh
modulemaker nest new module users . --root
```
This will generate a `users` module with files pre-filled for NestJS, without making a separate folder for them.  

### Available Frameworks  
- `nestjs`  
- `react`  
- `aspnet`

## 📄 License  
MIT  

