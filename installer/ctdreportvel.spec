# from https://chriskiehl.com/article/packaging-gooey-with-pyinstaller

import gooey
gooey_root = os.path.dirname(gooey.__file__)
gooey_languages = Tree(os.path.join(gooey_root, 'languages'), prefix = 'gooey/languages')
gooey_images = Tree(os.path.join(gooey_root, 'images'), prefix = 'gooey/images')
a = Analysis(['C:\\Users\\patrice.ponchant\\Documents\\GitHub\\ctdreport-vel\\src\\ctdreportvel\\ctdreportvel.py'],
             pathex=['C:\\Users\\patrice.ponchant\\Documents\\GitHub\\ctdreport-vel\\src\\ctdreportvel'],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             )
pyz = PYZ(a.pure)

options = [('u', None, 'OPTION'), ('u', None, 'OPTION'), ('u', None, 'OPTION')]

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          options,
          gooey_languages, # Add them in to collected files
          gooey_images, # Same here.
          name='ctdreportvel',
          debug=False,
          strip=None,
          upx=True,
          console=False,
          windowed=True,
          icon=os.path.join(gooey_root, 'images', 'program_icon.ico'))