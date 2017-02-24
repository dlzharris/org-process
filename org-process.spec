# -*- mode: python -*-

block_cipher = None

a = Analysis(['src\\org-process.py'],
             pathex=['C:\\code\\projects\\org-process\\src'],
             binaries=None,
             datas=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='org-process',
          debug=False,
          strip=False,
          upx=True,
          console=False )

# coll = COLLECT(exe,
#                a.binaries,
#                a.zipfiles,
#                a.datas,
#                strip=False,
#                upx=True,
#                name='org-process')

