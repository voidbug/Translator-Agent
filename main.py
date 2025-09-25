import sys
from argostranslate import package, translate
import tkinter as tk
from tkinter import ttk, messagebox

# 检查并安装中文-英文包（可按需更换）
def ensure_package_installed():
    # 下载并安装语言包（仅首次需联网，之后离线）
    import os
    pkg_dir = os.path.expanduser("~/.argos-translate/packages")
    if not os.path.exists(pkg_dir):
        os.makedirs(pkg_dir)
    available_packages = package.get_available_packages()
    for pkg in available_packages:
        if pkg.from_code == "zh" and pkg.to_code == "en":
            pkg.download()
            download_path = pkg.download()
            package.install_from_path(download_path)

# 初始化翻译包（首次联网，后续可离线使用）
ensure_package_installed()
installed_languages = translate.get_installed_languages()
zh = next((l for l in installed_languages if l.code == "zh"), None)
en = next((l for l in installed_languages if l.code == "en"), None)
translation = zh.get_translation(en) if zh and en else None

# 简易GUI
def translate_text():
    src_text = input_text.get("1.0", tk.END).strip()
    if not src_text:
        messagebox.showinfo("提示", "请输入需要翻译的内容。")
        return
    if translation:
        result = translation.translate(src_text)
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, result)
    else:
        messagebox.showerror("错误", "未找到合适的翻译包。")

root = tk.Tk()
root.title("Argos Translate 桌面翻译智能体")
root.geometry("400x300")

ttk.Label(root, text="中文 → 英文翻译").pack(pady=5)
input_text = tk.Text(root, height=6)
input_text.pack(fill=tk.BOTH, padx=10, pady=5)

ttk.Button(root, text="翻译", command=translate_text).pack(pady=5)
output_text = tk.Text(root, height=6)
output_text.pack(fill=tk.BOTH, padx=10, pady=5)

root.mainloop()
