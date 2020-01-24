# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['run.py'],
             pathex=['C:\\Users\\flore\\Documents\\Python Scripts\\MCOCScript'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

a.datas += [('help-button.png' , 'images\\help-button.png', "DATA"),
('empty-slot-bottom' , 'images\\empty-slot-bottom.png', "DATA"),
('accept' , 'images\\accept.png', "DATA"),
('continue' , 'images\\continue.png', "DATA"),
('end-match' , 'images\\end-match.png', "DATA"),
('final-fight' , 'images\\final-fight.png', "DATA"),
('find-match' , 'images\\find-match.png', "DATA"),
('next-fight' , 'images\\next-fight.png', "DATA"),
('next-series' , 'images\\next-series.png', "DATA"),
('pause' , 'images\\pause.png', "DATA"),
('exit' , 'images\\exit.png', "DATA"),
('find-match-free' , 'images\\find-match-free.png', "DATA"),
('find-match-2000' , 'images\\find-match-2000.png', "DATA"),
('info' , 'images\\info.png', "DATA")]



exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='run',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False )
